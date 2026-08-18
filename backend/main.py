from fastapi import FastAPI, Depends, HTTPException, status, Response, Request, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import List
import os
import pickle
import base64
import yaml
import subprocess
import time
import jinja2
from lxml import etree

from . import database, models, auth
from .labs.config import LABS, CHALLENGES

app = FastAPI(
    title="SecureShop Lab API",
    description="An intentionally secure application for cybersecurity education."
)

# Mount frontend files
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


# =========================
# CORS CONFIGURATION
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Local development
        "http://127.0.0.1:5500",
        "http://localhost:5500",

        # Vercel production frontend
        "https://secure-shop-cybersecurity-lab.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/login"
)


@app.on_event("startup")
def startup_event():
    database.init_db()


# =========================
# AUTHENTICATION
# =========================

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validates JWT and retrieves current user."""

    payload = auth.decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username: str = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    users = database.execute_read_query(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    if not users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return users[0]


# =========================
# REGISTER
# =========================

@app.post("/api/register", status_code=status.HTTP_201_CREATED)
def register(user: models.UserCreate):

    existing = database.execute_read_query(
        "SELECT id FROM users WHERE username = ? OR email = ?",
        (user.username, user.email)
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )

    hashed_password = auth.get_password_hash(user.password)

    user_id = database.execute_write_query(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (
            user.username,
            user.email,
            hashed_password
        )
    )

    if not user_id:
        raise HTTPException(
            status_code=500,
            detail="Database error during registration"
        )

    return {
        "message": "User created successfully"
    }


# =========================
# LOGIN
# =========================

@app.post("/api/login", response_model=models.Token)
def login(form_data: models.UserLogin):

    users = database.execute_read_query(
        "SELECT * FROM users WHERE username = ?",
        (form_data.username,)
    )

    if not users or not auth.verify_password(
        form_data.password,
        users[0]["password_hash"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = auth.create_access_token(
        data={"sub": users[0]["username"]},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================
# PRODUCTS
# =========================

@app.get(
    "/api/products",
    response_model=List[models.ProductResponse]
)
def get_products(response: Response):
    # CTF FLAG: Information Disclosure in Headers
    response.headers["X-Flag"] = "flag{headers_leak_info}"
    response.headers["X-Admin-Portal"] = "/admin_hidden_login"

    products = database.execute_read_query(
        "SELECT * FROM products"
    )

    return products


@app.get(
    "/api/products/search",
    response_model=List[models.ProductResponse]
)
def search_products(q: str):

    query = """
        SELECT * FROM products
        WHERE name LIKE ? OR description LIKE ?
    """

    search_term = f"%{q}%"

    products = database.execute_read_query(
        query,
        (search_term, search_term)
    )

    return products

@app.get(
    "/api/products/search/vulnerable",
)
def search_products_vulnerable(q: str):
    """
    INTENTIONALLY VULNERABLE ENDPOINT FOR CTF
    Do not use parameterized queries here!
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    # Intentionally vulnerable to SQLi
    query = f"SELECT * FROM products WHERE name LIKE '%{q}%' OR description LIKE '%{q}%'"
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        products = [dict(row) for row in rows]
        
        # If they successfully injected ' OR 1=1 --, they get all products. 
        # Let's give them the flag if they return all products via injection,
        # or if they explicitly have ' OR in the query.
        if "' OR" in q.upper() or "' UNION" in q.upper():
            products.append({"id": 999, "name": "FLAG", "description": "flag{sqli_union_master}", "price": 0, "stock": 1})
            
        return products
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()


# =========================
# USER PROFILE
# =========================

@app.get("/api/users/me")
def read_users_me(
    current_user: dict = Depends(get_current_user)
):

    stats = database.execute_read_query(
        "SELECT SUM(xp_awarded) as total_xp, COUNT(id) as total_completed FROM user_challenges WHERE user_id = ?",
        (current_user["id"],)
    )
    
    total_xp = stats[0]["total_xp"] if stats and stats[0]["total_xp"] else 0
    total_completed = stats[0]["total_completed"] if stats and stats[0]["total_completed"] else 0

    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "email": current_user["email"],
        "total_xp": total_xp,
        "completed_challenges": total_completed
    }

@app.get("/api/leaderboard")
def get_leaderboard():
    query = """
        SELECT u.username, u.role, 
               COALESCE(SUM(uc.xp_awarded), 0) as total_xp, 
               COUNT(uc.id) as challenges_completed
        FROM users u
        LEFT JOIN user_challenges uc ON u.id = uc.user_id
        GROUP BY u.id
        ORDER BY total_xp DESC
        LIMIT 50
    """
    results = database.execute_read_query(query)
    # Ensure values are integers
    for r in results:
        r["total_xp"] = int(r["total_xp"]) if r["total_xp"] else 0
        r["challenges_completed"] = int(r["challenges_completed"]) if r["challenges_completed"] else 0
    return results


# =========================
# ORDERS
# =========================

@app.post(
    "/api/orders",
    status_code=status.HTTP_201_CREATED
)
def create_order(
    order: models.OrderCreate,
    current_user: dict = Depends(get_current_user)
):

    products = database.execute_read_query(
        "SELECT * FROM products WHERE id = ?",
        (order.product_id,)
    )

    if not products:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    order_id = database.execute_write_query(
        """
        INSERT INTO orders
        (user_id, product_id, quantity)
        VALUES (?, ?, ?)
        """,
        (
            current_user["id"],
            order.product_id,
            order.quantity
        )
    )

    return {
        "message": "Order placed",
        "order_id": order_id
    }


@app.get(
    "/api/orders",
    response_model=List[models.OrderResponse]
)
def get_user_orders(
    current_user: dict = Depends(get_current_user)
):

    orders = database.execute_read_query(
        "SELECT * FROM orders WHERE user_id = ?",
        (current_user["id"],)
    )

    return orders


@app.delete(
    "/api/orders",
    status_code=status.HTTP_200_OK
)
def clear_user_orders(
    current_user: dict = Depends(get_current_user)
):

    database.execute_write_query(
        "DELETE FROM orders WHERE user_id = ?",
        (current_user["id"],)
    )

    return {"message": "Order history cleared"}


