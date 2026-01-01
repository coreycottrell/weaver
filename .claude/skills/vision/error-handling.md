---
name: vision-error-handling
version: 1.1.0
author: vision-orchestrator
created: 2025-12-26
last_updated: 2025-12-26
line_count: 320
compliance_status: compliant

description: Error handling patterns for vision-based automation. Structured retry, fallback, and escalation protocols.

applicable_agents:
  - primary
  - vision-orchestrator
  - ux-specialist
  - ai-entity-player
  - tester

activation_trigger: |
  Load this skill when:
  - Vision action fails
  - Need retry/fallback logic
  - Handling timeouts or unexpected states

required_tools:
  - mcp__desktop-automation__screen_capture
  - mcp__desktop-automation__mouse_click

category: vision

depends_on:
  - vision-action-loop

related_skills:
  - state-tracking
  - visual-regression
  - error-detection
---

# Vision Error Handling Skill

**Structured error recovery for vision automation.**

---

## Error Categories

| Category | Examples | Action | Max Retries |
|----------|----------|--------|-------------|
| TRANSIENT | Loading spinner, network delay | Wait + retry | 3 |
| RECOVERABLE | Element moved, scroll needed | Re-analyze + retry | 2 |
| BLOCKING | Element not found, unexpected page | Screenshot + escalate | 0 |
| FATAL | System error, crash | Abort + notify | 0 |
| TIMEOUT | Action did not complete in time | Retry once, then escalate | 1 |
| PARTIAL | Action completed, wrong result | Re-analyze, reclassify | 1 |

---

## Golden Rules

1. **Always screenshot on failure** - Evidence before recovery
2. **Log the error category** - Enables pattern analysis
3. **Retry intelligently** - Different strategies per category
4. **Escalate decisively** - Don't retry infinitely
5. **Preserve context** - Pass original intent through retries

---

## TIMEOUT Error Protocol

**Symptoms:** Action started but did not complete within expected time

```
Default Timeouts:
- Screen capture: 5 seconds
- Mouse click: 3 seconds
- Page navigation: 15 seconds
- Form submission: 10 seconds
- Element search: 5 seconds

Protocol:
1. Action exceeds timeout threshold
2. Screenshot current state (evidence)
3. Classify as TIMEOUT
4. Attempt 1 retry with 1.5x timeout
5. If timeout persists: Reclassify as BLOCKING
6. Escalate with timeout context
```

---

## PARTIAL Error Protocol

**Symptoms:** Action completed but verification shows unexpected state

**Examples:**
- Button clicked, but wrong page loaded
- Form submitted, but validation error shown
- Navigation successful, but content missing

```
Protocol:
1. Action completed (no exception)
2. Verification shows unexpected state
3. Screenshot both expected vs actual
4. Classify as PARTIAL
5. Determine sub-classification:
   - If recoverable state: PARTIAL -> RECOVERABLE
   - If blocking state: PARTIAL -> BLOCKING
6. Execute appropriate recovery
```

---

## TRANSIENT Error Protocol

**Symptoms:** Loading indicator, "Please wait", spinner visible

```
1. Screenshot current state (evidence)
2. Wait 2 seconds
3. Screenshot again
4. If still loading: wait 3 more seconds
5. If still loading: wait 5 more seconds (backoff)
6. After 3 retries: escalate to BLOCKING
```

**Detection patterns:**
- Spinner/loading icon visible
- "Loading..." text
- Grayed-out interface
- Progress bar visible

---

## RECOVERABLE Error Protocol

**Symptoms:** Element in different position, needs scroll, focus lost

```
1. Screenshot current state
2. Re-analyze entire screen (fresh look)
3. Identify new element location
4. Adjust coordinates
5. Retry action once
6. If still failing: try alternative approach
7. After 2 retries: escalate to BLOCKING
```

**Recovery strategies:**
- Scroll up/down to find element
- Click background first to clear overlays
- Close any modal that appeared
- Refresh if state is inconsistent

---

## BLOCKING Error Protocol

**Symptoms:** Expected element truly absent, wrong page, authentication required

```
1. Screenshot immediately (preserve state)
2. Log detailed context:
   - What action was attempted
   - What was expected
   - What was found instead
3. Save screenshot to evidence directory
4. Escalate to human or abort flow
5. DO NOT retry - state requires intervention
```

---

## FATAL Error Protocol

**Symptoms:** Browser crash, MCP disconnect, system unresponsive

```
1. Log error immediately (may lose context)
2. Attempt one screenshot (may fail)
3. Send alert notification
4. Abort all pending actions
5. DO NOT attempt recovery
```

---

## Recovery Context Preservation

**Critical:** Always preserve original action intent through retries.

```python
class RecoveryContext:
    def __init__(self, action_name, target, expected_outcome):
        self.action_name = action_name
        self.target = target
        self.expected_outcome = expected_outcome
        self.attempt = 0
        self.max_attempts = 3
        self.history = []

    def record_attempt(self, result, screenshot_path):
        self.attempt += 1
        self.history.append({
            "attempt": self.attempt,
            "result": result,
            "screenshot": screenshot_path,
            "timestamp": datetime.utcnow().isoformat()
        })
```

---

## Timeout Thresholds by Action Type

| Action Type | Default Timeout | Extended Timeout |
|-------------|-----------------|------------------|
| Screen capture | 5s | 8s |
| Mouse move | 2s | 3s |
| Mouse click | 3s | 5s |
| Keyboard type | 5s | 8s |
| Page navigation | 15s | 25s |
| Form submission | 10s | 20s |
| Element visibility | 5s | 10s |

---

## Retry Wait Times

| Attempt | Wait Before Retry |
|---------|-------------------|
| 1 | 2 seconds |
| 2 | 4 seconds |
| 3 | 8 seconds |
| 4+ | Escalate |

---

## Error Classification Heuristics

| Observation | Likely Category |
|-------------|-----------------|
| Same screenshot after action | TRANSIENT (loading) |
| Element at different position | RECOVERABLE |
| Unexpected dialog/modal | RECOVERABLE |
| Login page shown | BLOCKING |
| 404/error page | BLOCKING |
| No response from tool | FATAL |
| Action ran but wrong page loaded | PARTIAL |
| Tool returned success but verification failed | PARTIAL |
| Action exceeded time limit | TIMEOUT |

---

## Evidence Requirements

**On ANY error, capture:**
1. Screenshot (PNG)
2. Error type/category
3. Action that was attempted
4. Expected outcome
5. Actual outcome
6. Timestamp
7. Session/task ID
8. Attempt number (for retries)
9. Recovery context (if applicable)

---

## Success Indicators

You're using this skill correctly when:
- [ ] Every error results in a screenshot
- [ ] Error category is logged before retry
- [ ] Retries use appropriate backoff
- [ ] BLOCKING errors are escalated, not retried infinitely
- [ ] Evidence is preserved for post-mortem
- [ ] Timeout errors handled with extended timeout retry
- [ ] Partial successes properly reclassified
- [ ] Recovery context preserved across retries

---

## Related Skills

- `vision-action-loop.md` - The core loop this extends
- `state-tracking.md` - Track state across retries
- `error-detection.md` - Detect console/JS errors

---

**Last Updated**: 2025-12-26 (v1.1.0 - Added TIMEOUT, PARTIAL, recovery context)
