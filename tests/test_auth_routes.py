# tests/test_auth_routes.py
# Tests authentication routes.
# - Sign up new users
# - Prevent duplicate signup
# - Log in with correct/incorrect credentials
# - Check session endpoint
# - Log out session

def test_signup_and_login(client):
    """Sign up a new user and then log in successfully."""

    # Signup
    resp = client.post("/signup", json={
        "username": "newuser",
        "password": "pw",
        "password_confirmation": "pw"
    })
    assert resp.status_code == 201
    assert resp.json["username"] == "newuser"

    # Login
    resp = client.post("/login", json={
        "username": "newuser",
        "password": "pw"
    })
    assert resp.status_code == 200
    assert "username" in resp.json


def test_signup_duplicate_username(client):
    """Signing up with an already-used username returns 400."""

    client.post("/signup", json={
        "username": "dupuser",
        "password": "pw",
        "password_confirmation": "pw"
    })
    resp = client.post("/signup", json={
        "username": "dupuser",
        "password": "pw",
        "password_confirmation": "pw"
    })
    assert resp.status_code == 400
    assert "already" in resp.json["error"]


def test_login_invalid_username(client):
    """Login attempt with non-existent username returns 401 Unauthorized."""

    resp = client.post("/login", json={
        "username": "nope",
        "password": "pw"
    })
    assert resp.status_code == 401
    assert "Invalid" in resp.json["error"]


def test_login_wrong_password(client):
    """Login with correct username but wrong password returns 401."""

    client.post("/signup", json={
        "username": "userpw",
        "password": "pw",
        "password_confirmation": "pw"
    })
    resp = client.post("/login", json={
        "username": "userpw",
        "password": "wrong"
    })
    assert resp.status_code == 401
    assert "error" in resp.json


def test_check_session_requires_login(client):
    """Accessing /check_session without login should return empty {}."""

    resp = client.get("/check_session")
    assert resp.status_code == 200
    assert resp.json == {}


def test_logout(client):
    """User can log out and session is cleared."""

    # Signup + login
    client.post("/signup", json={
        "username": "logoutuser",
        "password": "pw",
        "password_confirmation": "pw"
    })
    resp = client.delete("/logout")
    assert resp.status_code == 200
    assert resp.json == {}

def test_signup_password_confirmation_mismatch(client):
    """Signup with mismatched password and confirmation returns 400."""
    resp = client.post("/signup", json={
        "username": "mismatchuser",
        "password": "pw1",
        "password_confirmation": "pw2"
    })
    assert resp.status_code == 400
    assert "confirmation" in resp.json["error"]