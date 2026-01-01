---
name: vision-error-detection
version: 1.1.0
author: vision-orchestrator
created: 2025-12-26
last_updated: 2025-12-26
line_count: 340
compliance_status: compliant

description: Detect and capture JavaScript errors, console warnings, and UI error states during visual testing.

applicable_agents:
  - primary
  - vision-orchestrator
  - ux-specialist
  - tester

activation_trigger: |
  Load this skill when:
  - Testing web applications
  - Need to monitor console output
  - Detecting JS errors during UI interaction

required_tools:
  - mcp__playwright__launch_browser
  - mcp__playwright__get_console_logs
  - mcp__playwright__capture_screenshot

category: vision

depends_on:
  - vision-action-loop

related_skills:
  - error-handling
  - visual-regression
---

# Vision Error Detection Skill

**Monitor JavaScript console and UI for errors during visual testing.**

---

## When to Use

- Web application testing where JS errors indicate bugs
- Pre-deployment validation
- Testing forms, authentication, API interactions
- Debugging "silent" failures (UI looks ok but console has errors)

---

## Console Log Types

| Log Type | Severity | Action |
|----------|----------|--------|
| `error` | HIGH | Screenshot + report immediately |
| `warning` | MEDIUM | Collect, report at end |
| `log` | LOW | Collect if relevant |
| `info` | LOW | Collect if debugging |

**Focus on `error` type - these are bugs.**

---

## Error Severity Scoring

**Quantify errors for automated pass/fail decisions:**

| Error Type | Severity Score | Priority |
|------------|----------------|----------|
| TypeError | 10 | Critical |
| ReferenceError | 10 | Critical |
| SyntaxError | 10 | Critical |
| Network 4xx | 8 | High |
| Network 5xx | 9 | High |
| Unhandled Promise | 8 | High |
| React/Vue errors | 5 | Medium |
| Console.error | 5 | Medium |
| Deprecation | 2 | Low |
| Console.warn | 2 | Low |

**Pass/Fail Threshold:**
```python
FAIL_THRESHOLD = 15  # Sum of severity scores

def evaluate_test(errors):
    total_severity = sum(error.severity for error in errors)
    if total_severity > FAIL_THRESHOLD:
        return "FAIL", f"Severity {total_severity} exceeds threshold {FAIL_THRESHOLD}"
    elif total_severity > 0:
        return "PASS_WITH_WARNINGS", f"Severity {total_severity}"
    else:
        return "PASS", "No errors detected"
```

---

## Error Fingerprinting

**Identify and deduplicate errors:**

```python
import hashlib

def fingerprint_error(error):
    """Generate unique fingerprint for error deduplication."""
    key_parts = [
        error.get("type", "unknown"),
        error.get("message", "").split("\n")[0][:100],
        error.get("source", "").split("/")[-1]
    ]
    key = "|".join(key_parts)
    return hashlib.md5(key.encode()).hexdigest()[:12]
```

---

## Expected Errors Whitelist

**Some errors are known/acceptable - don't fail tests for these:**

```json
{
  "expected_errors": [
    {
      "pattern": "ResizeObserver loop limit exceeded",
      "reason": "Known browser quirk, does not affect functionality"
    },
    {
      "pattern": "Failed to load favicon.ico",
      "reason": "Dev server doesn't serve favicon"
    },
    {
      "pattern": "ERR_BLOCKED_BY_CLIENT",
      "reason": "Ad blocker in test environment"
    }
  ]
}
```

---

## Detection Pattern

```
+---------------------------------------------+
|  1. LAUNCH with console monitoring          |
|     launch_browser with devtools enabled    |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  2. NAVIGATE to target                      |
|     Capture any immediate errors            |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  3. INTERACT (click, type, submit)          |
|     Each interaction may trigger errors     |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  4. COLLECT console logs                    |
|     Filter, fingerprint, deduplicate        |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  5. APPLY whitelist                         |
|     Remove expected errors                  |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  6. SCORE severity                          |
|     Calculate pass/fail threshold           |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  7. REPORT findings                         |
|     Screenshot + console output + context   |
+---------------------------------------------+
```

---

## Error Classification

### JavaScript Errors (Critical - Score 10)
```
TypeError: Cannot read property 'x' of undefined
ReferenceError: variableName is not defined
SyntaxError: Unexpected token
```
**Action**: Report immediately, screenshot, stop test if blocking.

### Network Errors (High - Score 8-9)
```
Failed to load resource: the server responded with 404
CORS policy blocked
net::ERR_CONNECTION_REFUSED
```
**Action**: Report, screenshot, may indicate backend issue.

### React/Vue Errors (Medium - Score 5)
```
Warning: Each child in a list should have a unique "key"
Error: Maximum update depth exceeded
Unhandled Promise rejection
```
**Action**: Report as potential bug, note component.

### Deprecation Warnings (Low - Score 2)
```
[Deprecation] Feature X is deprecated
```
**Action**: Collect for report, don't block test.

---

## Detection at Key Points

### After Page Load
```
1. Navigate to URL
2. Wait 2 seconds (let JS execute)
3. Get console logs
4. Filter through whitelist
5. Fingerprint and deduplicate
6. Calculate severity score
7. If score > threshold: screenshot + report
```

### After Each Interaction
```
1. Click/type/submit
2. Wait 500ms
3. Get console logs (incremental)
4. Note any new errors since last check
5. Screenshot if new critical error
6. Determine action from error-action mapping
```

---

## UI Error State Detection

Visual indicators of errors (supplement console monitoring):

| UI Element | Error State |
|------------|-------------|
| Form field | Red border, error message text |
| Alert/toast | Red background, error icon |
| Button | Disabled, error text |
| Page | Error page (404, 500, etc.) |

**Detection method:**
1. Screenshot
2. Analyze for red borders, error icons, alert text
3. Note any visible error messages

---

## Report Format

```json
{
  "test_id": "login-test-001",
  "timestamp": "2025-12-26T15:30:00Z",
  "severity_score": 18,
  "threshold": 15,
  "verdict": "FAIL",
  "unique_errors": 2,
  "total_occurrences": 5,
  "errors_found": [
    {
      "fingerprint": "a1b2c3d4e5f6",
      "count": 3,
      "type": "console_error",
      "severity": 10,
      "message": "TypeError: Cannot read property 'user' of null",
      "source": "auth.js:42",
      "screenshot": "error-auth-001.png"
    }
  ]
}
```

---

## Success Indicators

You're using this skill correctly when:
- [ ] Console logs checked after every interaction
- [ ] Errors captured with context (what action triggered)
- [ ] Screenshots accompany error reports
- [ ] Network errors distinguished from JS errors
- [ ] UI error states detected visually
- [ ] Errors deduplicated via fingerprinting
- [ ] Expected errors filtered via whitelist
- [ ] Severity scoring applied for pass/fail decisions

---

## Related Skills

- `vision-action-loop.md` - Core loop
- `error-handling.md` - Recovery strategies
- `visual-regression.md` - Compare screenshots

---

**Last Updated**: 2025-12-26 (v1.1.0 - Added severity scoring, fingerprinting, whitelist)
