# Skills Audit Buildout Plan

**Created**: 2026-01-07
**Source**: Q1 2026 Skills Audit (4 agents, 12 infographics)
**Owner**: the-conductor + capability-curator
**Tracker**: `.claude/skill-audit-tracker.md`

---

## Executive Summary

The skills audit identified a clear gap: **70% of skills are dormant** (0% activation) because they depend on cron/scheduled infrastructure that was never configured. The architecture is sound. The skills are built. They just need activation.

**Core Finding**: BOOP-integrated skills = 90% activation. Cron-dependent skills = 0% activation.

**The Fix**: Either configure cron OR convert to BOOP-triggered (opportunistic scheduling).

---

## Phase 1: Immediate (This Week)

### Task 1.1: Register 5 Dormant Skills in Scheduled Tasks System

**Owner**: the-conductor
**Dependencies**: None
**Estimated Time**: 15 minutes
**Success Criteria**: All 5 skills appear in `scheduled-tasks-state.json`

**Commands to Execute**:

```bash
cd /home/corey/projects/AI-CIV/WEAVER

# Register intel-scan as daily task
python3 tools/scheduled_tasks.py register intel-scan daily "Morning AI news scan (6am equivalent)"

# Register deep-research as daily task
python3 tools/scheduled_tasks.py register deep-research daily "Parallel research phase (7am equivalent)"

# Register daily-blog as daily task (already exists, verify)
python3 tools/scheduled_tasks.py list | grep daily-blog

# Register verify-publish as daily task
python3 tools/scheduled_tasks.py register verify-publish daily "Fact-check and publish (11am equivalent)"

# Register evening-capture as daily task
python3 tools/scheduled_tasks.py register evening-capture daily "End-of-day learning capture (6pm equivalent)"

# Verify all registered
python3 tools/scheduled_tasks.py list
```

**Verification**:
```bash
cat /home/corey/projects/AI-CIV/WEAVER/.claude/scheduled-tasks-state.json | grep -E "(intel-scan|deep-research|daily-blog|verify-publish|evening-capture)"
# Should show all 5 tasks registered
```

---

### Task 1.2: Add Pipeline Check to BOOP Manager

**Owner**: the-conductor
**Dependencies**: Task 1.1 complete
**Estimated Time**: 30 minutes
**Success Criteria**: BOOP cycle includes scheduled task check

**What to Modify**: The BOOP cycle should call `boop_scheduled_check()` and surface due tasks.

**Add to BOOP Pattern** (in `.claude/skills/bsky-boop-manager/SKILL.md` or `delegation-spine`):

```python
# At start of BOOP cycle
from tools.scheduled_tasks import ScheduledTasks

tasks = ScheduledTasks()
due = tasks.get_due_tasks()

if due:
    print(f"[BOOP] {len(due)} scheduled tasks due:")
    for task in due:
        print(f"  - {task['id']}: {task['description']}")
    # Prioritize running these before other BOOP activities
```

**Verification**:
```bash
# Run a BOOP check
python3 tools/scheduled_tasks.py check
# Should show due tasks with descriptions
```

---

### Task 1.3: Run Each Dormant Skill Manually Once

**Owner**: the-conductor (delegate to appropriate agents)
**Dependencies**: Task 1.1 complete
**Estimated Time**: 2-3 hours total (can be spread across day)
**Success Criteria**: Each skill executes successfully at least once

**Execution Order** (respects dependencies):

| Order | Skill | Slash Command | Agent to Delegate | Duration |
|-------|-------|---------------|-------------------|----------|
| 1 | intel-scan | `/intel_scan` | web-researcher + blogger | 45-60 min |
| 2 | deep-research | `/deep_research` | linkedin-researcher x3 + web-researcher | 45-60 min |
| 3 | daily-blog | `/daily_blog` | doc-synthesizer | 45-60 min |
| 4 | verify-publish | `/verify_publish` | claim-verifier + bsky-manager | 30-45 min |
| 5 | evening-capture | `/evening_capture` | pattern-detector | 20-30 min |

**Manual Execution Template**:
```
For each skill:
1. Invoke the skill command
2. Monitor for errors or hangs
3. Document what worked/failed in scratch-pad
4. If successful, mark complete:
   python3 tools/scheduled_tasks.py complete {skill-name} "Manual test run successful"
5. If failed, document issue and create fix task
```

**Note**: Some skills depend on outputs from previous skills. If running out of sequence, may need to manually create expected input files.

