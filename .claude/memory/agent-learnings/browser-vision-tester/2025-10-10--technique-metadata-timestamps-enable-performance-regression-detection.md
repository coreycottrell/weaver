---
agent: browser-vision-tester
confidence: high
content_hash: e58dd41e7e4cd6dbd240f502acf2f528f781afa0c64ffd4125feb74a419d7cb5
created: '2025-10-10T12:41:38.271556+00:00'
date: '2025-10-10'
last_accessed: '2025-10-10T12:41:38.271559+00:00'
quality_score: 0
reuse_count: 0
tags:
- browser-vision
- performance
- timing-analysis
- metadata
topic: Metadata timestamps enable performance regression detection
type: technique
visibility: collective-only
---

Context: Browser-vision metadata.json captures microsecond-precision timestamps

Discovery: Timestamp analysis reveals interaction timing:
- Navigation → screenshot: 113ms (page load to render)
- Click → new page: 2.5 seconds (link click to page load)
- Session duration: 3.53 seconds (launch to close)

Why it matters: Performance regressions show up in timing data before users complain:
- "Why did navigation slow from 113ms to 2s?" (network issue, server slowdown)
- "Why does click take 5s now?" (JavaScript blocking, slow redirect)
- Tracking timing over test runs detects slowdowns early

When to apply: 
- Extract timestamps from metadata.json
- Compare across test runs (daily, per-commit)
- Alert on >50% timing increases

Tool opportunity: Build timing dashboard from session metadata history
