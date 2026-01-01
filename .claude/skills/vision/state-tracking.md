---
name: vision-state-tracking
version: 1.1.0
author: vision-orchestrator
created: 2025-12-26
last_updated: 2025-12-26
line_count: 290
compliance_status: compliant

description: State tracking patterns for multi-step vision workflows. Maintain context, track progress, enable recovery.

applicable_agents:
  - primary
  - vision-orchestrator
  - ux-specialist
  - ai-entity-player
  - tester

activation_trigger: |
  Load this skill when:
  - Multi-step workflow (3+ actions)
  - Need to resume from failure
  - Testing flows with sequential dependencies

required_tools:
  - mcp__desktop-automation__screen_capture
  - Write

category: vision

depends_on:
  - vision-action-loop

related_skills:
  - error-handling
  - form-interaction
---

# Vision State Tracking Skill

**Maintain workflow context across multi-step vision operations.**

---

## Why State Tracking

Without state:
- Can't resume from failure
- Don't know what's already done
- Repeat work unnecessarily
- Lose context between screenshots

With state:
- Know exactly where you are
- Resume from last good step
- Skip completed actions
- Generate progress reports

---

## State Object Structure

```json
{
  "workflow_id": "login-test-20251226-143000",
  "workflow_name": "Login Flow Test",
  "started_at": "2025-12-26T14:30:00Z",
  "current_step": 3,
  "total_steps": 5,
  "status": "in_progress",
  "steps": [
    {"step": 1, "name": "Navigate to login", "status": "completed", "screenshot": "step1.png"},
    {"step": 2, "name": "Enter username", "status": "completed", "screenshot": "step2.png"},
    {"step": 3, "name": "Enter password", "status": "in_progress", "screenshot": null},
    {"step": 4, "name": "Click submit", "status": "pending", "screenshot": null},
    {"step": 5, "name": "Verify dashboard", "status": "pending", "screenshot": null}
  ],
  "data": {
    "username": "test@example.com",
    "current_url": "https://app.example.com/login"
  },
  "retry_count": 0,
  "max_retries": 3
}
```

---

## State Operations

### Initialize State

```python
def initialize_state(workflow_name, steps, data=None):
    workflow_id = f"{workflow_name.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    state = {
        "workflow_id": workflow_id,
        "workflow_name": workflow_name,
        "started_at": datetime.utcnow().isoformat() + "Z",
        "current_step": 0,
        "total_steps": len(steps),
        "status": "pending",
        "steps": [
            {"step": i+1, "name": step, "status": "pending", "screenshot": None}
            for i, step in enumerate(steps)
        ],
        "data": data or {},
        "retry_count": 0,
        "max_retries": 3
    }
    return state
```

### Update State After Step

```python
def complete_step(state, screenshot_path=None, step_data=None):
    current = state["current_step"]

    state["steps"][current]["status"] = "completed"
    state["steps"][current]["screenshot"] = screenshot_path
    state["steps"][current]["completed_at"] = datetime.utcnow().isoformat() + "Z"

    if step_data:
        state["data"].update(step_data)

    state["current_step"] += 1

    if state["current_step"] >= state["total_steps"]:
        state["status"] = "completed"
    else:
        state["steps"][state["current_step"]]["status"] = "in_progress"

    return state
```

### Resume from State

```python
def resume_workflow(state):
    # Find first non-completed step
    for i, step in enumerate(state["steps"]):
        if step["status"] != "completed":
            state["current_step"] = i
            state["status"] = "in_progress"
            state["steps"][i]["status"] = "in_progress"
            break
    return state
```

---

## State Validation

**Before resuming, verify screen matches expected state:**

```python
def validate_state_matches_screen(state, current_screenshot):
    current_step = state["current_step"]
    step_info = state["steps"][current_step]

    expected_state = get_expected_screen_state(step_info["name"])
    analysis = analyze_screenshot(current_screenshot)

    if analysis_matches(analysis, expected_state):
        return True, "Screen matches expected state"
    else:
        if can_navigate_to_state(expected_state):
            return False, "NAVIGATE_TO_STATE"
        else:
            return False, "RESET_WORKFLOW"
```

---

## Concurrent Workflow Handling

**Each workflow gets unique ID and separate state file:**

```python
# Workflow 1
state1 = initialize_state("login-test", [...])
# Creates: vision-state/login-test-20251226-143000.json

# Workflow 2 (started 5 seconds later)
state2 = initialize_state("login-test", [...])
# Creates: vision-state/login-test-20251226-143005.json

# No collision - unique timestamps
```

---

## File Location

**State files:**
```
.claude/memory/agents/{agent}/vision-state/
  +-- login-test-20251226-143000.json
  +-- form-test-20251226-150000.json
  +-- archive/
      +-- old-workflow-20251201-100000.json
```

**Screenshot evidence:**
```
.claude/memory/agents/{agent}/evidence/
  +-- login-test-20251226-143000/
      +-- step-01-navigate.png
      +-- step-02-username.png
```

---

## Step Status Values

| Status | Meaning |
|--------|---------|
| `pending` | Not yet started |
| `in_progress` | Currently executing |
| `completed` | Successfully finished |
| `failed` | Failed (see error field) |
| `skipped` | Intentionally skipped |

---

## Data Collection

The `data` field accumulates information throughout workflow:

```json
{
  "data": {
    "username": "test@example.com",
    "form_values": {"field1": "value1"},
    "extracted_text": "Welcome, User!",
    "element_coordinates": {"submit_button": [400, 350]},
    "urls_visited": ["https://app.example.com/login"],
    "response_times": {"step1": 1.2, "step2": 0.8}
  }
}
```

---

## Integration with Error Handling

When error-handling triggers retry:
1. State persists across retries
2. Retry count tracked in state
3. On escalation: state preserved for human review

```python
def record_failure(state, error_info):
    current = state["current_step"]
    state["steps"][current]["status"] = "failed"
    state["steps"][current]["error"] = error_info
    state["retry_count"] += 1

    if state["retry_count"] >= state["max_retries"]:
        state["status"] = "failed"

    return state
```

---

## State Cleanup

**Archive completed states, retain recent history:**

```python
def cleanup_old_states(state_dir, archive_dir, keep_recent=20):
    # Get all state files sorted by modification time
    state_files = sorted(state_dir.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)

    # Keep recent, archive rest
    for i, state_file in enumerate(state_files):
        if i >= keep_recent:
            shutil.move(str(state_file), str(archive_dir / state_file.name))
```

---

## Success Indicators

You're using this skill correctly when:
- [ ] State file created before workflow starts
- [ ] Each step updates state immediately after completion
- [ ] Screenshots saved with step reference
- [ ] Workflow can resume from last completed step
- [ ] Data accumulates correctly
- [ ] State validation checks screen matches expected
- [ ] Concurrent workflows don't collide
- [ ] Old states are archived appropriately

---

## Related Skills

- `vision-action-loop.md` - The core loop
- `error-handling.md` - Error recovery
- `form-interaction.md` - Multi-field forms (uses state tracking)

---

**Last Updated**: 2025-12-26 (v1.1.0 - Added concrete examples, state validation, concurrent handling)
