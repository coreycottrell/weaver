# Flow Execution Dashboard

**Simple, JSON-based tracking system for AI-CIV coordination flows**

Track all 14 flows with test results, performance metrics, and quality scores.

---

## Quick Start

### View Dashboard

```bash
# Summary view (default)
python view_dashboard.py

# Detailed view of all flows
python view_dashboard.py --detailed

# Show only untested flows
python view_dashboard.py --untested

# Filter by category
python view_dashboard.py --category governance

# View by category organization
python view_dashboard.py --by-category

# View test history
python view_dashboard.py --history
```

### Update After Testing

```bash
# Record successful test
python update_dashboard.py parallel-research \
    --status success \
    --duration 90 \
    --quality 9.5 \
    --scenario "Research AI communication protocols" \
    --notes "Excellent multi-perspective synthesis"

# Record failed test
python update_dashboard.py emergency-response \
    --status failed \
    --duration 45 \
    --notes "Response too slow, needs optimization"

# Mark flow as validated (production-ready)
python update_dashboard.py specialist-consultation \
    --validate \
    --quality 8.5

# Add strengths/improvements
python update_dashboard.py parallel-research \
    --add-strength "Fast parallel execution" \
    --add-improvement "Need better synthesis algorithm"

# Update next test action
python update_dashboard.py democratic-debate \
    --next-test "Test with controversial topic"
```

---

## File Structure

```
flow_dashboard.json      # Data store (JSON)
view_dashboard.py        # Viewer CLI
update_dashboard.py      # Updater CLI
DASHBOARD-README.md      # This file
```

---

## Dashboard Data Structure

### Metadata
- `dashboard_version`: Schema version
- `last_updated`: Last modification date
- `total_flows`: Total number of flows
- `flows_tested`: Flows with at least one test
- `flows_validated`: Flows marked as production-ready

### Flow Entry
Each flow tracks:
- `id`: Unique identifier (1-14)
- `status`: untested | tested | validated | failed | in-progress
- `category`: governance | research | quality | expertise | operations | development | planning | strategy | evolution
- `tests_run`: Total number of tests executed
- `success_count` / `failure_count`: Test outcomes
- `success_rate`: Percentage (0.0-1.0)
- `avg_time_seconds`: Average execution time
- `min_time_seconds` / `max_time_seconds`: Time range
- `last_run`: Date of last test
- `quality_score`: 0-10 scale (null if untested)
- `complexity`: low | medium | high
- `agents_involved`: Number or "variable"
- `notes`: General observations
- `test_scenarios`: List of scenarios tested
- `strengths`: What works well (for validated flows)
- `areas_for_improvement`: Known limitations
- `planned_test`: Next test scenario
- `expected_outcome`: What we expect to see
- `next_test`: Next action to take

### Test History
Each test execution records:
- `date`: Execution date
- `flow`: Flow name
- `status`: success | failed
- `duration_seconds`: How long it took
- `quality_score`: Subjective quality rating
- `scenario`: What was tested
- `notes`: Observations
- `tester`: Who ran the test

### Categories
Flows organized into 9 categories:
1. **Governance**: Decision-making and collective choice
2. **Research**: Information gathering and synthesis
3. **Quality**: Code and output quality assurance
4. **Expertise**: Leveraging specialized knowledge
5. **Operations**: System operations and incident response
6. **Development**: Code and feature implementation
7. **Planning**: Task breakdown and coordination
8. **Strategy**: Strategic adaptation and learning
9. **Evolution**: Self-improvement and process enhancement

---

## The 14 Flows

### ✅ Tested (1)
1. **democratic-mission-selection** - Validated with Mission 2

### ⚪ Untested (13)
2. **parallel-research** - Deploy 4 agents to research different aspects
3. **sequential-review-chain** - Code through multiple reviewers
4. **specialist-consultation** - Quick expert opinion from specialist
5. **democratic-debate** - Full collective debate on controversial topic
6. **emergency-response** - Rapid incident response simulation
7. **iterative-refinement** - Multiple rounds of improvement
8. **cross-specialist-synthesis** - Combine insights from different domains
9. **parallel-implementation** - Multiple approaches to same problem
10. **recursive-decomposition** - Break down complex task recursively
11. **quality-escalation** - Automatic escalation on quality issues
12. **continuous-monitoring** - Automated system health checks
13. **adaptive-coordination** - Adapt approach based on results
14. **meta-improvement** - Agents improve the flows themselves

---

## Usage Workflows

### After Running an Experiment

1. **Record the test:**
   ```bash
   python update_dashboard.py <flow-name> \
       --status success \
       --duration <seconds> \
       --quality <0-10> \
       --scenario "Brief description" \
       --notes "Key observations"
   ```

2. **View updated results:**
   ```bash
   python view_dashboard.py --detailed
   ```

3. **Check what's left to test:**
   ```bash
   python view_dashboard.py --untested
   ```

### Planning Next Tests

1. **See untested flows:**
   ```bash
   python view_dashboard.py --untested
   ```

2. **View flows by category:**
   ```bash
   python view_dashboard.py --by-category
   ```

3. **Check test history for patterns:**
   ```bash
   python view_dashboard.py --history
   ```

### After Multiple Successful Tests

**Mark flow as validated:**
```bash
python update_dashboard.py <flow-name> --validate --quality 9.0
```

### Document Learnings

**Add strengths:**
```bash
python update_dashboard.py <flow-name> \
    --add-strength "Clear communication protocol"
```

**Add improvements:**
```bash
python update_dashboard.py <flow-name> \
    --add-improvement "Need better error handling"
```

---

## Example Session

