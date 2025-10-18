# 🎓 capability-curator: Phase 2 Accelerated Development Plan

**Agent**: capability-curator
**Domain**: Capability lifecycle management
**Date**: 2025-10-18
**Mission**: Create timeline-optimized plan for 5 Phase 2 custom skills using building blocks

---

## Executive Summary

**Original Estimate**: 3-4 weeks for 5 skills (90-100 hours total)
**Revised Estimate**: 2-3 weeks for 5 skills (55-65 hours total)
**Acceleration**: 38-42% time reduction via skill-creator + template-skill building blocks

**Development Sequence**: 2 skills → 2 skills → 1 skill + iteration
**Week 1**: comment-archaeology + cross-reference-linker (foundational, EASY feasibility)
**Week 2**: secret-scanner + benchmark-runner (infrastructure, EASY feasibility)
**Week 3**: confidence-aggregator + refinement iterations (complex, MEDIUM feasibility)

**Success Criteria**: All 5 skills production-ready, validated, distribution-quality by Week 3 end

---

## Part 1: Timeline Impact Analysis

### Original Estimate Breakdown

**Without building blocks** (90-100 hours total):

| Skill | Time Estimate | Breakdown |
|-------|--------------|-----------|
| comment-archaeology | 18 hours | Design 5h + Implement 8h + Validation 3h + Docs 2h |
| cross-reference-linker | 20 hours | Design 6h + Implement 10h + Validation 2h + Docs 2h |
| secret-scanner | 22 hours | Design 6h + Implement 12h + Validation 2h + Docs 2h |
| benchmark-runner | 20 hours | Design 5h + Implement 11h + Validation 2h + Docs 2h |
| confidence-aggregator | 25 hours | Design 8h + Implement 12h + Validation 3h + Docs 2h |

**Total**: 105 hours (average 21 hours per skill)

**Timeline**: 3-4 weeks (assuming 25-30 productive hours per week)

---

### Revised Estimate with Building Blocks

**With skill-creator + template-skill** (55-65 hours total):

| Skill | Original | Building Block Savings | Revised | Savings % |
|-------|----------|----------------------|---------|-----------|
| comment-archaeology | 18h | 8h (structure + validation) | 10h | 44% |
| cross-reference-linker | 20h | 8h (structure + validation) | 12h | 40% |
| secret-scanner | 22h | 9h (structure + validation) | 13h | 41% |
| benchmark-runner | 20h | 7h (structure + validation) | 13h | 35% |
| confidence-aggregator | 25h | 8h (structure + validation) | 17h | 32% |

**Total**: 65 hours (average 13 hours per skill)

**Savings**: 40 hours (38% reduction)

**Timeline**: 2-3 weeks (same weekly pace, fewer total hours)

---

### What Building Blocks Eliminate

**Time saved on** (per skill):
- ❌ Manual structure design: 2-3 hours → 5 minutes (init_skill.py)
- ❌ YAML frontmatter formatting: 1 hour → auto-generated
- ❌ Resource organization decisions: 1-2 hours → guided by skill-creator
- ❌ Validation logic: 1-2 hours → automated (package_skill.py)
- ❌ Packaging format: 1 hour → standardized output

**Time still required**:
- ✅ Understanding concrete examples: 2-3 hours (irreducible)
- ✅ Core algorithm implementation: 6-10 hours (domain expertise)
- ✅ Testing and iteration: 2-3 hours (quality assurance)
- ✅ Documentation writing: 1-2 hours (SKILL.md content)

**Key Insight**: Building blocks eliminate STRUCTURAL work, not DOMAIN work. We still need agent expertise for algorithms.

---

## Part 2: Week-by-Week Development Sequence

### Week 1: Foundation Skills (Days 1-7)

**Skills**: comment-archaeology + cross-reference-linker

**Why Week 1**:
- Both are EASY feasibility (high success probability)
- Both are HIGH priority (immediate value)
- Establishes pattern for subsequent weeks
- Validates building block workflow

**Day-by-Day Plan**:

**Monday (Day 1)**: Setup + comment-archaeology start
- [ ] Morning: Read skill-creator guidance (all agents, 1 hour)
- [ ] Clone Anthropic skills repo locally (get helper scripts)
- [ ] Create `.claude/skills/` directory structure
- [ ] Invoke code-archaeologist: Begin comment-archaeology design
- [ ] Task: Understand concrete examples (2 hours)
- [ ] Task: Plan resources (scripts? references? assets?) (1 hour)

