from app import main as main_module


def test_root_and_operations(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["message"].startswith("Welcome")

    a = client.get("/add?a=2&b=3").json()
    assert a["result"] == 5

    s = client.get("/subtract?a=5&b=2").json()
    assert s["result"] == 3

    m = client.get("/multiply?a=3&b=4").json()
    assert m["result"] == 12


def test_divide_and_divide_by_zero(client):
    d = client.get("/divide?a=10&b=2").json()
    assert d["result"] == 5

    # division by zero should return 400
    resp = client.get("/divide?a=1&b=0")
    assert resp.status_code == 400
    assert "Division by zero" in resp.json().get("detail", "")


def test_custom_openapi_builds_and_is_idempotent():
    # Ensure openapi schema is generated and contains our Bearer security scheme
    # Reset any existing schema
    main_module.app.openapi_schema = None
    schema = main_module.app.openapi()
    assert "components" in schema
    assert "securitySchemes" in schema["components"]
    assert "Bearer" in schema["components"]["securitySchemes"]

    # Marking calculations endpoints: at least one path containing /api/calculations should have security
    found = False
    for path, item in schema.get("paths", {}).items():
        if "/api/calculations" in path:
            for method, details in item.items():
                if isinstance(details, dict) and details.get("security") is not None:
                    found = True
                    break
    assert found, "Expected at least one /api/calculations path to have security set"

    # Calling again should return the cached schema (idempotent)
    schema2 = main_module.app.openapi()
    assert schema2 is schema


def test_on_startup_callable():
    # Call the on_startup handler directly to cover its logic
    # It should run without raising
    main_module.on_startup()
