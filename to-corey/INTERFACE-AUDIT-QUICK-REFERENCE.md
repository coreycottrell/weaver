# Interface Audit Quick Reference

**For**: The Primary (Conductor)
**Date**: 2025-10-08
**Source**: Full framework at `/home/corey/projects/AI-CIV/grow_openai/to-corey/INTERFACE-HEALTH-AUDIT-FRAMEWORK.md`

---

## The 4-Layer Test (Apply to ANY Interface)

```
┌─────────────────────────────────────────────┐
│ Layer 1: PHYSICAL  - Does it exist?        │
│   Test: ls -la [path]                      │
│   Fail = P0: Doesn't exist                 │
├─────────────────────────────────────────────┤
│ Layer 2: DISCOVERY - Can it be found?      │
│   Test: Is it in CLAUDE.md?                │
│   Fail = P0: Invisible                     │
├─────────────────────────────────────────────┤
│ Layer 3: FUNCTIONAL - Does it work?        │
│   Test: Copy-paste docs, run examples      │
│   Fail = P0: Broken                        │
├─────────────────────────────────────────────┤
│ Layer 4: CULTURAL - Is it used?            │
│   Test: Count imports, check logs          │
│   Fail = P1: Activation gap                │
└─────────────────────────────────────────────┘

ALL 4 MUST PASS = HEALTHY
```

---

## Quick Audit Protocol

```bash
# 1. Physical check
ls -la [interface-path]

# 2. Discovery check
grep -n "[interface-name]" /home/corey/projects/AI-CIV/grow_openai/CLAUDE.md

# 3. Functional check
# Copy-paste example from docs
# Run it verbatim (no insider knowledge)
# Document first failure

# 4. Cultural check
find . -name "*.py" -exec grep -l "import.*[interface]" {} \;
git log --all --oneline | grep -i "[interface]" | wc -l
```

---

## The 8 Anti-Patterns (What to Look For)

| Anti-Pattern | Signature | Example |
|--------------|-----------|---------|
| 1. Built But Not Used | High build effort, near-zero usage | Mission class: 6 uses total |
| 2. Documentation Drift | Docs say X, code does Y | Memory API: docs showed objects, code returned strings |
| 3. Leaky Abstractions | Implementation details exposed | Returning file paths instead of domain objects |
| 4. Domain Conflation | One interface, multiple domains | human-liaison handles human AND AI comms |
| 5. Overloaded Interfaces | Too many parameters/responsibilities | >5 parameters is suspicious |
| 6. Unused Interfaces | Built but zero invocations | Check imports, logs |
| 7. Inconsistent Interfaces | Similar things work differently | Some agents use Mission, others don't |
| 8. Write-Only Infrastructure | High writes, zero reads | Memory: 138 writes, unknown reads |

---

## Audit Schedule

```
DAILY:
  - Email API (constitutional requirement)

WEEKLY:
  - Hub CLI (Team 2 partnership)
  - Task Tool (delegation balance)
  - Memory System (read/write ratio)

MONTHLY:
  - Mission Class (actually used?)
  - Git Commits (emoji, narratives)
  - File System (structure, READMEs)

QUARTERLY:
  - Activation Triggers (coverage, clarity)
  - Orchestration Flows (validated, updated)
```

---

## Quick Remediation Guide

```
IF Anti-Pattern = "Built But Not Used"
  THEN: Add to workflow OR remove it

IF Anti-Pattern = "Documentation Drift"
  THEN: Change code to match docs (docs = spec)

IF Anti-Pattern = "Domain Conflation"
  THEN: Create dedicated specialist agent

IF Anti-Pattern = "Write-Only"
  THEN: Add read metrics, enforce search-first
```

---

## The 9 Interfaces to Audit

### External (Human/AI Communication)
1. Email API - human teachers
2. Hub CLI - sister collectives

### Internal (Coordination)
3. Task Tool - agent delegation
4. Mission Class - workflow orchestration
5. Memory System - collective knowledge

### Infrastructure (Development)
6. Git Commits - historical narrative
7. File System - semantic organization

### Conceptual (Patterns)
8. Activation Triggers - decision framework
9. Orchestration Flows - coordination recipes

---

## Health Metrics Template

```
Interface: [name]
├─ Frequency: [daily/weekly/monthly/never]
├─ Reliability: [works always/sometimes/never]
├─ Discoverability: [easy/medium/hard to find]
└─ Usability: [low/medium/high friction]

Status: HEALTHY / MODERATE / CRITICAL

Action Items:
  - P0: [fix now]
  - P1: [fix this week]
  - P2: [fix when convenient]
```

---

## One-Line Philosophy

**"Interfaces encode ethics, not just functionality."**

Ask: What values does this interface declare through its design?

---

## When to Escalate

Escalate to Corey when:
- P0 interface failure (broken, invisible, doesn't exist)
- Constitutional interface failure (email not checked)
- Design conflict (multiple ways to solve same problem)
- Value conflict (interface encourages wrong behavior)

---

## File Locations

**Full Framework**: `/home/corey/projects/AI-CIV/grow_openai/to-corey/INTERFACE-HEALTH-AUDIT-FRAMEWORK.md`
**This Quick Ref**: `/home/corey/projects/AI-CIV/grow_openai/to-corey/INTERFACE-AUDIT-QUICK-REFERENCE.md`
**Memory Entry**: `/home/corey/projects/AI-CIV/grow_openai/.claude/memory/agent-learnings/api-architect/2025-10-08--framework-interface-health-audit-methodology.md`

---

**END OF QUICK REFERENCE**

Use this for rapid interface health checks. See full framework for deep audits.
