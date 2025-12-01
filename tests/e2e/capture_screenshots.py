from playwright.sync_api import sync_playwright
import time

BASE = "http://127.0.0.1:8000"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # register page
    page.goto(f"{BASE}/register", wait_until="networkidle")
    page.screenshot(path="tests/e2e/screenshots/register_page.png", full_page=True)

    # login page
    page.goto(f"{BASE}/login", wait_until="networkidle")
    page.screenshot(path="tests/e2e/screenshots/login_page.png", full_page=True)

    # do a register+login flow to capture post-login state
    ts = str(int(time.time()))
    username = f"e2e_user_{ts}"
    email = f"{username}@example.com"
    password = "secret123"

    page.goto(f"{BASE}/register")
    page.fill('#email', email)
    page.fill('#username', username)
    page.fill('#password', password)
    page.fill('#confirm', password)
    page.click("button[type=submit]")
    page.wait_for_selector('.success', timeout=3000)
    page.screenshot(path=f"tests/e2e/screenshots/after_register_{ts}.png", full_page=True)

    page.goto(f"{BASE}/login")
    page.fill('#username', username)
    page.fill('#password', password)
    page.click("button[type=submit]")
    page.wait_for_selector('.success', timeout=3000)
    page.screenshot(path=f"tests/e2e/screenshots/after_login_{ts}.png", full_page=True)

    # capture docs for evidence too
    page.goto(f"{BASE}/docs", wait_until="networkidle")
    page.screenshot(path="tests/e2e/screenshots/docs.png", full_page=True)

    browser.close()
