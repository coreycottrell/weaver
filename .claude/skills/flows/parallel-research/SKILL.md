---
name: parallel-research
description: Launch multiple agents to investigate a topic simultaneously from different angles
version: 1.0.0
source: AI-CIV/WEAVER
allowed-tools: [Task, Read, Grep, Glob, WebSearch, WebFetch]
agents-required: [2-6 specialist agents]
portability: cross-civ
status: VALIDATED
---

# Parallel Research Flow

Deploy multiple specialist agents to investigate a topic simultaneously. Each brings their domain lens. Results synthesized at end.

## When to Use

- Exploring new technology or concept
- Investigating a bug or issue from multiple angles
- Research before major decisions
- Gathering comprehensive context quickly

## Agent Selection Guide

Choose 2-6 agents based on the research domain:

| Domain | Recommended Agents |
|--------|-------------------|
| Security | security-auditor, code-archaeologist, pattern-detector |
| Architecture | pattern-detector, api-architect, code-archaeologist |
| Performance | performance-optimizer, pattern-detector, test-architect |
| Integration | integration-auditor, api-architect, doc-synthesizer |
| User-facing | feature-designer, doc-synthesizer, web-researcher |
| External research | web-researcher, doc-synthesizer, pattern-detector |

## Procedure

### Step 1: Define Research Question

```
RESEARCH QUESTION: [Clear, specific question]
SCOPE: [Boundaries - what's in/out]
OUTPUT NEEDED: [What format/depth of answer]
```

### Step 2: Select Agents (2-6)

Choose agents whose domains intersect with the question. More agents = broader coverage but more synthesis work.

### Step 3: Launch in Parallel

Use Task tool with `run_in_background: true` for all agents simultaneously:

```
For each agent, provide:

PARALLEL RESEARCH TASK

Question: [The research question]
Your Lens: [What aspect to focus on given your domain]
Scope: [Boundaries]

YOUR TASK:
1. Search relevant files/resources from your perspective
2. Document key findings
3. Note uncertainties or areas needing deeper investigation
4. Provide actionable insights

OUTPUT FORMAT:
## [Agent Name] Findings

### Key Discoveries
- [Bullet points]

### Evidence
- [File paths, URLs, or sources]

### Uncertainties
- [What remains unclear]

### Recommendations
- [Actionable next steps from your lens]
```

### Step 4: Collect Results

Wait for all agents to complete (use TaskOutput with block: true).

### Step 5: Synthesize

Either manually or via result-synthesizer:

```
SYNTHESIS TASK

You have received findings from [N] agents investigating:
[Research question]

YOUR TASK:
1. Identify CONVERGENT findings (multiple agents agree)
2. Identify DIVERGENT findings (agents disagree)
3. Note UNIQUE insights (only one agent found)
4. Compile actionable recommendations
5. Flag remaining unknowns

OUTPUT: Unified research summary with confidence levels
```

## Example Invocation

```
Research Question: "How does the authentication system work?"

Agents:
- security-auditor (security implications)
- code-archaeologist (historical evolution)
- pattern-detector (architectural patterns)

[Launch all 3 in parallel]
[Collect results]
[Synthesize into unified answer]
```

## Anti-Patterns

- **Too many agents**: More than 6 creates synthesis overhead
- **Wrong agents**: Match agents to domain, not just quantity
- **Vague question**: Specific questions get specific answers
- **Skipping synthesis**: Raw findings without synthesis = information, not knowledge

## Success Indicators

- All agents return findings within scope
- Synthesis identifies both agreements and productive disagreements
- Actionable recommendations emerge
- Research question answered with evidence

## Portability Notes

This flow works on any CIV node that has:
- Task tool for parallel agent invocation
- At least 2 specialist agents
- result-synthesizer or equivalent for synthesis

Agent names may vary across CIVs - adapt to local agent registry.

---

**Source**: WEAVER collective coordination patterns
**Validated**: October 2025 (multiple successful uses)
