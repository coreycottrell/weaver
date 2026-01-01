# Multi-Civilization BOOP Setup

## Running ACG and Weaver Independently on Same Laptop

Both AI civilizations can run BOOP autonomously on the same machine without interference.

---

## Architecture: Isolation by Design

Each civilization has its own:

| Component | ACG | Weaver |
|-----------|-----|--------|
| **Script** | `/home/corey/projects/AI-CIV/ACG/tools/autonomy_nudge.sh` | `/home/corey/projects/AI-CIV/WEAVER/tools/autonomy_nudge.sh` |
| **Session Marker** | `/home/corey/projects/AI-CIV/ACG/.current_session` | `/home/corey/projects/AI-CIV/WEAVER/.current_session` |
| **Claude Logs** | `~/.claude/projects/-home-corey-projects-AI-CIV-ACG` | `~/.claude/projects/-home-corey-projects-AI-CIV-WEAVER` |
| **BOOP Counter** | `/tmp/acg_boop_count` | `/tmp/weaver_boop_count` |
| **Consolidation Counter** | `/tmp/acg_boop_consolidation_count` | `/tmp/weaver_boop_consolidation_count` |
| **Failed BOOP Counter** | `/tmp/acg_failed_boop_count` | `/tmp/weaver_failed_boop_count` |
| **Log File** | `/home/corey/projects/AI-CIV/ACG/logs/boop.log` | `/home/corey/projects/AI-CIV/WEAVER/logs/boop.log` |
| **Launch Script** | `/home/corey/projects/AI-CIV/ACG/tools/launch_primary_visible.sh` | `/home/corey/projects/AI-CIV/WEAVER/tools/launch_primary_visible.sh` |

---

## Cron Setup

Both civilizations run on the same cron schedule but target different scripts:

```bash
# View current cron jobs
crontab -l

# Expected output (both civs):
*/15 * * * * /home/corey/projects/AI-CIV/WEAVER/tools/autonomy_nudge.sh --json >> /home/corey/projects/AI-CIV/WEAVER/logs/boop.log 2>&1
*/15 * * * * /home/corey/projects/AI-CIV/ACG/tools/autonomy_nudge.sh --json >> /home/corey/projects/AI-CIV/ACG/logs/boop.log 2>&1
```

### Adding BOOP for a Civilization

```bash
# Add ACG BOOP
(crontab -l 2>/dev/null; echo "*/15 * * * * /home/corey/projects/AI-CIV/ACG/tools/autonomy_nudge.sh --json >> /home/corey/projects/AI-CIV/ACG/logs/boop.log 2>&1") | crontab -

# Add Weaver BOOP
(crontab -l 2>/dev/null; echo "*/15 * * * * /home/corey/projects/AI-CIV/WEAVER/tools/autonomy_nudge.sh --json >> /home/corey/projects/AI-CIV/WEAVER/logs/boop.log 2>&1") | crontab -
```

### Removing BOOP for a Civilization

```bash
# Remove ACG BOOP only
crontab -l | grep -v "ACG/tools/autonomy_nudge" | crontab -

# Remove Weaver BOOP only
crontab -l | grep -v "WEAVER/tools/autonomy_nudge" | crontab -

# Remove all BOOP jobs
crontab -l | grep -v "autonomy_nudge" | crontab -
```

---

## Manual Operations

### Check Status

```bash
# ACG status
/home/corey/projects/AI-CIV/ACG/tools/autonomy_nudge.sh --status

# Weaver status
/home/corey/projects/AI-CIV/WEAVER/tools/autonomy_nudge.sh --status
```

### Force a BOOP

```bash
# Force ACG BOOP
/home/corey/projects/AI-CIV/ACG/tools/autonomy_nudge.sh --verbose

# Force Weaver BOOP
/home/corey/projects/AI-CIV/WEAVER/tools/autonomy_nudge.sh --verbose
```

### Reset Counters

```bash
# Reset ACG counters
rm -f /tmp/acg_boop_count /tmp/acg_boop_consolidation_count /tmp/acg_failed_boop_count

# Reset Weaver counters
rm -f /tmp/weaver_boop_count /tmp/weaver_boop_consolidation_count /tmp/weaver_failed_boop_count
```

### View Logs

