# manage.py
import os
import sys
from flask.cli import FlaskGroup
from flask_migrate import Migrate
from app import create_app, db
from app import models

# Make sure the current directory is on sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = create_app()
cli = FlaskGroup(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    cli()