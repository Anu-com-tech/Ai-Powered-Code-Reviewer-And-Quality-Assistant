# import streamlit as st
# from pathlib import Path
# import json

# from core.parser.python_parser import PythonParser
# from core.reporter.coverage_reporter import CoverageReporter

# st.set_page_config(page_title="Milestone 1 – Parser", layout="wide")

# parser = PythonParser()
# reporter = CoverageReporter()
# REPORT_PATH = Path("storage/review_logs.json")


# # ---------------------------------------------------------------------
# # SESSION STATE
# # ---------------------------------------------------------------------
# if "tree_output" not in st.session_state:
#     st.session_state.tree_output = ""

# if "parsed_files" not in st.session_state:
#     st.session_state.parsed_files = []

# if "report_ready" not in st.session_state:
#     st.session_state.report_ready = False


# # ---------------------------------------------------------------------
# # FOLDER TREE GENERATOR
# # ---------------------------------------------------------------------
# def folder_tree(path: Path, prefix: str = ""):
#     tree_str = f"{prefix}{path.name}/\n"
#     entries = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))

#     for idx, entry in enumerate(entries):
#         connector = "├── " if idx < len(entries) - 1 else "└── "
#         new_prefix = prefix + ("│   " if idx < len(entries) - 1 else "    ")

#         if entry.is_dir():
#             tree_str += f"{prefix}{connector}{entry.name}/\n"
#             tree_str += folder_tree(entry, new_prefix)
#         else:
#             tree_str += f"{prefix}{connector}{entry.name}\n"

#     return tree_str


# # ---------------------------------------------------------------------
# # UI INPUT
# # ---------------------------------------------------------------------
# st.title("📁 Milestone-1 : Python Parser + Folder Structure Viewer")

# folder_path = st.text_input("Enter folder path", placeholder="./examples or C:/Users/Project")


# # ---------------------------------------------------------------------
# # BUTTONS
# # ---------------------------------------------------------------------
# col1, col2 = st.columns(2)

# with col1:
#     if st.button("📂 Show Folder Structure"):
#         p = Path(folder_path)
#         if not p.exists():
#             st.error("❌ Folder does not exist.")
#         else:
#             st.session_state.tree_output = folder_tree(p)
#             st.success("✅ Folder structure generated")

# with col2:
#     if st.button("🔍 Scan for Python Files"):
#         p = Path(folder_path)
#         if not p.exists():
#             st.error("❌ Folder does not exist.")
#         else:
#             st.session_state.parsed_files = []

#             for py_file in p.rglob("*.py"):
#                 st.session_state.parsed_files.append(parser.parse_file(py_file))

#             reporter.generate_report(st.session_state.parsed_files, REPORT_PATH)
#             st.session_state.report_ready = True
#             st.success("✅ Scan complete. Report generated.")


# # ---------------------------------------------------------------------
# # SHOW FOLDER STRUCTURE
# # ---------------------------------------------------------------------
# if st.session_state.tree_output:
#     st.subheader("📁 Folder Structure")
#     st.code(st.session_state.tree_output)


# # ---------------------------------------------------------------------
# # TABS → File Summary / Coverage / AST
# # ---------------------------------------------------------------------
# tab1, tab2, tab3 = st.tabs(["📄 File Summary", "📊 Coverage", "🧬 AST Output"])

# # -------- Tab1: Summary ----------
# with tab1:
#     st.subheader("📄 Python Files Detected")

#     if st.session_state.parsed_files:
#         for f in st.session_state.parsed_files:
#             st.write(f"### 📌 {Path(f['path']).name}")
#             st.write(f"• Functions: {len(f['functions'])}")
#             st.write(f"• Classes: {len(f['classes'])}")
#             st.divider()
#     else:
#         st.info("No files scanned yet.")


# # -------- Tab2: Coverage ----------
# with tab2:
#     if st.session_state.report_ready and REPORT_PATH.exists():
#         report = json.loads(REPORT_PATH.read_text())

#         metrics = report["metrics"]

#         st.metric("Files Scanned", metrics["files_scanned"])
#         st.metric("Functions", metrics["functions_total"])
#         st.metric("Docstrings", metrics["functions_documented"])
#         st.metric("Coverage %", metrics["coverage_percent"])

#         st.divider()

#         with open(REPORT_PATH, "rb") as f:
#             st.download_button("⬇️ Download Report", f, file_name="review_logs.json")

#     else:
#         st.info("Run scan to see coverage.")


# # -------- Tab3: AST ----------
# with tab3:
#     if st.session_state.report_ready and REPORT_PATH.exists():
#         st.json(json.loads(REPORT_PATH.read_text()))
#     else:
#         st.info("AST will appear after scanning.")

# import sys
# from pathlib import Path
# import json
# import streamlit as st

# # Add project root
# sys.path.append(str(Path(__file__).parent))

# from core.parser.python_parser import parse_python_files
# from core.review_engine.ai_review import AIReviewer
# from core.validator.pylint_runner import run_pylint
# from core.utils.diff_utils import generate_diff

# # ---------- PAGE CONFIG ----------
# st.set_page_config(
#     page_title="AI-Powered Code Reviewer",
#     layout="wide"
# )

# # ---------- SIDEBAR ----------
# st.sidebar.title("🧠 AI Code Reviewer")

# docstring_style = st.sidebar.selectbox(
#     "Docstring Style",
#     ["Google", "NumPy", "REST API"]
# )

# view = st.sidebar.selectbox(
#     "Select View",
#     ["🏠 Home", "📄 Docstrings", "✅ Validation", "📊 Metrics"]
# )

# path = st.sidebar.text_input("Path to scan", "examples")
# scan = st.sidebar.button("Scan Code")


# # ---------- APPLY DOCSTRING & DEFAULT IMPLEMENTATION ----------
# def apply_docstring_change(func):
#     file_path = func["file"]
#     new_doc = func["preview_docstring"].strip()
#     new_doc = new_doc.replace('"""', '\\"""')

#     with open(file_path, "r", encoding="utf-8") as f:
#         lines = f.readlines()

#     start = func.get("docstring_start")
#     end = func.get("docstring_end")

#     # Create docstring block
#     doc_block = ['    """\n']
#     for line in new_doc.splitlines():
#         doc_block.append(f"    {line}\n")
#     doc_block.append('    """\n')

#     # Replace or insert docstring
#     if start is not None and end is not None:
#         lines[start:end] = doc_block
#         insert_index = end
#     else:
#         for i, line in enumerate(lines):
#             if line.strip().startswith(f"def {func['name']}"):
#                 lines[i+1:i+1] = doc_block
#                 insert_index = i + 1 + len(doc_block)
#                 break

#     # Insert simple default function logic if needed
#     func_name = func['name'].lower()
#     default_body = []

#     if func_name == 'calculate_average':
#         default_body = [
#             '    if not numbers:\n',
#             '        return 0\n',
#             '    return sum(numbers) / len(numbers)\n'
#         ]
#     elif func_name == 'add':
#         default_body = [
#             '    return a + b\n'
#         ]
#     elif func_name == 'process':
#         default_body = [
#             '    return [d * 2 for d in data]\n'
#         ]
#     # Add more rules for your other functions here

#     if default_body:
#         lines[insert_index:insert_index] = default_body

#     with open(file_path, "w", encoding="utf-8") as f:
#         f.writelines(lines)


# # ---------- SCAN ----------
# if scan:
#     functions = parse_python_files(path)
#     reviewer = AIReviewer(style=docstring_style)
#     coverage, previews = reviewer.review(functions)

#     for f, preview in zip(functions, previews):
#         f["preview_docstring"] = preview

#     st.session_state["functions"] = functions
#     st.session_state["coverage"] = coverage
#     st.session_state["previews"] = previews
#     st.session_state["pylint"] = run_pylint(path)
#     st.session_state["scan_completed"] = True


# # ---------- MAIN ----------
# if "coverage" in st.session_state:
#     coverage = st.session_state["coverage"]
#     functions = st.session_state["functions"]

#     # ---------- DOCSTRINGS ----------
#     if view == "📄 Docstrings":
#         st.title("Docstrings Preview")

#         for idx, func in enumerate(functions):
#             st.markdown(f"## Function: `{func['name']}`")

#             before = func.get("docstring") or ""
#             after = func.get("preview_docstring") or ""

#             col1, col2 = st.columns(2)

#             # BEFORE
#             with col1:
#                 st.subheader("Before")
#                 if before:
#                     st.code(before, language="python")
#                 else:
#                     st.error("No existing docstring")

#             # AFTER (Preview)
#             with col2:
#                 st.subheader("After (Preview)")
#                 st.code(after, language="python")

#             # DIFF
#             st.subheader("Diff")
#             st.code(generate_diff(before, after), language="diff")

#             c1, c2 = st.columns(2)

#             if c1.button("✅ Accept", key=f"accept_{idx}"):
#                 apply_docstring_change(func)

#                 # Re-scan & refresh session state
#                 updated_functions = parse_python_files(path)
#                 reviewer = AIReviewer(style=docstring_style)
#                 coverage, previews = reviewer.review(updated_functions)

#                 for f, p in zip(updated_functions, previews):
#                     f["preview_docstring"] = p

#                 st.session_state["functions"] = updated_functions
#                 st.session_state["coverage"] = coverage
#                 st.session_state["previews"] = previews

#                 st.success("Docstring applied successfully ✔")
#                 st.stop()  # refresh page safely

#             if c2.button("❌ Reject", key=f"reject_{idx}"):
#                 st.warning("Suggestion rejected")

