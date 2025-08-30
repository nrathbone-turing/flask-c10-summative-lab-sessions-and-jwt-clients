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
        return {"error": "Email and password are required."}, 400

    if User.query.filter_by(email=data["email"]).first():
        return {"error": "That email is already registered."}, 400

    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return {"user": user_schema.dump(user)}, 201


@bp.post("/login")
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return {"error": "Invalid email or password."}, 401
    login_user(user)
    return {"user": user_schema.dump(user)}, 200


@bp.post("/logout")
@login_required
def logout():
    logout_user()
    return {"message": "You have been logged out successfully."}, 200


@bp.get("/me")
@login_required
def me():
    return {"user": user_schema.dump(current_user)}, 200