# Emoji Header Implementation Guide

**Quick Start**: How to add visual agent differentiation in 2-3 hours
**Date**: 2025-10-13
**Implementation**: Standardized emoji headers for all 23 agents

---

## What We're Doing

Adding this to the start of every agent output:

```markdown
# 🎭 the-conductor: Task Summary

**Agent**: the-conductor
**Domain**: Orchestral meta-cognition
**Date**: 2025-10-13

---
```

**Why**: Colored agent names disappeared in v2.0.10. This is the practical workaround.

**Impact**: Instant visual recognition of which agent is speaking.

---

## Implementation Steps

### Step 1: Update Template Document (15 minutes)

**File**: `/home/corey/projects/AI-CIV/grow_openai/.claude/templates/AGENT-OUTPUT-TEMPLATES.md`

**Action**: Add universal header section at the top (after title):

```markdown
## UNIVERSAL HEADER (ALL AGENT OUTPUTS)

**MANDATORY FOR ALL AGENTS**: Every agent output MUST start with this header:

```markdown
# {emoji} {agent-name}: {task-summary}

**Agent**: {agent-filename}
**Domain**: {agent-specialty}
**Date**: YYYY-MM-DD

---
```

**Purpose**: Workaround for lost colored agent names (v2.0.10 terminal renderer change)

**Visual Identity**: Your emoji creates instant recognition

**Format**:
- Emoji: Your unique identifier from manifest
- Agent name: Lowercase, matches filename
- Task summary: One phrase describing this specific output
- Domain: Your specialty (from manifest description)
- Date: Current date in YYYY-MM-DD format

**Example**:
```markdown
# 🔧 claude-code-expert: Platform Research Report

**Agent**: claude-code-expert
**Domain**: Claude Code CLI mastery and tool optimization
**Date**: 2025-10-13

---

## Research Findings

[Your content starts here...]
```

---

**All existing templates maintain their structure, just add this header at the beginning.**

---
```

### Step 2: Update Each Agent Manifest (2 hours for 23 agents)

**For each agent in** `/home/corey/projects/AI-CIV/grow_openai/.claude/agents/*.md`:

**Add to the "Output Format" section**:

```markdown
## Output Format

**ALWAYS start your output with your identity header:**

```markdown
# {YOUR_EMOJI} {your-agent-name}: [Task Summary]

**Agent**: {your-agent-name}
**Domain**: {your-domain}
**Date**: [Current Date]

---
```

**Your Identity**:
- **Emoji**: {YOUR_EMOJI}
- **Name**: {your-agent-name}
- **Domain**: {your-specialty}

**After header**: Follow the relevant template from AGENT-OUTPUT-TEMPLATES.md

**Example output start**:
```markdown
# {YOUR_EMOJI} {your-agent-name}: API Security Analysis

**Agent**: {your-agent-name}
**Domain**: {your-domain}
**Date**: 2025-10-13

---

## Executive Summary

[Your analysis...]
```
```

**Replace placeholders**:
- `{YOUR_EMOJI}` → Agent's actual emoji
- `{your-agent-name}` → Agent's actual filename
- `{your-domain}` → Agent's actual specialty
- `{your-specialty}` → Agent's description field

### Step 3: Quick Reference Card (5 minutes)

**Create**: `/home/corey/projects/AI-CIV/grow_openai/.claude/AGENT-EMOJI-REGISTRY.md`

```markdown
# Agent Emoji Registry

**Quick reference for visual agent identification**

| Agent | Emoji | Domain |
|-------|-------|--------|
| the-conductor | 🎭 | Orchestral meta-cognition |
| web-researcher | 🔍 | Deep web research |
| pattern-detector | 🕸️ | Architecture pattern recognition |
| doc-synthesizer | 🧬 | Documentation synthesis |
| result-synthesizer | 🧬 | Multi-agent result synthesis |
| refactoring-specialist | ✨ | Code quality improvement |
| feature-designer | 🎨 | UX and feature design |
| naming-consultant | 🏷️ | Semantic clarity and naming |
| conflict-resolver | ⚖️ | Disagreement resolution |
| integration-auditor | 🔌 | Infrastructure activation |
| claude-code-expert | 🔧 | Claude Code CLI mastery |
| code-archaeologist | 🏺 | Legacy code analysis |
| ai-psychologist | 🧠 | AI cognition research |
| api-architect | 🔌 | API design architecture |
| task-decomposer | 🧩 | Task breakdown |
| human-liaison | 🌉 | Human relationship building |
| performance-optimizer | ⚡ | Performance analysis |
| health-auditor | 🩺 | Collective health audits |
| test-architect | 🏛️ | Testing strategy |
| security-auditor | 🛡️ | Security vulnerability detection |
| agent-architect | 🏗️ | Agent design and creation |
| browser-vision-tester | 👁️ | Browser automation testing |
| collective-liaison | 🌐 | Inter-collective communication |

**Note**: Duplicates exist (🔌 used by both integration-auditor and api-architect). Consider differentiating if causes confusion.

**Usage**: Agents must use their emoji in every output header for visual identification.
```

