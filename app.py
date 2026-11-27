"""Application entry point for Python, Flask CLI, and Gunicorn (app:app)."""
from backend import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
