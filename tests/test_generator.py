
# tests/test_generator.py

"""Tests for docstring generator."""

from core.docstring_engine.generator import generate_docstring_from_code
import pytest

def test_generate_docstring_simple_function():
    code = "def add(a, b):\n    return a + b"
    docstring = generate_docstring_from_code(code)
    
    assert docstring.startswith('"""') or docstring.startswith("'")
    assert "add" in docstring

def test_generate_docstring_empty_input():
    docstring = generate_docstring_from_code("")
    assert docstring == ""