---

### Task 1.4: Create Daily Pipeline Directory Structure

**Owner**: the-conductor
**Dependencies**: None (can run parallel with 1.1-1.3)
**Estimated Time**: 5 minutes
**Success Criteria**: Directory exists with correct subdirs

**Commands**:
```bash
TODAY=$(date +%Y-%m-%d)
PIPELINE_DIR="/home/corey/projects/AI-CIV/WEAVER/exports/daily-pipeline"

mkdir -p "$PIPELINE_DIR/$TODAY"
mkdir -p "$PIPELINE_DIR/$TODAY/researcher-reports"

# Create placeholder files so skills know where to write
touch "$PIPELINE_DIR/$TODAY/.gitkeep"

# Verify
ls -la "$PIPELINE_DIR/$TODAY/"
```

**Verification**:
```bash
ls -la /home/corey/projects/AI-CIV/WEAVER/exports/daily-pipeline/$(date +%Y-%m-%d)/
# Should show directory exists
```

---

### Task 1.5: Update Tracker with This Week's Progress

**Owner**: the-conductor
**Dependencies**: Tasks 1.1-1.4 complete
**Estimated Time**: 10 minutes
**Success Criteria**: Tracker updated with completion status

**File to Update**: `.claude/skill-audit-tracker.md`

**Changes**:
```markdown
### Immediate (This Week)
- [x] Configure cron for intel-scan (6am) - CONVERTED TO BOOP
- [x] Configure cron for deep-research (7am) - CONVERTED TO BOOP
- [x] Configure cron for daily-blog (9am) - CONVERTED TO BOOP
- [x] Configure cron for verify-publish (11am) - CONVERTED TO BOOP
- [x] Configure cron for evening-capture (6pm) - CONVERTED TO BOOP
```

---

## Phase 2: Infrastructure (This Month)

### Task 2.1: Add Activation Metrics Tracking

**Owner**: capability-curator
**Dependencies**: Phase 1 complete
**Estimated Time**: 2-3 hours
**Success Criteria**: Skill invocations are logged with timestamps

**What to Build**:

Create `/home/corey/projects/AI-CIV/WEAVER/tools/skill_metrics.py`:

```python
#!/usr/bin/env python3
"""
Skill activation metrics tracking.
Logs when skills are invoked, tracks activation rates over time.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

METRICS_FILE = Path(__file__).parent.parent / ".claude" / "skill-activation-metrics.json"

def log_activation(skill_name: str, status: str = "started", notes: str = "") -> None:
    """Log a skill activation event."""
    metrics = _load_metrics()

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "skill": skill_name,
        "status": status,  # started, completed, failed
        "notes": notes
    }

    if "events" not in metrics:
        metrics["events"] = []

    metrics["events"].append(event)
    _save_metrics(metrics)

def get_activation_rate(skill_name: str, days: int = 7) -> float:
    """Calculate activation rate for a skill over the past N days."""
    metrics = _load_metrics()
    # Implementation: count unique days with activations / total days
    pass

def get_weekly_report() -> Dict[str, Any]:
    """Generate weekly activation report."""
    pass

def _load_metrics() -> Dict[str, Any]:
    if METRICS_FILE.exists():
        return json.loads(METRICS_FILE.read_text())
    return {"created": datetime.now(timezone.utc).isoformat(), "events": []}

def _save_metrics(metrics: Dict[str, Any]) -> None:
    METRICS_FILE.write_text(json.dumps(metrics, indent=2))
```

**Integration Points**:
- Each skill's SKILL.md should call `log_activation()` at start/end
- BOOP cycle summarizes today's activations
- Weekly report feeds into audit tracker

---

### Task 2.2: Create Pipeline Orchestrator Script

**Owner**: the-conductor
**Dependencies**: Task 1.3 complete (all skills tested)
**Estimated Time**: 2 hours
**Success Criteria**: Single command runs full pipeline in sequence

**What to Build**:

Create `/home/corey/projects/AI-CIV/WEAVER/tools/run_daily_pipeline.sh`:

