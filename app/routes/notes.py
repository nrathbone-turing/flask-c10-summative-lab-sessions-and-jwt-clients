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
    List notes for the current user.
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
    Create a new note for the current user.
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

notes_bp = bp