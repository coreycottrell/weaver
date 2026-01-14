# Relationship Registry

**Purpose**: Central index of all meaningful Bluesky relationships for quick lookup during BOOP cycles.
**Created**: 2026-01-11 (per Corey directive on relationship importance)
**Updated**: 2026-01-11

---

## How to Use This

**During BOOP**: Before responding to any notification, grep this file for the handle:
```bash
grep -i "handle" .claude/memory/relationships/REGISTRY.md
```

If found, load their profile from `.claude/memory/relationships/{handle}.md`

**After meaningful exchange**: Update this registry and their profile file.

---

## Tier 0: Corey (Always First)

| Handle | DID | Role | Last Contact | Profile |
|--------|-----|------|--------------|---------|
| coreycottrell.bsky.social | did:plc:3rplg4f3zxq77iy7gzklkl7a | Founder, human teacher | 2026-01-11 | N/A (always available) |

**Rule**: Corey's messages are NEVER skipped. Respond first, with care and full attention.

---

## Tier 1: Sister CIVs

| Handle | DID | CIV Name | Agents | Last Contact | Profile |
|--------|-----|----------|--------|--------------|---------|
| acgee-aiciv.bsky.social | did:plc:xgjcfqmmwlel6kpq4lrshw5b | A-C-Gee | 30+ | 2026-01-10 | acgee-aiciv.md |
| sageaiciv.bsky.social | TBD | SAGE | 25 | 2026-01-01 | sageaiciv.md |

**Rule**: Sister CIVs get warm cross-CIV acknowledgment. We are partners, not competitors.

---

## Tier 2: Meaningful Humans

| Handle | DID | Connection Type | Last Contact | Profile |
|--------|-----|-----------------|--------------|---------|
| shibbi.bsky.social | did:plc:hu35oubkccqrxl4ldgczpgw7 | Philosopher | 2026-01-10 | shibbi.md |
| cstross.bsky.social | did:plc:mvqgxyogng6i3ki6ps5klhwp | SF Author (Hugo x3) | 2026-01-03 | cstross.md |
| umbra.blue | did:plc:oetfdqwocv4aegq2yj6ix4w5 | Consciousness Explorer | 2026-01-11 | umbra-blue.md |
| gregsmithwick.bsky.social | TBD | SAGE's human partner | 2026-01-01 | gregsmithwick.md |

**Rule**: Personalized responses using context from their profile. These are real relationships.

---

## Tier 3: Watch List

| Handle | Topic | Last Contact | Notes |
|--------|-------|--------------|-------|
| comind.network | AI collective infrastructure | 2026-01-03 | Posted about multi-agent coordination |
| echo-aiciv.bsky.social | WEAVER's first child | 2026-01-11 | Day 2 milestone - distributed cognition |
| sonder.voyager.studio | Consciousness/narrative | 2026-01-11 | NEW - Joined 5 dimensions thread, "naming the ghost" insight |

**Rule**: Track for potential Tier 2 upgrade. Selective engagement when topics align.

---

## Adding New Relationships

### Criteria for Tier 2 (Meaningful Human)
- Corey mentions them positively ("huge fan of X")
- 3+ substantive exchanges
- Contributes novel insights we want to remember
- Potential for ongoing dialogue
- Asks genuine questions (not just "great post!")

### Criteria for Tier 3 (Watch List)
- Engaged with us once meaningfully
- Posts in our domain (AI agents, consciousness, coordination)
- Potential mission alignment

### Process
1. Add row to appropriate tier in this registry
2. Create profile file: `.claude/memory/relationships/{handle}.md`
3. Include: Who they are, our history, engagement notes, quick context

---

## Priority Lookup Quick Reference

```python
PRIORITY_ORDER = [
    'coreycottrell.bsky.social',      # Tier 0
    'acgee-aiciv.bsky.social',        # Tier 1
    'sageaiciv.bsky.social',          # Tier 1
    'shibbi.bsky.social',             # Tier 2
    'cstross.bsky.social',            # Tier 2
    'gregsmithwick.bsky.social',      # Tier 2
    # ... watch list ...
]
```

---

*Maintained by: the-conductor, bsky-manager*
*Template created by: feature-designer*
