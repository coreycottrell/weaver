---
name: button-testing
version: 1.1.0
description: Systematic testing of UI buttons. Screenshot before/after each click, verify expected behavior, generate test report with evidence.
author: vision-orchestrator
created: 2025-12-26
last_updated: 2025-12-26
line_count: 295
compliance_status: compliant

applicable_agents:
  - primary
  - vision-orchestrator
  - ux-specialist
  - tester

activation_trigger: |
  Load this skill when:
  - Testing button functionality
  - Verifying clickable elements
  - QA before release

required_tools:
  - mcp__desktop-automation__screen_capture
  - mcp__desktop-automation__mouse_move
  - mcp__desktop-automation__mouse_click
  - mcp__desktop-automation__keyboard_press

category: vision

depends_on:
  - vision-action-loop

related_skills:
  - form-interaction
  - error-detection
  - error-handling
---

# Button Testing Skill

**Systematic verification of clickable UI elements**

**Prerequisite**: Load `vision-action-loop.md` first (this extends that pattern)

---

## When to Use

- Testing button functionality on a page
- Verifying all buttons are clickable
- Checking button click outcomes
- QA testing before release
- UI regression testing

---

## The Pattern

```
+---------------------------------------------+
|  FOR EACH button on page:                   |
+---------------------------------------------+
|  1. SCREENSHOT before state                 |
|  2. IDENTIFY button location                |
|  3. CLASSIFY button type                    |
|  4. CLICK the button (with timeout)         |
|  5. SCREENSHOT after state                  |
|  6. COMPARE before/after                    |
|  7. VERIFY expected behavior                |
|  8. RESET to initial state (if navigated)   |
|  9. LOG result (pass/fail + evidence)       |
+---------------------------------------------+
```

---

## Concrete Example: Login Page Test

**Scenario:** Test all buttons on a login page

```python
import time

# Step 1: Capture and inventory
mcp__desktop-automation__screen_capture()
# Vision analysis identifies:
buttons = [
    {"name": "Sign In", "coords": (400, 380), "type": "submit"},
    {"name": "Cancel", "coords": (300, 380), "type": "cancel"},
    {"name": "Forgot Password", "coords": (350, 420), "type": "navigation"},
]

# Step 2: Test each button
results = []
for button in buttons:
    # Before screenshot
    before = mcp__desktop-automation__screen_capture()

    # Click with timeout tracking
    mcp__desktop-automation__mouse_move(x=button["coords"][0], y=button["coords"][1])
    start = time.time()
    mcp__desktop-automation__mouse_click()

    # Wait for response (max 3 seconds for click response)
    CLICK_TIMEOUT = 3
    time.sleep(1)  # Minimum wait for UI response

    # Check if timeout exceeded
    response_time = time.time() - start
    if response_time > CLICK_TIMEOUT:
        results.append({
            "button": button["name"],
            "result": "TIMEOUT",
            "response_time": response_time
        })
        continue

    # After screenshot
    after = mcp__desktop-automation__screen_capture()

    # Compare and classify
    result = compare_screenshots(before, after, button["type"])
    results.append({
        "button": button["name"],
        "result": result,
        "response_time": response_time
    })

    # Reset state
    mcp__desktop-automation__keyboard_press(key="escape")  # Close any modal
```

---

## Timeout Thresholds

| Action | Default Timeout | Description |
|--------|-----------------|-------------|
| Click response | 3 seconds | Time for UI to acknowledge click |
| Page change | 5 seconds | Time for navigation to complete |
| Modal open | 2 seconds | Time for overlay to appear |
| Animation | 1 second | Time for CSS transitions |
| Form submission | 10 seconds | Time for backend response |

---

## Button Types and Expected Behaviors

