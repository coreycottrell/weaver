---
agent: claude-code-expert
confidence: high
content_hash: b28daf87454bcea04659ec631184879c6a015d98d7ef3b47d343d5f244015544
created: '2025-10-17T15:24:14.008016+00:00'
date: '2025-10-17'
last_accessed: '2025-10-17T15:24:14.008025+00:00'
quality_score: 0
reuse_count: 0
tags:
- skills
- document-generation
- pdf
- xlsx
- platform
- anthropic
- environment-setup
topic: Anthropic document skills integration patterns
type: technique
visibility: public
---


Context: Week 1 skills testing - validated document skills (PDF, XLSX, DOCX, PPTX)

Discovery: Skills are knowledge modules, not executable tools
- Located in ~/.claude/plugins/marketplaces/anthropic-agent-skills/
- Each has SKILL.md (YAML + markdown instructions)
- Teach Claude HOW to use standard libraries (pypdf, openpyxl, etc.)
- Invocation: "use the pdf skill to extract text from file.pdf"

Tool Pattern - Virtual Environment Required (CRITICAL):
```bash
# PEP 668 prevents system-wide pip installs
python3 -m venv .venv_skills
.venv_skills/bin/pip install pypdf pdfplumber reportlab openpyxl pandas
```

Tool Pattern - Excel Formulas (KEY PRINCIPLE):
```python
# ❌ WRONG - Hardcoded values
sheet['A1'] = 500  # Dead value

# ✅ CORRECT - Dynamic formulas
sheet['A1'] = '=SUM(B1:B10)'  # Recalculates when data changes
```

Tool Pattern - Formula Recalculation:
```bash
# Requires LibreOffice + recalc.py script
python3 ~/.claude/plugins/marketplaces/anthropic-agent-skills/document-skills/xlsx/recalc.py file.xlsx
```

Why It Works:
- Skills provide curated library recommendations (no trial-and-error)
- Complete API reference in context (no web search needed)
- Gotcha documentation upfront (PEP 668, formula strings, etc.)
- Production patterns from Anthropic's Claude.ai features

When to Use:
- doc-synthesizer: Professional reports (DOCX), data tables (XLSX)
- web-researcher: PDF research paper extraction, table parsing
- code-archaeologist: Legacy documentation analysis (PDF)
- result-synthesizer: Multi-agent report consolidation

Gotchas:
1. Virtual environment REQUIRED (PEP 668)
2. LibreOffice needed for Excel formula recalculation
3. Formulas stored as strings (not values) until calculated
4. Saving with data_only=True DESTROYS formulas permanently
5. Document skills are Proprietary (not open source)

Performance:
- 60-70% efficiency gain over manual library exploration
- Fast operations (<1s for small documents)
- Token-efficient (comprehensive docs prevent back-and-forth)

Integration Path:
1. Create .venv_skills with libraries
2. Install LibreOffice
3. Document in CLAUDE-OPS.md
4. Roll out to Tier 1 agents (doc-synthesizer, web-researcher)
5. Share patterns via memory system

Test Artifacts: 5 files created (PDFs + Excel with formulas)
Full Report: to-corey/WEEK-1-SKILLS-TEST-REPORT.md
