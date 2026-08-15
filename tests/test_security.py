from fastapi.testclient import TestClient
from backend.main import app
from backend import database
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    database.init_db()
    yield

def test_sqli_protection():
    # Attempt SQL injection in search
    # The payload ' OR '1'='1 should not return all products if parameterized correctly
    sqli_payload = "' OR '1'='1"
    response = client.get(f"/api/products/search?q={sqli_payload}")
    
    assert response.status_code == 200
    products = response.json()
    
    # If the app is secure, it searches for the literal string "' OR '1'='1"
    # and should return 0 results since no dummy product has that name.
    # If vulnerable, it would return all products.
    assert len(products) == 0

def test_idor_protection():
    # Setup: Register two users
    client.post("/api/register", json={"username": "user1", "email": "user1@example.com", "password": "SecurePassword123!"})
    client.post("/api/register", json={"username": "user2", "email": "user2@example.com", "password": "SecurePassword123!"})
    
    # Login as User 1
    res1 = client.post("/api/login", json={"username": "user1", "password": "SecurePassword123!"})
    token1 = res1.json().get("access_token")
    
    # Login as User 2
    res2 = client.post("/api/login", json={"username": "user2", "password": "SecurePassword123!"})
    token2 = res2.json().get("access_token")
    
    if token1 and token2:
        # User 1 creates an order
        order_res = client.post(
            "/api/orders",
            json={"product_id": 1, "quantity": 1},
            headers={"Authorization": f"Bearer {token1}"}
        )
        assert order_res.status_code == 201
        order_id = order_res.json()["order_id"]
        
        # User 2 attempts to fetch User 1's order (IDOR attempt)
        idor_res = client.get(
            f"/api/orders/{order_id}",
            headers={"Authorization": f"Bearer {token2}"}
        )
        
        # SECURE implementation should return 404
        assert idor_res.status_code == 404