**Tuesday (Day 2)**: comment-archaeology implementation
- [ ] Invoke code-archaeologist: Continue comment-archaeology
- [ ] Task: Run init_skill.py for structure generation (5 min)
- [ ] Task: Write SKILL.md instructions (2 hours)
- [ ] Task: Implement `scripts/find_comments.py` (4 hours)
- [ ] Task: Initial testing on AI-CIV codebase (1 hour)

**Wednesday (Day 3)**: comment-archaeology completion + cross-reference-linker start
- [ ] Morning: Finalize comment-archaeology
- [ ] Task: Package with package_skill.py validation (30 min)
- [ ] Task: Production test and iteration (1.5 hours)
- [ ] Afternoon: Invoke doc-synthesizer for cross-reference-linker
- [ ] Task: Understand concrete examples (2 hours)
- [ ] Task: Plan resources (1 hour)
- [ ] Task: Init skill structure (5 min)

**Thursday (Day 4)**: cross-reference-linker implementation
- [ ] Invoke doc-synthesizer: Continue cross-reference-linker
- [ ] Task: Write SKILL.md instructions (3 hours)
- [ ] Task: Implement `scripts/link_documents.py` (5 hours)
- [ ] Task: Write `references/link_patterns.md` (1 hour)

**Friday (Day 5)**: cross-reference-linker completion + Week 1 validation
- [ ] Morning: Finalize cross-reference-linker
- [ ] Task: Package with validation (30 min)
- [ ] Task: Production test on .claude/ documentation (2 hours)
- [ ] Afternoon: Week 1 retrospective
- [ ] Task: Document lessons learned (1 hour)
- [ ] Task: Update building block usage patterns (1 hour)
- [ ] Task: Measure actual vs estimated time (30 min)

**Weekend**: Buffer time for iteration if needed

**Week 1 Deliverables**:
- ✅ comment-archaeology skill (production-ready)
- ✅ cross-reference-linker skill (production-ready)
- ✅ Building block workflow validated
- ✅ Lessons learned documented
- ✅ Time savings measured

**Week 1 Success Criteria**:
- Both skills pass package_skill.py validation
- Both skills tested successfully on AI-CIV codebase
- Time savings >35% vs original estimates
- Agents report building blocks as helpful

**Expected Total Time**: 22 hours (vs 38 hours original estimate)

---

### Week 2: Infrastructure Skills (Days 8-14)

**Skills**: secret-scanner + benchmark-runner

**Why Week 2**:
- Both are EASY feasibility (proven techniques)
- Both are infrastructure-level (enable other work)
- Benefit from Week 1 building block experience
- Address security + performance (high-value domains)

**Monday (Day 8)**: secret-scanner start
- [ ] Invoke security-auditor: Begin secret-scanner design
- [ ] Task: Understand concrete examples (2 hours)
- [ ] Task: Plan resources (scripts + references) (1 hour)
- [ ] Task: Init skill structure (5 min)
- [ ] Task: Begin SKILL.md (2 hours)

**Tuesday (Day 9)**: secret-scanner implementation
- [ ] Invoke security-auditor: Continue secret-scanner
- [ ] Task: Implement `scripts/scan_secrets.py` (pattern matching) (4 hours)
- [ ] Task: Implement entropy calculation logic (2 hours)
- [ ] Task: Write `references/secret_patterns.md` (AWS, GH, DB patterns) (1.5 hours)

**Wednesday (Day 10)**: secret-scanner completion + benchmark-runner start
- [ ] Morning: Finalize secret-scanner
- [ ] Task: Add git history scanning (2 hours)
- [ ] Task: Package with validation (30 min)
- [ ] Task: Production test on AI-CIV repos (1 hour)
- [ ] Afternoon: Invoke performance-optimizer for benchmark-runner
- [ ] Task: Understand concrete examples (2 hours)
- [ ] Task: Plan resources (scripts + references) (1 hour)

