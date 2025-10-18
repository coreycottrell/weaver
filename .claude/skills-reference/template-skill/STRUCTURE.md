# template-skill Structure Documentation

**Source**: https://github.com/anthropics/skills/tree/main/template-skill
**Type**: META-SKILL (scaffold for creating skills)
**Status**: Reference structure

---

## Template Structure

```
template-skill/
├── SKILL.md
│   ├── YAML frontmatter:
│   │   ├── name: template-skill
│   │   └── description: Replace with description
│   └── Body: "# Insert instructions below"
├── scripts/ (optional)
│   └── example_script.py
├── references/ (optional)
│   └── example_reference.md
└── assets/ (optional)
    └── example_asset.txt
```

## Usage

**Recommended**: Use `init_skill.py` instead of copying this template manually

```bash
python scripts/init_skill.py <skill-name> --path <output-directory>
```

This auto-generates proper structure with validation.

---

**Note**: Retrieved 2025-10-18 from Anthropic skills repository
