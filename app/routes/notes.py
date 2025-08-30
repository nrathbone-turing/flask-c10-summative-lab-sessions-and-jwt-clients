from flask import Blueprint, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Note
from ..schemas import note_schema, notes_schema

bp = Blueprint("notes", __name__)

@bp.get("")
@login_required
def list_notes():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = Note.query.filter_by(user_id=current_user.id) \
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


@bp.get("/<int:note_id>")
@login_required
def get_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return {"error": f"Note with id {note_id} not found."}, 404
    return note_schema.dump(note), 200


@bp.post("")
@login_required
def create_note():
    data = request.get_json()
    if not data.get("title"):
        return {"error": "Title is required to create a note."}, 400
    note = Note(user_id=current_user.id, **data)
    db.session.add(note)
    db.session.commit()
    return note_schema.dump(note), 201


@bp.patch("/<int:note_id>")
@login_required
def update_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return {"error": f"Note with id {note_id} not found."}, 404

    data = request.get_json()
    if "title" in data and not data["title"].strip():
        return {"error": "Title cannot be empty."}, 400

    for field in ("title", "body"):
        if field in data:
            setattr(note, field, data[field])

    db.session.commit()
    return note_schema.dump(note), 200


@bp.delete("/<int:note_id>")
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return {"error": f"Note with id {note_id} not found."}, 404
    db.session.delete(note)
    db.session.commit()
    return {"message": f"Note {note_id} deleted successfully."}, 200