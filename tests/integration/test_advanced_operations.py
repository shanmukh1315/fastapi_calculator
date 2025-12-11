# tests/integration/test_advanced_operations.py
import pytest
from fastapi.testclient import TestClient


def test_percent_of_operation(client, auth_headers):
    """Test percent_of operation: 15% of 200 = 30"""
    response = client.post(
        "/api/calculations",
        headers=auth_headers,
        json={"a": 15, "b": 200, "type": "percent_of"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["a"] == 15
    assert data["b"] == 200
    assert data["type"] == "percent_of"
    assert data["result"] == 30.0


def test_nth_root_operation(client, auth_headers):
    """Test nth_root operation: 4th root of 16 = 2"""
    response = client.post(
        "/api/calculations",
        headers=auth_headers,
        json={"a": 16, "b": 4, "type": "nth_root"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["a"] == 16
    assert data["b"] == 4
    assert data["type"] == "nth_root"
    assert abs(data["result"] - 2.0) < 1e-10


def test_nth_root_validation(client, auth_headers):
    """Test nth_root validation: even root of negative number"""
    response = client.post(
        "/api/calculations",
        headers=auth_headers,
        json={"a": -16, "b": 2, "type": "nth_root"}
    )
    assert response.status_code == 400
    assert "even root" in response.json()["detail"].lower()


def test_log_base_operation(client, auth_headers):
    """Test log_base operation: log_2(8) = 3"""
    response = client.post(
        "/api/calculations",
        headers=auth_headers,
        json={"a": 8, "b": 2, "type": "log_base"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["a"] == 8
    assert data["b"] == 2
    assert data["type"] == "log_base"
    assert abs(data["result"] - 3.0) < 1e-10


def test_log_base_validation_negative_arg(client, auth_headers):
    """Test log_base validation: negative argument"""
    response = client.post(
        "/api/calculations",
        headers=auth_headers,
        json={"a": -8, "b": 2, "type": "log_base"}
    )
    assert response.status_code == 400
    assert "positive" in response.json()["detail"].lower()


def test_log_base_validation_base_one(client, auth_headers):
    """Test log_base validation: base cannot be 1"""
    response = client.post(
        "/api/calculations",
        headers=auth_headers,
        json={"a": 8, "b": 1, "type": "log_base"}
    )
    assert response.status_code == 400
    assert "cannot be 1" in response.json()["detail"].lower()
    assert "cannot be 1" in response.json()["detail"].lower()