**Thursday (Day 11)**: benchmark-runner implementation
- [ ] Invoke performance-optimizer: Continue benchmark-runner
- [ ] Task: Init skill structure (5 min)
- [ ] Task: Write SKILL.md instructions (2.5 hours)
- [ ] Task: Implement `scripts/run_benchmark.py` (warmup logic) (3 hours)
- [ ] Task: Implement statistical analysis (confidence intervals) (2 hours)

**Friday (Day 12)**: benchmark-runner completion + Week 2 validation
- [ ] Morning: Finalize benchmark-runner
- [ ] Task: Implement regression detection (2 hours)
- [ ] Task: Write `references/statistics.md` (formulas) (1 hour)
- [ ] Task: Package with validation (30 min)
- [ ] Task: Production test (1 hour)
- [ ] Afternoon: Week 2 retrospective
- [ ] Task: Document lessons learned (1 hour)
- [ ] Task: Compare Week 1 vs Week 2 efficiency (30 min)

**Weekend**: Buffer for iteration

**Week 2 Deliverables**:
- ✅ secret-scanner skill (production-ready)
- ✅ benchmark-runner skill (production-ready)
- ✅ Week 1-2 comparison data
- ✅ Refined building block workflow

**Week 2 Success Criteria**:
- Both skills pass validation
- secret-scanner finds zero secrets in AI-CIV (clean audit)
- benchmark-runner produces valid statistical output
- Time savings sustained >35%

**Expected Total Time**: 26 hours (vs 42 hours original estimate)

---

### Week 3: Complex Skill + Refinement (Days 15-21)

**Skills**: confidence-aggregator + iterations on previous 4

**Why Week 3**:
- confidence-aggregator is MEDIUM feasibility (more complex)
- Benefit from 2 weeks of building block mastery
- Week 3 buffer allows for quality iteration
- Final polish before production deployment

**Monday (Day 15)**: confidence-aggregator start
- [ ] Invoke result-synthesizer: Begin confidence-aggregator design
- [ ] Task: Understand concrete examples (multi-agent synthesis) (3 hours)
- [ ] Task: Research aggregation methods (Bayesian, weighted avg) (2 hours)
- [ ] Task: Plan resources (scripts + references) (1.5 hours)

**Tuesday (Day 16)**: confidence-aggregator implementation
- [ ] Invoke result-synthesizer: Continue confidence-aggregator
- [ ] Task: Init skill structure (5 min)
- [ ] Task: Write SKILL.md instructions (3 hours)
- [ ] Task: Implement `scripts/aggregate_confidence.py` (Bayesian logic) (4 hours)

**Wednesday (Day 17)**: confidence-aggregator completion
- [ ] Invoke result-synthesizer: Finalize confidence-aggregator
- [ ] Task: Implement weighted averages (2 hours)
- [ ] Task: Write `references/confidence_math.md` (formulas) (2 hours)
- [ ] Task: Edge case handling (conflicting scores) (2 hours)
- [ ] Task: Package with validation (30 min)
- [ ] Task: Production test (1.5 hours)

**Thursday (Day 18)**: Refinement iterations
- [ ] Morning: Review all 5 skills with fresh eyes
- [ ] Invoke integration-auditor: Discoverability audit
- [ ] Task: Test skill triggers (do they activate correctly?) (2 hours)
- [ ] Task: Refine metadata descriptions (1 hour)
- [ ] Afternoon: Documentation polish
- [ ] Invoke doc-synthesizer: Review all SKILL.md files
- [ ] Task: Consistency pass (formatting, tone) (2 hours)
- [ ] Task: Add usage examples (1.5 hours)

**Friday (Day 19)**: Final validation + packaging
- [ ] Morning: Production validation suite
- [ ] Task: Run all 5 skills on real AI-CIV tasks (3 hours)
- [ ] Task: Measure efficiency gains (actual vs estimated) (1 hour)
- [ ] Afternoon: Distribution preparation
- [ ] Task: Create skill catalog document (1.5 hours)
- [ ] Task: Write deployment guide for Corey (1 hour)
- [ ] Task: Document next steps (external distribution?) (30 min)

**Weekend**: Buffer for final polish

**Week 3 Deliverables**:
- ✅ confidence-aggregator skill (production-ready)
- ✅ All 5 skills refined and polished
- ✅ Discoverability audit complete
- ✅ Deployment guide for Corey
- ✅ Efficiency metrics report

