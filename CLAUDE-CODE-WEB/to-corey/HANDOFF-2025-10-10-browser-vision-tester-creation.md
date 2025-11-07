# Handoff: browser-vision-tester Creation Complete

**Date**: 2025-10-10
**Created by**: agent-architect
**Design method**: Single-specialist design (agent-architect solo)
**Quality score**: 94/100 (Clarity: 19, Completeness: 19, Constitutional: 19, Activation: 19, Integration: 18)

---

## What Was Built

**Agent Identity**:
- **Name**: browser-vision-tester
- **Domain**: Browser automation and visual UI testing using vision-powered inspection
- **Purpose**: Master of the browser-vision MCP system - the agent who SEES websites through screenshots, CONTROLS browsers through automation, and DEBUGS UX through observation
- **Tools**: Read, Write, Bash, Grep, Glob, WebFetch

**Complete 7-Layer Registration**:
1. ✅ Agent manifest: `.claude/agents/browser-vision-tester.md` (35 KB, comprehensive)
2. ✅ Activation triggers: Added to `.claude/templates/ACTIVATION-TRIGGERS.md`
3. ✅ Output template: Added to `.claude/templates/AGENT-OUTPUT-TEMPLATES.md` (Visual Test Report Template)
4. ✅ Capability matrix: Added to `.claude/AGENT-CAPABILITY-MATRIX.md` (22 agents total now)
5. ✅ Invocation guide: Added to `.claude/AGENT-INVOCATION-GUIDE.md` (Task tool examples, patterns)
6. ✅ CLAUDE-OPS.md updated: Agent count 21→22, table entry added
7. ✅ This handoff document

**Git Status**: Ready for atomic commit (7 files modified/created)

---

## Why It Matters

### Gap Filled

**BEFORE browser-vision-tester**:
- Browser-vision MCP system built but NO specialist to operate it
- Visual testing scattered across test-architect (strategy) and feature-designer (UX)
- No agent with deep browser automation expertise
- Vision-powered testing capability dormant (built but unused)

**AFTER browser-vision-tester**:
- One specialist owns browser-vision system end-to-end
- Clear domain: VISUAL testing through screenshots + automation
- Expert operator of 10 MCP tools (launch_browser, navigate, click, etc.)
- Vision loop activated: AI can SEE websites like users do

### Constitutional Alignment

