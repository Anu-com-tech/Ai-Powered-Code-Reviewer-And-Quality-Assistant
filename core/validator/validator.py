# core/validator/validator.py
import subprocess

class DocstringValidator:
    """
    Validates Python docstrings using pydocstyle.
    """

    def run_pydocstyle(self, file_path: str) -> list:
        """
        Runs pydocstyle on a Python file and returns a list of issues.
        If pydocstyle is not installed, returns a warning message.
        """
        try:
            result = subprocess.run(
                ["pydocstyle", file_path],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return []
            return result.stdout.strip().split("\n")
        except FileNotFoundError:
            return ["pydocstyle not installed"]


def compute_docstring_complexity(function_code: str) -> int:
    """
    Computes a simple 'complexity' score of a function's docstring.
    Currently, it's just the number of lines in the docstring.
    """
    if not function_code:
        return 0
    return len(function_code.strip().splitlines())

