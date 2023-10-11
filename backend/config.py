"""Configure the app."""

from pathlib import Path

ROOT_DIR = Path(__file__).absolute().parent.parent

DATABASE_URL = "sqlite+pysqlite:///./app.db"

CORS_ORIGINS = [
    "http://localhost:5173/",
]
