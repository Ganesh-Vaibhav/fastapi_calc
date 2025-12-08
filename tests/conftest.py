import subprocess
import time
import pytest
from playwright.sync_api import sync_playwright
import requests
import sys
import os

# Set test database URL before importing app
os.environ["TEST_DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from main import app
from app.users import get_db
from app.db import Base, engine, SessionLocal

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope='session')
def fastapi_server():
    """
    Fixture to start the FastAPI server before E2E tests and stop it after tests complete.
    """
    # Determine Python command
    python_cmd = sys.executable
    
    # Get the project root directory (parent of tests directory)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Start FastAPI app using uvicorn directly
    log_file = open("server.log", "w")
    fastapi_process = subprocess.Popen(
        [python_cmd, '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000'],
        cwd=project_root,
        stdout=log_file,
        stderr=log_file
    )
    
    # Define the URL to check if the server is up
    server_url = 'http://127.0.0.1:8000/'
    
    # Wait for the server to start by polling the root endpoint
    timeout = 30  # seconds
    start_time = time.time()
    server_up = False
    
    print("Starting FastAPI server...")
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(server_url)
            if response.status_code == 200:
                server_up = True
                print("FastAPI server is up and running.")
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    
    if not server_up:
        fastapi_process.terminate()
        raise RuntimeError("FastAPI server failed to start within timeout period.")
    
    yield
    
    # Terminate FastAPI server
    print("Shutting down FastAPI server...")
    fastapi_process.terminate()
    fastapi_process.wait()
    print("FastAPI server has been terminated.")

@pytest.fixture(scope="session")
def playwright_instance_fixture():
    """
    Fixture to manage Playwright's lifecycle.
    """
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance_fixture):
    """
    Fixture to launch a browser instance.
    """
    browser = playwright_instance_fixture.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    """
    Fixture to create a new page for each test.
    """
    page = browser.new_page()
    yield page
    page.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture
def test_user(client):
    user_data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 201
    return user_data

@pytest.fixture
def token(client, test_user):
    response = client.post("/users/login", json={"username": test_user["username"], "password": test_user["password"]})
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}",
    }
    return client
