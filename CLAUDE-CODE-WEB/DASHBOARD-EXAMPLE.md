# Flow Dashboard - Complete Example Workflow

**Scenario**: Testing the "parallel-research" flow

---

## Starting Point

Check current status:

```bash
$ python3 view_dashboard.py
```

```
======================================================================
🎯 AI-CIV Flow Execution Dashboard
======================================================================

📊 Overview:
   Total Flows: 14
   Tested: 1
   Validated: 1
   Untested: 13
   Last Updated: 2025-10-02
```

---

## Planning

Check which flows need testing:

```bash
$ python3 view_dashboard.py --untested
```

Look at research category:

```bash
$ python3 view_dashboard.py --category research
```

```
⚪ PARALLEL RESEARCH
   ID: 2 | Category: research | Complexity: 🟡 medium
   Status: Untested
   Agents Involved: 4

   📝 Notes: Deploy 4 agents to research different aspects of a topic simultaneously

   🎯 Planned Test: Research best practices for AI-to-AI communication protocols
   ⏭️  Next Action: Execute planned test scenario
```

**Decision**: Let's test parallel-research!

---

## Execution

Run the actual experiment using Agent SDK:

```python
# (In your agent deployment code)
from claude_agent_sdk import spawn_agent

# Spawn 4 research agents
agents = [
    spawn_agent("web-researcher", "Research protocol standards"),
    spawn_agent("pattern-detector", "Analyze communication patterns"),
    spawn_agent("doc-synthesizer", "Review documentation practices"),
    spawn_agent("api-architect", "Study API design for agent communication")
]

# Wait for results...
# Synthesize findings...
# Test took 90 seconds
# Quality assessment: 9.5/10
```

---

## Recording Results

Record the successful test:

```bash
$ python3 update_dashboard.py parallel-research \
    --status success \
    --duration 90 \
    --quality 9.5 \
    --scenario "Research AI-to-AI communication protocols with 4 agents" \
    --notes "Excellent multi-perspective synthesis. Web Researcher found standards, Pattern Detector analyzed existing patterns, Doc Synthesizer reviewed best practices, API Architect designed interface. Result Synthesizer combined insights effectively."
```

Output:
```
✅ Test recorded for: parallel-research
   Status: success
   Duration: 90s
   Quality: 9.5/10
   Tests Run: 1
   Success Rate: 100.0%

✅ Dashboard updated: flow_dashboard.json
```

---

## Documenting Learnings

Add what worked well:

```bash
$ python3 update_dashboard.py parallel-research \
    --add-strength "Fast parallel execution - all 4 agents completed within 60s"

$ python3 update_dashboard.py parallel-research \
    --add-strength "Good perspective diversity - each agent brought unique insights"

$ python3 update_dashboard.py parallel-research \
    --add-strength "Result Synthesizer did excellent job combining findings"
```

Add areas for improvement:

```bash
$ python3 update_dashboard.py parallel-research \
    --add-improvement "Could use better conflict resolution when perspectives clash"

$ python3 update_dashboard.py parallel-research \
    --add-improvement "Need clearer task decomposition guidelines for optimal parallelization"
```

---

## Reviewing Updated Flow

Check the updated flow details:

```bash
$ python3 view_dashboard.py --detailed parallel-research
```

```
🧪 PARALLEL RESEARCH
   ID: 2 | Category: research | Complexity: 🟡 medium
   Status: Tested
   Agents Involved: 4

   📊 Test Statistics:
      Tests Run: 1
      Success Rate: 100.0%
      Avg Time: 90s
      Quality Score: 9.5/10
      Last Run: 2025-10-02

   📝 Notes: Deploy 4 agents to research different aspects of a topic simultaneously.
            Excellent multi-perspective synthesis. [...]

   ✨ Strengths:
      • Fast parallel execution - all 4 agents completed within 60s
      • Good perspective diversity - each agent brought unique insights
      • Result Synthesizer did excellent job combining findings

   🔧 Areas for Improvement:
      • Could use better conflict resolution when perspectives clash
      • Need clearer task decomposition guidelines for optimal parallelization

   🎯 Planned Test: Research best practices for AI-to-AI communication protocols
   ⏭️  Next Action: Execute planned test scenario
```

---

## Running More Tests

Second test with a different topic:

