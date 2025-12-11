from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models import User
from app.users import security

def test_update_profile_success(authorized_client: TestClient, test_user: dict, db_session: Session):
    response = authorized_client.put(
        "/users/me",
        json={"username": "newusername", "email": "newemail@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newusername"
    assert data["email"] == "newemail@example.com"
    
    # Verify DB update
    user_model = db_session.query(User).filter(User.username == "newusername").first()
    assert user_model is not None
    assert user_model.email == "newemail@example.com"

def test_update_profile_duplicate_username(authorized_client: TestClient, db_session: Session):
    # Create another user
    other_user = User(username="otheruser", email="other@example.com", password_hash="hash")
    db_session.add(other_user)
    db_session.commit()

    response = authorized_client.put(
        "/users/me",
        json={"username": "otheruser"}
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Username already taken"

def test_change_password_success(authorized_client: TestClient, test_user: dict, db_session: Session):
    old_password = test_user["password"]
    new_password = "newpassword123"
    
    response = authorized_client.post(
        "/users/me/password",
        json={"old_password": old_password, "new_password": new_password}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"

    # Verify new password works (manually check hash)
    user_model = db_session.query(User).filter(User.username == test_user["username"]).first()
    assert security.verify_password(new_password, user_model.password_hash)

def test_change_password_wrong_old(authorized_client: TestClient):
    response = authorized_client.post(
        "/users/me/password",
        json={"old_password": "wrongpassword", "new_password": "newpassword123"}
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Incorrect old password"
