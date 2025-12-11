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
        (CalculationType.POWER, 2, 3, 8),
        (CalculationType.MODULUS, 10, 3, 1),
        (CalculationType.PERCENT_OF, 15, 200, 30.0),
        (CalculationType.NTH_ROOT, 16, 4, 2.0),
        (CalculationType.LOG_BASE, 8, 2, 3.0),
    ],
)
def test_factory_returns_correct_result(calc_type, a, b, expected):
    op = CalculationFactory.get_operation(calc_type)
    result = op.compute(a, b)
    # Use approximate equality for floating point
    if isinstance(expected, float):
        assert abs(result - expected) < 1e-10
    else:
        assert result == expected


def test_factory_invalid_type_raises_value_error():
    with pytest.raises(ValueError):
        # type: ignore[arg-type] used to intentionally pass a bad value
        CalculationFactory.get_operation("invalid_type")  # invalid type


def test_divide_operation_zero_division():
    op = CalculationFactory.get_operation(CalculationType.DIVIDE)
    with pytest.raises(ZeroDivisionError):
        op.compute(1, 0)


def test_modulus_operation_zero_division():
    op = CalculationFactory.get_operation(CalculationType.MODULUS)
    with pytest.raises(ZeroDivisionError):
        op.compute(10, 0)


def test_nth_root_validation():
    op = CalculationFactory.get_operation(CalculationType.NTH_ROOT)
    
    # Test negative root index
    with pytest.raises(ValueError, match="Root index"):
        op.compute(16, -2)
    
    # Test even root of negative number
    with pytest.raises(ValueError, match="even root of negative"):
        op.compute(-16, 2)


def test_log_base_validation():
    op = CalculationFactory.get_operation(CalculationType.LOG_BASE)
    
    # Test negative argument
    with pytest.raises(ValueError, match="Logarithm argument"):
        op.compute(-8, 2)
    
    # Test negative base
    with pytest.raises(ValueError, match="Logarithm base"):
        op.compute(8, -2)
    
    # Test base = 1
    with pytest.raises(ValueError, match="cannot be 1"):
        op.compute(8, 1)

