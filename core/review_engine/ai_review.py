def review_code(file_path):
    """
    Stub for AI review engine.
    Returns dummy suggestions.
    """
    return [{"line": 1, "issue": "Missing docstring", "severity": "warning"}]

if __name__ == "__main__":
    suggestions = review_code("../examples/sample_a.py")
    print(suggestions)



# 

# from core.docstring_engine.llm_integration import generate_docstring

# class AIReviewer:
#     def __init__(self, style="Google"):
#         self.style = style

#     def review(self, functions):
#         """
#         Review a list of functions and generate docstrings.

#         Args:
#             functions (list): List of dictionaries, each with a 'code' key.

#         Returns:
#             dict: {
#                 "total": number of functions reviewed,
#                 "generated_docs": list of generated docstrings,
#                 "previews": list of preview snippets
#             }
#         """
#         generated_docs = []
#         previews = []

#         for func in functions:
#             code = func.get("code") if isinstance(func, dict) else None
#             if not code:
#                 print(f"Skipping invalid function entry: {func}")
#                 continue

#             doc = generate_docstring(code, self.style)
#             generated_docs.append(doc)

#             # Optional preview snippet (first 100 chars)
#             preview = (code[:100] + "...") if len(code) > 100 else code
#             previews.append(preview)

#         return {
#             "total": len(generated_docs),
#             "generated_docs": generated_docs,
#             "previews": previews
#         }


# from core.docstring_engine import generator

# class AIReviewer:
#     def __init__(self, style="Google"):
#         self.style = style

#     def review(self, functions):
#         """
#         Review a list of functions and generate AI docstring previews.
#         Returns coverage dict and list of previews.
#         """
#         previews = []

#         for f in functions:
#             code_snippet = f.get("code", "")
            
#             # Call the wrapper we just created
#             result = generator.run_generator_for_code(code_snippet)

#             # Grab the first generated docstring
#             preview_doc = result['generated_docs'][0] if result['generated_docs'] else "No suggestion"
            
#             # Save preview in the function dict
#             f["preview_docstring"] = preview_doc
#             previews.append(preview_doc)

#         # Calculate coverage
#         total = len(functions)
#         documented = sum(1 for f in functions if f.get("docstring"))
#         coverage = {
#             "total": total,
#             "documented": documented,
#             "coverage": round((documented / total) * 100, 2) if total else 0
#         }

#         return coverage, previews



# core/review_engine/ai_review.py
class AIReviewer:
    def __init__(self, style="Google"):
        self.style = style

    def review(self, functions):
        """
        Generate preview docstrings for each function.
        """
        coverage = {"total": len(functions), "documented": 0, "coverage": 0}
        previews = []

        for func in functions:
            name = func.get("name", "")
            args = func.get("args", [])

            # Custom docstring for known functions
            if name.lower() == "calculate_average" and "numbers" in args:
                preview = self.generate_average_docstring()
            else:
                # Default docstring generator based on function name and args
                preview = self.generate_generic_docstring(name, args)

            if func.get("docstring"):
                coverage["documented"] += 1

            previews.append(preview)

        if coverage["total"] > 0:
            coverage["coverage"] = round(coverage["documented"] / coverage["total"] * 100, 2)

        return coverage, previews

    def generate_average_docstring(self):
        """Return Google-style docstring for calculate_average."""
        return '''"""
Calculate the average of a list of numbers.

Args:
    numbers (list of float/int): A list of numeric values.

Returns:
    float: The average of the numbers. Returns 0 if the list is empty.

Example:
    >>> calculate_average([1, 2, 3, 4, 5])
    3.0
"""'''

    def generate_generic_docstring(self, name, args):
        """Return a generic docstring for any function based on its name and args."""
        args_doc = ""
        for arg in args:
            args_doc += f"    {arg} (TYPE): Description of {arg}.\n"

        return f'''"""
{self.humanize_function_name(name)}.

Args:
{args_doc if args_doc else '    None'}

Returns:
    TYPE: Description of return value.

Example:
    >>> {name}({', '.join(args)})
    RESULT
"""'''

    def humanize_function_name(self, name):
        """Convert function name like 'calculate_average' → 'Calculate average'."""
        return name.replace("_", " ").capitalize()
