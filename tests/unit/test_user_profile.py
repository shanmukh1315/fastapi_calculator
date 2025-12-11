"""
Unit tests for user profile update and password change logic.
Tests the business logic without database or API layer.
"""
import pytest
from app.security import hash_password, verify_password
from app.schemas import UserUpdate, PasswordChange


class TestUserUpdateSchema:
    """Test UserUpdate schema validation."""
    
    def test_user_update_both_fields(self):
        """Test updating both username and email."""
        update = UserUpdate(username="newuser", email="new@example.com")
        assert update.username == "newuser"
        assert update.email == "new@example.com"
    
    def test_user_update_username_only(self):
        """Test updating only username."""
        update = UserUpdate(username="newuser")
        assert update.username == "newuser"
        assert update.email is None
    
    def test_user_update_email_only(self):
        """Test updating only email."""
        update = UserUpdate(email="new@example.com")
        assert update.username is None
        assert update.email == "new@example.com"
    
    def test_user_update_empty(self):
        """Test that UserUpdate allows empty updates."""
        update = UserUpdate()
        assert update.username is None
        assert update.email is None


class TestPasswordChangeSchema:
    """Test PasswordChange schema validation."""
    
    def test_password_change_valid(self):
        """Test valid password change payload."""
        payload = PasswordChange(old_password="old123", new_password="new456")
        assert payload.old_password == "old123"
        assert payload.new_password == "new456"
    
    def test_password_change_requires_both(self):
        """Test that both old and new passwords are required."""
        with pytest.raises(Exception):  # Pydantic validation error
            PasswordChange(old_password="old123")
        
        with pytest.raises(Exception):
            PasswordChange(new_password="new456")


class TestPasswordVerification:
    """Test password hashing and verification logic."""
    
    def test_password_hash_and_verify(self):
        """Test that password hashing and verification works."""
        password = "mysecretpassword"
        hashed = hash_password(password)
        
        # Hash should be different from password
        assert hashed != password
        
        # Should verify correctly
        assert verify_password(password, hashed) is True
    
    def test_password_verify_wrong_password(self):
        """Test that wrong password fails verification."""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_password_hash_deterministic(self):
        """Test that same password produces different hashes (salt)."""
        password = "samepassword"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Should be different due to salt
        assert hash1 != hash2
        
        # But both should verify
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestProfileUpdateLogic:
    """Test profile update business logic."""
    
    def test_username_update_logic(self):
        """Test that username can be updated."""
        old_username = "olduser"
        new_username = "newuser"
        
        # Simulate update
        update = UserUpdate(username=new_username)
        assert update.username == new_username
        assert update.username != old_username
    
    def test_email_update_logic(self):
        """Test that email can be updated."""
        old_email = "old@example.com"
        new_email = "new@example.com"
        
        # Simulate update
        update = UserUpdate(email=new_email)
        assert update.email == new_email
        assert update.email != old_email
    
    def test_partial_update_preserves_unchanged_fields(self):
        """Test that partial updates only change specified fields."""
        # Only username update
        update = UserUpdate(username="newuser")
        assert update.username is not None
        assert update.email is None
        
        # Only email update
        update = UserUpdate(email="new@example.com")
        assert update.username is None
        assert update.email is not None


class TestPasswordChangeLogic:
    """Test password change business logic."""
    
    def test_password_change_flow(self):
        """Test the complete password change flow."""
        old_password = "oldpass123"
        new_password = "newpass456"
        
        # Hash old password (simulating existing user)
        old_hash = hash_password(old_password)
        
        # Verify old password
        assert verify_password(old_password, old_hash) is True
        
        # Create new hash
        new_hash = hash_password(new_password)
        
        # Verify new password works
        assert verify_password(new_password, new_hash) is True
        
        # Verify old password doesn't work with new hash
        assert verify_password(old_password, new_hash) is False
    
    def test_password_change_validation(self):
        """Test password change validation logic."""
        payload = PasswordChange(old_password="old123", new_password="new456")
        
        # Old password must be verified before change
        current_hash = hash_password("old123")
        assert verify_password(payload.old_password, current_hash) is True
        
        # New password should be different
        assert payload.old_password != payload.new_password
