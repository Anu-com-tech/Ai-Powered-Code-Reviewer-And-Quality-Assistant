# import difflib

# def generate_diff(before, after):
#     """
#     Generate a unified diff showing only actual differences between two strings.
#     If no differences, returns a friendly message.
#     """
#     before = before or ""
#     after = after or ""

#     diff = list(difflib.unified_diff(
#         before.splitlines(),
#         after.splitlines(),
#         fromfile='Before',
#         tofile='After',
#         lineterm=''
#     ))

#     if not diff:
#         return "No differences found."  # show this if everything is identical

#     return "\n".join(diff)




# core/utils/diff_utils.py
import difflib

def generate_diff(before, after):
    diff = difflib.unified_diff(
        before.splitlines(),
        after.splitlines(),
        fromfile='Before',
        tofile='After',
        lineterm=''
    )
    return "\n".join(diff)
