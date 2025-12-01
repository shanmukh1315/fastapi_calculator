# tests/integration/test_users_api.py

def test_create_user_success(client):
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "secret123",
    }
    resp = client.post("/api/users", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data
    assert "created_at" in data


def test_create_user_duplicate_username(client):
    # First user
    payload1 = {
        "username": "bob",
        "email": "bob1@example.com",
        "password": "secret123",
    }
    # Second user with same username but different email
    payload2 = {
        "username": "bob",
        "email": "bob2@example.com",
        "password": "secret123",
    }

    client.post("/api/users", json=payload1)
    resp = client.post("/api/users", json=payload2)

    assert resp.status_code == 400
    assert resp.json()["detail"] == "Username already taken"


def test_create_user_duplicate_email(client):
    # First user
    payload1 = {
        "username": "charlie1",
        "email": "charlie@example.com",
        "password": "secret123",
    }
    # Second user with same email but different username
    payload2 = {
        "username": "charlie2",
        "email": "charlie@example.com",
        "password": "secret123",
    }

    client.post("/api/users", json=payload1)
    resp = client.post("/api/users", json=payload2)

    assert resp.status_code == 400
    assert resp.json()["detail"] == "Email already registered"


def test_login_success(client):
    payload = {
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "secret123",
    }
    # register
    client.post("/api/users", json=payload)

    login_payload = {"username": "loginuser", "password": "secret123"}
    resp = client.post("/api/users/login", json=login_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data


def test_login_fail_wrong_password(client):
    payload = {
        "username": "loginuser2",
        "email": "loginuser2@example.com",
        "password": "secret123",
    }
    client.post("/api/users", json=payload)
    login_payload = {"username": "loginuser2", "password": "wrongpass"}
    resp = client.post("/api/users/login", json=login_payload)
    assert resp.status_code == 401


def test_login_user_not_found(client):
    # login with unknown user
    login_payload = {"username": "no_such_user", "password": "whatever"}
    resp = client.post("/api/users/login", json=login_payload)
    assert resp.status_code == 401


def test_register_alias(client):
    payload = {"username": "aliasuser", "email": "alias@example.com", "password": "secret123"}
    resp = client.post("/api/users/register", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "aliasuser"