@app.get(
    "/api/orders/{order_id}",
    response_model=models.OrderResponse
)
def get_order(
    order_id: int,
    current_user: dict = Depends(get_current_user)
):

    orders = database.execute_read_query(
        "SELECT * FROM orders WHERE id = ?",
        (order_id,)
    )

    if not orders:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order = orders[0]

    # INTENTIONAL VULNERABILITY: IDOR
    # The authorization check has been "commented out" by a lazy developer.
    # if (
    #     order["user_id"] != current_user["id"]
    #     and current_user["role"] != "admin"
    # ):
    #     raise HTTPException(
    #         status_code=404,
    #         detail="Order not found"
    #     )
    
    # If they successfully access order ID 1 (which shouldn't belong to them)
    if order_id == 1 and current_user["id"] != 1:
        # We inject the flag into the response status
        order["status"] = "flag{idor_access_granted}"

    return order


# =========================
# REVIEWS
# =========================

@app.post(
    "/api/reviews",
    status_code=status.HTTP_201_CREATED
)
def create_review(
    review: models.ReviewCreate,
    current_user: dict = Depends(get_current_user)
):

    review_id = database.execute_write_query(
        """
        INSERT INTO reviews
        (user_id, product_id, rating, comment)
        VALUES (?, ?, ?, ?)
        """,
        (
            current_user["id"],
            review.product_id,
            review.rating,
            review.comment
        )
    )

    return {
        "message": "Review added",
        "review_id": review_id
    }


@app.get(
    "/api/reviews/{product_id}",
    response_model=List[models.ReviewResponse]
)
def get_product_reviews(product_id: int):

    reviews = database.execute_read_query(
        "SELECT * FROM reviews WHERE product_id = ?",
        (product_id,)
    )

    return reviews

# =========================
# PLATFORM CTF ENDPOINTS
# =========================

oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/login", auto_error=False)

@app.get("/api/labs", response_model=List[models.LabConfig])
def get_labs(token: str = Depends(oauth2_scheme_optional)):
    user_id = None
    try:
        user = get_current_user(token)
        user_id = user["id"]
    except:
        pass

    result = []
    for l in LABS:
        lab_data = l.copy()
        lab_data["completed_challenges"] = 0
        lab_data["progress_percentage"] = 0
        
        if user_id:
            completed = database.execute_read_query(
                "SELECT challenge_id FROM user_challenges WHERE user_id = ? AND lab_id = ?",
                (user_id, l["id"])
            )
            lab_data["completed_challenges"] = len(completed)
            if l["challenges_count"] > 0:
                lab_data["progress_percentage"] = int((len(completed) / l["challenges_count"]) * 100)
                
        result.append(lab_data)
        
    return result

@app.get("/api/challenges", response_model=List[models.Challenge])
def get_challenges(
    lab_id: str,
    token: str = Depends(oauth2_scheme_optional)
):
    if lab_id not in CHALLENGES:
        raise HTTPException(status_code=404, detail="Lab not found")

    user_id = None
    try:
        user = get_current_user(token)
        user_id = user["id"]
    except:
        pass
        
    completed_ids = []
    if user_id:
        completed = database.execute_read_query(
            "SELECT challenge_id FROM user_challenges WHERE user_id = ? AND lab_id = ?",
            (user_id, lab_id)
        )
        completed_ids = [c["challenge_id"] for c in completed]

    result = []
    for c in CHALLENGES[lab_id]:
        challenge = c.copy()
        challenge.pop("flag", None)
        challenge.pop("badge", None)
        challenge["completed"] = challenge["id"] in completed_ids
        result.append(challenge)
        
    return result

@app.post("/api/challenges/submit", response_model=models.ChallengeResponse)
def submit_flag(
    submit: models.ChallengeSubmit,
    current_user: dict = Depends(get_current_user)
):
    if submit.lab_id not in CHALLENGES:
        raise HTTPException(status_code=404, detail="Lab not found")
        
    challenge = next((c for c in CHALLENGES[submit.lab_id] if c["id"] == submit.challenge_id), None)
    
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
        
    if submit.flag.strip() == challenge["flag"]:
        # Record completion
        try:
            database.execute_write_query(
                "INSERT INTO user_challenges (user_id, lab_id, challenge_id, xp_awarded) VALUES (?, ?, ?, ?)",
                (current_user["id"], submit.lab_id, challenge["id"], challenge["xp"])
            )
            return {
                "success": True,
                "message": f"Flag accepted! Challenge completed. +{challenge['xp']} XP",
                "xp_awarded": challenge["xp"],
                "badge_awarded": challenge.get("badge")
            }
        except Exception as e:
            # UNIQUE constraint failed = Already completed
            return {
                "success": True,
                "message": "Flag accepted! (You have already completed this challenge)",
                "xp_awarded": 0,
                "badge_awarded": None
            }
    else:
        return {
            "success": False,
            "message": "Incorrect flag.",
            "xp_awarded": 0,
            "badge_awarded": None
        }

# =========================
# VULNERABLE LAB TARGETS 
# =========================

# --- SQL INJECTION LAB ---
@app.get("/api/labs/sqli/search")
def sqli_lab_search(q: str = ""):
    """INTENTIONALLY VULNERABLE ENDPOINT"""
    conn = database.get_db_connection()
    cursor = conn.cursor()
    # Vulnerable to UNION injection
    query = f"SELECT id, name, description FROM products WHERE name LIKE '%{q}%'"
    try:
        cursor.execute(query)
        rows = [dict(row) for row in cursor.fetchall()]
        
        flags = []
        
        # 1. Blind SQLi Concept
        if "1=1" in q or "1=2" in q or "true" in q.lower():
            flags.append("flag{sqli_blind_concept}")
            
        # 2. UNION Version
        if "' UNION" in q.upper() and "sqlite_version" in q.lower():
            flags.append("flag{sqli_union_version}")
            
        # 3. Data Extraction
        if "super_secret" in q.lower() and "' UNION" in q.upper():
            flags.append("flag{sqli_data_extraction}")
            rows.append({"id": 999, "name": "super_secret", "description": "Here is the data extraction flag: flag{sqli_data_extraction}"})
            
        if flags:
            return {"results": rows, "flags": flags, "message": "Multiple flags unlocked!" if len(flags)>1 else "Flag unlocked!"}
            
        return {"results": rows}
    except Exception as e:
        # If the input caused a SQL error and contained a quote, they found the basic injection vector!
        if "'" in q:
            return {"error": str(e), "hint": "Check your syntax near the quote.", "flag": "flag{sqli_basic_error}"}
        return {"error": str(e), "hint": "Check your syntax near the quote."}
    finally:
        conn.close()

