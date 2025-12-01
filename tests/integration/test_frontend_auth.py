import json
from app.security import hash_password
from app.models import User


def test_register_page_serves_html(client):
    resp = client.get("/register")
    assert resp.status_code == 200
    assert "Register" in resp.text


def test_login_page_serves_html(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert "Login" in resp.text


def test_register_api_creates_user(client, db_session):
    payload = {"username": "testuser1", "email": "test1@example.com", "password": "secret123"}
    resp = client.post("/register", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]


def test_login_api_returns_token(client, db_session):
    # insert user directly (use distinct username to avoid collisions)
    pw = "mypassword"
    user = User(username="fe_loginuser", email="fe_login@example.com", password_hash=hash_password(pw))
    db_session.add(user)
    db_session.commit()

    resp = client.post("/login", json={"username": "fe_loginuser", "password": pw})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data


def test_register_top_level_duplicate_username(client):
    payload1 = {"username": "dupuser", "email": "dup1@example.com", "password": "secret123"}
    payload2 = {"username": "dupuser", "email": "dup2@example.com", "password": "secret123"}
    r1 = client.post("/register", json=payload1)
    assert r1.status_code == 200
    r2 = client.post("/register", json=payload2)
    assert r2.status_code == 400
    assert r2.json()["detail"] == "Username already taken"


def test_register_top_level_duplicate_email(client):
    payload1 = {"username": "dupe1", "email": "dupe@example.com", "password": "secret123"}
    payload2 = {"username": "dupe2", "email": "dupe@example.com", "password": "secret123"}
    r1 = client.post("/register", json=payload1)
    assert r1.status_code == 200
    r2 = client.post("/register", json=payload2)
    assert r2.status_code == 400
    assert r2.json()["detail"] == "Email already registered"


def test_login_top_level_invalid_credentials(client):
    # no such user -> 401
    resp = client.post("/login", json={"username": "noexists", "password": "x"})
    assert resp.status_code == 401
