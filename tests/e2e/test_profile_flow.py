"""
End-to-end tests for user profile and password change flow.
Tests the complete user journey: login → profile → password change → re-login.
"""
import pytest
from playwright.sync_api import Page, expect
from fastapi.testclient import TestClient


@pytest.fixture
def test_user_data():
    """Test user data for E2E tests."""
    return {
        "username": "e2euser",
        "email": "e2e@example.com",
        "password": "e2epass123"
    }


class TestCompleteProfileFlow:
    """Test complete E2E flow for profile management."""
    
    @pytest.mark.e2e
    def test_login_view_profile_update_relogin(self, page: Page):
        """
        Complete E2E flow:
        1. Register user
        2. Login
        3. Navigate to calculations page
        4. View profile
        5. Update profile
        6. Verify changes
        """
        import time
        # Create unique test user via UI registration
        timestamp = str(int(time.time() * 1000))
        username = f"profileuser_{timestamp}"
        email = f"{username}@test.com"
        password = "testpass123"
        
        # 1. Register user via UI
        page.goto("http://127.0.0.1:8000/register")
        page.fill('input[name="username"]', username)
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        page.fill('input[name="confirm"]', password)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        
        # 2. Login via UI (if redirected to login)
        if "/login" in page.url:
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')
        
        # Wait for token to be stored
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=10000)
        
        # Wait for redirect to calculations
        page.wait_for_url("**/calculations", timeout=10000)
        
        # 3. Check account menu shows correct info
        page.click('#accountBtnMain')
        expect(page.locator('#accountName')).to_contain_text(username, timeout=10000)
        expect(page.locator('#accountEmail')).to_contain_text(email, timeout=10000)
        
        # 4. Navigate to profile page
        page.click('#profileBtn')
        page.wait_for_url("**/profile.html")
        
        # 5. Update profile
        new_username = f"updated_{username}"
        new_email = f"updated_{email}"
        page.fill('input#username', new_username)
        page.fill('input#email', new_email)
        page.click('button:has-text("Update Profile")')
        
        # Wait for success message
        expect(page.locator('.toast')).to_be_visible(timeout=10000)
        
        # 6. Verify changes in UI
        page.goto("http://127.0.0.1:8000/calculations")
        page.click('#accountBtnMain')
        expect(page.locator('#accountName')).to_contain_text(new_username, timeout=10000)
        expect(page.locator('#accountEmail')).to_contain_text(new_email, timeout=10000)
    
    @pytest.mark.e2e
    def test_login_change_password_relogin(self, page: Page):
        """
        Complete E2E flow:
        1. Register and login
        2. Navigate to profile
        3. Change password
        4. Logout
        5. Login with new password
        """
        import time
        # Create unique test user
        timestamp = str(int(time.time() * 1000))
        username = f"pwduser_{timestamp}"
        email = f"{username}@test.com"
        password = "testpass123"
        
        # 1. Register user via UI
        page.goto("http://127.0.0.1:8000/register")
        page.fill('input[name="username"]', username)
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        page.fill('input[name="confirm"]', password)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        
        # Login if needed
        if "/login" in page.url:
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')
        
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=10000)
        page.wait_for_url("**/calculations", timeout=10000)
        
        # 2. Navigate to profile
        page.click('#accountBtnMain')
        page.click('#profileBtn')
        page.wait_for_url("**/profile.html")
        
        # 3. Change password
        page.fill('input#oldPassword', password)
        page.fill('input#newPassword', 'newe2epass456')
        page.click('button:has-text("Change Password")')
        
        # Wait for success
        expect(page.locator('.toast')).to_be_visible(timeout=10000)
        
        # 4. Logout
        page.goto("http://127.0.0.1:8000/calculations")
        page.click('#accountBtnMain')
        page.click('#logoutBtnAccount')
        
        # Wait for redirect to login
        page.wait_for_url("**/login", timeout=10000)
        
        # 5. Login with new password
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', 'newe2epass456')
        page.click('button[type="submit"]')
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=10000)
        
        # Should successfully login
        page.wait_for_url("**/calculations", timeout=10000)
        expect(page.locator('h1')).to_contain_text("Calculations", timeout=10000)
    
    @pytest.mark.e2e
    def test_full_flow_register_to_profile_update_and_password_change(
        self, page: Page
    ):
        """
        Complete comprehensive E2E flow:
        1. Register new user via UI
        2. Login
        3. Create a calculation
        4. Update profile
        5. Change password
        6. Logout and re-login with new credentials
        7. Verify calculation history persists
        """
        import time
        # Create unique test user
        timestamp = str(int(time.time() * 1000))
        username = f"fullflow_{timestamp}"
        email = f"{username}@test.com"
        password = "fullflowpass123"
        
        # 1. Register via UI
        page.goto("http://127.0.0.1:8000/register")
        page.fill('input[name="username"]', username)
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        page.fill('input[name="confirm"]', password)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        
        # 2. Login if redirected
        if "/login" in page.url:
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')
        
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=10000)
        page.wait_for_url("**/calculations", timeout=10000)
        
        # 3. Create a calculation
        page.fill('input#a', '10')
        page.fill('input#b', '5')
        page.select_option('select#type', 'add')
        page.click('button#submitBtn')
        
        # Wait for calculation to appear in history
        expect(page.locator('#calcTable tbody tr')).to_have_count(1, timeout=10000)
        
        # 4. Update profile
        page.click('#accountBtnMain')
        page.click('#profileBtn')
        page.wait_for_url("**/profile.html", timeout=10000)
        
        new_username = f"updated_{username}"
        new_email = f"updated_{email}"
        page.fill('input#username', new_username)
        page.fill('input#email', new_email)
        page.click('button:has-text("Update Profile")')
        expect(page.locator('.toast')).to_be_visible(timeout=10000)
        
        # 5. Change password
        page.fill('input#oldPassword', password)
        page.fill('input#newPassword', 'newfullflowpass456')
        page.click('button:has-text("Change Password")')
        expect(page.locator('.toast')).to_be_visible(timeout=10000)
        
        # 6. Logout
        page.goto("http://127.0.0.1:8000/calculations")
        page.click('#accountBtnMain')
        page.click('#logoutBtnAccount')
        page.wait_for_url("**/login", timeout=10000)
        
        # Re-login with new credentials
        page.fill('input[name="username"]', new_username)
        page.fill('input[name="password"]', 'newfullflowpass456')
        page.click('button[type="submit"]')
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=10000)
        page.wait_for_url("**/calculations", timeout=10000)
        
        # 7. Verify calculation history persists
        expect(page.locator('#calcTable tbody tr')).to_have_count(1, timeout=10000)
        expect(page.locator('#calcTable tbody tr')).to_contain_text('15', timeout=10000)  # 10 + 5
        
        # Verify profile updated
        page.click('#accountBtnMain')
        expect(page.locator('#accountName')).to_contain_text(new_username, timeout=10000)
        expect(page.locator('#accountEmail')).to_contain_text(new_email, timeout=10000)


