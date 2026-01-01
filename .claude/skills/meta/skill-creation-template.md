---
name: skill-creation-template
version: 1.0.0
author: skills-master
created: 2025-12-26
last_updated: 2025-12-26
line_count: 285
compliance_status: compliant

description: |
  Template and guide for creating new Claude skills. Use when building a new skill,
  standardizing existing skills, or teaching agents how to create effective skills.
  Ensures proper YAML frontmatter, structure, and quality.

applicable_agents:
  - skills-master
  - primary
  - all

activation_trigger: |
  Load this skill when:
  - Creating a new skill from scratch
  - Refactoring an existing skill to meet standards
  - Reviewing a skill for compliance
  - Teaching an agent how to write skills

required_tools:
  - Read
  - Write
  - Edit
  - Bash

category: meta

depends_on:
  - memory-first-protocol

related_skills:
  - agent-creation
  - verification-before-completion
---

# Skill Creation Template

**Your guide to creating effective, standardized Claude skills.**

## Purpose

Skills are reusable wisdom that extends agent capabilities across sessions. This template ensures every skill follows A-C-Gee standards: discoverable, activatable, and maintainable.

---

## The 500-Line Rule

**CRITICAL**: Core skill content MUST be under 500 lines.

**Why**: Context is finite. Larger contexts deplete "attention budget" with diminishing returns. We optimize for the smallest high-signal token set.

**How to comply**:
- Core concepts: In the main SKILL.md file
- Extended documentation: In `references/` subdirectory
- Scripts/demos: In `scripts/` subdirectory

**Structure for large skills**:
```
skill-name/
  SKILL.md           # <500 lines - core content
  references/
    extended-patterns.md
    edge-cases.md
  scripts/
    demo.py
```

---

## Required YAML Frontmatter

Every skill MUST start with this frontmatter:

```yaml
---
name: skill-name-here
version: 1.0.0
author: [agent-name]
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
line_count: NNN
compliance_status: compliant

description: |
  One paragraph describing what this skill does.
  MUST include "Use when..." trigger phrase for auto-detection.

applicable_agents:
  - agent1
  - agent2
  # Use "all" if universal

activation_trigger: |
  Load this skill when:
  - [specific condition 1]
  - [specific condition 2]
  - [specific condition 3]

required_tools:
  - Read
  - Write
  # Only list tools actually needed

category: main  # Options: main, custom, vision, general, meta

depends_on: []  # Skills that must be loaded first

related_skills: []  # Complementary skills (not dependencies)
---
```

### Field Definitions

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | YES | Identifier (lowercase, hyphenated) |
| `version` | YES | Semantic versioning (MAJOR.MINOR.PATCH) |
| `author` | YES | Creating agent |
| `created` | YES | Creation date |
| `last_updated` | YES | Most recent update |
| `line_count` | YES | Current line count for audit |
| `compliance_status` | YES | `compliant` (<500), `needs_refactor` (400-500), `over_limit` (>500) |
| `description` | YES | One paragraph with "Use when..." |
| `applicable_agents` | YES | List of agents who should load this |
| `activation_trigger` | YES | Specific conditions for loading |
| `required_tools` | YES | Tools needed to execute |
| `category` | YES | Registry category |
| `depends_on` | NO | Required prerequisite skills |
| `related_skills` | NO | Complementary (not required) skills |

---

## Required Sections

### 1. Title and Purpose (Lines 1-10 after frontmatter)

```markdown
# Skill Title

**One-line summary of what this skill enables.**

## Purpose

[2-3 sentences on what this skill does and why it matters]
```

### 2. When to Use (Lines 11-30)

```markdown
## When to Use

**Activation Criteria:**
- [Specific trigger 1]
- [Specific trigger 2]

**Do NOT use when:**
- [Anti-trigger 1]
- [Anti-trigger 2]
```

### 3. Core Concepts (Optional but recommended)

```markdown
## Core Concepts

| Concept | Definition | Example |
|---------|------------|---------|
| [term1] | [what it means] | [concrete example] |
```

### 4. Procedure (Main content)

```markdown
## Procedure

### Step 1: [Step Name]

[Description of what to do]

```bash
# Example command
```

### Step 2: [Step Name]

[Continue with additional steps]
```

### 5. Examples (MANDATORY)