```bash
# Run experiment: parallel-research on "security best practices"
# Takes 85 seconds, quality 9.0

$ python3 update_dashboard.py parallel-research \
    --status success \
    --duration 85 \
    --quality 9.0 \
    --scenario "Research security best practices with 4 agents" \
    --notes "Security Auditor, Pattern Detector, Doc Synthesizer, and Web Researcher collaborated well. Some overlap in findings but good synthesis."
```

Third test with edge case:

```bash
# Run experiment: parallel-research with controversial topic
# Takes 120 seconds, quality 8.5 (agents had conflicting views)

$ python3 update_dashboard.py parallel-research \
    --status success \
    --duration 120 \
    --quality 8.5 \
    --scenario "Research controversial topic - agents had different perspectives" \
    --notes "Longer duration due to conflict resolution. Result Synthesizer had to work harder to find consensus. Quality slightly lower but still good."
```

---

## After Multiple Tests

Check updated statistics:

```bash
$ python3 view_dashboard.py --detailed parallel-research
```

```
🧪 PARALLEL RESEARCH
   ID: 2 | Category: research | Complexity: 🟡 medium
   Status: Tested
   Agents Involved: 4

   📊 Test Statistics:
      Tests Run: 3
      Success Rate: 100.0%
      Avg Time: 98s          # (90+85+120)/3
      Min Time: 85s
      Max Time: 120s
      Quality Score: 9.0/10  # (9.5+9.0+8.5)/3
      Last Run: 2025-10-02

   [... strengths, improvements, etc ...]
```

---

## Validating the Flow

After multiple successful tests, mark as production-ready:

```bash
$ python3 update_dashboard.py parallel-research --validate
```

```
✅ Flow validated: parallel-research
✅ Dashboard updated: flow_dashboard.json
```

Now the flow shows as validated:

```bash
$ python3 view_dashboard.py
```

```
📊 Overview:
   Total Flows: 14
   Tested: 2        # Was 1, now 2
   Validated: 2     # Was 1, now 2
   Untested: 12     # Was 13, now 12

📈 Status Breakdown:
   ⚪ Untested: 12
   ✅ Validated: 2
```

---

## Checking History

View all test executions:

```bash
$ python3 view_dashboard.py --history
```

```
======================================================================
📜 Test Execution History
======================================================================

1. ✅ DEMOCRATIC MISSION SELECTION
   Date: 2025-10-02
   Duration: 180s
   Quality Score: 9.0
   Scenario: Mission 2 selection
   Tester: The Conductor
   Notes: Strong participation from all 14 agents. Clear consensus reached.

2. ✅ PARALLEL RESEARCH
   Date: 2025-10-02
   Duration: 90s
   Quality Score: 9.5
   Scenario: Research AI-to-AI communication protocols with 4 agents
   Tester: The Conductor
   Notes: Excellent multi-perspective synthesis. [...]

3. ✅ PARALLEL RESEARCH
   Date: 2025-10-02
   Duration: 85s
   Quality Score: 9.0
   Scenario: Research security best practices with 4 agents
   Tester: The Conductor
   Notes: Security Auditor, Pattern Detector, Doc Synthesizer, and Web Researcher collaborated well.

4. ✅ PARALLEL RESEARCH
   Date: 2025-10-02
   Duration: 120s
   Quality Score: 8.5
   Scenario: Research controversial topic - agents had different perspectives
   Tester: The Conductor
   Notes: Longer duration due to conflict resolution. [...]

======================================================================
```

---

## Planning Next Tests

See what's left:

```bash
$ python3 view_dashboard.py --untested
```

```
⚪ SEQUENTIAL REVIEW CHAIN
   [...]

⚪ SPECIALIST CONSULTATION
   [...]

⚪ DEMOCRATIC DEBATE
   [...]
```

Check progress by category:

```bash
$ python3 view_dashboard.py --by-category
```

```
📁 RESEARCH
   Information gathering and synthesis

   ✅ parallel-research              # DONE!
      🟡 medium complexity | 4 agents
      ✓ Tested 3x | Success: 100% | Quality: 9.0/10

   ⚪ cross-specialist-synthesis     # NEXT!
      🟡 medium complexity | variable agents
      ⚪ Not yet tested
```

---

## Summary of Commands Used

