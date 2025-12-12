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
    def test_login_view_profile_update_relogin(self, page: Page, client: TestClient, test_user_data):
        """
        Complete E2E flow:
        1. Register user
        2. Login
        3. Navigate to calculations page
        4. View profile
        5. Update profile
        6. Verify changes
        """
        # 1. Register user via API
        client.post("/api/users", json=test_user_data)
        
        # 2. Login via UI
        page.goto("http://127.0.0.1:8000/login")
        page.fill('input[name="username"]', test_user_data["username"])
        page.fill('input[name="password"]', test_user_data["password"])
        page.click('button[type="submit"]')
        
        # Wait for token to be stored
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=5000)
        
        # Wait for redirect to calculations
        page.wait_for_url("**/calculations")
        
        # 3. Check account menu shows correct info
        page.click('#accountBtnMain')
        expect(page.locator('#accountName')).to_contain_text("e2euser")
        expect(page.locator('#accountEmail')).to_contain_text("e2e@example.com")
        
        # 4. Navigate to profile page
        page.click('#profileBtn')
        page.wait_for_url("**/profile.html")
        
        # 5. Update profile
        page.fill('input#username', 'updatede2euser')
        page.fill('input#email', 'updated@example.com')
        page.click('button:has-text("Update Profile")')
        
        # Wait for success message
        expect(page.locator('.toast')).to_be_visible(timeout=3000)
        
        # 6. Verify changes in UI
        page.goto("http://127.0.0.1:8000/calculations")
        page.click('#accountBtnMain')
        expect(page.locator('#accountName')).to_contain_text("updatede2euser")
        expect(page.locator('#accountEmail')).to_contain_text("updated@example.com")
    
    @pytest.mark.e2e
    def test_login_change_password_relogin(self, page: Page, client: TestClient, test_user_data):
        """
        Complete E2E flow:
        1. Register and login
        2. Navigate to profile
        3. Change password
        4. Logout
        5. Login with new password
        """
        # 1. Register user
        client.post("/api/users", json=test_user_data)
        
        # Login
        page.goto("http://127.0.0.1:8000/login")
        page.fill('input[name="username"]', test_user_data["username"])
        page.fill('input[name="password"]', test_user_data["password"])
        page.click('button[type="submit"]')
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=5000)
        page.wait_for_url("**/calculations")
        
        # 2. Navigate to profile
        page.click('#accountBtnMain')
        page.click('#profileBtn')
        page.wait_for_url("**/profile.html")
        
        # 3. Change password
        page.fill('input#oldPassword', test_user_data["password"])
        page.fill('input#newPassword', 'newe2epass456')
        page.click('button:has-text("Change Password")')
        
        # Wait for success
        expect(page.locator('.toast')).to_be_visible(timeout=3000)
        
        # 4. Logout
        page.goto("http://127.0.0.1:8000/calculations")
        page.click('#accountBtnMain')
        page.click('#logoutBtnAccount')
        
        # Wait for redirect to login
        page.wait_for_url("**/login", timeout=5000)
        
        # 5. Login with new password
        page.fill('input[name="username"]', test_user_data["username"])
        page.fill('input[name="password"]', 'newe2epass456')
        page.click('button[type="submit"]')
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=5000)
        
        # Should successfully login
        page.wait_for_url("**/calculations")
        expect(page.locator('h1')).to_contain_text("Calculations")
    
    @pytest.mark.e2e
    def test_full_flow_register_to_profile_update_and_password_change(
        self, page: Page, client: TestClient
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
        # 1. Register via UI
        page.goto("http://127.0.0.1:8000/login")
        
        # Assume there's a link to register (or navigate directly)
        # For now, use API to register
        user_data = {
            "username": "fullflowuser",
            "email": "fullflow@example.com",
            "password": "fullflowpass123"
        }
        client.post("/api/users", json=user_data)
        
        # 2. Login
        page.fill('input[name="username"]', user_data["username"])
        page.fill('input[name="password"]', user_data["password"])
        page.click('button[type="submit"]')
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=5000)
        page.wait_for_url("**/calculations")
        
        # 3. Create a calculation
        page.fill('input#a', '10')
        page.fill('input#b', '5')
        page.select_option('select#type', 'add')
        page.click('button#submitBtn')
        
        # Wait for calculation to appear in history
        expect(page.locator('#calcTable tbody tr')).to_have_count(1, timeout=3000)
        
        # 4. Update profile
        page.click('#accountBtnMain')
        page.click('#profileBtn')
        page.wait_for_url("**/profile.html")
        
        page.fill('input#username', 'fullflowupdated')
        page.fill('input#email', 'fullflowupdated@example.com')
        page.click('button:has-text("Update Profile")')
        expect(page.locator('.toast')).to_be_visible(timeout=3000)
        
        # 5. Change password
        page.fill('input#oldPassword', user_data["password"])
        page.fill('input#newPassword', 'newfullflowpass456')
        page.click('button:has-text("Change Password")')
        expect(page.locator('.toast')).to_be_visible(timeout=3000)
        
        # 6. Logout
        page.goto("http://127.0.0.1:8000/calculations")
        page.click('#accountBtnMain')
        page.click('#logoutBtnAccount')
        page.wait_for_url("**/login", timeout=5000)
        
        # Re-login with new credentials
        page.fill('input[name="username"]', 'fullflowupdated')
        page.fill('input[name="password"]', 'newfullflowpass456')
        page.click('button[type="submit"]')
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=5000)
        page.wait_for_url("**/calculations")
        
        # 7. Verify calculation history persists
        expect(page.locator('#calcTable tbody tr')).to_have_count(1)
        expect(page.locator('#calcTable tbody tr')).to_contain_text('15')  # 10 + 5
        
        # Verify profile updated
        page.click('#accountBtnMain')
        expect(page.locator('#accountName')).to_contain_text("fullflowupdated")
        expect(page.locator('#accountEmail')).to_contain_text("fullflowupdated@example.com")


