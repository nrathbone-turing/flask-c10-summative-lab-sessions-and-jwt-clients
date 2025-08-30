from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from ..extensions import db
from ..schemas import user_schema

bp = Blueprint("auth", __name__)

@bp.post("/register")
def register():
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return {"error": "Email and password required"}, 400

    if User.query.filter_by(email=data["email"]).first():
        return {"error": "Email already exists"}, 400

    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    login_user(user)  # start a session
    return {"user": user_schema.dump(user)}

@bp.post("/login")
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return {"error": "Invalid credentials"}, 401
    login_user(user)
    return {"user": user_schema.dump(user)}

@bp.post("/logout")
@login_required
def logout():
    logout_user()
    return {"message": "Logged out"}

@bp.get("/me")
@login_required
def me():
    return {"user": user_schema.dump(current_user)}
