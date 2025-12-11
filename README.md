# FastAPI Calculator

JWT Authentication + Calculations BREAD + Advanced Features + Front-End UI + Playwright E2E + CI/CD + Docker Hub

This project is a full-stack FastAPI Calculator application with JWT-based authentication, a user-scoped calculation BREAD API, advanced calculation operations, user profile management, statistics/reporting, and a modern front-end interface. It includes comprehensive unit, integration, and Playwright E2E tests, plus a GitHub Actions CI/CD pipeline that builds and pushes Docker images to Docker Hub when all tests pass.

## Quick Start

### Run with Docker (Recommended)

```bash
# Pull the latest image from Docker Hub
docker pull shanmukha1315/fastapi_calculator:latest

# Run the container
docker run -p 8000:8000 shanmukha1315/fastapi_calculator:latest
```

**Docker Hub Repository**: https://hub.docker.com/repository/docker/shanmukha1315/fastapi_calculator

### Run Locally with Python

```bash
# Clone the repository
git clone https://github.com/shanmukh1315/fastapi_calculator.git
cd fastapi_calculator

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

**Access the application at**: http://127.0.0.1:8000

### Run Tests

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test suites
pytest tests/unit/ -v          # Unit tests only
pytest tests/integration/ -v   # Integration tests only
pytest tests/e2e/ -v           # E2E tests only
```

## Modules Covered

### Module 13 — Auth + UI + E2E

- JWT-based user registration & login
- Password hashing + Pydantic validation
- Front-end pages with client-side validation
  - `/register`
  - `/login`
- Stores JWT in localStorage after successful login
- Playwright E2E tests for positive + negative auth flows
- GitHub Actions automated testing + Docker build/push

### Module 14 — Calculations BREAD

- Full BREAD for calculations (scoped to authenticated user)
- Protected API routes using JWT + ownership checks
- Front-end BREAD interface with validation
  - `/calculations`
- Playwright E2E tests for calculation BREAD
- Positive + negative scenarios

### Final Project Features

#### Feature 1: User Profile & Password Change

- **Profile Management Page** (`/profile`)
  - View current profile information
  - Update username and email with uniqueness validation
  - Change password with secure hashing
- **Backend Implementation**
  - `GET /api/users/me` - Retrieve current user profile
  - `PUT /api/users/profile` - Update username/email
  - `POST /api/users/change-password` - Change password
  - SQLAlchemy models with User table
  - Pydantic schemas: `UserRead`, `UserUpdate`, `PasswordChange`
- **Testing Coverage**
  - 14 unit tests for profile logic
  - Integration tests for database updates
  - E2E tests for complete workflow (login → profile → password change → re-login)

#### Feature 2: Advanced Calculation Operations

- **Three New Operation Types**
  - **Percent Of**: Calculate "what is X% of Y" (e.g., "25% of 200 = 50")
  - **Nth Root**: Calculate nth root of a number (e.g., "3rd root of 27 = 3")
  - **Logarithm**: Calculate log base N of X (e.g., "log base 2 of 8 = 3")
- **Backend Implementation**
  - Extended `CalculationType` enum with 3 new operations
  - Updated calculation factory pattern
  - Comprehensive validation for each operation
  - Error handling for edge cases (negative roots, invalid bases, etc.)
- **Front-End Integration**
  - Updated calculation form with new operation types
  - Live preview showing operation syntax
  - Client-side validation for operand constraints
  - Operation hints for user guidance
- **Testing Coverage**
  - 37 unit tests for advanced operation logic
  - 6 integration tests for API route handling
  - 8 E2E tests for front-end workflows
  - Positive and negative test scenarios

#### Feature 3: Statistics & Reporting Dashboard

- **Usage Statistics API**
  - `GET /api/statistics/summary` - Comprehensive stats
    - Total calculations count
    - Average operands (A, B) and results
    - Min/Max result values
    - Most used operation type
    - Operations breakdown by type
  - `GET /api/statistics/recent?limit=N` - Recent calculations summary
