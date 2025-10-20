# Telegram Infrastructure Quick Reference

**Last Updated**: 2025-10-20
**Status**: ✅ WORKING (zero duplicates)

---

## 🚀 Every Session (Copy-Paste)

```bash
cd /home/corey/projects/AI-CIV/grow_openai

# Start Telegram infrastructure
nohup python3 tools/prod/tg/openai_telegram_jsonl_monitor.py >> /tmp/openai_telegram_jsonl_monitor.log 2>&1 &
nohup python3 tools/openai_telegram_bridge_diagnostic.py >> /tmp/openai_telegram_bridge_diagnostic.log 2>&1 &
sleep 2

# Verify both started
ps aux | grep -E "openai_telegram" | grep -v grep
```

**Expected**: 2 processes (monitor + bridge)

---

## 🧪 Test (Every Session)

Send via Telegram: `Wake-up test`

**Expected**:
- ✅ Appears ONCE in Claude Code
- ✅ No duplicates after 30 seconds
- ✅ Your response arrives on Telegram

---

## 🛑 Stop (If Needed)

```bash
pkill -f openai_telegram_bridge_diagnostic
pkill -f openai_telegram_jsonl_monitor
```

---

## 📁 Files (Working)

- **Bridge**: `tools/openai_telegram_bridge_diagnostic.py` ✅
- **Monitor**: `tools/prod/tg/openai_telegram_jsonl_monitor.py` ✅
- **Config**: `config/telegram_config.json` ✅
- **Logs**: `/tmp/openai_telegram_bridge_diagnostic.log`, `/tmp/openai_telegram_jsonl_monitor.log`

---

## 🔧 Troubleshooting

**Duplicates?**
- Check bridge: `ps aux | grep openai_telegram_bridge_diagnostic`
- Should see diagnostic version, not `tools/prod/tg/openai_telegram_bridge.py` (broken)

**No response on Telegram?**
- Restart monitor: `pkill -f openai_telegram_jsonl_monitor && cd /home/corey/projects/AI-CIV/grow_openai && nohup python3 tools/prod/tg/openai_telegram_jsonl_monitor.py >> /tmp/openai_telegram_jsonl_monitor.log 2>&1 &`

**Check logs**:
```bash
tail -20 /tmp/openai_telegram_bridge_diagnostic.log
tail -20 /tmp/openai_telegram_jsonl_monitor.log
```

---

## 📚 Full Documentation

**Wake-Up**: `to-corey/TELEGRAM-WAKEUP-PROCEDURE.md` (detailed)
**Production Lock**: `tools/prod/tg/PRODUCTION-LOCK-STATUS.md` (for agents)
**Archive**: `tools/.archive/telegram-cleanup-2025-10-20/MANIFEST.md` (what was broken)

---

**Keep this handy. It's all you need for perfect Telegram wake-ups.**
