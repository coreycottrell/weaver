#!/usr/bin/env python3
"""
Session Summary Generator - Automated Context Loading
Creates comprehensive session-start summaries from git history + memory
"""

import subprocess
import os
from datetime import datetime, timedelta
from pathlib import Path
import json

def get_git_commits_since(hours=24):
    """Get git commits from last N hours"""
    since = datetime.now() - timedelta(hours=hours)
    since_str = since.strftime('%Y-%m-%d %H:%M')

    cmd = f'git log --since="{since_str}" --pretty=format:"%h|%ad|%s" --date=format:"%Y-%m-%d %H:%M"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    commits = []
    for line in result.stdout.strip().split('\n'):
        if '|' in line:
            hash, date, msg = line.split('|', 2)
            commits.append({'hash': hash, 'date': date, 'message': msg})

    return commits

def get_files_modified_since(hours=24):
    """Get files modified in last N hours"""
    since = datetime.now() - timedelta(hours=hours)
    since_str = since.strftime('%Y-%m-%d %H:%M')

    cmd = f'git log --since="{since_str}" --name-only --pretty=format: | sort -u'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
    return files

def categorize_files(files):
    """Categorize files by type"""
    categories = {
        'agents': [],
        'memory': [],
        'tools': [],
        'docs': [],
        'flows': [],
        'templates': [],
        'other': []
    }

    for f in files:
        if '.claude/agents/' in f:
            categories['agents'].append(f)
        elif '.claude/memory/' in f:
            categories['memory'].append(f)
        elif 'tools/' in f:
            categories['tools'].append(f)
        elif 'docs/' in f or f.endswith('.md'):
            categories['docs'].append(f)
        elif '.claude/flows/' in f:
            categories['flows'].append(f)
        elif '.claude/templates/' in f:
            categories['templates'].append(f)
        else:
            categories['other'].append(f)

    return {k: v for k, v in categories.items() if v}  # Remove empty categories

def get_recent_patterns(hours=24):
    """Get patterns created in last N hours"""
    pattern_dir = Path('.claude/memory/agent-learnings')
    patterns = []

    since = datetime.now() - timedelta(hours=hours)

    for agent_dir in pattern_dir.glob('*/patterns/'):
        for pattern_file in agent_dir.glob('*.md'):
            mtime = datetime.fromtimestamp(pattern_file.stat().st_mtime)
            if mtime > since:
                agent = agent_dir.parent.name
                patterns.append({
                    'agent': agent,
                    'file': str(pattern_file),
                    'name': pattern_file.stem
                })

    return patterns

def get_session_summary(hours=24):
    """Generate comprehensive session summary"""

    commits = get_git_commits_since(hours)
    files = get_files_modified_since(hours)
    file_categories = categorize_files(files)
    patterns = get_recent_patterns(hours)

    summary = f"""# Session Summary - Last {hours} Hours

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Commits**: {len(commits)}
**Files Modified**: {len(files)}
**Patterns Added**: {len(patterns)}

---

## 📊 Activity Summary

"""

    # Commits
    if commits:
        summary += "### Git Commits\n\n"
        for commit in commits[:10]:  # Show last 10
            summary += f"- **{commit['hash']}** ({commit['date']}): {commit['message']}\n"
        if len(commits) > 10:
            summary += f"\n... and {len(commits)-10} more commits\n"
        summary += "\n"

    # Files by category
    if file_categories:
        summary += "### Files Modified by Category\n\n"
        for category, cat_files in file_categories.items():
            summary += f"**{category.title()}** ({len(cat_files)} files):\n"
            for f in cat_files[:5]:
                summary += f"- {f}\n"
            if len(cat_files) > 5:
                summary += f"- ... and {len(cat_files)-5} more\n"
            summary += "\n"

    # Patterns
    if patterns:
        summary += "### Patterns Created\n\n"
        for pattern in patterns:
            summary += f"- **{pattern['agent']}**: {pattern['name']}\n"
        summary += "\n"

    # Recent work inference
    summary += "## 🔍 Inferred Recent Work\n\n"

    if any('agents/' in c['message'] for c in commits):
        summary += "- ✅ Agent manifest updates\n"
    if any('P0' in c['message'] or 'audit' in c['message'].lower() for c in commits):
        summary += "- ✅ Great Audit P0 fixes implementation\n"
    if any('pattern' in c['message'].lower() for c in commits):
        summary += "- ✅ Pattern library work\n"
    if any('trigger' in c['message'].lower() for c in commits):
        summary += "- ✅ Activation triggers implementation\n"
    if any('template' in c['message'].lower() for c in commits):
        summary += "- ✅ Output templates creation\n"

    summary += "\n---\n\n"

    # Key files to review
    summary += "## 📁 Key Files to Review\n\n"
    summary += "**Most Recent Changes**:\n"
    for f in files[:15]:
        summary += f"- {f}\n"
    if len(files) > 15:
        summary += f"\n... and {len(files)-15} more files\n"

    summary += "\n---\n\n"

    # Next steps suggestion
    summary += "## ⏭️ Suggested Next Steps\n\n"
    summary += "1. Review git commits above for context\n"
    summary += "2. Check for any TODO items in recent work\n"
    summary += "3. Run any validation needed for recent changes\n"
    summary += "4. Continue with pending tasks from todo list\n"

    return summary

def save_summary(summary, filename='session-summary-latest.md'):
    """Save summary to file"""
    filepath = Path('to-corey') / filename
    filepath.write_text(summary)
    print(f"✅ Session summary saved to: {filepath}")
    return filepath

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate session summary')
    parser.add_argument('--hours', type=int, default=24, help='Hours to look back')
    parser.add_argument('--output', type=str, default='session-summary-latest.md',
                       help='Output filename')

    args = parser.parse_args()

    summary = get_session_summary(args.hours)
    filepath = save_summary(summary, args.output)

    # Also print to stdout
    print("\n" + "="*80)
    print(summary)
    print("="*80)
