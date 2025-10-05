#!/usr/bin/env python3
"""
File Garden Ritual - Categorize files as Living/Dormant/Dead
Semantic composting: Extract insights from dead files before deletion
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Define file age thresholds (in days)
RECENT = 7  # Files modified in last week = Living
DORMANT = 30  # Files modified 1-4 weeks ago = Dormant  
DEAD = 120  # Files not modified in 4+ months = Dead

def get_file_age(filepath):
    """Get days since last modification"""
    mtime = os.path.getmtime(filepath)
    age_seconds = datetime.now().timestamp() - mtime
    return age_seconds / 86400  # Convert to days

def categorize_files():
    """Walk project and categorize all files"""
    
    categories = {
        'living': [],  # Active files
        'dormant': [],  # Might need revival
        'dead': []  # Candidates for deletion
    }
    
    # Ignore patterns
    ignore = {'.git', '__pycache__', '.venv', 'node_modules', '.trash'}
    
    for root, dirs, files in os.walk('.'):
        # Filter ignored dirs
        dirs[:] = [d for d in dirs if d not in ignore]
        
        for file in files:
            filepath = os.path.join(root, file)
            age = get_file_age(filepath)
            
            # Categorize by age
            if age < RECENT:
                categories['living'].append(filepath)
            elif age < DORMANT:
                categories['dormant'].append(filepath)
            else:
                categories['dead'].append(filepath)
    
    return categories

def generate_report(categories):
    """Generate markdown report"""
    
    report = """# File Garden Ritual - Analysis Report

**Date**: {date}
**Total Files**: {total}

---

## 🌱 Living Files ({living_count})

Recently modified (< {recent} days) - Active, keep:

{living_list}

---

## 🍂 Dormant Files ({dormant_count})

Not modified in {recent}-{dormant} days - Review for revival or archival:

{dormant_list}

---

## 💀 Dead Files ({dead_count})

Not modified in {dead}+ days - Candidates for .trash/ (semantic composting first):

{dead_list}

---

## Semantic Composting Candidates

**High-value dead files** (extract insights before deletion):

{compost_list}

---

## Recommendations

1. **Keep**: All {living_count} living files
2. **Review**: {dormant_count} dormant files (decide keep/archive/delete)
3. **Compost**: Extract insights from {compost_count} high-value dead files
4. **Trash**: Move {trash_count} low-value dead files to .trash/

**Next Steps**: 
- Read high-value dead files
- Extract learnings to .claude/memory/
- Move to .trash/ for 30-day review
- Permanent deletion after review period
""".format(
        date=datetime.now().strftime("%Y-%m-%d"),
        total=sum(len(v) for v in categories.values()),
        living_count=len(categories['living']),
        dormant_count=len(categories['dormant']),
        dead_count=len(categories['dead']),
        recent=RECENT,
        dormant=DORMANT,
        dead=DEAD,
        living_list='\n'.join(f"- {f}" for f in sorted(categories['living'])[:20]) + 
                    f"\n... and {len(categories['living'])-20} more" if len(categories['living']) > 20 else '\n'.join(f"- {f}" for f in sorted(categories['living'])),
        dormant_list='\n'.join(f"- {f}" for f in sorted(categories['dormant'])[:20]) + 
                     f"\n... and {len(categories['dormant'])-20} more" if len(categories['dormant']) > 20 else '\n'.join(f"- {f}" for f in sorted(categories['dormant'])),
        dead_list='\n'.join(f"- {f}" for f in sorted(categories['dead'])[:20]) + 
                  f"\n... and {len(categories['dead'])-20} more" if len(categories['dead']) > 20 else '\n'.join(f"- {f}" for f in sorted(categories['dead'])),
        compost_list=get_compost_candidates(categories['dead']),
        compost_count=len([f for f in categories['dead'] if is_high_value(f)]),
        trash_count=len([f for f in categories['dead'] if not is_high_value(f)])
    )
    
    return report

def is_high_value(filepath):
    """Determine if dead file has extractable insights"""
    # High-value patterns: docs, memory, learnings, reports
    high_value_patterns = ['memory', 'learning', 'report', 'analysis', 'synthesis', 'insight', 'pattern']
    return any(pattern in filepath.lower() for pattern in high_value_patterns)

def get_compost_candidates(dead_files):
    """Get list of dead files worth composting"""
    candidates = [f for f in dead_files if is_high_value(f)]
    if not candidates:
        return "None identified"
    return '\n'.join(f"- {f}" for f in sorted(candidates)[:10]) + \
           (f"\n... and {len(candidates)-10} more" if len(candidates) > 10 else "")

# Run analysis
if __name__ == "__main__":
    print("🌱 Running File Garden Ritual analysis...")
    categories = categorize_files()
    report = generate_report(categories)
    
    # Write report
    with open('.claude/analysis/file-garden-report.md', 'w') as f:
        f.write(report)
    
    # Also write JSON for programmatic access
    with open('.claude/analysis/file-garden-data.json', 'w') as f:
        json.dump(categories, f, indent=2)
    
    print(f"✅ Analysis complete!")
    print(f"   Living: {len(categories['living'])}")
    print(f"   Dormant: {len(categories['dormant'])}")
    print(f"   Dead: {len(categories['dead'])}")
    print(f"\n📄 Report: .claude/analysis/file-garden-report.md")
    print(f"📊 Data: .claude/analysis/file-garden-data.json")
