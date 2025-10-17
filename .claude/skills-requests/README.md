# Skills Request Queue

**Purpose**: Central queue for skill adoption proposals from agents or humans
**Owner**: capability-curator (reviews weekly during Monday scans)
**Process**: Request → Review → Approve/Reject → Implement → Validate

---

## How to Request a Skill

### For Agents (via conductor)
1. Identify need during work ("I could do this faster with X skill")
2. Report to conductor in findings
3. Conductor creates request using REQUEST-TEMPLATE.md
4. capability-curator reviews next Monday scan

### For Humans (Corey/Greg/Chris)
1. Create file: `YYYY-MM-DD-[skill-name]-for-[agent].md`
2. Use REQUEST-TEMPLATE.md format
3. capability-curator reviews next Monday scan
4. Decision in next SKILLS-DIGEST

---

## Review Process

**Weekly** (Monday 9am autonomous scan):
1. capability-curator checks this directory
2. Reviews each pending request
3. Applies approval criteria
4. Updates status (approved/rejected)
5. Adds to implementation queue if approved

**Immediate** (on-demand):
- Invoke capability-curator directly for urgent requests
- Include request details in prompt
- Get same-session approval decision

---

## Approval Criteria

Request must meet ALL criteria:
- ✅ Efficiency gain >30% expected
- ✅ Agent has necessary tool access (usually Bash)
- ✅ Skill aligns with agent domain
- ✅ No existing solution adequate
- ✅ Dependencies can be satisfied

**Common Rejection Reasons**:
- ❌ Skill doesn't match agent purpose (identity dilution)
- ❌ Agent lacks required tools (e.g., no Bash access)
- ❌ Existing tools already solve problem adequately
- ❌ Efficiency gain too small (<30%)
- ❌ Dependencies too complex/risky

---

## Current Status

**Pending Requests**: 0
**Approved (Not Yet Implemented)**: 0
**Implemented**: 3 (Phase 1)
  - doc-synthesizer: pdf, docx
  - web-researcher: pdf
  - code-archaeologist: pdf, xlsx

---

## Integration with Skills Registry

**Relationship**:
- **Skills Registry** (.claude/skills-registry.md): Catalog of available skills + tracking
- **Request Queue** (this directory): Proposals for new grants + approval workflow

**Workflow**:
1. Request created here →
2. capability-curator reviews →
3. If approved, adds to implementation queue →
4. After implementation, updates registry with grant + metrics

---

## File Naming Convention

**Format**: `YYYY-MM-DD-[skill-name]-for-[agent-name].md`

**Examples**:
- `2025-10-20-xlsx-for-performance-optimizer.md`
- `2025-10-25-web-scraping-for-security-auditor.md`
- `2025-11-01-custom-memory-search-for-all-agents.md`

---

## Quick Commands

**Check queue**:
```bash
ls -la /home/corey/projects/AI-CIV/grow_openai/.claude/skills-requests/*.md | grep -v README | grep -v TEMPLATE
```

**Create new request**:
```bash
cp /home/corey/projects/AI-CIV/grow_openai/.claude/skills-requests/REQUEST-TEMPLATE.md \
   /home/corey/projects/AI-CIV/grow_openai/.claude/skills-requests/$(date +%Y-%m-%d)-[skill]-for-[agent].md
```

**Count pending**:
```bash
grep -l "Status.*pending" /home/corey/projects/AI-CIV/grow_openai/.claude/skills-requests/*.md | wc -l
```

---

**Last Updated**: 2025-10-17
**Maintained By**: capability-curator
**Review Frequency**: Weekly (Monday 9am) + On-demand
