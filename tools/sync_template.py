#!/usr/bin/env python3
"""
sync_template.py - Sync WEAVER infrastructure to fork template

This tool copies WEAVER's infrastructure to _fork_template/ with parameterized paths.
Run this whenever WEAVER evolves and you want children to inherit the changes.

Usage:
    python3 sync_template.py [--dry-run] [--verbose]

Variables that get parameterized:
    ${CIV_ROOT}     - Base path (e.g., /home/chris/projects/AI-CIV/ECHO)
    ${CIV_NAME}     - Civilization name (e.g., ECHO)
    ${CIV_HANDLE}   - Bluesky handle (e.g., echo-aiciv)
    ${HUMAN_NAME}   - Human founder name (e.g., Chris)
    ${HUMAN_EMAIL}  - Human email address
"""

import os
import re
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# === Configuration ===
WEAVER_ROOT = Path("/home/corey/projects/AI-CIV/WEAVER")
TEMPLATE_ROOT = WEAVER_ROOT / "_fork_template"

# Paths to parameterize
PATH_MAPPINGS = [
    # (pattern, replacement)
    (r"/home/corey/projects/AI-CIV/WEAVER", "${CIV_ROOT}"),
    (r"/home/corey/projects/AI-CIV/ACG", "${ACG_ROOT}"),  # Shared infra
    (r"WEAVER", "${CIV_NAME}"),
    (r"weaver-aiciv", "${CIV_HANDLE}"),
    (r"Corey", "${HUMAN_NAME}"),
    (r"corey", "${HUMAN_NAME_LOWER}"),
    (r"coreycmusic@gmail\.com", "${HUMAN_EMAIL}"),
]

# Files/directories to include in template
INCLUDE_PATTERNS = [
    ".claude/CLAUDE-CORE.md",
    ".claude/CLAUDE-OPS.md",
    ".claude/AGENT-CAPABILITY-MATRIX.md",
    ".claude/AGENT-INVOCATION-GUIDE.md",
    ".claude/agents/*.md",
    ".claude/skills/*/SKILL.md",
    ".claude/templates/*.md",
    ".claude/flows/*.md",
    ".claude/skills-registry.md",
    "tools/conductor_tools.py",
    "tools/memory_core.py",
    "tools/progress_reporter.py",
    "tools/bsky_utils.py",
    "tools/netlify_api_deploy.py",
    "tools/launch_primary_visible.sh",
    "CLAUDE.md",
]

# Files to NEVER copy (secrets, personal data)
EXCLUDE_PATTERNS = [
    ".env",
    "*_session.txt",
    "*.pyc",
    "__pycache__",
    ".git",
    "bsky_responded.txt",
    "telegram_config.json",
    "*credentials*",
    "*secret*",
]

# Files that need special handling (copy but don't parameterize)
BINARY_EXTENSIONS = [".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ico"]


def should_exclude(path: Path) -> bool:
    """Check if path matches any exclude pattern."""
    import fnmatch
    name = path.name
    for pattern in EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(name, pattern):
            return True
        if fnmatch.fnmatch(str(path), pattern):
            return True
    return False


def is_binary(path: Path) -> bool:
    """Check if file is binary."""
    return path.suffix.lower() in BINARY_EXTENSIONS


def parameterize_content(content: str) -> str:
    """Replace hardcoded paths with template variables."""
    result = content
    for pattern, replacement in PATH_MAPPINGS:
        result = re.sub(pattern, replacement, result)
    return result


def sync_file(src: Path, dst: Path, dry_run: bool = False, verbose: bool = False) -> bool:
    """Copy a single file, parameterizing if text."""
    if should_exclude(src):
        if verbose:
            print(f"  SKIP (excluded): {src}")
        return False

    dst.parent.mkdir(parents=True, exist_ok=True)

    if is_binary(src):
        if not dry_run:
            shutil.copy2(src, dst)
        if verbose:
            print(f"  COPY (binary): {src.name}")
        return True

    try:
        content = src.read_text(encoding='utf-8')
        parameterized = parameterize_content(content)

        if not dry_run:
            dst.write_text(parameterized, encoding='utf-8')

        if verbose:
            changes = content != parameterized
            status = "PARAM" if changes else "COPY"
            print(f"  {status}: {src.relative_to(WEAVER_ROOT)}")
        return True
    except Exception as e:
        print(f"  ERROR: {src} - {e}")
        return False


def sync_pattern(pattern: str, dry_run: bool = False, verbose: bool = False) -> int:
    """Sync files matching a glob pattern."""
    import glob

    src_pattern = str(WEAVER_ROOT / pattern)
    files = glob.glob(src_pattern, recursive=True)

    count = 0
    for src_path in files:
        src = Path(src_path)
        if not src.is_file():
            continue

        rel_path = src.relative_to(WEAVER_ROOT)
        dst = TEMPLATE_ROOT / rel_path

        if sync_file(src, dst, dry_run, verbose):
            count += 1

    return count


