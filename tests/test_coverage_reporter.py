# tests/test_coverage_reporter.py

from core.reporter.coverage_reporter import CoverageReporter
from core.parser.python_parser import parse_python_files  # or whatever parser you have

def test_coverage_calculation():
    reporter = CoverageReporter()
    
    # Example data
    total_functions = 10
    documented_functions = 8
    
    report = reporter.calculate(total_functions, documented_functions)
    
    assert "total" in report
    assert "documented" in report
    assert "coverage" in report
    assert report["coverage"] == 80  # 8/10*100

