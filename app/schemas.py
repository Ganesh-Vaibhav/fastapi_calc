from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    password: str = Field(..., min_length=8)


class CalculationCreate(BaseModel):
    a: float
    b: float
    type: str = Field(..., pattern="^(add|subtract|multiply|divide)$")


class CalculationRead(CalculationCreate):
    id: int
    result: float
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
