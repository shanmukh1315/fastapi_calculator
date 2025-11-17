# tests/conftest.py
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.db import Base, get_db
from app.main import app

# Use Postgres in CI (TEST_DATABASE_URL is set there),
# and SQLite locally by default.
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "sqlite:///./test.db",
)

# Extra connect args only needed for SQLite
connect_args = {}
if TEST_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(TEST_DATABASE_URL, connect_args=connect_args)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Create all tables at the start of the test session
    and drop them at the end.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """
    Provide a fresh DB session for each test.
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """
    FastAPI TestClient that uses the test database session
    by overriding the get_db dependency.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Clean up overrides after the test
    app.dependency_overrides.clear()
