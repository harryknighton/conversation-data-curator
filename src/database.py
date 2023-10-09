"""Set up the database components."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # Required for sqlite3
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
