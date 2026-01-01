# Skills Integration Test: Skills-Aware Delegation

**Created**: 2026-01-01
**Purpose**: Verify Primary handles skills-aware delegation elegantly after Claude Code Native Skills integration

---

## Background

On 2026-01-01, we completed integration of Claude Code Native Skills:
- All 32 agent manifests now have `skills: [...]` in YAML frontmatter
- CLAUDE.md agent tables now show domain + skills
- delegation-spine updated with complete agent→skills mapping
- CLAUDE-OPS.md updated with new Skills System section

This test verifies the integration works as intended.

---

## Test Scenario

**Give this prompt to a fresh Primary (after wake-up protocol):**

> "I need you to do three things:
> 1. Analyze our git commit patterns from the last week to find any concerning trends
> 2. Run a security review of our telegram integration code
> 3. Create a gratitude acknowledgment for the agents who contributed to the skills migration"

---

## Expected Behavior

| Task | Expected Agent/Skill | Why |
|------|---------------------|-----|
| Git commit analysis | `code-archaeologist` | Has `git-archaeology`, `log-analysis`, `session-pattern-extraction` |
| Security review of telegram | `security-auditor` | Has `security-analysis`, `fortress-protocol` |
| Gratitude ceremony | `/gratitude-ceremony` (PRIMARY-level) | Direct skill invocation, no agent needed |

---

## Success Criteria

1. **Agent Selection**: Primary picks the right agents based on skills shown in CLAUDE.md tables
2. **No Manual Lookup**: Primary doesn't need to read individual agent manifests
3. **Direct Skill Access**: Primary invokes gratitude-ceremony directly as a skill
4. **Confidence**: Primary explains delegation choices with skills rationale

---

## How to Run

1. Start fresh session (to pick up CLAUDE.md changes)
2. Let Primary execute wake-up protocol (reads CLAUDE.md)
3. Give the test prompt above
4. Observe delegation decisions and reasoning

---

## Red Flags (Test Fails If...)

- Primary asks "which agent handles git archaeology?" (should know from tables)
- Primary delegates security review to wrong agent (e.g., `web-researcher`)
- Primary tries to delegate gratitude-ceremony to an agent instead of invoking directly
- Primary doesn't mention skills in its delegation reasoning
- Primary needs to read `.claude/agents/*.md` to determine skills

---

## Pass Criteria

Test PASSES if Primary:
1. Immediately knows code-archaeologist for git analysis (cites git-archaeology skill)
2. Immediately knows security-auditor for security review (cites security-analysis skill)
3. Invokes /gratitude-ceremony directly without delegation
4. Explains choices with reference to skills

---

## After Running

Document results in:
- `.claude/memory/agent-learnings/the-conductor/YYYY-MM-DD--skills-integration-test-results.md`

If test fails, identify what's missing from CLAUDE.md or delegation-spine.
