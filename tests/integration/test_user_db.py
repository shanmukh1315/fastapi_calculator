# tests/integration/test_user_db.py
import pytest
from sqlalchemy.exc import IntegrityError

from app.models import User
from app.security import hash_password

def test_user_uniqueness_username(db_session):
    user1 = User(
        username="duplicate",
        email="user1@example.com",
        password_hash=hash_password("password123"),
    )
    db_session.add(user1)
    db_session.commit()

    user2 = User(
        username="duplicate",
        email="user2@example.com",
        password_hash=hash_password("password123"),
    )
    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.commit()
