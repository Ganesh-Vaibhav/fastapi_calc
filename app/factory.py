from typing import Union
from .operations import add, subtract, multiply, divide

class CalculationFactory:
    @staticmethod
    def create_calculation(a: Union[int, float], b: Union[int, float], operation_type: str) -> float:
        """
        Perform calculation based on the operation type.
        
        Args:
            a (int | float): First number
            b (int | float): Second number
            operation_type (str): Type of operation ('add', 'subtract', 'multiply', 'divide')
            
        Returns:
            float: Result of the calculation
            
        Raises:
            ValueError: If operation type is invalid or division by zero occurs
        """
        if operation_type == "add":
            return add(a, b)
        elif operation_type == "subtract":
            return subtract(a, b)
        elif operation_type == "multiply":
            return multiply(a, b)
        elif operation_type == "divide":
            return divide(a, b)
        else:
            raise ValueError(f"Invalid operation type: {operation_type}")