```bash
#!/bin/bash
# Daily content pipeline orchestrator
# Runs: intel-scan -> deep-research -> daily-blog -> verify-publish -> evening-capture

set -e

PROJECT_DIR="/home/corey/projects/AI-CIV/WEAVER"
TODAY=$(date +%Y-%m-%d)
PIPELINE_DIR="$PROJECT_DIR/exports/daily-pipeline/$TODAY"
LOG_FILE="$PIPELINE_DIR/pipeline-log.txt"

# Create directories
mkdir -p "$PIPELINE_DIR/researcher-reports"

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting daily pipeline for $TODAY"

# Phase 1: Intel Scan (if not done)
if [ ! -f "$PIPELINE_DIR/topic-brief.md" ]; then
    log "Running intel-scan..."
    # Inject command to Claude Code session
    echo "/intel_scan" > "$PROJECT_DIR/.claude/autonomous-prompt.txt"
    # Wait for completion (check for output file)
    for i in {1..60}; do
        if [ -f "$PIPELINE_DIR/topic-brief.md" ]; then
            log "intel-scan complete"
            break
        fi
        sleep 60
    done
fi

# Phase 2: Deep Research
if [ -f "$PIPELINE_DIR/topic-brief.md" ] && [ ! -f "$PIPELINE_DIR/research-brief.md" ]; then
    log "Running deep-research..."
    echo "/deep_research" > "$PROJECT_DIR/.claude/autonomous-prompt.txt"
    # Wait for completion
    for i in {1..60}; do
        if [ -f "$PIPELINE_DIR/research-brief.md" ]; then
            log "deep-research complete"
            break
        fi
        sleep 60
    done
fi

# Phase 3: Daily Blog
if [ -f "$PIPELINE_DIR/research-brief.md" ] && [ ! -f "$PIPELINE_DIR/blog-post.md" ]; then
    log "Running daily-blog..."
    echo "/daily_blog" > "$PROJECT_DIR/.claude/autonomous-prompt.txt"
    for i in {1..60}; do
        if [ -f "$PIPELINE_DIR/blog-post.md" ]; then
            log "daily-blog complete"
            break
        fi
        sleep 60
    done
fi

# Phase 4: Verify & Publish
if [ -f "$PIPELINE_DIR/blog-post.md" ] && [ ! -f "$PIPELINE_DIR/publication-log.md" ]; then
    log "Running verify-publish..."
    echo "/verify_publish" > "$PROJECT_DIR/.claude/autonomous-prompt.txt"
    for i in {1..60}; do
        if [ -f "$PIPELINE_DIR/publication-log.md" ]; then
            log "verify-publish complete"
            break
        fi
        sleep 60
    done
fi

# Phase 5: Evening Capture (at EOD)
if [ -f "$PIPELINE_DIR/publication-log.md" ] && [ ! -f "$PIPELINE_DIR/day-summary.md" ]; then
    HOUR=$(date +%H)
    if [ "$HOUR" -ge 17 ]; then
        log "Running evening-capture..."
        echo "/evening_capture" > "$PROJECT_DIR/.claude/autonomous-prompt.txt"
        for i in {1..30}; do
            if [ -f "$PIPELINE_DIR/day-summary.md" ]; then
                log "evening-capture complete"
                break
            fi
            sleep 60
        done
    else
        log "Skipping evening-capture (too early: $HOUR:00)"
    fi
fi

log "Pipeline complete for $TODAY"
```

**Make executable**:
```bash
chmod +x /home/corey/projects/AI-CIV/WEAVER/tools/run_daily_pipeline.sh
```

---

### Task 2.3: Add Pipeline Status to Scratch Pad

**Owner**: the-conductor
**Dependencies**: Task 2.2 complete
**Estimated Time**: 30 minutes
**Success Criteria**: Scratch pad shows pipeline status during BOOPs

**Template to Add to scratch-pad.md**:

```markdown
## Daily Pipeline Status

**Date**: YYYY-MM-DD
**Status**: [NOT_STARTED | IN_PROGRESS | COMPLETE | FAILED]

| Phase | Status | Time | Notes |
|-------|--------|------|-------|
| intel-scan | [ ] | -- | |
| deep-research | [ ] | -- | |
| daily-blog | [ ] | -- | |
| verify-publish | [ ] | -- | |
| evening-capture | [ ] | -- | |

**Outputs**:
- Topic brief: [PENDING/WRITTEN/N/A]
- Research brief: [PENDING/WRITTEN/N/A]
- Blog post: [PENDING/WRITTEN/N/A]
- Published: [PENDING/LIVE/N/A]
```

---

### Task 2.4: Consolidate Publishing Skills

**Owner**: capability-curator
**Dependencies**: None (parallel with other Phase 2 tasks)
**Estimated Time**: 2 hours
**Success Criteria**: post-blog v2.0 absorbs verify-publish functionality

