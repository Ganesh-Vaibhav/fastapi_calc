# Reflection: JWT Authentication, E2E Testing & CI/CD

## Key Experiences

Developing the authentication system and end-to-end tests for this FastAPI application provided valuable hands-on experience with modern web development practices. Key highlights include:

1.  **Secure Authentication**: Implementing user registration and login endpoints required a deep dive into security best practices. I used `passlib` with `pbkdf2_sha256` to securely hash passwords before storing them in the database, ensuring that sensitive user credentials are never exposed in plain text.
2.  **RESTful API Development**: Building the User and Calculation routes reinforced the principles of REST. I utilized Pydantic schemas (`UserCreate`, `UserRead`) to validate incoming data and structure API responses, ensuring type safety and automatic documentation.
3.  **Database Integration**: Integrating SQLAlchemy with FastAPI allowed for efficient database management. I learned to model relationships between `Users` and `Calculations`, using Foreign Keys to associate data securely with specific users.
4.  **Automated Testing Strategy**:
    *   **Unit & Integration Tests**: I wrote comprehensive tests using `pytest` and `FastAPI TestClient` to verify the logic of my API endpoints and database interactions.
    *   **End-to-End (E2E) Tests**: Implementing Playwright tests was a major step forward. I created tests to verify the actual user experience, such as the calculator functionality (`test_calculator_add`, `test_calculator_divide_by_zero`), ensuring the front-end interacts correctly with the backend.
5.  **CI/CD & DevOps**: Configuring GitHub Actions to automatically run the full test suite (Unit, Integration, E2E) on every push was critical. This pipeline ensures that no broken code reaches the main branch and automatically builds and pushes a Docker image to Docker Hub upon success.

## Challenges Faced & Solutions

### 1. Database Connection in Tests
**Challenge**: Integration tests initially failed because they attempted to connect to a PostgreSQL database that wasn't running in the local test environment.
**Solution**: I configured the test suite to use an in-memory SQLite database (`sqlite:///:memory:`) when running locally. This involved modifying `conftest.py` to set a `TEST_DATABASE_URL` and ensuring the SQLAlchemy engine used `StaticPool` to maintain the connection state across test functions.

### 2. Password Hashing Compatibility
**Challenge**: I encountered a `ValueError: password cannot be longer than 72 bytes` when using `bcrypt` with `passlib`. This was due to a specific version incompatibility in the environment.
**Solution**: I switched the hashing scheme to `pbkdf2_sha256`. This algorithm is secure, standard-compliant, and resolved the compatibility issue, allowing for reliable password hashing without length constraints.

### 3. Test Isolation & Transaction Management
**Challenge**: Tests were interfering with each other's state. A `rollback()` triggered in one test would sometimes affect the shared database session of another, causing sporadic failures.
**Solution**: I implemented nested transactions (savepoints) in the `db_session` fixture. Each test now runs within its own savepoint, which is rolled back at the end of the test. This ensures complete isolation, so the database state remains clean for every test case.

## Learning Outcomes

This project successfully addressed the following learning outcomes:

*   **CLO3: Create Python applications with automated testing.**
    *   Implemented a robust test suite including `tests/unit`, `tests/integration`, and `tests/e2e` using Pytest and Playwright.
*   **CLO4: Set up GitHub Actions for Continuous Integration (CI).**
    *   Created a `.github/workflows/ci.yml` file that automates testing and linting on every commit.
*   **CLO9: Apply containerization techniques using Docker.**
    *   Built a `Dockerfile` to containerize the FastAPI application and configured the CI pipeline to push the image to Docker Hub.
*   **CLO10: Create, consume, and test REST APIs using Python.**
    *   Developed `/users/register`, `/users/login`, and calculation BREAD endpoints using FastAPI.
*   **CLO11: Integrate Python programs with SQL databases.**
    *   Used SQLAlchemy ORM to interact with a PostgreSQL database (and SQLite for testing), managing complex data models and relationships.
*   **CLO12: Serialize, deserialize, and validate JSON using Pydantic.**
    *   Defined Pydantic models (`UserCreate`, `CalculationRead`) to enforce data validation rules and schema consistency.
*   **CLO13: Implement secure authentication and authorization techniques.**
    *   Applied password hashing using `passlib` and designed a secure login flow to protect user credentials.
