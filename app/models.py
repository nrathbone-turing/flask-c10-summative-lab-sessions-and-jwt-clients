# app/models.py
# SQLAlchemy models.
# - User model with bcrypt password hashing (Flask-Login compatible)
# - Note model with user ownership relationship

from flask_login import UserMixin
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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text)
