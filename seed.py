# seed.py
# Database seeding script.
# - Drops and recreates tables
# - Adds demo user (demo@example.com / password123)
# - Adds sample notes for testing

from faker import Faker
from app import create_app
from app.extensions import db
from app.models import User, Note

fake = Faker()
app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(email="demo@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.flush()

    for _ in range(5):
        note = Note(user_id=user.id, title=fake.sentence(), body=fake.paragraph())
        db.session.add(note)

    db.session.commit()
    print("Seeded demo user demo@example.com / password123 and 5 notes")
