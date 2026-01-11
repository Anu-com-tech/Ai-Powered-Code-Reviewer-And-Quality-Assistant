import subprocess
from pathlib import Path
import sys  # add this

def run_pylint(path: str):
    path = Path(path)

    if not path.exists():
        return ["Path does not exist"]

    result = subprocess.run(
        [
            sys.executable, "-m", "pylint", str(path), 
            "--disable=all",
            "--enable=missing-module-docstring,missing-function-docstring,missing-class-docstring"
        ],
        capture_output=True,
        text=True
    )

    issues = []
    for line in result.stdout.splitlines():
        if ":" in line:
            issues.append(line)

    return issues

