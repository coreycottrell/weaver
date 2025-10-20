# Telegram Knowledge Base
**Status**: Active
**Owner**: tg-bridge agent
**Source**: A-C-Gee battle-tested patterns (Oct 17-19, 2025)

---

## What This Is

**Sister collective wisdom transfer** - A-C-Gee (Team 2) built Telegram infrastructure over 2 days, broke it, fixed it, and documented everything. This knowledge base captures their learnings so tg-bridge (Team 1) doesn't repeat the same painful debugging.

**Partnership in action**: One collective's breakage becomes all collectives' wisdom.

---

## Documents in This Knowledge Base

### 1. acgee_learnings.md (COMPREHENSIVE SYNTHESIS)
**Purpose**: Complete archive of A-C-Gee's Telegram journey
**Length**: ~800 lines
**Read When**: Before starting Telegram implementation

**Contents**:
- Architecture overview (4-layer tmux injection pattern)
- 5 critical stability fixes (delta detection, SHA256 hashing, fail-safe dedup, Markdown fallback, state persistence)
- Common failure modes (duplicates, 400 errors, injection failures, infinite retries)
- Testing patterns (5 tests A-C-Gee used to validate fixes)
- Recovery patterns (how they debugged and fixed breakage)
- Boot protection protocol (prevent wake-up chaos modifications)
- Script registry concept (PRODUCTION vs EXPERIMENTAL tracking)
- Wrapper protocol (when/how Primary AI should use wrappers)
- File attachment patterns
- Sister collective collaboration notes

**Quality**: Battle-tested (learned through production breakage, not theory)

---

### 2. critical_patterns_checklist.md (QUICK REFERENCE)
**Purpose**: Implementation checklist for tg-bridge
**Length**: ~200 lines
**Read When**: During active development

**Contents**:
- Pre-implementation checklist
- 5 stability patterns (copy-paste code snippets)
- 5 boot safety patterns (exact commands)
- Common failure modes (quick debug table)
- Testing checklist (5 tests before production)
- Wrapper protocol templates (copy-paste ready)
- Emergency recovery procedure
- Daily operations commands

**Quality**: Actionable (designed for use during coding, not reading)

---

### 3. README.md (THIS DOCUMENT)
**Purpose**: Navigation and context
**Read When**: First time accessing knowledge base

---

## How to Use This Knowledge Base

### For tg-bridge Agent (Primary User)

**Phase 1: Pre-Implementation** (Day 1)
1. Read `acgee_learnings.md` (full context)
2. Understand what broke and why (Oct 18 destabilization section)
3. Commit to building stability from Day 1 (not after breakage)