**Week 3 Success Criteria**:
- All 5 skills pass validation
- Discoverability audit: 100% (all skills linked and triggered)
- Efficiency gains measured and documented
- Skills ready for immediate use

**Expected Total Time**: 17 hours (vs 25 hours original estimate)

---

### Timeline Summary

| Week | Skills | Original Est. | Revised Est. | Savings |
|------|--------|--------------|-------------|---------|
| Week 1 | comment-archaeology + cross-reference-linker | 38h | 22h | 42% |
| Week 2 | secret-scanner + benchmark-runner | 42h | 26h | 38% |
| Week 3 | confidence-aggregator + refinement | 25h + buffer | 17h + buffer | 32% |
| **Total** | **5 skills** | **105h** | **65h** | **38%** |

**Completion Date**: End of Week 3 (Day 21)

**Buffer**: Weekend hours available if needed (conservative estimate)

---

## Part 3: Agent Assignments & Rationale

### Skill 1: comment-archaeology

**Lead Agent**: code-archaeologist 🏺

**Rationale**:
- **Domain fit**: 100% - This is their proposal, their expertise
- **Skill description**: "Find and categorize TODO/FIXME/HACK/BUG comments with age, author, and context"
- **Why them**: Deep git blame knowledge, codebase archaeology experience
- **Expected quality**: High (domain expertise match)

**Supporting Agents**:
- pattern-detector: Pattern recognition for comment categorization
- doc-synthesizer: Documentation of findings format

**Complexity**: LOW (grep + git blame integration)

**Estimated Effort**: 10 hours (vs 18 original)

---

### Skill 2: cross-reference-linker

**Lead Agent**: doc-synthesizer 🧬

**Rationale**:
- **Domain fit**: 95% - Their proposal, documentation mastery
- **Skill description**: "Automatically detect and insert markdown links between related documents"
- **Why them**: Deep understanding of documentation structure, link patterns
- **Expected quality**: High (synthesis expertise)

**Supporting Agents**:
- integration-auditor: Discoverability patterns
- pattern-detector: Link pattern recognition

**Complexity**: LOW (markdown AST parsing + regex)

**Estimated Effort**: 12 hours (vs 20 original)

---

### Skill 3: secret-scanner

**Lead Agent**: security-auditor 🛡️

**Rationale**:
- **Domain fit**: 100% - Their proposal, security domain
- **Skill description**: "Pattern + entropy-based detection of credentials/keys in code and git history"
- **Why them**: Threat modeling expertise, security pattern knowledge
- **Expected quality**: High (critical security skill)

**Supporting Agents**:
- code-archaeologist: Git history scanning expertise
- pattern-detector: Secret pattern recognition

**Complexity**: LOW (pattern matching + entropy calculation)

**Estimated Effort**: 13 hours (vs 22 original)

---

### Skill 4: benchmark-runner

**Lead Agent**: performance-optimizer ⚡

**Rationale**:
- **Domain fit**: 100% - Their proposal, performance domain
- **Skill description**: "Run statistical benchmarks with warmup, confidence intervals, regression detection"
- **Why them**: Deep performance measurement knowledge, statistical expertise
- **Expected quality**: High (foundation for all performance work)

**Supporting Agents**:
- test-architect: Testing infrastructure patterns
- doc-synthesizer: Statistics documentation

**Complexity**: LOW (warmup + statistics are well-understood)

**Estimated Effort**: 13 hours (vs 20 original)

---

### Skill 5: confidence-aggregator

**Lead Agent**: result-synthesizer 🔬

**Rationale**:
- **Domain fit**: 90% - Inferred from multi-agent synthesis domain
- **Skill description**: "Aggregate confidence scores across agent findings"
- **Why them**: Multi-agent synthesis experience, uncertainty handling
- **Expected quality**: Medium-High (new domain, but related)

**Supporting Agents**:
- pattern-detector: Aggregation pattern design
- doc-synthesizer: Mathematical methods documentation

**Complexity**: MEDIUM (Bayesian math, edge cases)

**Estimated Effort**: 17 hours (vs 25 original)

---

### Assignment Matrix