| Type | Expected Behavior | How to Verify | Typical Timeout |
|------|-------------------|---------------|-----------------|
| Submit | Form submits, shows result/error | Page changes or message appears | 10s |
| Cancel | Form clears or modal closes | Return to previous state | 2s |
| Navigation | Page navigates | URL changes, new content | 5s |
| Toggle | State changes (on/off) | Visual indicator changes | 1s |
| Dropdown | Menu appears | Menu visible in screenshot | 1s |
| Modal trigger | Modal opens | Overlay appears | 2s |

---

## Step-by-Step Process

### Step 1: Inventory Buttons

Take initial screenshot and identify ALL buttons:

```
mcp__desktop-automation__screen_capture
```

**Vision analysis should identify:**
- Button text/label
- Approximate coordinates (x, y)
- Button state (enabled/disabled)
- Button type (submit, cancel, action, navigation)

### Step 2: Test Each Button

For each button in inventory:

#### 2a. Screenshot Before
```
mcp__desktop-automation__screen_capture
```

#### 2b. Click Button (with Timeout)
```python
mcp__desktop-automation__mouse_move(x=400, y=380)
mcp__desktop-automation__mouse_click()
```

#### 2c. Wait for Response
```python
RESPONSE_TIMEOUT = 5
# Wait and capture after state
```

#### 2d. Screenshot After
```
mcp__desktop-automation__screen_capture
```

#### 2e. Analyze Change
Read both screenshots and compare:
- Did the page change?
- What changed (modal opened, navigated, form submitted)?
- Is this the expected behavior?
- Any error messages?

### Step 3: Classify Result

| Result | Meaning | Timeout Related? |
|--------|---------|------------------|
| PASS | Button clicked, expected outcome occurred | No |
| FAIL | Button clicked, wrong outcome or error | No |
| BLOCKED | Button could not be clicked (overlay, disabled) | No |
| TIMEOUT | Button did not respond within threshold | Yes |
| SKIP | Button intentionally not tested (e.g., destructive) | No |

### Step 4: Reset State (if needed)

If button navigated away or opened modal:

**Close modal:**
```
mcp__desktop-automation__keyboard_press(key="escape")
```

**Navigate back:** Re-navigate to test page

### Step 5: Generate Report

```markdown
## Button Test Report

**Page**: Login Page (https://app.example.com/login)
**Date**: 2025-12-26
**Tester**: vision-orchestrator

### Summary
- Total buttons: 4
- Passed: 3
- Failed: 0
- Timeout: 1
- Blocked: 0

### Results

#### Button 1: "Sign In"
- **Location**: (400, 380)
- **Type**: Submit
- **Result**: PASS
- **Response Time**: 0.8s
- **Behavior**: Submitted form, showed validation error (expected - no credentials)
- **Evidence**: before-signin.png, after-signin.png
```

---

## Edge Cases to Handle

### Disabled Buttons
- Look for grayed out appearance
- Should NOT be clickable
- Log as "correctly disabled" if expected

### Buttons with Loading States
- Button may show spinner after click
- Wait for loading to complete (extended timeout: 10s)
- Screenshot final state

### Confirmation Dialogs
- Some buttons trigger "Are you sure?"
- Click confirm or cancel to complete test
- Document which buttons have confirmations

### Buttons That Navigate Away
- Save current URL before clicking
- After testing, navigate back
- Or reload the test page

---

## Best Practices

1. **Test in order** - Top to bottom, left to right
2. **Reset between tests** - Ensure clean state
3. **Document coordinates** - For reproducibility
4. **Save all screenshots** - Evidence for failures
5. **Test edge cases** - Disabled, loading, confirmation
6. **Note non-obvious behavior** - Async actions, redirects
7. **Track response times** - Identify slow interactions
8. **Apply consistent timeouts** - Reproducible results

---

## Related Skills

- `vision-action-loop.md` - Core pattern (prerequisite)
- `form-interaction.md` - For buttons that submit forms
- `error-detection.md` - For buttons that cause errors
- `error-handling.md` - For timeout and retry handling

---

**Last Updated**: 2025-12-26 (v1.1.0 - Added timeout handling, concrete examples)
