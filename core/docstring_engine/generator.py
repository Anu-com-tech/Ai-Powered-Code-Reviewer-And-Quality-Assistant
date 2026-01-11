# core/docstring_engine/generator.py
#from typing import Dict, List, Optional

#def generate_function_docstring(func: Dict) -> str:
 #   """
  #  Generate a simple Google-style docstring for a function dict:
   # func keys: name, args (list), returns (optional)
    #"""
    #ame = func.get("name", "function")
    #args: List[str] = func.get("args", []) or []
    #returns: Optional[str] = func.get("returns")

    #lines = [f'"""{name.replace("_", " ").capitalize()}.', ""]

    # if args:
    #     lines.append("Args:")
    #     for a in args:
    #         lines.append(f"    {a} (TYPE): Description.")
    #     lines.append("")

    # if returns:
    #     lines.append("Returns:")
    #     lines.append(f"    {returns}: Description.")
    #     lines.append("")

    # lines.append('"""')
    # return "\n".join(lines)








# class DocstringGenerator:
#     def generate(self, func):
#         return f'''def {func["name"]}(...):
#     """
#     Auto-generated docstring
#     Args: {func["args"]}
#     Returns: {func["returns"]}
#     """
# '''


# core/docstring_engine/generator.py

# def run_generator_for_code(code_snippet: str):
#     """
#     Generate docstring for a single function code snippet.
#     Returns a dict similar to the output of 'python -m core.docstring_engine.generator'.
#     """
#     # If your existing generator code can handle a single snippet, use it here.
#     # For demonstration, we’ll mock it using your working generator format.

#     # Example: call your existing generator function internally
#     # Replace this with actual generator logic
#     generated_doc = f'"""Generated docstring for function:\n\n{code_snippet[:50]}...\n"""'

#     return {
#         "total": 1,
#         "generated_docs": [generated_doc],
#         "previews": [generated_doc],
#         "error": None
#     }


# core/docstring_engine/generator.py

# core/docstring_engine/generator.py

# core/docstring_engine/generator.py

# core/docstring_engine/generator.py

# core/docstring_engine/generator.py

# core/docstring_engine/generator.py

from core.docstring_engine.llm_integration import call_llm
import ast


# ---------------- DocstringGenerator Class ----------------
class DocstringGenerator:
    def __init__(self, style: str = "Google"):
        self.style = style

    def generate(self, function_meta: dict) -> str:
        """
        Generate a docstring using LLM without predefined templates.
        """
        fn_name = function_meta.get("name", "function")

        prompt = f"""
You are an expert Python developer.

Write a clear Python docstring describing the purpose of the function below.

Function name:
{fn_name}

Source code:
{function_meta.get("code")}

The docstring MUST mention the function name.
"""

        llm_response = call_llm(prompt).strip()

        # IMPORTANT: ensure function name is inside docstring
        return f'"""{fn_name}: {llm_response}"""'


# ---------------- Helper Function ----------------
def generate_docstring_from_code(code: str) -> str:
    """Generate docstring for a given function code string."""
    if not code.strip():
        return ""

    try:
        tree = ast.parse(code)
        fn_node = next(
            n for n in tree.body if isinstance(n, ast.FunctionDef)
        )
        function_meta = {
            "name": fn_node.name,
            "code": code
        }
    except Exception:
        function_meta = {
            "name": "function",
            "code": code
        }

    generator = DocstringGenerator()
    return generator.generate(function_meta)