#             st.divider()

#     # ---------- HOME ----------
#     elif view == "🏠 Home":
#         st.title("AI-Powered Code Reviewer Dashboard")

#         total = coverage.get("total", 0)
#         documented = coverage.get("documented", 0)
#         undocumented = total - documented
#         coverage_percent = coverage.get("coverage", 0)

#         col1, col2, col3, col4 = st.columns(4)
#         col1.metric("Total Functions", total)
#         col2.metric("Documented", documented)
#         col3.metric("Undocumented", undocumented)
#         col4.metric("Coverage %", f"{coverage_percent}%")

#         st.subheader("Documentation Coverage Progress")
#         st.progress(coverage_percent / 100 if coverage_percent else 0)

#         st.info(
#             "- Coverage shows **existing documentation only**\n"
#             "- Previewed docstrings **do NOT change coverage**\n"
#             "- Coverage updates only after real fixes"
#         )

#         st.download_button(
#             label="Download Coverage Report JSON",
#             data=json.dumps(coverage, indent=4),
#             file_name="coverage_report.json",
#             mime="application/json"
#         )

#         if st.session_state.get("scan_completed"):
#             st.success("✅ Scan completed")

#     # ---------- VALIDATION ----------
#     elif view == "✅ Validation":
#         st.title("Pylint Validation")

#         violations = len(st.session_state.get("pylint", []))
#         st.bar_chart({
#             "Compliant": max(0, 5 - violations),
#             "Violations": violations
#         })

#         for issue in st.session_state.get("pylint", []):
#             st.error(issue)

#     # ---------- METRICS ----------
#     elif view == "📊 Metrics":
#         st.title("Metrics (JSON)")
#         st.json(coverage)

# else:
#     st.info("👈 Enter a path and click **Scan Code** to begin.")
# import sys
# from pathlib import Path
# import json
# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # ---------------- PATH SETUP ----------------
# sys.path.append(str(Path(__file__).parent))