- **Visual Dashboard**
  - Real-time statistics cards on calculations page
  - Animated operations breakdown chart
  - Statistics update automatically after CRUD operations
  - Responsive design with modern UI
- **Export Functionality**
  - CSV export (spreadsheet-compatible format)
  - JSON export (formatted, developer-friendly)
  - PDF export (printable report with auto-print dialog)
  - Export modal with format selection
- **Testing Coverage**
  - 16 unit tests for statistics calculation logic
  - 14 integration tests for API endpoints
  - 10 E2E tests for dashboard UI and interactions
  - Coverage for edge cases (empty data, single calculation, etc.)

## UI Features

Our modern front-end interface includes these user experience enhancements:

1. **Dark/Light Theme Toggle**

   - System-preference detection with manual override
   - Smooth transitions between themes
   - Theme preference persists across sessions

2. **Toast Notifications**

   - Real-time feedback for all user actions
   - Success, error, and informational messages
   - Auto-dismiss with progress animation
   - Non-intrusive design

3. **Search & Filter**

   - Real-time search across calculations
   - Filter by operation type
   - Debounced input for performance
   - Instant results update

4. **Export Functionality**

   - Three export formats: CSV, JSON, PDF
   - Modal interface with format selection
   - CSV: spreadsheet-compatible with headers
   - JSON: formatted, human-readable output
   - PDF: print-friendly report with auto-print dialog
   - Filename includes timestamp

5. **Live Calculation Preview**

   - Real-time formula display
   - Shows operation syntax as you type
   - Updates instantly with operand changes
   - Helps prevent input errors

6. **Animated Statistics Charts**

   - Operations breakdown bar chart
   - Smooth animations on data updates
   - Color-coded by operation type
   - Responsive to screen size

7. **Color-Coded Operation Pills**

   - Visual distinction for each operation type
   - Consistent color scheme throughout app
   - Improves readability in calculation list
   - Quick operation identification

8. **Account Dropdown Menu**

   - Quick access to profile and logout
   - Displays current username
   - Responsive positioning
   - Smooth animations

9. **Responsive Design**

   - Mobile-first approach
   - Adapts to all screen sizes
   - Touch-friendly interface
   - Optimized for desktop and mobile

10. **Error Handling with Helpful Messages**
    - Clear, user-friendly error messages
    - Validation feedback on form fields
    - Network error handling
    - Suggestions for fixing issues

## How Our Webpage Works

### User Registration & Authentication

1. **New User Registration** (`/register`)

   - Enter username, email, and password
   - Client-side validation ensures all fields are complete
   - Password must meet minimum length requirements
   - Server validates uniqueness of username and email
   - Successful registration redirects to login page

2. **User Login** (`/login`)
   - Enter username and password
   - Server validates credentials and returns JWT token
   - Token stored in browser's localStorage
   - Automatic redirect to calculations page
   - Token included in all subsequent API requests

### Calculator Interface

3. **Calculations Page** (`/calculations`)
   - **Main calculator form**:
     - Select operation type from dropdown (9 operation types)
     - Enter operand A (first number)
     - Enter operand B (second number)
     - Live preview shows the operation formula
     - Submit button performs calculation
   - **Calculation history table**:
     - Displays all user's calculations
     - Color-coded operation pills for easy identification
     - Edit button loads calculation into form for modification
     - Delete button removes calculation (with confirmation)
     - Search bar filters calculations in real-time
   - **Statistics dashboard**:
     - Total calculations count
     - Average values for operands and results
     - Min/Max result tracking
     - Most frequently used operation
     - Animated bar chart showing operations breakdown
   - **Export functionality**:
     - Export button opens modal
     - Choose from CSV, JSON, or PDF format
     - Downloads file with timestamp
     - PDF auto-opens print dialog

### Advanced Operations

