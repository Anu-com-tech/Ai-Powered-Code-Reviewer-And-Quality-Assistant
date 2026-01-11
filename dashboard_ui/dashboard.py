# dashboard_ui/dashboard.py

class Dashboard:
    def __init__(self):
        pass

    def prepare_dashboard_data(self, files_data: list) -> dict:
        """
        Prepares the data structure for the dashboard.

        Args:
            files_data (list): List of dictionaries containing file info and functions.

        Returns:
            dict: Contains files data and summary of total/documented functions.
        """
        total_functions = sum(len(f.get("functions", [])) for f in files_data)
        documented_functions = sum(
            1 for f in files_data for fn in f.get("functions", []) if fn.get("documented")
        )

        return {
            "files": files_data,
            "summary": {
                "total_functions": total_functions,
                "documented_functions": documented_functions
            }
        }