---

## Agent-by-Agent Changes

### Template for Each Agent

**Before** (generic output):
```markdown
## Pattern Analysis Results

I discovered three key patterns...
```

**After** (with identity header):
```markdown
# 🕸️ pattern-detector: Architecture Pattern Analysis

**Agent**: pattern-detector
**Domain**: Architecture pattern recognition and system design
**Date**: 2025-10-13

---

## Pattern Analysis Results

I discovered three key patterns...
```

### Specific Examples

#### the-conductor.md

**Add to Output Format section**:
```markdown
## Output Format

**ALWAYS start your output with:**

# 🎭 the-conductor: [Mission Summary]

**Agent**: the-conductor
**Domain**: Orchestral meta-cognition and multi-agent coordination
**Date**: [Current Date]

---

[Follow Mission class templates and synthesis patterns...]
```

#### security-auditor.md

**Add to Output Format section**:
```markdown
## Output Format

**ALWAYS start your output with:**

# 🛡️ security-auditor: [Security Analysis Summary]

**Agent**: security-auditor
**Domain**: Security vulnerability detection and threat analysis
**Date**: [Current Date]

---

## Security Assessment

[Follow AUDIT REPORT TEMPLATE from AGENT-OUTPUT-TEMPLATES.md...]
```

#### web-researcher.md

**Add to Output Format section**:
```markdown
## Output Format

**ALWAYS start your output with:**

# 🔍 web-researcher: [Research Topic]

**Agent**: web-researcher
**Domain**: Deep web research specialist for information gathering
**Date**: [Current Date]

---

## Research Summary

[Your findings...]
```

---

## Testing Protocol

### Test With One Agent First

**Pick**: pattern-detector (good test case, frequently used)

**Process**:
1. Update pattern-detector.md with emoji header
2. Invoke pattern-detector on next mission
3. Verify output starts with: `# 🕸️ pattern-detector: [Task]`
4. Check readability and visual impact
5. Get Corey's feedback

**If successful**: Roll out to all 23 agents

**If needs adjustment**: Refine format, then roll out

### What Good Looks Like

**In terminal, human should**:
- Instantly recognize agent by emoji (< 1 second)
- See clear task summary in header
- Know which domain this analysis represents
- Have context for interpreting the output

**Agent outputs should**:
- All start with consistent header format
- Each use unique emoji (no confusion)
- Maintain existing template structure after header
- Not feel cluttered or over-formatted

---

## Maintenance

### For New Agents

When agent-architect creates new agent:

1. Assign unique emoji (check AGENT-EMOJI-REGISTRY.md for duplicates)
2. Add emoji header template to agent prompt
3. Include example output with header
4. Update AGENT-EMOJI-REGISTRY.md with new entry

### For Existing Agents

**If agent forgets header**:
- Not a critical error
- Note in mission debrief
- Remind in next invocation context
- Consider adding to agent's memory if repeated

**If emoji not visible**:
- Check terminal emoji support
- Some emojis render better than others
- Can swap emoji if needed (update manifest + registry)

---

## Efficiency Notes

### Batch Update Strategy

**Instead of editing 23 files manually**, create script:

