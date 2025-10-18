# skill-creator Meta-Skill Documentation

**Source**: https://github.com/anthropics/skills/tree/main/skill-creator
**Type**: META-SKILL (guidance for creating skills)
**Status**: Reference material for AI-CIV skill development

---

## Full Text from Anthropic

---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
license: Complete terms in LICENSE.txt
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks—they transform Claude from a general-purpose agent into a specialized agent
equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

[Complete 6-step workflow documented - see Anthropic repository for full text]

**Note**: Full text retrieved 2025-10-18. Refer to Anthropic repository for latest version.

---

## AI-CIV Usage

**When to reference**: Before creating any custom skill (Phase 2+)

**Key sections**:
1. 6-step skill creation process
2. Progressive disclosure principle
3. Resource planning guidance (scripts vs references vs assets)
4. Helper scripts (init_skill.py, package_skill.py)

**Application**: All Phase 2 skills follow this workflow