@app.post("/api/labs/sqli/login")
def sqli_lab_login(username: str):
    """INTENTIONALLY VULNERABLE ENDPOINT"""
    conn = database.get_db_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = 'password123'"
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            return {"success": True, "flag": "flag{sqli_auth_bypass}"}
        return {"success": False}
    except Exception:
        return {"success": False}
    finally:
        conn.close()

# --- XSS LAB ---
@app.get("/api/labs/xss/search")
def xss_lab_search(response: Response, q: str = ""):
    """INTENTIONALLY VULNERABLE ENDPOINT - Reflected XSS"""
    # The flag is awarded simply if they inject a script tag, simulating reflection.
    # We return the flag in headers if they successfully pass a <script> payload.
    if "<script>" in q.lower():
        response.headers["X-Flag-XSS-1"] = "flag{xss_reflected_basic}"
    return {"message": f"Search results for: {q}"}

# Memory store for stored XSS simulation
xss_comments = []

@app.post("/api/labs/xss/comment")
def xss_lab_comment(comment: str):
    """INTENTIONALLY VULNERABLE ENDPOINT - Stored XSS"""
    xss_comments.append(comment)
    flag = None
    if "<script>" in comment.lower() or "javascript:" in comment.lower():
        flag = "flag{xss_stored_persistent}"
    return {"success": True, "comments_count": len(xss_comments), "flag": flag}

@app.get("/api/labs/xss/profile")
def xss_lab_profile(name: str = ""):
    """INTENTIONALLY VULNERABLE ENDPOINT - Context-aware XSS"""
    flag = None
    # To bypass an attribute context (e.g., <input value="... ">), you need ">
    # followed by a script payload or an event handler (e.g. " onmouseover="alert(1)")
    if ('"' in name or "'" in name) and (">" in name or "onmouseover" in name.lower() or "onerror" in name.lower()):
        flag = "flag{xss_context_attribute}"
    
    html_snippet = f'<input type="text" name="username" value="{name}">'
    return {"html_snippet": html_snippet, "flag": flag}

# --- AUTHENTICATION LAB ---
@app.post("/api/labs/auth/login")
def auth_lab_login(user: models.UserLogin):
    """INTENTIONALLY VULNERABLE ENDPOINT - Weak Password"""
    if user.username == "admin" and user.password == "admin123":
        return {"success": True, "flag": "flag{auth_weak_password}"}
    return {"success": False, "message": "Invalid credentials"}

from fastapi import Request
import base64
import json

@app.get("/api/labs/auth/verify_token")
def auth_lab_verify_token(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - JWT None Algorithm"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    
    token = auth_header.split(" ")[1]
    parts = token.split(".")
    
    if len(parts) < 2:
        raise HTTPException(status_code=400, detail="Invalid token format")
        
    try:
        # Decode without verification to simulate "alg: none" bypass
        header = json.loads(base64.urlsafe_b64decode(parts[0] + "==").decode())
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + "==").decode())
        
        if header.get("alg", "").lower() == "none" and payload.get("role") == "admin":
            return {"success": True, "flag": "flag{auth_jwt_none_alg}"}
            
        return {"success": False, "message": "Token verified, but not an admin or alg is not none."}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error decoding token")

@app.post("/api/labs/auth/reset_password")
def auth_lab_reset_password(data: models.PasswordReset):
    """INTENTIONALLY VULNERABLE ENDPOINT - Insecure Password Reset"""
    # Flaw: The API trusts the email provided by the user in the payload
    if data.username == "admin" and data.email != "admin@secureshop.local" and "@" in data.email:
        return {"success": True, "message": f"Password reset link sent to {data.email}", "flag": "flag{auth_insecure_reset}"}
    return {"success": True, "message": f"Password reset link sent to {data.email}"}

# --- API SECURITY LAB ---
@app.get("/api/labs/api/users/{user_id}")
def api_lab_get_user(user_id: int, current_user: dict = Depends(get_current_user)):
    """INTENTIONALLY VULNERABLE ENDPOINT - BOLA / IDOR"""
    # Flaw: Does not check if the requested user_id matches the current_user's ID
    if user_id == 1: # Assuming user 1 is admin
        return {"id": 1, "username": "admin", "email": "admin@secureshop.local", "role": "admin", "flag": "flag{api_bola_access}"}
    return {"id": user_id, "message": "User data"}

@app.put("/api/labs/api/profile")
def api_lab_update_profile(profile: models.ProfileUpdate, current_user: dict = Depends(get_current_user)):
    """INTENTIONALLY VULNERABLE ENDPOINT - Mass Assignment"""
    # Flaw: Blindly accepts the "role" parameter
    if profile.role == "admin":
        return {"success": True, "message": "Profile updated successfully.", "role": "admin", "flag": "flag{api_mass_assignment}"}
    return {"success": True, "message": "Profile updated successfully.", "role": "user"}

@app.get("/api/labs/api/v0/debug")
def api_lab_v0_debug():
    """INTENTIONALLY VULNERABLE ENDPOINT - Improper Asset Management"""
    # Flaw: An unauthenticated legacy debug endpoint was left active
    return {
        "status": "legacy_debug_active",
        "system_info": "Ubuntu 22.04 LTS, Python 3.10",
        "db_connection": "sqlite:///secureshop.db",
        "flag": "flag{api_improper_assets}"
    }

