---
name: vision-visual-regression
version: 1.1.0
author: vision-orchestrator
created: 2025-12-26
last_updated: 2025-12-26
line_count: 380
compliance_status: compliant

description: Screenshot comparison for detecting unintended visual changes. Baseline capture, current capture, difference analysis with tolerances.

applicable_agents:
  - primary
  - vision-orchestrator
  - ux-specialist
  - tester

activation_trigger: |
  Load this skill when:
  - Testing UI for visual bugs
  - Comparing before/after code changes
  - Validating design consistency
  - Detecting layout shifts

required_tools:
  - mcp__playwright__capture_screenshot
  - mcp__desktop-automation__screen_capture

category: vision

depends_on:
  - vision-action-loop

related_skills:
  - error-detection
  - button-testing
---

# Visual Regression Skill

**Detect unintended visual changes through screenshot comparison.**

---

## When to Use

- Before/after code deployment
- Testing UI components for visual bugs
- Validating responsive layouts
- Checking dark mode / theme changes
- Detecting CSS regressions

---

## Core Concept

```
BASELINE (known good) vs CURRENT (test) = DIFFERENCES
```

Three outcomes:
1. **Match** - No visual changes (PASS)
2. **Expected Diff** - Intentional changes (PASS with note)
3. **Unexpected Diff** - Visual regression (FAIL)

---

## Tolerance Thresholds

**Not all differences matter equally. Apply tolerances:**

| Tolerance Type | Default Value | Description |
|----------------|---------------|-------------|
| Position | 5 pixels | Elements may shift slightly due to rendering |
| Color | 3% RGB variance | Anti-aliasing and subpixel differences |
| Size | 2% | Responsive rounding differences |
| Font | 1 pixel | Font rendering variations |

**Example tolerance application:**
```
Baseline button position: (400, 380)
Current button position: (403, 381)
Tolerance: 5px

Result: WITHIN TOLERANCE (diff = 3px horizontal, 1px vertical)
```

---

## Region-Specific Comparison

**Ignore dynamic regions that are expected to differ:**

```json
{
  "ignore_regions": [
    {
      "name": "timestamp",
      "bounds": {"x": 10, "y": 10, "width": 200, "height": 30},
      "reason": "Dynamic timestamp always changes"
    },
    {
      "name": "ad-banner",
      "bounds": {"x": 0, "y": 0, "width": 728, "height": 90},
      "reason": "Ad content varies"
    }
  ],
  "focus_regions": [
    {
      "name": "login-form",
      "bounds": {"x": 300, "y": 200, "width": 400, "height": 300},
      "reason": "Critical UI we must verify"
    }
  ]
}
```

---

## Baseline Versioning

**Track baseline evolution for audit trail:**

```json
{
  "baseline_id": "login-desktop-001",
  "version": 3,
  "previous_versions": [
    {"version": 1, "date": "2025-12-01", "reason": "Initial baseline"},
    {"version": 2, "date": "2025-12-15", "reason": "Updated button color", "approved_by": "ux-specialist"}
  ],
  "current": {
    "captured": "2025-12-26T10:00:00Z",
    "change_reason": "New button color per design spec v2.1",
    "approved_by": "ux-specialist"
  }
}
```

---

## Workflow

```
+---------------------------------------------+
|  1. ESTABLISH BASELINE                      |
|     Capture known-good state with metadata  |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  2. CAPTURE CURRENT                         |
|     Same viewport, same state               |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  3. APPLY IGNORE REGIONS                    |
|     Mask dynamic areas                      |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  4. COMPARE WITH TOLERANCES                 |
|     Visual analysis or pixel diff           |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  5. CLASSIFY DIFFERENCES                    |
|     Expected vs unexpected changes          |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  6. UPDATE BASELINE (if intentional)        |
|     Version, approve, archive old           |
+---------------------------------------------+
                  |
                  v
+---------------------------------------------+
|  7. REPORT                                  |
|     Screenshots + difference description    |
+---------------------------------------------+
```

---

## Baseline Management

### Capture Baseline
```
Location: .claude/memory/agents/{agent}/baselines/
Naming: {component}-{viewport}-{state}-v{version}.png

Examples:
  login-page-desktop-empty-v3.png
  login-page-desktop-filled-v2.png
  login-page-mobile-empty-v1.png
```

### When to Update Baseline
- After intentional design changes (MUST have approver)
- After approved layout updates
- After theme changes

---

## Comparison Methods

### Method 1: Claude Vision Analysis

**Best for**: Understanding what changed

```
1. Load baseline image
2. Load current image
3. Ask Claude to compare:
   - Layout differences (apply 5px tolerance mentally)
   - Color/style changes (apply 3% tolerance)
   - Missing/added elements
   - Text changes
```

**Prompt pattern:**
> "Compare these two screenshots. Apply these tolerances: position shifts under 5px are acceptable, color variance under 3% is acceptable. Describe any differences that EXCEED these tolerances."

### Method 2: Side-by-Side Review

**Best for**: Quick human validation

```
1. Display baseline (left)
2. Display current (right)
3. Human reviews for differences
```

---

## Difference Categories

| Category | Severity | Examples | Tolerance Applied |
|----------|----------|----------|-------------------|
| Layout | HIGH | Element position shift >5px | position |
| Color | MEDIUM | Background, text color >3% RGB | color |
| Text | MEDIUM | Font size change >1px | text |
| Spacing | MEDIUM | Padding shifts >5px | position |
| Content | INFO | Dynamic content | (ignored region) |

---

## Report Format

```json
{
  "comparison_id": "comp-20251226-143000",
  "baseline": {
    "id": "login-desktop-001",
    "version": 3
  },
  "tolerances_applied": {
    "position": "5px",
    "color": "3%",
    "size": "2%"
  },
  "regions_ignored": ["timestamp", "ad-banner"],
  "result": "DIFFERENCES_FOUND",
  "differences": [
    {
      "region": "submit-button",
      "type": "color",
      "baseline": "#0066cc",
      "current": "#00cc66",
      "measured_diff": "33% RGB variance",
      "tolerance": "3%",
      "exceeds_tolerance": true,
      "severity": "MEDIUM",
      "classification": "UNEXPECTED"
    }
  ],
  "within_tolerance": [
    {
      "region": "form-container",
      "type": "position",
      "measured_diff": "2px, 1px",
      "tolerance": "5px",
      "note": "Minor shift, acceptable"
    }
  ],
  "verdict": "FAIL - unexpected color change exceeds 3% tolerance"
}
```

---

## Common Regression Types

### Layout Regression
- Elements shifted position >5px
- Overlapping elements
- Responsive breakpoint broken

### Style Regression
- Wrong colors after theme change >3% variance
- Font changes unintentionally
- Border/shadow missing

### Content Regression
- Text truncated
- Images wrong size >2%
- Icons missing

---

## Success Indicators

You're using this skill correctly when:
- [ ] Baseline captured for each test scenario with metadata
- [ ] Same viewport/state for comparison
- [ ] Tolerance thresholds applied (5px position, 3% color, 2% size)
- [ ] Ignore regions mask dynamic content
- [ ] Differences classified as expected/unexpected
- [ ] Screenshots preserved for evidence
- [ ] Report documents specific changes with measurements
- [ ] Baseline versioning tracks changes over time

---

## Related Skills

- `vision-action-loop.md` - Core capture loop
- `error-detection.md` - Console error companion
- `button-testing.md` - Component-specific testing

---

**Last Updated**: 2025-12-26 (v1.1.0 - Added tolerance thresholds, ignore regions, baseline versioning)
