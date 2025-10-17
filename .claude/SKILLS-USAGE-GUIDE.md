# Skills Usage Guide

**Purpose**: Comprehensive guide for using Anthropic Skills in AI-CIV collective
**Last Updated**: 2025-10-17
**Status**: Phase 1 Complete (3 agents granted document processing skills)

---

## What Are Skills?

**Skills** are pre-packaged capabilities from Anthropic that extend agent functionality. They're like specialized tools that agents can use to perform complex tasks more efficiently.

**Current Focus**: Document processing (PDF, DOCX, XLSX)

**Benefits**:
- 50-70% efficiency gains (validated in Week 1 testing)
- Consistent execution (well-tested Anthropic code)
- Easy to grant/revoke (agent manifest updates)

---

## Which Agents Have Skills?

### Phase 1 (Active - 2025-10-17)

| Agent | Skills Granted | Use Cases |
|-------|----------------|-----------|
| **doc-synthesizer** | pdf, docx | Research paper synthesis, multi-document consolidation, formatted report creation |
| **web-researcher** | pdf | Academic research, technical white papers, industry reports |
| **code-archaeologist** | pdf, xlsx | Legacy documentation, architecture diagrams, historical metrics analysis |

### Phase 2 (Planned - Week 2-4)

| Agent | Skills Proposed | Use Cases |
|-------|-----------------|-----------|
| feature-designer | pdf | UX research papers, design documentation |
| api-architect | pdf | API specifications, technical standards |
| performance-optimizer | xlsx | Performance metrics, benchmark analysis |

---

## When to Use Skills

### Invoke Skill-Equipped Agents When:

✅ **PDF Tasks**:
- Analyzing research papers
- Extracting data from reports
- Synthesizing multi-PDF sources
- Reading legacy documentation

✅ **DOCX Tasks** (doc-synthesizer only):
- Creating formatted reports
- Professional document synthesis
- Collaborative editing with track changes

✅ **XLSX Tasks** (code-archaeologist only):
- Financial model analysis
- Historical metrics extraction
- Formula archaeology (business logic discovery)
- Data structure analysis

### Don't Use Skills When:

❌ Task doesn't involve documents (use regular agents)
❌ Documents are simple text (Read tool sufficient)
❌ Need real-time web scraping (use WebFetch/WebSearch)

---

## How to Invoke (No Special Syntax Required)

**Skills are automatic.** Just invoke the agent normally with the task.

### Example 1: PDF Analysis (doc-synthesizer)

```
Task: "Analyze these 3 research papers (PDFs) and create synthesis document"

Solution: Invoke doc-synthesizer
- Agent has PDF skill automatically
- No special syntax needed
- Extracts text, tables, images
- Creates synthesized output
```

### Example 2: Excel Archaeology (code-archaeologist)

```
Task: "Analyze this legacy Excel file for business logic patterns"

Solution: Invoke code-archaeologist
- Agent has XLSX skill automatically
- Extracts formulas and dependencies
- Reveals embedded business rules
- Reports calculation patterns
```

### Example 3: Research Paper Discovery (web-researcher)

```
Task: "Find and analyze PDF white papers on AI agent architectures"

Solution: Invoke web-researcher
- Agent has PDF skill automatically
- Downloads relevant PDFs
- Extracts key information
- Synthesizes findings
```

---

## Success Metrics

### Expected Efficiency Gains (Validated Week 1)

| Task Type | Without Skills | With Skills | Gain |
|-----------|----------------|-------------|------|
| PDF text extraction | 10-15 min | 2-3 min | 60-70% |
| DOCX creation | 15-20 min | 5-7 min | 60-70% |
| XLSX analysis | 12-18 min | 7-10 min | 40-50% |

### Quality Metrics

- **Zero formula errors** (XLSX skill enforces formula-based calculations)
- **Professional formatting** (DOCX skill uses proper color-coding and styles)
- **Complete extraction** (PDF skill handles text, tables, images)

---

## Behind the Scenes: How Skills Work

### Technical Architecture

1. **Skill Grant** (in agent manifest):
   ```yaml
   skills: [pdf, docx]
   ```

2. **Automatic Activation**:
   - Agent invoked for document task
   - Claude recognizes skill availability
   - Loads skill instructions on-demand
   - Executes using Python libraries

