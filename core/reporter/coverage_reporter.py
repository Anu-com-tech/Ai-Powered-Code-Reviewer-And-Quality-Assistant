# import json
# from pathlib import Path


# class CoverageReporter:

#     def generate_report(self, parsed_files, output_path="storage/review_logs.json"):
#         total_files = len(parsed_files)
#         total_funcs = 0
#         total_doc_funcs = 0

#         for f in parsed_files:
#             funcs = f.get("functions", [])
#             total_funcs += len(funcs)
#             total_doc_funcs += sum(1 for fn in funcs if fn.get("has_docstring"))

#         coverage = int((total_doc_funcs / total_funcs) * 100) if total_funcs else 100

#         report = {
#             "files": parsed_files,
#             "metrics": {
#                 "files_scanned": total_files,
#                 "functions_total": total_funcs,
#                 "functions_documented": total_doc_funcs,
#                 "coverage_percent": coverage,
#                 "parser_accuracy_percent": 95,
#             },
#         }

#         Path(output_path).parent.mkdir(parents=True, exist_ok=True)
#         Path(output_path).write_text(json.dumps(report, indent=4))

#         return report




class CoverageReporter:
    def calculate(self, total, documented):
        return {
            "total": total,
            "documented": documented,
            "coverage": int((documented / total) * 100)
        }
