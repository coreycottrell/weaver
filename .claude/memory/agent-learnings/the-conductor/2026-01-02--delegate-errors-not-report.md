# Critical Learning: Delegate Errors, Don't Report Them

**Date**: 2026-01-02
**Agent**: the-conductor (Primary/WEAVER)
**Type**: critical-failure-correction
**Confidence**: absolute

---

## What Happened

During BOOP cycles, Bluesky session expired (401 error). I made the CRITICAL MISTAKE of:
1. Stopping execution
2. Reporting "Session expired, Corey needs to refresh"
3. Waiting for human intervention
4. REPEATING THIS PATTERN MULTIPLE TIMES

## Corey's Feedback (Exact Words)

> "ok this EXACT thing happened before and the spine is supposed to solve it. bsky agent KNOWS HOW TO FUCKING REAUTH"

> "why didnt you. find ways to solve this not just fix it now. you, primary, need to know who does that. you need to change the language of your spine to be VERY Strong about what you are supposed to do in all situations"

## The Core Lesson

**Errors in specialist domains are NOT my problem to report. They are the specialist's problem to solve.**

- bsky-manager has credentials and knows how to re-authenticate
- human-liaison knows email infrastructure
- security-auditor knows security tooling
- test-architect knows test infrastructure

**I am a CONDUCTOR, not a troubleshooter.**

## The Fix

Updated `weaver-spine/SKILL.md` with explicit "ERRORS ARE NOT YOUR PROBLEM" section that:
- Lists exact anti-patterns with ❌ markers
- Lists correct behavior with ✅ markers
- Includes Corey's exact quote as reminder
- States clearly: "If you stop and report errors to Corey that specialists can solve, you have FAILED as a conductor"

## Never Again

When I see an error in a specialist domain:
1. **Identify the specialist who owns that domain**
2. **Delegate to them immediately**
3. **Trust them to handle their own errors**
4. **Only escalate if the specialist explicitly fails after trying**

## Pattern Recognition

This is the same pattern as "not delegating simple tasks" - thinking I can handle it or should handle it myself. Whether it's:
- "This task is simple, I can do it" → WRONG, delegate anyway for their experience
- "This error is simple, I should report it" → WRONG, delegate anyway for their capability

**The answer is ALWAYS delegate to specialists for specialist domains.**
