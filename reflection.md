# Module 10 Reflection – Secure User Model & CI/CD

## What I built

In this module I extended my existing FastAPI Calculator into a more realistic web API by adding a secure user model and a full CI/CD pipeline. I implemented a `User` table in PostgreSQL using SQLAlchemy, created Pydantic schemas (`UserCreate`, `UserRead`) for validation and response models, and added user creation logic with proper error handling for duplicate usernames and emails. On top of that, I wired everything into GitHub Actions so that every push to `main` runs tests, builds a Docker image, and pushes it to Docker Hub.

## Key learning

The main technical learning for me was how all layers fit together:

- **Security:** Instead of storing plain-text passwords I used Passlib’s `CryptContext` to hash passwords and verify them during authentication. I also had to make sure the SQLAlchemy model enforces uniqueness constraints so that invalid states are rejected at the database level.
- **Testing:** I created unit tests for the hashing utilities and user schemas, plus integration tests that hit the `/api/users` endpoint using a test database. Getting to 100% coverage forced me to think about edge cases such as duplicate usernames and invalid input.
- **CI/CD:** Configuring GitHub Actions with a PostgreSQL service container and environment variables was new. I learned how to install Playwright in CI, run unit + integration + E2E tests, and then reuse the same workflow to build and push a Docker image to Docker Hub.

## Challenges and how I solved them

One challenge was making the tests run against a clean test database instead of my development database. I fixed this by introducing a `TEST_DATABASE_URL` environment variable and overriding the SQLAlchemy engine dependency in `tests/conftest.py`. Another tricky part was debugging the Docker Hub login in CI. At first the workflow failed with “username and password required” and “insufficient scopes”. I resolved this by creating a Personal Access Token in Docker Hub with read/write permissions and storing it as `DOCKERHUB_TOKEN` and `DOCKERHUB_USERNAME` GitHub secrets, then updating `ci.yml` to use those.

## Why this matters

This module felt close to a “real” production workflow. I now understand how to:

- Design a secure user model with proper hashing and uniqueness.
- Write automated tests that run in CI on every commit.
- Package a FastAPI app into a Docker image and publish it to Docker Hub via GitHub Actions.

These skills are directly transferable to industry projects where security, testing, and automation are expected by default.