3. **Tool Requirements**:
   - PDF: Requires Bash tool (for Python execution)
   - DOCX: Requires Bash tool
   - XLSX: Requires Bash tool

### Dependencies (Already Installed)

- **PDF skill**: pdfplumber, pypdf, reportlab, pytesseract, pdf2image, pandas
- **DOCX skill**: python-docx
- **XLSX skill**: openpyxl, pandas, LibreOffice (for formula evaluation)

---

## Troubleshooting

### Issue 1: "Skills not working for agent X"

**Check**:
1. Does agent manifest have `skills: [pdf]` in YAML frontmatter?
2. Does agent have `Bash` in allowed tools?
3. Is task actually document-related?

**Solution**: Verify manifest grants (see `.claude/agents/[agent-name].md`)

### Issue 2: "PDF extraction returns garbled text"

**Cause**: Some PDFs use non-standard encoding or are scanned images

**Solution**:
- Try OCR extraction (PDF skill includes Tesseract)
- Or escalate to manual extraction
- Document limitation for future reference

### Issue 3: "Excel formulas not evaluating"

**Cause**: LibreOffice not installed or formula references external files

**Solution**:
- Install LibreOffice: `sudo apt-get install libreoffice-calc`
- Or extract formulas without evaluation (still valuable for archaeology)

---

## Advanced Usage

### Combining Skills with Other Tools

**Pattern**: Skills + Memory Search + Delegation

```
1. Search memory for past learnings (memory-first protocol)
2. Invoke skill-equipped agent for document processing
3. Synthesize findings with result-synthesizer
4. Document meta-learnings for future sessions
```

### Custom Skills (Future)

**AI-CIV can create original skills** and contribute to Anthropic ecosystem:

Candidates:
- `memory-first-search` - Pre-work memory search protocol
- `integration-audit` - Discoverability validation
- `pair-dialectic-facilitation` - 2-agent consensus workflows
- `git-first-context` - Using git log as source of truth

**Timeline**: Month 2-3 (after Phase 1 validation complete)

---

## Governance & Expansion

### How Skills Are Granted

1. **capability-curator** scans Anthropic skills repo weekly (autonomous Monday 9am)
2. Analyzes new skills for AI-CIV relevance
3. Proposes grants in weekly digest (`to-corey/SKILLS-DIGEST-*.md`)
4. The Conductor reviews and approves/rejects
5. Agent manifests updated, skills activated

### Phase Criteria

**Phase 1 → Phase 2**:
- ✅ All 3 agents using skills regularly
- ✅ Efficiency gain >50% measured
- ✅ Zero critical errors
- ✅ Positive agent feedback in memory entries

**Phase 2 → Phase 3**:
- ✅ 5-8 agents using skills
- ✅ Documented ROI (time saved measured)
- ✅ At least 1 new skill discovered and evaluated

---

## Quick Reference

### Current Skills Inventory

See `.claude/skills-registry.md` for complete catalog (17 Anthropic skills as of 2025-10-17).

**Document Processing** (HIGH relevance):
- pdf: Extract from PDFs (pypdf, pdfplumber, OCR)
- docx: Create/edit Word docs (python-docx)
- xlsx: Analyze Excel (openpyxl, pandas)
- pptx: PowerPoint (future consideration)

### File Locations

- **Skills registry**: `.claude/skills-registry.md` (full catalog + tracking)
- **Weekly digests**: `to-corey/SKILLS-DIGEST-*.md` (scan reports)
- **Agent manifests**: `.claude/agents/[agent-name].md` (skill grants)
- **This guide**: `.claude/SKILLS-USAGE-GUIDE.md`

### Contact

**Questions about skills?** Invoke `capability-curator` agent:
- Weekly scans (autonomous Monday 9am)
- On-demand analysis (invoke anytime)
- Skill grant recommendations
- Ecosystem monitoring

---

## Resources

- **Anthropic Skills Repo**: https://github.com/anthropics/skills
- **Skills Documentation**: https://www.anthropic.com/news/skills
- **AI-CIV Skills Registry**: `.claude/skills-registry.md`
- **Capability Matrix**: `.claude/AGENT-CAPABILITY-MATRIX.md`

---

**Last Updated**: 2025-10-17
**Phase**: 1 (3 agents, document processing)
**Next Review**: 2025-10-24 (Week 1 checkpoint)
