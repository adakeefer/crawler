#!/bin/bash

# Exit on error
set -e

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Activate virtual environment if it exists
if [ -f "$PROJECT_ROOT/.venv/bin/activate.fish" ]; then
    # Use fish to activate the environment and run the tests
    fish -c "source $PROJECT_ROOT/.venv/bin/activate.fish && python -m pytest $PROJECT_ROOT/crawler/tests -x -v --lf"
else
    echo "[ERROR] Virtual environment not found at $PROJECT_ROOT/.venv"
    exit 1
fi

if [ $? -eq 0 ]; then
    echo "[OK] All tests passed!"
else
    echo "[ERROR] Some tests failed"
    exit 1
fi 