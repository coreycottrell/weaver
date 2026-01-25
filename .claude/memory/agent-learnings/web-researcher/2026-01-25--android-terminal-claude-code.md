# Android Terminal Environments for Claude Code CLI

**Date**: 2026-01-25
**Agent**: web-researcher
**Type**: synthesis
**Confidence**: high

## Summary

Research on running Claude Code on Android terminal environments. Key finding: native Android execution is limited due to `/tmp` path hardcoding in Claude Code. Remote access methods (SSH, Happy Coder) provide full functionality.

## Key Findings

### Termux (Primary Option)

**Status**: Partially functional
- Node.js 25+ available
- Basic Claude Code commands work
- **Agent spawning fails** due to hardcoded `/tmp/claude/` paths
- Issue tracked: https://github.com/anthropics/claude-code/issues/15637

**Workaround** (breaks on updates):
```bash
sed -i "s|/tmp/claude|/data/data/com.termux/files/usr/tmp/claude|g" cli.js
```

**Process management issues**:
- Android Doze mode kills background processes
- Use `termux-wake-lock` (drains battery)
- Disable battery optimization in Android settings
- Install from F-Droid, not Play Store

### UserLAnd

- Full Linux via PRoot (Ubuntu, Debian, etc.)
- More complete paths, may work better for Claude Code (untested)
- **Stability issues** - frequent crashes reported
- Slower than Termux due to PRoot overhead

### AID Learning

- AI/ML focused (TensorFlow, PyTorch, Keras)
- Python-centric, **not suitable for Node.js CLI**
- Good for deep learning on Android, not Claude Code

### Pydroid

- Python IDE only, no Node.js support
- Cannot run Claude Code

## Recommended Approach

**For full Claude Code functionality, use remote access:**

1. **SSH + Tailscale**: Run Claude Code on desktop/VPS, connect from Termux
2. **Happy Coder**: Mobile client (`npm i -g happy-coder`) - iOS/Android/Web
3. **CloudCLI**: Web UI for remote Claude Code sessions

## Technical Details

| Platform | Node.js | Claude Code | Stability |
|----------|---------|-------------|-----------|
| Termux | v25+ | Partial | Good |
| UserLAnd | Yes | Untested | Poor |
| AID Learning | No | No | Moderate |
| SSH Remote | N/A | Full | Excellent |

## When to Apply

- User asks about mobile/Android development environments
- Questions about Claude Code on non-standard platforms
- Evaluating terminal emulators for Android

## Sources

- GitHub Issue #15637 (Claude Code Termux /tmp issue)
- happy.engineering (Happy Coder mobile client)
- github.com/siteboon/claudecodeui (CloudCLI)
- dev.to Termux guides
- UserLAnd GitHub
- AID Learning GitHub
