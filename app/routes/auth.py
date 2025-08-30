# app/routes/auth.py
# Authentication routes using Flask-Login.
# - /signup: Register new user
# - /login: Log in existing user
# - /logout: Log out user
# - /check_session: Return current logged-in user (or {} if none)

from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from ..extensions import db
from ..schemas import user_schema

bp = Blueprint("auth", __name__)

@bp.post("/signup")
def signup():
    """
    Register a new user and start a session.
    - Requires 'username', 'password', and 'password_confirmation' in JSON body.
    - Returns 201 with user data if successful.
    - Returns 400 if fields are missing, confirmation mismatch, or username already exists.
    """
    data = request.get_json()

    if not data.get("username") or not data.get("password"):
        return {"error": "Username and password are required."}, 400

    if data.get("password") != data.get("password_confirmation"):
        return {"error": "Password and confirmation do not match."}, 400

    if User.query.filter_by(email=data["username"]).first():
        return {"error": "That username is already taken."}, 400

    user = User(email=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    login_user(user)  # start a session automatically

    return {"id": user.id, "username": user.email}, 201


@bp.post("/login")
def login():
    """
    Log in an existing user.
    - Requires 'username' and 'password' in JSON body.
    - Returns 200 with user data if credentials are valid.
    - Returns 401 if username not found or password is incorrect.
    """
    data = request.get_json()
    user = User.query.filter_by(email=data.get("username")).first()
    if not user or not user.check_password(data.get("password", "")):
        return {"error": "Invalid username or password."}, 401

    login_user(user)
    return {"id": user.id, "username": user.email}, 200


@bp.delete("/logout")
def logout():
    """
    Log out the current user.
    - Returns {} whether or not a session existed.
    """
    if current_user.is_authenticated:
        logout_user()
    return {}, 200

@bp.get("/check_session")
def check_session():
    """
    Check if a user session is active.
    - Returns 200 with user data if logged in.
    - Returns 200 with {} if not logged in.
    """
    if not current_user.is_authenticated:
        return {}, 200
    return {"id": current_user.id, "username": current_user.email}, 200


auth_bp = bp