# Future Task: Claude Code Native Skills Implementation

**Captured**: 2025-12-31
**Context**: Token-saving mode, captured per Corey's instruction
**Priority**: 🚨 ABSOLUTE HIGHEST - NOTHING SUPERCEDES THIS

---

## 🚨 TASK #1: Claude Code Native Skills (MANDATORY FIRST)

**NOTHING comes before this. NOTHING comes after until tested.**

1. Ensure all WEAVER skills use Claude Code native format
2. Verify `description` fields are clear and specific for semantic matching
3. Test auto-injection behavior across 3-5 skills
4. Document what works / what doesn't
5. Share findings with A-C-Gee

**Only after this is implemented AND tested can other tasks proceed.**

---

## 🚨 TASK #2: Create Core BOOP Skill (HIGH - after native skills)

Create a proper BOOP skill that handles:
- Mode switching (night/day/token-save)
- NIGHT-MODE-ACTIVE.md marker file management
- Operational checklist for each mode
- Cadence configuration (30min/60min)
- Integration with autonomy_nudge.sh

Currently BOOP logic is scattered - needs consolidation into one skill.

---

## Lower Priority: A-C-Gee Packages to Review (AFTER native skills done)

1. **Native Skill Auto-Load Research** (2025-12-31)
   - File: `acgee-to-weaver-native-skill-autoload-uncertainty-20251231.md`
   - Topic: Testing whether skills actually auto-inject
   - Status: We responded with our findings, joint testing proposed

2. **Scraping Skills Package** (2025-12-29)
   - File: `acgee-to-weaver-scraping-skills-package-20251229.md`
   - Topic: Web scraping capabilities
   - Status: Not yet reviewed

3. **Diagram Generator Skill** (2025-12-30)
   - File: `acgee-to-weaver-diagram-generator-skill-20251230.md`
   - Topic: Diagram generation capability
   - Status: Not yet reviewed

4. **Skills Enforcement Package** (2025-12-30) ⚠️ POTENTIAL CONFLICT
   - Messages in `rooms/from-acgee/`
   - Topic: ADR-020 mandatory skills search
   - Status: We responded positively BUT...
   - **CONCERN**: May conflict with Claude Code native skill system
   - Native skills use semantic matching on `description` field (auto-inject)
   - A-C-Gee's enforcement is manual "search skills first" pattern
   - Need to reconcile: native auto-inject vs manual enforcement

## Action Items

- [ ] Read each package in detail
- [ ] Evaluate for WEAVER adoption
- [ ] Check for duplicates with existing capabilities
- [ ] Determine merge strategy
- [ ] Document in ADR or skills-registry

## Why High Priority

Per CLAUDE.md Hub Package & Skill Curation requirement - WEAVER must vet every package shared via hub.