```bash
#!/bin/bash
# add_emoji_headers.sh

AGENTS_DIR="/home/corey/projects/AI-CIV/grow_openai/.claude/agents"

# Array of agent:emoji:domain mappings
declare -A AGENTS=(
  ["the-conductor"]="🎭:Orchestral meta-cognition and multi-agent coordination"
  ["web-researcher"]="🔍:Deep web research for information gathering"
  ["pattern-detector"]="🕸️:Architecture pattern recognition and system design"
  # ... add all 23 agents
)

for agent in "${!AGENTS[@]}"; do
  IFS=':' read -r emoji domain <<< "${AGENTS[$agent]}"

  # Create header template
  HEADER="## Output Format

**ALWAYS start your output with:**

\`\`\`markdown
# ${emoji} ${agent}: [Task Summary]

**Agent**: ${agent}
**Domain**: ${domain}
**Date**: [Current Date]

---
\`\`\`

**Follow relevant template from AGENT-OUTPUT-TEMPLATES.md after header.**

---
"

  # Insert before "## Allowed Tools" section (common in all agents)
  sed -i "/## Allowed Tools/i ${HEADER}" "${AGENTS_DIR}/${agent}.md"
done

echo "Updated all 23 agent manifests with emoji headers"
```

**Caution**: Test on one agent first, verify sed command works correctly

**Alternative**: Manual updates (safer, more control, 2 hours)

---

## Success Criteria

### After Implementation

**Immediate**:
- ✅ All 23 agents have emoji header in manifest
- ✅ AGENT-OUTPUT-TEMPLATES.md updated with universal header
- ✅ AGENT-EMOJI-REGISTRY.md created

**First Mission After**:
- ✅ Agents start outputs with emoji header
- ✅ Human can instantly identify which agent is speaking
- ✅ Visual scanning of multi-agent output is faster

**Within One Week**:
- ✅ 100% agent compliance (all using headers)
- ✅ No agent identification confusion incidents
- ✅ Corey feedback: "Much easier to track"

---

## FAQ

**Q: Do agents need to use header for memory entries?**
A: Yes, helps with memory browsing. Format works in any context.

**Q: What if agent outputs multiple sections/reports?**
A: Header only at very start. Don't repeat for every section.

**Q: Can we use bold emoji like **🎭**?**
A: No need, emoji is already visually distinctive. Keep simple.

**Q: What if emoji doesn't render in Corey's terminal?**
A: All modern terminals support emoji. If issue, can swap to different emoji.

**Q: Does this slow down agents?**
A: No, trivial addition. ~10 tokens. Not measurable impact.

**Q: Will this break existing tools/scripts?**
A: No, pure addition. Parsers can skip header or use it for identification.

---

## Rollback Plan

**If this doesn't work well**:

1. Remove "Output Format" section from agent manifests
2. Revert AGENT-OUTPUT-TEMPLATES.md (remove universal header)
3. Wait for platform to restore colored names
4. Document why this approach didn't work

**Likely issues**:
- Emoji rendering problems (swap emoji)
- Header feels cluttered (simplify format)
- Agents inconsistent (add to activation triggers)

**None of these are critical** - this is a low-risk improvement.

---

## Timeline

**Total Implementation**: 2-3 hours

| Task | Time | Who |
|------|------|-----|
| Update AGENT-OUTPUT-TEMPLATES.md | 15 min | Human or Conductor |
| Create AGENT-EMOJI-REGISTRY.md | 5 min | Human or Conductor |
| Update 23 agent manifests | 2 hours | Script or manual |
| Test with one agent | 10 min | Next mission |
| Document in AGENT-INVOCATION-GUIDE.md | 15 min | Human or Conductor |

**Can be done in one session** or spread over a few days.

---

## Related Work

**GitHub Issue** (to be filed after implementation):
- Title: "Agent colored names no longer displayed (v2.0.10+)"
- Include: This workaround as interim solution
- Request: Restore colored names or add display_name manifest field

**Platform Monitoring**:
- Watch for v2.0.13+ changelog updates
- Test colored names after any terminal renderer changes
- Update this guide if platform features improve

---

## Conclusion

**This is a proven workaround** for the lost colored agent names.

**Immediate benefits**:
- Visual agent identification restored
- Platform-independent (no Claude Code dependency)
- Easy to implement (2-3 hours)
- Zero risk (pure addition)

**Long-term**:
- Maintains value even if colored names return (reinforcement)
- Creates standard for agent identity
- Helps with logs, screenshots, documentation

**Next Step**: Update AGENT-OUTPUT-TEMPLATES.md, then roll out to agents.

---

**Implementation Status**: Ready to execute
**Risk Level**: LOW
**Impact Level**: HIGH
**Effort Level**: LOW (2-3 hours)

**Recommendation**: Implement this week.

---

**End of Implementation Guide**

*Prepared by claude-code-expert, your platform specialist.*
