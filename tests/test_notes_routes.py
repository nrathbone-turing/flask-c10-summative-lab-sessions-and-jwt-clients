# tests/test_notes_routes.py
# Tests Notes resource routes.
# - Create and list notes
# - Enforce login for notes endpoints
# - Pagination of notes
# - Handle invalid/missing notes (404s)

def login(client, email="noteuser@example.com", password="pw"):
    """Helper: register and log in a test user."""

    client.post("/auth/register", json={"email": email, "password": password})
    return client

def test_create_and_list_notes(client):
    """Create a note and verify it appears in notes list."""

    client = login(client)

    # Create
    resp = client.post("/notes", json={"title": "Test Note", "body": "Hello"})
    assert resp.status_code == 201
    assert resp.json["title"] == "Test Note"

    # List
    resp = client.get("/notes")
    assert resp.status_code == 200
    assert len(resp.json["data"]) == 1

def test_notes_requires_login(client):
    """Accessing /notes without login should return 302 or 401."""
    
    resp = client.get("/notes")
    assert resp.status_code in (302, 401)

def test_notes_pagination(client):
    """Verify pagination works: per_page, page count, empty pages."""
    
    client = login(client)

    # Create 15 notes
    for i in range(15):
        client.post("/notes", json={"title": f"Note {i}", "body": "Body"})

    # Page 1 with per_page=5
    resp = client.get("/notes?page=1&per_page=5")
    assert resp.status_code == 200
    data = resp.json
    assert len(data["data"]) == 5
    assert data["meta"]["page"] == 1
    assert data["meta"]["per_page"] == 5
    assert data["meta"]["total"] == 15
    assert data["meta"]["pages"] == 3

    # Page 2 with per_page=5
    resp = client.get("/notes?page=2&per_page=5")
    assert resp.status_code == 200
    data = resp.json
    assert len(data["data"]) == 5
    assert data["meta"]["page"] == 2

    # Page beyond range returns empty list but valid meta
    resp = client.get("/notes?page=10&per_page=5")
    assert resp.status_code == 200
    data = resp.json
    assert data["data"] == []
    assert data["meta"]["page"] == 10
    assert data["meta"]["pages"] == 3

def test_cannot_access_notes_without_login(client):
    """Unauthorized request to /notes should be blocked."""
    
    resp = client.get("/notes")
    assert resp.status_code in (302, 401)

def test_get_nonexistent_note_returns_404(client):
    """Requesting a non-existent note ID should return 404."""
    
    client.post("/auth/register", json={"email": "noteuser@example.com", "password": "pw"})
    resp = client.get("/notes/999")
    assert resp.status_code == 404
    assert "not found" in resp.json["error"]  # explicit error message check