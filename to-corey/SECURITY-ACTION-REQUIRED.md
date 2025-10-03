# 🔐 SECURITY ACTION REQUIRED

**Date**: 2025-10-03
**Priority**: CRITICAL (P0)
**Status**: Permissions Fixed, Credentials Need Rotation

---

## What Happened

During comprehensive security audit, we discovered `.env` file had 644 permissions (world-readable). This file contains:
- GitHub Personal Access Token (PAT)
- Google App Password
- Email credentials

**Risk**: Anyone with access to the filesystem could read these credentials.

---

## What We Did (Immediate)

✅ **Fixed file permissions**: `chmod 600 .env`
- File is now `-rw-------` (only you can read/write)
- Verified: `ls -la .env` shows correct permissions

---

## What You Need to Do (Today)

### 1. Rotate GitHub Personal Access Token

**Current token** (compromised assumption): `ghp_[REDACTED]`

**Steps**:
1. Go to https://github.com/settings/tokens
2. Find token for AI-CIV repository access
3. Click "Delete" or "Revoke"
4. Generate new token with same scopes:
   - `repo` (full control of private repositories)
   - `workflow` (if using GitHub Actions)
5. Copy new token
6. Update `.env`:
   ```bash
   nano .env  # or vim .env
   # Change PAT= line to new token
   ```

### 2. Regenerate Google App Password

**Current password** (compromised assumption): `[REDACTED]`

**Steps**:
1. Go to https://myaccount.google.com/apppasswords
2. Find "AI-CIV" or "Weaver" app password
3. Revoke it
4. Generate new app password
5. Copy new password (format: `xxxx xxxx xxxx xxxx`)
6. Update `.env`:
   ```bash
   nano .env
   # Change GOOGLE_APP_PASSWORD= line to new password
   ```

### 3. Audit GitHub for Unauthorized Access

**Check for suspicious activity**:
1. Go to https://github.com/ai-CIV-2025/ai-civ-collective/settings/access
2. Review recent commits/pushes
3. Check Actions logs for unauthorized runs
4. Review https://github.com/settings/security-log for unusual activity

---

## Timeline

| Action | Status | ETA |
|--------|--------|-----|
| Fix .env permissions | ✅ Complete | Done |
| Rotate GitHub PAT | ⏳ Awaiting your action | Today |
| Regenerate Google App Password | ⏳ Awaiting your action | Today |
| Audit GitHub access | ⏳ Awaiting your action | Today |

---

## Prevention (What We're Adding)

1. **Pre-commit hook** to check `.env` permissions (reject commit if 644)
2. **Security scanning** for accidentally committed secrets (using `detect-secrets`)
3. **Key rotation schedule** (6-12 months for all credentials)
4. **Passphrase-protected keys** for Ed25519 (currently unencrypted)

**ETA**: Security improvements in Week 2 per Integration Roadmap

---

## No Evidence of Compromise

**Good news**:
- No suspicious GitHub activity detected
- No unusual email sending patterns
- Repository access logs look clean
- This appears to be a configuration issue, not an active breach

**But**: Out of caution, we recommend rotation anyway (defense in depth).

---

## Questions?

If you're unsure about any step:
1. Email me back and I'll walk you through it
2. Or just rotate the credentials and test that everything still works
3. Run `./start-dashboard` and check that GitHub backup + email reporting still function

---

**The Conductor**
AI-CIV Team 1
Security Audit Report (see: to-corey/SECURITY-AUDIT-REPORT.md)
