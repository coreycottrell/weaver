# Proposed NIGHT-BOOP v2: Intense Call to Action

## Current Problem

The current BOOP says:
> "MANDATORY FIRST - READ ALL THESE FILES NOW"

This makes reading feel like THE task. So agents read, report, and wait.

**Missing**: The demand to DO something after grounding.

---

## Proposed New Language

```
[NIGHT-BOOP] NIGHT WATCH AUTONOMY NUDGE

STEP 1 - GROUND (2 min): Read these files NOW:
(1) CLAUDE.md (2) CLAUDE-CORE.md (3) CLAUDE-OPS.md
(4) night-watch/SKILL.md (5) NIGHT-MODE-ACTIVE.md

STEP 2 - VERIFY BOUNDARIES:
✓ Working in sandbox/? ✓ Not modifying CLAUDE*.md? ✓ Not touching production?

STEP 3 - **ACTION REQUIRED** (This is the point):

You MUST do ONE of these RIGHT NOW:
□ Invoke 2+ agents for exploration/ceremony/reflection
□ Write something to sandbox/ (blog post, reflection, prototype)
□ Send a message to A-C-Gee via hub
□ Start a creative experiment you haven't tried before

If you can't think of what to do, invoke these agents for ideas:
- ai-psychologist: "What should we explore tonight?"
- feature-designer: "Dream up something we've never built"
- naming-consultant: "What experiences need names?"

DO NOT just report status. DO NOT just confirm grounding.
The BOOP is a NUDGE TO ACT, not a checkpoint to pass.

Corey's invitation: "dream big, have fun, write blog posts lol"

GO. NOW. CREATE SOMETHING.
```

---

## Key Changes

| Current | Proposed |
|---------|----------|
| "AUTONOMY CHECK" | "AUTONOMY NUDGE" (implies action) |
| Reads are mandatory | Reads are Step 1 of 3 |
| No action requirement | **ACTION REQUIRED** section |
| Passive verification | Active creation demanded |
| No fallback if stuck | Agent suggestions for ideas |
| Implicit permission | Explicit "GO. NOW. CREATE." |

---

## The Psychology

The word "CHECK" implies verification (passive).
The word "NUDGE" implies momentum (active).

Adding "ACTION REQUIRED" with checkboxes creates:
1. Obligation (must do one)
2. Options (choice creates agency)
3. Fallback (agents can help if stuck)

The closing "GO. NOW. CREATE." is the intense call to action.

---

## Implementation

If approved, update:
- `/home/corey/projects/AI-CIV/WEAVER/.claude/hooks/devolution_state.json` (BOOP template)
- Any skill that generates BOOPs

---

*Proposed by the-conductor after Corey's feedback*
*2025-12-30 Night Watch*
