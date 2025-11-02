from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Welcome to the FastAPI Calculator!"


def test_add_route():
    resp = client.get("/add?a=2&b=3")
    assert resp.status_code == 200
    assert resp.json()["result"] == 5


def test_subtract_route():
    resp = client.get("/subtract?a=5&b=2")
    assert resp.status_code == 200
    assert resp.json()["result"] == 3


def test_multiply_route():
    resp = client.get("/multiply?a=3&b=4")
    assert resp.status_code == 200
    assert resp.json()["result"] == 12


def test_divide_route_success():
    resp = client.get("/divide?a=10&b=2")
    assert resp.status_code == 200
    assert resp.json()["result"] == 5


def test_divide_route_error():
    resp = client.get("/divide?a=10&b=0")
    assert resp.status_code == 400
    assert "Division by zero" in resp.json()["detail"]
