import pytest
from app.operations import add, subtract, multiply, divide, power, modulus, percent_of, nth_root, log_base


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract():
    assert subtract(5, 2) == 3
    assert subtract(0, 5) == -5


def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6


def test_divide_normal():
    assert divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(4, 0)


def test_power():
    assert power(2, 3) == 8
    assert power(5, 2) == 25
    assert power(10, 0) == 1
    assert power(2, -1) == 0.5


def test_modulus_normal():
    assert modulus(10, 3) == 1
    assert modulus(17, 5) == 2
    assert modulus(8, 4) == 0


def test_modulus_by_zero():
    with pytest.raises(ValueError):
        modulus(10, 0)


def test_percent_of():
    assert percent_of(15, 200) == 30.0  # 15% of 200 = 30
    assert percent_of(50, 100) == 50.0  # 50% of 100 = 50
    assert percent_of(10, 50) == 5.0    # 10% of 50 = 5


def test_nth_root_normal():
    assert nth_root(16, 4) == 2.0       # 4th root of 16 = 2
    assert nth_root(27, 3) == 3.0       # cube root of 27 = 3
    assert nth_root(100, 2) == 10.0     # square root of 100 = 10


def test_nth_root_negative_index():
    with pytest.raises(ValueError, match="Root index .* must be positive"):
        nth_root(16, 0)
    with pytest.raises(ValueError, match="Root index .* must be positive"):
        nth_root(16, -2)


def test_nth_root_even_root_of_negative():
    with pytest.raises(ValueError, match="Cannot take even root of negative number"):
        nth_root(-16, 2)
    with pytest.raises(ValueError, match="Cannot take even root of negative number"):
        nth_root(-81, 4)


def test_nth_root_odd_root_of_negative():
    # Odd roots of negative numbers are allowed
    result = nth_root(-8, 3)
    assert abs(result - (-2)) < 1e-10  # cube root of -8 = -2


def test_log_base_normal():
    assert abs(log_base(8, 2) - 3.0) < 1e-10       # log_2(8) = 3
    assert abs(log_base(1000, 10) - 3.0) < 1e-10   # log_10(1000) = 3
    assert abs(log_base(1, 10) - 0.0) < 1e-10      # log_10(1) = 0


def test_log_base_invalid_argument():
    with pytest.raises(ValueError, match="Logarithm argument .* must be positive"):
        log_base(0, 2)
    with pytest.raises(ValueError, match="Logarithm argument .* must be positive"):
        log_base(-5, 2)


def test_log_base_invalid_base():
    with pytest.raises(ValueError, match="Logarithm base .* must be positive"):
        log_base(8, 0)
    with pytest.raises(ValueError, match="Logarithm base .* must be positive"):
        log_base(8, -2)
    with pytest.raises(ValueError, match="Logarithm base .* cannot be 1"):
        log_base(8, 1)