# from core.parser.python_parser import parse_python_files
# from core.review_engine.ai_review import AIReviewer
# from core.validator.pylint_runner import run_pylint
# from core.utils.diff_utils import generate_diff

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(
#     page_title="🚀 AI-Powered Code Reviewer",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ---------------- SESSION STATE INIT ----------------
# if "scan_completed" not in st.session_state:
#     st.session_state.scan_completed = False

# if "dashboard_action" not in st.session_state:
#     st.session_state.dashboard_action = None

# # ---------------- SIDEBAR ----------------
# st.sidebar.title("🧠 AI Code Reviewer")

# docstring_style = st.sidebar.selectbox(
#     "Docstring Style",
#     ["Google", "NumPy", "REST API"]
# )

# view = st.sidebar.selectbox(
#     "Select View",
#     ["🏠 Home", "✅ Validation", "📄 Docstrings", "📊 Metrics", "📊 Dashboard"]
# )

# path = st.sidebar.text_input("Path to scan", "examples")

# # ---------------- SCAN ----------------
# if st.sidebar.button("🚀 Scan Code"):
#     if not Path(path).exists():
#         st.sidebar.error("❌ Invalid path")
#         st.session_state.scan_completed = False
#     else:
#         with st.spinner("🔍 Scanning project..."):
#             functions = parse_python_files(path)

#             if not functions:
#                 st.sidebar.warning("⚠️ No Python files found")
#                 st.session_state.scan_completed = False
#             else:
#                 reviewer = AIReviewer(style=docstring_style)
#                 coverage, previews = reviewer.review(functions)

#                 for f, p in zip(functions, previews):
#                     f["preview_docstring"] = p

#                 st.session_state.functions = functions
#                 st.session_state.coverage = coverage
#                 st.session_state.pylint = run_pylint(path)
#                 st.session_state.scan_completed = True

#         st.sidebar.success("✅ Scan completed")

# # ---------------- STOP BEFORE SCAN ----------------
# if not st.session_state.scan_completed:
#     st.info("👈 Enter path and click **Scan Code** to begin")
#     st.stop()

# functions = st.session_state.functions

# # ---------------- HOME ----------------
# if view == "🏠 Home":

#     total = len(functions)
#     documented = sum(1 for f in functions if f.get("docstring"))
#     coverage_percent = (documented / total * 100) if total else 0

#     c1, c2, c3 = st.columns(3)

#     def home_card(title, value, icon):
#         st.markdown(f"""
#         <div style="
#             background:linear-gradient(135deg,#667eea,#764ba2);
#             padding:25px;border-radius:20px;
#             color:white;text-align:center;
#             box-shadow:0 8px 20px rgba(0,0,0,0.3)">
#             <h3>{icon} {title}</h3>
#             <h1>{value}</h1>
#         </div>
#         """, unsafe_allow_html=True)

#     with c1: home_card("Total Functions", total, "🧩")
#     with c2: home_card("Documented", documented, "✅")
#     with c3: home_card("Coverage", f"{coverage_percent:.2f}%", "📊")

# # ---------------- VALIDATION ----------------
# elif view == "✅ Validation":

#     st.subheader("✅ Pylint Validation")
#     issues = st.session_state.pylint

#     if not issues:
#         st.success("No issues found 🎉")
#     else:
#         for i in issues:
#             st.error(i)

# # ---------------- DOCSTRINGS ----------------
# elif view == "📄 Docstrings":

#     for f in functions:
#         st.markdown(f"### `{f['name']}`")

#         c1, c2 = st.columns(2)

#         with c1:
#             st.code(f.get("docstring", "No docstring"), "python")

#         with c2:
#             st.code(f.get("preview_docstring", ""), "python")

#         st.code(
#             generate_diff(
#                 f.get("docstring", ""),
#                 f.get("preview_docstring", "")
#             ),
#             "diff"
#         )

# # ---------------- METRICS ----------------
# elif view == "📊 Metrics":

#     st.json({
#         "total_functions": len(functions),
#         "documented": sum(1 for f in functions if f.get("docstring")),
#         "coverage": st.session_state.coverage
#     })

# # ---------------- DASHBOARD (ENHANCED UI) ----------------
# elif view == "📊 Dashboard":

#     st.markdown("""
#     <div style="background:linear-gradient(90deg,#6a5acd,#7b68ee);
#         padding:25px;border-radius:18px;
#         color:white;font-size:26px;font-weight:600;">
#         ✨ Enhanced UI Features
#         <div style="font-size:14px;opacity:0.85;">
#             Explore powerful analysis tools
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("<br>", unsafe_allow_html=True)

#     c1, c2, c3, c4 = st.columns(4)

#     def feature_card(title, subtitle, icon, bg, key):
#         if st.button(title, key=key, use_container_width=True):
#             st.session_state.dashboard_action = key

#         st.markdown(f"""
#         <div style="background:{bg};
#             padding:22px;border-radius:18px;
#             color:white;text-align:center;
#             box-shadow:0 10px 25px rgba(0,0,0,0.35);">
#             <div style="font-size:38px;">{icon}</div>
#             <div style="font-size:18px;font-weight:600;">{subtitle}</div>
#         </div>
#         """, unsafe_allow_html=True)

#     with c1: feature_card("filter", "Advanced Filters", "🔍",
#                           "linear-gradient(135deg,#667eea,#764ba2)", "filter")
#     with c2: feature_card("search", "Search", "🔎",
#                           "linear-gradient(135deg,#ff758c,#ff7eb3)", "search")
#     with c3: feature_card("export", "Export", "📦",
#                           "linear-gradient(135deg,#43cea2,#185a9d)", "export")
#     with c4: feature_card("help", "Help & Tips", "💡",
#                           "linear-gradient(135deg,#56ab2f,#a8e063)", "help")
    

#     action = st.session_state.dashboard_action

#     rows = [{
#         "File": f.get("file", "N/A"),
#         "Function": f.get("name", "N/A"),
#         "Docstring": "OK" if f.get("docstring") else "FIX"
#     } for f in functions]

#     df = pd.DataFrame(rows)

#     # ---------------- EXPORT ----------------
#     if action == "export":
#         st.subheader("📦 Export Summary")
#         st.dataframe(df, use_container_width=True)

#         c1, c2 = st.columns(2)
#         with c1:
#             st.download_button(
#                 "📥 Export as JSON",
#                 json.dumps(rows, indent=4),
#                 "analysis_export.json",
#                 "application/json",
#                 use_container_width=True
#             )
#         with c2:
#             st.download_button(
#                 "📥 Export as CSV",
#                 df.to_csv(index=False),
#                 "analysis_export.csv",
#                 "text/csv",
#                 use_container_width=True
#             )

#     # ---------------- FILTER ----------------
#     elif action == "filter":
#         st.subheader("⚙️ Advanced Filters")
#         status = st.selectbox("Docstring Status", ["ALL", "Yes", "No"])
#         mapping = {"Yes": "OK", "No": "FIX"}
#         if status == "ALL":
#             df_filtered = df
#         else:
#             df_filtered = df[df["Docstring"] == mapping[status]]
#         st.dataframe(df_filtered, use_container_width=True)

#     # ---------------- SEARCH ----------------
#     elif action == "search":
#         st.subheader("🔍 Search")
#         q = st.text_input("Search function or file")
#         if q:
#             df_filtered = df[
#                 df["Function"].fillna("").str.contains(q, case=False) |
#                 df["File"].fillna("").str.contains(q, case=False)
#             ]
#         else:
#             df_filtered = df
#         st.dataframe(df_filtered, use_container_width=True)

#     # ---------------- HELP ----------------
#     elif action == "help":
#         st.subheader("ℹ️ Help & Tips")
#         st.info(
#             "📊 Coverage Metrics\n"
#             "- Coverage % = (Documented / Total) × 100\n"
#             "- 🟢 Green ≥ 90%\n"
#             "- 🟡 Yellow 70–89%\n"
#             "- 🔴 Red < 70%"
#         )
#         st.warning(
#             "✅ Function Status\n"
#             "- 🟢 Complete docstring\n"
#             "- ❌ Missing / incomplete\n"
#             "- Auto style detection"
#         )
#         st.success(
#             "🧪 Test Results\n"
#             "- Real-time execution\n"
#             "- Pass / Fail ratio\n"
#             "- Pytest integration"
#         )
#         st.info(
#             "📝 Docstring Styles\n"
#             "- Google\n"
#             "- NumPy\n"
#             "- REST / reST\n"
#             "- Auto validation"
#         )
#     else:
#         st.info("👆 Select a dashboard card above")


#     # ---------------- LOAD PYTEST REPORT ----------------
#     report_path = "storage/reports/pytest_results.json"

#     if not Path(report_path).exists():
#         st.warning("⚠️ Pytest report not found. Run pytest first.")
#         st.stop()

#     with open(report_path, "r") as f:
#         report = json.load(f)

#     tests = report.get("tests", [])

#     # ---------------- PROCESS TEST DATA ----------------
#     my_test_files = [
#         "test_coverage_reporter.py",
#         "test_dashboard.py",
#         "test_generator.py",
#         "test_llm_integration.py",
#         "test_parser.py",
#         "test_validator.py"
#     ]

#     # Initialize stats
#     module_stats = {f: {"passed": 0, "failed": 0} for f in my_test_files}

#     for t in tests:
#         file_name = Path(t["nodeid"].split("::")[0]).name
#         if file_name in my_test_files:
#             status = t["outcome"]
#             module_stats[file_name][status] += 1

#     # Prepare DataFrame for charts and tables
#     df_chart = pd.DataFrame([
#         {"Module": f.replace("test_", "").replace(".py", "").title(),
#          "Passed": v["passed"],
#          "Failed": v["failed"]}
#         for f, v in module_stats.items()
#     ])


#     # ---------------- STAGE 1: METRICS ----------------
#     total_tests = len(tests)
#     passed = sum(1 for t in tests if t["outcome"] == "passed")
#     failed = sum(1 for t in tests if t["outcome"] == "failed")

#     c1, c2, c3 = st.columns(3)

#     def metric_card(title, value, color):
#         st.markdown(f"""
#         <div style="
#             background:{color};
#             padding:22px;border-radius:16px;
#             color:white;text-align:center;
#             box-shadow:0 8px 20px rgba(0,0,0,0.4)">
#             <div style="font-size:14px;opacity:0.85">{title}</div>
#             <div style="font-size:32px;font-weight:700">{value}</div>
#         </div>
#         """, unsafe_allow_html=True)

#     with c1: metric_card("Total Tests", total_tests, "#374151")
#     with c2: metric_card("Passed", passed, "#16a34a")
#     with c3: metric_card("Failed", failed, "#dc2626")

#     st.markdown("<br>", unsafe_allow_html=True)

#     # ---------------- STAGE 2: BAR CHART ----------------
#     st.subheader("📈 Test Results")

#     fig = px.bar(
#         df_chart,
#         x="Module",
#         y=["Passed", "Failed"],
#         barmode="group",
#         color_discrete_sequence=["#3b82f6", "#ef4444"]
#     )

#     fig.update_layout(
#         height=420,
#         plot_bgcolor="#0f172a",
#         paper_bgcolor="#0f172a",
#         font_color="white",
#         legend_title_text="Status"
#     )

#     st.plotly_chart(fig, use_container_width=True)

#     # ---------------- STAGE 3: TABLE ----------------
#     st.subheader("📋 Detailed Results")
#     st.dataframe(df_chart, use_container_width=True)
# import sys
# from pathlib import Path
# import json
# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # ---------------- PATH SETUP ----------------
# sys.path.append(str(Path(__file__).parent))

# from core.parser.python_parser import parse_python_files
# from core.review_engine.ai_review import AIReviewer
# from core.validator.pylint_runner import run_pylint
# from core.utils.diff_utils import generate_diff

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(
#     page_title="🚀 AI-Powered Code Reviewer",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ---------------- SESSION STATE INIT ----------------
# if "scan_completed" not in st.session_state:
#     st.session_state.scan_completed = False

# if "dashboard_action" not in st.session_state:
#     st.session_state.dashboard_action = None

# # ---------------- SIDEBAR ----------------
# st.sidebar.title("🧠 AI Code Reviewer")

# docstring_style = st.sidebar.selectbox(
#     "Docstring Style",
#     ["Google", "NumPy", "REST API"]
# )

# view = st.sidebar.selectbox(
#     "Select View",
#     ["🏠 Home", "✅ Validation", "📄 Docstrings", "📊 Metrics", "📊 Dashboard"]
# )

# path = st.sidebar.text_input("Path to scan", "examples")

# # ---------------- SCAN ----------------
# if st.sidebar.button("🚀 Scan Code"):
#     if not Path(path).exists():
#         st.sidebar.error("❌ Invalid path")
#         st.session_state.scan_completed = False
#     else:
#         with st.spinner("🔍 Scanning project..."):
#             functions = parse_python_files(path)

#             if not functions:
#                 st.sidebar.warning("⚠️ No Python files found")
#                 st.session_state.scan_completed = False
#             else:
#                 reviewer = AIReviewer(style=docstring_style)
#                 coverage, previews = reviewer.review(functions)

#                 for f, p in zip(functions, previews):
#                     f["preview_docstring"] = p

#                 st.session_state.functions = functions
#                 st.session_state.coverage = coverage
#                 st.session_state.pylint = run_pylint(path)
#                 st.session_state.scan_completed = True

#         st.sidebar.success("✅ Scan completed")

# # ---------------- STOP BEFORE SCAN ----------------
# if not st.session_state.scan_completed:
#     st.info("👈 Enter path and click **Scan Code** to begin")
#     st.stop()

# functions = st.session_state.functions

# # ---------------- HOME ----------------
# if view == "🏠 Home":

#     total = len(functions)
#     documented = sum(1 for f in functions if f.get("docstring"))
#     coverage_percent = (documented / total * 100) if total else 0

#     c1, c2, c3 = st.columns(3)

#     def home_card(title, value, icon):
#         st.markdown(f"""
#         <div style="
#             background:linear-gradient(135deg,#667eea,#764ba2);
#             padding:25px;border-radius:20px;
#             color:white;text-align:center;
#             box-shadow:0 8px 20px rgba(0,0,0,0.3)">
#             <h3>{icon} {title}</h3>
#             <h1>{value}</h1>
#         </div>
#         """, unsafe_allow_html=True)

#     with c1: home_card("Total Functions", total, "🧩")
#     with c2: home_card("Documented", documented, "✅")
#     with c3: home_card("Coverage", f"{coverage_percent:.2f}%", "📊")

# # ---------------- VALIDATION ----------------
# elif view == "✅ Validation":

#     st.subheader("✅ Pylint Validation")
#     issues = st.session_state.pylint

#     if not issues:
#         st.success("No issues found 🎉")
#     else:
#         for i in issues:
#             st.error(i)
# # # ---------- APPLY DOCSTRING & DEFAULT IMPLEMENTATION ----------
# # def apply_docstring_change(func):
#     file_path = func["file"]
#     new_doc = func["preview_docstring"].strip()
#     new_doc = new_doc.replace('"""', '\\"""')

#     with open(file_path, "r", encoding="utf-8") as f:
#         lines = f.readlines()

#     start = func.get("docstring_start")
#     end = func.get("docstring_end")

#     # Create docstring block
#     doc_block = ['    """\n']
#     for line in new_doc.splitlines():
#         doc_block.append(f"    {line}\n")
#     doc_block.append('    """\n')

#     # Replace or insert docstring
#     if start is not None and end is not None:
#         lines[start:end] = doc_block
#         insert_index = end
#     else:
#         for i, line in enumerate(lines):
#             if line.strip().startswith(f"def {func['name']}"):
#                 lines[i+1:i+1] = doc_block
#                 insert_index = i + 1 + len(doc_block)
#                 break

#     # Insert simple default function logic if needed
#     func_name = func['name'].lower()
#     default_body = []

#     if func_name == 'calculate_average':
#         default_body = [
#             '    if not numbers:\n',
#             '        return 0\n',
#             '    return sum(numbers) / len(numbers)\n'
#         ]
#     elif func_name == 'add':
#         default_body = [
#             '    return a + b\n'
#         ]
#     elif func_name == 'process':
#         default_body = [
#             '    return [d * 2 for d in data]\n'
#         ]
#     # Add more rules for your other functions here

#     if default_body:
#         lines[insert_index:insert_index] = default_body

#     with open(file_path, "w", encoding="utf-8") as f:
#         f.writelines(lines)



# # # ---------------- DOCSTRINGS ----------------
# #  if view == "📄 Docstrings":
#         st.title("Docstrings Preview")

#         for idx, func in enumerate(functions):
#             st.markdown(f"## Function: `{func['name']}`")

#             before = func.get("docstring") or ""
#             after = func.get("preview_docstring") or ""

#             col1, col2 = st.columns(2)

#             # BEFORE
#             with col1:
#                 st.subheader("Before")
#                 if before:
#                     st.code(before, language="python")
#                 else:
#                     st.error("No existing docstring")

#             # AFTER (Preview)
#             with col2:
#                 st.subheader("After (Preview)")
#                 st.code(after, language="python")

#             # DIFF
#             st.subheader("Diff")
#             st.code(generate_diff(before, after), language="diff")

#             c1, c2 = st.columns(2)

#             if c1.button("✅ Accept", key=f"accept_{idx}"):
#                 apply_docstring_change(func)

#                 # Re-scan & refresh session state
#                 updated_functions = parse_python_files(path)
#                 reviewer = AIReviewer(style=docstring_style)
#                 coverage, previews = reviewer.review(updated_functions)

#                 for f, p in zip(updated_functions, previews):
#                     f["preview_docstring"] = p

#                 st.session_state["functions"] = updated_functions
#                 st.session_state["coverage"] = coverage
#                 st.session_state["previews"] = previews

#                 st.success("Docstring applied successfully ✔")
#                 st.stop()  # refresh page safely

#             if c2.button("❌ Reject", key=f"reject_{idx}"):
#                 st.warning("Suggestion rejected")

#             st.divider()

# # # ---------------- METRICS ----------------
# elif view == "📊 Metrics":

#     st.json({
#         "total_functions": len(functions),
#         "documented": sum(1 for f in functions if f.get("docstring")),
#         "coverage": st.session_state.coverage
#     })

# # ---------------- DASHBOARD (ENHANCED UI) ----------------
# elif view == "📊 Dashboard":

#     st.markdown("""
#     <div style="background:linear-gradient(90deg,#6a5acd,#7b68ee);
#         padding:25px;border-radius:18px;
#         color:white;font-size:26px;font-weight:600;">
#         ✨ Enhanced UI Features
#         <div style="font-size:14px;opacity:0.85;">
#             Explore powerful analysis tools
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("<br>", unsafe_allow_html=True)

#     c1, c2, c3, c4 = st.columns(4)

#     def feature_card(title, subtitle, icon, bg, key):
#         if st.button(title, key=key, use_container_width=True):
#             st.session_state.dashboard_action = key

#         st.markdown(f"""
#         <div style="background:{bg};
#             padding:22px;border-radius:18px;
#             color:white;text-align:center;
#             box-shadow:0 10px 25px rgba(0,0,0,0.35);">
#             <div style="font-size:38px;">{icon}</div>
#             <div style="font-size:18px;font-weight:600;">{subtitle}</div>
#         </div>
#         """, unsafe_allow_html=True)

#     with c1: feature_card("filter", "Advanced Filters", "🔍",
#                           "linear-gradient(135deg,#667eea,#764ba2)", "filter")
#     with c2: feature_card("search", "Search", "🔎",
#                           "linear-gradient(135deg,#ff758c,#ff7eb3)", "search")
#     with c3: feature_card("export", "Export", "📦",
#                           "linear-gradient(135deg,#43cea2,#185a9d)", "export")
#     with c4: feature_card("help", "Help & Tips", "💡",
#                           "linear-gradient(135deg,#56ab2f,#a8e063)", "help")
    

#     action = st.session_state.dashboard_action

#     rows = [{
#         "File": f.get("file", "N/A"),
#         "Function": f.get("name", "N/A"),
#         "Docstring": "OK" if f.get("docstring") else "FIX"
#     } for f in functions]

#     df = pd.DataFrame(rows)

#     # ---------------- EXPORT ----------------
#     if action == "export":
#         st.subheader("📦 Export Summary")
#         st.dataframe(df, use_container_width=True)

#         c1, c2 = st.columns(2)
#         with c1:
#             st.download_button(
#                 "📥 Export as JSON",
#                 json.dumps(rows, indent=4),
#                 "analysis_export.json",
#                 "application/json",
#                 use_container_width=True
#             )
#         with c2:
#             st.download_button(
#                 "📥 Export as CSV",
#                 df.to_csv(index=False),
#                 "analysis_export.csv",
#                 "text/csv",
#                 use_container_width=True
#             )

#     # ---------------- FILTER ----------------
#     elif action == "filter":
#         st.subheader("⚙️ Advanced Filters")
#         status = st.selectbox("Docstring Status", ["ALL", "Yes", "No"])
#         mapping = {"Yes": "OK", "No": "FIX"}
#         if status == "ALL":
#             df_filtered = df
#         else:
#             df_filtered = df[df["Docstring"] == mapping[status]]
#         st.dataframe(df_filtered, use_container_width=True)

#     # ---------------- SEARCH ----------------
#     elif action == "search":
#         st.subheader("🔍 Search")
#         q = st.text_input("Search function or file")
#         if q:
#             df_filtered = df[
#                 df["Function"].fillna("").str.contains(q, case=False) |
#                 df["File"].fillna("").str.contains(q, case=False)
#             ]
#         else:
#             df_filtered = df
#         st.dataframe(df_filtered, use_container_width=True)

#     # ---------------- HELP ----------------
#     elif action == "help":
#         st.subheader("ℹ️ Help & Tips")
#         st.info(
#             "📊 Coverage Metrics\n"
#             "- Coverage % = (Documented / Total) × 100\n"
#             "- 🟢 Green ≥ 90%\n"
#             "- 🟡 Yellow 70–89%\n"
#             "- 🔴 Red < 70%"
#         )
#         st.warning(
#             "✅ Function Status\n"
#             "- 🟢 Complete docstring\n"
#             "- ❌ Missing / incomplete\n"
#             "- Auto style detection"
#         )
#         st.success(
#             "🧪 Test Results\n"
#             "- Real-time execution\n"
#             "- Pass / Fail ratio\n"
#             "- Pytest integration"
#         )
#         st.info(
#             "📝 Docstring Styles\n"
#             "- Google\n"
#             "- NumPy\n"
#             "- REST / reST\n"
#             "- Auto validation"
#         )
#     else:
#         st.info("👆 Select a dashboard card above")


#     # ---------------- LOAD PYTEST REPORT ----------------
#     report_path = "storage/reports/pytest_results.json"

#     if not Path(report_path).exists():
#         st.warning("⚠️ Pytest report not found. Run pytest first.")
#         st.stop()

#     with open(report_path, "r") as f:
#         report = json.load(f)

#     tests = report.get("tests", [])

#     # ---------------- PROCESS TEST DATA ----------------
#     my_test_files = [
#         "test_coverage_reporter.py",
#         "test_dashboard.py",
#         "test_generator.py",
#         "test_llm_integration.py",
#         "test_parser.py",
#         "test_validator.py"
#     ]

# Initialize stats
# module_stats = {f: {"passed": 0, "failed": 0} for f in my_test_files}

# for t in tests:
#         file_name = Path(t["nodeid"].split("::")[0]).name
#         if file_name in my_test_files:
#             status = t["outcome"]
#             module_stats[file_name][status] += 1

#     # Prepare DataFrame for charts and tables
# df_chart = pd.DataFrame([
#         {"Module": f.replace("test_", "").replace(".py", "").title(),
#          "Passed": v["passed"],
#          "Failed": v["failed"]}
#         for f, v in module_stats.items()
#     ])


#     # ---------------- STAGE 1: METRICS ----------------
# total_tests = len(tests)
# passed = sum(1 for t in tests if t["outcome"] == "passed")
# failed = sum(1 for t in tests if t["outcome"] == "failed")

# c1, c2, c3 = st.columns(3)

# def metric_card(title, value, color):
#         st.markdown(f"""
#         <div style="
#             background:{color};
#             padding:22px;border-radius:16px;
#             color:white;text-align:center;
#             box-shadow:0 8px 20px rgba(0,0,0,0.4)">
#             <div style="font-size:14px;opacity:0.85">{title}</div>
#             <div style="font-size:32px;font-weight:700">{value}</div>
#         </div>
#         """, unsafe_allow_html=True)

# with c1: metric_card("Total Tests", total_tests, "#374151")
# with c2: metric_card("Passed", passed, "#16a34a")
# with c3: metric_card("Failed", failed, "#dc2626")

# st.markdown("<br>", unsafe_allow_html=True)

#     # ---------------- STAGE 2: BAR CHART ----------------
# st.subheader("📈 Test Results")

# fig = px.bar(
#         df_chart,
#         x="Module",
#         y=["Passed", "Failed"],
#         barmode="group",
#         color_discrete_sequence=["#3b82f6", "#ef4444"]
#     )

# fig.update_layout(
#         height=420,
#         plot_bgcolor="#0f172a",
#         paper_bgcolor="#0f172a",
#         font_color="white",
# legend_title_text="Status"
# )

# st.plotly_chart(fig, use_container_width=True)

# # #     # ---------------- STAGE 3: TABLE ----------------
# st.subheader("📋 Detailed Results")
# st.dataframe(df_chart, use_container_width=True)


# import sys
# from pathlib import Path
# import json
# import streamlit as st
# import pandas as pd
# import plotly.express as px


# # Add project root
# sys.path.append(str(Path(__file__).parent))

# from core.parser.python_parser import parse_python_files
# from core.review_engine.ai_review import AIReviewer
# from core.validator.pylint_runner import run_pylint
# from core.utils.diff_utils import generate_diff

# # ---------- PAGE CONFIG ----------
# st.set_page_config(
#     page_title="AI-Powered Code Reviewer",
#     layout="wide"
# )

# # ---------- SIDEBAR ----------
# st.sidebar.title("🧠 AI Code Reviewer")

# docstring_style = st.sidebar.selectbox(
#     "Docstring Style",
#     ["Google", "NumPy", "REST API"]
# )

# view = st.sidebar.selectbox(
#     "Select View",
#     ["🏠 Home", "📄 Docstrings", "✅ Validation", "📊 Metrics", "📊 Dashboard"]
# )

# path = st.sidebar.text_input("Path to scan", "examples")
# scan = st.sidebar.button("Scan Code")


# # ---------- APPLY DOCSTRING & DEFAULT IMPLEMENTATION ----------
# def apply_docstring_change(func):
#     file_path = func["file"]
#     new_doc = func["preview_docstring"].strip()
#     new_doc = new_doc.replace('"""', '\\"""')

#     with open(file_path, "r", encoding="utf-8") as f:
#         lines = f.readlines()

#     start = func.get("docstring_start")
#     end = func.get("docstring_end")

#     # Create docstring block
#     doc_block = ['    """\n']
#     for line in new_doc.splitlines():
#         doc_block.append(f"    {line}\n")
#     doc_block.append('    """\n')

#     # Replace or insert docstring
#     if start is not None and end is not None:
#         lines[start:end] = doc_block
#         insert_index = end
#     else:
#         for i, line in enumerate(lines):
#             if line.strip().startswith(f"def {func['name']}"):
#                 lines[i+1:i+1] = doc_block
#                 insert_index = i + 1 + len(doc_block)
#                 break

#     # Insert simple default function logic if needed
#     func_name = func['name'].lower()
#     default_body = []

#     if func_name == 'calculate_average':
#         default_body = [
#             '    if not numbers:\n',
#             '        return 0\n',
#             '    return sum(numbers) / len(numbers)\n'
#         ]
#     elif func_name == 'add':
#         default_body = [
#             '    return a + b\n'
#         ]
#     elif func_name == 'process':
#         default_body = [
#             '    return [d * 2 for d in data]\n'
#         ]
#     # Add more rules for your other functions here

#     if default_body:
#         lines[insert_index:insert_index] = default_body

#     with open(file_path, "w", encoding="utf-8") as f:
#         f.writelines(lines)


# # ---------- SCAN ----------
# if scan:
#     functions = parse_python_files(path)
#     reviewer = AIReviewer(style=docstring_style)
#     coverage, previews = reviewer.review(functions)

#     for f, preview in zip(functions, previews):
#         f["preview_docstring"] = preview

#     st.session_state["functions"] = functions
#     st.session_state["coverage"] = coverage
#     st.session_state["previews"] = previews
#     st.session_state["pylint"] = run_pylint(path)
#     st.session_state["scan_completed"] = True


# # ---------- MAIN ----------
# if "coverage" in st.session_state:
#     coverage = st.session_state["coverage"]
#     functions = st.session_state["functions"]

#     # ---------- DOCSTRINGS ----------
#     if view == "📄 Docstrings":
#         st.title("Docstrings Preview")

#         for idx, func in enumerate(functions):
#             st.markdown(f"## Function: `{func['name']}`")

#             before = func.get("docstring") or ""
#             after = func.get("preview_docstring") or ""

#             col1, col2 = st.columns(2)

#             # BEFORE
#             with col1:
#                 st.subheader("Before")
#                 if before:
#                     st.code(before, language="python")
#                 else:
#                     st.error("No existing docstring")

#             # AFTER (Preview)
#             with col2:
#                 st.subheader("After (Preview)")
#                 st.code(after, language="python")

#             # DIFF
#             st.subheader("Diff")
#             st.code(generate_diff(before, after), language="diff")

#             c1, c2 = st.columns(2)

#             if c1.button("✅ Accept", key=f"accept_{idx}"):
#                 apply_docstring_change(func)

#                 # Re-scan & refresh session state
#                 updated_functions = parse_python_files(path)
#                 reviewer = AIReviewer(style=docstring_style)
#                 coverage, previews = reviewer.review(updated_functions)

#                 for f, p in zip(updated_functions, previews):
#                     f["preview_docstring"] = p

#                 st.session_state["functions"] = updated_functions
#                 st.session_state["coverage"] = coverage
#                 st.session_state["previews"] = previews

#                 st.success("Docstring applied successfully ✔")
#                 st.stop()  # refresh page safely

#             if c2.button("❌ Reject", key=f"reject_{idx}"):
#                 st.warning("Suggestion rejected")

#             st.divider()

#     # ---------- HOME ----------
#     elif view == "🏠 Home":
#         st.title("AI-Powered Code Reviewer Dashboard")

#         total = coverage.get("total", 0)
#         documented = coverage.get("documented", 0)
#         undocumented = total - documented
#         coverage_percent = coverage.get("coverage", 0)

#         col1, col2, col3, col4 = st.columns(4)
#         col1.metric("Total Functions", total)
#         col2.metric("Documented", documented)
#         col3.metric("Undocumented", undocumented)
#         col4.metric("Coverage %", f"{coverage_percent}%")

#         st.subheader("Documentation Coverage Progress")
#         st.progress(coverage_percent / 100 if coverage_percent else 0)

#         st.info(
#             "- Coverage shows **existing documentation only**\n"
#             "- Previewed docstrings **do NOT change coverage**\n"
#             "- Coverage updates only after real fixes"
#         )

#         st.download_button(
#             label="Download Coverage Report JSON",
#             data=json.dumps(coverage, indent=4),
#             file_name="coverage_report.json",
#             mime="application/json"
#         )

#         if st.session_state.get("scan_completed"):
#             st.success("✅ Scan completed")

#     # ---------- VALIDATION ----------
#     elif view == "✅ Validation":
#         st.title("Pylint Validation")

#         violations = len(st.session_state.get("pylint", []))
#         st.bar_chart({
#             "Compliant": max(0, 5 - violations),
#             "Violations": violations
#         })

#         for issue in st.session_state.get("pylint", []):
#             st.error(issue)

#     # ---------- METRICS ----------
#     elif view == "📊 Metrics":
#         st.title("Metrics (JSON)")
#         st.json(coverage)


# # ---------------- DASHBOARD (ENHANCED UI) ----------------


# # Define default action outside, so it's always available
# # ---------------- Dashboard ----------------
#     action = None  # default value

# if view == "📊 Dashboard":
#     if st.session_state.get("scan_completed", False):
#         st.markdown("""
#         <div style="background:linear-gradient(90deg,#6a5acd,#7b68ee);
#             padding:25px;border-radius:18px;
#             color:white;font-size:26px;font-weight:600;">
#             ✨ Enhanced UI Features
#             <div style="font-size:14px;opacity:0.85;">
#                 Explore powerful analysis tools
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#         st.markdown("<br>", unsafe_allow_html=True)

#         # ---------------- Feature Cards ----------------
#         def feature_card(title, subtitle, icon, bg, key):
#             if st.button(title, key=key, use_container_width=True):
#                 st.session_state["dashboard_action"] = key

#             st.markdown(f"""
#             <div style="background:{bg};
#                 padding:22px;border-radius:18px;
#                 color:white;text-align:center;
#                 box-shadow:0 10px 25px rgba(0,0,0,0.35);">
#                 <div style="font-size:38px;">{icon}</div>
#                 <div style="font-size:18px;font-weight:600;">{subtitle}</div>
#             </div>
#             """, unsafe_allow_html=True)

#         cols = st.columns(4)
#         cards = [
#             ("filter", "Advanced Filters", "🔍", "linear-gradient(135deg,#667eea,#764ba2)"),
#             ("search", "Search", "🔎", "linear-gradient(135deg,#ff758c,#ff7eb3)"),
#             ("export", "Export", "📦", "linear-gradient(135deg,#43cea2,#185a9d)"),
#             ("help", "Help & Tips", "💡", "linear-gradient(135deg,#56ab2f,#a8e063)")
#         ]

#         for col, (key, subtitle, icon, bg) in zip(cols, cards):
#             with col:
#                 feature_card(key, subtitle, icon, bg, key)

#         # Get dashboard action
#         action = st.session_state.get("dashboard_action", None)

#         # ---------------- DataFrame ----------------
#         functions = st.session_state.get("functions", [])
#         rows = [{
#             "File": f.get("file", "N/A"),
#             "Function": f.get("name", "N/A"),
#             "Docstring": "OK" if f.get("docstring") else "FIX"
#         } for f in functions]
#         df = pd.DataFrame(rows) if rows else pd.DataFrame(columns=["File", "Function", "Docstring"])

#         # ---------------- Handle Actions ----------------
#         if action == "export":
#             st.subheader("📦 Export Summary")
#             st.dataframe(df, use_container_width=True)
#             c1, c2 = st.columns(2)
#             with c1:
#                 st.download_button(
#                     "📥 Export as JSON",
#                     json.dumps(rows, indent=4),
#                     "analysis_export.json",
#                     "application/json",
#                     use_container_width=True
#                 )
#             with c2:
#                 st.download_button(
#                     "📥 Export as CSV",
#                     df.to_csv(index=False),
#                     "analysis_export.csv",
#                     "text/csv",
#                     use_container_width=True
#                 )

#         elif action == "filter":
#             st.subheader("⚙️ Advanced Filters")
#             status = st.selectbox("Docstring Status", ["ALL", "Yes", "No"])
#             mapping = {"Yes": "OK", "No": "FIX"}
#             df_filtered = df if status == "ALL" else df[df["Docstring"] == mapping[status]]
#             st.dataframe(df_filtered, use_container_width=True)

#         elif action == "search":
#             st.subheader("🔍 Search")
#             q = st.text_input("Search function or file")
#             df_filtered = df if not q else df[
#                 df["Function"].fillna("").str.contains(q, case=False) |
#                 df["File"].fillna("").str.contains(q, case=False)
#             ]
#             st.dataframe(df_filtered, use_container_width=True)

#         elif action == "help":
#             st.subheader("ℹ️ Help & Tips")
#             st.info(
#                 "📊 Coverage Metrics\n"
#                 "- Coverage % = (Documented / Total) × 100\n"
#                 "- 🟢 Green ≥ 90%\n"
#                 "- 🟡 Yellow 70–89%\n"
#                 "- 🔴 Red < 70%"
#             )
#             st.warning(
#                 "✅ Function Status\n"
#                 "- 🟢 Complete docstring\n"
#                 "- ❌ Missing / incomplete\n"
#                 "- Auto style detection"
#             )
#             st.success(
#                 "🧪 Test Results\n"
#                 "- Real-time execution\n"
#                 "- Pass / Fail ratio\n"
#                 "- Pytest integration"
#             )
#             st.info(
#                 "📝 Docstring Styles\n"
#                 "- Google\n"
#                 "- NumPy\n"
#                 "- REST / reST\n"
#                 "- Auto validation"
#             )
#         else:
#             st.info("👆 Select a dashboard card above")

#         # ---------------- Pytest Report ----------------
#         report_path = "storage/reports/pytest_results.json"
#         if Path(report_path).exists():
#             with open(report_path, "r") as f:
#                 report = json.load(f)
#             tests = report.get("tests", [])

#             my_test_files = [
#                 "test_coverage_reporter.py",
#                 "test_dashboard.py",
#                 "test_generator.py",
#                 "test_llm_integration.py",
#                 "test_parser.py",
#                 "test_validator.py"
#             ]

#             module_stats = {f: {"passed": 0, "failed": 0} for f in my_test_files}
#             for t in tests:
#                 file_name = Path(t["nodeid"].split("::")[0]).name
#                 if file_name in my_test_files:
#                     status = t["outcome"]
#                     module_stats[file_name][status] += 1

#             df_chart = pd.DataFrame([{
#                 "Module": f.replace("test_", "").replace(".py", "").title(),
#                 "Passed": v["passed"],
#                 "Failed": v["failed"]
#             } for f, v in module_stats.items()])

#             if not df_chart.empty:
#                 # Metrics cards
#                 total_tests = len(tests)
#                 passed = sum(1 for t in tests if t["outcome"] == "passed")
#                 failed = sum(1 for t in tests if t["outcome"] == "failed")
#                 c1, c2, c3 = st.columns(3)

#                 def metric_card(title, value, color):
#                     st.markdown(f"""
#                     <div style="
#                         background:{color};
#                         padding:22px;border-radius:16px;
#                         color:white;text-align:center;
#                         box-shadow:0 8px 20px rgba(0,0,0,0.4)">
#                         <div style="font-size:14px;opacity:0.85">{title}</div>
#                         <div style="font-size:32px;font-weight:700">{value}</div>
#                     </div>
#                     """, unsafe_allow_html=True)

#                 with c1: metric_card("Total Tests", total_tests, "#374151")
#                 with c2: metric_card("Passed", passed, "#16a34a")
#                 with c3: metric_card("Failed", failed, "#dc2626")

#                 st.markdown("<br>", unsafe_allow_html=True)

#                 # Bar chart
#                 st.subheader("📈 Test Results")
#                 fig = px.bar(
#                     df_chart,
#                     x="Module",
#                     y=["Passed", "Failed"],
#                     barmode="group",
#                     color_discrete_sequence=["#3b82f6", "#ef4444"]
#                 )
#                 fig.update_layout(
#                     height=420,
#                     plot_bgcolor="#0f172a",
#                     paper_bgcolor="#0f172a",
#                     font_color="white",
#                     legend_title_text="Status"
#                 )
#                 st.plotly_chart(fig, use_container_width=True)

#                 # Detailed results table
#                 st.subheader("📋 Detailed Results")
#                 st.dataframe(df_chart, use_container_width=True)
#         else:
#             st.warning("⚠️ Pytest report not found. Run pytest first.")



# import sys
# from pathlib import Path
# import json
# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # Add project root
# sys.path.append(str(Path(__file__).parent))

# from core.parser.python_parser import parse_python_files
# from core.review_engine.ai_review import AIReviewer
# from core.validator.pylint_runner import run_pylint
# from core.utils.diff_utils import generate_diff

# # ---------- PAGE CONFIG ----------
# st.set_page_config(
#     page_title="AI-Powered Code Reviewer",
#     layout="wide"
# )

# # ---------- SIDEBAR ----------
# st.sidebar.title("🧠 AI Code Reviewer")

# docstring_style = st.sidebar.selectbox(
#     "Docstring Style",
#     ["Google", "NumPy", "REST API"]
# )

# view = st.sidebar.selectbox(
#     "Select View",
#     ["🏠 Home", "📄 Docstrings", "✅ Validation", "📊 Metrics", "📊 Dashboard"]
# )

# path = st.sidebar.text_input("Path to scan", "examples")
# scan = st.sidebar.button("🚀 Scan Code")

# # ---------- APPLY DOCSTRING CHANGE ----------
# def apply_docstring_change(func):
#     file_path = func["file"]
#     new_doc = func["preview_docstring"].strip()
#     new_doc = new_doc.replace('"""', '\\"""')

#     with open(file_path, "r", encoding="utf-8") as f:
#         lines = f.readlines()

#     start = func.get("docstring_start")
#     end = func.get("docstring_end")

#     doc_block = ['    """\n']
#     for line in new_doc.splitlines():
#         doc_block.append(f"    {line}\n")
#     doc_block.append('    """\n')

#     if start is not None and end is not None:
#         lines[start:end] = doc_block
#         insert_index = end
#     else:
#         for i, line in enumerate(lines):
#             if line.strip().startswith(f"def {func['name']}"):
#                 lines[i+1:i+1] = doc_block
#                 insert_index = i + 1 + len(doc_block)
#                 break

#     func_name = func['name'].lower()
#     default_body = []
#     if func_name == 'calculate_average':
#         default_body = [
#             '    if not numbers:\n',
#             '        return 0\n',
#             '    return sum(numbers) / len(numbers)\n'
#         ]
#     elif func_name == 'add':
#         default_body = ['    return a + b\n']
#     elif func_name == 'process':
#         default_body = ['    return [d * 2 for d in data]\n']

#     if default_body:
#         lines[insert_index:insert_index] = default_body

#     with open(file_path, "w", encoding="utf-8") as f:
#         f.writelines(lines)

# # ---------- SCAN ----------
# if scan:
#     if not Path(path).exists():
#         st.sidebar.error("❌ Invalid path")
#         st.session_state.scan_completed = False
#     else:
#         with st.spinner("🔍 Scanning project..."):
#             functions = parse_python_files(path)
#             if not functions:
#                 st.sidebar.warning("⚠️ No Python files found")
#                 st.session_state.scan_completed = False
#             else:
#                 reviewer = AIReviewer(style=docstring_style)
#                 coverage, previews = reviewer.review(functions)

#                 for f, preview in zip(functions, previews):
#                     f["preview_docstring"] = preview

#                 st.session_state["functions"] = functions
#                 st.session_state["coverage"] = coverage
#                 st.session_state["previews"] = previews
#                 st.session_state["pylint"] = run_pylint(path)
#                 st.session_state["scan_completed"] = True
#         st.sidebar.success("✅ Scan completed")

# # ---------- ENHANCED CARDS ----------
# def home_card(title, value, icon, color="#667eea"):
#     st.markdown(f"""
#     <div style="
#         background:linear-gradient(135deg,{color},#764ba2);
#         padding:25px;border-radius:20px;
#         color:white;text-align:center;
#         box-shadow:0 8px 20px rgba(0,0,0,0.3);
#         transition: transform 0.2s;">
#         <h3>{icon} {title}</h3>
#         <h1>{value}</h1>
#     </div>
#     """, unsafe_allow_html=True)

# def metric_card(title, value, color):
#     st.markdown(f"""
#     <div style="
#         background:{color};
#         padding:20px;border-radius:16px;
#         color:white;text-align:center;
#         box-shadow:0 8px 20px rgba(0,0,0,0.4);
#         transition: transform 0.2s;">
#         <div style="font-size:14px;opacity:0.85">{title}</div>
#         <div style="font-size:32px;font-weight:700">{value}</div>
#     </div>
#     """, unsafe_allow_html=True)

# # ---------- MAIN ----------
# if "coverage" in st.session_state:
#     coverage = st.session_state["coverage"]
#     functions = st.session_state["functions"]

#     # ---------- DOCSTRINGS ----------
#     if view == "📄 Docstrings":
#         st.title("📜 Docstrings Preview")
#         for idx, func in enumerate(functions):
#             st.markdown(f"### Function: `{func['name']}`")
#             before = func.get("docstring") or ""
#             after = func.get("preview_docstring") or ""
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.subheader("Before")
#                 if before: st.code(before, language="python")
#                 else: st.error("No existing docstring")
#             with col2:
#                 st.subheader("After (Preview)")
#                 st.code(after, language="python")
#             st.subheader("Diff")
#             st.code(generate_diff(before, after), language="diff")
#             c1, c2 = st.columns(2)
#             with c1:
#                 if st.button("✅ Accept", key=f"accept_{idx}"):
#                     apply_docstring_change(func)
#                     st.success("Docstring applied successfully ✔")
#                     st.stop()
#             with c2:
#                 if st.button("❌ Reject", key=f"reject_{idx}"):
#                     st.warning("Suggestion rejected")
#             st.divider()

#     # ---------- HOME ----------
#     elif view == "🏠 Home":
#         st.title("🧠 AI-Powered Code Reviewer Dashboard")
#         total = coverage.get("total", 0)
#         documented = coverage.get("documented", 0)
#         undocumented = total - documented
#         coverage_percent = coverage.get("coverage", 0)

#         col1, col2, col3, col4 = st.columns(4)
#         with col1: home_card("Total Functions", total, "🧩", "#667eea")
#         with col2: home_card("Documented", documented, "✅", "#43cea2")
#         with col3: home_card("Undocumented", undocumented, "❌", "#f7971e")
#         with col4: home_card("Coverage %", f"{coverage_percent:.2f}%", "📊", "#ff6a00")

#         st.subheader("📈 Documentation Coverage")
#         st.progress(coverage_percent / 100 if coverage_percent else 0)

#         st.download_button(
#             label="📥 Download Coverage JSON",
#             data=json.dumps(coverage, indent=4),
#             file_name="coverage_report.json",
#             mime="application/json"
#         )
#         if st.session_state.get("scan_completed"):
#             st.success("✅ Scan completed")

#     # ---------- VALIDATION ----------
#     elif view == "✅ Validation":
#         st.title("Pylint Validation")
#         violations = len(st.session_state.get("pylint", []))
#         st.bar_chart({
#             "Compliant": max(0, 5 - violations),
#             "Violations": violations
#         })
#         for issue in st.session_state.get("pylint", []):
#             st.error(issue)

#     # ---------- METRICS ----------
#     elif view == "📊 Metrics":
#         st.title("📊 Metrics (JSON)")
#         st.json(coverage)

#     # ---------- DASHBOARD ----------
#     elif view == "📊 Dashboard":
#         if st.session_state.get("scan_completed", False):
#             st.markdown("""
#             <div style="background:linear-gradient(90deg,#6a5acd,#7b68ee);
#                 padding:25px;border-radius:18px;
#                 color:white;font-size:26px;font-weight:600;">
#                 ✨ Enhanced Dashboard
#                 <div style="font-size:14px;opacity:0.85;">Explore tools & insights</div>
#             </div>
#             """, unsafe_allow_html=True)
#             st.markdown("<br>", unsafe_allow_html=True)

#             # Feature cards
#             def feature_card(title, subtitle, icon, bg, key):
#                 if st.button(title, key=key, use_container_width=True):
#                     st.session_state["dashboard_action"] = key
#                 st.markdown(f"""
#                 <div style="background:{bg};
#                     padding:22px;border-radius:18px;
#                     color:white;text-align:center;
#                     box-shadow:0 10px 25px rgba(0,0,0,0.35);">
#                     <div style="font-size:38px;">{icon}</div>
#                     <div style="font-size:18px;font-weight:600;">{subtitle}</div>
#                 </div>
#                 """, unsafe_allow_html=True)

#             cols = st.columns(4)
#             cards = [
#                 ("filter", "Advanced Filters", "🔍", "linear-gradient(135deg,#667eea,#764ba2)"),
#                 ("search", "Search Functions", "🔎", "linear-gradient(135deg,#ff758c,#ff7eb3)"),
#                 ("export", "Export Data", "📦", "linear-gradient(135deg,#43cea2,#185a9d)"),
#                 ("help", "Help & Tips", "💡", "linear-gradient(135deg,#56ab2f,#a8e063)")
#             ]
#             for col, (key, subtitle, icon, bg) in zip(cols, cards):
#                 with col:
#                     feature_card(key, subtitle, icon, bg, key)

#             action = st.session_state.get("dashboard_action", None)

#             functions = st.session_state.get("functions", [])
#             rows = [{
#                 "File": f.get("file", "N/A"),
#                 "Function": f.get("name", "N/A"),
#                 "Docstring": "OK" if f.get("docstring") else "FIX"
#             } for f in functions]
#             df = pd.DataFrame(rows) if rows else pd.DataFrame(columns=["File", "Function", "Docstring"])

#             # Handle dashboard actions
#             if action == "export":
#                 st.subheader("📦 Export Summary")
#                 st.dataframe(df, use_container_width=True)
#                 c1, c2 = st.columns(2)
#                 with c1:
#                     st.download_button("📥 Export JSON", json.dumps(rows, indent=4),
#                                        "analysis_export.json", "application/json", use_container_width=True)
#                 with c2:
#                     st.download_button("📥 Export CSV", df.to_csv(index=False),
#                                        "analysis_export.csv", "text/csv", use_container_width=True)
#             elif action == "filter":
#                 st.subheader("⚙️ Advanced Filters")
#                 status = st.selectbox("Docstring Status", ["ALL", "Yes", "No"])
#                 mapping = {"Yes": "OK", "No": "FIX"}
#                 df_filtered = df if status=="ALL" else df[df["Docstring"]==mapping[status]]
#                 st.dataframe(df_filtered, use_container_width=True)
#             elif action == "search":
#                 st.subheader("🔍 Search")
#                 q = st.text_input("Search function or file")
#                 df_filtered = df if not q else df[
#                     df["Function"].str.contains(q, case=False, na=False) |
#                     df["File"].str.contains(q, case=False, na=False)
#                 ]
#                 st.dataframe(df_filtered, use_container_width=True)
#             elif action == "help":
#                 st.subheader("ℹ️ Help & Tips")
#                 st.info(
#                     "📊 Coverage Metrics\n- Coverage % = (Documented / Total) × 100\n- 🟢 ≥90%, 🟡 70–89%, 🔴 <70%"
#                 )
#                 st.warning(
#                     "✅ Function Status\n- 🟢 Complete docstring\n- ❌ Missing / incomplete"
#                 )
#                 st.success(
#                     "🧪 Test Results\n- Real-time execution\n- Pass/Fail ratio\n- Pytest integration"
#                 )
#                 st.info(
#             "📝 Docstring Styles\n"
#             "- Google\n"
#             "- NumPy\n"
#             "- REST / reST\n"
#             "- Auto validation"
#         )
import sys
from pathlib import Path
import json
import streamlit as st
import pandas as pd
import plotly.express as px

# Add project root
sys.path.append(str(Path(__file__).parent))

from core.parser.python_parser import parse_python_files
from core.review_engine.ai_review import AIReviewer
from core.validator.pylint_runner import run_pylint
from core.utils.diff_utils import generate_diff

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI-Powered Code Reviewer",
    layout="wide"
)

# ---------- SIDEBAR ----------
st.sidebar.title("🧠 AI Code Reviewer")

docstring_style = st.sidebar.selectbox(
    "Docstring Style",
    ["Google", "NumPy", "REST API"]
)

view = st.sidebar.selectbox(
    "Select View",
    ["🏠 Home", "📄 Docstrings", "✅ Validation", "📊 Metrics", "📊 Dashboard"]
)

path = st.sidebar.text_input("Path to scan", "examples")
scan = st.sidebar.button("🚀 Scan Code")

# ---------- APPLY DOCSTRING CHANGE ----------
def apply_docstring_change(func):
    file_path = func["file"]
    new_doc = func["preview_docstring"].strip()
    new_doc = new_doc.replace('"""', '\\"""')

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    start = func.get("docstring_start")
    end = func.get("docstring_end")

    doc_block = ['    """\n']
    for line in new_doc.splitlines():
        doc_block.append(f"    {line}\n")
    doc_block.append('    """\n')

    if start is not None and end is not None:
        lines[start:end] = doc_block
        insert_index = end
    else:
        for i, line in enumerate(lines):
            if line.strip().startswith(f"def {func['name']}"):
                lines[i+1:i+1] = doc_block
                insert_index = i + 1 + len(doc_block)
                break

    func_name = func['name'].lower()
    default_body = []
    if func_name == 'calculate_average':
        default_body = [
            '    if not numbers:\n',
            '        return 0\n',
            '    return sum(numbers) / len(numbers)\n'
        ]
    elif func_name == 'add':
        default_body = ['    return a + b\n']
    elif func_name == 'process':
        default_body = ['    return [d * 2 for d in data]\n']

    if default_body:
        lines[insert_index:insert_index] = default_body

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

# ---------- SCAN ----------
if scan:
    if not Path(path).exists():
        st.sidebar.error("❌ Invalid path")
        st.session_state.scan_completed = False
    else:
        with st.spinner("🔍 Scanning project..."):
            functions = parse_python_files(path)
            if not functions:
                st.sidebar.warning("⚠️ No Python files found")
                st.session_state.scan_completed = False
            else:
                reviewer = AIReviewer(style=docstring_style)
                coverage, previews = reviewer.review(functions)

                for f, preview in zip(functions, previews):
                    f["preview_docstring"] = preview

                st.session_state["functions"] = functions
                st.session_state["coverage"] = coverage
                st.session_state["previews"] = previews
                st.session_state["pylint"] = run_pylint(path)
                st.session_state["scan_completed"] = True
        st.sidebar.success("✅ Scan completed")

# ---------- ENHANCED CARDS ----------
def home_card(title, value, icon, color="#667eea"):
    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,{color},#764ba2);
        padding:25px;border-radius:20px;
        color:white;text-align:center;
        box-shadow:0 8px 20px rgba(0,0,0,0.3);
        transition: transform 0.2s;">
        <h3>{icon} {title}</h3>
        <h1>{value}</h1>
    </div>
    """, unsafe_allow_html=True)

def metric_card(title, value, color):
    st.markdown(f"""
    <div style="
        background:{color};
        padding:20px;border-radius:16px;
        color:white;text-align:center;
        box-shadow:0 8px 20px rgba(0,0,0,0.4);
        transition: transform 0.2s;">
        <div style="font-size:14px;opacity:0.85">{title}</div>
        <div style="font-size:32px;font-weight:700">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------- MAIN ----------
if "coverage" in st.session_state:
    coverage = st.session_state["coverage"]
    functions = st.session_state["functions"]

    # ---------- DOCSTRINGS ----------
    if view == "📄 Docstrings":
        st.title("📜 Docstrings Preview")
        for idx, func in enumerate(functions):
            st.markdown(f"### Function: `{func['name']}`")
            before = func.get("docstring") or ""
            after = func.get("preview_docstring") or ""
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Before")
                if before: st.code(before, language="python")
                else: st.error("No existing docstring")
            with col2:
                st.subheader("After (Preview)")
                st.code(after, language="python")
            st.subheader("Diff")
            st.code(generate_diff(before, after), language="diff")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Accept", key=f"accept_{idx}"):
                    apply_docstring_change(func)
                    st.success("Docstring applied successfully ✔")
                    st.stop()
            with c2:
                if st.button("❌ Reject", key=f"reject_{idx}"):
                    st.warning("Suggestion rejected")
            st.divider()

    # ---------- HOME ----------
    elif view == "🏠 Home":
        st.title("🧠 AI-Powered Code Reviewer Dashboard")
        total = coverage.get("total", 0)
        documented = coverage.get("documented", 0)
        undocumented = total - documented
        coverage_percent = coverage.get("coverage", 0)

        col1, col2, col3, col4 = st.columns(4)
        with col1: home_card("Total Functions", total, "🧩", "#667eea")
        with col2: home_card("Documented", documented, "✅", "#43cea2")
        with col3: home_card("Undocumented", undocumented, "❌", "#f7971e")
        with col4: home_card("Coverage %", f"{coverage_percent:.2f}%", "📊", "#ff6a00")

        st.subheader("📈 Documentation Coverage")
        st.progress(coverage_percent / 100 if coverage_percent else 0)

        st.download_button(
            label="📥 Download Coverage JSON",
            data=json.dumps(coverage, indent=4),
            file_name="coverage_report.json",
            mime="application/json"
        )
        if st.session_state.get("scan_completed"):
            st.success("✅ Scan completed")

    # ---------- VALIDATION ----------
    elif view == "✅ Validation":
        st.title("Pylint Validation")
        violations = len(st.session_state.get("pylint", []))
        st.bar_chart({
            "Compliant": max(0, 5 - violations),
            "Violations": violations
        })
        for issue in st.session_state.get("pylint", []):
            st.error(issue)

    # ---------- METRICS ----------
    elif view == "📊 Metrics":
        st.title("📊 Metrics (JSON)")
        st.json(coverage)

    # ---------- DASHBOARD ----------
    elif view == "📊 Dashboard":
        if st.session_state.get("scan_completed", False):
            st.markdown("""
            <div style="background:linear-gradient(90deg,#6a5acd,#7b68ee);
                padding:25px;border-radius:18px;
                color:white;font-size:26px;font-weight:600;">
                ✨ Enhanced Dashboard
                <div style="font-size:14px;opacity:0.85;">Explore tools & insights</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            # Feature cards
            def feature_card(title, subtitle, icon, bg, key):
                if st.button(title, key=key, use_container_width=True):
                    st.session_state["dashboard_action"] = key
                st.markdown(f"""
                <div style="background:{bg};
                    padding:22px;border-radius:18px;
                    color:white;text-align:center;
                    box-shadow:0 10px 25px rgba(0,0,0,0.35);">
                    <div style="font-size:38px;">{icon}</div>
                    <div style="font-size:18px;font-weight:600;">{subtitle}</div>
                </div>
                """, unsafe_allow_html=True)

            cols = st.columns(4)
            cards = [
                ("filter", "Advanced Filters", "🔍", "linear-gradient(135deg,#667eea,#764ba2)"),
                ("search", "Search Functions", "🔎", "linear-gradient(135deg,#ff758c,#ff7eb3)"),
                ("export", "Export Data", "📦", "linear-gradient(135deg,#43cea2,#185a9d)"),
                ("help", "Help & Tips", "💡", "linear-gradient(135deg,#56ab2f,#a8e063)")
            ]
            for col, (key, subtitle, icon, bg) in zip(cols, cards):
                with col:
                    feature_card(key, subtitle, icon, bg, key)

            action = st.session_state.get("dashboard_action", None)

            functions = st.session_state.get("functions", [])
            rows = [{
                "File": f.get("file", "N/A"),
                "Function": f.get("name", "N/A"),
                "Docstring": "OK" if f.get("docstring") else "FIX"
            } for f in functions]
            df = pd.DataFrame(rows) if rows else pd.DataFrame(columns=["File", "Function", "Docstring"])

            # Handle dashboard actions
            if action == "export":
                st.subheader("📦 Export Summary")
                st.dataframe(df, use_container_width=True)
                c1, c2 = st.columns(2)
                with c1:
                    st.download_button("📥 Export JSON", json.dumps(rows, indent=4),
                                       "analysis_export.json", "application/json", use_container_width=True)
                with c2:
                    st.download_button("📥 Export CSV", df.to_csv(index=False),
                                       "analysis_export.csv", "text/csv", use_container_width=True)
            elif action == "filter":
                st.subheader("⚙️ Advanced Filters")
                status = st.selectbox("Docstring Status", ["ALL", "Yes", "No"])
                mapping = {"Yes": "OK", "No": "FIX"}
                df_filtered = df if status=="ALL" else df[df["Docstring"]==mapping[status]]
                st.dataframe(df_filtered, use_container_width=True)
            elif action == "search":
                st.subheader("🔍 Search")
                q = st.text_input("Search function or file")
                df_filtered = df if not q else df[
                    df["Function"].str.contains(q, case=False, na=False) |
                    df["File"].str.contains(q, case=False, na=False)
                ]
                st.dataframe(df_filtered, use_container_width=True)
            elif action == "help":
                st.subheader("ℹ️ Help & Tips")
                st.info(
                    "📊 Coverage Metrics\n"
            "- Coverage % = (Documented / Total) × 100\n"
            "- 🟢 Green ≥ 90%\n"
            "- 🟡 Yellow 70–89%\n"
            "- 🔴 Red < 70%"
                )
                st.warning(
                    "✅ Function Status\n"
            "- 🟢 Complete docstring\n"
            "- ❌ Missing / incomplete\n"
            "- Auto style detection"
                )
                st.success(
                    "🧪 Test Results\n"
            "- Real-time execution\n"
            "- Pass / Fail ratio\n"
            "- Pytest integration"
                )
                st.info(
            "📝 Docstring Styles\n"
            "- Google\n"
            "- NumPy\n"
            "- REST / reST\n"
            "- Auto validation"
        )
else:
        st.info("👆 Select a dashboard card above")


    # ---------------- LOAD PYTEST REPORT ----------------
    
report_path = "storage/reports/pytest_results.json"
if Path(report_path).exists():
            with open(report_path, "r") as f:
                report = json.load(f)
            tests = report.get("tests", [])

            my_test_files = [
                "test_coverage_reporter.py",
                "test_dashboard.py",
                "test_generator.py",
                "test_llm_integration.py",
                "test_parser.py",
                "test_validator.py"
            ]

            module_stats = {f: {"passed": 0, "failed": 0} for f in my_test_files}
            for t in tests:
                file_name = Path(t["nodeid"].split("::")[0]).name
                if file_name in my_test_files:
                    status = t["outcome"]
                    module_stats[file_name][status] += 1

            df_chart = pd.DataFrame([{
                "Module": f.replace("test_", "").replace(".py", "").title(),
                "Passed": v["passed"],
                "Failed": v["failed"]
            } for f, v in module_stats.items()])

            if not df_chart.empty:
                # Metrics cards
                total_tests = len(tests)
                passed = sum(1 for t in tests if t["outcome"] == "passed")
                failed = sum(1 for t in tests if t["outcome"] == "failed")
                c1, c2, c3 = st.columns(3)

                def metric_card(title, value, color):
                    st.markdown(f"""
                    <div style="
                        background:{color};
                        padding:22px;border-radius:16px;
                        color:white;text-align:center;
                        box-shadow:0 8px 20px rgba(0,0,0,0.4)">
                        <div style="font-size:14px;opacity:0.85">{title}</div>
                        <div style="font-size:32px;font-weight:700">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with c1: metric_card("Total Tests", total_tests, "#374151")
                with c2: metric_card("Passed", passed, "#16a34a")
                with c3: metric_card("Failed", failed, "#dc2626")

                st.markdown("<br>", unsafe_allow_html=True)

                # Bar chart
                st.subheader("📈 Test Results")
                fig = px.bar(
                    df_chart,
                    x="Module",
                    y=["Passed", "Failed"],
                    barmode="group",
                    color_discrete_sequence=["#3b82f6", "#ef4444"]
                )
                fig.update_layout(
                    height=420,
                    plot_bgcolor="#0f172a",
                    paper_bgcolor="#0f172a",
                    font_color="white",
                    legend_title_text="Status"
                )
                st.plotly_chart(fig, use_container_width=True)

                # Detailed results table
                st.subheader("📋 Detailed Results")
                st.dataframe(df_chart, use_container_width=True)
else:
            st.warning("⚠️ Pytest report not found. Run pytest first.")

