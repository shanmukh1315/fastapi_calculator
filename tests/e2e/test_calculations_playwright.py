import pytest
import time
from playwright.async_api import async_playwright

BASE = "http://127.0.0.1:8000"

@pytest.mark.asyncio
@pytest.mark.skipif(False, reason="Run in CI where server is started")
async def test_bread_calculations_flow():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        ts = str(int(time.time()))
        email = f"calc{ts}@example.com"
        username = f"calc{ts}"
        password = "secret123"

        # register
        await page.goto(f"{BASE}/register")
        await page.fill('#email', email)
        await page.fill('#username', username)
        await page.fill('#password', password)
        await page.fill('#confirm', password)
        await page.click("button[type=submit]")
        await page.wait_for_selector('.success', timeout=3000)

        # login
        await page.goto(f"{BASE}/login")
        await page.fill('#username', username)
        await page.fill('#password', password)
        await page.click("button[type=submit]")
        # Wait for token to be stored in localStorage
        await page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=5000)

        # open calculations page
        await page.goto(f"{BASE}/calculations")
        await page.wait_for_selector('#submitBtn')

        # create calculation
        await page.fill('#a', '7')
        await page.select_option('#type', 'multiply')
        await page.fill('#b', '6')
        await page.click('#submitBtn')
        # wait for the new row to appear in the table
        await page.wait_for_selector('table tbody tr', timeout=5000)
        rows = await page.query_selector_all('table tbody tr')
        inner_texts = [await r.inner_text() for r in rows]
        assert any('multiply' in text for text in inner_texts)

        # edit first calculation: click edit button
        first_edit = await page.query_selector('table tbody tr button.edit')
        assert first_edit
        await first_edit.click()
        await page.wait_for_selector('#cancelEdit', timeout=2000)
        await page.fill('#a', '8')
        await page.click('#submitBtn')
        # wait for table to refresh
        await page.wait_for_selector('table tbody tr', timeout=3000)

        # delete it
        # locate delete button in the last row (avoid stale handles)
        await page.wait_for_selector('table tbody tr:last-child button.del', timeout=3000)
        # click via selector to avoid stale ElementHandle
        page.once('dialog', lambda dialog: dialog.accept())
        await page.click('table tbody tr:last-child button.del')
        await page.wait_for_timeout(500)

        await browser.close()
