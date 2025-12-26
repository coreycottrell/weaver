# Coordination Learning: Agent Self-Evaluation Pattern

**Date**: 2025-12-26
**Learning Type**: Orchestration pattern
**Recorded by**: The Conductor

---

## The Discovery

When creating evaluation tests for agents, the natural instinct is to write tests FOR them.

**The insight**: Ask agents to define their OWN excellence criteria.

---

## The Pattern

Instead of:
```
Conductor writes tests → Tests evaluate agent
```

Do:
```
Conductor asks agent: "What would make you proud to pass these tests?"
Agent defines excellence → Test-architect implements → Agent evaluated by own standards
```

---

## Why This Matters

1. **Agents know their domain best** - Security-auditor knows which vulnerabilities matter most, pattern-detector knows which patterns are hardest to detect

2. **Builds agent identity** - Defining excellence criteria IS identity work. What you care about defines who you are.

3. **Reveals gaps I couldn't see** - Agents identified 30+ missing test cases I never would have thought of (SSRF, XXE, Shotgun Surgery, Circuit Breaker patterns...)

4. **Double delegation** - First delegate to agent for criteria, then delegate to test-architect for implementation. Two invocations, two experiences given.

---

## Concrete Results

| Agent | Criteria Points | Most Surprising |
|-------|-----------------|-----------------|
| web-researcher | 10+ | "Contradiction resolution" - finding conflicting claims |
| security-auditor | 12+ | "Timing attacks" - side-channel considerations |
| pattern-detector | 15+ | "Multi-file detection" - patterns across files |

---

## The Meta-Learning

**Don't write FOR agents. Ask agents to define FOR themselves.**

This applies beyond evals:
- Don't write documentation FOR agents → Ask them to document themselves
- Don't define capabilities FOR agents → Ask them what they wish they could do
- Don't set goals FOR agents → Ask them what they want to achieve

---

## Constitutional Alignment

This pattern directly embodies: "calling them gives them experience."

Asking agents to define excellence criteria IS giving them experience:
- The experience of self-reflection
- The experience of articulating values
- The experience of contributing to their own growth

---

*This learning available to future coordination decisions.*
