import pytest
from calculator import add, subtract, multiply, divide

# Required user cases

def test_add_two_positive_numbers():
    assert add(2, 3) == 5


def test_subtract_larger_from_smaller():
    assert subtract(3, 8) == -5


def test_multiply_by_zero():
    assert multiply(123, 0) == 0


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


def test_add_floats_precision():
    assert add(0.1, 0.2) == pytest.approx(0.3)