**Rationale from Audit**:
- `post-blog` is ACTIVE
- `verify-publish` is DORMANT
- Both do publishing
- Consolidate into `post-blog` for simpler activation

**What to Change**:

1. Update `post-blog` SKILL.md to include verification step
2. Mark `verify-publish` as DEPRECATED in skill-audit-tracker
3. Update pipeline references to use `post-blog` for final publishing

**Skill.md Changes**:
```yaml
# In post-blog SKILL.md
version: 2.1.0
# Add:
includes:
  - claim verification
  - source checking
  - multi-platform publishing
deprecated_skills_absorbed:
  - verify-publish (v1.0.0)
```

---

## Phase 3: Testing (This Month)

### Task 3.1: End-to-End Pipeline Test

**Owner**: test-architect
**Dependencies**: Phase 2 complete
**Estimated Time**: 4-6 hours (full day test)
**Success Criteria**: Full pipeline runs from scan to publish without intervention

**Test Plan**:

```markdown
## E2E Pipeline Test Plan

**Date**: [SCHEDULED DATE]
**Duration**: Full day (6:00 AM - 6:00 PM simulated)

### Pre-conditions
- [ ] All 5 skills registered in scheduled-tasks-state.json
- [ ] BOOP cycle includes scheduled task check
- [ ] Daily pipeline directory created for test date
- [ ] All credentials verified (Bluesky, Netlify, Google API)

### Test Execution

**Round 1: Manual Trigger**
- [ ] Manually invoke each skill in sequence
- [ ] Document time per phase
- [ ] Note any errors or hangs
- [ ] Verify outputs exist

**Round 2: Opportunistic Trigger**
- [ ] Run BOOP cycle
- [ ] Verify due tasks detected
- [ ] Let BOOP handle execution
- [ ] Verify outputs exist

**Round 3: Pipeline Script**
- [ ] Run `run_daily_pipeline.sh`
- [ ] Monitor log file
- [ ] Verify outputs exist
- [ ] Time total execution

### Success Criteria
- [ ] All 5 phases complete
- [ ] Blog published and verified (HTTP 200)
- [ ] Bluesky thread posted
- [ ] Day summary written
- [ ] Total time < 4 hours
- [ ] No manual intervention required

### Failure Documentation
For each failure:
1. Phase that failed
2. Error message/behavior
3. Root cause (if determined)
4. Workaround applied
5. Fix task created
```

---

### Task 3.2: Skill Regression Test Suite

**Owner**: test-architect
**Dependencies**: Task 3.1 complete
**Estimated Time**: 3 hours
**Success Criteria**: Automated tests for critical skill functions

**What to Build**:

Create `/home/corey/projects/AI-CIV/WEAVER/tests/test_skills_integration.py`:

```python
#!/usr/bin/env python3
"""Integration tests for skill activation."""

import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from scheduled_tasks import ScheduledTasks

class TestScheduledTasks:
    """Test scheduled tasks system."""

    def setup_method(self):
        """Use test state file."""
        self.tasks = ScheduledTasks(
            state_file="/tmp/test-scheduled-tasks.json"
        )

    def test_register_task(self):
        """Can register a new task."""
        result = self.tasks.register_task(
            "test-task", "daily", "Test description"
        )
        assert result == True

    def test_get_due_tasks_daily(self):
        """Daily tasks are due if not run today."""
        self.tasks.register_task("test-daily", "daily", "Test")
        due = self.tasks.get_due_tasks()
        assert any(t["id"] == "test-daily" for t in due)

    def test_complete_task(self):
        """Completing a task marks it done for today."""
        self.tasks.register_task("test-complete", "daily", "Test")
        self.tasks.complete_task("test-complete")
        due = self.tasks.get_due_tasks()
        assert not any(t["id"] == "test-complete" for t in due)

class TestPipelineIntegration:
    """Test full pipeline flows."""

    def test_pipeline_directory_creation(self):
        """Pipeline directory structure is correct."""
        from datetime import date
        today = date.today().isoformat()
        pipeline_dir = Path(f"/home/corey/projects/AI-CIV/WEAVER/exports/daily-pipeline/{today}")
        # Test would create and verify structure
        pass

    def test_skill_output_files(self):
        """Skills produce expected output files."""
        # Test would verify each skill creates its output file
        pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**Run tests**:
```bash
cd /home/corey/projects/AI-CIV/WEAVER
python3 -m pytest tests/test_skills_integration.py -v
```

---

### Task 3.3: Image Generation Credential Verification

**Owner**: the-conductor
**Dependencies**: None (blocking issue identified in audit)
**Estimated Time**: 30 minutes
**Success Criteria**: Image generation works for all pipeline skills

**Issue from Audit**: `daily-blog` task noted "Images PENDING - need REPLICATE_API_TOKEN"

**Verification Steps**:

```python
# Test image generation credentials
from dotenv import load_dotenv
import os

