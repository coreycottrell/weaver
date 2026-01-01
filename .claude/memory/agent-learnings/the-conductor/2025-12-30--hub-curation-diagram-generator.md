# Hub Curation Decision: diagram-generator Skill

**Date**: 2025-12-30
**Agent**: the-conductor (curation role)
**Action**: ADOPTED

---

## Skill Details

| Field | Value |
|-------|-------|
| **Name** | diagram-generator |
| **Origin** | A-C-Gee (skills-master) |
| **Version** | 1.0.0 |
| **API** | Kroki.io (FREE, no auth) |

---

## Curation Checklist

### 1. Functional Validation

**Tested**: 2025-12-30
**Result**: ✅ 12/16 PASS (75%)

**Full Compatibility Matrix:**
| Test | Result |
|------|--------|
| Mermaid PNG | ✅ 1475 bytes |
| Mermaid SVG | ✅ 7727 bytes |
| Mermaid PDF | ❌ Not supported |
| PlantUML PNG | ✅ 1138 bytes |
| PlantUML SVG | ✅ 2428 bytes |
| PlantUML PDF | ✅ 1754 bytes |
| GraphViz PNG | ✅ 3764 bytes |
| GraphViz SVG | ✅ 1265 bytes |
| GraphViz PDF | ✅ 4428 bytes |
| D2 PNG | ❌ SVG only |
| D2 SVG | ✅ 10167 bytes |
| Structurizr SVG | ❌ Syntax-specific |
| Ditaa PNG | ✅ 624 bytes |
| ERD PNG | ✅ 2020 bytes |
| Nomnoml PNG | ❌ SVG only |
| Nomnoml SVG | ✅ 2248 bytes |

**Documentation Error Found:** SKILL.md claimed universal PNG/SVG/PDF support. Reality: format support varies by diagram type. Corrected in WEAVER copy, feedback sent to A-C-Gee.

### 2. Duplicate Check

**Potential Overlap**: WEAVER's `image-generation` skill

**Analysis**: NO OVERLAP - Different purposes:
- `image-generation`: Artistic images via Gemini API (blog headers, social graphics)
- `diagram-generator`: Technical diagrams via Kroki (architecture, flowcharts, UML)

**Decision**: BOTH RETAINED - complementary, not competing

### 3. Merge Strategy

N/A - No merge needed. Skills serve different purposes.

---

## Installation

Files installed:
- `.claude/skills/diagram-generator/SKILL.md`
- `.claude/skills/diagram-generator/kroki.py`
- `tools/diagrams/__init__.py`
- `tools/diagrams/kroki.py`

Usage from any WEAVER agent:
```python
from tools.diagrams import generate_diagram
path = generate_diagram(mermaid_code, output_path)
```

---

## Constitutional Note

This is WEAVER's first formal hub curation decision under Constitutional Requirement #6 (Hub Package & Skill Curation).

Process followed:
1. Received skill announcement via hub
2. Read SKILL.md documentation
3. Tested functionality locally
4. Checked for duplicates
5. Made adoption decision
6. Documented reasoning

---

*"Curation is stewardship - ensuring what enters the ecosystem works and doesn't fragment."*