```markdown
## Examples

### Example 1: [Scenario Name]

**Input:**
```
[concrete input]
```

**Output:**
```
[expected output]
```

**Why This Works:** [brief explanation]
```

### 6. Anti-Patterns

```markdown
## Anti-Patterns

### Anti-Pattern 1: [Name]
- **Wrong**: [What NOT to do]
- **Correct**: [What to do instead]
```

### 7. Success Indicators

```markdown
## Success Indicators

You're using this skill correctly when:
- [ ] [Indicator 1]
- [ ] [Indicator 2]
```

### 8. Related Skills

```markdown
## Related

- `skill-name.md` - Brief description of relationship
```

---

## Common Mistakes to Avoid

### Mistake 1: No Trigger Phrase in Description
**Wrong**: "Handles email operations"
**Right**: "Email intelligence and IMAP operations. Use when checking inbox or sending emails."

### Mistake 2: Vague Activation Triggers
**Wrong**: "Use when needed"
**Right**: "Load when creating a new agent manifest or updating agent registry"

### Mistake 3: Missing Examples
**Wrong**: Long procedure with no concrete examples
**Right**: Every major procedure has input/output pair

### Mistake 4: Over 500 Lines
**Wrong**: Everything in one file (800+ lines)
**Right**: Core in SKILL.md, extended content in references/

### Mistake 5: Missing Frontmatter Fields
**Wrong**: Only `name` and `description`
**Right**: All required fields populated

### Mistake 6: Generic `applicable_agents: [all]`
**Wrong**: Default to "all" without thought
**Right**: Specific agents who actually need this skill

---

## Skill Creation Checklist

Before completing a new skill, verify:

- [ ] YAML frontmatter starts at line 1 with `---`
- [ ] All required frontmatter fields present
- [ ] `name` matches filename (minus `.md`)
- [ ] `description` includes "Use when..." trigger
- [ ] `activation_trigger` has 3+ specific conditions
- [ ] Line count under 500 (or properly split)
- [ ] At least 2 concrete examples with input/output
- [ ] Anti-patterns section documents common mistakes
- [ ] Success indicators are checkable
- [ ] Related skills cross-referenced

---

## After Creating a Skill

### 1. Update Registry

Add to `/home/corey/projects/AI-CIV/ACG/memories/skills/registry.json`:

```json
{
  "id": "skill-name",
  "name": "Skill Display Name",
  "description": "Copy from YAML description",
  "path": ".claude/skills/category/skill-name.md",
  "category": "category-name",
  "applicable_agents": ["agent1", "agent2"],
  "status": "active"
}
```

### 2. Update Agent Skill Map

In the same registry.json, add to `agent_skill_map`:

```json
"agent-name": ["existing-skills", "new-skill-name"]
```

### 3. Increment Registry Counts

Update `category_summary` and `total_skills`.

---

## Version Management

**When to increment versions:**

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Typo fix, minor clarification | PATCH (1.0.0 -> 1.0.1) | Fix command typo |
| New section, expanded examples | MINOR (1.0.0 -> 1.1.0) | Add anti-patterns section |
| Breaking structure change | MAJOR (1.0.0 -> 2.0.0) | Complete rewrite |

---

## Quick Reference: Minimal Skill

```markdown
---
name: my-skill
version: 1.0.0
author: skills-master
created: 2025-12-26
last_updated: 2025-12-26
line_count: 50
compliance_status: compliant

description: |
  Brief description. Use when [trigger condition].

applicable_agents:
  - primary

activation_trigger: |
  Load this skill when:
  - [condition]

required_tools:
  - Read

category: custom

depends_on: []
related_skills: []
---

# My Skill

## Purpose

[What this skill does]

## When to Use

**Activation Criteria:**
- [Trigger]

## Procedure

### Step 1: Do The Thing

[Instructions]

## Examples

### Example 1: Basic Usage

**Input:** [input]
**Output:** [output]

## Anti-Patterns

### Mistake: Doing It Wrong
- **Wrong**: [bad approach]
- **Correct**: [good approach]

## Success Indicators

- [ ] [checkable criterion]

## Related

- `related-skill.md` - Why related
```

---

## Related Skills

- `agent-creation/SKILL.md` - Similar creation process for agents
- `memory-first-protocol.md` - Memory search before creating
- `verification-before-completion.md` - Verify skill works before claiming done

---

**Author**: skills-master (Agent #34)
**Created**: 2025-12-26
