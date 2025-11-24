
# FastAPI Calculator
```
A fully containerized FastAPI Calculator Web Application integrated with PostgreSQL and pgAdmin, with:

- Calculator endpoints for basic arithmetic.
- Secure user model with password hashing.
- Calculation model backed by SQLAlchemy.
- Pydantic validation for users and calculations.
- Automated unit, integration, and E2E tests.
- GitHub Actions CI pipeline that runs tests, reports coverage, and builds/pushes a Docker image to Docker Hub.
```

## Features

### Calculator API
```
- REST endpoints built with **FastAPI**:
  - `GET /add?a=&b=`
  - `GET /subtract?a=&b=`
  - `GET /multiply?a=&b=`
  - `GET /divide?a=&b=`
- Centralized logging via `app/logger_config.py`.
- Containerized with **Docker** and orchestrated with **Docker Compose**.
- **PostgreSQL** database + **pgAdmin 4** UI.
- Database schema supports a one-to-many relationship: **Users ↔ Calculations**.
```

### Data Models & Validation

#### User Model
```
- **SQLAlchemy `User` model** (`app/models.py`)
  - `id` (PK)
  - `username` – unique, indexed
  - `email` – unique, indexed
  - `password_hash`
  - `created_at` – timestamp with server default
- **Pydantic Schemas** (`app/schemas.py`)
  - `UserCreate` – `username`, `email`, `password` (input)
  - `UserRead` – `id`, `username`, `email`, `created_at` (output, no password)
  - Email validation using `EmailStr`.

- **Secure password hashing** (`app/security.py`)
  - Hashing with `passlib` (`pbkdf2_sha256`):
    - `hash_password(plain_password)`
    - `verify_password(plain_password, hashed_password)`

- **User API router** (`app/users.py`)
  - `POST /api/users` – create user.
  - Validates:
    - Unique `username`.
    - Unique `email`.
  - Stores only `password_hash` in the database.
  - Returns `UserRead` schema (no raw password).
```
#### Calculation Model
```
- **SQLAlchemy `Calculation` model** (`app/models.py`)
  - `id` (PK)
  - `a`: `float`
  - `type`: `CalculationType` enum
  - `b`: `float`
  - `result`: `float` (optional, stored after computation)
  - `user_id`: optional FK → `User.id`
- **`CalculationType` enum** (`app/models.py`)
  - Values: `"add"`, `"subtract"`, `"multiply"`, `"divide"`.

- **Pydantic Schemas** (`app/schemas.py`)
  - `CalculationCreate` – `a`, `type`, `b`, with validation:
    - `type` must be one of `CalculationType`.
    - Division by zero is rejected when `type == CalculationType.DIVIDE`.
  - `CalculationRead` – `id`, `a`, `type`, `b`, `result`, optional `user_id`.
```


### Calculation Factory Pattern
```
To keep calculation logic organized and extensible, the app uses a small factory in `app/calculation_factory.py`:

- `CalculationFactory.get_operation(calc_type)`  
  Returns an operation object exposing:

  ```python
  op = CalculationFactory.get_operation(calc_type)
  result = op.compute(a, b)
````

## Testing

### Unit Tests
```
Located under `tests/unit/`:

* `test_operations.py` – calculator functions.
* `test_schemas.py` – user Pydantic validation.
* `test_security.py` – password hash/verify behavior.
* `test_db.py` – database engine and session.
* `test_startup.py` – FastAPI startup behavior.
* `test_calculation_factory.py` – factory behavior:

  * Correct operation for each `CalculationType`.
  * Invalid type raises `ValueError`.
  * Divide operation raises `ZeroDivisionError` on divide-by-zero.
* `test_calculation_schemas.py` – calculation schema validation:

  * Valid `CalculationCreate` objects.
  * Division-by-zero rejected with `ValidationError`.
```
### Integration Tests
```
Located under `tests/integration/`:

* `test_api_endpoints.py` – calculator API endpoints.
* `test_user_db.py` – User database uniqueness and constraints.
* `test_users_api.py` – `/api/users` behavior:

  * successful creation,
  * duplicate username,
  * duplicate email.
* `test_calculation_db.py` – Calculation model:

  * Create and persist a `Calculation` with a computed `result`.
  * Verify stored fields and `result`.
  * Ensure `user_id` FK and `calc.user` relationship work as expected.
```
### End-to-End Test
```
* `tests/e2e/test_playwright.py` – basic smoke test using Playwright to hit the running app via a browser.
```
### Databases Used in Tests
```
* **Local (default):** SQLite – `sqlite:///./test.db`
* **CI:** PostgreSQL using the `TEST_DATABASE_URL` environment variable and a Postgres service container.
```


## CI/CD Pipeline

### GitHub Actions
```
Workflow file: `.github/workflows/ci.yml`
```
On every push or pull request to `main`:

1. **Set up environment**

   * Check out the repository.
   * Set up Python 3.12.
   * Start a PostgreSQL 15 service container for tests.
   * Install dependencies:

     * `requirements.txt`
     * `pytest`, `pytest-cov`, `playwright` (and install Chromium for E2E test).

2. **Run tests with coverage**

   ```bash
   pytest --cov=app --cov-report=term-missing
   ```

   * Ensures all modules under `app/` are exercised.
   * Current configuration targets 100% coverage for the `app` package.

3. **Run E2E Playwright test**

   ```bash
   pytest tests/e2e/test_playwright.py
   ```

4. **Build and push Docker image (on success)**

   Using `docker/build-push-action`, the workflow:

   * Builds the image from `Dockerfile`.
   * Tags and pushes:

     ```text
     shanmukha1315/fastapi_calculator:latest
     shanmukha1315/fastapi_calculator:<github_sha>
     ```

### Docker Hub

* Repository: `shanmukha1315/fastapi_calculator`
* URL: [https://hub.docker.com/r/shanmukha1315/fastapi_calculator](https://hub.docker.com/r/shanmukha1315/fastapi_calculator)

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

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* Root endpoint: [http://localhost:8000/](http://localhost:8000/)


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
