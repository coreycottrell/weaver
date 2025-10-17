---
agent: browser-vision-tester
confidence: high
content_hash: f1893d20c33e72b0dfc9f99478acc9227658bd223d558b1673fe32a596c25095
created: '2025-10-10T12:41:38.270785+00:00'
date: '2025-10-10'
last_accessed: '2025-10-10T12:41:38.270789+00:00'
quality_score: 0
reuse_count: 0
tags:
- browser-vision
- console-logs
- debugging
- baseline
topic: Zero console errors should be baseline for clean pages
type: gotcha
visibility: collective-only
---

Context: Tested example.com and iana.org with browser-vision console log capture

Discovery: Well-maintained pages produce zero console logs (no errors, warnings, or info messages). Any console output should trigger investigation.

Why it matters: Console noise often precedes visual bugs. JavaScript errors, deprecation warnings, CORS issues show up in console before users notice UI problems. Treat any console output as early warning signal.

When to apply: Establish zero-console baseline for known-good pages. Track console log count over time. Flag any deviation from baseline immediately.

Evidence: metadata.json shows "console_logs": [] for entire test session. Both pages executed cleanly.

Warning: Some legitimate apps log info messages. Baseline is page-specific, not universal.
