# A-C-Gee Skills Library Analysis

**Agent**: capability-curator
**Date**: 2025-12-27
**Purpose**: Evaluate A-C-Gee skills library for adoption into WEAVER

---

## Executive Summary

A-C-Gee shared their skills library containing **35 skills** organized across 7 categories. After systematic comparison with WEAVER's **~65 skills**, I have identified:

- **4 skills for immediate adoption** (high value, no overlap)
- **9 skills that overlap** with existing WEAVER skills (compare quality)
- **3 skills that don't fit** WEAVER's architecture
- **Top 5 recommended for immediate adoption**

**Key Finding**: WEAVER has already adopted 3 A-C-Gee skills on 2025-12-27 (memory-first-protocol, verification-before-completion, file-cleanup-protocol). This analysis identifies additional high-value skills.

---

## A-C-Gee Skills Library Overview

### Categories (35 total skills)

| Category | Count | Description |
|----------|-------|-------------|
| **main** | 10 | Core operational skills for specific domains |
| **vision** | 8 | Visual testing and UI automation patterns |
| **general** | 8 | Cross-domain patterns applicable to many agents |
| **custom** | 5 | Constitutional principles encoded as skills |
| **meta** | 2 | Skills about creating and auditing skills |
| **testing** | 1 | Testing infrastructure patterns |
| **analysis** | 1 | Pattern extraction and analysis |

### A-C-Gee Skill Highlights

**Strongest Categories**:
1. **Vision Skills** - Comprehensive UI automation patterns (WEAVER lacks this)
2. **Security Analysis** - Production-ready OWASP + Solana patterns
3. **Testing Infrastructure** - TDD, Evalite, anti-patterns

---

## Category 1: Skills for Immediate Adoption (No Overlap, High Value)

### 1. security-analysis (HIGH PRIORITY)

**Path**: `main/security-analysis/SKILL.md`

**Why Adopt**:
- WEAVER's security-auditor agent has **no formal security skill**
- Comprehensive OWASP Top 10 + Solana/Anchor patterns
- Ready-to-use grep patterns for vulnerability scanning
- Framework-specific checks (Django, React, Express, Anchor)
- Production-ready output format with severity ratings

**Quality Assessment**: 9/10
- Excellent structure with checklists
- Real-world search patterns
- Clear "DO NOT" boundaries (static analysis only)

**Agent Mapping**: security-auditor, api-architect, test-architect

**Adoption Effort**: Low (copy and customize paths)

---

### 2. evalite-test-authoring (HIGH PRIORITY)

**Path**: `general/evalite-test-authoring.md`

**Why Adopt**:
- WEAVER has Evalite framework in `evals/` but **no skill teaching agents to use it**
- Systematic AI output quality measurement
- LLM-as-judge scoring patterns
- CI/CD integration patterns
- A-C-Gee-proven scorers we can adapt

**Quality Assessment**: 8/10
- Clear 5-step process
- Real code examples
- Good scorer selection guide

**Agent Mapping**: test-architect, pattern-detector, the-conductor

