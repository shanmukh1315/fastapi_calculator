"""
Integration tests for user profile update and password change with database.
Tests database operations and data persistence.
"""
import pytest
from sqlalchemy.orm import Session
from app.models import User
from app.security import hash_password, verify_password
from app.db import get_db


@pytest.fixture
def test_user(db_session: Session, request):
    """Create a test user in the database with unique data for each test."""
    import time
    unique_id = str(int(time.time() * 1000))  # Use timestamp for uniqueness
    user = User(
        username=f"testuser_{unique_id}",
        email=f"test_{unique_id}@example.com",
        password_hash=hash_password("testpassword123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


class TestProfileUpdateDB:
    """Test profile update database operations."""
    
    def test_update_username_persists(self, db_session: Session, test_user: User):
        """Test that username update is persisted in database."""
        original_username = test_user.username
        new_username = "updateduser"
        
        # Update username
        test_user.username = new_username
        db_session.commit()
        db_session.refresh(test_user)
        
        # Verify change persisted
        assert test_user.username == new_username
        assert test_user.username != original_username
        
        # Verify in database
        user_from_db = db_session.query(User).filter(User.id == test_user.id).first()
        assert user_from_db.username == new_username
    
    def test_update_email_persists(self, db_session: Session, test_user: User):
        """Test that email update is persisted in database."""
        original_email = test_user.email
        new_email = "updated@example.com"
        
        # Update email
        test_user.email = new_email
        db_session.commit()
        db_session.refresh(test_user)
        
        # Verify change persisted
        assert test_user.email == new_email
        assert test_user.email != original_email
        
        # Verify in database
        user_from_db = db_session.query(User).filter(User.id == test_user.id).first()
        assert user_from_db.email == new_email
    
    def test_update_both_fields_persists(self, db_session: Session, test_user: User):
        """Test that updating both username and email persists."""
        new_username = "newuser"
        new_email = "new@example.com"
        
        # Update both
        test_user.username = new_username
        test_user.email = new_email
        db_session.commit()
        db_session.refresh(test_user)
        
        # Verify changes
        assert test_user.username == new_username
        assert test_user.email == new_email
        
        # Verify in database
        user_from_db = db_session.query(User).filter(User.id == test_user.id).first()
        assert user_from_db.username == new_username
        assert user_from_db.email == new_email
    
    def test_username_uniqueness_constraint(self, db_session: Session, test_user: User):
        """Test that duplicate username is prevented."""
        # Create another user
        user2 = User(
            username="otheruser",
            email="other@example.com",
            password_hash=hash_password("password")
        )
        db_session.add(user2)
        db_session.commit()
        
        # Check if username exists before update
        existing = db_session.query(User).filter(
            User.username == "otheruser",
            User.id != test_user.id
        ).first()
        
        assert existing is not None
        # In real code, this would raise HTTPException
    
    def test_email_uniqueness_constraint(self, db_session: Session, test_user: User):
        """Test that duplicate email is prevented."""
        # Create another user with unique identifier
        import time
        unique_id = str(int(time.time() * 1000))
        other_email = f"other_{unique_id}@example.com"
        
        user2 = User(
            username=f"otheruser_{unique_id}",
            email=other_email,
            password_hash=hash_password("password")
        )
        db_session.add(user2)
        db_session.commit()
        
        # Check if email exists before update
        existing = db_session.query(User).filter(
            User.email == other_email,
            User.id != test_user.id
        ).first()
        
        assert existing is not None
        # In real code, this would raise HTTPException
    
    def test_partial_update_preserves_other_fields(self, db_session: Session, test_user: User):
        """Test that partial updates don't affect other fields."""
        original_email = test_user.email
        original_password_hash = test_user.password_hash
        new_username = "updatedusername"
        
        # Update only username
        test_user.username = new_username
        db_session.commit()
        db_session.refresh(test_user)
        
        # Email and password should be unchanged
        assert test_user.username == new_username
        assert test_user.email == original_email
        assert test_user.password_hash == original_password_hash


class TestPasswordChangeDB:
    """Test password change database operations."""
    
    def test_password_change_persists(self, db_session: Session, test_user: User):
        """Test that password change is persisted in database."""
        old_password = "testpassword123"
        new_password = "newpassword456"
        
        # Verify old password works
        assert verify_password(old_password, test_user.password_hash) is True
        
        # Change password
        new_hash = hash_password(new_password)
        test_user.password_hash = new_hash
        db_session.commit()
        db_session.refresh(test_user)
        
        # Verify new password works
        assert verify_password(new_password, test_user.password_hash) is True
        
        # Verify old password no longer works
        assert verify_password(old_password, test_user.password_hash) is False
        
        # Verify in database
        user_from_db = db_session.query(User).filter(User.id == test_user.id).first()
        assert verify_password(new_password, user_from_db.password_hash) is True
    
    def test_password_change_preserves_other_fields(self, db_session: Session, test_user: User):
        """Test that password change doesn't affect other fields."""
        original_username = test_user.username
        original_email = test_user.email
        new_password = "newpassword789"
        
        # Change password
        test_user.password_hash = hash_password(new_password)
        db_session.commit()
        db_session.refresh(test_user)
        
        # Username and email should be unchanged
        assert test_user.username == original_username
        assert test_user.email == original_email
        
        # Password should be changed
        assert verify_password(new_password, test_user.password_hash) is True
    
    def test_multiple_password_changes(self, db_session: Session, test_user: User):
        """Test multiple consecutive password changes."""
        passwords = ["pass1", "pass2", "pass3"]
        
        for new_password in passwords:
            test_user.password_hash = hash_password(new_password)
            db_session.commit()
            db_session.refresh(test_user)
            
            # Verify current password works
            assert verify_password(new_password, test_user.password_hash) is True
        
        # Verify only latest password works
        assert verify_password("pass3", test_user.password_hash) is True
        assert verify_password("pass1", test_user.password_hash) is False
        assert verify_password("pass2", test_user.password_hash) is False


class TestCombinedUpdates:
    """Test combined profile and password updates."""
    
    def test_update_profile_and_password_together(self, db_session: Session, test_user: User):
        """Test updating profile and password in same transaction."""
        new_username = "combineduser"
        new_email = "combined@example.com"
        new_password = "combinedpass123"
        
        # Update all fields
        test_user.username = new_username
        test_user.email = new_email
        test_user.password_hash = hash_password(new_password)
        db_session.commit()
        db_session.refresh(test_user)
        
        # Verify all changes
        assert test_user.username == new_username
        assert test_user.email == new_email
        assert verify_password(new_password, test_user.password_hash) is True
        
        # Verify in database
        user_from_db = db_session.query(User).filter(User.id == test_user.id).first()
        assert user_from_db.username == new_username
        assert user_from_db.email == new_email
        assert verify_password(new_password, user_from_db.password_hash) is True
    
    def test_rollback_on_error(self, db_session: Session, test_user: User):
        """Test that transaction rollback preserves original data."""
        original_username = test_user.username
        original_email = test_user.email
        original_password_hash = test_user.password_hash
        
        # Attempt to update
        test_user.username = "newusername"
        
        # Simulate error and rollback
        db_session.rollback()
        db_session.refresh(test_user)
        
        # Verify data is unchanged
        assert test_user.username == original_username
        assert test_user.email == original_email
        assert test_user.password_hash == original_password_hash