# --- AUTHORIZATION LAB ---
@app.get("/api/labs/authz/admin_panel")
def authz_admin_panel(current_user: dict = Depends(get_current_user)):
    """INTENTIONALLY VULNERABLE ENDPOINT - Missing Function Level Access Control"""
    # Flaw: No check for current_user['role'] == 'admin'
    return {"message": "Welcome to the secret admin panel!", "flag": "flag{authz_missing_flac}"}

@app.put("/api/labs/authz/tickets/{ticket_id}")
def authz_update_ticket(ticket_id: int, ticket: models.TicketUpdate, current_user: dict = Depends(get_current_user)):
    """INTENTIONALLY VULNERABLE ENDPOINT - IDOR Modification"""
    # Flaw: Does not check if the ticket belongs to the current user
    if ticket_id == 1: # Admin's ticket
        return {"success": True, "message": "Admin ticket updated!", "flag": "flag{authz_idor_modification}"}
    return {"success": True, "message": f"Ticket {ticket_id} updated!"}

@app.post("/api/labs/authz/checkout")
def authz_checkout(cart: models.Checkout, current_user: dict = Depends(get_current_user)):
    """INTENTIONALLY VULNERABLE ENDPOINT - Parameter Tampering"""
    # Flaw: Trusts the total_price parameter sent by the client
    if cart.total_price <= 0:
        return {"success": True, "message": "Order placed for free!", "flag": "flag{authz_param_tampering}"}
    return {"success": True, "message": f"Order placed for ${cart.total_price}!"}

# --- BROWSER SECURITY LAB ---
from fastapi.responses import RedirectResponse

@app.get("/api/labs/browser/redirect")
def browser_redirect(url: str = ""):
    """INTENTIONALLY VULNERABLE ENDPOINT - Open Redirect"""
    if "evil.com" in url.lower() or "hacker" in url.lower():
        return {"success": True, "flag": "flag{browser_open_redirect}", "redirect_to": url}
    return RedirectResponse(url="/" if not url else url)

@app.get("/api/labs/browser/cors_data")
def browser_cors_data(request: Request, response: Response):
    """INTENTIONALLY VULNERABLE ENDPOINT - CORS Misconfiguration"""
    origin = request.headers.get("Origin")
    if origin:
        # Flaw: Improperly reflects any origin
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        if "evil.com" in origin.lower() or "hacker" in origin.lower():
            return {"secret_data": "This is sensitive user data.", "flag": "flag{browser_cors_misconfig}"}
    return {"secret_data": "This is sensitive user data."}

@app.post("/api/labs/browser/update_email")
def browser_update_email(data: models.EmailUpdate, current_user: dict = Depends(get_current_user)):
    """INTENTIONALLY VULNERABLE ENDPOINT - CSRF"""
    # Flaw: Does not validate data.csrf_token, relies solely on Bearer token (simulating cookie auth)
    if "evil.com" in data.email or "hacker" in data.email:
        return {"success": True, "message": "Email updated without CSRF token!", "flag": "flag{browser_csrf_bypass}"}
    return {"success": True, "message": f"Email updated to {data.email}."}

# --- NETWORK SECURITY LAB ---
import urllib.request
import urllib.error

@app.post("/api/labs/network/fetch")
def network_ssrf_fetch(data: models.FetchRequest):
    """INTENTIONALLY VULNERABLE ENDPOINT - SSRF"""
    # Flaw: No validation on the URL being fetched
    try:
        req = urllib.request.Request(data.url)
        with urllib.request.urlopen(req, timeout=3) as response:
            content = response.read().decode('utf-8')
            return {"success": True, "content": content}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/labs/network/internal/secret")
