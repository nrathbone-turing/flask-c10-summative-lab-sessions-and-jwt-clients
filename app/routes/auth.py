from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from ..extensions import db
from ..schemas import user_schema

bp = Blueprint("auth", __name__)

@bp.post("/register")
def register():
    """
    Register a new user.
    - Requires 'email' and 'password' in JSON body.
    - Returns 201 with user data and starts a session on success.
    - Returns 400 if fields are missing or email already exists.
    """
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return {"error": "Email and password are required."}, 400

    if User.query.filter_by(email=data["email"]).first():
        return {"error": "That email is already registered."}, 400

    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    login_user(user)  # start a session automatically
    return {"user": user_schema.dump(user)}, 201


@bp.post("/login")
def login():
    """
    Log in an existing user.
    - Requires 'email' and 'password' in JSON body.
    - Returns 200 with user data if credentials are valid.
    - Returns 401 if email not found or password is incorrect.
    """
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()
    if not user or not user.check_password(data.get("password", "")):
        return {"error": "Invalid email or password."}, 401

    login_user(user)
    return {"user": user_schema.dump(user)}, 200


@bp.post("/logout")
@login_required
def logout():
    """
    Log out the current user.
    - Requires an active session.
    - Returns 200 with confirmation message.
    """
    logout_user()
    return {"message": "You have been logged out successfully."}, 200


@bp.get("/me")
@login_required
def me():
    """
    Get details of the current logged-in user.
    - Requires an active session.
    - Returns 200 with user data.
    """
    return {"user": user_schema.dump(current_user)}, 200