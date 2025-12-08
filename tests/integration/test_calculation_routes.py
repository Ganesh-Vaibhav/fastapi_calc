import pytest
from app import models

def test_create_calculation(authorized_client, db_session):
    # Create calculation
    calc_data = {"a": 10, "b": 5, "type": "add"}
    response = authorized_client.post("/calculations/", json=calc_data)
    assert response.status_code == 201
    data = response.json()
    assert data["result"] == 15
    assert data["type"] == "add"
    assert "id" in data

def test_read_calculations(authorized_client, db_session):
    # Create calculation
    authorized_client.post("/calculations/", json={"a": 10, "b": 5, "type": "subtract"})
    
    response = authorized_client.get("/calculations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["result"] == 5

def test_read_calculation_by_id(authorized_client, db_session):
    create_res = authorized_client.post("/calculations/", json={"a": 10, "b": 2, "type": "multiply"})
    calc_id = create_res.json()["id"]
    
    response = authorized_client.get(f"/calculations/{calc_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 20
    assert data["id"] == calc_id

def test_update_calculation(authorized_client, db_session):
    create_res = authorized_client.post("/calculations/", json={"a": 10, "b": 2, "type": "divide"})
    calc_id = create_res.json()["id"]
    
    update_data = {"a": 20, "b": 2, "type": "divide"}
    response = authorized_client.put(f"/calculations/{calc_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 10.0
    
    # Verify persistence
    get_res = authorized_client.get(f"/calculations/{calc_id}")
    assert get_res.json()["result"] == 10.0

def test_delete_calculation(authorized_client, db_session):
    create_res = authorized_client.post("/calculations/", json={"a": 5, "b": 5, "type": "add"})
    calc_id = create_res.json()["id"]
    
    response = authorized_client.delete(f"/calculations/{calc_id}")
    assert response.status_code == 204
    
    # Verify deletion
    get_res = authorized_client.get(f"/calculations/{calc_id}")
    assert get_res.status_code == 404

def test_invalid_calculation_type(authorized_client, db_session):
    response = authorized_client.post("/calculations/", json={"a": 10, "b": 5, "type": "modulo"})
    assert response.status_code == 400  # Pydantic validation error converted to 400 by exception handler
