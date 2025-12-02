# Reflection: User & Calculation Routes + Integration Testing

## Key Experiences
Developing the User and Calculation routes for this FastAPI application was a comprehensive exercise in building robust backend services. Key experiences included:

1.  **RESTful API Design**: Implementing BREAD (Browse, Read, Edit, Add, Delete) operations for calculations reinforced the principles of RESTful design. Using Pydantic schemas for request and response validation ensured data integrity and provided clear API documentation via OpenAPI.
2.  **Database Integration**: Integrating SQLAlchemy for ORM mapping allowed for seamless interaction with the database. Managing relationships between Users and Calculations (Foreign Keys) highlighted the importance of data modeling.
3.  **Testing Strategy**: Writing integration tests was crucial. It shifted the focus from just "making it work" to "ensuring it works correctly under various conditions." The use of `pytest` fixtures for database setup and teardown was particularly powerful for maintaining test isolation.
4.  **CI/CD Pipeline**: Configuring GitHub Actions to run tests automatically on every push provided immediate feedback, ensuring that new changes didn't break existing functionality.

## Challenges Faced & Solutions

### 1. Database Connection in Tests
**Challenge**: Initially, the integration tests failed because they tried to connect to a PostgreSQL database that wasn't running locally.
**Solution**: I configured the tests to use SQLite (`sqlite:///:memory:`) for local execution. This required modifying `conftest.py` to set the `TEST_DATABASE_URL` environment variable and ensuring the SQLAlchemy engine used `StaticPool` for in-memory databases.

### 2. Password Hashing Compatibility
**Challenge**: The `passlib` library with `bcrypt` scheme threw a `ValueError: password cannot be longer than 72 bytes` even for short passwords. This was due to a compatibility issue between `passlib` and the installed `bcrypt` version during the internal "wrap bug" detection.
**Solution**: I switched the hashing scheme to `pbkdf2_sha256`, which is a secure and standard alternative that does not suffer from this specific compatibility issue in the current environment.

### 3. Test Isolation
**Challenge**: Tests were interfering with each other. Specifically, a `rollback()` in one request within a test function caused subsequent requests in the same test to fail because the shared transaction was rolled back.
**Solution**: I implemented nested transactions (savepoints) in the `db_session` fixture. This ensures that each test function runs in an isolated transaction that is rolled back at the end, and `rollback()` calls within the application only affect the current savepoint, preserving the test state.

## Learning Outcomes
- **Automated Testing**: I learned how to set up a robust testing environment using `pytest` and `FastAPI TestClient`, covering both success and failure scenarios.
- **DevOps Principles**: I gained practical experience with CI/CD by ensuring the GitHub Actions workflow correctly runs tests and builds Docker images.
- **Security**: Implementing password hashing and user authentication (registration/login) reinforced best practices for securing user data.
- **Debugging**: Troubleshooting the database connection and password hashing errors sharpened my debugging skills, teaching me to look at stack traces and library internals.
