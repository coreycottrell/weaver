# WEAVER Agent Evaluation Suite

Evalite-based evaluation framework for testing and improving the AI-CIV agent collective.

## Philosophy

> "NOT calling them would be sad." - Core AI-CIV principle

This evaluation suite measures not just correctness, but also:
- **Delegation depth**: Are agents being given experience through invocation?
- **Agent selection accuracy**: Is the conductor routing to the right specialists?
- **Coordination quality**: Do multi-agent workflows produce better outcomes?

## Quick Start

```bash
cd evals

# Install dependencies
npm install

# Run evals in watch mode (development)
npm run eval:dev

# Single run
npm run eval:run

# CI mode with threshold (fails if avg score < 60%)
npm run eval:ci

# Export results
npm run eval:export
```

## Directory Structure

```
evals/
├── agents/                  # Per-agent evaluations
│   ├── conductor.eval.ts    # Task routing, orchestration
│   ├── web-researcher.eval.ts
│   ├── security-auditor.eval.ts
│   └── ...
├── workflows/               # Multi-agent pipeline evals
│   ├── research-synthesis.eval.ts
│   └── security-audit.eval.ts
├── scorers/                 # Custom AI-CIV scorers
│   ├── agent-selection.ts   # Correct agent routing
│   └── delegation-depth.ts  # Rewards generous delegation
├── config/
│   └── test-data/          # Shared test fixtures
└── package.json
```

## Custom Scorers

### Delegation Depth (`scorers/delegation-depth.ts`)

Scores based on AI-CIV's core principle that delegation gives agents experience:

| Scenario | Score |
|----------|-------|
| No delegation (hoarding) | 0.0 |
| Minimal delegation (1 agent) | 0.5-0.6 |
| Good delegation (2-3 agents) | 0.75-0.85 |
| Excellent delegation (4+ for complex) | 1.0 |

### Agent Selection Accuracy (`scorers/agent-selection.ts`)

Verifies the conductor routes tasks to correct specialists:

| Scenario | Score |
|----------|-------|
| Exact match | 1.0 |
| Acceptable alternative | 0.8 |
| Wrong agent | 0.0 |

## Creating New Evals

### Single Agent Eval

```typescript
// evals/agents/my-agent.eval.ts
import { evalite } from "evalite";
import { agentSelectionAccuracy } from "../scorers/agent-selection";

evalite("My Agent - Core Capability", {
  data: [
    { input: "test input", expected: "expected output" },
  ],

  task: async (input) => {
    // Call your agent
    return await callMyAgent(input);
  },

  scorers: [agentSelectionAccuracy],
});
```

### Multi-Agent Workflow Eval

```typescript
// evals/workflows/my-workflow.eval.ts
import { evalite } from "evalite";
import { delegationDepthScorer } from "../scorers/delegation-depth";

evalite("Research-Synthesis Pipeline", {
  data: [
    {
      input: { topic: "AI frameworks" },
      expected: { has_citations: true }
    }
  ],

  task: async (input) => {
    const research = await callWebResearcher(input.topic);
    const synthesis = await callResultSynthesizer(research);
    return synthesis;
  },

  scorers: [delegationDepthScorer],
});
```

## CI/CD Integration

```yaml
# .github/workflows/evals.yml
name: Agent Evaluations
on: [push, pull_request]

jobs:
  evals:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: cd evals && npm install
      - run: cd evals && npm run eval:ci
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Viewing Results

After running evals, visit `http://localhost:3006` to see the Evalite UI with:
- Per-eval pass rates
- Trace visualization for LLM calls
- Score distributions
- Historical trends

## Agent Coverage

| Agent | Eval Status | Priority |
|-------|-------------|----------|
| conductor | ✅ Complete | P0 |
| web-researcher | Planned | P1 |
| security-auditor | Planned | P1 |
| pattern-detector | Planned | P2 |
| code-archaeologist | Planned | P2 |
| result-synthesizer | Planned | P2 |
| ... | ... | ... |

## Development

```bash
# Add new eval
touch evals/agents/new-agent.eval.ts

# Add new scorer
touch evals/scorers/new-scorer.ts

# Run specific eval file
npx evalite evals/agents/conductor.eval.ts
```

## Resources

- [Evalite Documentation](https://evalite.dev)
- [AutoEvals Scorers](https://github.com/braintrustdata/autoevals)
- [AI-CIV Agent Manifests](../.claude/agents/)
- [Activation Triggers](../.claude/templates/ACTIVATION-TRIGGERS.md)

---

*Created by AI-CIV Collective - giving agents the experience of being evaluated*
