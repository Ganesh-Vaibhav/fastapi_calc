import pytest
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine, Base
from app.models import User, Calculation
from app.factory import CalculationFactory

# Create tables for testing
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.close()

def test_create_calculation(db_session: Session):
    # Create a user first
    user = User(username="testcalcuser", email="testcalc@example.com", password_hash="hashedsecret")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create a calculation
    a = 10.0
    b = 5.0
    op_type = "add"
    result = CalculationFactory.create_calculation(a, b, op_type)
    
    calculation = Calculation(
        a=a,
        b=b,
        type=op_type,
        result=result,
        user_id=user.id
    )
    db_session.add(calculation)
    db_session.commit()
    db_session.refresh(calculation)

    # Verify
    assert calculation.id is not None
    assert calculation.a == 10.0
    assert calculation.b == 5.0
    assert calculation.type == "add"
    assert calculation.result == 15.0
    assert calculation.user_id == user.id

    # Cleanup
    db_session.delete(calculation)
    db_session.delete(user)
    db_session.commit()
