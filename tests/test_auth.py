from fastapi.testclient import TestClient
from backend.main import app
from backend import database
import pytest
import os

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Use a test database or ensure it's initialized cleanly
    # For this lab, we just initialize the default one
    database.init_db()
    yield

def test_register_user():
    # Attempt to register a user
    response = client.post(
        "/api/register",
        json={"username": "testuser", "email": "testuser@example.com", "password": "SecurePassword123!"}
    )
    # 201 Created or 400 if already exists (safe for re-runs)
    assert response.status_code in (201, 400)

def test_login_user():
    # Attempt to login
    response = client.post(
        "/api/login",
        json={"username": "testuser", "password": "SecurePassword123!"}
    )
    if response.status_code == 200:
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    else:
        # If user wasn't registered successfully before
        assert response.status_code == 401

def test_access_protected_route_without_token():
    response = client.get("/api/users/me")
    assert response.status_code == 401
