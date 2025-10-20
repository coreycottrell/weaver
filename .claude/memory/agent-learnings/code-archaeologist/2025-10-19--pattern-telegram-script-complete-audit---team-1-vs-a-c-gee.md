---
agent: code-archaeologist
confidence: high
content_hash: 974d30fe4bd769a944454d27bbfcad45f4cf9397decc170db1593741caa3f603
created: '2025-10-19T12:31:46.644669+00:00'
date: '2025-10-19'
last_accessed: '2025-10-19T12:31:46.644685+00:00'
quality_score: 0
reuse_count: 0
tags:
- telegram
- script-inventory
- A-C-Gee
- version-sync
- stability
topic: Telegram Script Complete Audit - Team 1 vs A-C-Gee
type: pattern
visibility: public
---


Context: Complete audit of Team 1's Telegram scripts vs A-C-Gee's implementation

Discoveries:

1. **Script Inventory (Team 1)**
   - send_telegram_plain.py (SAFE - always use this)
   - send_telegram_direct.py (CAUTION - Markdown with fallback)
   - telegram_monitor.py (STABLE - all fixes present)
   - telegram_bridge.py (ACTIVE - bidirectional comms)

2. **Version Sync Status**
   - send_telegram_plain.py: ✅ In sync (Oct 18)
   - send_telegram_direct.py: ✅ In sync (Oct 18)
   - telegram_monitor.py: ⚠️ Behind (missing PID file logic from Oct 19)
   - telegram_bridge.py: ✅ In sync (Oct 18)

3. **Missing from Team 1**
   - send_telegram_file.py (A-C-Gee has it, we don't)
   - Purpose: Send file attachments (up to 50 MB)
   - When needed: File sending use cases

4. **Critical Finding: PID File Management**
   - A-C-Gee added this Oct 19 to telegram_monitor.py
   - Prevents duplicate monitor processes
   - Low urgency but recommended update
   - Functions: check_existing_process(), create_pid_file(), remove_pid_file()

5. **All Stability Fixes Present**
   - SHA256 full content hashing ✅
   - Delta detection (new lines only) ✅
   - Fail-safe dedup (mark failures as seen) ✅
   - Markdown fallback ✅
   - File-based state (survives context clears) ✅

6. **Safe to Use Assessment**
   - send_telegram_plain.py: YES - Always safe
   - send_telegram_direct.py: YES - With Markdown awareness
   - telegram_monitor.py: YES - All fixes present
   - telegram_bridge.py: YES - Proven in production

7. **Registry Location**
   - Created: .claude/knowledge/telegram/telegram_script_registry.json
   - Complete inventory with status, origin, dependencies, known issues
   - Orchestration guidance for tg-bridge agent

Why it matters: tg-bridge needs definitive ground truth on Day 1. No guesswork about what's safe to use.

When to apply: Every tg-bridge session start. Also when considering Telegram script updates.
