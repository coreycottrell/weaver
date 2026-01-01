---
name: vision-action-loop
version: 1.0.0
author: vision-orchestrator
created: 2025-12-16
last_updated: 2025-12-26
line_count: 180
compliance_status: compliant

description: The universal pattern for vision-guided interaction. Screenshot, Analyze, Decide, Act, Verify. Load this for ANY vision task.

applicable_agents:
  - primary
  - ux-specialist
  - ai-entity-player
  - tester
  - vision-orchestrator

activation_trigger: |
  Load this skill when:
  - ANY task requiring visual understanding of screen
  - Testing UI elements
  - Navigating applications
  - Verifying visual state

required_tools:
  - mcp__desktop-automation__screen_capture
  - mcp__desktop-automation__mouse_move
  - mcp__desktop-automation__mouse_click
  - mcp__desktop-automation__keyboard_type

category: vision

depends_on: []
---

# Vision Action Loop Skill

**The Core Pattern for Vision-Guided Automation**

---

## When to Use

- ANY task requiring visual understanding of screen
- Testing UI elements
- Navigating applications
- Verifying visual state
- Debugging UI issues

**This is the foundation skill. Other vision skills extend this pattern.**

---

## The Loop

```
+---------------------------------------------+
|  1. CAPTURE                                  |
|     Take screenshot to see current state     |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  2. ANALYZE                                  |
|     Use vision to understand what you see    |
|     - What elements are visible?             |
|     - What is the current state?             |
|     - What can be interacted with?           |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  3. DECIDE                                   |
|     Determine next action                    |
|     - What should I do to achieve goal?      |
|     - What coordinates/elements to target?   |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  4. ACT                                      |
|     Execute the action                       |
|     - Click, type, press key                 |
|     - Navigate, scroll                       |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  5. VERIFY                                   |
|     Screenshot again to confirm outcome      |
|     - Did the action work?                   |
|     - Is the new state as expected?          |
+---------------------------------------------+
                  |
                  v
          Goal achieved?
              | No
         [Return to 1]
              | Yes
            DONE
```

---

## Step-by-Step Implementation

### Step 1: CAPTURE

**Desktop (MCP direct):**
```
mcp__desktop-automation__screen_capture
```

**Browser (Playwright MCP):**
```
mcp__playwright__navigate(url, capture_screenshot=True)
# or
mcp__playwright__capture_screenshot()
```

### Step 2: ANALYZE

**Read the screenshot with vision:**
The screenshot will be returned as an image that you can analyze directly.

**What to identify:**
- Page/window title
- Key UI elements (buttons, inputs, links)
- Current state (logged in? error displayed? loading?)
- Coordinates of elements you need to interact with
- Any unexpected elements or issues

**Example analysis:**
> "I see a login form with:
> - 'Email' input at approximately (400, 250)
> - 'Password' input at approximately (400, 310)
> - Blue 'Sign In' button at approximately (400, 380)
> - 'Forgot password?' link below the button"

### Step 3: DECIDE

**Based on analysis, determine:**
1. What action achieves the goal?
2. What element to target?
3. What coordinates to use?
4. Any preconditions needed?

### Step 4: ACT

**Mouse actions:**
```
mcp__desktop-automation__mouse_move(x=400, y=380)
mcp__desktop-automation__mouse_click(button="left", double=false)
```

**Keyboard actions:**
```
mcp__desktop-automation__keyboard_type(text="user@example.com")
mcp__desktop-automation__keyboard_press(key="enter")
mcp__desktop-automation__keyboard_press(key="c", modifiers=["control"])
```

### Step 5: VERIFY

**Take another screenshot and compare:**
- Did the expected change occur?
- Any error messages?
- Is the new state correct?

**If not verified:**
- Log the issue
- Decide: retry, try different approach, or escalate

---

## Common Patterns

### Click and Verify
```
1. Screenshot (before)
2. Identify target coordinates
3. Click target
4. Screenshot (after)
5. Compare before/after
```

### Type and Submit
```
1. Screenshot
2. Identify input field
3. Click to focus
4. Type text
5. Identify submit button
6. Click submit
7. Screenshot (result)
```

### Navigate Menu
```
1. Screenshot
2. Identify menu location
3. Click menu
4. Screenshot (menu open)
5. Identify menu item
6. Click item
7. Screenshot (result)
```

---

## Best Practices

1. **Always screenshot before acting** - Know the state
2. **Always verify after acting** - Confirm the change
3. **Log coordinates used** - For debugging
4. **Set iteration limits** - Prevent infinite loops
5. **Handle failures gracefully** - Retry or escalate
6. **Save all screenshots** - Evidence trail

---

## Related Skills

- `button-testing.md` - Extends this for button verification
- `form-interaction.md` - Extends this for form filling
- `error-detection.md` - Extends this with console monitoring

---

**Last Updated**: 2025-12-26
