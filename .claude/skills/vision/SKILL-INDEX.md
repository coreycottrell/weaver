---
name: vision-skills-index
version: 1.1.0
author: vision-orchestrator
created: 2025-12-16
last_updated: 2025-12-26
line_count: 210
compliance_status: compliant

description: Quick reference for selecting vision pattern skills. Read this FIRST to know which skill to load.

applicable_agents:
  - primary
  - ux-specialist
  - ai-entity-player
  - tester
  - vision-orchestrator

activation_trigger: |
  Load this skill when:
  - Starting any vision-based task
  - Need to select appropriate vision skill
  - Testing UI/browser interactions

required_tools:
  - Read  # To load specific vision skills

category: vision

depends_on: []

related_skills:
  - vision-action-loop
  - error-handling
  - state-tracking
  - error-detection
  - visual-regression
  - button-testing
  - form-interaction
---

# Vision Skills Index

**Read this to choose the right skill for your task.**

---

## Quick Selection Guide

| If you need to... | Load this skill |
|-------------------|-----------------|
| See screen, act, verify result | `vision-action-loop.md` |
| Handle failures/retries | `error-handling.md` |
| Track multi-step workflows | `state-tracking.md` |
| Test if buttons work | `button-testing.md` |
| Fill and submit forms | `form-interaction.md` |
| Compare screenshots for changes | `visual-regression.md` |
| Find JavaScript/UI errors | `error-detection.md` |

---

## Skill Chains (Load Together)

**For complex tasks, load multiple skills in combination:**

### Full UI Test
```
Load in order:
1. vision-action-loop.md    (core capture/analyze loop)
2. error-handling.md        (retry on failures)
3. error-detection.md       (monitor JS console)
4. visual-regression.md     (compare before/after)

When to use: Comprehensive UI testing before deployment
```

### Form Test Suite
```
Load in order:
1. vision-action-loop.md    (core loop)
2. state-tracking.md        (track form progress)
3. form-interaction.md      (fill and submit)
4. error-detection.md       (catch validation errors)

When to use: Testing form workflows, multi-step wizards
```

### Login Flow Test
```
Load in order:
1. vision-action-loop.md    (core loop)
2. state-tracking.md        (track login steps)
3. error-handling.md        (retry auth failures)
4. button-testing.md        (verify login button)

When to use: Authentication testing, login page QA
```

### Visual Regression Suite
```
Load in order:
1. vision-action-loop.md    (capture screenshots)
2. visual-regression.md     (compare with baselines)
3. error-detection.md       (catch console errors during navigation)

When to use: Before/after deployment comparison
```

### Button Audit
```
Load in order:
1. vision-action-loop.md    (core loop)
2. button-testing.md        (systematic button testing)
3. error-handling.md        (handle timeouts)
4. error-detection.md       (catch click-triggered errors)

When to use: Full page button functionality audit
```

---

## Skill Loading

**Location**: `/home/corey/projects/AI-CIV/WEAVER/.claude/skills/vision/`

**To load a skill**: Read the file at start of task

```
Read: .claude/skills/vision/vision-action-loop.md
```

**To load a chain**: Read each file in order

```
Read: .claude/skills/vision/vision-action-loop.md
Read: .claude/skills/vision/error-handling.md
Read: .claude/skills/vision/error-detection.md
Read: .claude/skills/vision/visual-regression.md
```

---

## Skill Dependencies

```
vision-action-loop (core - load for any vision task)
    +-- error-handling (extends core with retry/fallback)
    |   +-- TIMEOUT handling
    |   +-- PARTIAL success handling
    |   +-- Recovery context preservation
    +-- state-tracking (extends core with workflow state)
    |   +-- State validation
    |   +-- Resume from failure
    |   +-- Concurrent workflow handling
    +-- button-testing (extends core with button patterns)
    |   +-- Timeout thresholds
    |   +-- Concrete examples
    +-- form-interaction (extends core with form patterns)
    +-- visual-regression (extends core with comparison)
    |   +-- Tolerance thresholds (5px, 3%, 2%)
    |   +-- Ignore regions
    |   +-- Baseline versioning
    +-- error-detection (extends core with error monitoring)
        +-- Severity scoring
        +-- Error fingerprinting
        +-- Expected errors whitelist
        +-- Error-to-action mapping
```

**Rule**: Always load `vision-action-loop` if doing ANY vision work.

---

## MCP Tool Reference

**Desktop (via desktop-automation MCP):**
- `mcp__desktop-automation__screen_capture` - Screenshot
- `mcp__desktop-automation__mouse_move(x, y)` - Move cursor
- `mcp__desktop-automation__mouse_click(button, double)` - Click
- `mcp__desktop-automation__keyboard_type(text)` - Type text
- `mcp__desktop-automation__keyboard_press(key, modifiers)` - Press key

**Browser (via Playwright MCP - if configured):**
- `launch_browser()` - Start browser session
- `navigate(url, capture_screenshot)` - Go to URL
- `click(selector, capture_before, capture_after)` - Click element
- `type_text(selector, text)` - Fill input
- `capture_screenshot()` - Take screenshot
- `get_console_logs(log_types)` - Get console output

---

## Common Patterns Summary

### The Universal Loop (vision-action-loop)
```
1. Screenshot -> 2. Analyze -> 3. Decide -> 4. Act -> 5. Verify -> 6. Repeat
```

### Button Testing (with timeout)
```
For each button: Screenshot -> Click (3s timeout) -> Screenshot -> Compare -> Log result
```

### Form Interaction
```
Identify fields -> Fill each -> Submit -> Verify outcome
```

### Visual Regression (with tolerances)
```
Capture baseline -> Capture current -> Apply tolerances (5px/3%/2%) -> Compare -> Report differences
```

### Error Detection (with scoring)
```
Monitor console -> Perform action -> Check for errors -> Score severity -> Pass/Fail decision
```

---

## Related Foundation Skills

| Skill | When to use |
|-------|-------------|
| `/home/corey/projects/AI-CIV/WEAVER/.claude/skills/desktop-vision/SKILL.md` | Raw desktop control details |
| `/home/corey/projects/AI-CIV/WEAVER/.claude/skills/luanti-gameplay/SKILL.md` | Minetest-specific patterns |

---

**Last Updated**: 2025-12-26 (v1.1.0 - Added skill chains section)