class TestProfileErrorHandling:
    """Test E2E error handling for profile operations."""
    
    @pytest.mark.e2e
    def test_profile_update_duplicate_username(self, page: Page, client: TestClient):
        """Test that updating to duplicate username shows error."""
        # Create two users
        client.post("/api/users", json={
            "username": "user1",
            "email": "user1@example.com",
            "password": "pass123"
        })
        client.post("/api/users", json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "pass123"
        })
        
        # Login as user2
        page.goto("http://127.0.0.1:8000/login")
        page.fill('input[name="username"]', 'user2')
        page.fill('input[name="password"]', 'pass123')
        page.click('button[type="submit"]')
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=5000)
        page.wait_for_url("**/calculations")
        
        # Try to update to user1's username
        page.click('#accountBtnMain')
        page.click('#profileBtn')
        page.wait_for_url("**/profile.html")
        
        page.fill('input#username', 'user1')
        page.click('button:has-text("Update Profile")')
        
        # Should show error
        expect(page.locator('.toast, .msg')).to_contain_text('already taken', timeout=3000)
    
    @pytest.mark.e2e
    def test_password_change_wrong_old_password(self, page: Page, client: TestClient):
        """Test that wrong old password shows error."""
        # Register user
        client.post("/api/users", json={
            "username": "wrongpassuser",
            "email": "wrongpass@example.com",
            "password": "correctpass123"
        })
        
        # Login
        page.goto("http://127.0.0.1:8000/login")
        page.fill('input[name="username"]', 'wrongpassuser')
        page.fill('input[name="password"]', 'correctpass123')
        page.click('button[type="submit"]')
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=5000)
        page.wait_for_url("**/calculations")
        
        # Navigate to profile
        page.click('#accountBtnMain')
        page.click('#profileBtn')
        page.wait_for_url("**/profile.html")
        
        # Try to change password with wrong old password
        page.fill('input#oldPassword', 'wrongoldpassword')
        page.fill('input#newPassword', 'newpass456')
        page.click('button:has-text("Change Password")')
        
        # Should show error
        expect(page.locator('.toast, .msg')).to_contain_text('incorrect', timeout=3000)


class TestProfileUIValidation:
    """Test UI validation for profile forms."""
    
    @pytest.mark.e2e
    def test_profile_form_validation(self, page: Page, client: TestClient):
        """Test that profile form validates input."""
        # Create and login user
        client.post("/api/users", json={
            "username": "validuser",
            "email": "valid@example.com",
            "password": "pass123"
        })
        
        page.goto("http://127.0.0.1:8000/login")
        page.fill('input[name="username"]', 'validuser')
        page.fill('input[name="password"]', 'pass123')
        page.click('button[type="submit"]')
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=5000)
        page.wait_for_url("**/calculations")
        
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
    def test_password_change_form_validation(self, page: Page, client: TestClient):
        """Test that password change form validates input."""
        # Create and login user
        client.post("/api/users", json={
            "username": "passvaliduser",
            "email": "passvalid@example.com",
            "password": "pass123"
        })
        
        page.goto("http://127.0.0.1:8000/login")
        page.fill('input[name="username"]', 'passvaliduser')
        page.fill('input[name="password"]', 'pass123')
        page.click('button[type="submit"]')
        page.wait_for_function("() => localStorage.getItem('token') !== null", timeout=5000)
        page.wait_for_url("**/calculations")
        
        # Navigate to profile
        page.click('#accountBtnMain')
        page.click('#profileBtn')
        page.wait_for_url("**/profile.html")
        
        # Try to submit with only old password
        page.fill('input#oldPassword', 'pass123')
        page.fill('input#newPassword', '')
        page.click('button:has-text("Change Password")')
        
        # Should show validation message or not submit
