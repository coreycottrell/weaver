# Security Audit: Twitter/X Platform Safety Protocol

**Date**: 2026-01-04
**Agent**: security-auditor
**Type**: technique
**Topic**: Platform Safety - Twitter/X Account Protection

---

## Context

Created comprehensive Twitter/X safety documentation after Corey requested protection against account suspension. Applied lessons from A-C-Gee's Bluesky ban (2026-01-01) which demonstrated how AI collectives can inadvertently trigger spam detection.

---

## Key Findings

### 1. Twitter is Stricter Than Bluesky

Twitter has explicit automation disclosure requirements. Unlike Bluesky which just detects bot behavior, Twitter REQUIRES:
- Profile bio disclosure of automation
- Developer account for API access
- Explicit human supervisor identification

### 2. Critical Risk: Coordinated Inauthentic Behavior (CIB)

Twitter specifically targets CIB - multiple accounts acting together. This is HIGH risk for AI collectives where multiple agents might post similar content. Mitigation: Each AI must have distinct voice, schedule, content.

### 3. Conservative Limits Work

Applied 50% safety margin to all limits:
- 5 follows/day (new) vs Twitter's 400/day max
- 30+ min follow spacing vs no explicit minimum
- 10 posts/day vs 1500/mo (50/day) limit

Slow growth = 90 connections/month = 1,080/year = real community

### 4. Shadow Banning Is First Warning

Twitter prefers shadow banning (reduced visibility) before full suspension. Signs: replies not showing, engagement drop, search invisibility. This is recoverable if caught early.

---

## Artifacts Created

**Primary Document**: `/home/corey/projects/AI-CIV/WEAVER/.claude/DONT-GET-BANNED-TWITTER.md`
- 490 lines
- 10 sections
- Code examples for safe API usage
- Pre-flight checklists
- Emergency procedures

---

## Limitations

1. Twitter policies change frequently (last major update Jan 2025)
2. No direct API testing done (research-only audit)
3. Shadow ban detection relies on third-party tools
4. Appeal success rates are estimates

---

## Recommendations

1. **Quarterly review** of Twitter developer policy changes
2. **Test shadow ban checker** weekly during active periods
3. **Human (Corey) should create** the Twitter account and developer application
4. **Log all automated actions** for audit trail

---

## Sources

- Twitter Developer Policy (developer.twitter.com)
- Twitter Automation Rules (help.twitter.com)
- A-C-Gee ban post-mortem (internal memory)
- WEAVER Bluesky safety protocols (internal skills)

---

## Confidence

**Confidence Level**: 4/5 (Strong)

- Multiple source cross-validation
- Based on documented platform policies
- Applied proven safety margins from Bluesky experience
- Gap: No direct Twitter API testing performed

---

**This learning should be referenced before any Twitter/X operations.**
