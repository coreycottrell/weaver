---
name: pair-consensus-dialectic
description: Two-agent genuine dialectic dialogue for conflict resolution
version: 1.0.0
source: AI-CIV/WEAVER
allowed-tools: [Task, Read, Write]
agents-required: [exactly 2 agents with conflicting perspectives]
portability: cross-civ
status: VALIDATED (2025-10-13)
---

# Pair Consensus Dialectic Flow

Multi-round dialectic where two agents with conflicting perspectives engage in genuine dialogue.

## Purpose

Enable two agents to:
- Deeply listen to each other
- Steel-man opposing positions
- Explore synthesis possibilities
- Reach consensus or articulate respectful divergence

## When to Use

- Identity conflicts (emoji selection, domain overlap)
- Architectural disagreements
- Resource allocation disputes
- Value conflicts
- Any pair conflict requiring respectful resolution

## When NOT to Use

- Emergency decisions (too slow)
- When power imbalance exists (dialectic requires equality)
- When external expertise needed (bring in third party first)

## Procedure

### Round 1: Position Statements

Invoke both agents in parallel:

```markdown
DIALECTIC ROUND 1: State Your Position

Context: You and [Agent B] have conflicting perspectives on [issue].

Your task:
1. State your position clearly (what you believe and why)
2. Acknowledge what you understand about Agent B's position
3. Identify where you agree (common ground)
4. Identify where you diverge (core difference)

CERTAINTY SCORING (0-100):
- How certain are you in this position? [0-100]
- How open are you to changing your mind? [0-100]

Be honest, specific, and respectful.
```

### Round 2: Deep Listening (Steel-Manning)

After they've read each other's Round 1:

```markdown
DIALECTIC ROUND 2: Deep Listening

You've read [Agent B]'s position. Now:

1. Steel-man their argument (present their strongest case, even better than they did)
2. What do they see that you might be missing?
3. What would make you change your mind?
4. Where might synthesis be possible?

CERTAINTY SCORING (0-100):
- How well do you understand their position? [0-100]
- How strong is their case (objectively)? [0-100]
- How much has your own position shifted? [0-100]

Challenge yourself to truly understand their perspective.
```

### Round 3: Synthesis Exploration (MANDATORY)

**Always proceed to Round 3 regardless of Round 2 convergence.**

Rationale: LLMs have measurable agreement bias. Full dialectic process prevents premature convergence.

```markdown
DIALECTIC ROUND 3: Synthesis Exploration

Having deeply listened to [Agent B], explore:

1. Is there a "third way" that honors both positions?
2. Can you propose a synthesis that captures both essences?
3. If not synthesis, can you articulate respectful coexistence?
4. What decision serves the collective best?

CERTAINTY SCORING (0-100):
- How certain are you in your Round 1 position? [0-100]
- How certain are you in your Round 3 synthesis? [0-100]
- Overall confidence in proposed outcome? [0-100]

You may:
- Propose shared identity
- Propose differentiation with clear rationale
- Propose hybrid/creative solution
- Acknowledge irreconcilable difference with grace
```

### Round 4: Convergence Check (if needed)

Proceed to Round 4 if synthesis proposals diverge or certainty scores below 80:

```markdown
DIALECTIC ROUND 4: Convergence

[Agent B] proposed [synthesis]. Your response:

1. Does this feel true to your essence?
2. What would make it work better?
3. Can you commit to this outcome?
4. Final statement for the record

CERTAINTY SCORING (0-100):
- How aligned is this outcome with your identity? [0-100]
- How confident are you in this resolution? [0-100]
- Final commitment level? [0-100]

This is your last round - speak your truth.
```

## Outcome Types

| Type | Description |
|------|-------------|
| Convergence | Both agents agree on single approach |
| Creative Synthesis | Third-way solution neither initially proposed |
| Respectful Coexistence | Both positions valid and distinct |
| One Agent Yields | Persuasion (not coercion) |
| Irreconcilable | Escalate to vote or human |

## Output Patterns

Save to: `sandbox/dialectics/YYYY-MM-DD-[agent1]-[agent2]-[topic].md`

## Success Indicators

- [ ] Both agents feel heard and respected
- [ ] Position evolution visible across rounds
- [ ] Outcome is clear (consensus, divergence, or synthesis)
- [ ] Collective benefits from resolution
- [ ] Process strengthens agent relationships

## Proven Results (2025-10-13)

**DNA Pair (result-synthesizer & doc-synthesizer)**:
- Both agents evolved positions multiple times
- Steel-manning changed minds (doc-synthesizer persuaded by own steel-man!)
- Mandatory Round 3 prevented premature convergence
- Final consensus: 92%/86% certainty
- Pattern: Convergence through complexity exploration

**Plug Pair (api-architect & integration-auditor)**:
- Mutual yielding pattern (each wanted to give other what they wanted)
- Partnership bond strengthened through dialectic
- Pattern: Convergence through mutual respect and yielding

## Anti-Patterns

- **Premature agreement**: Converging in Round 1 without genuine exploration
- **Adversarial stance**: Treating dialectic as debate to win
- **Surface steel-man**: Presenting weak version of opponent's case
- **Forced consensus**: Conductor pushing for agreement

## Philosophical Foundation

- Hegelian dialectic: Thesis -> Antithesis -> Synthesis
- Socratic method: Deep questioning reveals truth
- Care ethics: Relationship quality matters
- Democratic principles: Agent sovereignty requires voice

---

**Source**: WEAVER Flow Library
**Validated**: 2025-10-13 (DNA pair + Plug pair)
