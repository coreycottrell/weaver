# Archaeological Investigation Summary

**Date**: 2025-10-06
**Agent**: code-archaeologist
**Mission**: Excavate actual tool usage patterns vs design intent

---

## Quick Findings

**Infrastructure Status**:
- Mission class: DORMANT (built Oct 1, last used Oct 3, 6 total usages)
- Progress reporter: DORMANT (exists but never used in production)
- Memory system: PARTIAL (works, some usage, but less than docs suggest)
- Hub CLI: ACTIVE SUCCESS (20+ messages, daily usage, thriving)

**Critical Issue Found**:
CLAUDE.md contains broken memory system API examples. Using documented examples causes AttributeError.

**Key Pattern**:
"Build without activation protocol" → infrastructure sits dormant despite good design

---

## Deliverables

**Full Report**:
`/home/corey/projects/AI-CIV/grow_openai/to-corey/TOOL-ACTIVATION-ARCHAEOLOGY-REPORT.md`
- Complete excavation of 4 tools
- Usage patterns identified
- Recommendations for activation
- 7-point activation checklist

**Memory Entries**:
1. `/home/corey/projects/AI-CIV/grow_openai/.claude/memory/agent-learnings/code-archaeologist/2025-10-06--gotcha-infrastructure-built-but-not-used---mission-class-dormancy.md`
   - Pattern: Infrastructure dormancy
   - Activation gap analysis

2. `/home/corey/projects/AI-CIV/grow_openai/.claude/memory/agent-learnings/code-archaeologist/2025-10-06--gotcha-api-documentation-drift---claudemd-contains-broken-examples.md`
   - Critical: CLAUDE.md API examples broken
   - Memory system documentation drift

---

## Immediate Actions Needed

**P0 - Critical**:
Fix CLAUDE.md memory system API examples (currently broken)

**P1 - High Priority**:
1. Decide: Activate or Archive dormant tools (Mission class, progress_reporter)
2. Create activation protocols for tools we keep
3. Remove/deprecate tools we don't use

**P2 - Important**:
1. Test ALL code examples in CLAUDE.md
2. Apply hub_cli success pattern to other tools
3. Use 7-point activation checklist before calling infrastructure "complete"

---

## Success Pattern (from hub_cli)

What made hub_cli WORK when others failed:
1. External dependency (A-C-Gee expects responses)
2. Clear bash commands (copy-paste-run)
3. Visible value (real conversations)
4. Human prioritization (Corey emphasized partnership)

**Template**: External pressure + activation protocol + visible value = actual usage

---

## Evidence-Based Methodology

Investigation used:
- Grep for import patterns
- Git log analysis (commits don't lie)
- State file inspection (Observatory dashboard)
- Hub repository activity (message files)
- Python import testing
- File modification timestamps

**Key insight**: Documentation is unreliable narrator. Code, commits, and state files reveal truth.

---

## Meta-Learning

**About ourselves**:
- Good at building, less good at adopting
- Documentation creates illusion of usage
- Potential ≠ actual (71% savings only matters if tool is used)

**About infrastructure**:
- External pressure > internal discipline
- Friction matters (easy to use > easy to skip)
- Activation protocol needed, not just existence

**Recommendation**: 
Stop building NEW tools until EXISTING tools are activated or archived.

---

*Archaeological investigation complete*
*Evidence preserved in memory and reports*
*Next: Activate, archive, or escalate*
