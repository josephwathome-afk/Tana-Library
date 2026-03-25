"""
TDD Phase 2 — GREEN: Minimal implementation to make all tests pass.
"""

import requests


def fetch_value(url: str) -> float:
    """Fetch a single numeric value from an external API endpoint.

    In production this hits a real URL; in tests it is mocked so no
    network call is ever made.

    Raises:
        ValueError: If the response body cannot be parsed as a float.
    """
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    try:
        return float(response.json()["value"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid API response from {url}: {response.text}") from exc


def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of a minus b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return a divided by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return float(a / b)


import requests


def fetch_value(url: str) -> float:
    """Fetch a numeric value from an API endpoint.

    The API must return JSON with a 'value' key containing a number.

    Args:
        url: The API endpoint URL.

    Returns:
        The value as a float.

    Raises:
        ValueError: If the response is invalid or missing 'value'.
    """
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if 'value' not in data:
        raise ValueError("Invalid API response")
    return float(data['value'])