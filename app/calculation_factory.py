# app/calculation_factory.py
from app.models import CalculationType


class CalculationOperation:
    """
    Simple operation wrapper with a uniform compute(a, b) interface.
    The factory returns instances of this class bound to specific logic.
    """

    def __init__(self, func):
        self._func = func

    def compute(self, a: float, b: float) -> float:
        return self._func(a, b)


def _add(a: float, b: float) -> float:
    return a + b


def _subtract(a: float, b: float) -> float:
    return a - b


def _multiply(a: float, b: float) -> float:
    return a * b


def _divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed")
    return a / b


def _power(a: float, b: float) -> float:
    """Calculate a raised to the power of b (a^b)."""
    return a ** b


def _modulus(a: float, b: float) -> float:
    """Calculate the modulus (remainder) of a divided by b."""
    if b == 0:
        raise ZeroDivisionError("Modulus by zero is not allowed")
    return a % b


def _percent_of(a: float, b: float) -> float:
    """Calculate b% of a."""
    return (a * b) / 100


def _nth_root(a: float, b: float) -> float:
    """Calculate the b-th root of a."""
    if b <= 0:
        raise ValueError("Root index (b) must be positive")
    if a < 0 and int(b) == b and int(b) % 2 == 0:
        raise ValueError("Cannot take even root of negative number")
    # For negative a with odd root, use abs and negate result
    if a < 0 and int(b) == b and int(b) % 2 == 1:
        return -(abs(a) ** (1 / b))
    return a ** (1 / b)


def _log_base(a: float, b: float) -> float:
    """Calculate logarithm of a with base b."""
    import math
    if a <= 0:
        raise ValueError("Logarithm argument (a) must be positive")
    if b <= 0:
        raise ValueError("Logarithm base (b) must be positive")
    if b == 1:
        raise ValueError("Logarithm base (b) cannot be 1")
    return math.log(a, b)


class CalculationFactory:
    @staticmethod
    def get_operation(calc_type: CalculationType) -> CalculationOperation:
        """
        Return an operation object whose .compute(a, b) method performs
        the requested calculation. Raises ValueError for unsupported types.
        """
        if calc_type == CalculationType.ADD:
            return CalculationOperation(_add)
        if calc_type == CalculationType.SUBTRACT:
            return CalculationOperation(_subtract)
        if calc_type == CalculationType.MULTIPLY:
            return CalculationOperation(_multiply)
        if calc_type == CalculationType.DIVIDE:
            return CalculationOperation(_divide)
        if calc_type == CalculationType.POWER:
            return CalculationOperation(_power)
        if calc_type == CalculationType.MODULUS:
            return CalculationOperation(_modulus)
        if calc_type == CalculationType.PERCENT_OF:
            return CalculationOperation(_percent_of)
        if calc_type == CalculationType.NTH_ROOT:
            return CalculationOperation(_nth_root)
        if calc_type == CalculationType.LOG_BASE:
            return CalculationOperation(_log_base)

        # This branch is exercised in tests when an invalid type is passed
        raise ValueError(f"Unsupported calculation type: {calc_type}")
