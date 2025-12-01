# FastAPI Calculator

A fully containerized FastAPI Calculator Web Application integrated with PostgreSQL and pgAdmin.

Features:

- Calculator REST API with basic arithmetic operations
- Secure `User` model (password hashing)
- Calculation model stored with SQLAlchemy and linked to users
- Pydantic validation for request/response models
- Unit, integration, and E2E tests with `pytest` and `playwright`
- GitHub Actions CI to run tests, report coverage, and build/push a Docker image

---

## Quick Links

- API docs (locally): `http://localhost:8000/docs`
- App root (locally): `http://localhost:8000/`

---

## API Endpoints

Public arithmetic endpoints (also available via `app/operations.py` and `app/calculation_factory.py`):

- `GET /add?a=<float>&b=<float>`
- `GET /subtract?a=<float>&b=<float>`
- `GET /multiply?a=<float>&b=<float>`
- `GET /divide?a=<float>&b=<float>`

User & calculation REST API (prefixed with `/api`):

- `POST /api/users` — create a user (returns `UserRead` schema)
- `POST /api/users/register` — alias for register
- `POST /api/users/login` — returns JWT `access_token`
- `GET /api/calculations` — browse (requires Bearer token)
- `POST /api/calculations` — create calculation (requires Bearer token)
- `GET /api/calculations/{id}` — read calculation (user-scoped)
- `PUT /api/calculations/{id}` — update calculation (user-scoped)
- `DELETE /api/calculations/{id}` — delete calculation (user-scoped)

Authentication: endpoints under `/api/calculations` require a Bearer JWT token obtained from `POST /api/users/login`.

OpenAPI/Swagger UI includes an Authorize button so you can paste `Bearer <token>` to test protected endpoints.

---

## Data Models (high level)

- `User` (`app/models.py`) — `id`, `username`, `email`, `password_hash`, `created_at`
- `Calculation` (`app/models.py`) — `id`, `a`, `type` (`add|subtract|multiply|divide`), `b`, `result`, `user_id`

Validation rules (in `app/schemas.py`):

- `UserCreate` validates `username`, `email` (as `EmailStr`) and `password` length
- `CalculationCreate` rejects division-by-zero when `type == "divide"`

Computation is centralized by `app/calculation_factory.py` which returns operation objects that implement `.compute(a,b)`.

---

## Testing

Run tests locally (virtualenv recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest --maxfail=1 -q
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

E2E Playwright test (requires `playwright` browsers):

```bash
playwright install chromium
pytest tests/e2e/test_playwright.py
```

Frontend pages

- `http://localhost:8000/register` — simple registration page with client-side validation.
- `http://localhost:8000/login` — simple login page that stores JWT in `localStorage` on success.

To run the frontend and E2E locally:

```bash
# start the server
uvicorn app.main:app --reload
# in another terminal: install playwright browsers
playwright install chromium
# run the E2E tests (they target http://127.0.0.1:8000)
pytest tests/e2e -q
```

CI (GitHub Actions) runs the same tests and a coverage gate (currently set to 95% line coverage).

---

## Manual verification via OpenAPI (Swagger UI)

Use the interactive docs to manually verify Module 12 BREAD flows and auth:

1. Start the app locally:

```bash
uvicorn app.main:app --reload
```

2. Open the interactive docs at `http://localhost:8000/docs`.

3. Register a user (POST `/api/users` or `/api/users/register`):

Request example (JSON):

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "secret123"
}
```

4. Login (POST `/api/users/login`) and copy the `access_token` from the response:

Request example (JSON):

```json
{
  "username": "alice",
  "password": "secret123"
}
```

Response example:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

5. Click the "Authorize" button in Swagger UI and enter the value `Bearer <access_token>`.

6. Test BREAD operations under `/api/calculations` (examples):

- Create (POST `/api/calculations`):

```json
{
  "a": 10,
  "type": "add",
  "b": 5
}
```

- Browse (GET `/api/calculations`) — lists the authenticated user's calculations.
- Read (GET `/api/calculations/{id}`) — returns specific calculation if owned.
- Update (PUT `/api/calculations/{id}`) — modify fields and recompute result.
- Delete (DELETE `/api/calculations/{id}`) — remove calculation.

7. Curl examples (replace `localhost:8000` if running elsewhere):

```bash
# register
curl -s -X POST http://localhost:8000/api/users -H "Content-Type: application/json" -d '{"username":"alice","email":"alice@example.com","password":"secret123"}'

