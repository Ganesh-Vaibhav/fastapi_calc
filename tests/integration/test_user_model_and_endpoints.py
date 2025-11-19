import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db import Base
from app.models import User
from main import app


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/fastapi_db_test",
)

engine = create_engine(TEST_DATABASE_URL, future=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session() -> Session:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session, monkeypatch):
    from app import users

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[users.get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_create_user_and_uniqueness(client, db_session):
    response = client.post(
        "/users/",
        json={"username": "alice", "email": "alice@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"

    # Duplicate username
    response_dup_username = client.post(
        "/users/",
        json={"username": "alice", "email": "alice2@example.com", "password": "password123"},
    )
    assert response_dup_username.status_code == 400

    # Duplicate email
    response_dup_email = client.post(
        "/users/",
        json={"username": "alice2", "email": "alice@example.com", "password": "password123"},
    )
    assert response_dup_email.status_code == 400


def test_login_success_and_failure(client, db_session):
    client.post(
        "/users/",
        json={"username": "bob", "email": "bob@example.com", "password": "password123"},
    )

    # Successful login
    response_ok = client.post(
        "/users/login",
        params={"username": "bob"},
        json={"password": "password123"},
    )
    # login endpoint currently uses query/body mix; call with form-like query only
    if response_ok.status_code == 422:
        response_ok = client.post("/users/login?username=bob&password=password123")
    assert response_ok.status_code == 200
    assert response_ok.json()["authenticated"] is True

    # Wrong password
    response_bad = client.post("/users/login?username=bob&password=wrong")
    assert response_bad.status_code == 401
