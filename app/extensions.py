# app/extensions.py
# Centralized extension initialization.
# Holds instances of db, migrate, bcrypt for import in other modules.

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()