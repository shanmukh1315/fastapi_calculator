# FastAPI Calculator – Modules 8, 9 & 10
```
A fully containerized FastAPI Calculator Web Application integrated with PostgreSQL and pgAdmin, extended in Module 10 with a **secure user model, Pydantic validation, password hashing, database tests, and a full CI/CD pipeline that builds and pushes a Docker image to Docker Hub.
```

---

## Features

### Calculator API (Modules 8 & 9)
```
- REST endpoints built with **FastAPI**:
  - `GET /add?a=&b=`
  - `GET /subtract?a=&b=`
  - `GET /multiply?a=&b=`
  - `GET /divide?a=&b=`
- Centralized logging via `logger_config.py`
- Containerized with **Docker** and orchestrated with **Docker Compose**
- **PostgreSQL** database + **pgAdmin 4** UI
- Raw SQL in pgAdmin:
  - `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`
  - One-to-many relationship: **Users ↔ Calculations**
```
### Secure User Model & Validation (Module 10)
```
- **SQLAlchemy `User` model** (`app/models.py`)
  - `id` (PK)
  - `username` – unique
  - `email` – unique
  - `password_hash`
  - `created_at` – timestamp defaulting to current time
- **Pydantic Schemas** (`app/schemas.py`)
  - `UserCreate` – `username`, `email`, `password`
  - `UserRead` – `id`, `username`, `email`, `created_at` (no password exposed)
  - Email validation using `EmailStr`
- **Secure password hashing** (`app/security.py`)
  - Hashing with `passlib` (`pbkdf2_sha256`)
  - `hash_password(plain_password)`
  - `verify_password(plain_password, hashed_password)`
- **User API router** (`app/users.py`)
  - `POST /api/users` – create user
  - Validates:
    - Unique `username`
    - Unique `email`
  - Stores only `password_hash` in the database
  - Returns `UserRead` schema (no raw password)
```
### Testing & CI/CD (Module 10)
```
- **Unit tests**
  - `tests/unit/test_operations.py` – calculator operations
  - `tests/unit/test_schemas.py` – Pydantic validation (valid + invalid data)
  - `tests/unit/test_security.py` – hash/verify password
  - `tests/unit/test_db.py` – DB connection / engine
  - `tests/unit/test_startup.py` – FastAPI startup behaviour
- **Integration tests**
  - `tests/integration/test_api_endpoints.py` – calculator API endpoints
  - `tests/integration/test_user_db.py` – user uniqueness at DB level
  - `tests/integration/test_users_api.py` – `/api/users` behaviour:
    - successful creation
    - duplicate username
    - duplicate email
- **E2E test**
  - `tests/e2e/test_playwright.py` – basic browser test (smoke)
- **Database for tests**
  - Local default: SQLite (`sqlite:///./test.db`)
  - CI: uses `TEST_DATABASE_URL` env var (PostgreSQL service in GitHub Actions)
- **GitHub Actions CI**
  - Runs on every `push` / `pull_request`
  - Steps:
    - Check out repo
    - Set up Python
    - Install dependencies
    - Run all unit, integration, and E2E tests
    - Build and push Docker image to Docker Hub (on successful tests)
- **Docker Hub deployment**
  - Image: `shanmukha1315/fastapi_calculator:latest`
  - Link: https://hub.docker.com/r/shanmukha1315/fastapi_calculator
