# FastAPI Calculator 

### **JWT Authentication + Front-End Pages + Playwright E2E + CI/CD + Docker Hub Deployment**

This project implements a fully authenticated FastAPI application with **JWT login/registration**, **client-side validated frontend pages**, **Playwright E2E tests**, and a complete **CI/CD pipeline** that builds and deploys Docker images to **Docker Hub** on each successful commit.

---

#  Module-13 Features Completed

* ✔ **JWT-based user registration & login**
* ✔ **Password hashing + Pydantic validation**
* ✔ **Frontend pages** (`/register`, `/login`) with **JavaScript client-side validation**
* ✔ **Stores JWT in localStorage on successful login**
* ✔ **Playwright E2E tests (positive + negative cases)**
* ✔ **CI/CD GitHub Actions workflow**

  * Spins up Postgres + server
  * Runs unit + integration tests
  * Runs Playwright E2E tests
  * Builds & pushes Docker image to Docker Hub
* ✔ **Docker Compose for local development**
* ✔ **Swagger UI testing with Bearer token**
* ✔ **Calculator BREAD routes protected by JWT**

---

# **Repository & Docker Hub Links**

| Resource             | Link                                                                                                                 |
| -------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **GitHub Repo**      | [https://github.com/shanmukh1315/fastapi_calculator](https://github.com/shanmukh1315/fastapi_calculator)             |
| **Docker Hub Image** | https://hub.docker.com/repository/docker/shanmukha1315/fastapi_calculator/general |
| **Local App URL**    | [http://127.0.0.1:8000](http://127.0.0.1:8000)                                                                       |
| **Swagger UI**       | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)                                                             |
| **Register Page**    | [http://127.0.0.1:8000/register](http://127.0.0.1:8000/register)                                                     |
| **Login Page**       | [http://127.0.0.1:8000/login](http://127.0.0.1:8000/login)                                                           |

---

#  Project Overview

A secure calculator web app with:

* User registration/login using JWT
* Client-side validated front-end templates
* Authenticated calculation BREAD API
* SQLAlchemy + PostgreSQL
* CI/CD + E2E testing
* Docker Hub publishing workflow

---

#  **JWT Authentication Routes**

### **POST /register**

Body:

```json
{
  "email": "example@gmail.com",
  "username": "admin",
  "password": "secret123"
}
```

### **POST /login**

Returns:

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

Swagger UI lets you click **Authorize → paste token** → now all protected endpoints work.

You already demonstrated it here:

*(Based on your screenshot of Swagger UI authorized)*

---

# **Frontend Pages**

Frontend lives inside `app/templates`.

### **/register**

* Email format validation
* Password length check
* Confirm password match
* On success → shows green message:
  **“Registered successfully. You can now log in.”**

(Your screenshot confirms this is working perfectly.)

### ** /login**

* Username + password
* On success → JWT stored in `localStorage`
* UI shows:
  **“Login successful. Token stored in localStorage.”**

(Your screenshot confirms this.)

---

#  **Testing**

###  Unit + Integration Tests

Run locally:

```bash
pytest
```

With coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

```
_________________________ coverage: platform darwin, python 3.12.4-final-0 __________________________

Name                         Stmts   Miss  Cover   Missing
----------------------------------------------------------
app/__init__.py                  0      0   100%
app/calculation_factory.py      28      0   100%
app/calculations.py             76      0   100%
app/db.py                       17      0   100%
app/logger_config.py             6      0   100%
app/main.py                     91      0   100%
app/models.py                   26      0   100%
app/operations.py               10      0   100%
app/schemas.py                  39      0   100%
app/security.py                 25      0   100%
app/users.py                    32      0   100%
----------------------------------------------------------
TOTAL                          350      0   100%
```
### ✔ Playwright E2E Tests

Install browsers:

```bash
playwright install chromium
```

Run tests:

```bash
pytest tests/e2e -q
```

Your E2E tests include:

| Test Type             | Behavior                                 |
| --------------------- | ---------------------------------------- |
| **Positive Register** | valid email + password → success         |
| **Positive Login**    | valid credentials → success + save token |
| **Negative Register** | short password → UI error                |
| **Negative Login**    | wrong password → invalid credentials     |

---

#  CI/CD Pipeline (GitHub Actions)

Your `ci.yml` performs:

1. Set up Python
2. Install dependencies
3. Start PostgreSQL container
4. Start FastAPI server
5. Run unit + integration tests
6. Run Playwright E2E tests
7. If all pass → **build & push Docker image**

Images pushed to:

```
shanmukh1315/fastapi_calculator:latest
shanmukh1315/fastapi_calculator:<sha>
```

Your Docker Hub screenshots confirm this works.

---

# Docker & Docker Compose

### **Run everything locally:**

```bash
docker compose up --build
```

This starts:

| Service       | Port | Purpose        |
| ------------- | ---- | -------------- |
| `fastapi_app` | 8000 | API + Frontend |
| `postgres_db` | 5432 | Database       |
| `pgadmin`     | 5050 | Database UI    |

Environment variables are loaded from `.env`.

---

# Swagger BREAD API (Protected With JWT)

Must include:

```
Authorization: Bearer <token>
```

### Endpoints:

| Method | Route                    |
| ------ | ------------------------ |
| GET    | `/api/calculations`      |
| POST   | `/api/calculations`      |
| GET    | `/api/calculations/{id}` |
| PUT    | `/api/calculations/{id}` |
| DELETE | `/api/calculations/{id}` |

Your screenshots show:

* Creating a calculation works
* Reading works
* Unauthorized reads return 403 (correct behavior)

---

# Project Structure

```
fastapi_calculator/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── users.py
│   ├── templates/
│   │   ├── register.html
│   │   └── login.html
│   └── calculation_factory.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .github/workflows/ci.yml
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```