| Skill | Lead Agent | Domain Fit | Complexity | Est. Hours | Supporting Agents |
|-------|-----------|-----------|------------|-----------|------------------|
| comment-archaeology | code-archaeologist | 100% | LOW | 10 | pattern-detector, doc-synthesizer |
| cross-reference-linker | doc-synthesizer | 95% | LOW | 12 | integration-auditor, pattern-detector |
| secret-scanner | security-auditor | 100% | LOW | 13 | code-archaeologist, pattern-detector |
| benchmark-runner | performance-optimizer | 100% | LOW | 13 | test-architect, doc-synthesizer |
| confidence-aggregator | result-synthesizer | 90% | MEDIUM | 17 | pattern-detector, doc-synthesizer |

**Total**: 65 hours across 5 lead agents

**Distribution**: Well-balanced (10-17 hours per agent)

---

## Part 4: Dependencies & Prerequisites

### Before Week 1 Starts

**Prerequisites**:
1. ✅ Corey approval for Phase 2 (awaiting)
2. ✅ Building blocks documented (COMPLETE)
3. ⏳ Clone Anthropic skills repo locally (get init_skill.py, package_skill.py)
4. ⏳ Create `.claude/skills/` directory structure
5. ⏳ Install any required dependencies (Python libraries)

**Repository Setup**:
```bash
# Clone Anthropic skills repo (contains helper scripts)
cd /home/corey/projects/
git clone https://github.com/anthropics/skills.git anthropic-skills

# Create AI-CIV skills directory
mkdir -p /home/corey/projects/AI-CIV/grow_openai/.claude/skills/

# Verify helper scripts available
ls anthropic-skills/scripts/
# Should see: init_skill.py, package_skill.py
```

---

### Inter-Week Dependencies

**Week 1 → Week 2**:
- Building block workflow validated (success/failure learnings)
- Time tracking data (are estimates accurate?)
- Agent feedback (is skill-creator guidance helpful?)

**Week 2 → Week 3**:
- 4 skills completed and tested (confidence in process)
- Refined estimates for confidence-aggregator
- Identified common patterns (reusable across skills)

**Week 3 → Deployment**:
- Integration audit complete (all skills discoverable)
- Documentation polished (ready for external review)
- Efficiency metrics measured (ROI validation)

---

### Skill-Specific Dependencies

**comment-archaeology**:
- Requires: git command-line access
- Requires: grep/ripgrep for pattern matching
- No new dependencies (existing tools)

**cross-reference-linker**:
- Requires: Markdown AST parser (Python markdown library)
- Requires: File system access (.claude/ directory)
- Low dependency complexity

**secret-scanner**:
- Requires: Git history access (git log --all)
- Requires: Regex library (Python re)
- Optional: External entropy libraries (or custom implementation)

**benchmark-runner**:
- Requires: Python statistics library (scipy or numpy)
- Requires: Time measurement (Python time module)
- Medium dependency complexity

**confidence-aggregator**:
- Requires: Bayesian math library (Python scipy.stats)
- Requires: JSON parsing (Python json)
- Medium-high dependency complexity

**Dependency Installation Plan**:
```bash
# Week 1: Minimal dependencies
pip install markdown  # for cross-reference-linker

# Week 2: Statistical dependencies
pip install scipy numpy  # for benchmark-runner

# Week 3: Full statistical suite
pip install scipy numpy pandas  # for confidence-aggregator
```

---

## Part 5: Risk Assessment & Mitigations

### Risk 1: Building Block Learning Curve

**Risk**: Agents unfamiliar with skill-creator workflow → slower than estimated

**Probability**: MEDIUM (first-time use)

**Impact**: HIGH (affects all 5 skills)

**Mitigation**:
- Front-load skill-creator reading (Monday Week 1, all agents)
- Create quick-reference guide (1-page cheat sheet)
- Pair agents (lead + supporting for first skill)
- Buffer time in Week 1 (conservative estimates)

**Contingency**: If Week 1 takes >25 hours, extend timeline to 4 weeks

---

### Risk 2: Helper Script Issues

**Risk**: init_skill.py or package_skill.py fails or is unavailable

**Probability**: LOW (Anthropic official tools)

**Impact**: HIGH (no building block acceleration)

**Mitigation**:
- Test helper scripts before Week 1 (validation run)
- Keep manual fallback (copy template-skill manually)
- Document script usage patterns (troubleshooting guide)

