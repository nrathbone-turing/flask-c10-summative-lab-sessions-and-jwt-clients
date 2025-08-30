from flask import Blueprint, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Note
from ..schemas import note_schema, notes_schema

bp = Blueprint("notes", __name__)

@bp.get("")
@login_required
def list_notes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return {"data": notes_schema.dump(notes)}

@bp.post("")
@login_required
def create_note():
    data = request.get_json()
    note = Note(user_id=current_user.id, **data)
    db.session.add(note)
    db.session.commit()
    return note_schema.dump(note), 201
