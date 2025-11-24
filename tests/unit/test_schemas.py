import pytest
from pydantic import ValidationError
from app.schemas import CalculationCreate

def test_calculation_create_valid():
    calc = CalculationCreate(a=10, b=5, type="add")
    assert calc.a == 10
    assert calc.b == 5
    assert calc.type == "add"

def test_calculation_create_invalid_type():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=5, type="invalid")

def test_calculation_create_missing_field():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, type="add")