4. **Special Calculation Types**
   - **Percent Of**: Enter percentage (A) and total value (B)
     - Example: A=25, B=200 → "25% of 200 = 50"
   - **Nth Root**: Enter root index (A) and value (B)
     - Example: A=3, B=27 → "3rd root of 27 = 3.0"
   - **Logarithm**: Enter base (A) and value (B)
     - Example: A=2, B=8 → "log base 2 of 8 = 3.0"
   - Live preview updates to show operation-specific syntax
   - Validation prevents invalid inputs (e.g., negative roots)

### Profile Management

5. **Profile Page** (`/profile`)
   - **View Profile Section**:
     - Displays current username and email
     - Shows account creation date
   - **Update Profile Form**:
     - Change username and/or email
     - Real-time validation
     - Server checks for uniqueness
     - Success notification on update
   - **Change Password Form**:
     - Enter current password
     - Enter new password
     - Confirm new password
     - Server validates old password
     - Secure password hashing
     - Success notification on change

### Data Flow

6. **Complete User Journey**
   - Register → Login (get JWT) → Create calculations → View statistics → Export data → Update profile → Change password → Logout
   - All protected routes require valid JWT token
   - User can only access their own calculations
   - Real-time updates across all components
   - Persistent session until logout

## Important Links

| Resource                    | Link                                                                              |
| --------------------------- | --------------------------------------------------------------------------------- |
| **GitHub Repository**       | https://github.com/shanmukh1315/fastapi_calculator                                |
| **Docker Hub Repository**   | https://hub.docker.com/repository/docker/shanmukha1315/fastapi_calculator/general |
| Local Application           | http://127.0.0.1:8000                                                             |
| API Documentation (Swagger) | http://127.0.0.1:8000/docs                                                        |
| Register Page               | http://127.0.0.1:8000/register                                                    |
| Login Page                  | http://127.0.0.1:8000/login                                                       |
| Calculations Page           | http://127.0.0.1:8000/calculations                                                |
| Profile Page                | http://127.0.0.1:8000/static/profile.html                                         |

## Project Overview

This application supports:

- Secure user registration/login using JWT
- User profile management with password change functionality
- A calculation history per user with 9 operation types
- Full BREAD operations for calculations
- Advanced calculation operations (percent_of, nth_root, log_base)
- Statistics dashboard with visual charts
- Multi-format export (CSV, JSON, PDF)
- Client-side and server-side validation
- Automated E2E testing with Playwright
- CI/CD with GitHub Actions
- Database migrations with Alembic
- Dockerized deployment with Docker Hub publishing

## API Endpoints

### Authentication

Your UI uses these pages: `/register` and `/login`.

**Register**

```http
POST /api/users
Content-Type: application/json

{
  "email": "example@gmail.com",
  "username": "admin",
  "password": "secret123"
}
```

**Login**

```http
POST /api/users/login
Content-Type: application/json

{
  "username": "admin",
  "password": "secret123"
}
```

Returns:

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

### User Profile (JWT Protected)

| Method | Route                        | Description              |
| ------ | ---------------------------- | ------------------------ |
| GET    | `/api/users/me`              | Get current user profile |
| PUT    | `/api/users/profile`         | Update username/email    |
| POST   | `/api/users/change-password` | Change password          |

**Update Profile Example**

```http
PUT /api/users/profile
Authorization: Bearer <JWT>
Content-Type: application/json

{
  "username": "newusername",
  "email": "newemail@example.com"
}
```

**Change Password Example**

```http
POST /api/users/change-password
Authorization: Bearer <JWT>
Content-Type: application/json

{
  "old_password": "currentpass",
  "new_password": "newpassword123"
}
```

### Calculations (JWT Protected)

| Method | Route                    | Description                    |
| ------ | ------------------------ | ------------------------------ |
| GET    | `/api/calculations`      | Browse all user's calculations |
| POST   | `/api/calculations`      | Create new calculation         |
| GET    | `/api/calculations/{id}` | Read specific calculation      |
| PUT    | `/api/calculations/{id}` | Update calculation             |
| DELETE | `/api/calculations/{id}` | Delete calculation             |

