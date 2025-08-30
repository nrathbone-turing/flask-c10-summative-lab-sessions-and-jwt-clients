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
- **Frontend Integration**: Connect this backend to the provided React client (`client-with-sessions`) for a complete user experience.  
- **Production Database**: Swap SQLite for Postgres (or another RDBMS) for scalability.  
- **Security Enhancements**: Add CSRF protection, stronger password policies, and rate limiting.  
- **Additional Resources**: Extend beyond notes (e.g., tasks, expenses, journal entries) with more models and CRUD endpoints.  
- **Testing Coverage**: Add more validation/error-handling tests (e.g., empty note title updates, invalid JSON payloads).  

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
- `POST /auth/register` – Register a new user
- `POST /auth/login` – Log in as existing user
- `POST /auth/logout` – Log out of session
- `GET /auth/me` – Get current logged-in user

### Notes
- `GET /notes?page=1&per_page=10` – List notes (paginated)
- `POST /notes` – Create a new note
- `GET /notes/<id>` – Get a note by ID
- `PATCH /notes/<id>` – Update a note
- `DELETE /notes/<id>` – Delete a note

## Example REST calls

```
# Register a new user
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"new@example.com","password":"secret"}' \
  -c cookies.txt -b cookies.txt

# Login
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"new@example.com","password":"secret"}' \
  -c cookies.txt -b cookies.txt

# Check session
curl http://127.0.0.1:5000/auth/me -c cookies.txt -b cookies.txt

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
- App health endpoint
- User model password hashing
- Auth routes (register, login, logout, me, duplicate/invalid credentials)
- Notes routes (CRUD, pagination, auth protection, 404s)

## Project Structure

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

## About This Repo
**Author:** Nick Rathbone | [GitHub Profile](https://github.com/nrathbone-turing)

This project is part of the Flatiron Full Auth Flask Backend summative assessment.

**License**: MIT — feel free to use or remix!