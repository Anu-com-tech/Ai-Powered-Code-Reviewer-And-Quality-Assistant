# import ast
# from pathlib import Path


# class PythonParser:
#     """Extract functions, classes, and docstring coverage from Python files."""

#     def parse_file(self, file_path: str):
#         file_path = Path(file_path)

#         try:
#             source = file_path.read_text()
#             tree = ast.parse(source)

#         except SyntaxError:
#             return {
#                 "path": str(file_path),
#                 "error": "SyntaxError",
#                 "functions": [],
#                 "classes": [],
#             }

#         functions = []
#         classes = []

#         for node in ast.walk(tree):

#             # ---------- Functions ----------
#             if isinstance(node, ast.FunctionDef):
#                 functions.append({
#                     "name": node.name,
#                     "lineno": node.lineno,
#                     "args": [a.arg for a in node.args.args],
#                     "has_docstring": ast.get_docstring(node) is not None,
#                 })

#             # ---------- Classes ----------
#             if isinstance(node, ast.ClassDef):
#                 classes.append({
#                     "name": node.name,
#                     "lineno": node.lineno,
#                     "methods": [c.name for c in node.body if isinstance(c, ast.FunctionDef)],
#                     "has_docstring": ast.get_docstring(node) is not None,
#                 })

#         return {
#             "path": str(file_path),
#             "functions": functions,
#             "classes": classes,
#         }


# core/parser/python_parser.py
import os
import ast

def parse_python_files(folder_path: str) -> list:
    result = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=file)
                for node in [n for n in tree.body if isinstance(n, ast.FunctionDef)]:
                    doc = ast.get_docstring(node)
                    result.append({
                        "file": file_path,
                        "name": node.name,
                        "args": [a.arg for a in node.args.args],
                        "docstring": doc or "",
                    })
    return result