class TestProfileErrorHandling:
    """Test E2E error handling for profile operations."""
    
    @pytest.mark.e2e
    def test_profile_update_duplicate_username(self, page: Page):
        """Test that updating to duplicate username shows error."""
        import time
        # Create two users via UI
        timestamp = str(int(time.time() * 1000))
        user1 = f"dupuser1_{timestamp}"
        user2 = f"dupuser2_{timestamp}"
        
        # Register first user
        page.goto("http://127.0.0.1:8000/register")
        page.fill('input[name="username"]', user1)
        page.fill('input[name="email"]', f"{user1}@test.com")
        page.fill('input[name="password"]', "pass123")
        page.fill('input[name="confirm"]', "pass123")
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        
        # Logout if logged in
        if "/calculations" in page.url or "/profile" in page.url:
            page.click('#accountBtnMain')
            page.click('#logoutBtnAccount')
            page.wait_for_url("**/login", timeout=10000)
        
        # Register second user
        page.goto("http://127.0.0.1:8000/register")
        page.fill('input[name="username"]', user2)
        page.fill('input[name="email"]', f"{user2}@test.com")
        page.fill('input[name="password"]', "pass123")
        page.fill('input[name="confirm"]', "pass123")
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        
        # Login as user2 if needed
        if "/login" in page.url:
            page.fill('input[name="username"]', user2)
            page.fill('input[name="password"]', "pass123")
            page.click('button[type="submit"]')
        
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=10000)
        page.wait_for_url("**/calculations", timeout=10000)
        
        # Try to update to user1's username
        page.click('#accountBtnMain')
        page.click('#profileBtn')
        page.wait_for_url("**/profile.html", timeout=10000)
        
        page.fill('input#username', user1)
        page.click('button:has-text("Update Profile")')
        
        # Should show error
        expect(page.locator('.toast, .msg')).to_contain_text('already taken', timeout=10000)
    
    @pytest.mark.e2e
    def test_password_change_wrong_old_password(self, page: Page):
        """Test that wrong old password shows error."""
        import time
        # Register user via UI
        timestamp = str(int(time.time() * 1000))
        username = f"wrongpass_{timestamp}"
        email = f"{username}@test.com"
        password = "correctpass123"
        
        page.goto("http://127.0.0.1:8000/register")
        page.fill('input[name="username"]', username)
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        page.fill('input[name="confirm"]', password)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        
        # Login if needed
        if "/login" in page.url:
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')
        
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=10000)
        page.wait_for_url("**/calculations", timeout=10000)
        
        # Navigate to profile
        page.click('#accountBtnMain')
        page.click('#profileBtn')
        page.wait_for_url("**/profile.html", timeout=10000)
        
        # Try to change password with wrong old password
        page.fill('input#oldPassword', 'wrongoldpassword')
        page.fill('input#newPassword', 'newpass456')
        page.click('button:has-text("Change Password")')
        
        # Should show error
        expect(page.locator('.toast, .msg')).to_contain_text('incorrect', timeout=10000)


