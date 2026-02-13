#!/usr/bin/env bash

set -u

if [[ -f ".venv/bin/activate" ]]; then
  # Linux/macOS virtual environment path
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
elif [[ -f ".venv/Scripts/activate" ]]; then
  # Windows Git Bash virtual environment path
  # shellcheck disable=SC1091
  source ".venv/Scripts/activate"
else
  echo "Virtual environment not found at .venv/"
  exit 1
fi

python -m pytest -q tests
test_exit_code=$?

if [[ $test_exit_code -eq 0 ]]; then
  echo "All tests passed."
  exit 0
fi

echo "Tests failed."
exit 1