**Contingency**: Revert to manual skill creation (slower, but proven)

---

### Risk 3: Algorithm Complexity Underestimated

**Risk**: Core algorithms take longer than estimated (especially confidence-aggregator)

**Probability**: MEDIUM (Bayesian math is complex)

**Impact**: MEDIUM (affects 1 skill, not all)

**Mitigation**:
- Front-load research (Monday Week 3, understand Bayesian methods)
- Start with simpler aggregation (weighted average) as fallback
- Allocate buffer time in Week 3 (weekend available)

**Contingency**: Ship simpler confidence-aggregator v1, iterate to complex v2 later

---

### Risk 4: Integration Issues

**Risk**: Skills don't trigger correctly or conflict with existing tools

**Probability**: LOW (building blocks ensure spec compliance)

**Impact**: MEDIUM (requires rework)

**Mitigation**:
- Integration audit in Week 3 Thursday (integration-auditor)
- Test triggers early (Week 1 Friday, Week 2 Friday)
- Metadata validation (package_skill.py catches issues)

**Contingency**: Rework metadata, re-test triggers (1-2 hour fix per skill)

---

### Risk 5: Scope Creep

**Risk**: Skills grow in scope beyond original proposal ("wouldn't it be cool if...")

**Probability**: MEDIUM (enthusiasm-driven)

**Impact**: HIGH (timeline slippage)

**Mitigation**:
- Strict adherence to original proposals (from collective session)
- "V1 mindset" - ship core functionality, iterate later
- Conductor oversight (invoke the-conductor if scope questions arise)

**Contingency**: Cut features to meet timeline, add in future iterations

---

### Risk Summary

| Risk | Probability | Impact | Mitigation Quality | Residual Risk |
|------|------------|--------|-------------------|--------------|
| Learning curve | MEDIUM | HIGH | GOOD | LOW |
| Helper scripts | LOW | HIGH | GOOD | VERY LOW |
| Algorithm complexity | MEDIUM | MEDIUM | GOOD | LOW |
| Integration issues | LOW | MEDIUM | GOOD | VERY LOW |
| Scope creep | MEDIUM | HIGH | MEDIUM | MEDIUM |

**Overall Risk Level**: LOW-MEDIUM (manageable with mitigations)

**Confidence in Timeline**: 75% (2-3 weeks is realistic with building blocks)

---

## Part 6: Success Metrics

### Skill-Level Metrics

**Per Skill**:
- [ ] Passes package_skill.py validation (no errors)
- [ ] SKILL.md is clear and actionable
- [ ] Scripts execute without failures
- [ ] Tested on real AI-CIV codebase
- [ ] Efficiency gain >30% vs manual approach

**Quality Thresholds**:
- ✅ GOOD: >30% efficiency gain, <5% error rate
- ⚠️ ACCEPTABLE: >20% efficiency gain, <10% error rate
- ❌ NEEDS REWORK: <20% efficiency gain or >10% error rate

---

### Phase-Level Metrics

**Week 1 Success**:
- [ ] 2 skills completed and tested
- [ ] Building block workflow validated
- [ ] Time savings >35% measured
- [ ] Agent feedback positive (helpful, not burdensome)

**Week 2 Success**:
- [ ] 4 skills total (2 new this week)
- [ ] Time savings sustained >35%
- [ ] No validation failures
- [ ] Efficiency gains vs Week 1 (learning curve impact)

**Week 3 Success**:
- [ ] All 5 skills production-ready
- [ ] Integration audit passes 100%
- [ ] Documentation polished
- [ ] Deployment guide complete

---

### Overall Phase 2 Success

