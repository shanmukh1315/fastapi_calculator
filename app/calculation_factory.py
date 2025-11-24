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

        # This branch is exercised in tests when an invalid type is passed
        raise ValueError(f"Unsupported calculation type: {calc_type}")
