#!/bin/bash
# One-time injection test - auto-removes itself after running

cd /home/corey/projects/AI-CIV/grow_openai

# Run injection
./cron/inject-prompt.sh force 03-full-protocol.txt >> /home/corey/projects/AI-CIV/grow_openai/cron/cron.log 2>&1

# Remove this script and cron job
crontab -l | grep -v "one-time-test.sh" | crontab -
rm -f /home/corey/projects/AI-CIV/grow_openai/cron/one-time-test.sh

echo "[$(date '+%Y-%m-%d %H:%M:%S')] One-time injection test complete, cron job removed" >> /home/corey/projects/AI-CIV/grow_openai/cron/cron.log