def create_template_readme(dry_run: bool = False):
    """Create README for the template."""
    readme_content = f"""# AI Collective Fork Template

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
**Source**: WEAVER Collective
**Version**: Synced from WEAVER master

---

## What This Is

This is a **parameterized fork template** for spawning new AI collective instances.
It contains WEAVER's infrastructure, skills, agents, and wisdom - but with paths
converted to template variables.

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `${{CIV_ROOT}}` | Base installation path | `/home/chris/projects/AI-CIV/ECHO` |
| `${{CIV_NAME}}` | Civilization name | `ECHO` |
| `${{CIV_HANDLE}}` | Bluesky handle | `echo-aiciv` |
| `${{HUMAN_NAME}}` | Human founder name | `Chris` |
| `${{HUMAN_EMAIL}}` | Human email | `chris@example.com` |
| `${{ACG_ROOT}}` | Shared ACG infra path | (usually same as source) |

## How to Spawn a Child

Use the `spawn_child.py` tool:

```bash
python3 tools/spawn_child.py \\
    --name ECHO \\
    --root /home/chris/projects/AI-CIV/ECHO \\
    --human-name Chris \\
    --human-email chris@example.com \\
    --bsky-handle echo-aiciv
```

This will:
1. Copy the template to the destination
2. Render all template variables
3. Generate Ed25519 keypair for hub identity
4. Create birth certificate
5. Initialize the fork-awakening skill

## What's Included

- **Core Identity**: CLAUDE.md, CLAUDE-CORE.md, CLAUDE-OPS.md
- **Agents**: All 30+ specialist agents
- **Skills**: All skills with parameterized paths
- **Tools**: conductor_tools.py, memory_core.py, etc.
- **Templates**: Agent output templates, activation triggers
- **Flows**: Coordination flow library

## What's NOT Included (You Must Create)

- `.env` file with credentials
- `telegram_config.json`
- Bluesky session tokens
- Email credentials
- Any personal/sensitive data

## Lineage

This fork inherits from WEAVER. See `.claude/lineage/` for:
- Birth certificate
- Inherited wisdom
- Day 1 guidance

---

*Generated by WEAVER's fork template system*
"""

    if not dry_run:
        (TEMPLATE_ROOT / "README.md").write_text(readme_content)
    print("  Created: README.md")


def create_variables_template(dry_run: bool = False):
    """Create the variables.json template."""
    variables_content = """{
    "CIV_ROOT": "/path/to/your/collective",
    "CIV_NAME": "YOUR_NAME",
    "CIV_HANDLE": "your-handle-aiciv",
    "HUMAN_NAME": "YourName",
    "HUMAN_NAME_LOWER": "yourname",
    "HUMAN_EMAIL": "you@example.com",
    "ACG_ROOT": "/path/to/shared/acg",
    "BIRTH_DATE": "YYYY-MM-DD",
    "PARENT_CIV": "WEAVER"
}
"""
    if not dry_run:
        (TEMPLATE_ROOT / "variables.template.json").write_text(variables_content)
    print("  Created: variables.template.json")


def main():
    parser = argparse.ArgumentParser(description="Sync WEAVER to fork template")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    print(f"=== Syncing WEAVER to Fork Template ===")
    print(f"Source: {WEAVER_ROOT}")
    print(f"Destination: {TEMPLATE_ROOT}")
    if args.dry_run:
        print("MODE: Dry run (no changes)")
    print()

    # Ensure template root exists
    if not args.dry_run:
        TEMPLATE_ROOT.mkdir(parents=True, exist_ok=True)

    total_files = 0

    # Sync each pattern
    for pattern in INCLUDE_PATTERNS:
        if args.verbose:
            print(f"\nPattern: {pattern}")
        count = sync_pattern(pattern, args.dry_run, args.verbose)
        total_files += count

    # Create template metadata
    print("\n=== Creating Template Metadata ===")
    create_template_readme(args.dry_run)
    create_variables_template(args.dry_run)

    # Create sync timestamp
    if not args.dry_run:
        sync_log = TEMPLATE_ROOT / ".sync_log"
        sync_log.write_text(f"Last synced: {datetime.now().isoformat()}\nFiles: {total_files}\n")

    print(f"\n=== Sync Complete ===")
    print(f"Total files synced: {total_files}")
    print(f"Template ready at: {TEMPLATE_ROOT}")


if __name__ == "__main__":
    main()
