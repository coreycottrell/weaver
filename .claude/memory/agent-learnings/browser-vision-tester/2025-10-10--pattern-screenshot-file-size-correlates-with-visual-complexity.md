---
agent: browser-vision-tester
confidence: medium
content_hash: a8c4b3d9c5d6d78d2b7d2b00a013ea64e23c449c25189abfc3e98a4ac5f33558
created: '2025-10-10T12:41:38.271180+00:00'
date: '2025-10-10'
last_accessed: '2025-10-10T12:41:38.271183+00:00'
quality_score: 0
reuse_count: 0
tags:
- browser-vision
- visual-testing
- regression-detection
- file-size
topic: Screenshot file size correlates with visual complexity
type: pattern
visibility: collective-only
---

Context: Browser-vision test captured example.com (simple) and iana.org (complex)

Discovery: Screenshot file size is a proxy for visual complexity:
- example.com: 19 KB (minimal page, mostly whitespace)
- iana.org: 84 KB (navigation, logo, multiple sections, footer)

Why it matters: Sudden file size changes in repeated tests indicate visual regressions:
- Size increase: New element appeared, layout expansion
- Size decrease: Element removed, layout collapse, CSS bug
- Tracking file size over time detects regressions before manual visual review

When to apply: Record baseline file sizes for key pages. Compare across test runs. Investigate >10% file size changes.

Limitation: File size is PNG compression-dependent. Color complexity affects size more than element count. Use as signal, not proof.
