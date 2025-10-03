#!/bin/bash
# Quick Start Script for Memory System
# Demonstrates basic operations

set -e

echo "============================================================"
echo "AI-CIV MEMORY SYSTEM - QUICK START"
echo "============================================================"

# Change to tools directory
cd "$(dirname "$0")"

echo ""
echo "1️⃣  Running integration tests..."
python3 test_memory_integration.py

echo ""
echo "2️⃣  Building search indexes..."
python3 memory_cli.py index

echo ""
echo "3️⃣  Showing system statistics..."
python3 memory_cli.py stats

echo ""
echo "4️⃣  Running agent usage example..."
python3 example_agent_memory_usage.py

echo ""
echo "============================================================"
echo "✅ QUICK START COMPLETE"
echo "============================================================"
echo ""
echo "📚 Next Steps:"
echo "   - Read MEMORY-SYSTEM-README.md for full documentation"
echo "   - Check MEMORY-SYSTEM-IMPLEMENTATION-REPORT.md for details"
echo "   - Run 'python3 memory_cli.py --help' for CLI usage"
echo ""
echo "📝 Example Commands:"
echo "   python3 memory_cli.py search \"authentication\""
echo "   python3 memory_cli.py list security-auditor"
echo "   python3 memory_cli.py scan"
echo ""
