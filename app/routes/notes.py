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
    }

@bp.post("")
@login_required
def create_note():
    data = request.get_json()
    note = Note(user_id=current_user.id, **data)
    db.session.add(note)
    db.session.commit()
    return note_schema.dump(note), 201
