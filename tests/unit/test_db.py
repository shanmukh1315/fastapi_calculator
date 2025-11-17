# tests/unit/test_db.py
from sqlalchemy.orm import Session
from app.db import get_db

def test_get_db_yields_session():
    """
    Ensure get_db yields a Session and closes cleanly.
    This covers the body of get_db for 100% coverage in app/db.py.
    """
    gen = get_db()
    db = next(gen)

    assert isinstance(db, Session)

    # Exhaust generator to trigger the "finally" block
    try:
        next(gen)
    except StopIteration:
        pass