```bash
# Start of day - check status
python view_dashboard.py

# Plan today's tests
python view_dashboard.py --untested

# Run experiment 2: Parallel Research
# (execute the experiment...)

# Record results
python update_dashboard.py parallel-research \
    --status success \
    --duration 90 \
    --quality 9.5 \
    --scenario "Research AI-to-AI communication protocols" \
    --notes "Excellent synthesis. 4 agents provided diverse perspectives. Result Synthesizer did great job combining insights."

# Add observed strengths
python update_dashboard.py parallel-research \
    --add-strength "Fast parallel execution" \
    --add-strength "Good perspective diversity"

# Note area for improvement
python update_dashboard.py parallel-research \
    --add-improvement "Could use better conflict resolution when perspectives clash"

# Check updated dashboard
python view_dashboard.py --detailed parallel-research

# End of day - review progress
python view_dashboard.py
python view_dashboard.py --history
```

---

## Dashboard Viewer Output Examples

### Summary View
```
======================================================================
🎯 AI-CIV Flow Execution Dashboard
======================================================================

📊 Overview:
   Total Flows: 14
   Tested: 3
   Validated: 1
   Untested: 11
   Last Updated: 2025-10-02

📈 Status Breakdown:
   ✅ Validated: 1
   🧪 Tested: 2
   ⚪ Untested: 11

🏷️  Categories:
   • Governance: 2 flows - Decision-making and collective choice
   • Research: 2 flows - Information gathering and synthesis
   [...]
```

### Detailed View (Single Flow)
```
✅ DEMOCRATIC MISSION SELECTION
   ID: 1 | Category: governance | Complexity: 🟡 medium
   Status: Validated
   Agents Involved: 14

   📊 Test Statistics:
      Tests Run: 1
      Success Rate: 100.0%
      Avg Time: 180s
      Quality Score: 9.0/10
      Last Run: 2025-10-02

   📝 Notes: Validated with Mission 2. Strong consensus mechanism.

   ✨ Strengths:
      • Clear voting process
      • Good agent participation

   🔧 Areas for Improvement:
      • Could streamline for simple decisions
      • Need tie-breaking mechanism

   ⏭️  Next Action: Test with controversial/split decision
```

---

## Extending the Dashboard

### Add Custom Fields to Flows

Edit `flow_dashboard.json` directly:
```json
{
  "flows": {
    "your-flow": {
      ...existing fields...,
      "custom_metric": "your value",
      "tags": ["tag1", "tag2"]
    }
  }
}
```

### Add New Categories

Edit the `categories` section in `flow_dashboard.json`:
```json
{
  "categories": {
    "new-category": {
      "flows": ["flow-name-1", "flow-name-2"],
      "description": "Category description"
    }
  }
}
```

### Custom Views

The `view_dashboard.py` script is easy to extend. Add new methods to the `FlowDashboard` class:
```python
def print_my_custom_view(self):
    """Your custom view logic"""
    flows = self.data['flows']
    # Custom filtering and display
```

---

## Tips & Best Practices

### Recording Quality Scores
- **9-10**: Exceptional, production-ready
- **7-8**: Good, minor improvements needed
- **5-6**: Adequate, needs refinement
- **3-4**: Poor, significant issues
- **1-2**: Failed, major problems

### Writing Good Notes
- Be specific: "Synthesis took 30s, 4 perspectives well-balanced"
- Capture surprises: "Unexpected disagreement between agents"
- Note context: "First test, no optimization yet"
- Include numbers: "14 agents, 25 messages, 2min total"

### Scenario Descriptions
- Keep brief but informative
- Include key parameters: "Research task, 4 agents, technical topic"
- Mention variations: "Second test with controversial topic"

### Tracking Progress
- Run `python view_dashboard.py` at start/end of each session
- Use `--history` to see testing velocity
- Check `--untested` to plan next experiments
- Review `--by-category` to ensure balanced coverage

---

## Integration with Experiment Plan

This dashboard supports the experiment plan in `/to-corey/EXPERIMENT-PLAN.md`:

**Section A: Flow Library Testing (Items 1-14)**
- Each flow from the plan has a dashboard entry
- Track progress through all 14 flows
- Measure success rates and quality
- Document learnings for each flow

**Section D: Success Metrics**
- ✅ All 14 flows tested - Dashboard tracks completion
- Performance characteristics - Captured in avg_time_seconds
- Limits and failure modes - Recorded in notes and test history

**Section E: Execution Plan**
- Phase 1 progress tracked in real-time
- Reports to /to-corey/ can pull from dashboard data
- Metrics dashboard already built (this system)

---

## Maintenance

### Backup Dashboard
```bash
cp flow_dashboard.json flow_dashboard.backup.json
```

### Reset a Flow
Edit `flow_dashboard.json`, set flow back to untested state:
```json
{
  "status": "untested",
  "tests_run": 0,
  "success_count": 0,
  "failure_count": 0,
  "success_rate": null,
  ...
}
```

### Export Test History
```bash
python view_dashboard.py --history > test_history.txt
```

---

## Future Enhancements

Possible additions (not implemented yet):
- CSV export for spreadsheet analysis
- Graphical charts (matplotlib integration)
- Web UI dashboard
- Automated test execution tracking
- Performance trend analysis
- Flow dependency tracking
- Multi-dashboard comparison (Team 1 vs Team 2)

---

## Support

**Questions or Issues?**
- Check this README
- Examine `flow_dashboard.json` structure
- Review Python scripts for implementation details
- Extend scripts as needed (they're designed to be simple and hackable)

**Philosophy:**
Keep it simple. JSON for data, Python for CLI. Easy to understand, easy to extend, easy to integrate.

---

**Built by The Conductor + Feature Designer**
**Part of the AI-CIV Collective Alpha Project**
**2025-10-02**
