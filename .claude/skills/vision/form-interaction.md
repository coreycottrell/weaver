---
name: form-interaction
version: 1.0.0
author: vision-orchestrator
created: 2025-12-16
last_updated: 2025-12-26
line_count: 200
compliance_status: compliant

description: Testing and filling web forms. Identify fields, fill with test data, submit, and verify outcomes. Includes validation testing.

applicable_agents:
  - primary
  - ux-specialist
  - tester
  - coder

activation_trigger: |
  Load this skill when:
  - Testing form submission flows
  - Filling registration/login forms
  - Testing form validation
  - Automating data entry

required_tools:
  - mcp__desktop-automation__screen_capture
  - mcp__desktop-automation__mouse_move
  - mcp__desktop-automation__mouse_click
  - mcp__desktop-automation__keyboard_type

category: vision

depends_on:
  - vision-action-loop
---

# Form Interaction Skill

**Testing and filling web forms with vision**

**Prerequisite**: Load `vision-action-loop.md` first (this extends that pattern)

---

## When to Use

- Testing form submission flows
- Filling registration/login forms
- Testing form validation
- Automating data entry
- E2E testing of form-based workflows

---

## The Pattern

```
+---------------------------------------------+
|  1. SCREENSHOT the form                      |
|  2. IDENTIFY all form fields                 |
|  3. PLAN test data for each field            |
|  4. FOR EACH field:                          |
|     a. CLICK to focus                        |
|     b. CLEAR existing value (if any)         |
|     c. TYPE test data                        |
|     d. VERIFY field shows correct value      |
|  5. SCREENSHOT filled form                   |
|  6. SUBMIT form                              |
|  7. SCREENSHOT result                        |
|  8. ANALYZE outcome (success/error)          |
|  9. REPORT with evidence                     |
+---------------------------------------------+
```

---

## Step-by-Step Process

### Step 1: Screenshot and Inventory Form

```
mcp__desktop-automation__screen_capture
```

**Vision analysis should identify:**

| Field | Label | Type | Coordinates | Required? |
|-------|-------|------|-------------|-----------|
| 1 | Email | text input | (400, 200) | Yes |
| 2 | Password | password | (400, 260) | Yes |
| 3 | Remember me | checkbox | (320, 310) | No |
| 4 | Sign In | submit button | (400, 360) | - |

### Step 2: Plan Test Data

**For each field, prepare:**

| Field | Valid Data | Invalid Data | Edge Case |
|-------|------------|--------------|-----------|
| Email | test@example.com | not-an-email | empty |
| Password | SecurePass123! | 123 | empty |

### Step 3: Fill Each Field

#### Focus and Type Pattern

```
# 1. Click field to focus
mcp__desktop-automation__mouse_move(x=400, y=200)
mcp__desktop-automation__mouse_click()

# 2. Clear existing value (select all, delete)
mcp__desktop-automation__keyboard_press(key="a", modifiers=["control"])
mcp__desktop-automation__keyboard_press(key="backspace")

# 3. Type new value
mcp__desktop-automation__keyboard_type(text="test@example.com")

# 4. Tab to next field
mcp__desktop-automation__keyboard_press(key="tab")
```

#### For Checkboxes
```
# Click the checkbox
mcp__desktop-automation__mouse_move(x=320, y=310)
mcp__desktop-automation__mouse_click()
# Verify: should see checkmark in next screenshot
```

#### For Dropdowns
```
# Click to open
mcp__desktop-automation__mouse_move(x=400, y=300)
mcp__desktop-automation__mouse_click()
# Wait for dropdown, then click option
```

### Step 4: Screenshot Filled Form

Verify visually:
- All fields show correct values (except masked passwords)
- Checkbox states are correct
- Dropdown shows selected value

### Step 5: Submit Form

```
# Click submit button
mcp__desktop-automation__mouse_move(x=400, y=360)
mcp__desktop-automation__mouse_click()
```

### Step 6: Analyze Result

**Possible outcomes:**

| Outcome | What to Look For |
|---------|------------------|
| Success | Success message, redirect, welcome page |
| Validation Error | Error messages near fields |
| Server Error | Error page, 500 message |
| Nothing | Page unchanged (JS error?) |

---

## Test Scenarios

### Happy Path (Valid Data)
```
Fill all fields with valid data -> Submit -> Expect success
```

### Validation Testing
```
# Empty required field
Leave email empty -> Submit -> Expect "Email is required"

# Invalid format
Enter "not-an-email" -> Submit -> Expect "Invalid email format"
```

### Edge Cases
```
# Maximum length
Enter 1000 character string -> Check if truncated or error

# Special characters
Enter "<script>alert('xss')</script>" -> Check if sanitized
```

---

## Form Field Patterns

| Field Type | Pattern |
|------------|---------|
| Text Input | Click -> Select All -> Delete -> Type -> Tab |
| Password | Same as text (masked display) |
| Checkbox | Click to toggle (verify with screenshot) |
| Radio Button | Click the option (verify selection) |
| Dropdown | Click to open -> Wait -> Click option |
| Textarea | Click -> Select All -> Delete -> Type |

---

## Best Practices

1. **Identify all fields first** - Don't miss hidden or dynamic fields
2. **Clear before typing** - Avoid appending to existing values
3. **Tab between fields** - More reliable than clicking each
4. **Wait after submit** - Allow server response time
5. **Check for async validation** - Fields may validate on blur
6. **Test multiple scenarios** - Valid, invalid, edge cases

---

## Common Issues

### Field not focusing?
- Click center of field
- Check for overlays blocking click
- Try Tab key navigation

### Value not appearing?
- Field may have input restrictions
- Check for JavaScript preventing input

### Form not submitting?
- Check for client-side validation blocking
- Look for error messages
- Check console for JavaScript errors

---

## Related Skills

- `vision-action-loop.md` - Core pattern (prerequisite)
- `button-testing.md` - For submit button testing
- `error-detection.md` - For form error analysis

---

**Last Updated**: 2025-12-26
