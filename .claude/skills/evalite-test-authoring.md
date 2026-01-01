---
name: evalite-test-authoring
description: Systematic AI output quality measurement using the Evalite framework for agent validation
---

# Evalite Test Authoring: AI Output Evaluation Skill

**Version**: 1.0
**Date**: 2025-12-14
**Created from**: AI Hero repository analysis (Corey directive: "all AICIVs grok this")
**Purpose**: Enable systematic AI output quality measurement using the Evalite framework
**Status**: Active

---

## When to Use This Skill

**Trigger scenarios:**
- Validating agent output quality (tester agent)
- Creating quality gates for agent workflows
- Measuring prompt effectiveness across iterations
- Building regression tests for AI behavior
- Establishing baseline scores for agent capabilities
- CI/CD integration for AI quality metrics

**This skill is MANDATORY for:**
- tester agent quality validation tasks
- reviewer and reviewer-audit quality scoring
- Any systematic AI output evaluation
- Pre-deployment quality gates

---

## The Core Problem This Solves

**What A-C-Gee lacks:**
1. Systematic AI output quality measurement
2. Regression detection when prompts change
3. Objective scoring (not just "looks good")
4. CI/CD integration for quality gates
5. Evidence-based quality claims

**What Evalite provides:**
1. `.eval.ts` files - test files specifically for AI outputs
2. Multiple scorer types (exact match, semantic, LLM-as-judge)
3. Threshold-based pass/fail criteria
4. Local UI for exploring outputs and traces
5. CI/CD integration with score thresholds

---

## The Golden Rule

**"If you can't measure it, you can't improve it."**

```typescript
// WRONG: Subjective assessment
// "The agent response looks good"

// RIGHT: Measured evaluation
evalite("Agent response quality", {
  data: () => testCases,
  task: async (input) => agentTask(input),
  scorers: [Factuality, Levenshtein],
  threshold: 0.8,  // Explicit pass/fail
});
```

---

## Evalite Framework Reference

### What is Evalite?

Evalite is an AI evaluation framework where **".eval.ts is the new .test.ts"**:
- Built on Vitest (familiar testing patterns)
- LLM-agnostic (works with any AI provider)
- Local development UI for exploration
- CI/CD ready with threshold-based failures

**Source**: https://evalite.dev

### Installation

```bash
# Install Evalite and dependencies
pnpm add -D evalite

# Required peer dependencies
pnpm add -D vitest

# Optional: AI SDK for task implementation
pnpm add ai @ai-sdk/anthropic
```

---

## The 5-Step Evaluation Process

### Step 1: Define Test Dataset

```typescript
// evals/datasets/agent-outputs.ts
export const emailTestCases = [
  {
    input: {
      task: "Draft email to Corey about session summary",
      context: "Completed 3 tasks, 1 blocker"
    },
    expected: {
      contains: ["Session Summary", "Completed", "Blocker"],
      tone: "professional",
      length: { min: 200, max: 1000 }
    }
  }
];
```

### Step 2: Write Scorer Functions

```typescript
// evals/scorers/acgee-scorers.ts
import { createScorer } from "evalite";

export const EmailStructure = createScorer<string, { contains: string[] }>({
  name: "EmailStructure",
  description: "Validates email contains required elements",
  scorer: async ({ output, expected }) => {
    const content = output.toLowerCase();
    const required = expected.contains || [];

    let found = 0;
    for (const element of required) {
      if (content.includes(element.toLowerCase())) found++;
    }

    return {
      score: required.length > 0 ? found / required.length : 1,
      metadata: { found, total: required.length }
    };
  }
});

export const DelegationQuality = createScorer({
  name: "DelegationQuality",
  description: "Validates delegation contains essential elements",
  scorer: async ({ output, expected }) => {
    const content = output.toLowerCase();
    let score = 0, total = 0;

    if (expected.hasSuccessCriteria) {
      total++;
      if (content.includes("success") || content.includes("criteria")) score++;
    }
    if (expected.specifiesScope) {
      total++;
      if (content.includes("scope") || content.includes("in:")) score++;
    }
    if (expected.includesHandoff) {
      total++;
      if (content.includes("handoff") || content.includes("then")) score++;
    }

    return { score: total > 0 ? score / total : 1 };
  }
});
```

### Step 3: Write Evaluation Files

```typescript
// evals/email-quality.eval.ts
import { evalite } from "evalite";
import { EmailStructure } from "./scorers/acgee-scorers";
import { emailTestCases } from "./datasets/agent-outputs";

evalite("Email Generation Quality", {
  data: () => emailTestCases,
  task: async (input) => generateEmail(input.task, input.context),
  scorers: [EmailStructure],
  threshold: 0.75,
});
```

### Step 4: Run Evaluations

```bash
# Run all evaluations
npx evalite

# Watch mode
npx evalite --watch

# Open local UI
npx evalite ui
```

### Step 5: CI/CD Integration

```yaml
# .github/workflows/ai-quality.yml
- name: Run Evalite evaluations
  run: npx evalite --ci
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

---

## Scorer Selection Guide

| Scorer Type | Use When | Example |
|-------------|----------|---------|
| **Levenshtein** | Exact string similarity | Code generation |
| **Factuality** | Facts must be accurate | Research outputs |
| **LLM-as-Judge** | Subjective quality | Emails, tone |
| **Custom Rules** | Domain-specific | Delegation quality |

---

## A-C-Gee Specific Patterns

**Email agent:** `scorers: [EmailStructure, ToneAppropriate]`, threshold: 0.8
**Coder agent:** `scorers: [Factuality, CodeCompleteness]`, threshold: 0.85
**Delegation quality:** `scorers: [DelegationQuality]`, threshold: 0.9

---

## Pre-Evaluation Checklist

- [ ] Test dataset has 5+ cases per evaluation
- [ ] Expected outputs are measurable
- [ ] Thresholds are reasonable (0.75-0.9)
- [ ] Error handling in task functions
- [ ] API keys configured for LLM scorers

---

## Success Criteria

**Using correctly if:**
- Quality claims include numeric scores
- Regressions detected before production
- CI fails on threshold violations
- Test datasets grow with capabilities

**NOT using correctly if:**
- Quality is "looks good" without scores
- No baseline comparison
- Evaluations run manually only

---

## Related Resources

- https://evalite.dev - Official documentation
- https://github.com/ai-hero-dev/ai-hero - Source patterns
- `.claude/agents/tester.md` - Tester agent manifest

---

**Remember: "If you can't measure it, you can't improve it."**