```
---

## Architecture

| Service            | Description                                                                |
| ------------------ | -------------------------------------------------------------------------- |
| **FastAPI App**    | Hosts calculator + user API endpoints                                      |
| **PostgreSQL**     | Stores users and (optionally) calculation data                             |
| **pgAdmin 4**      | Web interface to manage and query PostgreSQL                               |
| **Docker Compose** | Orchestrates app, database, and pgAdmin containers                         |
| **GitHub Actions** | Runs tests, builds Docker image, pushes to Docker Hub on successful builds |

---

## Project Structure

```
fastapi_calculator/
│
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app, routes registration, startup
│   ├── operations.py     # Calculator logic
│   ├── db.py             # SQLAlchemy engine, SessionLocal, Base
│   ├── models.py         # SQLAlchemy models (User)
│   ├── schemas.py        # Pydantic models (UserCreate, UserRead)
│   ├── security.py       # Password hashing / verification
│   ├── users.py          # /api/users router
│   └── logger_config.py  # Logging configuration
│
├── tests/
│   ├── conftest.py       # Test DB + TestClient fixtures
│   ├── unit/
│   │   ├── test_db.py
│   │   ├── test_operations.py
│   │   ├── test_schemas.py
│   │   ├── test_security.py
│   │   └── test_startup.py
│   ├── integration/
│   │   ├── test_api_endpoints.py
│   │   ├── test_user_db.py
│   │   └── test_users_api.py
│   └── e2e/
│       └── test_playwright.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .github/workflows/ci.yml
├── .gitignore
└── README.md

```
Local Development Setup (without Docker)

Requires Python 3.9+.

# Create and activate virtual environment
```
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```
# Install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```

# Run the FastAPI app:
```
uvicorn app.main:app --reload
 ```
```
Open:
Swagger UI: http://localhost:8000/docs

Root endpoint: http://localhost:8000/
```

Running with Docker Compose

Build and start all services:
```
docker compose up --build

```
Expected logs snippet:
```
✔ fastapi_calculator-web  Built
✔ Container postgres_db   Running
✔ Container fastapi_app   Recreated
✔ Container pgadmin       Running
fastapi_app  | INFO:     Uvicorn running on http://0.0.0.0:8000

Service URLs
Service	URL	Notes
FastAPI App	http://localhost:8000/docs
	Interactive Swagger UI
pgAdmin 4	http://localhost:5050
	Default: admin@admin.com / admin
PostgreSQL	Host: db, Port: 5432	User: postgres, Password: postgres
```

Running Tests Locally

From the project root (with virtualenv activated):

Run all tests
```
pytest
```
Run unit + integration tests with coverage
```
pytest --cov=app --cov-report=term-missing tests/unit tests/integration
```

Example output:
```
venv) (base) shannu@Shannus-MacBook-Air fastapi_calculator % pytest --cov=app --cov-report=term-missing tests/unit tests/integration

============================================================= test session starts ==============================================================
platform darwin -- Python 3.12.4, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/shannu/Desktop/MS/web_API/fastapi_calculator
plugins: anyio-4.11.0, cov-7.0.0
collected 20 items                                                                                                                             

tests/unit/test_db.py .                                                                                                                  [  5%]
tests/unit/test_operations.py .....                                                                                                      [ 30%]
tests/unit/test_schemas.py ..                                                                                                            [ 40%]
tests/unit/test_security.py .                                                                                                            [ 45%]
tests/unit/test_startup.py .                                                                                                             [ 50%]
tests/integration/test_api_endpoints.py ......                                                                                           [ 80%]
tests/integration/test_user_db.py .                                                                                                      [ 85%]
tests/integration/test_users_api.py ...                                                                                                  [100%]
================================================================ tests coverage ================================================================
_______________________________________________ coverage: platform darwin, python 3.12.4-final-0 _______________________________________________

Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
app/__init__.py            0      0   100%
app/db.py                 17      0   100%
app/logger_config.py       6      0   100%
app/main.py               40      0   100%
app/models.py              9      0   100%
app/operations.py         10      0   100%
app/schemas.py            13      0   100%
app/security.py            6      0   100%
app/users.py              20      0   100%
----------------------------------------------------
TOTAL                    121      0   100%
```

CI/CD Pipeline (GitHub Actions → Docker Hub)

Workflow file: .github/workflows/ci.yml

On every push / PR:

Set up Python and dependencies

Run unit, integration, and E2E tests

If all tests pass:
```
Build Docker image from Dockerfile

Tag as ${DOCKERHUB_USERNAME}/fastapi_calculator:latest

Push image to Docker Hub
```
Docker Hub repository:
```
Name: shanmukha1315/fastapi_calculator

URL: https://hub.docker.com/r/shanmukha1315/fastapi_calculator
```
You can pull and run the image directly:
```
docker pull shanmukha1315/fastapi_calculator:latest
```
