def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b


def power(a: float, b: float) -> float:
    """Calculate a raised to the power of b (a^b)."""
    return a ** b


def modulus(a: float, b: float) -> float:
    """Calculate the modulus (remainder) of a divided by b."""
    if b == 0:
        raise ValueError("Modulus by zero is not allowed")
    return a % b


def percent_of(a: float, b: float) -> float:
    """Calculate b% of a (what is b percent of a)."""
    return (a * b) / 100


def nth_root(a: float, b: float) -> float:
    """Calculate the b-th root of a."""
    if b <= 0:
        raise ValueError("Root index (b) must be positive")
    if a < 0 and int(b) == b and int(b) % 2 == 0:
        raise ValueError("Cannot take even root of negative number")
    # For negative a with odd root, use abs and negate result
    if a < 0 and int(b) == b and int(b) % 2 == 1:
        return -(abs(a) ** (1 / b))
    return a ** (1 / b)


def log_base(a: float, b: float) -> float:
    """Calculate logarithm of a with base b."""
    import math
    if a <= 0:
        raise ValueError("Logarithm argument (a) must be positive")
    if b <= 0:
        raise ValueError("Logarithm base (b) must be positive")
    if b == 1:
        raise ValueError("Logarithm base (b) cannot be 1")
    return math.log(a, b)
