# Module 11 Reflection – Calculation Model, Factory Pattern & CI/CD

## What I built

In Module 10 I focused on securing my FastAPI Calculator with a proper `User` model, password hashing, database tests, and a GitHub Actions pipeline that runs tests and pushes a Docker image to Docker Hub. In Module 11 I extended that foundation by adding a `Calculation` model, Pydantic schemas, and an optional factory pattern, and by wiring all of this into my existing testing and CI/CD setup.

I implemented a new `Calculation` SQLAlchemy model with fields for `a`, `b`, `type`, and an optional `result`, plus an optional `user_id` foreign key back to the `User` table. On the Pydantic side, I created `CalculationCreate` and `CalculationRead` schemas that validate and serialize calculation data, including protection against invalid inputs like division by zero. To keep the calculation logic clean and extensible, I added a small factory pattern that maps a `CalculationType` enum (`add`, `subtract`, `multiply`, `divide`) to the correct operation class. Finally, I wrote unit tests for the factory and schema validation, and integration tests that insert `Calculation` records into the database, verify the stored result, and confirm the user foreign-key relationship works as expected. All of these tests now run automatically in my existing GitHub Actions pipeline, which still builds and pushes a Docker image to Docker Hub on success.

## Key learning

The main learning in this module was how to model domain logic in a way that is both **type-safe and testable**:

- **Data modeling with SQLAlchemy:** Defining the `Calculation` model and linking it to `User` through a foreign key made me think more carefully about relationships and how calculations belong to specific users in a realistic application.
- **Validation with Pydantic:** By adding `CalculationCreate` and `CalculationRead` schemas, I saw how Pydantic can enforce rules such as “no division by zero” and restrict the `type` field to an enum, so bad data is caught before it touches the database.
- **Factory pattern:** Implementing a simple factory for operations showed me how design patterns can keep business logic organized and open for extension. If I ever add new operations (like `power` or `mod`), the data model and tests can stay stable while the factory grows.
- **Testing and CI/CD:** Extending my existing tests to cover the new model, schemas, and factory reminded me that each new feature should come with its own tests. Seeing everything run in GitHub Actions against a real PostgreSQL service reinforced the value of automated pipelines and containerization.

## Challenges and how I solved them

One challenge was keeping the responsibilities clearly separated. It was tempting to compute results directly inside the SQLAlchemy model or to mix calculation logic into the API layer. I solved this by using the factory pattern plus a small CRUD helper so the steps are explicit: validate input with Pydantic, choose the operation via the factory, compute the result, and then persist the `Calculation` object.

Another challenge was making sure tests worked in both local and CI environments. Locally I use SQLite by default for speed, while the GitHub Actions workflow uses PostgreSQL via `TEST_DATABASE_URL`. I relied on the shared SQLAlchemy `Base` metadata and test fixtures so that the same tests run cleanly on both backends. This forced me to think about portability and not depend on database-specific features.

## Why this matters

Combining Module 10 and Module 11, I now have a small but realistic FastAPI service that includes user management, a typed `Calculation` model, strong validation, automated tests, and a CI/CD pipeline that builds and ships a Docker image. This directly supports the course learning outcomes around automated testing, DevOps practices, containerization, SQL integration, JSON validation with Pydantic, and secure application design. The experience feels very close to how a real team would evolve a service over multiple iterations: add a new feature, model it carefully, write tests, and make sure the pipeline still stays green.
