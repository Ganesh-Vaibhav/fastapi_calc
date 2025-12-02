


def test_create_user_and_uniqueness(client, db_session):
    response = client.post(
        "/users/register",
        json={"username": "alice", "email": "alice@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"

    # Duplicate username
    response_dup_username = client.post(
        "/users/register",
        json={"username": "alice", "email": "alice2@example.com", "password": "password123"},
    )
    assert response_dup_username.status_code == 400

    # Duplicate email
    response_dup_email = client.post(
        "/users/register",
        json={"username": "alice2", "email": "alice@example.com", "password": "password123"},
    )
    assert response_dup_email.status_code == 400



def test_login_user(client, db_session):
    # Register user
    client.post(
        "/users/register",
        json={"username": "bob", "email": "bob@example.com", "password": "password123"},
    )
    
    # Login success
    response = client.post(
        "/users/login",
        json={"password": "password123"},
        params={"username": "bob"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] is True
    assert data["user"]["username"] == "bob"

    # Login failure
    response_fail = client.post(
        "/users/login",
        json={"password": "wrongpassword"},
        params={"username": "bob"}
    )
    assert response_fail.status_code == 401
