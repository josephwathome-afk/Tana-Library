import pytest
from calculator import add, subtract, multiply, divide

class TestAdd:
    def test_add_two_positive_numbers(self):
        assert add(2, 3) == 5

    def test_add_positive_and_negative(self):
        assert add(10, -4) == 6

    def test_add_two_negatives(self):
        assert add(-1, -1) == -2

    def test_add_with_zero(self):
        assert add(0, 7) == 7

    def test_add_floats(self):
        assert add(0.1, 0.2) == pytest.approx(0.3)

class TestSubtract:
    def test_subtract_basic(self):
        assert subtract(10, 4) == 6

    def test_subtract_gives_negative(self):
        assert subtract(3, 8) == -5

    def test_subtract_same_numbers(self):
        assert subtract(5, 5) == 0

    def test_subtract_negative(self):
        assert subtract(-2, -5) == 3

    def test_subtract_floats(self):
        assert subtract(1.5, 0.5) == pytest.approx(1.0)


class TestMultiply:
    def test_multiply_two_positives(self):
        assert multiply(3, 4) == 12

    def test_multiply_by_zero(self):
        assert multiply(99, 0) == 0

    def test_multiply_negatives(self):
        assert multiply(-3, -4) == 12

    def test_multiply_mixed_signs(self):
        assert multiply(5, -2) == -10

    def test_multiply_floats(self):
        assert multiply(2.5, 4.0) == pytest.approx(10.0)

class TestDivide:
    def test_divide_basic(self):
        assert divide(10, 2) == 5.0

    def test_divide_returns_float(self):
        assert isinstance(divide(7, 2), float)

    def test_divide_negative_dividend(self):
        assert divide(-9, 3) == -3.0

    def test_divide_negative_divisor(self):
        assert divide(9, -3) == -3.0

    def test_divide_floats(self):
        assert divide(7.5, 2.5) == pytest.approx(3.0)

    def test_divide_by_zero_raises(self):
        """Division by zero must raise ValueError, not ZeroDivisionError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_divide_zero_by_number(self):
        assert divide(0, 5) == 0.0