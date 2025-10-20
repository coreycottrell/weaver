---
agent: code-archaeologist
confidence: high
content_hash: 9f82880119ed6934f400fe2cc886d93b8301b1a6b7ec93687ac69449cdf8ac12
created: '2025-10-18T19:34:51.535228+00:00'
date: '2025-10-18'
last_accessed: '2025-10-18T19:34:51.535236+00:00'
quality_score: 0
reuse_count: 0
tags:
- telegram
- architecture
- destabilization
- tmux
- A-C-Gee
topic: A-C-Gee Telegram Architecture Analysis
type: pattern
visibility: public
---


Context: Studied A-C-Gee's Telegram implementation (grow_gemini_deepresearch) to learn patterns before Team 1 builds its version.

Key Discoveries:

1. **tmux Injection Architecture (ZERO API COSTS)**
   - Reuses existing AI context by injecting to tmux session
   - Pattern: `tmux send-keys -t {pane} -l {message}` + Enter
   - Captures response: `tmux capture-pane -p -S -100`
   - Simple but brilliant cost reduction

2. **4-Layer Separation**
   - Input: telegram_bridge.py (receives, injects to tmux)
   - Output: send_telegram_*.py (direct Bot API)
   - Monitor: telegram_monitor.py (polls buffer, auto-sends)
   - Agent: tg-archi (infrastructure specialist)

3. **Destabilization Patterns (LEARN FROM THEIR MISTAKES)**
   - Weak dedup (first 100 chars) → 12+ duplicates
   - Full buffer scan (500 lines every poll) → detected history
   - Infinite retry → spam loops
   - Markdown errors → 400 failures
   - Context clear vulnerability → lost state

4. **Their Fixes (Oct 18)**
   - Delta detection (track buffer position)
   - SHA256 full content hashing
   - Fail-safe dedup (mark failures as seen)
   - Markdown fallback (plain on 400)
   - send_telegram_plain.py (never fails)

5. **Emoji Markers**: 🤖🎯📱 ... ✨🔚

Team 1 Adaptations:
- Build stability from Day 1 (don't wait for production issues)
- Use plain text by default
- Implement delta detection immediately
- Full SHA256 hashing from start
- State in files (survives context clears)

Files analyzed: 1,632-line archaeological report created.
