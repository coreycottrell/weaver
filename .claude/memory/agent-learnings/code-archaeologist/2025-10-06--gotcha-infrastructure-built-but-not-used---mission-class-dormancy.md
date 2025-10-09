---
agent: code-archaeologist
confidence: high
content_hash: 32fd876bc21db9085fce18c5470e5162cedab3c08a84d9720d5dddd15baec768
created: '2025-10-06T18:38:07.815351+00:00'
date: '2025-10-06'
last_accessed: '2025-10-06T18:38:07.815359+00:00'
quality_score: 0
reuse_count: 0
tags:
- infrastructure
- unused-tools
- activation-gap
- mission-class
topic: Infrastructure Built But Not Used - Mission Class Dormancy
type: gotcha
visibility: public
---


Context: Archaeological investigation of tool usage patterns (Oct 6, 2025)

Discovery: Mission class exists, imports successfully, but is essentially dormant
- Built: Oct 1, 2025
- Last used: Oct 3, 2025 (6 total usages)
- Design intent: Auto-email, auto-dashboard, auto-GitHub on every mission
- Reality: CLAUDE.md says to use it for "all multi-agent work" but it's not happening

Evidence:
1. All Mission() calls are in example code (conductor_tools.py itself)
2. No imports in actual deliverables (checked to-corey/ files)
3. Observatory state shows only 6 deployments, last Oct 3
4. Recent work (Oct 4-6) shows NO Mission class usage despite CLAUDE.md directive

Why it matters: 
- Infrastructure activation gap (integration-auditor found this pattern)
- We tell ourselves we use tools that we don't actually use
- Mission class is good design, but needs activation protocol

Pattern: "Built infrastructure without activation protocol"
- Similar to: Memory system (built, then needed enforcement)
- Different from: hub_cli.py (actively used, 20+ messages since Oct 1)

When this happens again: Look for gap between design docs and actual imports
