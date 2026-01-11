# cli/commands.py
import argparse
import subprocess
import sys
from core.reporter.coverage_reporter import scan_project

def main():
    parser = argparse.ArgumentParser(prog="ai-review-cli")
    parser.add_argument("command", choices=["scan", "ui"], help="scan = update report, ui = launch streamlit UI")
    parser.add_argument("--path", "-p", default="examples", help="path to scan")
    args = parser.parse_args()

    if args.command == "scan":
        print(f"Scanning path: {args.path} ...")
        report = scan_project(parse_root=args.path)
        print("Scan complete. Metrics:", report.get("metrics", {}))
    elif args.command == "ui":
        cmd = [sys.executable, "-m", "streamlit", "run", "main_app.py"]
        subprocess.run(cmd)

if __name__ == "__main__":
    main()