# login -> extract token (requires jq)
TOKEN=$(curl -s -X POST http://localhost:8000/api/users/login -H "Content-Type: application/json" -d '{"username":"alice","password":"secret123"}' | jq -r .access_token)

# create a calculation
curl -s -X POST http://localhost:8000/api/calculations -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"a":10,"type":"add","b":5}'

# list calculations
curl -s -X GET http://localhost:8000/api/calculations -H "Authorization: Bearer $TOKEN"

# get a calculation (id 1)
curl -s -X GET http://localhost:8000/api/calculations/1 -H "Authorization: Bearer $TOKEN"

# update calculation (id 1)
curl -s -X PUT http://localhost:8000/api/calculations/1 -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"a":20,"type":"add","b":5}'

# delete calculation (id 1)
curl -s -X DELETE http://localhost:8000/api/calculations/1 -H "Authorization: Bearer $TOKEN"
```

Notes:

- If you get `401 Unauthorized`, verify the `Authorization` header and that the token was generated by the running server (`SECRET_KEY` must match).
- If you get `403 Forbidden`, the authenticated user is not the owner of the requested calculation.

---

## Docker & Deployment

Build and run locally with Docker Compose:

```bash
docker compose up --build
```

The `Dockerfile` and `docker-compose.yml` are included; CI builds the same image and pushes to Docker Hub when workflow succeeds.

To pull the published image:

```bash
docker pull shanmukh1315/fastapi_calculator:latest
```

Note: CI requires GitHub repository secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, and `SECRET_KEY`.

---

## Project layout

```
fastapi_calculator/
├── app/                       # application package
├── tests/                     # unit, integration, e2e tests
├── .github/workflows/ci.yml   # CI workflow
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Contributing

1. Create a feature branch
2. Run tests locally: `pytest`
3. Open a PR against `main`

---

If you want a slightly different README variant (more compact or more detailed API examples), tell me which sections to expand and I will update it.
pytest --cov=app --cov-report=term-missing

````

- Ensures all modules under `app/` are exercised.
- Current configuration targets 100% coverage for the `app` package.

3. **Run E2E Playwright test**

```bash
pytest tests/e2e/test_playwright.py
````

4. **Build and push Docker image (on success)**

   Using `docker/build-push-action`, the workflow:

   - Builds the image from `Dockerfile`.
   - Tags and pushes:

     ```text
     shanmukha1315/fastapi_calculator:latest
     shanmukha1315/fastapi_calculator:<github_sha>
     ```

### Docker Hub

- Repository: `shanmukha1315/fastapi_calculator`
- URL: [https://hub.docker.com/r/shanmukha1315/fastapi_calculator](https://hub.docker.com/r/shanmukha1315/fastapi_calculator)

Pull the latest image:

```bash
docker pull shanmukha1315/fastapi_calculator:latest
```

---

## Architecture

| Service            | Description                                                                 |
| ------------------ | --------------------------------------------------------------------------- |
| **FastAPI App**    | Hosts calculator and user API endpoints                                     |
| **PostgreSQL**     | Stores users and calculation records                                        |
| **pgAdmin 4**      | Web interface to manage and query PostgreSQL                                |
| **Docker Compose** | Orchestrates app, database, and pgAdmin containers                          |
| **GitHub Actions** | Runs tests, computes coverage, builds and pushes Docker image to Docker Hub |

---

## Project Structure

```text
fastapi_calculator/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── operations.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── users.py
│   ├── calculation_factory.py
│   └── logger_config.py
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_db.py
│   │   ├── test_operations.py
│   │   ├── test_schemas.py
│   │   ├── test_security.py
│   │   ├── test_startup.py
│   │   ├── test_calculation_factory.py
│   │   └── test_calculation_schemas.py
│   ├── integration/
│   │   ├── test_api_endpoints.py
│   │   ├── test_user_db.py
│   │   ├── test_users_api.py
│   │   └── test_calculation_db.py
│   └── e2e/
│       └── test_playwright.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .coveragerc
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── reflection.md
├── .gitignore
└── README.md
```

## Local Development (without Docker)

Requires **Python 3.9+** (tested with 3.12).

### 1. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the FastAPI app

```bash
uvicorn app.main:app --reload
```

Then open:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Root endpoint: [http://localhost:8000/](http://localhost:8000/)

## Running with Docker Compose

Build and start all services:

```bash
docker compose up --build
```

Example logs:

```text
✔ fastapi_calculator-web  Built
✔ Container postgres_db   Running
✔ Container fastapi_app   Recreated
✔ Container pgadmin       Running
fastapi_app  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Service URLs

| Service     | URL                                                      | Notes                                                      |
| ----------- | -------------------------------------------------------- | ---------------------------------------------------------- |
| FastAPI App | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive Swagger UI                                     |
| pgAdmin 4   | [http://localhost:5050](http://localhost:5050)           | Default: [admin@admin.com](mailto:admin@admin.com) / admin |
| PostgreSQL  | `db:5432`                                                | User: `postgres`, Password: `postgres`                     |

## Running Tests Locally

From the project root (with virtualenv activated):

### All tests

```bash
pytest
```

### Tests with coverage

```bash
 pytest --cov=app --cov=tests --cov-report=term-missing
```

```
================================================================ tests coverage ================================================================
_______________________________________________ coverage: platform darwin, python 3.12.4-final-0 _______________________________________________

Name                                       Stmts   Miss  Cover   Missing
------------------------------------------------------------------------
app/__init__.py                                0      0   100%
app/calculation_factory.py                    28      0   100%
app/db.py                                     17      0   100%
app/logger_config.py                           6      0   100%
app/main.py                                   40      0   100%
app/models.py                                 26      0   100%
app/operations.py                             10      0   100%
app/schemas.py                                33      0   100%
app/security.py                                6      0   100%
app/users.py                                  20      0   100%
tests/__init__.py                              0      0   100%
tests/conftest.py                             34      0   100%
tests/e2e/__init__.py                          0      0   100%
tests/integration/__init__.py                  0      0   100%
tests/integration/test_api_endpoints.py       27      0   100%
tests/integration/test_calculation_db.py      34      0   100%
tests/integration/test_user_db.py             12      0   100%
tests/integration/test_users_api.py           23      0   100%
tests/unit/__init__.py                         0      0   100%
tests/unit/test_calculation_factory.py        14      0   100%
tests/unit/test_calculation_schemas.py        12      0   100%
tests/unit/test_db.py                         10      0   100%
tests/unit/test_operations.py                 16      0   100%
tests/unit/test_schemas.py                     9      0   100%
tests/unit/test_security.py                    7      0   100%
tests/unit/test_startup.py                     3      0   100%
------------------------------------------------------------------------
TOTAL                                        387      0   100%
```
