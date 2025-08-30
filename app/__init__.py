import os
from flask import Flask
from flask_login import LoginManager
from .extensions import db, migrate, bcrypt
from .models import User

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # --- Config ---
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-me")  # needed for sessions

    # --- Init extensions ---
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # --- Blueprints ---
    from .routes.auth import bp as auth_bp
    from .routes.notes import bp as notes_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(notes_bp, url_prefix="/notes")

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))