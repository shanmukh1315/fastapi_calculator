import pytest
import time
from playwright.sync_api import Page

BASE = "http://127.0.0.1:8000"

@pytest.mark.skipif(False, reason="Run in CI where server is started")
def test_register_and_login_positive(page: Page):
    ts = str(int(time.time() * 1000000))
    email = f"user{ts}@example.com"
    username = f"user{ts}"
    password = "secret123"

    # Register
    page.goto(f"{BASE}/register")
    page.fill('#email', email)
    page.fill('#username', username)
    page.fill('#password', password)
    page.fill('#confirm', password)
    page.click("button[type=submit]")
    # wait for success message
    page.wait_for_selector('.success', timeout=3000)
    assert 'Registered successfully' in page.inner_text('#msg')

    # Login
    page.goto(f"{BASE}/login")
    page.fill('#username', username)
    page.fill('#password', password)
    page.click("button[type=submit]")
    # Wait for token to be stored in localStorage
    page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=5000)
    # token stored in localStorage
    token = page.evaluate("() => localStorage.getItem('token')")
    assert token and len(token) > 10

@pytest.mark.skipif(False, reason="Run in CI where server is started")
def test_register_short_password_shows_error(page: Page):
    page.goto(f"{BASE}/register")
    page.fill('#email', 'shortpass@example.com')
    page.fill('#username', 'shortpass')
    page.fill('#password', '123')
    page.fill('#confirm', '123')
    page.click("button[type=submit]")
    # client-side validation should show error immediately
    page.wait_for_selector('.error', timeout=2000)
    assert 'Password must be at least 6 characters' in page.inner_text('#msg')

@pytest.mark.skipif(False, reason="Run in CI where server is started")
def test_login_wrong_password_shows_invalid_credentials(page: Page):
    # Attempt to login with an existing username but wrong password.
    # We'll create a user via direct API call to ensure it exists.
    ts = str(int(time.time() * 1000000))
    username = f"user{ts}"
    email = f"user{ts}@example.com"
    password = "secret123"

    # Create via fetch (server API)
    page.goto(f"{BASE}/register")
    page.fill('#email', email)
    page.fill('#username', username)
    page.fill('#password', password)
    page.fill('#confirm', password)
    page.click("button[type=submit]")
    page.wait_for_selector('.success', timeout=3000)

    # Now attempt wrong login
    page.goto(f"{BASE}/login")
    page.fill('#username', username)
    page.fill('#password', 'wrongpassword')
    page.click("button[type=submit]")
    page.wait_for_selector('.error', timeout=3000)
    assert 'Invalid credentials' in page.inner_text('#msg')
