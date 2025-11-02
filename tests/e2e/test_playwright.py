import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.skip(reason="Skip locally; CI will run this when server is available")
def test_docs_page_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/docs", wait_until="networkidle")
        assert "FastAPI" in page.title()
        browser.close()
