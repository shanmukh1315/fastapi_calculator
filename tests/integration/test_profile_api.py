"""
Integration tests for user profile and password change API endpoints.
Tests the complete API flow with authentication.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models import User
from app.security import hash_password, verify_password


@pytest.fixture
def authenticated_user(client: TestClient, db_session: Session):
    """Create a user and return authenticated client with token."""
    # Create user
    user_data = {
        "username": "authuser",
        "email": "auth@example.com",
        "password": "authpass123"
    }
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 200
    
    # Login to get token
    login_response = client.post("/api/users/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    return {
        "client": client,
        "token": token,
        "user_data": user_data,
        "db": db_session
    }


class TestGetCurrentUserAPI:
    """Test GET /api/users/me endpoint."""
    
    def test_get_current_user_authenticated(self, authenticated_user):
        """Test getting current user info with valid token."""
        client = authenticated_user["client"]
        token = authenticated_user["token"]
        
        response = client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "authuser"
        assert data["email"] == "auth@example.com"
        assert "id" in data
        assert "password_hash" not in data  # Should not expose password
    
    def test_get_current_user_no_token(self, client: TestClient):
        """Test getting current user without token fails."""
        response = client.get("/api/users/me")
        assert response.status_code == 401
    
    def test_get_current_user_invalid_token(self, client: TestClient):
        """Test getting current user with invalid token fails."""
        response = client.get(
            "/api/users/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401


class TestUpdateProfileAPI:
    """Test PUT /api/users/profile endpoint."""
    
    def test_update_username_success(self, authenticated_user):
        """Test updating username successfully."""
        client = authenticated_user["client"]
        token = authenticated_user["token"]
        
        response = client.put(
            "/api/users/profile",
            json={"username": "newusername"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newusername"
        assert data["email"] == "auth@example.com"  # Email unchanged
    
    def test_update_email_success(self, authenticated_user):
        """Test updating email successfully."""
        client = authenticated_user["client"]
        token = authenticated_user["token"]
        
        response = client.put(
            "/api/users/profile",
            json={"email": "newemail@example.com"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newemail@example.com"
        assert data["username"] == "authuser"  # Username unchanged
    
    def test_update_both_fields_success(self, authenticated_user):
        """Test updating both username and email."""
        client = authenticated_user["client"]
        token = authenticated_user["token"]
        
        response = client.put(
            "/api/users/profile",
            json={
                "username": "bothupdate",
                "email": "both@example.com"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "bothupdate"
        assert data["email"] == "both@example.com"
    
    def test_update_username_duplicate(self, authenticated_user, client: TestClient):
        """Test updating to existing username fails."""
        # Create another user
        client.post("/api/users", json={
            "username": "existinguser",
            "email": "existing@example.com",
            "password": "pass123"
        })
        
        # Try to update to existing username
        token = authenticated_user["token"]
        response = client.put(
            "/api/users/profile",
            json={"username": "existinguser"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 400
        assert "already taken" in response.json()["detail"].lower()
    
    def test_update_email_duplicate(self, authenticated_user, client: TestClient):
        """Test updating to existing email fails."""
        # Create another user
        client.post("/api/users", json={
            "username": "anotheruser",
            "email": "another@example.com",
            "password": "pass123"
        })
        
        # Try to update to existing email
        token = authenticated_user["token"]
        response = client.put(
            "/api/users/profile",
            json={"email": "another@example.com"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_update_without_token(self, client: TestClient):
        """Test updating profile without token fails."""
        response = client.put(
            "/api/users/profile",
            json={"username": "newname"}
        )
        assert response.status_code == 401
    
    def test_update_empty_payload(self, authenticated_user):
        """Test updating with empty payload succeeds but changes nothing."""
        client = authenticated_user["client"]
        token = authenticated_user["token"]
        
        response = client.put(
            "/api/users/profile",
            json={},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "authuser"  # Unchanged
        assert data["email"] == "auth@example.com"  # Unchanged


class TestChangePasswordAPI:
    """Test POST /api/users/change-password endpoint."""
    
    def test_change_password_success(self, authenticated_user):
        """Test changing password successfully."""
        client = authenticated_user["client"]
        token = authenticated_user["token"]
        
        response = client.post(
            "/api/users/change-password",
            json={
                "old_password": "authpass123",
                "new_password": "newpass456"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 204
        
        # Verify old password no longer works
        login_old = client.post("/api/users/login", json={
            "username": "authuser",
            "password": "authpass123"
        })
        assert login_old.status_code == 401
        
        # Verify new password works
        login_new = client.post("/api/users/login", json={
            "username": "authuser",
            "password": "newpass456"
        })
        assert login_new.status_code == 200
    
    def test_change_password_wrong_old_password(self, authenticated_user):
        """Test changing password with wrong old password fails."""
        client = authenticated_user["client"]
        token = authenticated_user["token"]
        
        response = client.post(
            "/api/users/change-password",
            json={
                "old_password": "wrongpassword",
                "new_password": "newpass456"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 400
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_change_password_without_token(self, client: TestClient):
        """Test changing password without token fails."""
        response = client.post(
            "/api/users/change-password",
            json={
                "old_password": "old",
                "new_password": "new"
            }
        )
        assert response.status_code == 401
    
    def test_change_password_missing_fields(self, authenticated_user):
        """Test changing password with missing fields fails."""
        client = authenticated_user["client"]
        token = authenticated_user["token"]
        
        # Missing new_password
        response = client.post(
            "/api/users/change-password",
            json={"old_password": "authpass123"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 422  # Validation error
        
        # Missing old_password
        response = client.post(
            "/api/users/change-password",
            json={"new_password": "newpass"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 422


class TestProfilePasswordIntegration:
    """Test combined profile and password operations."""
    
    def test_update_profile_then_password(self, authenticated_user):
        """Test updating profile then changing password."""
        client = authenticated_user["client"]
        token = authenticated_user["token"]
        
        # Update profile
        profile_response = client.put(
            "/api/users/profile",
            json={"username": "updateduser", "email": "updated@example.com"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert profile_response.status_code == 200
        
        # Change password
        password_response = client.post(
            "/api/users/change-password",
            json={
                "old_password": "authpass123",
                "new_password": "newpass789"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert password_response.status_code == 204
        
        # Login with new credentials
        login = client.post("/api/users/login", json={
            "username": "updateduser",
            "password": "newpass789"
        })
        assert login.status_code == 200
    
    def test_password_change_preserves_profile(self, authenticated_user):
        """Test that password change doesn't affect profile data."""
        client = authenticated_user["client"]
        token = authenticated_user["token"]
        
        # Change password
        client.post(
            "/api/users/change-password",
            json={
                "old_password": "authpass123",
                "new_password": "newpass999"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Check profile unchanged
        profile = client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert profile.status_code == 200
        data = profile.json()
        assert data["username"] == "authuser"
        assert data["email"] == "auth@example.com"