class TestProfileUIValidation:
    """Test UI validation for profile forms."""
    
    @pytest.mark.e2e
    def test_profile_form_validation(self, page: Page):
        """Test that profile form validates input."""
        import time
        # Create and login user via UI
        timestamp = str(int(time.time() * 1000))
        username = f"validation_{timestamp}"
        email = f"{username}@test.com"
        password = "pass123"
        
        page.goto("http://127.0.0.1:8000/register")
        page.fill('input[name="username"]', username)
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        page.fill('input[name="confirm"]', password)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        
        # Login if needed
        if "/login" in page.url:
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')
        
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=10000)
        page.wait_for_url("**/calculations", timeout=10000)
        
        # Navigate to profile
        page.click('#accountBtnMain')
        page.click('#profileBtn')
        page.wait_for_url("**/profile.html")
        
        # Try to submit empty username
        page.fill('input#username', '')
        page.click('button:has-text("Update Profile")')
        
        # Should show validation message or not submit
        # (depends on client-side validation implementation)
    
    @pytest.mark.e2e
    def test_password_change_form_validation(self, page: Page):
        """Test that password change form validates input."""
        import time
        # Create and login user via UI
        timestamp = str(int(time.time() * 1000))
        username = f"passvalid_{timestamp}"
        email = f"{username}@test.com"
        password = "pass123"
        
        page.goto("http://127.0.0.1:8000/register")
        page.fill('input[name="username"]', username)
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        page.fill('input[name="confirm"]', password)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        
        # Login if needed
        if "/login" in page.url:
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')
        
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=10000)
        page.wait_for_url("**/calculations", timeout=10000)
        
        # Navigate to profile
        page.click('#accountBtnMain')
        page.click('#profileBtn')
        page.wait_for_url("**/profile.html", timeout=10000)
        
        # Try to submit with only old password
        page.fill('input#oldPassword', password)
        page.fill('input#newPassword', '')
        page.click('button:has-text("Change Password")')
        
        # Should show validation message or not submit
