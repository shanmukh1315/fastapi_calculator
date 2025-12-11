# tests/integration/test_statistics_api.py
import pytest
from fastapi.testclient import TestClient


class TestStatisticsSummaryEndpoint:
    """Test /api/statistics/summary endpoint."""
    
    def test_summary_with_no_calculations(self, client, auth_headers):
        """Test statistics summary when user has no calculations."""
        response = client.get("/api/statistics/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_calculations"] == 0
        assert data["average_operand_a"] == 0
        assert data["average_operand_b"] == 0
        assert data["average_result"] == 0
        assert data["most_used_operation"] is None
        assert data["operations_breakdown"] == {}
        assert data["min_result"] is None
        assert data["max_result"] is None
    
    def test_summary_with_single_calculation(self, client, auth_headers):
        """Test statistics summary with one calculation."""
        # Create a calculation
        client.post(
            "/api/calculations",
            headers=auth_headers,
            json={"a": 10, "b": 5, "type": "add"}
        )
        
        response = client.get("/api/statistics/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_calculations"] == 1
        assert data["average_operand_a"] == 10.0
        assert data["average_operand_b"] == 5.0
        assert data["average_result"] == 15.0
        assert data["most_used_operation"] == "add"
        assert data["operations_breakdown"]["add"] == 1
        assert data["min_result"] == 15.0
        assert data["max_result"] == 15.0
    
    def test_summary_with_multiple_calculations(self, client, auth_headers):
        """Test statistics summary with multiple calculations."""
        # Create multiple calculations
        calcs = [
            {"a": 10, "b": 5, "type": "add"},      # 15
            {"a": 20, "b": 10, "type": "add"},     # 30
            {"a": 6, "b": 2, "type": "multiply"},  # 12
        ]
        
        for calc in calcs:
            client.post("/api/calculations", headers=auth_headers, json=calc)
        
        response = client.get("/api/statistics/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_calculations"] == 3
        assert data["average_operand_a"] == 12.0  # (10+20+6)/3
        assert data["average_operand_b"] == 5.67   # (5+10+2)/3, rounded
        assert data["average_result"] == 19.0     # (15+30+12)/3
        assert data["most_used_operation"] == "add"  # appears twice
        assert data["operations_breakdown"]["add"] == 2
        assert data["operations_breakdown"]["multiply"] == 1
        assert data["min_result"] == 12.0
        assert data["max_result"] == 30.0
    
    def test_summary_with_advanced_operations(self, client, auth_headers):
        """Test statistics with percent_of, nth_root, and log_base."""
        calcs = [
            {"a": 15, "b": 200, "type": "percent_of"},  # 30
            {"a": 16, "b": 4, "type": "nth_root"},       # 2
            {"a": 8, "b": 2, "type": "log_base"},        # 3
        ]
        
        for calc in calcs:
            client.post("/api/calculations", headers=auth_headers, json=calc)
        
        response = client.get("/api/statistics/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_calculations"] == 3
        assert "percent_of" in data["operations_breakdown"]
        assert "nth_root" in data["operations_breakdown"]
        assert "log_base" in data["operations_breakdown"]
        assert data["operations_breakdown"]["percent_of"] == 1
        assert data["operations_breakdown"]["nth_root"] == 1
        assert data["operations_breakdown"]["log_base"] == 1
    
    def test_summary_unauthorized(self, client):
        """Test statistics endpoint without authentication."""
        response = client.get("/api/statistics/summary")
        
        assert response.status_code == 401
    
    def test_summary_values_are_rounded(self, client, auth_headers):
        """Test that statistics values are rounded to 2 decimal places."""
        # Create calculations that result in repeating decimals
        calcs = [
            {"a": 10, "b": 3, "type": "divide"},  # 3.333...
            {"a": 7, "b": 3, "type": "divide"},   # 2.333...
        ]
        
        for calc in calcs:
            client.post("/api/calculations", headers=auth_headers, json=calc)
        
        response = client.get("/api/statistics/summary", headers=auth_headers)
        data = response.json()
        
        # Check that values are rounded
        assert isinstance(data["average_operand_a"], (int, float))
        assert isinstance(data["average_result"], (int, float))
        # Values should be rounded to 2 decimal places
        assert abs(data["average_operand_a"] - 8.5) < 0.01


