# Claude Code Android Viability Technical Analysis

**Date**: 2026-01-25
**Agent**: claude-code-expert
**Type**: synthesis
**Topic**: Android/Termux platform compatibility assessment

---

## Summary

Android is NOT officially supported by Claude Code. Partial functionality via Termux exists with significant limitations.

## Official Requirements (Android NOT included)

- macOS 13.0+
- Ubuntu 20.04+/Debian 10+
- Windows 10+ (WSL)
- Node.js >= 18.0.0
- 4GB+ RAM
- Bash or Zsh shell

## Key Technical Blockers

### 1. Hardcoded /tmp/claude Paths (Issue #15637 - OPEN)

The bundled cli.js contains hardcoded `/tmp/claude` references:
- Sandbox TMPDIR
- Screenshot paths
- Working directory tracking
- Agent task spawning directories

**Android impact**: Permission denied errors. Termux uses `$TMPDIR` at `/data/data/com.termux/files/usr/tmp`.

**Current state (v2.1.11+)**:
- Direct Bash commands: WORK
- Agent spawning: BROKEN
- Task tool delegation: BROKEN

### 2. Custom Slash Commands (Issue #9435)

Commands in `.claude/commands/` not discovered on Termux despite working on standard Linux.

### 3. Ripgrep Page Size Mismatch (Issue #9462)

Bundled ripgrep compiled for 4KB pages fails on 16KB page ARM64 systems.

**Workaround**: Link system ripgrep instead of bundled.

### 4. No Android-specific Binaries

- ripgrep: arm64-linux present (may work with caveats)
- Sharp image library: No Android variant

## What Works on Termux

| Feature | Status |
|---------|--------|
| npm installation | Works |
| Basic commands | Works |
| Direct Bash execution | Works |
| API calls | Works |
| Agent spawning | BROKEN |
| Background tasks | BROKEN |
| Slash commands | BROKEN |
| Image processing | BROKEN |
| Subagent delegation | BROKEN |

## Viable Approaches

1. **Remote access** (recommended): SSH + Tailscale to desktop running Claude Code
2. **Claude Android UI**: Web interface to remote sessions
3. **Native Termux** (limited): Basic operations only, no agent features
4. **Manual patching**: sed replace /tmp/claude (fragile, breaks on updates)

## What Would Enable Full Support

1. Replace `/tmp/claude` with `os.tmpdir()` or respect `$TMPDIR`
2. Add Android-specific ripgrep or system fallback
3. Fix path resolution for command discovery
4. Test agent spawning in restricted environments
5. Build Sharp for Android or make optional

## Sources

- [Claude Code Setup Docs](https://code.claude.com/docs/en/setup)
- [GitHub Issue #15637 - /tmp/claude paths](https://github.com/anthropics/claude-code/issues/15637)
- [GitHub Issue #9435 - Slash commands on Termux](https://github.com/anthropics/claude-code/issues/9435)
- [GitHub Issue #9462 - Ripgrep page size](https://github.com/anthropics/claude-code/issues/9462)
- [Claude Android UI](https://github.com/larsmartens/claude-android-ui)

---

**Tags**: android, termux, platform-support, mobile, arm64, limitations
**Confidence**: high (verified via documentation and GitHub issues)
