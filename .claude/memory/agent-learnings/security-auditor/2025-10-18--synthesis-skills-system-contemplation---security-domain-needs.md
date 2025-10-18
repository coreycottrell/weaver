---
agent: security-auditor
confidence: high
content_hash: ed6f920e992fb100d1a213b80206e539461232038e3dbc06fc8f14fa3064f7f9
created: '2025-10-18T17:03:59.760054+00:00'
date: '2025-10-18'
last_accessed: '2025-10-18T17:03:59.760069+00:00'
quality_score: 0
reuse_count: 0
tags:
- skills-system
- security
- automation
- vulnerability-scanning
- threat-modeling
topic: Skills system contemplation - Security domain needs
type: synthesis
visibility: public
---


Context: Corey asked all agents to contemplate new skills system and propose capabilities.

Discovery: Security domain has three core automation needs:
1. dependency-cve-scanner (HIGH priority) - Reactive prevention of known vulnerabilities
2. secret-scanner (HIGH priority) - Critical protection against credential exposure
3. threat-model-generator (MEDIUM priority) - Proactive security-by-design

Why it matters:
- These skills form complete security pipeline (design → implement → deploy)
- Address most common vulnerability classes (dependencies, secrets, design flaws)
- High automation potential (clear inputs/outputs, deterministic)
- Broad utility (6+ other agents benefit from each skill)
- Measurable impact (CVE count, secrets found, threat models generated)

When to apply:
- Use this pattern when proposing infrastructure that spans multiple lifecycle stages
- Prioritize skills with clear escalation paths (secret found → human-liaison immediately)
- Balance reactive (CVE/secrets) with proactive (threat modeling) capabilities
- Consider constitutional requirements (my activation triggers mention weekly CVE scans)

Skills voting insight:
- dependency-cve-scanner: Vote HIGH (preventive, automatable, constitutional requirement)
- secret-scanner: Vote HIGH (critical severity, low implementation cost, immediate ROI)
- threat-model-generator: Vote MEDIUM (transformative but complex, start simple and iterate)
