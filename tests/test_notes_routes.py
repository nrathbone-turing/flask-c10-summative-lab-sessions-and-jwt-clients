# tests/test_notes_routes.py
# Tests Notes resource routes.
# - Create and list notes
# - Enforce login for notes endpoints
# - Pagination of notes
# - Handle invalid/missing notes (404s)

def signup_and_login(client, username="noteuser", password="pw"):
    """Helper: sign up and log in a test user."""
    client.post("/signup", json={
        "username": username,
        "password": password,
        "password_confirmation": password
    })
    return client


def test_create_and_list_notes(client):
    """Create a note and verify it appears in notes list."""

    client = signup_and_login(client)

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

    client = signup_and_login(client)

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


def test_get_nonexistent_note_returns_404(client):
    """Requesting a non-existent note ID should return 404."""

    signup_and_login(client)
    resp = client.get("/notes/999")
    assert resp.status_code == 404
    assert "not found" in resp.json["error"]

def test_update_note(client):
    """Update an existing note owned by the user."""
    # Register + login
    client.post("/signup", json={
        "username": "noteup@example.com",
        "password": "pw",
        "password_confirmation": "pw"
    })
    # Create a note
    resp = client.post("/notes", json={"title": "Original", "body": "Hello"})
    note_id = resp.json["id"]

    # Update title
    resp = client.put(f"/notes/{note_id}", json={"title": "Updated Title"})
    assert resp.status_code == 200
    assert resp.json["title"] == "Updated Title"

    # Update body
    resp = client.put(f"/notes/{note_id}", json={"body": "New body"})
    assert resp.status_code == 200
    assert resp.json["body"] == "New body"

def test_update_note_invalid_fields(client):
    """Updating with no valid fields should return 400."""
    client.post("/signup", json={
        "username": "noteinv@example.com",
        "password": "pw",
        "password_confirmation": "pw"
    })
    resp = client.post("/notes", json={"title": "To update", "body": "Body"})
    note_id = resp.json["id"]

    resp = client.put(f"/notes/{note_id}", json={})
    assert resp.status_code == 400
    assert "error" in resp.json

def test_update_note_unauthorized(client):
    """Users cannot update notes they don't own."""
    # First user creates a note
    client.post("/signup", json={
        "username": "owner@example.com",
        "password": "pw",
        "password_confirmation": "pw"
    })
    resp = client.post("/notes", json={"title": "Owner note"})
    note_id = resp.json["id"]

    # Second user registers
    client.post("/logout")
    client.post("/signup", json={
        "username": "intruder@example.com",
        "password": "pw",
        "password_confirmation": "pw"
    })
    # Try to update owner's note
    resp = client.put(f"/notes/{note_id}", json={"title": "Hacked!"})
    assert resp.status_code == 403

def test_delete_note(client):
    """Delete a note owned by the current user."""
    client.post("/signup", json={
        "username": "notedel@example.com",
        "password": "pw",
        "password_confirmation": "pw"
    })
    resp = client.post("/notes", json={"title": "To delete"})
    note_id = resp.json["id"]

    resp = client.delete(f"/notes/{note_id}")
    assert resp.status_code == 204

    # Confirm it's gone
    resp = client.get("/notes")
    assert all(n["id"] != note_id for n in resp.json["data"])

def test_delete_note_not_found(client):
    """Deleting a non-existent note returns 404."""
    client.post("/signup", json={
        "username": "missingdel@example.com",
        "password": "pw",
        "password_confirmation": "pw"
    })
    resp = client.delete("/notes/9999")
    assert resp.status_code == 404
    assert "error" in resp.json
