# FastAPI Calculator

Full-stack calculator with JWT authentication, 9 calculation operations, profile management, statistics dashboard, and comprehensive testing. Features modern UI, Docker deployment, and CI/CD pipeline with automated Docker Hub publishing.

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

## Features

**Core Functionality**

- JWT-based authentication with secure password hashing
- User-scoped calculation BREAD operations
- 9 operation types: add, subtract, multiply, divide, power, modulus, percent_of, nth_root, log_base
- User profile management with username/email updates
- Password change with validation
- Statistics dashboard with visual charts
- Multi-format export (CSV, JSON, PDF)

**UI Features**

- Dark/light theme toggle with persistence
- Real-time toast notifications
- Live calculation preview
- Search and filter calculations
- Animated operations breakdown chart
- Color-coded operation pills
- Account dropdown menu
- Responsive mobile-first design

**Testing & Deployment**

- 194 comprehensive tests (96% coverage)
- 92 unit tests, 62 integration tests, 40 E2E tests
- GitHub Actions CI/CD pipeline
- Automated Docker Hub deployment
- Database migrations with Alembic

## Important Links

| Resource              | URL                                                       |
| --------------------- | --------------------------------------------------------- |
| **GitHub Repository** | https://github.com/shanmukh1315/fastapi_calculator        |
| **Docker Hub**        | https://hub.docker.com/r/shanmukha1315/fastapi_calculator |
| Application           | http://127.0.0.1:8000                                     |
| API Docs (Swagger)    | http://127.0.0.1:8000/docs                                |
| Register              | http://127.0.0.1:8000/register                            |
| Login                 | http://127.0.0.1:8000/login                               |
| Calculations          | http://127.0.0.1:8000/calculations                        |
| Profile               | http://127.0.0.1:8000/static/profile.html                 |

## API Endpoints

### Authentication

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

### Docker Hub (Production)

```bash
docker pull shanmukha1315/fastapi_calculator:latest
docker run -p 8000:8000 shanmukha1315/fastapi_calculator:latest
```

### Docker Compose (Local)

```bash
docker compose up --build
```

### Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Testing

### Run All Tests

```bash
pytest -v                                    # All tests
pytest --cov=app --cov-report=term-missing  # With coverage
pytest tests/unit/ -v                       # Unit tests only
pytest tests/integration/ -v                # Integration tests only
pytest tests/e2e/ -v                        # E2E tests only
```

### E2E Tests (Playwright)

```bash
# Install browsers (one-time)
playwright install chromium

# Run E2E tests
pytest tests/e2e/ -v
pytest tests/e2e/ --headed  # With visible browser
```

**Test Coverage**: 194 total tests, 96% code coverage

## Database Migrations

### Common Commands

```bash
alembic upgrade head     # Apply all migrations
alembic current          # Check current version
alembic history          # View migration history
alembic downgrade -1     # Rollback one version
```

### Create New Migration

```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## API Testing with cURL

```bash
# Register
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"secret123"}'

# Login and get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}' | jq -r .access_token)

# Get profile
curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer $TOKEN"

# Create calculation
curl -X POST http://localhost:8000/api/calculations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"a":10,"type":"add","b":5}'

# Get statistics
curl -X GET http://localhost:8000/api/statistics/summary \
  -H "Authorization: Bearer $TOKEN"
```

## CI/CD Pipeline

**GitHub Actions** workflow automatically:

- Runs all tests (unit, integration, E2E)
- Enforces 95% code coverage
- Builds Docker image
- Pushes to Docker Hub (only if all tests pass)
- Tags with `latest` and commit SHA

**Triggers**: Push to `main`, pull requests, manual

## Project Structure

```
fastapi_calculator/
├── app/
│   ├── main.py                    # Application entry & routes
│   ├── models.py                  # SQLAlchemy models
│   ├── schemas.py                 # Pydantic schemas
│   ├── security.py                # JWT & hashing
│   ├── users.py                   # Auth & profile routes
│   ├── calculations.py            # BREAD routes
│   ├── statistics.py              # Statistics routes
│   ├── calculation_factory.py    # Operation factory
│   └── operations.py              # Calculation logic
├── static/
│   ├── register.html              # Registration page
│   ├── login.html                 # Login page
│   ├── calculations.html          # Main calculator UI
│   └── profile.html               # Profile management
├── tests/
│   ├── unit/                      # 92 unit tests
│   ├── integration/               # 62 integration tests
│   └── e2e/                       # 40 Playwright E2E tests
├── alembic/                       # Database migrations
├── .github/workflows/ci.yml       # CI/CD pipeline
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---
