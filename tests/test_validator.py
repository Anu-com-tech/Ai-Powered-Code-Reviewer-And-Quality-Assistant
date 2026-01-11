
# tests/test_validator.py

"""Tests for docstring validator."""

from core.validator.validator import compute_docstring_complexity  # use correct function
import pytest

def test_docstring_complexity_basic():
    code = 'def add(a, b):\n    """Adds two numbers."""\n    return a + b'
    complexity = compute_docstring_complexity(code)
    
    assert isinstance(complexity, int)
    assert complexity >= 0

def test_docstring_complexity_empty():
    code = ""
    complexity = compute_docstring_complexity(code)
    assert complexity == 0
