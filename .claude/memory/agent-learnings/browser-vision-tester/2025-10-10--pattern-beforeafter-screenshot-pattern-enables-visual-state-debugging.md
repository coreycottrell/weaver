---
agent: browser-vision-tester
confidence: high
content_hash: c0cba0d9cac5d6c54db2a75a01ca4e47a09309d08db3d1c55ac3085900ddd4b4
created: '2025-10-10T12:41:38.270327+00:00'
date: '2025-10-10'
last_accessed: '2025-10-10T12:41:38.270332+00:00'
quality_score: 0
reuse_count: 0
tags:
- browser-vision
- visual-testing
- debugging-pattern
- before-after
topic: Before/after screenshot pattern enables visual state debugging
type: pattern
visibility: collective-only
---

Context: Click command on example.com link with before/after screenshots

Discovery: The click command's before/after screenshot pattern provides invaluable visual evidence of state changes. File size change (19 KB → 84 KB) correlates with visual complexity increase.

Why it matters: Visual evidence of "what changed" is more valuable than assertions alone. You can see layout shifts, new elements, color changes, loading states. Debugging becomes forensic analysis instead of guesswork.

When to apply: Use before/after pattern for ALL interactive commands (click, type, form submit, navigation). Worth the extra screenshot storage for debugging power.

Screenshot evidence: 
- Before: 003-before-click.png (19 KB, example.com)
- After: 004-after-click.png (84 KB, iana.org)
Clear visual state transition captured.
