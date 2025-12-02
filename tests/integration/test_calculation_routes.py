import pytest
from app import models

def test_create_calculation(client, db_session):
    # First create a user
    user_data = {"username": "calcuser", "email": "calc@example.com", "password": "password123"}
    client.post("/users/register", json=user_data)
    
    # Create calculation
    calc_data = {"a": 10, "b": 5, "type": "add"}
    response = client.post("/calculations/", json=calc_data)
    assert response.status_code == 201
    data = response.json()
    assert data["result"] == 15
    assert data["type"] == "add"
    assert "id" in data

def test_read_calculations(client, db_session):
    # Create user and calculation
    client.post("/users/register", json={"username": "readuser", "email": "read@example.com", "password": "password123"})
    client.post("/calculations/", json={"a": 10, "b": 5, "type": "subtract"})
    
    response = client.get("/calculations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["result"] == 5

def test_read_calculation_by_id(client, db_session):
    client.post("/users/register", json={"username": "iduser", "email": "id@example.com", "password": "password123"})
    create_res = client.post("/calculations/", json={"a": 10, "b": 2, "type": "multiply"})
    calc_id = create_res.json()["id"]
    
    response = client.get(f"/calculations/{calc_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 20
    assert data["id"] == calc_id

def test_update_calculation(client, db_session):
    client.post("/users/register", json={"username": "updateuser", "email": "update@example.com", "password": "password123"})
    create_res = client.post("/calculations/", json={"a": 10, "b": 2, "type": "divide"})
    calc_id = create_res.json()["id"]
    
    update_data = {"a": 20, "b": 2, "type": "divide"}
    response = client.put(f"/calculations/{calc_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 10.0
    
    # Verify persistence
    get_res = client.get(f"/calculations/{calc_id}")
    assert get_res.json()["result"] == 10.0

def test_delete_calculation(client, db_session):
    client.post("/users/register", json={"username": "deluser", "email": "del@example.com", "password": "password123"})
    create_res = client.post("/calculations/", json={"a": 5, "b": 5, "type": "add"})
    calc_id = create_res.json()["id"]
    
    response = client.delete(f"/calculations/{calc_id}")
    assert response.status_code == 204
    
    # Verify deletion
    get_res = client.get(f"/calculations/{calc_id}")
    assert get_res.status_code == 404

def test_invalid_calculation_type(client, db_session):
    client.post("/users/register", json={"username": "invaliduser", "email": "invalid@example.com", "password": "password123"})
    response = client.post("/calculations/", json={"a": 10, "b": 5, "type": "modulo"})
    assert response.status_code == 400  # Pydantic validation error converted to 400 by exception handler