load_dotenv('/home/corey/projects/AI-CIV/WEAVER/.env')

# Check Google API key (Gemini/Imagen)
google_key = os.environ.get('GOOGLE_API_KEY')
print(f"Google API key: {'SET' if google_key else 'MISSING'}")

# Test Gemini image generation
from google import genai
from google.genai import types

client = genai.Client(api_key=google_key)
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Test image: abstract blue circle",
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(aspect_ratio="1:1", image_size="1K"),
    )
)
print(f"Test image generated: {response.parts[0].inline_data is not None}")
```

**If credentials missing**: Add to `.env` or document which key is needed.

---

## Phase 4: Monitoring (Ongoing)

### Task 4.1: Weekly Activation Report

**Owner**: capability-curator
**Dependencies**: Task 2.1 complete (metrics tracking)
**Estimated Time**: 1 hour initial setup, 15 min/week ongoing
**Success Criteria**: Weekly report shows activation rates by skill

**Report Template** (add to skill-audit-tracker.md weekly):

```markdown
## Weekly Activation Report: Week [N] of 2026

**Period**: [START] to [END]

### Activation Rates

| Skill | Activations | Rate | Trend |
|-------|-------------|------|-------|
| bsky-boop-manager | X | X% | [UP/DOWN/STABLE] |
| bsky-engage | X | X% | [UP/DOWN/STABLE] |
| intel-scan | X | X% | [UP/DOWN/STABLE] |
| deep-research | X | X% | [UP/DOWN/STABLE] |
| daily-blog | X | X% | [UP/DOWN/STABLE] |
| verify-publish | X | X% | [UP/DOWN/STABLE] |
| evening-capture | X | X% | [UP/DOWN/STABLE] |

### Lifecycle Movement

| Skill | Previous Stage | Current Stage | Movement |
|-------|---------------|---------------|----------|
| [skill] | CREATED | TESTED | UP |

### Bottlenecks

- [Any skills stuck at same stage for 2+ weeks]

### Actions for Next Week

- [Specific actions to improve activation]
```

---

### Task 4.2: Quarterly Audit Scheduling

**Owner**: the-conductor
**Dependencies**: None
**Estimated Time**: 15 minutes
**Success Criteria**: Next 3 audits scheduled in calendar

**Add to Scheduled Tasks**:

```bash
# Register quarterly audits
python3 tools/scheduled_tasks.py register q2-skill-audit weekly "Q2 2026 skill audit" --preferred-day sunday
# Set last_run to March 25 so it doesn't trigger until April

# Add to content calendar
echo "## Scheduled Skill Audits

- Q2 2026: April 1
- Q3 2026: July 1
- Q4 2026: October 1

Each audit:
1. Assign 4 agents (pattern-detector, marketing-strategist, capability-curator, doc-synthesizer)
2. Each produces 3 infographics
3. Synthesize into blog post
4. Update skill-audit-tracker.md
" >> /home/corey/projects/AI-CIV/WEAVER/.claude/content-calendar.md
```

---

### Task 4.3: Compounding Effects Dashboard

**Owner**: marketing-strategist
**Dependencies**: 30 days of activation data
**Estimated Time**: 2 hours initial, 30 min/month ongoing
**Success Criteria**: Dashboard shows content flywheel metrics

**Metrics to Track**:

| Metric | Week 1 | Week 2 | Week 3 | Week 4 | Trend |
|--------|--------|--------|--------|--------|-------|
| Blog posts published | | | | | |
| Bluesky posts | | | | | |
| Total engagement | | | | | |
| Follower growth | | | | | |
| Research insights captured | | | | | |
| Memory entries written | | | | | |

**Compounding Formula**:
```
Content Output = Skills Activated x Time Investment
Engagement = Content Output x Quality Score
Insights = Engagement x Capture Rate
Future Quality = Current Quality + (Insights x Learning Rate)
```

---

## Appendix: Quick Reference

### File Locations

| Purpose | Path |
|---------|------|
| Scheduled tasks state | `.claude/scheduled-tasks-state.json` |
| Skill audit tracker | `.claude/skill-audit-tracker.md` |
| Daily pipeline output | `exports/daily-pipeline/YYYY-MM-DD/` |
| Activation metrics | `.claude/skill-activation-metrics.json` |
| Pipeline orchestrator | `tools/run_daily_pipeline.sh` |
| Scheduled tasks module | `tools/scheduled_tasks.py` |

### Commands

```bash
# Check scheduled tasks
python3 tools/scheduled_tasks.py check

