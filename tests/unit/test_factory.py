import pytest
from app.factory import CalculationFactory

def test_factory_add():
    result = CalculationFactory.create_calculation(2, 3, "add")
    assert result == 5

def test_factory_subtract():
    result = CalculationFactory.create_calculation(5, 3, "subtract")
    assert result == 2

def test_factory_multiply():
    result = CalculationFactory.create_calculation(2, 3, "multiply")
    assert result == 6

def test_factory_divide():
    result = CalculationFactory.create_calculation(6, 3, "divide")
    assert result == 2.0

def test_factory_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        CalculationFactory.create_calculation(5, 0, "divide")

def test_factory_invalid_operation():
    with pytest.raises(ValueError, match="Invalid operation type"):
        CalculationFactory.create_calculation(2, 3, "unknown")