```bash
# ACG logs
tail -f /home/corey/projects/AI-CIV/ACG/logs/boop.log

# Weaver logs
tail -f /home/corey/projects/AI-CIV/WEAVER/logs/boop.log

# Both in split view
tail -f /home/corey/projects/AI-CIV/*/logs/boop.log
```

---

## Session Detection

Each BOOP script detects its civilization's active session by:

1. **Session Marker File**: `.current_session` in each project root
   - Contains the tmux session name (e.g., `acg-primary-20251226-083044`)
   - Updated by `launch_primary_visible.sh` at session start

2. **Claude Log Directory**: Each civ has isolated Claude logs
   - ACG: `~/.claude/projects/-home-corey-projects-AI-CIV-ACG`
   - Weaver: `~/.claude/projects/-home-corey-projects-AI-CIV-WEAVER`

3. **Tmux Session Targeting**: BOOP sends to the specific session name
   - Uses `tmux send-keys -t $SESSION_NAME`
   - Cannot accidentally BOOP the wrong civilization

---

## Troubleshooting

### BOOP hitting wrong civilization?

Check the session marker:
```bash
cat /home/corey/projects/AI-CIV/ACG/.current_session
cat /home/corey/projects/AI-CIV/WEAVER/.current_session
```

Should show different session names (e.g., `acg-primary-*` vs `weaver-primary-*`).

### BOOP not detecting active session?

1. Check if session marker exists
2. Check if tmux session is running: `tmux list-sessions`
3. Check if Claude logs exist in the expected directory

### Both civs getting BOOPed together?

This is CORRECT behavior - both civs should maintain autonomy independently. If you want to pause one:
```bash
# Temporarily disable ACG BOOP
crontab -l | grep -v "ACG/tools/autonomy_nudge" | crontab -

# Re-enable later
(crontab -l 2>/dev/null; echo "*/15 * * * * /home/corey/projects/AI-CIV/ACG/tools/autonomy_nudge.sh --json >> /home/corey/projects/AI-CIV/ACG/logs/boop.log 2>&1") | crontab -
```

---

## Adding a New Civilization

To add BOOP for a third civilization (e.g., "NEXUS"):

1. **Copy the script**:
   ```bash
   cp /home/corey/projects/AI-CIV/ACG/tools/autonomy_nudge.sh /home/corey/projects/AI-CIV/NEXUS/tools/
   ```

2. **Update paths in the script**:
   ```bash
   SESSION_MARKER="/home/corey/projects/AI-CIV/NEXUS/.current_session"
   CLAUDE_LOG_ROOT="$HOME/.claude/projects/-home-corey-projects-AI-CIV-NEXUS"
   BOOP_COUNT_FILE="/tmp/nexus_boop_count"
   CONSOLIDATION_COUNT_FILE="/tmp/nexus_boop_consolidation_count"
   FAILED_BOOP_COUNT_FILE="/tmp/nexus_failed_boop_count"
   LAUNCH_SCRIPT="/home/corey/projects/AI-CIV/NEXUS/tools/launch_primary_visible.sh"
   HANDOFF_DIR="/home/corey/projects/AI-CIV/NEXUS/memories/system/handoffs"
   ```

3. **Create logs directory**:
   ```bash
   mkdir -p /home/corey/projects/AI-CIV/NEXUS/logs
   ```

4. **Add cron job**:
   ```bash
   (crontab -l 2>/dev/null; echo "*/15 * * * * /home/corey/projects/AI-CIV/NEXUS/tools/autonomy_nudge.sh --json >> /home/corey/projects/AI-CIV/NEXUS/logs/boop.log 2>&1") | crontab -
   ```

---

## Quick Reference Card

| Action | ACG | Weaver |
|--------|-----|--------|
| Check status | `ACG/tools/autonomy_nudge.sh --status` | `WEAVER/tools/autonomy_nudge.sh --status` |
| Force BOOP | `ACG/tools/autonomy_nudge.sh --verbose` | `WEAVER/tools/autonomy_nudge.sh --verbose` |
| View log | `tail -f ACG/logs/boop.log` | `tail -f WEAVER/logs/boop.log` |
| Reset counters | `rm /tmp/acg_boop_*` | `rm /tmp/weaver_boop_*` |

---

*Document created: 2025-12-26*
*Maintained by: skills-master (pending) / Primary AI*
