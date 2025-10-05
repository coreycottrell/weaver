#!/bin/bash
echo "=== FILE AUDIT - Oct 4, 2025 ==="
find . -type f \( -name "*.md" -o -name "*.py" -o -name "*.json" \) | grep -v ".git" | grep -v "__pycache__" | grep -v ".venv" | wc -l
