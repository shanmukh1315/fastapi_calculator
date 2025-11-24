# tests/unit/test_calculation_factory.py
import pytest

from app.models import CalculationType
from app.calculation_factory import CalculationFactory


@pytest.mark.parametrize(
    "calc_type,a,b,expected",
    [
        (CalculationType.ADD, 1, 2, 3),
        (CalculationType.SUBTRACT, 5, 2, 3),
        (CalculationType.MULTIPLY, 3, 4, 12),
        (CalculationType.DIVIDE, 10, 2, 5),
    ],
)
def test_factory_returns_correct_result(calc_type, a, b, expected):
    op = CalculationFactory.get_operation(calc_type)
    assert op.compute(a, b) == expected


def test_factory_invalid_type_raises_value_error():
    with pytest.raises(ValueError):
        # type: ignore[arg-type] used to intentionally pass a bad value
        CalculationFactory.get_operation("power")  # invalid type


def test_divide_operation_zero_division():
    op = CalculationFactory.get_operation(CalculationType.DIVIDE)
    with pytest.raises(ZeroDivisionError):
        op.compute(1, 0)
