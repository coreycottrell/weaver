#!/usr/bin/env python3
"""
Test dashboard rendering with mock active deployment
"""

import sys
import time
from observatory import start_deployment, update_agent_status, log_agent_activity
from dashboard import render_dashboard
from rich.console import Console

# Create mock active deployment
print("Creating mock active deployment...")
dep_id = start_deployment(
    "Meta-analysis of AI-CIV Collective architecture",
    ["code-archaeologist", "pattern-detector", "doc-synthesizer"]
)
print(f"✓ Created deployment: {dep_id}")

# Simulate agent progress
print("\nSimulating agent activity...")

# Agent 1: code-archaeologist
update_agent_status("code-archaeologist", "working", 33, "Analyzing file structure")
time.sleep(0.5)
log_agent_activity("code-archaeologist", "Found 4 core layers")
update_agent_status("code-archaeologist", "working", 67, "Mapping dependencies")
time.sleep(0.5)
update_agent_status("code-archaeologist", "completed", 100, "Analysis complete")

# Agent 2: pattern-detector
update_agent_status("pattern-detector", "working", 25, "Identifying architectural patterns")
time.sleep(0.5)
update_agent_status("pattern-detector", "working", 75, "Scoring pattern quality")

# Agent 3: doc-synthesizer
update_agent_status("doc-synthesizer", "working", 10, "Reading documentation files")

print("✓ Mock deployment active with 3 agents in various states")

# Render dashboard once
print("\nRendering dashboard...\n")
console = Console()
console.print(render_dashboard())

print("\n✅ Dashboard test complete!")
print("\nTo view live dashboard, run:")
print("  .venv/bin/python .claude/observatory/dashboard.py")
