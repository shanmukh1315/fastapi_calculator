# FastAPI Calculator – Module 8 & 9 (Docker + PostgreSQL + pgAdmin)

A fully containerized **FastAPI Calculator Web Application** integrated with **PostgreSQL** and **pgAdmin**, built as part of **FA25-IS601101 Modules 8 & 9**.  
The project demonstrates both API-driven and raw SQL database operations using Docker Compose.

---

## Overview

This project showcases:
- Creating and consuming REST APIs with **FastAPI**
- Writing and testing Python code using **pytest**
- Containerizing FastAPI, PostgreSQL, and pgAdmin using **Docker Compose**
- Executing **raw SQL queries** (CREATE, INSERT, SELECT, UPDATE, DELETE) via **pgAdmin**
- Managing one-to-many database relationships (Users ↔ Calculations)
- Achieving full reproducibility through version control and GitHub Actions CI

---

## Architecture

| Service | Description |
|----------|-------------|
| **FastAPI App** | Hosts the calculator API endpoints (`/add`, `/subtract`, `/multiply`, `/divide`) |
| **PostgreSQL** | Stores user and calculation data |
| **pgAdmin 4** | Web interface for managing and querying the PostgreSQL database |
| **Docker Compose** | Orchestrates all three containers into one environment |

---

##  Project Structure
```
fastapi_calculator/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── operations.py
│   └── db.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md

```

## Setup

Requires Python 3.9+.

```bash
python3 -m venv .venv
source .venv/bin/activate               # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```
**Setup & Run with Docker Compose**

### Build and Run Containers
```bash
docker compose up --build
```
```
 ✔ fastapi_calculator-web  Built                                             0.0s 
 ✔ Container postgres_db   Running                                           0.0s 
 ✔ Container fastapi_app   Recreated                                         0.4s 
 ✔ Container pgadmin       Running                                           0.0s 
Attaching to fastapi_app, pgadmin, postgres_db
fastapi_app  | INFO:     Will watch for changes in these directories: ['/app']
fastapi_app  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
fastapi_app  | INFO:     Started reloader process [1] using StatReload
fastapi_app  | INFO:     Started server process [8]
fastapi_app  | INFO:     Waiting for application startup.
fastapi_app  | INFO:     Application startup complete.
```
**Access the Services**
```
Service                    	URL                          	Notes
FastAPI App	        http://localhost:8000/docs	   Interactive Swagger UI
pgAdmin 4	          http://localhost:5050	         Default login: admin@admin.com/ admin
PostgreSQL	        Host: db Port: 5432	           User: postgres Password: postgres
```
## SQL Operations in pgAdmin
## (A) Create Tables
```
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
```
CREATE TABLE calculations (
    id SERIAL PRIMARY KEY,
    operation VARCHAR(20) NOT NULL,
    operand_a FLOAT NOT NULL,
    operand_b FLOAT NOT NULL,
    result FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```
## (B) Insert Records
```
INSERT INTO users (username, email) 
VALUES 
('alice', 'alice@example.com'), 
('bob', 'bob@example.com');

INSERT INTO calculations (operation, operand_a, operand_b, result, user_id)
VALUES
('add', 2, 3, 5, 1),
('divide', 10, 2, 5, 1),
('multiply', 4, 5, 20, 2);
```
## (C) Query Data
```
SELECT * FROM users;
SELECT * FROM calculations;
SELECT u.username, c.operation, c.operand_a, c.operand_b, c.result
FROM calculations c
JOIN users u ON c.user_id = u.id;
```

## (D) Update a Record
```
UPDATE calculations
SET result = 6
WHERE id = 1;
```
## (E) Delete a Record
```
DELETE FROM calculations
WHERE id = 2;
```
**Verification Steps**
```
Docker Compose – all containers run successfully
pgAdmin – connected to database fastapi_db
SQL Queries – created, inserted, joined, updated, and deleted records successfully
FastAPI – endpoints verified via Swagger UI
```
## Run Tests Locally:
```
pytest --cov=app
```

## Expected Output:
```
venv) (base) shannu@Shannus-MacBook-Air fastapi_calculator % pytest --cov=app

======================================== test session starts ========================================
platform darwin -- Python 3.12.4, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/shannu/Desktop/MS/web_API/fastapi_calculator
plugins: anyio-4.11.0, cov-7.0.0
collected 12 items                                                                                  

tests/e2e/test_playwright.py s                                                                [  8%]
tests/integration/test_api_endpoints.py ......                                                [ 58%]
tests/unit/test_operations.py .....                                                           [100%]

========================================== tests coverage ===========================================
_________________________ coverage: platform darwin, python 3.12.4-final-0 __________________________

Name                   Stmts   Miss  Cover
------------------------------------------
app/__init__.py            0      0   100%
app/logger_config.py       6      0   100%
app/main.py               33      0   100%
app/operations.py         10      0   100%
------------------------------------------
TOTAL                     49      0   100%
=================================== 11 passed, 1 skipped in 0.86s ===================================
(venv) (base) shannu@Shannus-MacBook-Air fastapi_calculator %
```
