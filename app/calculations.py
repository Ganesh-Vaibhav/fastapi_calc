from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas, operations
from .users import get_db, security

router = APIRouter(prefix="/calculations", tags=["calculations"])

@router.get("/", response_model=List[schemas.CalculationRead])
def read_calculations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    calculations = db.query(models.Calculation).offset(skip).limit(limit).all()
    return calculations

@router.get("/{id}", response_model=schemas.CalculationRead)
def read_calculation(id: int, db: Session = Depends(get_db)):
    calculation = db.query(models.Calculation).filter(models.Calculation.id == id).first()
    if calculation is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calculation

@router.post("/", response_model=schemas.CalculationRead, status_code=status.HTTP_201_CREATED)
def create_calculation(calculation_in: schemas.CalculationCreate, db: Session = Depends(get_db)):
    # Perform calculation using operations module
    try:
        if calculation_in.type == "add":
            result = operations.add(calculation_in.a, calculation_in.b)
        elif calculation_in.type == "subtract":
            result = operations.subtract(calculation_in.a, calculation_in.b)
        elif calculation_in.type == "multiply":
            result = operations.multiply(calculation_in.a, calculation_in.b)
        elif calculation_in.type == "divide":
            result = operations.divide(calculation_in.a, calculation_in.b)
        else:
            raise HTTPException(status_code=400, detail="Invalid calculation type")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # For now, assigning a default user_id since we don't have full auth with current user context yet
    # In a real app, we would get the current user from the token.
    # Assuming user with ID 1 exists or we will need to handle this.
    # Requirement says "Integrate these endpoints with your existing models".
    # Since I need a user_id for the foreign key, I will assume a user exists or make it optional in model if allowed,
    # but model says nullable=False.
    # I'll fetch the first user or create a dummy one if needed, but for now let's assume the client passes user_id or we hardcode 1 for simplicity if not authenticated.
    # Wait, the requirement says "Optionally track user sessions/tokens".
    # If I don't implement auth, I can't easily get "current user".
    # I will modify the schema to accept user_id or just hardcode 1 for now and ensure a user exists in tests.
    # Actually, better to just pick the first user in DB to avoid FK error, or require user_id in request?
    # The schema `CalculationCreate` does NOT have user_id.
    # So I must infer it. I'll just use the first user found in DB for this assignment's scope unless I implement full auth.
    
    user = db.query(models.User).first()
    if not user:
        raise HTTPException(status_code=400, detail="No users exist to assign calculation to")

    calculation = models.Calculation(
        a=calculation_in.a,
        b=calculation_in.b,
        type=calculation_in.type,
        result=result,
        user_id=user.id
    )
    db.add(calculation)
    db.commit()
    db.refresh(calculation)
    return calculation

@router.put("/{id}", response_model=schemas.CalculationRead)
def update_calculation(id: int, calculation_in: schemas.CalculationCreate, db: Session = Depends(get_db)):
    calculation = db.query(models.Calculation).filter(models.Calculation.id == id).first()
    if calculation is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    # Recalculate result
    try:
        if calculation_in.type == "add":
            result = operations.add(calculation_in.a, calculation_in.b)
        elif calculation_in.type == "subtract":
            result = operations.subtract(calculation_in.a, calculation_in.b)
        elif calculation_in.type == "multiply":
            result = operations.multiply(calculation_in.a, calculation_in.b)
        elif calculation_in.type == "divide":
            result = operations.divide(calculation_in.a, calculation_in.b)
        else:
            raise HTTPException(status_code=400, detail="Invalid calculation type")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    calculation.a = calculation_in.a
    calculation.b = calculation_in.b
    calculation.type = calculation_in.type
    calculation.result = result
    
    db.commit()
    db.refresh(calculation)
    return calculation

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(id: int, db: Session = Depends(get_db)):
    calculation = db.query(models.Calculation).filter(models.Calculation.id == id).first()
    if calculation is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    db.delete(calculation)
    db.commit()
    return None
