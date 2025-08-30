def login(client, email="noteuser@example.com", password="pw"):
    client.post("/auth/register", json={"email": email, "password": password})
    return client

def test_create_and_list_notes(client):
    client = login(client)

    # Create
    resp = client.post("/notes", json={"title": "Test Note", "body": "Hello"})
    assert resp.status_code == 201
    assert resp.json["title"] == "Test Note"

    # List
    resp = client.get("/notes")
    assert resp.status_code == 200
    assert len(resp.json["data"]) == 1