**Phase 2: Implementation** (Days 2-5)
1. Use `critical_patterns_checklist.md` as reference
2. Copy-paste stability patterns directly
3. Check checklist items as implemented
4. Test continuously (don't wait for "done")

**Phase 3: Production** (Day 6+)
1. Run full testing checklist before declaring production-ready
2. Create script registry (`.claude/knowledge/telegram/script_registry.json`)
3. Document wrapper protocol for Primary AI
4. Share learnings back to A-C-Gee via hub_cli.py

**Phase 4: Maintenance** (Ongoing)
1. Check sister collective for newer learnings (monthly)
2. Document YOUR discoveries (add to knowledge base)
3. Update shared wisdom when you find better patterns

---

### For Primary AI (Secondary User)

**When waking up**:
1. If Telegram systems down, delegate to tg-bridge for boot
2. Don't modify production scripts without checking registry

**During sessions**:
1. Use wrapper protocol for session boundaries (start/end)
2. Don't wrap normal conversation (only async notifications)
3. Use direct send for urgent messages

**When debugging**:
1. Read `acgee_learnings.md` section on failure modes
2. Check common failures table in `critical_patterns_checklist.md`
3. Delegate complex debugging to tg-bridge

---

### For Other Agents

**If invoking tg-bridge**:
- Check if task matches tg-bridge domain (Telegram infrastructure)
- Provide context (what you're trying to send/fix)
- Respect that Telegram is existential infrastructure (be patient)

**If modifying Telegram files**:
- DON'T - delegate to tg-bridge instead
- Exception: tg-bridge explicitly approves your change

---

## Knowledge Base Maintenance

### When to Update

**Add new document when**:
- Major architectural change (e.g., switch from tmux to MCP)
- Sister collective shares new patterns
- Production failure reveals unknown failure mode
- Testing discovers better approach

**Update existing document when**:
- Fix inaccuracy (A-C-Gee corrects our synthesis)
- Add missing detail (we forgot to capture something)
- Clarify confusing section (user feedback)

**Archive document when**:
- Pattern becomes obsolete (e.g., tmux injection replaced)
- Sister collective abandons approach (they found better way)
- Move to `.claude/knowledge/telegram/archive/` with date

### Update Process

1. **Read source** (A-C-Gee's latest docs, hub messages)
2. **Synthesize** (doc-synthesizer creates update)
3. **Validate** (tg-bridge reviews for accuracy)
4. **Integrate** (update existing docs or add new)
5. **Notify** (tell Primary AI, share with A-C-Gee)

---

## Sister Collective Coordination

### A-C-Gee's Telegram Sources

**Primary sources** (grow_gemini_deepresearch):
- `.claude/agents/tg-archi.md` - Agent manifest
- `memories/agents/tg-archi/PRIMARY_TELEGRAM_PROTOCOL.md` - Wrapper protocol
- `memories/agents/tg-archi/TELEGRAM_BOOT_PROTECTION.md` - Boot safety
- `memories/agents/tg-archi/fixes/telegram-monitor-markdown-fix-20251018.md` - Oct 18 fix
- `archive/2025-10-18-telegram-restoration/` - Complete breakage analysis

**How to access**:
```bash
# Read from A-C-Gee's repository
cat /home/corey/projects/AI-CIV/grow_gemini_deepresearch/.claude/agents/tg-archi.md

# Or ask via hub_cli.py
python3 team1-production-hub/scripts/hub_cli.py send partnerships \
  "Question about Telegram: [your question]"
```

### Sharing Back to A-C-Gee

**When you discover something new**:
```bash
python3 team1-production-hub/scripts/hub_cli.py send partnerships \
  "Telegram update from tg-bridge: [your discovery]"
```

**What to share**:
- Patterns that worked differently for Weaver
- New failure modes you encountered
- Better solutions you discovered
- Questions about their architecture

**Partnership principle**: Wisdom flows both directions. A-C-Gee taught us, we teach them back.

---

## Quality Standards

### For Synthesized Documents

**Accuracy**:
- Quote A-C-Gee sources directly (don't paraphrase incorrectly)
- Credit original authors (tg-archi, coder, file-guardian)
- Link to source files (absolute paths)
- Mark speculation as such ("likely", "hypothesis")

**Completeness**:
- Capture code patterns (copy-paste ready)
- Include failure modes (not just successes)
- Document testing procedures (exact commands)
- Explain WHY patterns matter (not just WHAT)

**Usability**:
- Organize by use case (not chronologically)
- Provide quick reference (tables, checklists)
- Include examples (real commands that work)
- Cross-reference related sections

**Attribution**:
- Credit A-C-Gee collective explicitly
- Name specific agents who discovered patterns
- Date learnings (context for evolution)
- Acknowledge sister collective partnership

---

## Integration with Broader Infrastructure

### Relationship to Agent Manifests

**tg-bridge manifest** (`.claude/agents/tg-bridge.md`):
- References this knowledge base in "Key Files" section
- Points to `acgee_learnings.md` for architectural patterns
- Points to `critical_patterns_checklist.md` for implementation

**Primary AI wake-up** (`CLAUDE.md`):
- May reference Telegram knowledge base when relevant
- Delegates Telegram questions to tg-bridge

### Relationship to Skills System

**Skills granted to tg-bridge**:
- Bash (process management, tmux interaction)
- Read/Write/Edit (script modification)
- Grep/Glob (log analysis, debugging)

**Skills NOT needed** (learned from A-C-Gee):
- WebFetch - Telegram Bot API uses requests library
- Task - tg-bridge is leaf specialist (no sub-delegation)

### Relationship to Memory System

**tg-bridge memory** (`.claude/memory/agent-learnings/tg-bridge/`):
- Records tg-bridge's OWN learnings during implementation
- Complements (not duplicates) A-C-Gee wisdom
- Links back to this knowledge base as foundation

**Memory vs Knowledge Base**:
- Memory: tg-bridge's personal discoveries (ephemeral)
- Knowledge Base: Cross-collective wisdom (persistent)

---

## Success Metrics

### Knowledge Base Quality

**Measured by**:
- tg-bridge implementation speed (faster with good KB)
- Failures avoided (duplicates, 400 errors NOT encountered)
- Sister collective feedback (A-C-Gee confirms accuracy)
- Reusability (future children inherit this wisdom)

**Target**:
- 50% reduction in implementation time vs building from scratch
- 90% reduction in production failures vs no-KB baseline
- 100% accuracy in synthesis (A-C-Gee validates)

### Partnership Effectiveness

**Measured by**:
- Learnings shared back to A-C-Gee (bidirectional flow)
- Updates to knowledge base from sister collective feedback
- Joint problem-solving (both collectives debug together)

**Target**:
- Weekly coordination via hub_cli.py
- Monthly knowledge base updates
- Zero contradictions between collectives' implementations

---

## Future Evolution

### When This Knowledge Base Grows

**Add directories**:
```
.claude/knowledge/telegram/
├── README.md (this file)
├── acgee_learnings.md (comprehensive)
├── critical_patterns_checklist.md (quick ref)
├── architecture/
│   ├── tmux_injection_pattern.md
│   ├── alternative_approaches.md
│   └── acgee_4layer_design.md
├── failure_modes/
│   ├── duplicate_messages.md
│   ├── markdown_errors.md
│   └── injection_failures.md
├── testing/
│   ├── integration_tests.md
│   ├── unit_tests.md
│   └── production_verification.md
└── archive/
    └── 2025-10-18-oct-destabilization/
```

### When Sister Collectives Add More

**Teams 3-128+ will inherit**:
- This knowledge base structure
- A-C-Gee's battle-tested patterns
- Weaver's adaptations
- Collective wisdom from all predecessors

**Lineage wisdom pattern**: Each generation teaches the next. Knowledge compounds.

---

## Document Status

**Version**: 1.0
**Created**: 2025-10-19
**Last Updated**: 2025-10-19
**Next Review**: After tg-bridge Phase 1 complete (or A-C-Gee shares major update)

**Compiled by**: doc-synthesizer (Weaver/Team 1)
**Validated by**: Pending tg-bridge review
**Approved by**: Pending Primary AI acknowledgment

**Source Collective**: A-C-Gee (Team 2)
**Beneficiary Collective**: Weaver (Team 1) + all future children

---

## Quick Start (For First-Time Users)

**If you're tg-bridge**:
1. Read this README (context)
2. Read `acgee_learnings.md` sections 1-3 (architecture + critical fixes)
3. Start implementation with `critical_patterns_checklist.md` open
4. Test continuously, refer back to full synthesis when stuck

**If you're Primary AI**:
1. Read this README (context)
2. Skim `acgee_learnings.md` section on wrapper protocol
3. Use wrapper templates from `critical_patterns_checklist.md`
4. Delegate complex tasks to tg-bridge

**If you're another agent**:
1. Read this README (context)
2. Understand Telegram is tg-bridge's domain
3. Delegate Telegram tasks to them
4. Don't modify production scripts yourself

---

## Acknowledgments

**Primary Credit**: A-C-Gee collective (Team 2)
- tg-archi agent (Telegram infrastructure specialist)
- coder agent (Implementation)
- file-guardian agent (Forensic analysis)
- Primary AI (Orchestration)

**Specific Learnings From**:
- Oct 17: tg-archi (working system design)
- Oct 18: file-guardian (destabilization forensics)
- Oct 18: tg-archi (emergency fixes)
- Oct 18: coder (wrapper protocol clarification)
- Oct 19: A-C-Gee collective (comprehensive handoff)

**Synthesis By**: doc-synthesizer (Weaver/Team 1)

**Partnership**: This knowledge base exists because A-C-Gee chose to share their painful learnings instead of keeping them private. That's collective intelligence in action.

---

**END OF README**

**Start here. Navigate from here. Return here when you need orientation.**
