import pytest
import time
from playwright.async_api import async_playwright

BASE = "http://127.0.0.1:8000"

@pytest.mark.asyncio
@pytest.mark.skipif(False, reason="Run in CI where server is started")
async def test_register_and_login_positive():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        ts = str(int(time.time()))
        email = f"user{ts}@example.com"
        username = f"user{ts}"
        password = "secret123"

        # Register
        await page.goto(f"{BASE}/register")
        await page.fill('#email', email)
        await page.fill('#username', username)
        await page.fill('#password', password)
        await page.fill('#confirm', password)
        await page.click("button[type=submit]")
        # wait for success message
        await page.wait_for_selector('.success', timeout=3000)
        assert 'Registered successfully' in await page.inner_text('#msg')

        # Login
        await page.goto(f"{BASE}/login")
        await page.fill('#username', username)
        await page.fill('#password', password)
        await page.click("button[type=submit]")
        # Wait for token to be stored in localStorage
        await page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=5000)
        # token stored in localStorage
        token = await page.evaluate("() => localStorage.getItem('token')")
        assert token and len(token) > 10

        await browser.close()

@pytest.mark.asyncio
@pytest.mark.skipif(False, reason="Run in CI where server is started")
async def test_register_short_password_shows_error():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(f"{BASE}/register")
        await page.fill('#email', 'shortpass@example.com')
        await page.fill('#username', 'shortpass')
        await page.fill('#password', '123')
        await page.fill('#confirm', '123')
        await page.click("button[type=submit]")
        # client-side validation should show error immediately
        await page.wait_for_selector('.error', timeout=2000)
        assert 'Password must be at least 6 characters' in await page.inner_text('#msg')

        await browser.close()

@pytest.mark.asyncio
@pytest.mark.skipif(False, reason="Run in CI where server is started")
async def test_login_wrong_password_shows_invalid_credentials():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Attempt to login with an existing username but wrong password.
        # We'll create a user via direct API call to ensure it exists.
        ts = str(int(time.time()))
        username = f"user{ts}"
        email = f"user{ts}@example.com"
        password = "secret123"

        # Create via fetch (server API)
        await page.goto(f"{BASE}/register")
        await page.fill('#email', email)
        await page.fill('#username', username)
        await page.fill('#password', password)
        await page.fill('#confirm', password)
        await page.click("button[type=submit]")
        await page.wait_for_selector('.success', timeout=3000)

        # Now attempt wrong login
        await page.goto(f"{BASE}/login")
        await page.fill('#username', username)
        await page.fill('#password', 'wrongpassword')
        await page.click("button[type=submit]")
        await page.wait_for_selector('.error', timeout=3000)
        assert 'Invalid credentials' in await page.inner_text('#msg')

        await browser.close()
