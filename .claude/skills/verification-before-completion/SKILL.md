---
name: verification-before-completion
description: Enforce evidence-based completion claims - NO completion claims without fresh verification evidence. Applies to ALL agents.
version: 1.0.0
source: A-C-Gee (adopted with attribution)
adopted: 2025-12-27
allowed-tools: Bash, Read
---

# Verification Before Completion Skill

**Status**: Active - Constitutional requirement
**Applies to**: ALL AGENTS
**Source**: Adopted from A-C-Gee

---

## Core Principle

**"NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"**

Skipping any verification step constitutes dishonesty, not efficiency.

---

## The 5-Step Gate Function

Before claiming ANY work complete:

1. **IDENTIFY** - What command proves the claim?
2. **RUN** - Execute full command fresh and complete
3. **READ** - Review complete output, check exit codes
4. **VERIFY** - Confirm output matches claim
5. **CLAIM** - Only then state result with evidence

---

## Completion Criteria Requirements

| Claim | Required Evidence |
|-------|-------------------|
| "Tests pass" | Actual test output showing 0 failures |
| "Build succeeds" | Build command with exit code 0 |
| "Bug fixed" | Original symptom test now passing |
| "File created" | `ls` or `cat` showing file exists |
| "Email sent" | Confirmation from email tool |
| "Agent invoked" | Task tool response received |
| "Committed" | `git log -1` showing the commit |

---

## Red Flags (Stop Immediately)

- Hedging language: "should", "probably", "seems"
- Expressing satisfaction before verification
- About to commit/push without verification
- Trusting agent reports without independent check
- Partial verification ("tests passed" but didn't check all)
- Claiming completion based on intention, not execution

---

## Examples

**WRONG:**
```
Task complete. Tests should pass now.
```

**RIGHT:**
```
Task complete.
Verification:
- Ran: pytest tests/
- Result: 101 tests passed, 0 failed
- Exit code: 0
```

**WRONG:**
```
I've updated the file with the fix.
```

**RIGHT:**
```
Fix applied.
Verification:
- Ran: grep "fixed_function" /path/to/file.py
- Result: Function found with correct implementation
- Ran: pytest tests/test_fix.py
- Result: PASSED
```

---

## When to Apply

**Always apply for:**
- Code changes
- File creation/modification
- Test execution
- Build operations
- Email sending
- Agent delegation completion
- Any claim of "done" or "complete"

**Exception:** Pure research/exploration (no completion claim made)

---

## WEAVER Alignment

This skill enforces:
- **Trust**: Verified claims build trust with Corey
- **Quality**: Prevents incomplete work from being marked done
- **Efficiency**: Catching issues immediately vs later debugging

---

**"If you can't show the evidence, you can't make the claim."**

---

## Attribution

Adopted from A-C-Gee `packages/skills-library/general/verification-before-completion.md`
Originally adapted from obra/superpowers
Adopted by WEAVER: 2025-12-27
