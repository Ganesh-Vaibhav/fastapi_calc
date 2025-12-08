# Reflection Document

## Project Overview
This project involved enhancing a basic FastAPI calculator application by adding user authentication and BREAD (Browse, Read, Edit, Add, Delete) functionality for calculations. The goal was to transform a simple API into a multi-user application where users can securely manage their own calculation history.

## Key Implementations

### 1. User Authentication
- **JWT (JSON Web Tokens)**: Implemented stateless authentication using `python-jose`.
- **Security**: Passwords are hashed using `bcrypt` (via `passlib`).
- **Endpoints**: Added `/users/register` and `/users/login`.
- **Dependency**: Created `get_current_user` dependency to secure protected routes.

### 2. BREAD Functionality
- **Models**: Updated `Calculation` model to include `user_id` foreign key.
- **API**:
    - **Browse**: `GET /calculations` (filtered by current user).
    - **Read**: `GET /calculations/{id}` (user ownership check).
    - **Add**: `POST /calculations` (automatically associated with current user).
    - **Edit**: `PUT /calculations/{id}`.
    - **Delete**: `DELETE /calculations/{id}`.
- **Frontend**:
    - Created a Single Page Application (SPA) using vanilla JS.
    - Implemented dynamic view switching (Auth vs Dashboard).
    - Added forms for adding and editing calculations.
    - Integrated JWT handling in `localStorage`.

### 3. Testing
- **E2E Testing**: Updated Playwright tests to cover the full user flow:
    - Registration -> Login -> Add -> Verify -> Edit -> Verify -> Delete -> Verify -> Logout.
- **Challenges**:
    - **Database Isolation**: Configured SQLite for testing to avoid dependency on PostgreSQL during local development.
    - **Port Conflicts**: Handled `Address already in use` errors by identifying and killing stale processes.
    - **Frontend/Backend Sync**: Debugged issues where frontend error handling didn't match backend exception responses.

## Lessons Learned
- **Frontend Error Handling**: It's crucial to align frontend error parsing with backend exception structures. Custom exception handlers can change the expected response format (e.g., `error` vs `detail`).
- **Test Environment**: Ensuring a clean and isolated test environment (DB, ports) is vital for reliable E2E tests. Using `sqlite` for tests simplified the setup but required careful configuration in `conftest.py`.
- **Debugging**: Effective debugging of E2E tests requires a mix of console logging, screenshots, and server logs.

## Future Improvements
- **PostgreSQL Integration**: Fully enable PostgreSQL for production and CI environments.
- **UI Enhancements**: Improve the design with a CSS framework like Tailwind or Bootstrap.
- **Pagination**: Implement pagination in the frontend for the calculation list.
