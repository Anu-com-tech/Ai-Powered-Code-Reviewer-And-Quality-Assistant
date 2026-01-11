# tests/test_parser.py

"""Tests for Python parser."""

from core.parser.python_parser import parse_python_files


def test_parse_python_files_returns_list():
    functions = parse_python_files("examples")
    assert isinstance(functions, list)
    if functions:
        f = functions[0]
        assert "name" in f
        assert "file" in f
        assert "docstring" in f


def test_empty_directory_returns_empty_list(tmp_path):
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    functions = parse_python_files(str(empty_dir))
    assert functions == []
