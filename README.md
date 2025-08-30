# Flask Summative Lab – Sessions Backend

A summative assessment project implementing a secure REST API with session-based authentication (`Flask-Login`).

Users can register, log in, and manage personal notes securely. The backend is designed to integrate with the provided **client-with-sessions** frontend of the Productivity Tool project.

## Features
- User registration, login, logout
- Session-based authentication (Flask-Login + cookies)
- CRUD for user-owned Notes
- Notes index route supports pagination
- SQLite database with Flask-Migrate
- Seed script with demo user + notes

## Future Considerations
- **Frontend Integration**: Connect this backend to the provided React client (`client-with-sessions`) for full end-to-end functionality.
- **Production Database**: Replace SQLite with Postgres (or another production-ready RDBMS) for scalability.  
- **Security Enhancements**: Add CSRF protection, enforce stronger password rules, and consider rate limiting login/signup attempts.
- **Additional Resources**: Add additional resources beyond notes (e.g., tasks, expenses, journal entries) with corresponding CRUD + tests.
- **Testing Coverage**: Expand pytest coverage for edge cases (invalid JSON payloads, malformed requests, stress/performance tests).
- **Dev Experience**: Improve editor compatibility (e.g., Pipenv + VSCode/Pylance integration), Dockerize environment for smoother setup.

## Tech Stack
- **Backend**: Flask + Flask-Migrate + SQLAlchemy
- **Authentication**: Flask-Login (session-based, cookie auth)
- **Validation/Serialization**: Marshmallow
- **Database**: SQLite (default), configurable for Postgres
- **Testing**: pytest + Flask test client

## Installation & Setup
### 1. Clone & install dependencies
```
git clone git@github.com:nrathbone-turing/flask-c10-summative-lab-sessions-and-jwt-clients.git
cd flask-c10-summative-lab-sessions-and-jwt-clients

pipenv install --dev
pipenv shell
```

### 2. Initialize DB & migrations
```
flask db init
flask db migrate -m "init"
flask db upgrade
```

### 3. Seed sample data
```
python seed.py
```

This creates a demo user you can log in with:
- Email: `demo@example.com`
- Password: `password123`

### 4. Run server
```
python wsgi.py
# -> http://127.0.0.1:5000
```

## Data Model
```
User
- id          int, PK
- email       string, unique, required
- password    hashed string (bcrypt)

Note
- id          int, PK
- user_id     FK → User
- title       string, required
- body        text
- created_at  datetime
- updated_at  datetime
```

## API Endpoints

Note: All `/notes` routes and `/auth/me` are protected by login. Requests without an active session will return **401 Unauthorized**.

### Auth
- `POST /signup` – Register a new user
- `POST /login` – Log in as existing user
- `DELETE /logout` – Log out of session
- `GET /check_session` – Get current logged-in user

### Notes
- `GET /notes?page=1&per_page=10` – List notes (paginated)
- `POST /notes` – Create a new note
- `GET /notes/<id>` – Get a note by ID
- `PUT /notes/<id>` – Update a note
- `DELETE /notes/<id>` – Delete a note

## Example REST calls

```
# Register a new user
curl -X POST http://127.0.0.1:5000/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"secret","password_confirmation":"secret"}' \
  -c cookies.txt -b cookies.txt

# Login
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"secret"}' \
  -c cookies.txt -b cookies.txt

# Check session
curl http://127.0.0.1:5000/check_session -c cookies.txt -b cookies.txt

# Create a note
curl -X POST http://127.0.0.1:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"My first note","body":"Hello world"}' \
  -c cookies.txt -b cookies.txt

# List notes with pagination
curl "http://127.0.0.1:5000/notes?page=1&per_page=5" \
  -c cookies.txt -b cookies.txt
```

## Running Tests
```
pytest -v
```
Covers:
- Health endpoint
- User model password hashing
- Auth routes (signup, login, logout, check_session, invalid credentials)
- Notes routes (CRUD: create, list, get, update, delete)
- Pagination metadata
- Auth protection & unauthorized access
- 404 handling & validation errors


## Project Structure
```
flask-c10-summative-lab-sessions-and-jwt-clients/
├── app/
│   ├── __init__.py              # Flask app factory, register blueprints, init extensions
│   ├── extensions.py            # db, migrate, bcrypt, login_manager instances
│   ├── models.py                # SQLAlchemy models: User, Note
│   ├── schemas.py               # Marshmallow schemas for User and Note
│   └── routes/
│       ├── __init__.py          # Makes routes a package
│       ├── auth.py              # Auth routes: signup, login, logout, check_session
│       └── notes.py             # Notes CRUD routes (list, create, get, update, delete)
│
├── client-with-jwt/             # Provided frontend (JWT version) -- unused; use client-with-sessions for grading
├── client-with-sessions/        # Provided frontend (sessions version, target integration)
│
├── migrations/                  # Alembic migrations folder (auto-managed)
│   ├── versions/                # Auto-generated migration scripts
│   └── env.py / script.py.mako  # Migration config files
│
├── tests/                       # pytest suite for backend
│   ├── conftest.py              # Pytest fixtures (e.g., test client, db setup)
│   ├── test_app.py              # App-level tests (health check, etc.)
│   ├── test_models.py           # Model unit tests (password hashing, etc.)
│   ├── test_auth_routes.py      # Tests for signup, login, logout, check_session
│   └── test_notes_routes.py     # Tests for notes CRUD, pagination, auth protection
│
├── instance/                    # SQLite dev.db lives here (auto-created)
├── seed.py                      # Seed script: creates demo user + notes
├── wsgi.py                      # App entrypoint (used by flask run / python wsgi.py)
├── manage.py                    # Flask CLI entrypoint (db migrate/upgrade commands)
├── .flaskenv                    # Flask env vars (FLASK_APP, FLASK_DEBUG)
├── Pipfile                      # Pipenv dependency definitions
├── Pipfile.lock                 # Lockfile with exact dependency versions
├── .gitignore                   # Ignore rules for venv, db, pycache, etc.
└── README.md                    # Project documentation
```

## About This Repo
**Author:** Nick Rathbone | [GitHub Profile](https://github.com/nrathbone-turing)

This project is part of the Flatiron Full Auth Flask Backend summative assessment.

**License**: MIT — feel free to use or remix!