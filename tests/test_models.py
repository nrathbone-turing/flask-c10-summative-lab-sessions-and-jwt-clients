# tests/test_models.py
# Tests model functionality.
# - User model: password hashing, verification, email field
# - Note model: created_at and updated_at timestamps auto-population & update behavior

from app.models import User, Note
from app.extensions import db
import time

def test_password_hashing(user):
    """User password hashing and verification works."""
    assert user.check_password("password") is True
    assert user.check_password("wrong") is False

def test_user_email(user):
    """User email is stored correctly."""
    assert user.email == "test@example.com"

def test_note_timestamps(client, user):
    """Notes automatically set created_at and updated_at."""
    note = Note(user_id=user.id, title="Timestamp test", body="Body")
    db.session.add(note)
    db.session.commit()

    assert note.created_at is not None
    assert note.updated_at is not None
    created_at = note.created_at
    updated_at = note.updated_at

    # Trigger an update
    time.sleep(1)  # ensure timestamp difference
    note.title = "Updated Title"
    db.session.commit()

    assert note.updated_at > updated_at
    assert note.created_at == created_at  # created_at should remain constant