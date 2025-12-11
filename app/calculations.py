from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models import Calculation, User
from app.schemas import CalculationCreate, CalculationRead
from app.calculation_factory import CalculationFactory
from fastapi import Depends
from app.security import decode_access_token
from sqlalchemy.orm import Session
from fastapi import Header
from app.db import SessionLocal


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    """Simple bearer token parsing to load the current user.

    Expects header: `Authorization: Bearer <token>`
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    parts = authorization.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = parts[1]
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

router = APIRouter()


@router.get("/calculations", response_model=List[CalculationRead])
def browse_calculations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(Calculation).filter(Calculation.user_id == current_user.id).all()
    return items


@router.post("/calculations", response_model=CalculationRead)
def add_calculation(payload: CalculationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Compute result using factory
    operation = CalculationFactory.get_operation(payload.type)
    try:
        result = operation.compute(payload.a, payload.b)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    db_calc = Calculation(a=payload.a, b=payload.b, type=payload.type, result=result, user_id=current_user.id)
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc


@router.get("/calculations/{calc_id}", response_model=CalculationRead)
def read_calculation(calc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    if calc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return calc


@router.put("/calculations/{calc_id}", response_model=CalculationRead)
def update_calculation(calc_id: int, payload: CalculationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    if calc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    calc.a = payload.a
    calc.b = payload.b
    calc.type = payload.type
    # Recompute
    operation = CalculationFactory.get_operation(payload.type)
    try:
        calc.result = operation.compute(payload.a, payload.b)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


@router.delete("/calculations/{calc_id}")
def delete_calculation(calc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    if calc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(calc)
    db.commit()
    return {"detail": "Deleted"}
