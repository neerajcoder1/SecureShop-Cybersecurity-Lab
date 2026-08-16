from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import List
import os

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

    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "email": current_user["email"]
    }


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
        
        # Give UNION flag if they successfully injected UNION
        if "' UNION" in q.upper():
            return {"results": rows, "flag": "flag{sqli_union_version}"}
            
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
    html = f'<input type="text" name="profile_name" value="{name}">'
    flag = None
    if '"><script>' in name.lower() or '" autofocus onfocus="' in name.lower():
        flag = "flag{xss_context_attribute}"
    return {"html": html, "flag": flag}