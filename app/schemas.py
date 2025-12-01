# app/schemas.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator

from app.models import CalculationType


# ---------- User Schemas ----------

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# ---------- Calculation Schemas ----------

class CalculationBase(BaseModel):
    a: float
    type: CalculationType   # NOTE: type is before b so validator can see it
    b: float

    @validator("b")
    def prevent_division_by_zero(cls, v, values):
        calc_type = values.get("type")
        if calc_type == CalculationType.DIVIDE and v == 0:
            raise ValueError("Division by zero is not allowed")
        return v


class CalculationCreate(CalculationBase):
    """
    Incoming data when creating a calculation.
    """
    pass


class CalculationRead(CalculationBase):
    id: int
    result: float
    user_id: Optional[int] = None

    class Config:
        orm_mode = True


# ---------- Auth Schemas ----------
class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