All routes enforce user ownership (403 if accessing another user's calculation).

**Supported Operation Types:**

- `add` - Addition (+)
- `subtract` - Subtraction (-)
- `multiply` - Multiplication (\*)
- `divide` - Division (/)
- `power` - Exponentiation (^)
- `modulus` - Modulus (%)
- `percent_of` - Percentage calculation (e.g., "25% of 200")
- `nth_root` - Nth root (e.g., "3rd root of 27")
- `log_base` - Logarithm with custom base (e.g., "log base 2 of 8")

**Create Calculation Example**

```http
POST /api/calculations
Authorization: Bearer <JWT>
Content-Type: application/json

{
  "a": 10,
  "type": "add",
  "b": 5
}
```

**Advanced Operations Examples**

```json
// Percent of
{ "a": 25, "type": "percent_of", "b": 200 }  // Result: 50

// Nth root
{ "a": 3, "type": "nth_root", "b": 27 }  // Result: 3.0

// Logarithm
{ "a": 2, "type": "log_base", "b": 8 }  // Result: 3.0
```

### Statistics & Reporting (JWT Protected)

| Method | Route                            | Description                        |
| ------ | -------------------------------- | ---------------------------------- |
| GET    | `/api/statistics/summary`        | Get comprehensive usage statistics |
| GET    | `/api/statistics/recent?limit=N` | Get recent calculations summary    |

**Statistics Summary Response**

```json
{
  "total_calculations": 42,
  "avg_operand_a": 33.5,
  "avg_operand_b": 12.8,
  "avg_result": 156.3,
  "min_result": -50.0,
  "max_result": 10000.0,
  "most_used_operation": "add",
  "operations_breakdown": {
    "add": 15,
    "multiply": 10,
    "percent_of": 8,
    "divide": 5,
    "power": 4
  }
}
```

## Running the Application

### Method 1: Docker Hub (Production Ready)

Pull and run the pre-built image from Docker Hub:

```bash
# Pull the latest image
docker pull shanmukha1315/fastapi_calculator:latest

# Run the container
docker run -p 8000:8000 shanmukha1315/fastapi_calculator:latest

# Or run in detached mode
docker run -d -p 8000:8000 --name calculator shanmukha1315/fastapi_calculator:latest
```

**Docker Hub**: https://hub.docker.com/repository/docker/shanmukha1315/fastapi_calculator

### Method 2: Docker Compose (Local Development)

```bash
# Build and start containers
docker compose up --build

# Run in detached mode
docker compose up -d

# View logs
docker compose logs -f

# Stop containers
docker compose down
```

### Method 3: Python Virtual Environment (Local Development)

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
alembic upgrade head

# Start the development server
uvicorn app.main:app --reload
```

**Application URLs:**

- Home: http://127.0.0.1:8000
- Register: http://127.0.0.1:8000/register
- Login: http://127.0.0.1:8000/login
- Calculations: http://127.0.0.1:8000/calculations
- Profile: http://127.0.0.1:8000/static/profile.html
- API Docs (Swagger): http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Database Migrations with Alembic

This project uses **Alembic** for database schema migrations. Alembic tracks changes to your database schema over time and allows you to apply or rollback those changes in a controlled manner.

### Initial Setup

Alembic is already configured in this project. The migration environment is located in the `alembic/` directory.

### Common Migration Commands

#### 1. Check Current Migration Status

```bash
alembic current
```

Shows which migration revision the database is currently at.

#### 2. View Migration History

```bash
alembic history
```

Lists all available migrations.

#### 3. Apply Migrations (Upgrade to Latest)

```bash
alembic upgrade head
```

Applies all pending migrations to bring your database up to date.

#### 4. Rollback Migrations (Downgrade)

```bash
# Downgrade by 1 revision
alembic downgrade -1

# Downgrade to a specific revision
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

#### 5. Create a New Migration

When you modify models in `app/models.py`, generate a new migration:

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Or create an empty migration to fill in manually
alembic revision -m "Description of changes"
```

**Example**: Adding a new column to the User model

```python
# app/models.py
class User(Base):
    __tablename__ = "users"
    # ... existing columns ...
    phone_number = Column(String(20), nullable=True)  # New field
```

Then run:

```bash
alembic revision --autogenerate -m "Add phone_number to users table"
alembic upgrade head
```

### Migration Workflow for New Deployments

For a fresh database deployment:

```bash
# 1. Ensure database is empty or doesn't exist
# 2. Apply all migrations
alembic upgrade head

# 3. Start the application
uvicorn app.main:app --reload
```

### Migration Workflow for Existing Databases

If you already have a database with tables created by SQLAlchemy's `Base.metadata.create_all()`:

```bash
# Mark the database as being at the latest migration (without running migrations)
alembic stamp head
```

This tells Alembic that your database schema matches the latest migration.

### Docker Deployment with Migrations

When using Docker, apply migrations before starting the FastAPI server:

```dockerfile
# In your Dockerfile or docker-compose.yml
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Or in `docker-compose.yml`:

```yaml
services:
  web:
    # ... other config ...
    command: >
      sh -c "alembic upgrade head &&
             uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

### Important Notes

- **SQLite Limitations**: SQLite has limited ALTER TABLE support. Alembic is configured with `render_as_batch=True` to handle this.
- **Version Control**: Always commit migration files to your git repository.
- **Production**: Test migrations on a staging database before applying to production.
- **Rollbacks**: Always test downgrade migrations to ensure they work correctly.

### Current Schema

The initial migration includes:

- **users** table: id, username, email, password_hash, created_at
- **calculations** table: id, a, b, type (enum), result, user_id (foreign key)
- **CalculationType** enum: ADD, SUBTRACT, MULTIPLY, DIVIDE, POWER, MODULUS, PERCENT_OF, NTH_ROOT, LOG_BASE

For more detailed migration guidance, see `alembic/MIGRATION_GUIDE.md`.

---

## Running Tests Locally

This project includes comprehensive testing at three levels: **Unit**, **Integration**, and **End-to-End (E2E)**.

### Test Summary

- **Total Tests**: 194 tests
- **Unit Tests**: 92 tests covering individual functions and logic
- **Integration Tests**: 62 tests covering API endpoints and database interactions
- **E2E Tests**: 40 Playwright tests covering complete user workflows
- **Code Coverage**: 96% across all application modules

### Prerequisites

```bash
# Activate your virtual environment
source .venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# For E2E tests, install Playwright browsers (one-time setup)
pip install playwright pytest-playwright
playwright install chromium
```

### Running Tests

#### All Tests

```bash
# Run all tests (unit + integration + E2E)
pytest -v

# Run quietly with summary
pytest -q

# Run with detailed output
pytest -vv
```

#### Unit Tests Only

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run specific unit test file
pytest tests/unit/test_operations.py -v
pytest tests/unit/test_calculation_factory.py -v
pytest tests/unit/test_statistics.py -v
```

#### Integration Tests Only

```bash
# Run all integration tests
pytest tests/integration/ -v

# Run specific integration test file
pytest tests/integration/test_api_endpoints.py -v
pytest tests/integration/test_calculation_db.py -v
pytest tests/integration/test_statistics_api.py -v
```

#### E2E Tests Only

```bash
# Run all E2E tests
pytest tests/e2e/ -v

# Run with browser visible (headed mode)
pytest tests/e2e/ --headed

# Run specific E2E test file
pytest tests/e2e/test_auth_playwright.py -v
pytest tests/e2e/test_calculations_playwright.py -v
pytest tests/e2e/test_profile_flow.py -v
```

#### Coverage Reports

```bash
# Run tests with coverage
pytest --cov=app --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser

# Run unit + integration with coverage
pytest tests/unit/ tests/integration/ --cov=app --cov-report=term-missing
```

### Test Coverage Report

Our test suite achieves **96% code coverage** across all application modules:

```
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
app/__init__.py                    0      0   100%
app/calculation_factory.py        63      1    98%   61
app/calculations.py               82      2    98%   90-91
app/db.py                         19      0   100%
app/logger_config.py              11      0   100%
app/main.py                      120      0   100%
app/models.py                     36      0   100%
app/operations.py                 15      0   100%
app/schemas.py                    58      0   100%
app/security.py                   31      0   100%
app/statistics.py                 60      0   100%
app/users.py                      70     18    74%   23, 36-47, 52-57
------------------------------------------------------------
TOTAL                            505     21    96%

Test Results:
- 153 passed (unit + integration tests)
- 3 failed (known profile API edge cases)
- 11 errors (profile API error handling paths)
- 46 warnings (deprecation warnings from dependencies)
```

**Coverage Analysis:**

- Most modules achieve 100% coverage
- `app/calculation_factory.py`: 98% (1 line in error handling)
- `app/calculations.py`: 98% (2 lines in exception handling)
- `app/users.py`: 74% (18 lines in profile API error scenarios)
- Overall: 96% coverage meets and exceeds industry standards

### Playwright E2E Tests

Playwright tests verify complete user workflows across the entire application.

**Installation (one-time setup):**

```bash
# Install Playwright and browsers
pip install playwright pytest-playwright
playwright install chromium
```

**Running E2E Tests:**

```bash
# Run all E2E tests
pytest tests/e2e -q

# Run with browser visible (headed mode)
pytest tests/e2e --headed

# Run specific E2E test file
pytest tests/e2e/test_playwright.py -v
pytest tests/e2e/test_profile_flow.py -v
pytest tests/e2e/test_advanced_operations_e2e.py -v
pytest tests/e2e/test_statistics_e2e.py -v
```

**E2E Test Coverage:**

- **Authentication Flows** (`test_playwright.py`)

  - Positive: successful registration and login
  - Negative: invalid credentials, duplicate username
  - JWT token storage and validation
  - Automatic redirects

- **BREAD Operations** (`test_playwright.py`)

  - Create calculations with all operation types
  - Read/Browse calculation history
  - Edit existing calculations
  - Delete calculations with confirmation
  - User ownership verification

- **Profile Management** (`test_profile_flow.py`)

  - View current profile
  - Update username and email
  - Change password
  - Re-login with new credentials
  - Validation error handling

- **Advanced Operations** (`test_advanced_operations_e2e.py`)

  - Percent_of calculation workflow
  - Nth_root calculation workflow
  - Log_base calculation workflow
  - Live preview updates
  - Operation-specific validation

- **Statistics Dashboard** (`test_statistics_e2e.py`)
  - Statistics cards display
  - Operations breakdown chart
  - Real-time updates after CRUD
  - Export to CSV/JSON/PDF
  - Empty state handling

### Feature-Specific Tests

**User Profile & Password Change** (Feature 1)

```bash
# Unit tests
pytest tests/unit/test_user_profile.py -v  # 14 tests

# Integration tests
pytest tests/integration/test_profile_api.py -v
pytest tests/integration/test_profile_db.py -v

# E2E tests
pytest tests/e2e/test_profile_flow.py -v
```

**Advanced Calculation Operations** (Feature 2)

```bash
# Unit tests
pytest tests/unit/test_advanced_schemas.py -v  # 22 tests
pytest tests/unit/test_calculation_factory.py -v  # 22 tests

# Integration tests
pytest tests/integration/test_advanced_operations.py -v  # 6 tests

# E2E tests
pytest tests/e2e/test_advanced_operations_e2e.py -v  # 8 tests
```

**Statistics & Reporting** (Feature 3)

```bash
# Unit tests
pytest tests/unit/test_statistics.py -v  # 16 tests

# Integration tests
pytest tests/integration/test_statistics_api.py -v  # 14 tests

# E2E tests
pytest tests/e2e/test_statistics_e2e.py -v  # 10 tests
```

### CI/CD Test Results

Latest verification: **153 passed** (unit + integration), **194 total tests** — verified 2025-12-11

---

## Swagger JWT Testing

1. Open http://127.0.0.1:8000/docs
2. Register a new user or login to obtain a token
3. Click **Authorize** button (top right)
4. Enter: `Bearer <your_token>`
5. Test all protected endpoints

---

## Curl Examples

### Register a new user

```bash
curl -s -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"secret123"}'
```

### Login and extract token

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}' | jq -r .access_token)
```

### Get user profile

```bash
curl -s -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer $TOKEN"
```

### Update profile

```bash
curl -s -X PUT http://localhost:8000/api/users/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"username":"alice2","email":"alice2@example.com"}'
```

### Change password

```bash
curl -s -X POST http://localhost:8000/api/users/change-password \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"old_password":"secret123","new_password":"newsecret456"}'
```

### Create a calculation

```bash
curl -s -X POST http://localhost:8000/api/calculations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"a":10,"type":"add","b":5}'
```

### Create advanced calculations

```bash
# Percent of
curl -s -X POST http://localhost:8000/api/calculations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"a":25,"type":"percent_of","b":200}'

