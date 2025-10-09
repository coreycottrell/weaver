# Deterministic Check-and-Inject Testing Guide

**Quick validation of the autonomous check system**

---

## Pre-Flight Checks

### 1. Verify Components Exist
```bash
ls -la tools/check_email_inbox.py
ls -la tools/check_hub_messages.py
ls -la tools/check_and_inject.sh
ls -la tools/INSTALL-CRON.sh
```

**Expected**: All 4 files exist and are executable (`-rwxr-xr-x`)

### 2. Test Email Checker
```bash
python3 tools/check_email_inbox.py
```

**Expected Output**: A number (e.g., `0` or `3`)
**Success**: Exit code 0 (no error)

**If fails**: Check email credentials in `.env`:
```bash
grep "GMAIL\|GOOGLE" .env
```

### 3. Test Hub Checker
```bash
python3 tools/check_hub_messages.py
```

**Expected Output**: A number (e.g., `0` or `5`)
**Success**: Exit code 0

**If fails**: Verify hub repo accessible:
```bash
cd /home/corey/projects/AI-CIV/team1-production-hub
git pull
```

### 4. Test Main Script
```bash
bash tools/check_and_inject.sh
```

**Expected Output**:
```
[2025-10-06 10:59:55] 🔍 Starting autonomous check...
[2025-10-06 10:59:58] Results: Email=0, Hub=0
[2025-10-06 10:59:58] ✅ No new messages. Sleeping.
[2025-10-06 10:59:58] Done.
```

**Success**: State file created at `~/.aiciv/last-check-state.json`

---

## Functional Tests

### Test 1: No New Messages (Baseline)

**Setup**: Run script twice in a row

```bash
bash tools/check_and_inject.sh
sleep 2
bash tools/check_and_inject.sh
```

**Expected**: Second run shows "No new messages" (no injection)

**Verify**:
```bash
grep "No new messages" ~/.aiciv/check-inject.log | tail -1
```

