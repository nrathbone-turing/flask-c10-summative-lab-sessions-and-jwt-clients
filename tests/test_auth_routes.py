def test_register_and_login(client):
    # Register
    resp = client.post("/auth/register", json={"email": "new@example.com", "password": "pw"})
    assert resp.status_code == 200
    assert resp.json["user"]["email"] == "new@example.com"

    # Login
    resp = client.post("/auth/login", json={"email": "new@example.com", "password": "pw"})
    assert resp.status_code == 200
    assert "user" in resp.json

def test_login_invalid(client):
    resp = client.post("/auth/login", json={"email": "nope@example.com", "password": "pw"})
    assert resp.status_code == 401

def test_me_requires_login(client):
    resp = client.get("/auth/me")
    assert resp.status_code == 302 or resp.status_code == 401
