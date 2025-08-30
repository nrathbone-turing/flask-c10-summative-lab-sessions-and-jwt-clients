# wsgi.py
# Application entry point.
# Creates app via factory and runs Flask development server.

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=5555, debug=True)
