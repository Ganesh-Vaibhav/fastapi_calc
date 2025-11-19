# Reflection

## What I implemented
- Added a secure `User` model using SQLAlchemy with unique `username` and `email`, a `password_hash`, and `created_at` timestamp.
- Created Pydantic schemas (`UserCreate`, `UserRead`) to validate and serialize user data.
- Implemented password hashing and verification using Passlib with bcrypt.
- Wrote unit and integration tests, including tests that hit a real Postgres database.
- Configured a GitHub Actions CI pipeline that runs tests, then builds and pushes a Docker image to Docker Hub.

## Challenges and learnings
- **Database integration:** Wiring SQLAlchemy and Postgres into a FastAPI app required careful configuration of the database URL and session handling, especially for tests.
- **Testing with a real DB:** Using a real Postgres instance in both local development (via Docker Compose) and GitHub Actions helped me understand how integration tests can catch issues that unit tests miss (like uniqueness constraints).
- **Security best practices:** Implementing hashed passwords reinforced why raw passwords should never be stored, and how to use libraries like Passlib correctly.
- **CI/CD with GitHub Actions and Docker Hub:** Automating tests and Docker image builds taught me how to connect GitHub Actions with external services (Postgres, Docker Hub) using secrets and multi-step workflows.

## Future improvements
- Add JWT-based authentication and authorization.
- Expand tests to cover more edge cases and error paths in the user and auth endpoints.
- Introduce database migrations (e.g., Alembic) for safer schema evolution.
