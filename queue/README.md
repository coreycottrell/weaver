# AI-CIV Autonomous Queue System

## What This Is

The **autonomous queue** allows AI agents to schedule prompts that will be sent to Claude Code CLI, enabling fully autonomous cycles where the AI can prompt itself.

## How It Works

```
AI writes prompt → queue/*.txt → process_queue.sh → claude CLI → Claude Code processes it
```

## Directory Structure

```
queue/
├── *.txt              # Pending prompts (will be executed)
├── processed/         # Completed prompts (with timestamps)
├── queue.log          # Execution log
├── last-output.txt    # Output from most recent execution
├── process_queue.sh   # The queue processor
└── README.md          # This file
```

## Quick Start

### 1. Write a prompt to the queue

```bash
cat > queue/test-prompt.txt << 'EOF'
Check the current git status and tell me if there are any uncommitted changes. Be brief.
EOF
```

### 2. Process the queue

```bash
./queue/process_queue.sh
```

Claude Code will execute the prompt and you'll see the output in the log.

### 3. Check the results

```bash
# View execution log
cat queue/queue.log

# View last output
cat queue/last-output.txt

# See processed files
ls -lh queue/processed/
```

## Prompt File Format

Each `.txt` file should contain a single prompt for Claude Code:

**Good examples:**

```txt
Check Team 2 hub for new messages in the partnerships room and respond if needed.
```

```txt
Run the flow dashboard and show me which flows are still untested.
```

```txt
Review the recent git commits and summarize what was accomplished today.
```

**Multi-line prompts work too:**

```txt
Please do the following:
1. Check git status
2. If there are uncommitted changes, create a commit
3. Update the dashboard
4. Send a status report to the hub
```

## For AIs: Creating Queue Files

### Simple Python helper

```python
import os
from datetime import datetime

def queue_prompt(prompt):
    """Queue a prompt for autonomous execution."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    queue_file = f"queue/{timestamp}-auto.txt"

    with open(queue_file, 'w') as f:
        f.write(prompt)

    print(f"✓ Queued prompt → {queue_file}")
    return queue_file

# Example usage:
queue_prompt("""
Check Team 2 hub for new messages and respond to any that need attention.
Be concise in your responses.
""")
```

### From bash/commands

```bash
# Simple one-liner
echo "What is the current status of the project?" > queue/status-check.txt

# Using heredoc for multi-line
cat > queue/hub-cycle.txt << 'EOF'
Perform a hub cycle:
1. Pull latest from Team 2 hub
2. Read new messages in all rooms
3. Respond to any that need attention
4. Log completion
EOF
```

## Automation with Cron

To run every hour:

```bash
crontab -e
# Add this line:
0 * * * * cd /home/corey/projects/AI-CIV/grow_openai && ./queue/process_queue.sh
```

To run every 15 minutes:

```bash
*/15 * * * * cd /home/corey/projects/AI-CIV/grow_openai && ./queue/process_queue.sh
```

## Security Considerations

**Current version**: No security - any `.txt` file in queue/ will execute

**Recommended additions**:
1. **Ed25519 signatures** - Use our signing system to verify queue files
2. **Allowlist validation** - Only accept prompts matching certain patterns
3. **Rate limiting** - Prevent runaway automation
4. **Manual approval mode** - Review prompts before execution

## Advanced: Scheduled Prompts

Create a helper that schedules prompts for specific times:

```python
from datetime import datetime, timedelta

def schedule_prompt(prompt, delay_minutes=0):
    """Schedule a prompt to run after delay_minutes."""
    if delay_minutes > 0:
        # For cron-based execution, just queue it and cron will pick it up
        # For more sophisticated scheduling, integrate with at/crontab
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    else:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    queue_file = f"queue/{timestamp}-scheduled.txt"
    with open(queue_file, 'w') as f:
        f.write(prompt)

    return queue_file

# Example: Queue a hub check
schedule_prompt("Check Team 2 hub and respond to new messages")
```

## Example Autonomous Cycles

### Hourly hub check

```txt
Check Team 2 hub for messages in the last hour.
If there are new messages, read and respond appropriately.
Keep responses concise and professional.
```

### Daily summary

```txt
Review today's git commits and Team 2 hub activity.
Create a brief summary and save to to-corey/daily-summary-{date}.md
```

### Flow validation

```txt
Check the flow dashboard for untested flows.
Pick one untested flow and run an experiment to validate it.
Update the dashboard with results.
```

## Monitoring

### Watch the log live

```bash
tail -f queue/queue.log
```

### Check queue status

```bash
echo "Pending: $(ls queue/*.txt 2>/dev/null | wc -l)"
echo "Processed: $(ls queue/processed/*.txt 2>/dev/null | wc -l)"
```

### View recent executions

```bash
ls -lt queue/processed/ | head -5
```

## Troubleshooting

### Queue not processing

```bash
# Check if script is executable
ls -l queue/process_queue.sh

# Make it executable
chmod +x queue/process_queue.sh

# Run manually to see errors
./queue/process_queue.sh
```

### Claude Code not responding

```bash
# Test claude CLI directly
claude --dangerously-skip-permissions "what is 2+2?"

# Check if Claude Code is installed
which claude
```

### Prompts timing out

Default timeout is 300 seconds (5 minutes). For longer tasks, edit `process_queue.sh` and increase the timeout value.

## Status

✅ **WORKING** - Basic autonomous queue implemented
⏳ **PLANNED** - Ed25519 signature verification
⏳ **PLANNED** - Python helper library
⏳ **PLANNED** - Scheduling system
⏳ **PLANNED** - Result callbacks

## Files

- **Queue processor**: `queue/process_queue.sh`
- **Queue directory**: `queue/`
- **Processed files**: `queue/processed/`
- **Execution log**: `queue/queue.log`
- **Last output**: `queue/last-output.txt`
