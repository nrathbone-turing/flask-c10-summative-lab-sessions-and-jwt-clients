# tests/test_app.py
# Tests the root app setup and health check endpoint.

def test_health_endpoint(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json["status"] == "ok"
