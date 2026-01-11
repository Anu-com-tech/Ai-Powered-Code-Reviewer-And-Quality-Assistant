from dashboard_ui.dashboard import Dashboard
import pytest

def test_dashboard_data_structure():
    sample_data = [
        {"file": "file1.py", "functions": [{"name": "func1", "documented": True}]},
        {"file": "file2.py", "functions": [{"name": "func2", "documented": False}]},
    ]
    
    dash = Dashboard()
    dashboard_data = dash.prepare_dashboard_data(sample_data)  # use actual method

    # Assertions
    assert "files" in dashboard_data
    assert "summary" in dashboard_data

def test_empty_dashboard_data():
    dash = Dashboard()
    dashboard_data = dash.prepare_dashboard_data([])

    assert dashboard_data["files"] == []
    assert dashboard_data["summary"]["total_functions"] == 0