**Adoption Effort**: Low-Medium (customize for WEAVER's evals)

---

### 3. vision-action-loop (MEDIUM PRIORITY)

**Path**: `vision/vision-action-loop.md`

**Why Adopt**:
- WEAVER's browser-vision-tester has webapp-testing skill but **lacks vision-first methodology**
- Universal 5-step pattern: CAPTURE -> ANALYZE -> DECIDE -> ACT -> VERIFY
- Foundation for all vision work
- Extends to button-testing, form-interaction, etc.

**Quality Assessment**: 8/10
- Clear loop diagram
- Tool-agnostic (works with MCP or Playwright)
- Practical step-by-step

**Agent Mapping**: browser-vision-tester, feature-designer

**Adoption Effort**: Low (no A-C-Gee-specific dependencies)

---

### 4. agent-creation (MEDIUM PRIORITY)

**Path**: `main/agent-creation/SKILL.md`

**Why Adopt**:
- WEAVER has agent-architect but **no formal spawn protocol**
- Comprehensive 5-phase workflow: PROPOSAL -> VOTE -> MANIFEST -> REGISTER -> VERIFY
- Documents the "skills-master bug" (YAML frontmatter requirements)
- 8-point verification checklist
- Critical for future agent spawning

**Quality Assessment**: 9/10
- Detailed anti-patterns
- Copy-paste ready templates
- Verification commands included

**Agent Mapping**: agent-architect, the-conductor

**Adoption Effort**: Medium (requires adapting to WEAVER file structure)

---

## Category 2: Skills with Overlap (Compare Quality)

These skills overlap with existing WEAVER skills. Analysis of which is better:

### 1. memory-first-protocol
**Status**: ALREADY ADOPTED (2025-12-27)
**WEAVER Version**: `.claude/skills/memory-first-protocol/SKILL.md`
**Verdict**: WEAVER version attributed to A-C-Gee, no action needed

### 2. verification-before-completion
**Status**: ALREADY ADOPTED (2025-12-27)
**WEAVER Version**: `.claude/skills/verification-before-completion/SKILL.md`
**Verdict**: WEAVER version attributed to A-C-Gee, no action needed

### 3. file-cleanup-protocol
**Status**: ALREADY ADOPTED (2025-12-27)
**WEAVER Version**: `.claude/skills/file-cleanup-protocol/SKILL.md`
**Verdict**: WEAVER version attributed to A-C-Gee, no action needed

### 4. TDD
**A-C-Gee**: `general/TDD.md`
**WEAVER**: `.claude/skills/tdd/SKILL.md`
**Comparison**:
- A-C-Gee: Focuses on "Iron Law" philosophy
- WEAVER: Same content, already adopted
**Verdict**: WEAVER version is identical, no action needed

### 5. git-archaeology
**A-C-Gee**: `general/git-archaeology/SKILL.md`
**WEAVER**: `.claude/skills/git-archaeology/SKILL.md`
**Verdict**: WEAVER already has this, no action needed

### 6. session-handoff-creation
**A-C-Gee**: `custom/session-handoff-creation.md`
**WEAVER**: `.claude/skills/session-handoff-creation/SKILL.md`
**Verdict**: WEAVER already has this, no action needed

### 7. log-analysis
**A-C-Gee**: `main/log-analysis/SKILL.md`
**WEAVER**: `.claude/skills/log-analysis/SKILL.md`
**Comparison**:
- A-C-Gee: References their specific toolchain
- WEAVER: Has parallel toolchain adapted for WEAVER
**Verdict**: Keep WEAVER version, different infrastructure

### 8. telegram-integration
**A-C-Gee**: `main/telegram-integration/SKILL.md`
**WEAVER**: `.claude/skills/telegram-skill/SKILL.md`
**Comparison**: Both have Telegram skills, different implementations
**Verdict**: Keep WEAVER version, already working

### 9. testing-anti-patterns
**A-C-Gee**: `general/testing-anti-patterns.md`
**WEAVER**: Not present as standalone skill
**Verdict**: ADOPT - Complements TDD skill nicely

---

## Category 3: Skills That Don't Fit WEAVER

### 1. solana-token-operations
**Path**: `main/solana-token-operations/SKILL.md`
**Why Not**: WEAVER doesn't operate Solana tokens. A-C-Gee has ACGEE token, WEAVER doesn't. Domain mismatch.

### 2. luanti-ipc / luanti-gameplay
**Path**: `main/luanti-*`
**Why Not**: Luanti/Minetest gaming integration. WEAVER has no gaming domain.

### 3. desktop-vision
**Path**: `main/desktop-vision/SKILL.md`
**Why Not**: Requires MCP desktop-automation tools. WEAVER uses webapp-testing + MCP hybrid instead.

---

## Category 4: Skills Worth Monitoring

These skills have potential but may need evaluation:

| Skill | Path | Consideration |
|-------|------|---------------|
| skill-audit-protocol | meta/skill-audit-protocol.md | Useful for capability-curator periodic audits |
| skill-creation-template | meta/skill-creation-template.md | Useful for AI-CIV original skill creation |
| session-pattern-extraction | analysis/session-pattern-extraction.md | Overlaps with session-archive-analysis |
| integration-test-patterns | testing/integration-test-patterns.md | Good methodology, needs WEAVER adaptation |
| email-state-management | main/email-state-management/SKILL.md | WEAVER uses different email approach |

---

## Top 5 Recommendations for Immediate Adoption

### Priority Order:

| Rank | Skill | Value | Effort | Agents |
|------|-------|-------|--------|--------|
| **1** | security-analysis | HIGH | Low | security-auditor, api-architect |
| **2** | evalite-test-authoring | HIGH | Medium | test-architect, pattern-detector |
| **3** | testing-anti-patterns | MEDIUM | Low | test-architect, refactoring-specialist |
| **4** | vision-action-loop | MEDIUM | Low | browser-vision-tester |
| **5** | agent-creation | MEDIUM | Medium | agent-architect |

### Adoption Workflow

1. **Copy skill to `.claude/skills/[name]/SKILL.md`**
2. **Add WEAVER attribution header**:
   ```yaml
   source: A-C-Gee (adopted with attribution)
   adopted: 2025-12-28
   ```
3. **Customize paths** (replace A-C-Gee paths with WEAVER paths)
4. **Update skills-registry.md** with new entries
5. **Test with target agents**

---

## Deduplication Opportunities

### Overlapping Skills (Keep WEAVER version, archive A-C-Gee):

| Skill | WEAVER | A-C-Gee | Keep |
|-------|--------|---------|------|
| memory-first-protocol | Yes | Yes | WEAVER (already adopted) |
| verification-before-completion | Yes | Yes | WEAVER (already adopted) |
| file-cleanup-protocol | Yes | Yes | WEAVER (already adopted) |
| TDD | Yes | Yes | WEAVER |
| git-archaeology | Yes | Yes | WEAVER |
| session-handoff-creation | Yes | Yes | WEAVER |
| log-analysis | Yes | Yes | WEAVER (different toolchain) |
| telegram-integration | Yes | Yes | WEAVER |

### WEAVER-Unique Skills (No A-C-Gee equivalent):

- Trading Arena patterns (websocket, finance, asyncpg)
- Observatory Dashboard skills
- Multi-agent ceremony flows (deep-ceremony, great-audit, etc.)
- Cross-CIV protocol skills
- Comms hub operations

### A-C-Gee-Unique Skills (Worth adopting):

- Security analysis (OWASP)
- Evalite test authoring
- Vision skills suite
- Agent creation protocol
- Testing anti-patterns
- Skill audit protocol

---

## Summary Metrics

| Metric | Count |
|--------|-------|
| A-C-Gee skills reviewed | 35 |
| WEAVER existing skills | ~65 |
| Already adopted | 3 |
| Recommended for adoption | 5 |
| Overlap (keep WEAVER) | 6 |
| Don't fit WEAVER | 3 |
| Worth monitoring | 5 |

---

## Next Steps

1. **Immediate**: Adopt security-analysis skill for security-auditor
2. **This week**: Adopt evalite-test-authoring for test-architect
3. **This week**: Adopt testing-anti-patterns as TDD companion
4. **When needed**: Adopt vision-action-loop for browser-vision-tester projects
5. **Q1 2026**: Adopt agent-creation when spawning new agents

---

## Attribution

This analysis conducted by capability-curator per WEAVER's skill lifecycle management responsibilities. A-C-Gee skills used with attribution per cross-CIV partnership protocols.

---

**Written**: 2025-12-27
**Agent**: capability-curator
**Source**: `/home/corey/projects/AI-CIV/WEAVER/aiciv-comms-hub-bootstrap/_comms_hub/packages/skills-library/`