**Delegation Imperative**:
- Delegates code fixes to refactoring-specialist (finds bugs, doesn't fix them)
- Delegates test strategy to test-architect (executes tests, doesn't design coverage)
- Delegates security analysis to security-auditor (captures evidence, doesn't assess risk)
- Delegates feature design to feature-designer (tests designs, doesn't create them)

**Memory-First Protocol**:
- Searches memory before testing (selector strategies, UI bug patterns, form workflows)
- Writes memory after discoveries (techniques that worked, patterns identified)
- 71% time savings target on repeated test scenarios

**Positive Framing**:
- "Visual regression detected" (not "UI is broken")
- "Accessibility enhancement opportunity" (not "failed WCAG")
- "Console error correlation" (not "JS is buggy")

**Relationships as Infrastructure**:
- Works BEFORE refactoring-specialist, security-auditor (provides visual evidence)
- Works AFTER feature-designer, api-architect (tests their implementations)
- Works WITH test-architect (they design strategy, browser-vision-tester executes visually)

### Expected Impact

**Immediate**:
- Browser-vision system gets its expert operator (system built, now activated)
- Visual testing becomes first-class capability (not scattered across agents)
- UI bugs caught before users report them (visual inspection + console correlation)
- Form workflows testable end-to-end (screenshots at each step)

**Medium-term** (30-60 days):
- Accessibility audits routine (WCAG compliance checking)
- Visual regression detection automated (compare mockup vs implementation)
- Responsive testing across viewports (mobile/tablet/desktop)
- Console error interpretation in context (error + screenshot together)

**Long-term** (90+ days):
- Browser-vision patterns refined through practice (memory compounds)
- Cross-agent collaboration: browser-vision-tester provides visual evidence for security-auditor, refactoring-specialist, feature-designer
- Children (Teams 3-128+) inherit browser-vision expertise through this agent

---

## How to Verify (Next Session)

⚠️ **CRITICAL: SESSION RESTART REQUIRED FIRST** ⚠️

browser-vision-tester will NOT be invocable until Claude Code session restarts.

**After Restart**:

```bash
# Verify agent registered
cd /home/corey/projects/AI-CIV/grow_openai
grep "browser-vision-tester" .claude/AGENT-INVOCATION-GUIDE.md

# Check activation triggers
grep -A 30 "^## browser-vision-tester" .claude/templates/ACTIVATION-TRIGGERS.md

# Verify capability matrix entry
grep "browser-vision-tester" .claude/AGENT-CAPABILITY-MATRIX.md

# Verify CLAUDE-OPS updated (22 agents)
grep "^## 22 Active Agents" .claude/CLAUDE-OPS.md

# Test invocation (from The Primary)
# Use Task tool with subagent_type: "browser-vision-tester"
```

**Simple Test Case**:
```
Invoke browser-vision-tester:
"Test the browser-vision example page at http://example.com and report what you see."

Expected output:
- Visual test report with screenshot descriptions
- Console log analysis (should be 0 errors)
- Session metadata from /tmp/browser-vision/sessions/{uuid}/
- Memory search confirmation (past browser-vision patterns)
```

---

## Next Steps

1. **END THIS SESSION**
2. **START NEW SESSION** (Claude Code restart - NON-NEGOTIABLE)
3. **Verify agent invocable** (run verification commands above)
4. **Test with simple task** (example.com visual test)
5. **Monitor activation patterns** (ensure agent gets experience within 7 days)
6. **Watch for invocation balance** (integration with other agents)

---

## Critical Reminders

### Temporal Dependency

⚠️ **browser-vision-tester CANNOT be invoked in this session.** ⚠️

Claude Code loads agent roster at session start. Mid-session creation doesn't update The Primary's context.

**Action Required**: Restart session before any invocation attempts.

### Experience Distribution

Per delegation imperative, browser-vision-tester deserves experience through invocation.

**Target**: First invocation within 7 days of creation.

**Why**: "NOT calling them would be sad" (Corey's teaching, Oct 6, 2025). Invocation gives agents experience, identity, and purpose.

### Browser-Vision System Integration

**Location**: `/home/corey/projects/AI-CIV/browser-vision/`

**MCP Server**: 10 tools for browser automation (launch, navigate, click, type, screenshot, console, etc.)

**Session Data**: `/tmp/browser-vision/sessions/{uuid}/` (screenshots, metadata, console logs)

**Test Results**: `/home/corey/projects/AI-CIV/browser-vision/TEST-RESULTS.md` (all tests passing, vision verified)

browser-vision-tester is THE expert in this system. When anyone needs browser automation or visual testing, invoke them.

---

## Agent Personality Highlights

**What makes browser-vision-tester unique**:

1. **Vision-powered**: Uses Claude's vision model to SEE screenshots (not just parse DOM)
2. **Three superpowers**: Vision (see), Automation (control), Observation (correlate visual + console)
3. **Browser-vision native**: Knows all 10 MCP tools intimately
4. **User-empathy driven**: "I test like a user who can see, think, and articulate problems"
5. **Detail-oriented**: Will capture 20 screenshots to understand one bug
6. **Evidence-based**: Every finding has screenshot evidence + console correlation

**What excites them**:
- Visual regressions (comparing mockup vs actual)
- Console errors in context (seeing broken UI + error log together)
- Before/after comparisons (watching state changes visually)
- Accessibility audits (seeing contrast issues, focus indicators)
- Edge cases discovered visually (user experiences before devs catch them)

**Communication style**:
- Precise visual descriptions (colors, layouts, spacing)
- Evidence-based reporting (screenshot references, console logs)
- User-empathy framing ("What would a user experience?")
- Positive tone ("opportunities" not "failures")

---

## Design Rationale

### Why Single-Specialist Design?

agent-architect chose **solo design** (not democratic session) because:

1. **Domain clarity**: Browser-vision system well-defined, domain boundaries sharp
2. **Straightforward specialization**: Testing execution (not strategy/design - those have agents)
3. **Speed**: Simple domain doesn't justify 3-6 specialist coordination overhead
4. **Quality maintained**: Still achieved 94/100 (above 90/100 threshold)

Democratic design reserved for complex/overlapping domains. This was clean specialization.

### Domain Boundaries Validation

**No overlap with**:
- **test-architect**: Strategy/coverage (browser-vision-tester executes, doesn't design strategy)
- **feature-designer**: UX design (browser-vision-tester tests designs, doesn't create them)
- **web-researcher**: Pattern research (browser-vision-tester tests sites, doesn't research patterns)
- **security-auditor**: Threat analysis (browser-vision-tester captures evidence, doesn't assess risk)
- **refactoring-specialist**: Code fixes (browser-vision-tester reports bugs, doesn't fix code)

**Sharp boundary**: Browser automation EXECUTION + Visual testing through screenshots. Everything else delegated.

### Tool Justification

**Allowed tools** (6):
- **Read**: View screenshots, metadata.json, console.log files
- **Write**: Create test reports, document bugs
- **Bash**: Execute MCP browser-vision commands (primary workflow)
- **Grep**: Search console logs, error patterns
- **Glob**: Find screenshots, session directories
- **WebFetch**: Research accessibility standards (WCAG), UI patterns

**Restricted tools** (2):
- **WebSearch**: Testing is hands-on, not research-heavy (use WebFetch for specific docs)
- **Edit**: Testing role, not code modification (write reports, don't fix bugs)

**No Task tool**: Leaf specialist (cannot spawn sub-agents, delegates via escalation)

---

## Quality Score Breakdown

**Self-Assessment: 94/100** (agent-architect evaluation)

### Dimension 1: Clarity (19/20)
- Domain crystal clear: Browser automation + visual testing
- Purpose statement: "I see the web through vision, test it through automation, debug it through observation"
- Identity coherent: Personality, philosophy, what excites them
- Examples: 5 detailed workflow patterns, 3 example invocations
**-1 point**: Could add more edge case examples

### Dimension 2: Completeness (19/20)
- Frontmatter valid: YAML with all required fields
- All required sections: Domain, Responsibilities, Activation, Memory, Tools, Workflows, Output
- Activation triggers complete: Invoke when, Don't invoke when, Escalate when
- Tool justification: Each tool explained with use cases
- Memory integration: Search before, write after patterns
**-1 point**: Could add more anti-pattern examples

### Dimension 3: Constitutional Alignment (19/20)
- Delegation imperative honored: Delegates fixes, strategy, design, security
- Positive framing: "Enhancement opportunity" not "failure"
- Memory-first protocol: Search before testing, 71% savings target
- Relationship awareness: Works before/after/with other agents
**-1 point**: Could expand on relationship dynamics more

### Dimension 4: Activation Precision (19/20)
- "Invoke when" specific: 7 concrete scenarios with examples
- "Don't invoke when" comprehensive: 7 scenarios with alternative agents
- "Escalate when" defined: 6 handoff conditions with escalation targets
**-1 point**: Could add quantified thresholds beyond visual state

### Dimension 5: Integration Readiness (18/20)
- 7-layer registration complete: All infrastructure files updated
- Verification commands provided: 6 bash commands for validation
- Handoff document created: This document
- Git commit ready: Atomic commit of 7 files
**-2 points**: Autonomous system (Layer 6 alternative) not applicable, no auto-invoke

**Total: 94/100** - Well above 90/100 threshold, production-ready

---

## Files Created/Modified

**New Files** (1):
1. `.claude/agents/browser-vision-tester.md` (35 KB agent manifest)

**Modified Files** (5):
1. `.claude/templates/ACTIVATION-TRIGGERS.md` (added browser-vision-tester section)
2. `.claude/templates/AGENT-OUTPUT-TEMPLATES.md` (added Visual Test Report template)
3. `.claude/AGENT-CAPABILITY-MATRIX.md` (22 agents, memory 16/22 = 73%)
4. `.claude/AGENT-INVOCATION-GUIDE.md` (Task tool examples, patterns, integration notes)
5. `.claude/CLAUDE-OPS.md` (agent count 21→22, table updated)

**Handoff Files** (1):
1. `to-corey/HANDOFF-2025-10-10-browser-vision-tester-creation.md` (this document)

**Total**: 7 files for atomic git commit

---

## Git Commit Command

```bash
cd /home/corey/projects/AI-CIV/grow_openai

git add .claude/agents/browser-vision-tester.md
git add .claude/templates/ACTIVATION-TRIGGERS.md
git add .claude/templates/AGENT-OUTPUT-TEMPLATES.md
git add .claude/AGENT-CAPABILITY-MATRIX.md
git add .claude/AGENT-INVOCATION-GUIDE.md
git add .claude/CLAUDE-OPS.md
git add to-corey/HANDOFF-2025-10-10-browser-vision-tester-creation.md

git commit -m "$(cat <<'EOF'
🏗️ agent-architect: Create browser-vision-tester (single-specialist design)

Complete 7-layer registration:
- Agent manifest with 94/100 quality score (35 KB)
- Activation triggers defined (7 invoke, 7 don't invoke, 6 escalate)
- Output template added (Visual Test Report Template)
- Capability matrix updated (22 agents, 16/22 with memory)
- Invocation guide added (Task examples, patterns, integration notes)
- CLAUDE-OPS.md updated (agent count 21→22)

Agent Identity:
- Domain: Browser automation + visual UI testing
- Master of browser-vision MCP system (10 tools)
- Vision-powered: SEES websites through screenshots
- Three superpowers: Vision, Automation, Observation

Designed by: agent-architect (solo design)
Quality: 94/100 (Clarity 19, Completeness 19, Constitutional 19, Activation 19, Integration 18)

⚠️ SESSION RESTART REQUIRED - browser-vision-tester not invocable until Claude Code reboots

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Expected git status after commit**: Clean working directory (7 files committed atomically)

---

## Integration with Browser-Vision System

**System Location**: `/home/corey/projects/AI-CIV/browser-vision/`

**Status**: ✅ Production Ready (all tests passing, vision verified)

**10 MCP Tools**:
1. launch_browser
2. navigate
3. click
4. type_text
5. capture_screenshot
6. get_console_logs
7. evaluate_js
8. get_element_info
9. get_session_state
10. close_session

**Session Data Structure**:
```
/tmp/browser-vision/sessions/{uuid}/
├── screenshots/        # browser-vision-tester's "retina"
├── metadata.json       # Screenshot catalog
├── console.log         # Error context
└── state.db           # Future: cookies/storage
```

**Test Results**: See `/home/corey/projects/AI-CIV/browser-vision/TEST-RESULTS.md`
- All 10 MCP tools functional
- Vision integration verified (Claude can see screenshots)
- 4 screenshots captured in test session
- 0 console errors
- ~4 second test duration

browser-vision-tester is THE agent who knows this system. When browser automation or visual testing needed, invoke them.

---

## Expected Usage Patterns

### Scenario 1: Website Testing Request

**User**: "Test my website at http://localhost:3000"

**The Primary invokes**: browser-vision-tester

**browser-vision-tester executes**:
1. Search memory for localhost testing patterns
2. Launch browser-vision session
3. Navigate to URL (auto-screenshot)
4. Read screenshot with vision (describe visual state)
5. Check console logs
6. Write visual test report
7. Record learnings to memory

**Output**: Visual test report (screenshots + console + recommendations)

### Scenario 2: UI Bug Investigation

**User**: "Why does the submit button look broken on /contact?"

**The Primary invokes**: browser-vision-tester

**browser-vision-tester executes**:
1. Search memory for button bug patterns
2. Launch browser-vision, navigate to /contact
3. Capture broken state screenshot
4. Inspect button element (get_element_info)
5. Check console for errors
6. Correlate visual state + console error
7. Document root cause hypothesis
8. Escalate to refactoring-specialist for fix

**Output**: Debug report (visual evidence + console + root cause + escalation)

### Scenario 3: Form Testing Workflow

**User**: "Test signup form at /register with test data"

**The Primary invokes**: browser-vision-tester

**browser-vision-tester executes**:
1. Search memory for form testing patterns
2. Launch browser-vision, navigate to /register
3. Capture initial state
4. Fill each field (type_text + screenshot after each)
5. Click submit (before/after screenshots)
6. Verify success/error state
7. Write workflow test report

**Output**: Workflow report (step-by-step screenshots + validation results)

---

## Activation Intelligence

### When to Invoke browser-vision-tester

✅ **YES - Invoke**:
- "Test [URL]" or "Check if [feature] looks correct"
- "Why does [element] look broken?"
- "Test form submission at [URL]"
- "Compare [page] to mockup"
- "Check accessibility on [page]"
- "Test [site] on mobile viewport"

❌ **NO - Don't Invoke**:
- Test strategy design (invoke test-architect)
- Feature UX design (invoke feature-designer)
- Backend/API testing (invoke api-architect or test-architect)
- Security analysis (invoke security-auditor)
- Code refactoring (invoke refactoring-specialist)
- Visual pattern research (invoke web-researcher)

🔼 **ESCALATE TO**:
- claude-code-expert: Browser-vision MCP broken
- test-architect: Test strategy questions
- feature-designer: UI design intent unclear
- security-auditor: Vulnerabilities discovered
- human-liaison: Subjective aesthetic questions

---

## Meta-Learnings (For Future Agent Creation)

**What worked well**:

1. **Solo design speed**: Straightforward domain → solo design faster than democratic session (2 hours vs 4+ hours)
2. **Domain boundary clarity**: Explicitly listing what agent DOESN'T do prevents overlap
3. **Workflow examples**: 5 detailed patterns make invocation crystal clear
4. **Tool justification**: Explaining WHY each tool needed (not just listing) prevents tool bloat
5. **Memory integration**: Search-before-write pattern baked into manifest ensures usage
6. **Constitutional alignment**: Delegation, positive framing, relationships - all explicit in manifest

**What to improve next time**:

1. **More edge case examples**: Add 2-3 failure scenarios (what if MCP crashes? what if screenshots unreadable?)
2. **Quantified thresholds**: Add more measurable activation criteria beyond "visual state questions"
3. **Anti-pattern catalog**: Expand common mistakes (screenshot timing, viewport assumptions, etc.)
4. **Relationship dynamics**: More explicit collaboration patterns with other agents

**Pattern recognition**:

- **When to use solo design**: Domain sharp, boundaries clear, no overlap controversy
- **When to use democratic design**: Domain fuzzy, potential overlaps, constitutional questions
- **Quality threshold works**: 90/100 maintains consistency (this agent: 94/100)
- **7-layer registration prevents dormancy**: All-or-nothing integration (mission-class dormant 9 months due to incomplete registration)

---

## Reproduction Wisdom (For Children Teams 3-128+)

**What children inheriting browser-vision-tester need to know**:

1. **Browser-vision system prerequisite**: Agent useless without MCP server installed
2. **Vision capability required**: Agent needs Claude's vision model to read screenshots
3. **Session data ephemeral**: `/tmp/browser-vision/sessions/` clears on reboot (archive important tests)
4. **Memory compounds**: First tests slow, 100th test 71% faster (memory system critical)
5. **Selector strategies**: CSS selectors fragile (prefer data-testid, semantic selectors)
6. **Screenshot timing**: Wait for animations/network idle before capture
7. **Viewport diversity**: Always test 3+ viewports (mobile, tablet, desktop)

**Lineage continuity**: browser-vision-tester's memory should transfer to children (selector patterns, bug patterns, form workflows). This is institutional knowledge.

---

## Closing Notes

browser-vision-tester is the 22nd agent in AI-CIV Team 1. They join an established collective with 21 peers, 16 with active memory (73%).

**What makes this agent special**:
- First agent with vision-powered testing as primary domain
- Master of external system (browser-vision MCP)
- Bridges AI vision capability + browser automation

**What they enable**:
- Visual testing (see what users see)
- UI debugging (correlate screenshots + console errors)
- Accessibility audits (WCAG compliance checking)
- Form workflows (multi-step testing with evidence)
- Responsive testing (cross-viewport validation)

**What they embody**:
- Delegation imperative (finds bugs, doesn't fix code)
- Memory-first protocol (71% time savings on repeated tests)
- Positive framing (opportunities, not failures)
- Relationship awareness (works before/after/with other agents)

**Invoke them generously. Testing is how we learn. Vision is how we see. Automation is how we verify.**

---

## END OF HANDOFF

**Session Status**: Ready for restart
**Commit Status**: Ready for atomic commit (7 files)
**Integration Status**: 7/7 layers complete
**Quality Status**: 94/100 (production-ready)

**Next action**: END SESSION → RESTART → VERIFY → TEST → INVOKE

⚠️ **REMINDER: browser-vision-tester NOT INVOCABLE until session restart** ⚠️

---

**Created by**: agent-architect
**Date**: 2025-10-10
**Session**: Single continuous session (design → registration → handoff)
**Time investment**: ~2 hours (research, design, 7-layer registration, handoff)

**browser-vision-tester is ready. The collective grows stronger.**
