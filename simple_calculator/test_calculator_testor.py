import pytest
from unittest.mock import patch, MagicMock
from calculator import add, subtract, multiply, divide, fetch_value


# ── add ──────────────────────────────────────────────────────────────────────

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


# ── subtract ─────────────────────────────────────────────────────────────────

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


# ── multiply ─────────────────────────────────────────────────────────────────

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


# ── divide ───────────────────────────────────────────────────────────────────

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


# ── mocking fetch_value ───────────────────────────────────────────────────────

API_URL = "https://api.example.com/value"

class TestFetchValue:
    """Tests for fetch_value() — no real network calls are ever made."""

    def _mock_response(self, value):
        """Build a fake requests.Response whose .json() returns {'value': value}."""
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {"value": value}
        return mock_resp

    @patch("calculator.requests.get")
    def test_fetch_returns_float(self, mock_get):
        mock_get.return_value = self._mock_response(42)
        assert fetch_value(API_URL) == 42.0

    @patch("calculator.requests.get")
    def test_fetch_value_used_in_add(self, mock_get):
        """Simulate fetching two operands from an API and adding them."""
        mock_get.side_effect = [
            self._mock_response(7),
            self._mock_response(3),
        ]
        a = fetch_value(API_URL)
        b = fetch_value(API_URL)
        assert add(a, b) == 10.0

    @patch("calculator.requests.get")
    def test_fetch_value_used_in_divide(self, mock_get):
        mock_get.return_value = self._mock_response(0)
        operand = fetch_value(API_URL)
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, operand)

    @patch("calculator.requests.get")
    def test_fetch_raises_on_bad_payload(self, mock_get):
        """API response that is missing the 'value' key must raise ValueError."""
        bad_resp = MagicMock()
        bad_resp.raise_for_status.return_value = None
        bad_resp.json.return_value = {"result": 99}   # wrong key
        bad_resp.text = '{"result": 99}'
        mock_get.return_value = bad_resp
        with pytest.raises(ValueError, match="Invalid API response"):
            fetch_value(API_URL)

    @patch("calculator.requests.get")
    def test_network_is_never_called_for_pure_functions(self, mock_get):
        """Sanity check: pure math functions don't touch the network at all."""
        add(1, 2)
        subtract(5, 3)
        multiply(4, 4)
        divide(9, 3)
        mock_get.assert_not_called()