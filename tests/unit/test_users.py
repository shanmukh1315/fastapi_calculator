"""
Unit tests for user authentication and profile management functions.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from app.users import get_current_user
from app.models import User
from app.security import hash_password


class TestGetCurrentUser:
    """Test get_current_user function."""
    
    def test_missing_authorization_header(self):
        """Test error when Authorization header is missing."""
        db = Mock(spec=Session)
        request = Mock(spec=Request)
        request.headers.get.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(db, request)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Missing token"
    
    def test_invalid_authorization_header_format(self):
        """Test error when Authorization header doesn't start with 'Bearer '."""
        db = Mock(spec=Session)
        request = Mock(spec=Request)
        request.headers.get.return_value = "InvalidFormat token123"
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(db, request)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Missing token"
    
    @patch('app.security.decode_access_token')
    def test_invalid_jwt_token(self, mock_decode):
        """Test error when JWT token is invalid."""
        from jose import JWTError
        
        db = Mock(spec=Session)
        request = Mock(spec=Request)
        request.headers.get.return_value = "Bearer invalid_token"
        mock_decode.side_effect = JWTError("Invalid token")
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(db, request)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid token"
    
    @patch('app.security.decode_access_token')
    def test_user_not_found_in_database(self, mock_decode):
        """Test error when user from token doesn't exist in database."""
        db = Mock(spec=Session)
        request = Mock(spec=Request)
        request.headers.get.return_value = "Bearer valid_token"
        mock_decode.return_value = {"sub": "999"}
        
        # Mock database query to return None
        query_mock = MagicMock()
        db.query.return_value = query_mock
        query_mock.filter.return_value.first.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(db, request)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "User not found"
    
    @patch('app.security.decode_access_token')
    def test_successful_user_retrieval(self, mock_decode):
        """Test successful user retrieval from valid token."""
        db = Mock(spec=Session)
        request = Mock(spec=Request)
        request.headers.get.return_value = "Bearer valid_token"
        mock_decode.return_value = {"sub": "1"}
        
        # Mock user object
        mock_user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            password_hash=hash_password("password")
        )
        
        # Mock database query
        query_mock = MagicMock()
        db.query.return_value = query_mock
        query_mock.filter.return_value.first.return_value = mock_user
        
        result = get_current_user(db, request)
        
        assert result == mock_user
        assert result.id == 1
        assert result.username == "testuser"
