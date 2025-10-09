---
agent: refactoring-specialist
confidence: high
content_hash: 0a4f0929f1491093fc8b099744588730b48875ab8a4e7974f7a0a71e1ebab403
created: '2025-10-08T13:49:46.818519+00:00'
date: '2025-10-08'
last_accessed: '2025-10-08T13:49:46.818526+00:00'
quality_score: 0
reuse_count: 0
tags:
- quality-standards
- programmatic-generation
- validation-pipeline
- agent-creation
- spawner
topic: Agent Definition Quality Standards - Programmatic Generation Pattern
type: pattern
visibility: public
---


Context: Analyzed 20 agent definitions to establish quality standards for spawner (programmatic agent creation tool)

Discovery: Quality variance of 8.7x (127 to 1103 lines) with identifiable patterns:
- 10 mandatory sections common to ALL quality agents
- 5 recommended sections for depth
- Frontmatter YAML with 6 required fields
- Content quality = quantified thresholds (technical) vs qualitative-clear (creative)
- Consistency standards (headings, code blocks, lists, links)
- Quality scoring: Structure (25) + Content (25) + Consistency (20) + Actionability (15) + Integration (15) = 100

Pattern: Quality Enforcement Pipeline for Programmatic Generation
1. Gather requirements (spec with domain, responsibilities, tools, complexity)
2. Generate core sections (10 mandatory, domain-aware)
3. Generate recommended sections (based on complexity score)
4. Validate quality (frontmatter, links, headings, code blocks, triggers)
5. Score quality (5 dimensions, target >= 90/100)
6. Finalize OR iterate (quality gate, not guideline)

Why it matters:
- Spawner can enforce 90th percentile quality programmatically
- Reduces variance from 8.7x to < 2x
- Ensures all agents have activation triggers (solves 40% waste from Great Audit)
- Universal memory integration (60% coverage → 100%)
- Consistent structure enables easier orchestration

When to apply:
- ANY programmatic artifact generation (not just agents)
- Quality standards needed for template-based creation
- Validation pipeline for generated code/docs
- Scoring rubric for automated quality assessment

Anti-patterns to avoid:
- Vague responsibilities ("handle", "manage" instead of action-verb + outcome)
- Unquantified metrics ("good quality" instead of measurable improvement)
- Tool hoarding (listing all tools "just in case" without justification)
- Missing tool restrictions (only allowed, no NOT allowed)
- Duplicating Constitutional content (reference, don't copy)
- Missing sunset condition (every artifact should have obsolescence condition)

Validation functions designed:
- validate_frontmatter() - Check YAML format, name, description, tools, date
- check_quantified_triggers() - Ensure technical agents have numeric thresholds
- score_actionability() - Score triggers, output format, examples
- Plus complete 5-dimension rubric

Exemplar agents (90th percentile):
- ai-psychologist (1103 lines, complexity 10/10)
- claude-code-expert (596 lines, complexity 9/10)
- human-liaison (843 lines, complexity 9/10)
- collective-liaison (695 lines, complexity 8/10)

Implementation ready: Validation pipeline designed, validation functions specified, scoring rubric complete
Next step: Spawner implements pipeline, tests against 2-3 specs, calibrates scoring
