import pytest
import time
from playwright.sync_api import Page

BASE = "http://127.0.0.1:8000"

@pytest.mark.skipif(False, reason="Run in CI where server is started")
def test_bread_calculations_flow(page: Page):
    ts = str(int(time.time() * 1000000))
    email = f"calc{ts}@example.com"
    username = f"calc{ts}"
    password = "secret123"

    # register
    page.goto(f"{BASE}/register")
    page.fill('#email', email)
    page.fill('#username', username)
    page.fill('#password', password)
    page.fill('#confirm', password)
    page.click("button[type=submit]")
    page.wait_for_selector('.success', timeout=3000)

    # login
    page.goto(f"{BASE}/login")
    page.fill('#username', username)
    page.fill('#password', password)
    page.click("button[type=submit]")
    # Wait for token to be stored in localStorage
    page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=5000)

    # open calculations page
    page.goto(f"{BASE}/calculations")
    page.wait_for_selector('#submitBtn')

    # create calculation
    page.fill('#a', '7')
    page.select_option('#type', 'multiply')
    page.fill('#b', '6')
    page.click('#submitBtn')
    # wait for the new row to appear in the table
    page.wait_for_selector('table tbody tr', timeout=5000)
    rows = page.query_selector_all('table tbody tr')
    assert any('multiply' in r.inner_text() for r in rows)

    # edit first calculation: click edit button
    first_edit = page.query_selector('table tbody tr button.edit')
    assert first_edit
    first_edit.click()
    page.wait_for_selector('#cancelEdit', timeout=2000)
    page.fill('#a', '8')
    page.click('#submitBtn')
    # wait for table to refresh
    page.wait_for_selector('table tbody tr', timeout=3000)

    # delete it
    # locate delete button in the last row (avoid stale handles)
    page.wait_for_selector('table tbody tr:last-child button.del', timeout=3000)
    # click via selector to avoid stale ElementHandle
    page.once('dialog', lambda dialog: dialog.accept())
    page.click('table tbody tr:last-child button.del')
    page.wait_for_timeout(500)