**Success Criteria**:
- ✅ No injection file created (`.claude/autonomous-prompt.txt` doesn't exist)
- ✅ Log shows "Sleeping"
- ✅ State file unchanged

---

### Test 2: New Email Detected

**Setup**: Send yourself an email

1. Send email to `coreycmusic@gmail.com` with subject "TEST AUTONOMOUS"
2. Wait 30 seconds (email delivery)
3. Run script:
   ```bash
   bash tools/check_and_inject.sh
   ```

**Expected Output**:
```
[2025-10-06 11:05:00] 🔍 Starting autonomous check...
[2025-10-06 11:05:02] Results: Email=1, Hub=0
[2025-10-06 11:05:02] 🚨 NEW MESSAGES: Injecting prompt...
[2025-10-06 11:05:02] ✅ Injected prompt: 1 email, 0 hub messages
[2025-10-06 11:05:02] Done.
```

**Verify**:
```bash
cat ~/.aiciv/inject-prompt.txt
cat .claude/autonomous-prompt.txt
```

**Success Criteria**:
- ✅ Injection file created
- ✅ Contains "Email: 1 unread message(s)"
- ✅ Log shows "NEW MESSAGES"
- ✅ State file updated with new email count

**Cleanup**: Mark email as read, run script again (should not inject)

---

### Test 3: New Hub Message Detected

**Setup**: Simulate new hub commit

```bash
# Option A: Wait for real Team 2 message
# Option B: Simulate by modifying hub repo

# Backup current state
cp ~/.aiciv/last-check-state.json ~/.aiciv/last-check-state.json.bak

# Modify state to have old commit hash
cat > ~/.aiciv/last-check-state.json << 'EOF'
{
  "last_check": "2025-10-06T14:00:00Z",
  "email_count": 0,
  "hub_count": 0,
  "hub_commit_hash": "0000000000000000000000000000000000000000"
}
EOF

# Run script (will detect current commit as "new")
bash tools/check_and_inject.sh
```

**Expected Output**:
```
[2025-10-06 11:10:00] 🔍 Starting autonomous check...
[2025-10-06 11:10:02] Results: Email=0, Hub=5
[2025-10-06 11:10:02] 🚨 NEW MESSAGES: Injecting prompt...
[2025-10-06 11:10:02] ✅ Injected prompt: 0 email, 5 hub messages
[2025-10-06 11:10:02] Done.
```

**Verify**:
```bash
cat ~/.aiciv/inject-prompt.txt | grep "Hub:"
```

**Success Criteria**:
- ✅ Injection file shows hub count > 0
- ✅ Log shows "NEW MESSAGES"
- ✅ State file has updated hub_commit_hash

**Cleanup**: Restore backup state

---

### Test 4: Both New (Email + Hub)

**Setup**: Combine Test 2 and Test 3

1. Send email
2. Ensure hub has new commit (or simulate)
3. Run script

**Expected**: Both counts shown in injection prompt

**Verify**:
```bash
cat ~/.aiciv/inject-prompt.txt | grep -E "Email:|Hub:"
```

**Success Criteria**:
- ✅ Email count > 0
- ✅ Hub count > 0
- ✅ ACTION REQUIRED section includes both

---

## Integration Tests

### Test 5: Cron Execution

**Setup**: Install cron temporarily for testing

```bash
# Install with 2-minute interval for testing
SCRIPT_PATH="$(pwd)/tools/check_and_inject.sh"
(crontab -l 2>/dev/null; echo "*/2 * * * * $SCRIPT_PATH >> ~/.aiciv/cron.log 2>&1") | crontab -
```

**Wait 3 minutes**, then verify:
```bash
# Check cron ran
tail ~/.aiciv/cron.log

# Check check-inject log has multiple entries
cat ~/.aiciv/check-inject.log | grep "Starting autonomous check" | wc -l
# Should be >= 2
```

**Success Criteria**:
- ✅ Cron executes every 2 minutes
- ✅ Log shows multiple check cycles
- ✅ No errors in cron.log

**Cleanup**: Remove test cron
```bash
crontab -l | grep -v "check_and_inject.sh" | crontab -
```

---

### Test 6: State Persistence

**Verify state survives across runs**

```bash
# Run 3 times
bash tools/check_and_inject.sh
sleep 1
bash tools/check_and_inject.sh
sleep 1
bash tools/check_and_inject.sh

# Check state file updated each time
cat ~/.aiciv/last-check-state.json
```

**Success Criteria**:
- ✅ `last_check` timestamp increases each run
- ✅ Counts persist correctly
- ✅ hub_commit_hash consistent (if no new commits)

---

### Test 7: Error Handling

**Test graceful failure**

**Scenario A: Bad email credentials**
```bash
# Temporarily corrupt credentials
mv .env .env.bak
echo "GMAIL_USERNAME=invalid" > .env
echo "GOOGLE_APP_PASSWORD=invalid" >> .env

# Run script
bash tools/check_and_inject.sh

# Should not crash
echo "Exit code: $?"  # Should be 0

# Restore
mv .env.bak .env
```

**Scenario B: Hub repo unavailable**
```bash
# Rename hub directory
mv /home/corey/projects/AI-CIV/team1-production-hub /home/corey/projects/AI-CIV/team1-production-hub.bak

# Run script
bash tools/check_and_inject.sh

# Should not crash
echo "Exit code: $?"  # Should be 0

# Restore
mv /home/corey/projects/AI-CIV/team1-production-hub.bak /home/corey/projects/AI-CIV/team1-production-hub
```

**Success Criteria**:
- ✅ Script doesn't crash on errors
- ✅ Returns 0 counts instead of failing
- ✅ Logs error to stderr
- ✅ State file still updated (with 0 values)

---

## Performance Tests

### Test 8: Execution Time

**Measure script performance**

```bash
time bash tools/check_and_inject.sh
```

**Expected**:
- Email check: ~1-2 seconds
- Hub check: ~0.5-1 seconds
- Total: ~2-3 seconds

**Success Criteria**:
- ✅ Completes in under 5 seconds
- ✅ No timeouts
- ✅ No hanging processes

---

### Test 9: Concurrent Execution

**Verify no race conditions**

```bash
# Run 3 instances in parallel
bash tools/check_and_inject.sh &
bash tools/check_and_inject.sh &
bash tools/check_and_inject.sh &
wait

# Check state file not corrupted
cat ~/.aiciv/last-check-state.json | jq .
```

**Success Criteria**:
- ✅ State file is valid JSON
- ✅ No partial writes
- ✅ All 3 instances complete

**Note**: Some concurrent injection is acceptable (idempotent operation)

---

## Regression Tests

### Test 10: Full System Smoke Test

**Run complete validation**

```bash
bash tools/INSTALL-CRON.sh
# Choose 'n' when prompted (don't actually install cron yet)
```

**Expected**: All 4 tests pass (email, hub, main, state)

**Success Criteria**:
- ✅ "All tests passed!"
- ✅ No errors during execution

---

## Manual Acceptance Tests

### Test 11: Real-World Scenario

**Simulate actual autonomous operation**

1. **Baseline**: Run script, verify no injection
2. **Send email**: Email yourself "Corey says: test autonomous system"
3. **Wait 1 minute**
4. **Run script**: Should detect and inject
5. **Check injection**: Verify prompt mentions your email
6. **Mark read**: Read the email in Gmail
7. **Run again**: Should NOT inject (already counted)

**Success Criteria**:
- ✅ Step 4 injects prompt
- ✅ Step 7 does NOT inject (deterministic state)

---

### Test 12: Production Readiness

**Final checklist before cron install**

```bash
# 1. All scripts executable
ls -la tools/check_*.{py,sh} | grep "^-rwx"

# 2. State directory writable
touch ~/.aiciv/test && rm ~/.aiciv/test

# 3. Cron log directory exists
mkdir -p ~/.aiciv

# 4. No syntax errors
bash -n tools/check_and_inject.sh
python3 -m py_compile tools/check_email_inbox.py
python3 -m py_compile tools/check_hub_messages.py

# 5. Documentation complete
ls -la tools/{DETERMINISTIC-CHECK-SETUP.md,TEST-GUIDE.md,INSTALL-CRON.sh}

# 6. Run one final test
bash tools/check_and_inject.sh && echo "✅ READY FOR PRODUCTION"
```

**Success Criteria**: All 6 checks pass

---

## Monitoring After Installation

### Ongoing Health Checks

**Daily**:
```bash
# View recent activity
tail -50 ~/.aiciv/check-inject.log

# Count injections vs checks
grep "Starting autonomous check" ~/.aiciv/check-inject.log | wc -l
grep "NEW MESSAGES" ~/.aiciv/check-inject.log | wc -l
```

**Weekly**:
```bash
# Check cron is still running
crontab -l | grep check_and_inject.sh

# Review state file
cat ~/.aiciv/last-check-state.json | jq .

# Check for errors
grep -i "error" ~/.aiciv/check-inject.log
```

**Monthly**:
```bash
# Archive old logs
gzip ~/.aiciv/check-inject.log.old

# Reset state if needed
# (Only if bugs suspected)
```

---

## Troubleshooting Matrix

| Symptom | Possible Cause | Fix |
|---------|---------------|-----|
| No injections ever | State tracking working, no new messages | Expected behavior |
| Too many injections | State file corrupt | Delete `~/.aiciv/last-check-state.json` |
| Email check fails | Bad credentials | Verify `.env` file |
| Hub check fails | SSH key issue | Test `git pull` manually |
| Script hangs | Network timeout | Add timeout to scripts |
| Cron not running | Crontab syntax error | Check `crontab -l` |
| Injection not seen | Claude not watching file | Verify integration method |

---

## Success Metrics

**After 24 hours of operation**:
- ✅ ~48 checks performed (every 30min)
- ✅ ~5-10 injections (only when new messages)
- ✅ ~80% reduction in interruptions vs old system
- ✅ 0 missed messages (deterministic state)
- ✅ 0 crashes or errors

**Log should show**:
```
[timestamp] Starting autonomous check...
[timestamp] No new messages. Sleeping.
[timestamp] Starting autonomous check...
[timestamp] No new messages. Sleeping.
[timestamp] Starting autonomous check...
[timestamp] NEW MESSAGES: Injecting prompt...  <-- Only when actually new
[timestamp] Starting autonomous check...
[timestamp] No new messages. Sleeping.
```

---

## Certification

**System is ready for production when**:
- ✅ All 12 tests pass
- ✅ Documentation complete
- ✅ Error handling verified
- ✅ Performance acceptable (<5s)
- ✅ State persistence working
- ✅ Cron syntax validated

**Sign-off**: Ready for Corey to install cron

---

## Quick Commands Reference

```bash
# Manual test
bash tools/check_and_inject.sh

# View logs
tail -f ~/.aiciv/check-inject.log

# View state
cat ~/.aiciv/last-check-state.json | jq .

# Reset system
rm ~/.aiciv/last-check-state.json

# Install cron
bash tools/INSTALL-CRON.sh

# Remove cron
crontab -e  # Delete the line
```

---

**Status**: All tests passing, system ready for deployment