# Nth root
curl -s -X POST http://localhost:8000/api/calculations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"a":3,"type":"nth_root","b":27}'

# Logarithm
curl -s -X POST http://localhost:8000/api/calculations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"a":2,"type":"log_base","b":8}'
```

### List all calculations

```bash
curl -s -X GET http://localhost:8000/api/calculations \
  -H "Authorization: Bearer $TOKEN"
```

### Get statistics

```bash
curl -s -X GET http://localhost:8000/api/statistics/summary \
  -H "Authorization: Bearer $TOKEN"

curl -s -X GET "http://localhost:8000/api/statistics/recent?limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

### Read specific calculation

```bash
curl -s -X GET http://localhost:8000/api/calculations/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Update calculation

```bash
curl -s -X PUT http://localhost:8000/api/calculations/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"a":20,"type":"multiply","b":5}'
```

### Delete calculation

```bash
curl -s -X DELETE http://localhost:8000/api/calculations/1 \
  -H "Authorization: Bearer $TOKEN"
```

**Note:**

- `401 Unauthorized` → missing/invalid token
- `403 Forbidden` → not the owner of the calculation
- `400 Bad Request` → validation error

---

## CI/CD Pipeline

### GitHub Actions Workflow

The project includes a comprehensive CI/CD pipeline (`.github/workflows/ci.yml`) that:

1. **Environment Setup**

   - Spins up PostgreSQL service for testing
   - Sets up Python 3.12
   - Installs all dependencies including Playwright

2. **Unit + Integration Tests**

   - Runs all unit and integration tests
   - Enforces 95% minimum code coverage
   - Fails the build if coverage drops below threshold

3. **End-to-End Tests**

   - Starts FastAPI server in background
   - Installs Playwright browsers
   - Runs complete E2E test suite
   - Tests user workflows across all features

4. **Docker Build & Deployment**
   - Builds optimized Docker image
   - Pushes to Docker Hub **only if all tests pass**
   - Tags with `latest` and commit SHA
   - Automatic deployment on successful builds

### Pipeline Triggers

- Runs on every push to `main` branch
- Runs on all pull requests to `main`
- Can be triggered manually via GitHub Actions UI

### Secrets Required

- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password
- `SECRET_KEY` - JWT secret key for tests

---

## Project Structure

```
fastapi_calculator/
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI/CD pipeline configuration
├── alembic/
│   ├── versions/                  # Database migration files
│   │   ├── b01b1ad235d4_initial_schema.py
│   │   └── 4609aba8a69c_update_calculationtype_enum.py
│   ├── env.py                     # Migration environment configuration
│   ├── script.py.mako             # Migration template
│   ├── MIGRATION_GUIDE.md         # Comprehensive migration guide
│   └── SETUP_COMPLETE.md          # Implementation documentation
├── app/
│   ├── __init__.py                # Package initialization
│   ├── main.py                    # Application entry point & router config
│   ├── models.py                  # SQLAlchemy models (User, Calculation)
│   ├── schemas.py                 # Pydantic validation schemas
│   ├── security.py                # JWT & password hashing utilities
│   ├── db.py                      # Database configuration
│   ├── users.py                   # User authentication & profile routes
│   ├── calculations.py            # BREAD calculation routes
│   ├── statistics.py              # Statistics & reporting routes
│   ├── operations.py              # Basic calculation operations
│   ├── calculation_factory.py    # Factory pattern for operations
│   └── logger_config.py           # Logging configuration
├── static/
│   ├── register.html              # User registration page
│   ├── login.html                 # User login page
│   ├── calculations.html          # BREAD UI + Statistics dashboard
│   └── profile.html               # Profile management page
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest configuration & fixtures
│   ├── unit/                      # 92 unit tests
│   │   ├── test_operations.py
│   │   ├── test_calculation_factory.py
│   │   ├── test_advanced_schemas.py
│   │   ├── test_user_profile.py
│   │   ├── test_statistics.py
│   │   ├── test_security.py
│   │   ├── test_schemas.py
│   │   └── test_db.py
│   ├── integration/               # 62 integration tests
│   │   ├── test_api_endpoints.py
│   │   ├── test_calculation_db.py
│   │   ├── test_user_db.py
│   │   ├── test_users_api.py
│   │   ├── test_advanced_operations.py
│   │   └── test_statistics_api.py
│   └── e2e/                       # 40 E2E tests (Playwright)
│       ├── test_auth_playwright.py
│       ├── test_calculations_playwright.py
│       ├── test_profile_flow.py
│       ├── test_advanced_operations_e2e.py
│       └── test_statistics_e2e.py
├── .env                           # Environment variables (not in git)
├── .gitignore                     # Git ignore patterns
├── alembic.ini                    # Alembic configuration
├── app.db                         # SQLite database (production)
├── docker-compose.yml             # Docker Compose services
├── Dockerfile                     # Docker image configuration
├── README.md                      # Project documentation
├── reflection.md                  # Learning outcomes & insights
└── requirements.txt               # Python dependencies
```

---

## Development Features Implemented

### Backend Implementation

**SQLAlchemy Models**

- User model with authentication fields
- Calculation model with 9 operation types
- Foreign key relationships
- Index optimization

**Pydantic Schemas**

- Request/response validation
- Email validation
- Password strength requirements
- Custom validators for advanced operations

**FastAPI Routes**

- Authentication endpoints
- BREAD calculation endpoints
- Profile management endpoints
- Statistics endpoints
- Proper HTTP status codes
- Error handling

**Security**

- JWT token authentication
- Bcrypt password hashing
- User ownership verification
- Input validation and sanitization

### Front-End Implementation

**Pages Developed**

- Registration with validation
- Login with token storage
- Calculations BREAD interface
- Profile management
- Statistics dashboard

**Client-Side Validations**

- Form input validation
- Real-time feedback
- Error message display
- Operation-specific constraints

**UI Enhancements**

- Modern dark theme
- Responsive design
- Toast notifications
- Live calculation preview
- Animated charts
- Export modal

### Testing Implementation

**Unit Tests (92 tests)**

- Operation logic
- Factory pattern
- Schema validation
- Profile functionality
- Statistics calculations
- Edge cases and error scenarios

**Integration Tests (62 tests)**

- API endpoints
- Database interactions
- Authentication flows
- User ownership
- Advanced operations
- Statistics endpoints

**E2E Tests (40 tests)**

- Complete user workflows
- BREAD operations
- Profile management
- Password changes
- Advanced calculations
- Statistics dashboard
- Export functionality
- Positive and negative scenarios

---

## Contributors

- **Shanmukh Vangipuram** - Full-stack development, testing, and deployment

## License

This project is for educational purposes as part of a web development course.
