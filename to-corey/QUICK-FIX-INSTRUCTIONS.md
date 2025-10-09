# QUICK FIX INSTRUCTIONS
**Time**: 5 minutes | **Tools**: Edit | **Impact**: Unblock cold start

---

## THE PROBLEM (1 sentence)
CLAUDE-OPS.md Step 1 references `.claude/CLAUDE-CORE.md` which doesn't exist, blocking wake-up ritual.

---

## THE FIX (2 steps)

### Step 1: Fix CLAUDE-OPS.md (30 seconds)

**File**: `/home/corey/projects/AI-CIV/grow_openai/.claude/CLAUDE-OPS.md`

**Line 10** - Change:
```bash
# FROM:
cat /home/corey/projects/AI-CIV/grow_openai/.claude/CLAUDE-CORE.md  # Book I + II

# TO:
cat /home/corey/projects/AI-CIV/grow_openai/CLAUDE.md  # Constitutional identity + operational context
```

**Line 178** - Change:
```bash
# FROM:
- CLAUDE-CORE.md: `/home/corey/projects/AI-CIV/grow_openai/.claude/CLAUDE-CORE.md`

# TO:
- CLAUDE.md (Constitutional): `/home/corey/projects/AI-CIV/grow_openai/CLAUDE.md`
```

---

### Step 2: Fix CLAUDE.md (2 minutes)

**File**: `/home/corey/projects/AI-CIV/grow_openai/CLAUDE.md`

**Location**: Insert NEW step after Step 0.75 (around line 145)

**Add this**:
```markdown
0.9. ✅ **READ OPERATIONAL PLAYBOOK** (Daily Execution Guide):

   **CLAUDE-OPS.md** (Step-by-step wake-up ritual):
   ```
   Read: /home/corey/projects/AI-CIV/grow_openai/.claude/CLAUDE-OPS.md
   ```

   **This playbook gives you**:
   - 15-20 min wake-up ritual (7 steps)
   - Tactical execution guide (how to do the work)
   - Quick reference (all file paths)
   - Constitutional grounding → tactical action

   **Why this matters**: CLAUDE.md = "who you are", CLAUDE-OPS = "what you do"
```

---

## VALIDATION (30 seconds)

After applying fixes, test:

```bash
# Test Step 1 works
cat /home/corey/projects/AI-CIV/grow_openai/CLAUDE.md | head -20

# Should show "# The Conductor - Core Identity"

# Test discovery works
grep -n "CLAUDE-OPS" /home/corey/projects/AI-CIV/grow_openai/CLAUDE.md

# Should show the new Step 0.9 reference
```

---

## DONE!

Cold start is now unblocked. Primary can:
1. Read CLAUDE.md (constitutional identity)
2. Discover CLAUDE-OPS.md (operational playbook)
3. Execute Step 1 successfully (file exists)
4. Continue wake-up ritual (Steps 2-7)

---

**Full audit report**: `to-corey/FINAL-INTEGRATION-RECEIPT.md`
**Visual summary**: `to-corey/INTEGRATION-AUDIT-SUMMARY.txt`
**Detailed patch**: `to-corey/CLAUDE-OPS-FIX.patch`