class TestRecentStatisticsEndpoint:
    """Test /api/statistics/recent endpoint."""
    
    def test_recent_with_default_limit(self, client, auth_headers):
        """Test recent statistics with default limit of 10."""
        # Create 15 calculations
        for i in range(15):
            client.post(
                "/api/calculations",
                headers=auth_headers,
                json={"a": i, "b": 1, "type": "add"}
            )
        
        response = client.get("/api/statistics/recent", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["count"] == 10  # default limit
        assert len(data["operations_used"]) == 10
    
    def test_recent_with_custom_limit(self, client, auth_headers):
        """Test recent statistics with custom limit."""
        # Create 8 calculations
        for i in range(8):
            client.post(
                "/api/calculations",
                headers=auth_headers,
                json={"a": i, "b": 1, "type": "add"}
            )
        
        response = client.get("/api/statistics/recent?limit=5", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["count"] == 5
        assert len(data["operations_used"]) == 5
    
    def test_recent_with_no_calculations(self, client, auth_headers):
        """Test recent statistics when user has no calculations."""
        response = client.get("/api/statistics/recent", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["count"] == 0
        assert data["average_result"] == 0
        assert data["operations_used"] == []
    
    def test_recent_with_fewer_than_limit(self, client, auth_headers):
        """Test when total calculations < requested limit."""
        # Create only 3 calculations
        for i in range(3):
            client.post(
                "/api/calculations",
                headers=auth_headers,
                json={"a": i, "b": 1, "type": "add"}
            )
        
        response = client.get("/api/statistics/recent?limit=10", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["count"] == 3  # only 3 available
        assert len(data["operations_used"]) == 3
    
    def test_recent_operations_list(self, client, auth_headers):
        """Test that operations_used lists the operation types."""
        ops = ["add", "multiply", "subtract", "divide", "power"]
        for op in ops:
            client.post(
                "/api/calculations",
                headers=auth_headers,
                json={"a": 10, "b": 2, "type": op}
            )
        
        response = client.get("/api/statistics/recent?limit=5", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["count"] == 5
        # Operations should be in the list (order may vary due to ID ordering)
        assert all(op in ["add", "multiply", "subtract", "divide", "power"] 
                  for op in data["operations_used"])
    
    def test_recent_unauthorized(self, client):
        """Test recent endpoint without authentication."""
        response = client.get("/api/statistics/recent")
        
        assert response.status_code == 401


class TestStatisticsIsolation:
    """Test that statistics are isolated per user."""
    
    def test_statistics_only_show_user_calculations(self, client, auth_headers):
        """Test that statistics only include current user's calculations."""
        # Create calculations for current user
        for i in range(3):
            client.post(
                "/api/calculations",
                headers=auth_headers,
                json={"a": i, "b": 1, "type": "add"}
            )
        
        # Get statistics
        response = client.get("/api/statistics/summary", headers=auth_headers)
        data = response.json()
        
        # Should only count the 3 calculations we created
        assert data["total_calculations"] == 3


class TestStatisticsPerformance:
    """Test statistics endpoint performance with larger datasets."""
    
    def test_summary_with_many_calculations(self, client, auth_headers):
        """Test statistics performance with 50+ calculations."""
        # Create 50 calculations
        for i in range(50):
            op_type = ["add", "multiply", "subtract"][i % 3]
            client.post(
                "/api/calculations",
                headers=auth_headers,
                json={"a": i, "b": 1, "type": op_type}
            )
        
        response = client.get("/api/statistics/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_calculations"] == 50
        # Verify breakdown adds up
        breakdown_total = sum(data["operations_breakdown"].values())
        assert breakdown_total == 50
