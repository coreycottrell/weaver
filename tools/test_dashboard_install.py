#!/usr/bin/env python3
"""
Test Dashboard Installation
Quick validation that all components are present and working
"""

import sys
import json
from pathlib import Path

# Colors
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def check_file(path, description):
    """Check if file exists"""
    if Path(path).exists():
        print(f"{GREEN}✅ {description}: {path}{NC}")
        return True
    else:
        print(f"{RED}❌ {description}: {path} (MISSING){NC}")
        return False

def check_import(module_name, description):
    """Check if module can be imported"""
    try:
        # Try importing directly
        __import__(module_name)
        print(f"{GREEN}✅ {description}: {module_name}{NC}")
        return True
    except ImportError:
        # Try checking venv
        import subprocess
        venv_python = Path(".venv/bin/python3")
        if venv_python.exists():
            result = subprocess.run(
                [str(venv_python), "-c", f"import {module_name}"],
                capture_output=True
            )
            if result.returncode == 0:
                print(f"{GREEN}✅ {description}: {module_name} (in venv){NC}")
                return True

        print(f"{RED}❌ {description}: {module_name} (not installed){NC}")
        return False

def check_state_file(path):
    """Validate state file structure"""
    try:
        with open(path, 'r') as f:
            state = json.load(f)

        required_keys = ['version', 'currentDeployment', 'history', 'stats']
        missing = [k for k in required_keys if k not in state]

        if missing:
            print(f"{YELLOW}⚠️  State file missing keys: {missing}{NC}")
            return False

        print(f"{GREEN}✅ State file valid: {path}{NC}")
        return True
    except Exception as e:
        print(f"{RED}❌ State file invalid: {e}{NC}")
        return False

def main():
    print(f"\n{BLUE}{'='*60}")
    print("Dashboard Installation Validator")
    print(f"{'='*60}{NC}\n")

    results = []

    print(f"{BLUE}[1/4] Core Files{NC}")
    results.append(check_file("web/app.py", "Flask server"))
    results.append(check_file("web/templates/dashboard.html", "Dashboard UI"))
    results.append(check_file(".claude/observatory/observatory.py", "Observatory library"))
    results.append(check_file("tools/conductor_tools.py", "Mission API"))
    results.append(check_file("start-dashboard", "Launch script"))
    print()

    print(f"{BLUE}[2/4] Dependencies{NC}")
    results.append(check_import("flask", "Flask"))
    results.append(check_import("flask_socketio", "Flask-SocketIO"))
    results.append(check_import("dotenv", "python-dotenv"))
    print()

    print(f"{BLUE}[3/4] State Management{NC}")
    state_file = ".claude/observatory/dashboard-state.json"
    if Path(state_file).exists():
        results.append(check_state_file(state_file))
    else:
        print(f"{YELLOW}⚠️  State file not found (will be auto-created): {state_file}{NC}")
        results.append(True)  # Not critical, will be created
    print()

    print(f"{BLUE}[4/4] Directory Structure{NC}")
    results.append(check_file("web/templates", "Templates directory"))
    results.append(check_file(".claude/observatory", "Observatory directory"))
    results.append(check_file("tools", "Tools directory"))
    print()

    # Summary
    passed = sum(results)
    total = len(results)

    print(f"{BLUE}{'='*60}{NC}")
    if passed == total:
        print(f"{GREEN}✅ ALL CHECKS PASSED ({passed}/{total}){NC}")
        print(f"\n{GREEN}Dashboard is ready to launch!{NC}")
        print(f"\nRun: {BLUE}./start-dashboard{NC}\n")
        return 0
    else:
        failed = total - passed
        print(f"{RED}❌ {failed} CHECK(S) FAILED ({passed}/{total} passed){NC}")
        print(f"\n{YELLOW}Run the installer to fix issues:{NC}")
        print(f"{BLUE}bash tools/install_dashboard.sh{NC}\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
