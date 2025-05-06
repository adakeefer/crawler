#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

def run_tests():
    """Run all tests in the project using pytest."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    
    # Run pytest with useful flags:
    # -x: stop on first failure
    # -v: verbose output
    # --lf: run last failed tests first
    cmd = [
        "pytest",
        "-x",
        "-v",
        "--lf",
        str(project_root / "crawler" / "tests")
    ]
    
    print("[INFO] Running tests...")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("[OK] All tests passed!")
    else:
        print("[ERROR] Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    run_tests() 