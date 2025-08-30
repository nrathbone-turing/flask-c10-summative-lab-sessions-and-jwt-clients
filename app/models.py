# app/models.py
# SQLAlchemy models.
# - User model: unique email, bcrypt password hashing, Flask-Login integration
# - Note model: user-owned resource with title, body, and timestamp fields (created_at, updated_at)

from flask_login import UserMixin
from datetime import datetime
from .extensions import db, bcrypt

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, raw_password):
        self.password_hash = bcrypt.generate_password_hash(raw_password).decode()

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password_hash, raw_password)

class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False
    )
