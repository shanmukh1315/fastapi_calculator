# tests/e2e/test_advanced_operations_e2e.py
"""
End-to-end tests for advanced calculation operations.
Tests the complete flow: UI interaction → API → Database → UI update
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="module")
def test_user_credentials():
    """Provide test user credentials."""
    import time
    username = f"e2e_user_{int(time.time())}"
    return {
        "username": username,
        "email": f"{username}@test.com",
        "password": "TestPass123!"
    }


def register_and_login(page: Page, base_url: str, credentials: dict):
    """Helper to register and login a test user."""
    # Register
    page.goto(f"{base_url}/register")
    page.fill('input[name="username"]', credentials["username"])
    page.fill('input[name="email"]', credentials["email"])
    page.fill('input[name="password"]', credentials["password"])
    page.click('button[type="submit"]')
    
    # Wait for redirect to login or calculations
    page.wait_for_load_state("networkidle")
    
    # If on login page, login
    if "/login" in page.url:
        page.fill('input[name="username"]', credentials["username"])
        page.fill('input[name="password"]', credentials["password"])
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")


@pytest.mark.e2e
def test_percent_of_operation_e2e(page: Page, test_user_credentials):
    """
    E2E Test: Create percent_of calculation and verify UI updates.
    Scenario: Calculate 15% of 200 = 30
    """
    base_url = "http://127.0.0.1:8000"
    
    # Login
    register_and_login(page, base_url, test_user_credentials)
    page.goto(f"{base_url}/calculations")
    
    # Fill in calculation form
    page.fill('#a', '15')
    page.select_option('#type', 'percent_of')
    page.fill('#b', '200')
    
    # Verify helper text appears
    helper = page.locator('#operationHint')
    expect(helper).to_contain_text('15% of 200')
    
    # Verify live preview
    preview = page.locator('#previewText')
    expect(preview).to_have_text('30')
    
    # Submit calculation
    page.click('button:has-text("Create")')
    
    # Wait for toast notification
    page.wait_for_selector('.toast:has-text("created")', timeout=3000)
    
    # Verify calculation appears in table
    table = page.locator('#calcTable tbody')
    expect(table.locator('tr').last).to_contain_text('percent_of')
    expect(table.locator('tr').last).to_contain_text('30')
    
    # Verify stats update
    expect(page.locator('#statType')).to_have_text('percent_of')
    expect(page.locator('#statLast')).to_have_text('30')


@pytest.mark.e2e
def test_nth_root_operation_e2e(page: Page, test_user_credentials):
    """
    E2E Test: Create nth_root calculation and verify validation.
    Scenario: Calculate 4th root of 16 = 2
    """
    base_url = "http://127.0.0.1:8000"
    
    page.goto(f"{base_url}/calculations")
    
    # Fill in calculation form
    page.fill('#a', '16')
    page.select_option('#type', 'nth_root')
    page.fill('#b', '4')
    
    # Verify helper text
    helper = page.locator('#operationHint')
    expect(helper).to_contain_text('4th root of 16')
    
    # Verify live preview
    preview = page.locator('#previewText')
    expect(preview).to_have_text('2')
    
    # Submit calculation
    page.click('button:has-text("Create")')
    page.wait_for_selector('.toast:has-text("created")', timeout=3000)
    
    # Verify calculation in table
    table = page.locator('#calcTable tbody')
    expect(table.locator('tr').last).to_contain_text('nth_root')
    expect(table.locator('tr').last).to_contain_text('2')
    
    # Verify stats update
    expect(page.locator('#statType')).to_have_text('nth_root')


@pytest.mark.e2e
def test_nth_root_validation_e2e(page: Page, test_user_credentials):
    """
    E2E Test: Verify nth_root validation for even root of negative number.
    """
    base_url = "http://127.0.0.1:8000"
    
    page.goto(f"{base_url}/calculations")
    
    # Try to calculate even root of negative number
    page.fill('#a', '-16')
    page.select_option('#type', 'nth_root')
    page.fill('#b', '2')
    
    # Verify error message appears in preview
    error_msg = page.locator('#formMsg')
    expect(error_msg).to_contain_text('even root of negative')
    
    # Submit should be prevented or show error
    page.click('button:has-text("Create")')
    
    # Verify error message persists
    expect(error_msg).to_be_visible()


@pytest.mark.e2e
def test_log_base_operation_e2e(page: Page, test_user_credentials):
    """
    E2E Test: Create log_base calculation.
    Scenario: Calculate log_2(8) = 3
    """
    base_url = "http://127.0.0.1:8000"
    
    page.goto(f"{base_url}/calculations")
    
    # Fill in calculation form
    page.fill('#a', '8')
    page.select_option('#type', 'log_base')
    page.fill('#b', '2')
    
    # Verify helper text
    helper = page.locator('#operationHint')
    expect(helper).to_contain_text('log base 2 of 8')
    
    # Verify live preview (approximately 3)
    preview = page.locator('#previewText')
    expect(preview).to_have_text('3')
    
    # Submit calculation
    page.click('button:has-text("Create")')
    page.wait_for_selector('.toast:has-text("created")', timeout=3000)
    
    # Verify calculation in table
    table = page.locator('#calcTable tbody')
    expect(table.locator('tr').last).to_contain_text('log_base')
    expect(table.locator('tr').last).to_contain_text('3')


@pytest.mark.e2e
def test_log_base_validation_e2e(page: Page, test_user_credentials):
    """
    E2E Test: Verify log_base validation for base = 1.
    """
    base_url = "http://127.0.0.1:8000"
    
    page.goto(f"{base_url}/calculations")
    
    # Try to calculate log with base 1
    page.fill('#a', '8')
    page.select_option('#type', 'log_base')
    page.fill('#b', '1')
    
    # Verify error message appears
    error_msg = page.locator('#formMsg')
    expect(error_msg).to_contain_text('cannot be 1')
    
    # Submit should show error
    page.click('button:has-text("Create")')
    expect(error_msg).to_be_visible()


@pytest.mark.e2e
def test_all_operations_filter_e2e(page: Page, test_user_credentials):
    """
    E2E Test: Verify filtering works for new operation types.
    """
    base_url = "http://127.0.0.1:8000"
    
    page.goto(f"{base_url}/calculations")
    
    # Create one of each new operation type
    operations = [
        {'a': '10', 'type': 'percent_of', 'b': '100'},
        {'a': '27', 'type': 'nth_root', 'b': '3'},
        {'a': '100', 'type': 'log_base', 'b': '10'}
    ]
    
    for op in operations:
        page.fill('#a', op['a'])
        page.select_option('#type', op['type'])
        page.fill('#b', op['b'])
        page.click('button:has-text("Create")')
        page.wait_for_timeout(500)  # Wait for operation to complete
    
    # Test filter dropdown
    page.select_option('#filterType', 'percent_of')
    page.wait_for_timeout(300)
    
    # Verify only percent_of rows are visible
    visible_rows = page.locator('#calcTable tbody tr:visible')
    expect(visible_rows).to_have_count(1)
    expect(visible_rows.first).to_contain_text('percent_of')
    
    # Filter by nth_root
    page.select_option('#filterType', 'nth_root')
    page.wait_for_timeout(300)
    visible_rows = page.locator('#calcTable tbody tr:visible')
    expect(visible_rows.first).to_contain_text('nth_root')
    
    # Filter by log_base
    page.select_option('#filterType', 'log_base')
    page.wait_for_timeout(300)
    visible_rows = page.locator('#calcTable tbody tr:visible')
    expect(visible_rows.first).to_contain_text('log_base')
    
    # Show all
    page.select_option('#filterType', 'all')
    visible_rows = page.locator('#calcTable tbody tr:visible')
    expect(visible_rows.count()).to_be_greater_than(2)


@pytest.mark.e2e
def test_operation_pills_styling_e2e(page: Page, test_user_credentials):
    """
    E2E Test: Verify color-coded pills for new operations.
    """
    base_url = "http://127.0.0.1:8000"
    
    page.goto(f"{base_url}/calculations")
    
    # Create calculations if not already present
    page.fill('#a', '5')
    page.select_option('#type', 'percent_of')
    page.fill('#b', '20')
    page.click('button:has-text("Create")')
    page.wait_for_timeout(500)
    
    # Verify percent_of pill has correct class
    pill = page.locator('.pill-percent_of').first
    expect(pill).to_be_visible()
    expect(pill).to_have_text('percent_of')
    
    # Create nth_root
    page.fill('#a', '8')
    page.select_option('#type', 'nth_root')
    page.fill('#b', '3')
    page.click('button:has-text("Create")')
    page.wait_for_timeout(500)
    
    # Verify nth_root pill
    pill = page.locator('.pill-nth_root').first
    expect(pill).to_be_visible()
    
    # Create log_base
    page.fill('#a', '1000')
    page.select_option('#type', 'log_base')
    page.fill('#b', '10')
    page.click('button:has-text("Create")')
    page.wait_for_timeout(500)
    
    # Verify log_base pill
    pill = page.locator('.pill-log_base').first
    expect(pill).to_be_visible()
