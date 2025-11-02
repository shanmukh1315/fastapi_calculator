# FastAPI Calculator – Module 8 Assignment

A fully tested **FastAPI-based Calculator Web Application** built for the Module 8 assignment.  
Implements REST API endpoints for basic arithmetic operations with complete CI/CD, logging, and 100% automated test coverage.

---

##  Overview

This project demonstrates:
- Creating and consuming REST APIs with **FastAPI**
- Writing **unit**, **integration**, and **end-to-end (Playwright)** tests
- Implementing structured **logging**
- Running continuous integration (CI) using **GitHub Actions**
- Achieving **100% test coverage**

---

##  Features

| Feature | Description |
|----------|--------------|
| **Arithmetic Endpoints** | `/add`, `/subtract`, `/multiply`, `/divide` |
| **Unit Tests** | Validates logic in `operations.py` |
| **Integration Tests** | Tests all endpoints in `main.py` |
| **E2E Test (Playwright)** | Checks if Swagger UI loads correctly |
| **Logging** | Tracks operations and errors via `logger_config.py` |
| **CI Pipeline** | GitHub Actions runs all tests automatically on push |
| **Coverage** | 100% coverage across all application files |

---

##  Project Structure
```
fastapi_calculator/
│
├── app/
│ ├── init.py
│ ├── main.py
│ ├── operations.py
│ ├── logger_config.py
│
├── tests/
│ ├── unit/
│ ├── integration/
│ └── e2e/
│
├── .github/workflows/ci.yml # GitHub Actions CI pipeline
├── requirements.txt # Project dependencies
├── .gitignore # Ignore unnecessary files
└── README.md
```

##  Application Preview
```
You can access the interactive Swagger UI here when running locally:  
 **http://127.0.0.1:8000/docs**

![FastAPI Swagger UI Screenshot](./images/fastapi_calculator_ui.png)

<img width="1470" height="956" alt="Screenshot 2025-11-02 at 12 55 15 PM" src="https://github.com/user-attachments/assets/72f5cf9c-eef2-4c32-aa61-124c11356164" />
```

## Setup

Requires Python 3.9+.

```bash
python3 -m venv .venv
source .venv/bin/activate               # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

##  How to Run Locally

### 1️⃣ Install dependencies

```
pip install -r requirements.txt
```
2️⃣ Run the FastAPI app
```
uvicorn app.main:app --reload
```
Open your browser at:
👉 http://127.0.0.1:8000/docs

Run Tests
```
Run all tests:

pytest
Run with coverage:
pytest --cov=app
```
## Test Coverage Summary
```
(venv) (base) shannu@Shannus-MacBook-Air fastapi_calculator % pytest --cov=app

=================================== test session starts ===================================
platform darwin -- Python 3.12.4, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/shannu/Desktop/MS/web_API/fastapi_calculator
plugins: anyio-4.11.0, cov-7.0.0
collected 12 items                                                                        

tests/e2e/test_playwright.py s                                                      [  8%]
tests/integration/test_api_endpoints.py ......                                      [ 58%]
tests/unit/test_operations.py .....                                                 [100%]

===================================== tests coverage ======================================
____________________ coverage: platform darwin, python 3.12.4-final-0 _____________________

Name                   Stmts   Miss  Cover
------------------------------------------
app/__init__.py            0      0   100%
app/logger_config.py       6      0   100%
app/main.py               33      0   100%
app/operations.py         10      0   100%
------------------------------------------
TOTAL                     49      0   100%
============================== 11 passed, 1 skipped in 0.76s ==============================
```


