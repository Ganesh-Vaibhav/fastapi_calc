# 📦 Project Setup

---

# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## FastAPI Calculator

A simple calculator API built with FastAPI, supporting basic arithmetic operations and history tracking.
Now includes User Authentication and BREAD (Browse, Read, Edit, Add, Delete) functionality for calculations.

## Features

- **Basic Arithmetic**: Add, Subtract, Multiply, Divide.
- **User Authentication**: Register, Login, Logout (JWT-based).
- **Calculation History**: Save, View, Edit, and Delete your own calculations.
- **Dashboard**: A user-friendly interface to manage calculations.
- **REST API**: Fully documented API with Swagger UI.

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite (PostgreSQL ready).
- **Frontend**: HTML, CSS, JavaScript (Single Page Application).
- **Testing**: Pytest, Playwright (E2E).
- **Containerization**: Docker.

## Setup & Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   uvicorn main:app --reload
   ```
   Open [http://localhost:8000](http://localhost:8000) in your browser.

3. **Run Tests**:
   ```bash
   # Unit and Integration Tests
   pytest tests/unit tests/integration

   # E2E Tests (requires Playwright browsers)
   playwright install chromium
   pytest tests/e2e
   ```

## Docker

Build and run with Docker:
```bash
docker build -t fastapi_calc .
docker run -p 8000:8000 fastapi_calc
```

## API Documentation

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.
## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

# 🚀 6. Running the Project

- **Without Docker**:

```bash
python main.py
```

The application will be available at `http://127.0.0.1:8000`

- **With Docker**:

```bash
docker run -it --rm <image-name>
```

---

# 🧪 7. Running Tests

## Unit Tests

```bash
pytest tests/unit/ -v
```

## Integration Tests

```bash
pytest tests/integration/ -v
```

## End-to-End Tests

```bash
# First, install Playwright browsers
playwright install --with-deps chromium

# Then run E2E tests
pytest tests/e2e/ -v -m e2e
```

## Run All Tests

```bash
pytest tests/ -v
```

## Run Tests with Coverage

```bash
pytest --cov=app --cov-report=term-missing --cov-report=html
```

---

---

# 🧮 Calculation Model Tests

To run the specific tests for the Calculation model:

## Unit Tests

```bash
pytest tests/unit/test_factory.py tests/unit/test_schemas.py
```

## Integration Tests

To run integration tests locally without a running Postgres container, you can use SQLite:

```bash
TEST_DATABASE_URL=sqlite:///./test.db pytest tests/integration/test_calculation_model.py
```

---

# 📝 8. Submission Instructions


After finishing your work:

```bash
git add .
git commit -m "Complete Module X"
git push origin main
```

Then submit the GitHub repository link as instructed.

---

# 🔄 9. GitHub Actions CI/CD

This project includes a GitHub Actions workflow that automatically runs tests on every push and pull request. The workflow:

- Uses Python 3.10
- Runs unit tests, integration tests (including Postgres-backed user tests), and end-to-end tests
- Generates coverage reports
- Installs Playwright browsers for E2E testing

To view the workflow, check `.github/workflows/ci.yml`.

---

# 🔐 Secure User Model & Database

This project includes a secure `User` model backed by PostgreSQL using SQLAlchemy:

- `username` and `email` are unique and required.
- `password_hash` stores a pbkdf2_sha256-hashed password (no plain-text passwords).
- `created_at` records when the user was created.

Pydantic schemas:

- `UserCreate` – used for incoming data when creating users (`username`, `email`, `password`).
- `UserRead` – used for responses, omitting the raw password and exposing `id`, `username`, `email`, `created_at`.

Password hashing uses Passlib with pbkdf2_sha256, with helpers to hash and verify passwords.

Key endpoints:

- `POST /users/register` – create a new user.
- `POST /users/login` – verify credentials and return a simple authenticated response.

### Calculation Routes (BREAD)

- `GET /calculations` – Browse all calculations.
- `GET /calculations/{id}` – Read a specific calculation.
- `POST /calculations` – Add a new calculation.
- `PUT /calculations/{id}` – Edit a calculation.
- `DELETE /calculations/{id}` – Delete a calculation.

---

# 🧪 Database-Backed Tests Locally

To run the integration tests that depend on a database:

**Option 1: Using SQLite (Recommended for local dev)**

The tests are configured to automatically use an in-memory SQLite database if `TEST_DATABASE_URL` is not set to a Postgres URL.

```bash
pytest tests/integration/ -v
```

**Option 2: Using PostgreSQL (Docker)**

1. Start the database (using Docker Compose):

```bash
docker-compose up -d db
```

2. Set the test database URL:

```bash
export TEST_DATABASE_URL=postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/fastapi_db_test
```

3. Run tests:

```bash
pytest tests/integration/ -v
```

---

# 🐳 Docker Hub Image

The GitHub Actions workflow builds and pushes a Docker image to Docker Hub after tests pass.

- Repository: `ganesh396/fastapi_calc`
- tags: `docker pull ganesh396/fastapi_calc:latest`
You can pull and run the image with:

```bash
docker pull ganesh396/fastapi_calc:latest
docker run -it --rm -p 8000:8000 ganesh396/fastapi_calc:latest
```

---

# 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

---

# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is optional depending on the project.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
