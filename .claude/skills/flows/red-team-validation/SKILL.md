---
name: red-team-validation
description: Adversarial testing of proposals, code, or decisions before acceptance
version: 1.0.0
source: AI-CIV/WEAVER
allowed-tools: [Task, Read, Grep, Glob, Bash]
agents-required: [security-auditor, pattern-detector, test-architect]
portability: cross-civ
status: VALIDATED
---

# Red Team Validation Flow

Adversarial credibility assessment. Before accepting any proposal, code, or external package - attack it. Find weaknesses. Only what survives becomes trusted.

## When to Use

- Evaluating external packages or code
- Reviewing security-critical changes
- Testing architectural proposals
- Validating claims before acting on them
- Any high-stakes decision

## Core Principle

**Trust Through Adversity**: We don't trust because something looks good. We trust because it survived our best attempts to break it.

## Procedure

### Step 1: Define the Target

```
RED TEAM TARGET

Subject: [What we're validating]
Claims: [What it claims to do/be]
Stakes: [Why this matters - what's at risk]
Scope: [Boundaries of validation]
```

### Step 2: Assemble Red Team

Select agents whose domains can find weaknesses:

| Validation Type | Red Team Composition |
|-----------------|---------------------|
| Security | security-auditor (lead), pattern-detector, code-archaeologist |
| Architecture | pattern-detector (lead), api-architect, performance-optimizer |
| External Package | security-auditor, integration-auditor, code-archaeologist |
| Business Logic | test-architect (lead), pattern-detector, conflict-resolver |

### Step 3: Attack Phase (Parallel)

Each red team member attempts to break the target:

```
RED TEAM ATTACK

Target: [The subject]
Your Mission: Find weaknesses from your domain expertise

ATTACK VECTORS TO EXPLORE:
1. What could go wrong?
2. What assumptions might be false?
3. What edge cases aren't handled?
4. What dependencies could fail?
5. What's missing that should be there?
6. How could this be misused?

OUTPUT FORMAT:
## [Agent Name] Attack Report

### Vulnerabilities Found
- [Severity: CRITICAL/HIGH/MEDIUM/LOW]
  [Description]
  [Evidence/location]
  [Potential impact]

### Suspicious Patterns
- [Things that seem off but aren't proven vulnerabilities]

### Missing Elements
- [What should exist but doesn't]

### Attack Summary
- Total vulnerabilities: [count by severity]
- Recommendation: REJECT / ACCEPT WITH FIXES / ACCEPT
```

### Step 4: Aggregate Findings

Collect all attack reports and compile:

```
RED TEAM SUMMARY

Target: [Subject]
Red Team: [List of agents]
Date: [ISO date]

## Vulnerability Matrix

| ID | Severity | Finder | Description | Status |
|----|----------|--------|-------------|--------|
| V1 | CRITICAL | security-auditor | [desc] | OPEN |
| V2 | HIGH | pattern-detector | [desc] | OPEN |
...

## Aggregate Assessment

Critical: [count]
High: [count]
Medium: [count]
Low: [count]

## Verdict

[ ] REJECT - Critical flaws, do not use
[ ] ACCEPT WITH MANDATORY FIXES - Fixable issues before use
[ ] ACCEPT WITH ADVISORY - Minor issues, document for awareness
[ ] ACCEPT - Passed validation

## Required Actions Before Acceptance
1. [Action item]
2. [Action item]
...
```

### Step 5: Remediation (if applicable)

If verdict is "ACCEPT WITH FIXES":
1. Address each required action
2. Re-run red team on fixed version
3. Repeat until ACCEPT or REJECT

## Example: External Package Validation

```
Target: A-C-Gee skills-library package
Stakes: Will be integrated into our collective

Red Team:
- security-auditor: Check for malicious patterns
- integration-auditor: Verify integration requirements
- pattern-detector: Assess architectural fit

Results:
- 0 CRITICAL, 2 HIGH, 5 MEDIUM
- Verdict: ACCEPT WITH MANDATORY FIXES
- Required: Document dependencies, add validation tests

After fixes: ACCEPT with 87/100 confidence score
```

## Scoring Guide (Optional)

For quantitative assessment:

```
CONFIDENCE SCORE CALCULATION

Base: 100 points

Deductions:
- CRITICAL vulnerability: -30 points each
- HIGH vulnerability: -15 points each
- MEDIUM vulnerability: -5 points each
- LOW vulnerability: -2 points each
- Missing documentation: -10 points
- No tests: -15 points
- Unclear provenance: -10 points

Final Score: [X]/100
Threshold for acceptance: 70/100
```

## Anti-Patterns

- **Friendly validation**: Red team must WANT to find problems
- **Single perspective**: Always use 2+ agents with different lenses
- **Rushing**: Thorough attacks take time
- **Accepting despite CRITICAL**: Never accept with unresolved critical issues
- **Skipping re-validation**: Fixed code needs fresh attack

## Success Indicators

- Vulnerabilities found that weren't obvious
- Clear severity classification
- Actionable remediation steps
- Documented decision trail
- High-confidence final verdict

## Portability Notes

Works on any CIV with:
- Security-focused agent (security-auditor equivalent)
- Pattern recognition agent
- At least one domain specialist relevant to target

The adversarial mindset is the constant. Agent names adapt to local registry.

---

**Source**: WEAVER package validation methodology
**Validated**: December 2025 (A-C-Gee package assessment)
