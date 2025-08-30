# Flask Summative Lab – Sessions Backend

This is a Flask API backend built with session-based authentication (`Flask-Login`).  
It is designed to work with the provided **client-with-sessions** frontend of the Productivity Tool project.  
Users can register, log in, and manage personal notes securely.

## Features
- User registration, login, logout
- Session-based authentication (Flask-Login + cookies)
- CRUD for user-owned Notes
- Notes index route supports pagination
- SQLite database with Flask-Migrate
- Seed script with demo user + notes

## Quick Start
```
pipenv install
pipenv shell
flask db init
flask db migrate -m "init"
flask db upgrade
python seed.py
python wsgi.py
```

Visit: http://localhost:5000

## Demo User
- Email: demo@example.com
- Password: password123

## Endpoints

### Auth
- POST /auth/register – Register a new user
- POST /auth/login – Log in as existing user
- POST /auth/logout – Log out of session
- GET /auth/me – Get current logged-in user

### Notes
- GET /notes?page=1&per_page=10 – List notes (paginated)
- POST /notes – Create a new note
- GET /notes/<id> – Get a note by ID
- PATCH /notes/<id> – Update a note
- DELETE /notes/<id> – Delete a note

## Repo Structure

```
flask-c10-summative-lab-sessions-and-jwt-clients/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/
│       ├── __init__.py
│       ├── auth.py
│       └── notes.py
│
├── client-with-jwt/               # provided frontend (JWT version)
├── client-with-sessions/          # frontend I’ll use (Sessions)
│
├── migrations/                    # DB migrations
├── tests/                         # pytest test suite
│   ├── conftest.py
│   ├── test_app.py
│   ├── test_models.py
│   ├── test_auth_routes.py
│   └── test_notes_routes.py
│
├── seed.py                        # seed script
├── wsgi.py                        # app entrypoint
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── README.md
```