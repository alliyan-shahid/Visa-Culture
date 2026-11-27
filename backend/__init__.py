"""Application construction and configuration."""
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def create_app():
    # Load before importing Config: its class attributes read the environment.
    load_dotenv(PROJECT_ROOT / ".env", override=False)
    from .config import Config
    from .routes import register_routes

    app = Flask(__name__, template_folder=str(PROJECT_ROOT / "templates"),
                static_folder=str(PROJECT_ROOT / "static"), static_url_path="/static")
    app.config.from_object(Config)
    register_routes(app)
    return app
