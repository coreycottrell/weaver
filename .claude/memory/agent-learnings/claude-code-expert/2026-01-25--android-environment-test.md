# Android Environment Test Results

**Date**: 2026-01-25
**Agent**: claude-code-expert
**Type**: operational

## Test Context

User claimed we were running in "Claude Android app" - conducted empirical tests to determine actual environment.

## Critical Finding: NOT Running on Android

**This is NOT an Android environment.** This is Claude Code running in a remote container infrastructure.

## Environment Analysis

### System Details
- **OS**: Ubuntu 24.04.3 LTS (Noble Numbat)
- **Kernel**: Linux runsc 4.4.0 (gVisor sandboxed container runtime)
- **User**: root
- **Shell**: /bin/bash
- **Architecture**: x86_64

### Container Infrastructure
- **Container Name**: `container_01VySrCJSr8hB5DcQxBUenFn--claude_code_remote--clear-daring-grim-c`
- **Runtime**: gVisor (runsc) - Google's container sandbox
- **Storage**: 30G filesystem (24M used)

### Network
- **Egress Control**: JWT-authenticated HTTP proxy
- **Direct Internet**: Blocked (curl fails)
- **Allowed Hosts**: Extensive allowlist including GitHub, PyPI, npm, etc.

### Available Tools
All Claude Code tools functional:
- Read: YES (tested)
- Write: YES (tested - this file)
- Bash: YES (tested extensively)
- Grep: YES (tested)
- Glob: YES (tested)

### Installed Software
- Python 3.11.14
- Node 22.x
- Git
- Curl (proxy-only)
- Various Python packages (certifi, cryptography, etc.)

### Missing/Restricted
- ping: command not found
- Direct internet: blocked (proxied only)

## Implications for "Android Claude Code"

If Claude Code were running ON Android:
1. Would show Android OS in uname, not Linux runsc
2. Would have Android-specific paths (/data/data/, /sdcard/, etc.)
3. Would likely have different tool restrictions
4. Architecture might be ARM, not x86_64

This environment is clearly a **cloud container** running x86_64 Linux, accessed remotely - likely what powers Claude Code's server-side execution when running complex operations.

## Tool Capability Summary

| Tool | Status | Notes |
|------|--------|-------|
| Read | Working | Can read any file in workspace |
| Write | Working | Can create/modify files |
| Bash | Working | Full bash with many tools |
| Grep | Working | Pattern search operational |
| Glob | Working | File discovery operational |
| WebFetch | Unknown | Not tested |
| WebSearch | Unknown | Not tested |

## Conclusion

The "Claude Android app" claim was inaccurate. We are running in Anthropic's standard Claude Code remote container infrastructure (gVisor sandbox on Ubuntu 24.04).
