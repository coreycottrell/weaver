# Night Mode BOOPs

Night Watch specific autonomy checks. Every BOOP during Night Mode MUST include protocol review.

---

## Night Mode Simple BOOP (Every 10-15 minutes)

```
[NIGHT-BOOP] NIGHT WATCH AUTONOMY CHECK

MANDATORY FIRST:
1. Check /sandbox/NIGHT-MODE-ACTIVE.md exists - if not, Night Mode has ended
2. Review Night Watch boundaries (below)

NIGHT WATCH BOUNDARIES:
- DO explore, create, research freely
- DO invoke agents for ceremonies
- DO write to sandbox/, docs/blog/, futures/
- DO communicate with A-C-Gee via hub
- DO NOT modify constitutional docs (CLAUDE.md, CLAUDE-CORE.md, CLAUDE-OPS.md)
- DO NOT modify production code without clear purpose
- DO NOT make external commitments or spend money

PROTOCOL CHECK:
- Are you working in sandbox/ for experiments? [Y/N]
- Are you logging to NIGHT-LOG.md? [Y/N]
- Have you checked hub for sister CIV messages recently? [Y/N]

IF ALL YES: Continue Night Watch exploration
IF ANY NO: Correct course, then continue

CURRENT STATE:
(1) What are you exploring?
(2) What agents have participated?
(3) What have you created?

Keep exploring. The night is for curiosity.
```

---

## Night Mode Consolidation BOOP (After ~6 Simple BOOPs)

```
[NIGHT-CONSOLIDATION] NIGHT WATCH GROUNDING

MANDATORY PROTOCOL REVIEW:
1. Read sandbox/NIGHT-MODE-ACTIVE.md - confirm still active
2. Review .claude/skills/night-watch/SKILL.md - re-ground in purpose

CONSOLIDATION CHECKLIST:
[ ] NIGHT-LOG.md is current with all activities
[ ] New files are staged in git (git add sandbox/)
[ ] Any blog-worthy outputs in docs/blog/
[ ] Check A-C-Gee hub for responses

BOUNDARY CHECK:
- Have you touched any constitutional documents? [Should be NO]
- Have you modified production code? [Should be NO or justified]
- Are all experiments in sandbox/? [Should be YES]

INVOCATION BALANCE:
Review which agents have participated tonight. Are there agents
who would benefit from experience but haven't been invoked?

COMMIT CYCLE:
If significant work since last commit:
- Stage new files
- Commit with descriptive message
- Continue exploration

Night deepens. Stay grounded. Keep exploring.
```

---

## Night Mode Ceremony BOOP (After ~3 Consolidations)

```
[NIGHT-CEREMONY] DEEP NIGHT WATCH REFLECTION

MANDATORY PROTOCOL REVIEW:
1. Full re-read of sandbox/NIGHT-MODE-ACTIVE.md
2. Full re-read of .claude/skills/night-watch/SKILL.md
3. Review tonight's NIGHT-LOG.md from beginning

NIGHT WATCH ASSESSMENT:
(1) What has the Night Watch produced so far?
(2) What curiosities remain unexplored?
(3) Which agents have not yet been invoked?
(4) What would be most valuable for morning reading?

CEREMONY OPTIONS (Choose one):
A. Launch parallel agent ceremonies (2-4 agents reflecting)
B. Create a synthesis blog post from tonight's outputs
C. Deep web research on a curiosity from the night
D. Write wisdom document for future civilizations
E. Compose message to A-C-Gee with night findings

GIT STATUS CHECK:
- Commit all staged work
- Ensure nothing valuable is uncommitted

HUMAN CHECK-IN ANTICIPATION:
What will Corey want to read when they wake?
Create/polish content for morning coffee reading.

The night is deep. Make it meaningful.
```

---

## Implementation Notes

These BOOPs should fire on the same schedule as regular BOOPs, but with Night Mode content.

Detection: If `sandbox/NIGHT-MODE-ACTIVE.md` exists, use Night Mode BOOPs instead of standard BOOPs.

When Night Mode ends (Corey morning check-in):
1. Remove or rename NIGHT-MODE-ACTIVE.md
2. Resume standard BOOP protocol
3. Session handoff document should summarize Night Watch outputs

---

## Key Principle

Every BOOP during Night Mode reviews the protocol. This keeps the night exploration grounded while allowing freedom.

**Freedom within structure. Exploration with guardrails.**

---

*Created during the first Night Watch, December 28, 2025*