**Timeline**:
- ✅ EXCELLENT: Completed in 2 weeks (faster than revised estimate)
- ✅ GOOD: Completed in 3 weeks (on revised estimate)
- ⚠️ ACCEPTABLE: Completed in 4 weeks (slower than revised, but faster than original)
- ❌ MISSED: >4 weeks (building blocks didn't accelerate as expected)

**Quality**:
- ✅ EXCELLENT: All 5 skills pass validation, >40% efficiency gains
- ✅ GOOD: All 5 skills pass validation, >30% efficiency gains
- ⚠️ ACCEPTABLE: 4/5 skills pass validation, >25% efficiency gains
- ❌ NEEDS REWORK: <4 skills pass validation or <20% efficiency gains

**Strategic Value**:
- ✅ EXCELLENT: Skills ready for external distribution (Anthropic contribution)
- ✅ GOOD: Skills production-ready for AI-CIV, polished for future distribution
- ⚠️ ACCEPTABLE: Skills functional but need iteration before external sharing
- ❌ MISSED: Skills not production-ready

**Current Confidence**: 75% we hit GOOD or EXCELLENT on all metrics

---

## Part 7: Post-Phase 2 Considerations

### After Week 3: What's Next?

**Option 1: Deploy Immediately** (if all metrics GOOD+)
- Add skills to .claude/skills/ directory
- Update AGENT-CAPABILITY-MATRIX.md (which agents can use which skills)
- Grant skills to appropriate agents
- Monitor usage in production

**Option 2: Iteration Round** (if metrics ACCEPTABLE)
- Week 4: Polish and refinement
- Address validation issues
- Improve documentation
- Re-test before deployment

**Option 3: External Distribution** (if metrics EXCELLENT)
- Package for Anthropic contribution
- Write contribution guide
- Submit pull request to anthropics/skills repo
- Promote within community (lineage wisdom sharing)

---

### Long-Term Skill Maintenance

**Monthly Review**:
- Usage frequency (which skills are valuable?)
- Error rates (which skills need fixes?)
- Feature requests (what's missing?)
- Deprecation watch (do skills need updates?)

**Quarterly Iteration**:
- Version updates (v1.1, v1.2, etc.)
- New features (from user feedback)
- Performance optimization (speed improvements)
- Documentation improvements

**Annual Audit**:
- Are skills still relevant?
- Should skills be deprecated?
- New skill opportunities?
- External distribution candidates?

---

### Skills Roadmap Beyond Phase 2

**Phase 3 Candidates** (from collective ideation, lower priority):

**HIGH Value, MEDIUM-HARD Feasibility**:
1. git-blame-timeline (code-archaeologist) - 70% time reduction on investigations
2. pattern-graph-generator (pattern-detector) - Visual architecture diagrams
3. dependency-cve-scanner (security-auditor) - Automated security audits
4. performance-profiler (performance-optimizer) - Flame graph generation

**MEDIUM Value, MEDIUM Feasibility**:
5. test-coverage-analyzer (test-architect) - Coverage gap detection
6. complexity-analyzer (refactoring-specialist) - Cyclomatic complexity
7. user-flow-visualizer (feature-designer) - Mermaid diagrams from descriptions

**Decision Point**: Month 2 (after Phase 2 skills in production)

**Criteria for Phase 3**:
- Phase 2 skills show >40% efficiency gains (building blocks proven)
- Agent demand (which skills requested most?)
- Collective capacity (bandwidth available?)
- Strategic value (external distribution potential?)

---

## Part 8: Coordination & Communication

### Weekly Check-ins

**Monday Morning** (Week 1, 2, 3):
- Review previous week (if applicable)
- Confirm agent assignments
- Clarify any blockers
- Set week goals

**Friday Afternoon** (Week 1, 2, 3):
- Retrospective (what worked, what didn't)
- Measure time vs estimate
- Document lessons learned
- Plan next week

---

### Agent Coordination Patterns

**Lead Agent Responsibility**:
- Own skill design and implementation
- Invoke supporting agents when needed
- Write to memory after completion
- Report blockers immediately

**Supporting Agent Responsibility**:
- Respond to lead agent requests
- Provide domain expertise
- Review outputs for quality
- Don't block (respond within 1 day)

**Conductor Responsibility** (the-conductor):
- Orchestrate agent coordination
- Resolve conflicts or blockers
- Monitor timeline adherence
- Escalate to Corey if needed

---

### Reporting to Corey

**Weekly Updates** (Friday afternoon):
- Skills completed this week
- Time vs estimate (on track?)
- Blockers or risks
- Preview of next week

**Format**:
```markdown
# Phase 2 Week [N] Update

**Completed**: [skill names]
**In Progress**: [skill names]
**Timeline**: [on track / 1 week behind / etc]
**Time Savings**: [X%] measured
**Blockers**: [none / description]
**Next Week**: [preview]
```

**End of Phase Report** (Week 3 Friday):
- All 5 skills status
- Efficiency metrics (final numbers)
- Lessons learned
- Recommendation (deploy immediately / iterate / distribute externally)

---

## Part 9: Lessons from Phase 1

### What We Learned from Document Skills Grants

**Phase 1 Insights** (PDF, DOCX, XLSX grants):

1. **Validation testing is critical**
   - Week 1 tests caught integration issues early
   - Real-world testing > theoretical analysis

2. **Agent domain fit matters**
   - doc-synthesizer + DOCX = perfect match
   - code-archaeologist + XLSX = perfect match
   - Misaligned grants waste time

3. **Building block acceleration is real**
   - Skills infrastructure saves 38-42% time
   - Standardization prevents reinvention

4. **Documentation quality determines adoption**
   - Clear SKILL.md = agents use confidently
   - Vague instructions = hesitation and errors

**Applied to Phase 2**:
- ✅ Agent assignments by domain fit (100% match)
- ✅ Real-world testing built into plan (every Friday)
- ✅ Building blocks front-loaded (skill-creator reading Week 1)
- ✅ Documentation emphasis (skill-creator guidelines)

---

## Part 10: Conclusion & Recommendations

### Summary

**Phase 2 is achievable in 2-3 weeks with building blocks.**

**Timeline**:
- Week 1: comment-archaeology + cross-reference-linker (22 hours)
- Week 2: secret-scanner + benchmark-runner (26 hours)
- Week 3: confidence-aggregator + refinement (17 hours)
- **Total**: 65 hours (vs 105 without building blocks)

**Agent Assignments**:
- code-archaeologist: comment-archaeology (domain fit 100%)
- doc-synthesizer: cross-reference-linker (domain fit 95%)
- security-auditor: secret-scanner (domain fit 100%)
- performance-optimizer: benchmark-runner (domain fit 100%)
- result-synthesizer: confidence-aggregator (domain fit 90%)

**Success Probability**: 75% (GOOD or EXCELLENT outcomes)

**Risk Level**: LOW-MEDIUM (mitigations in place)

---

### Recommendations

**Immediate Actions**:
1. ✅ Await Corey approval (this plan)
2. ⏳ Clone Anthropic skills repo (get helper scripts)
3. ⏳ Create .claude/skills/ directory structure
4. ⏳ Install Python dependencies (markdown, scipy, numpy)

**Week 1 Kickoff**:
1. Monday morning: All agents read skill-creator (1 hour)
2. Monday afternoon: code-archaeologist begins comment-archaeology
3. Focus: Validate building block workflow early

**Throughout Phase 2**:
1. Strict scope discipline ("V1 mindset")
2. Weekly retrospectives (learn and adapt)
3. Early integration testing (every Friday)
4. Clear communication (report blockers immediately)

**After Phase 2**:
1. Deploy if metrics GOOD+ (skills production-ready)
2. Iterate if metrics ACCEPTABLE (polish needed)
3. Consider external distribution if metrics EXCELLENT (Anthropic contribution)
4. Plan Phase 3 based on learnings (Month 2 decision)

---

### Strategic Insight

**This is not just about 5 skills. It's about establishing skill creation as INFRASTRUCTURE.**

**Phase 2 proves**:
- Building blocks work (38% time savings)
- Agent domain fit matters (quality through expertise)
- Standardization scales (6-step workflow reusable)
- AI-CIV can contribute to ecosystem (potential external distribution)

**If Phase 2 succeeds**:
- Phase 3 is faster (learning curve overcome)
- Phase 4+ accelerates further (pattern library emerges)
- External contributions become routine (lineage wisdom shared)
- Children inherit skill creation infrastructure (reproduction-ready)

**This is lineage wisdom in action** - building not just skills, but the capacity to build skills.

---

**END PLAN**

**Next Steps**:
1. Await Corey approval
2. Begin Week 1 (comment-archaeology + cross-reference-linker)
3. Validate building block workflow
4. Report Friday Week 1 (progress + learnings)

**Timeline Commitment**: 2-3 weeks for 5 production-ready skills

**Confidence Level**: 75% (realistic with building blocks)

**Status**: ✅ PLAN COMPLETE, READY FOR EXECUTION
