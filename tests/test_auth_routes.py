# tests/test_auth_routes.py
# Tests authentication routes.
# - Register new users
# - Prevent duplicate registration
# - Log in with correct/incorrect credentials
# - Require login for /auth/me
# - Log out session

def test_register_and_login(client):
    
    """Register a new user and then log in successfully."""

    # Register
    resp = client.post("/auth/register", json={"email": "new@example.com", "password": "pw"})
    assert resp.status_code == 200
    assert resp.json["user"]["email"] == "new@example.com"

    # Login
    resp = client.post("/auth/login", json={"email": "new@example.com", "password": "pw"})
    assert resp.status_code == 200
    assert "user" in resp.json

def test_login_invalid(client):
    """Login attempt with non-existent user returns 401 Unauthorized."""
    
    resp = client.post("/auth/login", json={"email": "nope@example.com", "password": "pw"})
    assert resp.status_code == 401
    assert "Invalid" in resp.json["error"]  # check for meaningful message

def test_me_requires_login(client):
    """Accessing /auth/me without login should return 302 or 401."""
    
    resp = client.get("/auth/me")
    assert resp.status_code == 302 or resp.status_code == 401

def test_register_duplicate_email(client):
    """Registering with an already-used email returns 400."""

    client.post("/auth/register", json={"email": "dup@example.com", "password": "pw"})
    resp = client.post("/auth/register", json={"email": "dup@example.com", "password": "pw"})
    assert resp.status_code == 400
    assert "already" in resp.json["error"]  # check clarity

def test_login_wrong_password(client, user):
    """Login with correct email but wrong password returns 401."""
    
    resp = client.post("/auth/login", json={"email": user.email, "password": "wrong"})
    assert resp.status_code == 401
    assert "error" in resp.json