# app/routes/notes.py
# Notes resource routes (CRUD).
# - /notes: List or create notes (pagination supported)
# - /notes/<id>: Retrieve, update, or delete individual notes
# All routes require authentication.

from flask import Blueprint, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Note
from ..schemas import note_schema, notes_schema

bp = Blueprint("notes", __name__)

@bp.get("")
@login_required
def list_notes():
    """
    List notes for the current logged-in user.
    - Supports pagination with ?page=N&per_page=M.
    - Returns 200 with notes data and pagination metadata.
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = Note.query.filter_by(user_id=current_user.id)\
                           .paginate(page=page, per_page=per_page, error_out=False)

    return {
        "data": notes_schema.dump(pagination.items),
        "meta": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
        }
    }, 200


@bp.post("")
@login_required
def create_note():
    """
    Create a new note for the current logged-in user.
    - Requires at least 'title' in JSON body.
    - Returns 201 with created note on success.
    - Returns 400 if 'title' is missing or empty.
    """
    data = request.get_json() or {}

    if not data.get("title") or not data["title"].strip():
        return {"error": "Title is required to create a note."}, 400

    note = Note(user_id=current_user.id, title=data["title"], body=data.get("body", ""))
    db.session.add(note)
    db.session.commit()
    return note_schema.dump(note), 201


@bp.get("/<int:note_id>")
@login_required
def get_note(note_id):
    """
    Retrieve a single note by ID.
    - Returns 200 with the note if found and owned by the current user.
    - Returns 403 if the note belongs to another user.
    - Returns 404 if the note does not exist.
    """
    note = db.session.get(Note, note_id)
    if not note:
        return {"error": "Note not found"}, 404
    if note.user_id != current_user.id:
        return {"error": "Not authorized to view this note."}, 403
    return note_schema.dump(note), 200


@bp.put("/<int:id>")
@login_required
def update_note(id):
    """
    Update an existing note owned by the current logged-in user.
    - Path param: <id> (note ID)
    - Requires JSON body with at least one of: 'title', 'body'
    - Returns 200 with the updated note on success
    - Returns 400 if no updatable fields are provided
    - Returns 403 if the note does not belong to the current user
    - Returns 404 if the note is not found
    """
    note = db.session.get(Note, id)

    if note.user_id != current_user.id:
        return {"error": "Not authorized to update this note."}, 403

    data = request.get_json() or {}

    if not any(field in data for field in ("title", "body")):
        return {"error": "At least one of 'title' or 'body' is required."}, 400

    if "title" in data and data["title"].strip():
        note.title = data["title"].strip()
    if "body" in data:
        note.body = data["body"]

    db.session.commit()
    return note_schema.dump(note), 200


@bp.delete("/<int:note_id>")
@login_required
def delete_note(note_id):
    """
    Delete a note owned by the current logged-in user.
    - Requires the note ID in the URL path.
    - Only deletes the note if it belongs to the current user.
    - Returns 204 with an empty body if successful.
    - Returns 404 if the note does not exist or does not belong to the user.
    """
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return {"error": "Note not found"}, 404
    db.session.delete(note)
    db.session.commit()
    return {}, 204

notes_bp = bp