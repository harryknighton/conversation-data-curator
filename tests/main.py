"""Some example unit tests of the API and database CRUD code."""

from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.main import app, get_session
from backend.models import Base

# Set up database in memory
SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override session dependency
def override_get_session() -> Generator[Session, None, None]:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_session] = override_get_session


client = TestClient(app)


@pytest.fixture()
def test_db() -> Generator[None, None, None]:
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def _create_test_message() -> Any:
    response = client.post(
        "/messages/create",
        json={"content": "I'm a message!"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["content"] == "I'm a message!"
    assert "id" in data
    return data


def _read_messages() -> Any:
    response = client.get("/messages/")
    assert response.status_code == 200, response.text
    data = response.json()
    return data


def test_read_message(test_db: Any) -> None:
    _read_messages()


def test_create_message(test_db: Any) -> None:
    data = _create_test_message()
    message_id = data["id"]

    data = _read_messages()
    assert len(data) == 1
    assert data[0]["content"] == "I'm a message!"
    assert data[0]["id"] == message_id


def test_update_message(test_db: Any) -> None:
    data = _create_test_message()
    message_id = data["id"]

    response = client.post(
        "/messages/update/",
        json={"id": message_id, "content": "I'm an updated message!"},
    )
    assert response.status_code == 200, response.text
    data = response.json()

    data = _read_messages()
    assert len(data) == 1
    assert data[0]["content"] == "I'm an updated message!"
    assert data[0]["id"] == message_id


def test_delete_message(test_db: Any) -> None:
    data = _create_test_message()
    message_id = data["id"]

    response = client.post(
        "/messages/delete/",
        json={"id": message_id},
    )
    assert response.status_code == 200, response.text

    data = _read_messages()
    assert len(data) == 0


def test_creating_annotation_for_nonexistant_message_returns_error(
    test_db: Any,
) -> None:
    response = client.post(
        "/annotations/42/create/",
        json={
            "message_id": 42,
            "code_id": 1000,
            "start_idx": 5,
            "end_idx": 6,
        },
    )
    assert response.status_code == 404, response.text
