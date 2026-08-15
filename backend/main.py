from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import List
import os

from . import database, models, auth

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
def get_products():

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

    # IDOR protection
    if (
        order["user_id"] != current_user["id"]
        and current_user["role"] != "admin"
    ):
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

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