# tests/unit/test_startup.py
from app.main import on_startup

def test_on_startup_runs():
    """
    Call the startup handler directly to ensure it is covered.
    It should complete without raising any exceptions.
    """
    on_startup()