def network_internal_secret(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - SSRF Target"""
    # This endpoint is supposed to be internal only
    client_host = request.client.host
    if client_host in ["127.0.0.1", "::1", "localhost"]:
        return {"success": True, "secret": "Super secret internal data", "flag": "flag{network_ssrf_internal}"}
    raise HTTPException(status_code=403, detail="Forbidden: Internal access only")

@app.get("/api/labs/network/ping")
def network_ping(host: str = "127.0.0.1"):
    """INTENTIONALLY VULNERABLE ENDPOINT - Command Injection"""
    # Flaw: Blindly concatenating user input into a command string
    # We simulate the execution for safety
    import re
    if re.search(r'[;&|]\s*(whoami|ls|cat|id)', host.lower()):
        return {"success": True, "output": f"PING {host}\n...\nroot\n", "flag": "flag{network_command_injection}"}
    return {"success": True, "output": f"PING {host}\n64 bytes from {host}: icmp_seq=1 ttl=64 time=0.042 ms"}

@app.post("/api/labs/network/reset_password")
def network_host_header_injection(data: models.PasswordReset, request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - Host Header Injection"""
    # Flaw: Using the Host header to generate a password reset link
    host_header = request.headers.get("Host", "")
    reset_link = f"http://{host_header}/reset?token=12345"
    
    flag = None
    if "evil.com" in host_header.lower() or "hacker" in host_header.lower():
        flag = "flag{network_host_header}"
        
    return {"success": True, "message": f"Password reset link generated: {reset_link}", "flag": flag}

# --- CRYPTOGRAPHY LAB ---
import random
import hashlib

@app.get("/api/labs/crypto/lottery")
def crypto_lottery(guess: int = 0):
    """INTENTIONALLY VULNERABLE ENDPOINT - Weak RNG"""
    # Flaw: Uses a predictable, weak pseudo-random number generator
    random.seed(42) # Hardcoded seed makes it completely predictable
    winning_number = random.randint(1, 1000)
    if guess == winning_number:
        return {"success": True, "message": "You won the lottery!", "flag": "flag{crypto_weak_rng}"}
    return {"success": False, "message": f"Wrong guess. The winning number was {winning_number}."}

@app.post("/api/labs/crypto/hash")
def crypto_hash(data: models.HashRequest):
    """INTENTIONALLY VULNERABLE ENDPOINT - Insecure Hashing"""
    # Flaw: Uses MD5 which is vulnerable to collision attacks
    if hashlib.md5(data.data.encode()).hexdigest() == data.hash:
        return {"success": True, "message": "Hash matched!", "flag": "flag{crypto_md5_collision}"}
    return {"success": False, "message": "Hash mismatch!"}

@app.get("/api/labs/crypto/encryption_key")
def crypto_key(response: Response):
    """INTENTIONALLY VULNERABLE ENDPOINT - Hardcoded Secrets"""
    # Flaw: Developer accidentally left the key in the headers
    response.headers["X-Encryption-Key"] = "SuperSecretKey123!"
    return {"success": True, "message": "API is functioning normally.", "flag": "flag{crypto_hardcoded_key}"}

# --- BUSINESS LOGIC LAB ---
import time

coupon_uses = {}

@app.get("/api/labs/logic/apply_coupon")
def logic_apply_coupon(code: str, current_user: dict = Depends(get_current_user)):
    """INTENTIONALLY VULNERABLE ENDPOINT - Coupon Code Abuse"""
    user_id = str(current_user['id'])
    if code == "SAVE10":
        uses = coupon_uses.get(user_id, 0)
        coupon_uses[user_id] = uses + 1
        if uses >= 3:
            return {"success": True, "message": "Coupon applied successfully. Balance is negative!", "flag": "flag{logic_coupon_abuse}"}
        return {"success": True, "message": f"Coupon applied. Uses: {uses + 1}"}
    return {"success": False, "message": "Invalid coupon"}

@app.post("/api/labs/logic/cart")
def logic_cart(item: models.CartItem, current_user: dict = Depends(get_current_user)):
    """INTENTIONALLY VULNERABLE ENDPOINT - Trusting Client Data"""
    # Flaw: Does not validate if quantity is positive
    if item.quantity < 0:
        return {"success": True, "message": "Cart updated with negative quantity! We owe you money.", "flag": "flag{logic_negative_quantity}"}
    return {"success": True, "message": "Cart updated."}

account_balances = {}

@app.post("/api/labs/logic/transfer_funds")
def logic_transfer(transfer: models.TransferRequest, current_user: dict = Depends(get_current_user)):
    """INTENTIONALLY VULNERABLE ENDPOINT - Race Condition (TOCTOU)"""
    user_id = str(current_user['id'])
    if user_id not in account_balances:
        account_balances[user_id] = 100 # Initial balance
        
    balance = account_balances[user_id]
    if balance >= transfer.amount:
        # Flaw: Check is done here, but use is done later, allowing race conditions
        time.sleep(0.5) # Simulate processing delay to make race window large enough
        account_balances[user_id] -= transfer.amount
        
        if account_balances[user_id] < 0:
            return {"success": True, "message": f"Funds transferred. Balance negative! ({account_balances[user_id]})", "flag": "flag{logic_race_condition}"}
        return {"success": True, "message": f"Funds transferred successfully. Balance: {account_balances[user_id]}"}
    return {"success": False, "message": "Insufficient funds."}

# --- GRAPHQL SECURITY LAB ---
@app.post("/api/labs/graphql")
async def graphql_endpoint(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - GraphQL"""
    try:
        body = await request.json()
    except Exception:
        return {"error": "Invalid JSON"}

    def process_query(q_str):
        q_str_compact = q_str.replace(" ", "").replace("\n", "")
        # 1. Introspection
        if "__schema" in q_str_compact:
            return {"data": {"__schema": {"types": [{"name": "User"}]}}, "flag": "flag{graphql_introspection}"}
        # 2. BOLA in Resolvers
        if "user(id:1)" in q_str_compact and "email" in q_str_compact:
            return {"data": {"user": {"email": "admin@secureshop.local", "flag": "flag{graphql_bola_resolver}"}}}
        # 3. Query Batching
        if "verifyOTP" in q_str_compact:
            return {"data": {"verifyOTP": False}}
        return {"data": {}}

    if isinstance(body, list):
        # 3. Query Batching Bypass
        if len(body) >= 50:
            # If they batch many queries at once, they bypass rate limits
            for item in body:
                if "verifyOTP" in item.get("query", ""):
                    return {"data": "OTP Brute-forced!", "flag": "flag{graphql_query_batching}"}
        
        results = []
        for item in body:
            results.append(process_query(item.get("query", "")))
        return results
    else:
        return process_query(body.get("query", ""))

# --- ADVANCED INJECTION LAB ---
@app.get("/api/labs/adv_inject/template")
def adv_inject_template(name: str = "Guest"):
    """INTENTIONALLY VULNERABLE ENDPOINT - SSTI"""
    # Flaw: Evaluates the name parameter
    if "{{7*7}}" in name or "49" in name:
        return {"success": True, "rendered": f"Hello 49", "flag": "flag{adv_inject_ssti}"}
    return {"success": True, "rendered": f"Hello {name}"}

@app.post("/api/labs/adv_inject/xml")
async def adv_inject_xml(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - XXE"""
    body = await request.body()
    body_str = body.decode('utf-8', errors='ignore')
    # Flaw: Insecure XML parsing (simulated)
    if "<!ENTITY" in body_str and "SYSTEM" in body_str:
        return {"success": True, "message": "XML parsed. root:x:0:0:root:/root:/bin/bash", "flag": "flag{adv_inject_xxe}"}
    return {"success": True, "message": "XML parsed successfully."}

@app.post("/api/labs/adv_inject/ping_async")
def adv_inject_ping_async(data: models.PingRequest):
    """INTENTIONALLY VULNERABLE ENDPOINT - Blind Command Injection"""
    # Flaw: Command is executed asynchronously, output is not returned
    if "sleep" in data.host:
        import time
        import re
        m = re.search(r'sleep\s+(\d+)', data.host)
        if m:
            sleep_time = int(m.group(1))
            time.sleep(min(sleep_time, 5)) # Sleep up to 5 seconds
            return {"success": True, "message": "Ping started in background.", "flag": "flag{adv_inject_blind_cmd}"}
    return {"success": True, "message": "Ping started in background."}

# --- FILE UPLOAD LAB ---
@app.post("/api/labs/file_upload/basic")
async def file_upload_basic(file: UploadFile = File(...)):
    """INTENTIONALLY VULNERABLE ENDPOINT - Basic Extension Bypass"""
    if file.filename.endswith(".php"):
        return {"success": True, "message": f"File {file.filename} uploaded successfully. Shell executed!", "flag": "flag{upload_basic_bypass}"}
    return {"success": True, "message": f"File {file.filename} uploaded successfully."}

@app.post("/api/labs/file_upload/content_type")
async def file_upload_content_type(file: UploadFile = File(...)):
    """INTENTIONALLY VULNERABLE ENDPOINT - Content-Type Bypass"""
    if file.content_type in ["image/jpeg", "image/png"]:
        if file.filename.endswith(".php"):
            return {"success": True, "message": "Image uploaded! Wait... this is a shell!", "flag": "flag{upload_content_type_spoof}"}
        return {"success": True, "message": "Image uploaded successfully."}
    return {"success": False, "message": "Invalid file type. Only images are allowed."}

@app.post("/api/labs/file_upload/path_traversal")
async def file_upload_path_traversal(file: UploadFile = File(...)):
    """INTENTIONALLY VULNERABLE ENDPOINT - Path Traversal Upload"""
    if "../" in file.filename or "..\\" in file.filename:
        return {"success": True, "message": f"File written to /var/www/html/uploads/{file.filename}... System compromised!", "flag": "flag{upload_path_traversal}"}
    return {"success": True, "message": f"File written to /var/www/html/uploads/{file.filename}"}

# --- NOSQL INJECTION LAB ---
@app.post("/api/labs/nosql/auth_bypass")
async def nosql_auth_bypass(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - NoSQL $ne Authentication Bypass"""
    try:
        body = await request.json()
    except Exception:
        return {"success": False, "message": "Invalid JSON"}
    
    username = body.get("username", "")
    password = body.get("password", "")
    
    if username == "admin" and isinstance(password, dict) and "$ne" in password:
        return {"success": True, "message": "Logged in as admin!", "flag": "flag{nosql_auth_bypass}"}
    return {"success": False, "message": "Invalid credentials"}

@app.post("/api/labs/nosql/regex")
async def nosql_regex(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - NoSQL Data Extraction via Regex"""
    try:
        body = await request.json()
    except Exception:
        return {"success": False, "message": "Invalid JSON"}
    
    reset_token = body.get("reset_token", "")
    
    if isinstance(reset_token, dict) and "$regex" in reset_token:
        return {"success": True, "message": "Regex match found!", "flag": "flag{nosql_regex_extract}"}
    return {"success": False, "message": "User not found."}

@app.post("/api/labs/nosql/array")
async def nosql_array(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - NoSQL $in Array Bypass"""
    try:
        body = await request.json()
    except Exception:
        return {"success": False, "message": "Invalid JSON"}
    
    doc_id = body.get("doc_id", "")
    
    if isinstance(doc_id, dict) and "$in" in doc_id:
        return {"success": True, "message": "Access granted to multiple documents!", "flag": "flag{nosql_array_bypass}"}
    return {"success": False, "message": "Access denied."}

# --- SSRF LAB ---
@app.get("/api/internal-admin")
async def internal_admin(request: Request):
    """HIDDEN INTERNAL ENDPOINT FOR SSRF"""
    client_host = request.client.host
    if client_host == "127.0.0.1" or client_host == "localhost":
        return {"success": True, "message": "Welcome, internal admin.", "flag": "flag{ssrf_basic_internal}"}
    return {"success": False, "message": "Access Denied. Internal network only."}

@app.post("/api/labs/ssrf/fetch")
async def ssrf_fetch(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - SSRF Fetch"""
    try:
        body = await request.json()
    except Exception:
        return {"success": False, "message": "Invalid JSON"}
    
    url = body.get("url", "")
    
    if "169.254.169.254" in url and "iam" in url:
        return {"success": True, "message": "Fetched metadata: {\"AccessKeyId\": \"AKIAIOSFODNN7EXAMPLE\"}", "flag": "flag{ssrf_cloud_metadata}"}
    
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=2.0)
            
        if response.status_code == 200:
            try:
                data = response.json()
                if "flag{ssrf_basic_internal}" in str(data):
                    return {"success": True, "message": "Internal admin accessed!", "data": data, "flag": "flag{ssrf_basic_internal}"}
            except:
                pass
            return {"success": True, "message": "URL fetched successfully.", "data": response.text[:200]}
    except Exception as e:
        return {"success": False, "message": f"Failed to fetch URL: {str(e)}"}
    return {"success": False, "message": "Request failed."}

@app.post("/api/labs/ssrf/blind")
async def ssrf_blind(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - Blind SSRF"""
    try:
        body = await request.json()
    except Exception:
        return {"success": False, "message": "Invalid JSON"}
    
    url = body.get("url", "")
    
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=2.0)
            
        if response.status_code == 200:
            if "localhost" in url or "127.0.0.1" in url:
                return {"success": True, "message": "Service is UP.", "flag": "flag{ssrf_blind_ping}"}
            return {"success": True, "message": "Service is UP."}
    except Exception:
        return {"success": False, "message": "Service is DOWN."}
    return {"success": False, "message": "Service is DOWN."}

# --- DESERIALIZATION LAB ---
@app.post("/api/labs/deserialization/pickle")
async def deserialization_pickle(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - Python Pickle RCE"""
    try:
        body = await request.json()
    except Exception:
        return {"success": False, "message": "Invalid JSON"}
    
    data = body.get("data", "")
    
    try:
        obj = pickle.loads(base64.b64decode(data))
        return {"success": True, "message": f"Object deserialized: {obj}", "flag": "flag{deserialization_pickle_rce}"}
    except Exception as e:
        return {"success": False, "message": f"Deserialization failed: {str(e)}"}

@app.post("/api/labs/deserialization/yaml")
async def deserialization_yaml(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - YAML Deserialization"""
    try:
        body = await request.json()
    except Exception:
        return {"success": False, "message": "Invalid JSON"}
    
    data = body.get("data", "")
    
    try:
        obj = yaml.load(data, Loader=yaml.Loader)
        if "apply" in data or "os.system" in data:
            return {"success": True, "message": "RCE via YAML!", "flag": "flag{deserialization_yaml_rce}"}
        return {"success": True, "message": f"YAML loaded: {obj}"}
    except Exception as e:
        return {"success": False, "message": f"YAML error: {str(e)}"}

@app.post("/api/labs/deserialization/jwt_none")
async def deserialization_jwt_none(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - JWT None Algorithm"""
    try:
        body = await request.json()
    except Exception:
        return {"success": False, "message": "Invalid JSON"}
    
    token = body.get("token", "")
    
    try:
        header_b64 = token.split(".")[0]
        header_b64 += "=" * ((4 - len(header_b64) % 4) % 4)
        import json
        header = json.loads(base64.b64decode(header_b64).decode())
        
        if header.get("alg", "").lower() == "none":
            parts = token.split(".")
            if len(parts) >= 2:
                payload_b64 = parts[1]
                payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
                payload = json.loads(base64.b64decode(payload_b64).decode())
                
                if payload.get("username") == "admin":
                    return {"success": True, "message": "Logged in as admin via None algorithm bypass!", "flag": "flag{deserialization_jwt_none}"}
    except Exception:
        pass
        
    return {"success": False, "message": "Invalid token."}

# --- OAUTH & SSO LAB ---
@app.get("/api/labs/oauth/login")
async def oauth_login(code: str = None, state: str = None):
    """INTENTIONALLY VULNERABLE ENDPOINT - Flawed State Parameter"""
    if not code:
        return {"success": False, "message": "Missing authorization code"}
    return {"success": True, "message": "OAuth login successful! State validation bypassed.", "flag": "flag{oauth_flawed_state}"}

@app.get("/api/labs/oauth/callback")
async def oauth_callback(redirect_uri: str = None):
    """INTENTIONALLY VULNERABLE ENDPOINT - Redirect URI Manipulation"""
    if not redirect_uri:
        return {"success": False, "message": "Missing redirect_uri"}
    import re
    if re.search(r"trusted\.com", redirect_uri):
        if "attacker.com" in redirect_uri:
            return {"success": True, "message": f"Redirecting to malicious URI: {redirect_uri}", "flag": "flag{oauth_redirect_bypass}"}
        return {"success": True, "message": "Redirecting to trusted URI"}
    return {"success": False, "message": "Invalid redirect_uri"}

@app.get("/api/labs/oauth/implicit")
async def oauth_implicit(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - Implicit Flow Token Leak"""
    origin = request.headers.get("origin", "")
    if "attacker.com" in origin:
         return {"success": True, "message": "Token leaked to attacker origin!", "flag": "flag{oauth_implicit_leak}"}
    return {"success": False, "message": "Token safe... for now."}

# --- CORS LAB ---
@app.get("/api/labs/cors/reflected")
async def cors_reflected(request: Request, response: Response):
    """INTENTIONALLY VULNERABLE ENDPOINT - Reflected Origin"""
    origin = request.headers.get("origin", "")
    if origin:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        if "malicious.com" in origin:
            return {"success": True, "message": "CORS Reflected Origin Bypass!", "flag": "flag{cors_reflected_origin}"}
        return {"success": True, "message": "CORS data."}
    return {"success": False, "message": "Missing Origin header."}

@app.get("/api/labs/cors/null")
async def cors_null(request: Request, response: Response):
    """INTENTIONALLY VULNERABLE ENDPOINT - Null Origin Trusted"""
    origin = request.headers.get("origin", "")
    if origin == "null":
        response.headers["Access-Control-Allow-Origin"] = "null"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return {"success": True, "message": "CORS Null Origin Trusted!", "flag": "flag{cors_null_origin}"}
    return {"success": False, "message": "Origin not allowed."}

@app.get("/api/labs/cors/prefix")
async def cors_prefix(request: Request, response: Response):
    """INTENTIONALLY VULNERABLE ENDPOINT - Prefix Regex Bypass"""
    origin = request.headers.get("origin", "")
    if origin.startswith("https://trusted.com"):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        if origin != "https://trusted.com":
             return {"success": True, "message": "CORS Regex Bypass!", "flag": "flag{cors_prefix_bypass}"}
        return {"success": True, "message": "CORS data."}
    return {"success": False, "message": "Origin not allowed."}

# --- COMMAND INJECTION LAB ---
@app.post("/api/labs/cmd/ping")
async def cmd_ping(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - Basic Command Injection"""
    try:
        body = await request.json()
    except Exception:
        return {"success": False, "message": "Invalid JSON"}
    
    ip = body.get("ip", "")
    
    try:
        import platform
        cmd = f"ping -n 1 {ip}" if platform.system().lower() == "windows" else f"ping -c 1 {ip}"
        
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate(timeout=5)
        output = out.decode() + err.decode()
        
        if "whoami" in ip or "ls" in ip or "cat" in ip or "dir" in ip:
             return {"success": True, "message": f"Command executed successfully!\n{output}", "flag": "flag{cmd_basic_concat}"}
        return {"success": True, "message": f"Ping results:\n{output}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

@app.post("/api/labs/cmd/blind")
async def cmd_blind(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - Blind Command Injection"""
    try:
        body = await request.json()
    except Exception:
        return {"success": False, "message": "Invalid JSON"}
    
    ip = body.get("ip", "")
    
    try:
        import platform
        cmd = f"ping -n 1 {ip}" if platform.system().lower() == "windows" else f"ping -c 1 {ip}"
        start_time = time.time()
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate(timeout=10)
        end_time = time.time()
        
        if end_time - start_time >= 4:
            return {"success": True, "message": "Ping executed.", "flag": "flag{cmd_blind_sleep}"}
            
        return {"success": True, "message": "Ping executed."}
    except subprocess.TimeoutExpired:
        return {"success": True, "message": "Ping executed.", "flag": "flag{cmd_blind_sleep}"}
    except Exception as e:
        return {"success": False, "message": "Error occurred."}

@app.post("/api/labs/cmd/filter")
async def cmd_filter(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - Filter Bypass"""
    try:
        body = await request.json()
    except Exception:
        return {"success": False, "message": "Invalid JSON"}
    
    ip = body.get("ip", "")
    
    if " " in ip or ";" in ip:
        return {"success": False, "message": "Hacking Attempt Detected! Spaces and semicolons are blocked."}
        
    try:
        import platform
        cmd = f"ping -n 1 {ip}" if platform.system().lower() == "windows" else f"ping -c 1 {ip}"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate(timeout=5)
        output = out.decode() + err.decode()
        
        if "IFS" in ip or "|" in ip or "&" in ip or "`" in ip or "$" in ip:
             return {"success": True, "message": f"Command executed successfully!\n{output}", "flag": "flag{cmd_filter_bypass}"}
        return {"success": True, "message": f"Ping results:\n{output}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

# --- SSTI LAB ---
@app.post("/api/labs/ssti/math")
async def ssti_math(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - Template Math Evaluation"""
    try:
        body = await request.json()
    except Exception:
        return {"success": False, "message": "Invalid JSON"}
    
    template_str = body.get("template", "")
    
    try:
        template = jinja2.Template(f"Hello {template_str}!")
        rendered = template.render()
        
        if "49" in rendered and "*" in template_str:
            return {"success": True, "message": rendered, "flag": "flag{ssti_basic_math}"}
        return {"success": True, "message": rendered}
    except Exception as e:
        return {"success": False, "message": f"Template Error: {str(e)}"}

@app.post("/api/labs/ssti/env")
async def ssti_env(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - Env Dump"""
    try:
        body = await request.json()
    except Exception:
        return {"success": False, "message": "Invalid JSON"}
    
    template_str = body.get("template", "")
    
    try:
        mock_config = {"SECRET_KEY": "super_secret_key_123", "DB_PASS": "admin123"}
        template = jinja2.Template(f"Hello {template_str}!")
        rendered = template.render(config=mock_config)
        
        if "super_secret_key_123" in rendered or "admin123" in rendered:
            return {"success": True, "message": rendered, "flag": "flag{ssti_env_dump}"}
        return {"success": True, "message": rendered}
    except Exception as e:
        return {"success": False, "message": f"Template Error: {str(e)}"}

@app.post("/api/labs/ssti/rce")
async def ssti_rce(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - RCE via subclasses"""
    try:
        body = await request.json()
    except Exception:
        return {"success": False, "message": "Invalid JSON"}
    
    template_str = body.get("template", "")
    
    try:
        template = jinja2.Template(f"Hello {template_str}!")
        rendered = template.render()
        
        if "__subclasses__" in template_str and ("popen" in template_str or "system" in template_str):
            return {"success": True, "message": f"RCE triggered!\n{rendered[:200]}", "flag": "flag{ssti_rce_subclasses}"}
        return {"success": True, "message": rendered}
    except Exception as e:
        return {"success": False, "message": f"Template Error: {str(e)}"}

# --- XXE LAB ---
@app.post("/api/labs/xxe/lfi")
async def xxe_lfi(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - XXE LFI"""
    try:
        xml_data = await request.body()
    except Exception:
        return {"success": False, "message": "Invalid Request"}
    
    if not xml_data:
        return {"success": False, "message": "Missing XML data"}
        
    try:
        parser = etree.XMLParser(resolve_entities=True, no_network=False)
        root = etree.fromstring(xml_data, parser)
        
        rendered_text = "".join(root.itertext())
        if "root:x:0:0" in rendered_text or "daemon:x:1:1" in rendered_text or "windows" in rendered_text.lower():
             return {"success": True, "message": f"File read successfully!\n{rendered_text[:200]}", "flag": "flag{xxe_basic_lfi}"}
             
        if "SYSTEM" in xml_data.decode() and ("file://" in xml_data.decode() or "c:/" in xml_data.decode().lower()):
             return {"success": True, "message": f"Local file inclusion triggered!\n{rendered_text[:200]}", "flag": "flag{xxe_basic_lfi}"}

        return {"success": True, "message": f"Parsed XML: {rendered_text}"}
    except Exception as e:
        return {"success": False, "message": f"XML Parse Error: {str(e)}"}

@app.post("/api/labs/xxe/dos")
async def xxe_dos(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - XXE Billion Laughs DoS"""
    try:
        xml_data = await request.body()
    except Exception:
        return {"success": False, "message": "Invalid Request"}
    
    if not xml_data:
        return {"success": False, "message": "Missing XML data"}
        
    try:
        xml_str = xml_data.decode()
        if "lol9" in xml_str and "&lol8;" in xml_str:
            return {"success": True, "message": "Server Memory Exhausted! (Simulated DoS)", "flag": "flag{xxe_billion_laughs}"}
            
        parser = etree.XMLParser(resolve_entities=True, huge_tree=True)
        root = etree.fromstring(xml_data, parser)
        rendered_text = "".join(root.itertext())

        return {"success": True, "message": f"Parsed XML: {rendered_text}"}
    except Exception as e:
        return {"success": False, "message": f"XML Parse Error: {str(e)}"}

@app.post("/api/labs/xxe/ssrf")
async def xxe_ssrf(request: Request):
    """INTENTIONALLY VULNERABLE ENDPOINT - XXE SSRF"""
    try:
        xml_data = await request.body()
    except Exception:
        return {"success": False, "message": "Invalid Request"}
    
    if not xml_data:
        return {"success": False, "message": "Missing XML data"}
        
    try:
        xml_str = xml_data.decode()
        if "169.254.169.254" in xml_str or "localhost:8000/api/internal-admin" in xml_str:
             return {"success": True, "message": "SSRF triggered via XML external entity! Fetched internal resource.", "flag": "flag{xxe_ssrf_fetch}"}
             
        parser = etree.XMLParser(resolve_entities=True, no_network=False)
        root = etree.fromstring(xml_data, parser)
        rendered_text = "".join(root.itertext())

        return {"success": True, "message": f"Parsed XML: {rendered_text}"}
    except Exception as e:
        return {"success": False, "message": f"XML Parse Error: {str(e)}"}