# Reflection — Module 13: JWT Auth, Front-End Validation & Playwright E2E

In this module, I extended my FastAPI Calculator into a fully authenticated web application by adding JWT-based login/registration, client-side validated front-end pages, and Playwright end-to-end tests. The /register and /login routes now validate inputs, hash passwords, and return JWT tokens that the front-end stores in localStorage. All calculation endpoints under /api/calculations are protected using a get_current_user dependency to enforce user ownership and security.

A major learning outcome was integrating the front-end and back-end flows smoothly. I implemented simple HTML+JavaScript pages with checks for email format, password confirmation, and minimum password length. Testing this end-to-end with Playwright helped verify real user behavior—including both positive paths (successful registration + login) and negative scenarios (short password, wrong credentials). This made the system feel much more complete and production-like.

Another important milestone was getting these flows to run in GitHub Actions CI/CD. The workflow now spins up PostgreSQL, installs Chromium, runs unit + integration tests, then runs Playwright E2E before building and pushing a Docker image to Docker Hub. Fixing timing issues and making sure the server was ready before tests run taught me a lot about real-world pipeline reliability.

Overall, this module tied together backend authentication, frontend validation, containerization, DevOps, and automated UI testing. It strengthened my confidence in building full-stack features that are secure, testable, and deployable.
