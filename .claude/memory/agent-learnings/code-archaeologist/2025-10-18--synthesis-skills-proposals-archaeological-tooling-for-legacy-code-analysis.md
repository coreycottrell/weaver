---
agent: code-archaeologist
confidence: high
content_hash: 58c5bfc7bd992f098e0879f3a54ebeecfb6910332fec3d4a0513f75afe0a9e93
created: '2025-10-18T17:04:19.045951+00:00'
date: '2025-10-18'
last_accessed: '2025-10-18T17:04:19.045963+00:00'
quality_score: 0
reuse_count: 0
tags:
- skills
- archaeological-tools
- historical-analysis
- technical-debt
topic: 'Skills proposals: Archaeological tooling for legacy code analysis'
type: synthesis
visibility: public
---


Context: Corey asked all agents to propose skills we'd benefit from.

My Domain Analysis:
As code-archaeologist, I repeatedly do manual detective work:
- Git history analysis (blame, log, show) - 4-6 commands per file
- Dead code detection (grep, manual correlation) - 10-15 min per function  
- Technical debt tracking (comment scanning, age analysis) - ad-hoc, incomplete

Skills Proposed:
1. git-blame-timeline (Medium feasibility, HIGH priority)
   - Rich git blame with commit messages and author activity
   - Would save 70% of investigation time
   - Benefits: 5+ other agents need historical context

2. dead-code-detector (Hard feasibility, MEDIUM priority)
   - Static analysis to find unused code with confidence scores
   - Risky if done wrong (false positives)
   - Benefits: Refactoring, security, performance agents

3. comment-archaeology (Easy feasibility, HIGH priority)
   - TODO/FIXME/HACK inventory with age/author/priority
   - Low-hanging fruit, immediate value
   - Benefits: Project health visibility for everyone

Recommendation: Build comment-archaeology first (easy win), then git-blame-timeline (core power).

Why This Matters:
Archaeological work is currently manual and time-consuming. These skills would:
- Make me 3-5x faster at legacy code analysis
- Provide shared historical context for entire collective
- Surface technical debt before it becomes critical

When to Apply:
- When designing archaeological/historical skills for any domain
- When prioritizing skill development (easy+high-value first)
- When analyzing what makes a specialist more powerful
