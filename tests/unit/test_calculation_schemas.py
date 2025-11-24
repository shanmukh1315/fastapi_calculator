# tests/unit/test_calculation_schemas.py
import pytest
from pydantic import ValidationError

from app.schemas import CalculationCreate
from app.models import CalculationType


def test_calculation_create_valid_add():
    calc = CalculationCreate(a=2.0, b=3.0, type=CalculationType.ADD)
    assert calc.a == 2.0
    assert calc.b == 3.0
    assert calc.type == CalculationType.ADD


def test_calculation_create_divide_by_zero_rejected():
    with pytest.raises(ValidationError):
        CalculationCreate(a=1.0, b=0.0, type=CalculationType.DIVIDE)
