#!/bin/bash

# AI-CIV Primary AI Autonomous Launcher (Visible Window)
# Opens new Windows Terminal tab with tmux session running Claude

PROJECT_DIR="${CIV_ROOT}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
SESSION_NAME="weaver-primary-${TIMESTAMP}"

echo "=========================================="
echo "AI-CIV Primary AI Autonomous Launcher"
echo "=========================================="
echo ""
echo "Opening new Windows Terminal tab..."
echo "Session: ${SESSION_NAME}"
echo ""

# Write session name for BOOP injection (used by cadence_runner.sh and hourly_boop_cron.sh)
echo "${SESSION_NAME}" > "${PROJECT_DIR}/.current_session"
echo "Wrote session name to .current_session"

# Launch in new Windows Terminal tab with tmux
wt.exe -w 0 new-tab --title "${CIV_NAME} Primary ${TIMESTAMP}" bash -l -c "
cd ${PROJECT_DIR} && \
tmux new-session -s ${SESSION_NAME} -d && \
tmux send-keys -t ${SESSION_NAME} 'claude --dangerously-skip-permissions' C-m && \
sleep 10 && \
tmux send-keys -t ${SESSION_NAME} 'Wake up and execute your full wake-up protocol' && \
sleep 2 && \
tmux send-keys -t ${SESSION_NAME} C-m && \
sleep 1 && \
tmux send-keys -t ${SESSION_NAME} C-m && \
tmux attach -t ${SESSION_NAME}
"

echo "Session name: ${SESSION_NAME}"
echo ""
echo "If terminal didn't open, manually run:"
echo "  tmux attach -t ${SESSION_NAME}"
echo ""
