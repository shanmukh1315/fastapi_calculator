def test_calculation_crud(client):
    # Create a user + login
    user = {"username": "calcuser", "email": "calcuser@example.com", "password": "secret123"}
    client.post("/api/users", json=user)
    login = {"username": "calcuser", "password": "secret123"}
    token = client.post("/api/users/login", json=login).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create
    payload = {"a": 10, "b": 5, "type": "add"}
    resp = client.post("/api/calculations", json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    calc_id = data["id"]
    assert data["result"] == 15

    # Read
    resp = client.get(f"/api/calculations/{calc_id}", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["a"] == 10

    # Update
    update_payload = {"a": 20, "b": 2, "type": "multiply"}
    resp = client.put(f"/api/calculations/{calc_id}", json=update_payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] == 40

    # Browse
    resp = client.get("/api/calculations", headers=headers)
    assert resp.status_code == 200
    items = resp.json()
    assert any(item["id"] == calc_id for item in items)

    # Delete
    resp = client.delete(f"/api/calculations/{calc_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["detail"] == "Deleted"


def test_division_by_zero_validation(client):
    payload = {"a": 1, "b": 0, "type": "divide"}
    # login first
    user = {"username": "calcuser2", "email": "calcuser2@example.com", "password": "secret123"}
    client.post("/api/users", json=user)
    login = {"username": "calcuser2", "password": "secret123"}
    token = client.post("/api/users/login", json=login).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post("/api/calculations", json=payload, headers=headers)
    # Pydantic validator should block division by zero
    assert resp.status_code == 422


def test_calculation_not_found_errors(client):
    # Unauthenticated requests should be rejected (401)
    resp = client.get("/api/calculations/99999")
    assert resp.status_code == 401

    # Malformed Authorization header
    resp = client.get("/api/calculations/99999", headers={"Authorization": "Token abc"})
    assert resp.status_code == 401

    # Invalid token
    resp = client.get("/api/calculations/99999", headers={"Authorization": "Bearer badtoken"})
    assert resp.status_code == 401

    # Token for non-existent user
    from app.security import create_access_token

    bad_token = create_access_token({"sub": "99999"})
    resp = client.get("/api/calculations/99999", headers={"Authorization": f"Bearer {bad_token}"})
    assert resp.status_code == 401

    # Authenticated user but calc not found => 404
    user = {"username": "nfuser", "email": "nfuser@example.com", "password": "secret123"}
    client.post("/api/users", json=user)
    login = {"username": "nfuser", "password": "secret123"}
    token = client.post("/api/users/login", json=login).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.get("/api/calculations/99999", headers=headers)
    assert resp.status_code == 404

    payload = {"a": 1, "b": 2, "type": "add"}
    resp = client.put("/api/calculations/99999", json=payload, headers=headers)
    assert resp.status_code == 404

    resp = client.delete("/api/calculations/99999", headers=headers)
    assert resp.status_code == 404


def test_calculation_forbidden(client):
    # Create user1 and a calculation
    u1 = {"username": "owner1", "email": "owner1@example.com", "password": "secret123"}
    client.post("/api/users", json=u1)
    t1 = client.post("/api/users/login", json={"username": "owner1", "password": "secret123"}).json()["access_token"]
    h1 = {"Authorization": f"Bearer {t1}"}
    resp = client.post("/api/calculations", json={"a": 3, "b": 3, "type": "add"}, headers=h1)
    calc_id = resp.json()["id"]

    # Create user2 and attempt to access user1's calc
    u2 = {"username": "intruder", "email": "intruder@example.com", "password": "secret123"}
    client.post("/api/users", json=u2)
    t2 = client.post("/api/users/login", json={"username": "intruder", "password": "secret123"}).json()["access_token"]
    h2 = {"Authorization": f"Bearer {t2}"}

    # Read -> 403
    resp = client.get(f"/api/calculations/{calc_id}", headers=h2)
    assert resp.status_code == 403

    # Update -> 403
    resp = client.put(f"/api/calculations/{calc_id}", json={"a":1,"b":1,"type":"add"}, headers=h2)
    assert resp.status_code == 403

    # Delete -> 403
    resp = client.delete(f"/api/calculations/{calc_id}", headers=h2)
    assert resp.status_code == 403