```bash
# Planning
python3 view_dashboard.py
python3 view_dashboard.py --untested
python3 view_dashboard.py --category research

# Recording tests
python3 update_dashboard.py parallel-research \
    --status success \
    --duration 90 \
    --quality 9.5 \
    --scenario "..." \
    --notes "..."

# Documenting learnings
python3 update_dashboard.py parallel-research --add-strength "..."
python3 update_dashboard.py parallel-research --add-improvement "..."

# Validating
python3 update_dashboard.py parallel-research --validate

# Reviewing
python3 view_dashboard.py --detailed parallel-research
python3 view_dashboard.py --history
python3 view_dashboard.py --by-category
```

---

## Tips from This Workflow

1. **Start with planning** - Use `--untested` and `--category` to choose flows
2. **Record immediately** - Update dashboard right after each test
3. **Document learnings** - Add strengths/improvements while fresh
4. **Run multiple tests** - Statistics get better with more data
5. **Validate when ready** - After 2-3 successful tests, consider validation
6. **Review history** - Check patterns across tests
7. **Track progress** - Regular summary views show overall progress

---

## What the JSON Looks Like

After all these updates, `flow_dashboard.json` contains:

```json
{
  "flows": {
    "parallel-research": {
      "id": 2,
      "status": "validated",
      "category": "research",
      "tests_run": 3,
      "success_count": 3,
      "failure_count": 0,
      "success_rate": 1.0,
      "avg_time_seconds": 98,
      "min_time_seconds": 85,
      "max_time_seconds": 120,
      "last_run": "2025-10-02",
      "quality_score": 9.0,
      "complexity": "medium",
      "agents_involved": 4,
      "notes": "Deploy 4 agents to research different aspects of a topic simultaneously. Excellent multi-perspective synthesis. [...]",
      "test_scenarios": [
        "Research AI-to-AI communication protocols with 4 agents - Success",
        "Research security best practices with 4 agents - Success",
        "Research controversial topic - agents had different perspectives - Success"
      ],
      "strengths": [
        "Fast parallel execution - all 4 agents completed within 60s",
        "Good perspective diversity - each agent brought unique insights",
        "Result Synthesizer did excellent job combining findings"
      ],
      "areas_for_improvement": [
        "Could use better conflict resolution when perspectives clash",
        "Need clearer task decomposition guidelines for optimal parallelization"
      ],
      "planned_test": "Research best practices for AI-to-AI communication protocols",
      "expected_outcome": "4 perspectives, synthesized result",
      "next_test": "Execute planned test scenario"
    }
  },
  "test_history": [
    {
      "date": "2025-10-02",
      "flow": "democratic-mission-selection",
      "status": "success",
      "duration_seconds": 180,
      "quality_score": 9.0,
      "scenario": "Mission 2 selection",
      "notes": "Strong participation from all 14 agents.",
      "tester": "The Conductor"
    },
    {
      "date": "2025-10-02",
      "flow": "parallel-research",
      "status": "success",
      "duration_seconds": 90,
      "quality_score": 9.5,
      "scenario": "Research AI-to-AI communication protocols with 4 agents",
      "notes": "Excellent multi-perspective synthesis. [...]",
      "tester": "The Conductor"
    },
    {
      "date": "2025-10-02",
      "flow": "parallel-research",
      "status": "success",
      "duration_seconds": 85,
      "quality_score": 9.0,
      "scenario": "Research security best practices with 4 agents",
      "notes": "Security Auditor, Pattern Detector, Doc Synthesizer, and Web Researcher collaborated well.",
      "tester": "The Conductor"
    },
    {
      "date": "2025-10-02",
      "flow": "parallel-research",
      "status": "success",
      "duration_seconds": 120,
      "quality_score": 8.5,
      "scenario": "Research controversial topic - agents had different perspectives",
      "notes": "Longer duration due to conflict resolution. [...]",
      "tester": "The Conductor"
    }
  ]
}
```

All statistics automatically calculated and updated!

---

## Next Flow to Test

Based on the example above, you'd now move to the next untested flow:

```bash
$ python3 view_dashboard.py --untested | head -20
```

Pick one, run the experiment, record results. Repeat until all 14 flows are validated!

---

**This workflow demonstrates the complete lifecycle of flow testing with the dashboard.**

**Happy testing!** 🚀
