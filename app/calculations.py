from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas, operations
from .users import get_db, security

router = APIRouter(prefix="/calculations", tags=["calculations"])

@router.get("/", response_model=List[schemas.CalculationRead])
def read_calculations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    calculations = db.query(models.Calculation).filter(models.Calculation.user_id == current_user.id).offset(skip).limit(limit).all()
    return calculations

@router.get("/{id}", response_model=schemas.CalculationRead)
def read_calculation(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    calculation = db.query(models.Calculation).filter(models.Calculation.id == id, models.Calculation.user_id == current_user.id).first()
    if calculation is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calculation

@router.post("/", response_model=schemas.CalculationRead, status_code=status.HTTP_201_CREATED)
def create_calculation(calculation_in: schemas.CalculationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
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

    calculation = models.Calculation(
        a=calculation_in.a,
        b=calculation_in.b,
        type=calculation_in.type,
        result=result,
        user_id=current_user.id
    )
    db.add(calculation)
    db.commit()
    db.refresh(calculation)
    return calculation

@router.put("/{id}", response_model=schemas.CalculationRead)
def update_calculation(id: int, calculation_in: schemas.CalculationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    calculation = db.query(models.Calculation).filter(models.Calculation.id == id, models.Calculation.user_id == current_user.id).first()
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
def delete_calculation(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    calculation = db.query(models.Calculation).filter(models.Calculation.id == id, models.Calculation.user_id == current_user.id).first()
    if calculation is None:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    db.delete(calculation)
    db.commit()
    return None