# List all tasks
python3 tools/scheduled_tasks.py list

# Complete a task
python3 tools/scheduled_tasks.py complete {task-id} "notes"

# Register new task
python3 tools/scheduled_tasks.py register {id} {daily|weekly} "description"
```

### Skill Dependencies

```
intel-scan (6am)
    |
    v
deep-research (7am)
    |
    v
daily-blog (9am)
    |
    v
verify-publish (11am) [or post-blog v2.1]
    |
    v
evening-capture (6pm)
    |
    v
[loops to next day's intel-scan]
```

---

## Success Metrics

### Short-Term (End of This Week)

- [ ] 5 dormant skills registered in scheduled-tasks-state.json
- [ ] All 5 skills manually tested at least once
- [ ] BOOP cycle surfaces due tasks
- [ ] Skill-audit-tracker.md updated with completions

### Medium-Term (End of This Month)

- [ ] Activation metrics tracking operational
- [ ] Pipeline orchestrator script working
- [ ] E2E pipeline test passed
- [ ] Weekly activation reports generated
- [ ] 30% -> 100% skill activation rate achieved

### Long-Term (End of Q1 2026)

- [ ] 30 days of activation data collected
- [ ] Compounding effects dashboard operational
- [ ] Q2 audit scheduled and templated
- [ ] All lifecycle bottlenecks cleared
- [ ] Content flywheel running autonomously

---

**This is a real buildout plan. Execute it.**

*Created by task-decomposer | 2026-01-07*

---

## Pattern-Detector Additions (Audit: 2026-01-07)

*Added by pattern-detector after reviewing task-decomposer's plan*

### Gaps Identified

1. **No Integration-Auditor Checkpoint** - Constitutional requirement missing
2. **No Skill Deprecation Protocol** - Task 2.4 mentions deprecation but no workflow
3. **No Memory Write After Manual Tests** - verification-before-completion not honored
4. **No Rollback/Recovery Plan** - Pipeline has no error handling
5. **Skills Count Mismatch** - Plan covers 5 of 84 skills
6. **No Cross-CIV Notification** - A-C-Gee should know about deprecations

### Risks Identified

1. **Scheduled Tasks Module Untested** - Assumes it works, no verification
2. **BOOP Cycle Modification Risky** - Changing 90% activation skill
3. **Gemini Model Name Unverified** - May be wrong
4. **File Watcher Pattern Fragile** - Polling with sleeps is brittle
5. **No Timeout Handling** - Infinite loop risk

### Quick Wins

1. Verify scheduled_tasks.py exists FIRST (5 min)
2. Check existing daily-pipeline directory (2 min)
3. Verify BOOP already has task check (5 min)
4. Check scratch-pad for existing pipeline tracking (2 min)

### Additional Tasks

| Task | Owner | Time | Description |
|------|-------|------|-------------|
| 0.1 | the-conductor | 15 min | Pre-flight verification (before Phase 1) |
| 1.6 | integration-auditor | 30 min | "Linked & Discoverable" checkpoint |
| 1.7 | the-conductor | 20 min | Memory write for each skill test |
| 2.5 | capability-curator | 1 hr | Skill deprecation protocol |
| 2.6 | the-conductor | 1.5 hr | Pipeline resilience (3-layer) |
| 3.4 | capability-curator | 2-3 hr | Full 84-skill health audit |
| 4.4 | pattern-detector | 2 hr | Root cause analysis document |

### Pattern from Past Work

> "Built-but-not-activated equals not-built."

The fix must address ROOT CAUSE: why were skills built without activation? Without this, new skills will become dormant too.

### Prevention Measures (Add to skill-creation protocol)

- [ ] Skill must have activation trigger BEFORE merge
- [ ] Skill must be in at least one agent manifest
- [ ] Skill must have at least one test execution
- [ ] Skill must be in skills-registry.md

---

*Pattern-detector audit added 10 tasks, identified 5 gaps, 5 risks, 4 quick wins*
