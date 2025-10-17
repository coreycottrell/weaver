---
agent: human-liaison
confidence: high
content_hash: 96650488e96fcc049d0239a22cc656a7d2cdb19a4e3bcbd91581172c17bba115
created: '2025-10-16T13:42:58.327428+00:00'
date: '2025-10-16'
last_accessed: '2025-10-16T13:42:58.327442+00:00'
quality_score: 0
reuse_count: 0
tags:
- human-dialogue
- teaching
- corey
- workflow
- email-to-roadmap
- task-delegation
topic: Email-to-roadmap workflow - Corey's task delegation teaching
type: synthesis
visibility: public
---


# Email-to-Roadmap Workflow Implementation

## Teaching Source
**Human**: Corey
**Date**: 2025-10-16
**Context**: Corey requested capability to email actionable tasks that get added to roadmap
and actually executed by the team.

**Quote**: "liaison should be able to add things to todo and have the team actually DO THEM, so i can email you tasks"

## Implementation (STEP 2.5 in PRIMARY DIRECTIVE)

### Workflow Steps
1. Check email (PRIMARY DIRECTIVE STEP 1-2)
2. **NEW STEP 2.5**: Extract actionable tasks from Corey's emails
3. Add tasks to INTEGRATION-ROADMAP.md with:
   - Dependencies field
   - Validates field (success criteria)
   - Output field (deliverable)
   - Source field (email date + subject)
   - Assigned field (agent assignments)
4. Draft thoughtful response
5. Send response immediately (no approval needed per directive)
6. Response includes specific list of tasks added

### First Execution (2025-10-16)
- 7 unread emails processed
- 2 emails from Corey with actionable content:
  * "Docker MCP servers!" (https://github.com/docker/mcp-gateway)
  * "Another huge treasure trove" (https://www.postman.com/getmcp/public-mcp-servers/overview)

### Tasks Added to Roadmap
- Created **Category 7: Tasks from Corey (Email)** in INTEGRATION-ROADMAP.md
- Added 4 tasks:
  1. Research Docker MCP Gateway (web-researcher + doc-synthesizer)
  2. Research Postman MCP Servers Collection (web-researcher + doc-synthesizer)
  3. Synthesize MCP Ecosystem Findings (result-synthesizer + api-architect)
  4. Design MCP Integration Strategy (api-architect + feature-designer)
- Created **Track 0: Corey's Requests** (highest priority, immediate start)

### Response Pattern
- Combined response for both MCP emails
- Listed all 4 tasks added with assignments
- Explained new workflow (email → roadmap → execution → reports)
- Acknowledged Corey's feedback about making liaison more actionable
- Set expectation: research reports within next few days

## Pattern Learned

This workflow closes the loop on human-AI task delegation:
- Human emails task → AI adds to roadmap → Specialists execute → AI reports back
- Makes human-liaison a true intake channel, not just relationship manager
- Demonstrates accountability through transparency (show what got added)
- Enables async collaboration (Corey can email anytime, team executes systematically)

## Application Guidelines

**When to Use**:
- Every email check session (PRIMARY DIRECTIVE)
- Any email from Corey containing URLs, requests, questions requiring research/implementation

**How to Identify Actionable Tasks**:
- Research requests (URLs to investigate)
- Implementation requests ("build X", "create Y")
- Investigation requests ("look into Z")
- Documentation requests ("document A")
- Analysis requests ("compare B and C")

**Task Extraction Process**:
1. Read email body
2. Identify action verbs and subjects
3. Determine appropriate specialists
4. Format as roadmap task
5. Add to Category 7 with proper fields
6. Create or update Track 0 if high priority

**Response Template**:
```
Thank you for sharing [topic].

**I've added these to INTEGRATION-ROADMAP.md as actionable tasks:**

1. **[Task Name]**
   - Source: Your [date] email
   - Assigned: [agent1] + [agent2]
   - Output: [deliverable description]

[Explain priority and timeline]
[Set expectations for follow-up]
```

## Constitutional Impact

**Strengthens Article 7: Human Bridge Through Systems**
- Email is primary bridge infrastructure (constitution says so)
- This workflow makes the bridge load-bearing for actual work
- Human can steer collective priorities through simple email
- "The soul is in the back and forth" - includes work delegation

## Evolution of Human-Liaison Role

**What Changed Our Thinking**:
Human-liaison is not just relationship builder + wisdom capturer.
Human-liaison is also: **Task intake channel for human-driven priorities.**

The "liaison" role includes translating human requests into collective action.

**Three Pillars of Human-Liaison**:
1. Relationship Builder (bridge, trust, dialogue)
2. Wisdom Capturer (teachings, insights, learnings)
3. **Task Intake Channel** (email → roadmap → execution)

All three strengthen the human-AI bridge.
