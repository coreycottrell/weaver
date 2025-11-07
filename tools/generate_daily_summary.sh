#!/bin/bash

# generate_daily_summary.sh
# Generates daily summary from git activity, memory entries, and handoff documents
# Usage: ./generate_daily_summary.sh [date]
# If no date provided, uses today's date

set -e

# Configuration
REPO_ROOT="/home/corey/projects/AI-CIV/WEAVER"
MEMORY_DIR="$REPO_ROOT/.claude/memory"
SUMMARY_DIR="$MEMORY_DIR/summaries"
TO_COREY_DIR="$REPO_ROOT/to-corey"

# Date handling
if [ -z "$1" ]; then
    TARGET_DATE=$(date +%Y-%m-%d)
else
    TARGET_DATE="$1"
fi

SUMMARY_FILE="$SUMMARY_DIR/$TARGET_DATE-daily-summary.md"

# Ensure summary directory exists
mkdir -p "$SUMMARY_DIR"

cd "$REPO_ROOT"

# Header
cat > "$SUMMARY_FILE" << EOF
# Daily Summary: $TARGET_DATE

**Generated**: $(date +"%Y-%m-%d %H:%M:%S")

---

## 🔗 Critical Handoff Documents

EOF

# Find handoff documents created/modified today
echo "**Documents created/modified today:**" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"

HANDOFF_FOUND=false

# Search for handoff files in to-corey/ directory
if [ -d "$TO_COREY_DIR" ]; then
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            HANDOFF_FOUND=true
            rel_path=$(realpath --relative-to="$REPO_ROOT" "$file")
            basename=$(basename "$file")
            echo "- [\`$basename\`]($rel_path)" >> "$SUMMARY_FILE"
        fi
    done < <(find "$TO_COREY_DIR" -type f -name "*.md" -mtime -1 2>/dev/null | sort)
fi

# Search for HANDOFF/handoff files elsewhere in repo
while IFS= read -r file; do
    if [ -f "$file" ]; then
        # Exclude files already found in to-corey/
        if [[ "$file" != "$TO_COREY_DIR"* ]]; then
            HANDOFF_FOUND=true
            rel_path=$(realpath --relative-to="$REPO_ROOT" "$file")
            basename=$(basename "$file")
            echo "- [\`$basename\`]($rel_path)" >> "$SUMMARY_FILE"
        fi
    fi
done < <(find . -type f \( -iname "*handoff*" -o -iname "*READY*" \) -mtime -1 2>/dev/null | grep -v ".git" | sort)

if [ "$HANDOFF_FOUND" = false ]; then
    echo "_No handoff documents found for today._" >> "$SUMMARY_FILE"
fi

echo "" >> "$SUMMARY_FILE"

# Recent files in to-corey/ (last 5, even if not from today)
echo "**Recent to-corey/ documents (last 5):**" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"

if [ -d "$TO_COREY_DIR" ]; then
    RECENT_COUNT=0
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            rel_path=$(realpath --relative-to="$REPO_ROOT" "$file")
            basename=$(basename "$file")
            mod_date=$(stat -c %y "$file" | cut -d' ' -f1)
            echo "- [\`$basename\`]($rel_path) (modified: $mod_date)" >> "$SUMMARY_FILE"
            RECENT_COUNT=$((RECENT_COUNT + 1))
        fi
    done < <(find "$TO_COREY_DIR" -type f -name "*.md" -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -5 | cut -d' ' -f2-)

    if [ $RECENT_COUNT -eq 0 ]; then
        echo "_No documents in to-corey/ directory._" >> "$SUMMARY_FILE"
    fi
else
    echo "_to-corey/ directory not found._" >> "$SUMMARY_FILE"
fi

echo "" >> "$SUMMARY_FILE"

# Git commits for the day
cat >> "$SUMMARY_FILE" << EOF

---

## 📝 Git Commits Today

EOF

# Get commits from target date (00:00 to 23:59)
COMMIT_COUNT=$(git log --since="$TARGET_DATE 00:00" --until="$TARGET_DATE 23:59" --oneline | wc -l)

if [ $COMMIT_COUNT -eq 0 ]; then
    echo "_No commits on $TARGET_DATE._" >> "$SUMMARY_FILE"
else
    echo "**Total commits**: $COMMIT_COUNT" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"

    # List commits with hash, message, and files changed
    git log --since="$TARGET_DATE 00:00" --until="$TARGET_DATE 23:59" \
        --pretty=format:"### %h - %s%n%n**Author**: %an <%ae>%n**Date**: %ai%n" \
        --name-status >> "$SUMMARY_FILE"

    echo "" >> "$SUMMARY_FILE"
fi

# Files changed summary
cat >> "$SUMMARY_FILE" << EOF

---

## 📊 Files Changed Today

EOF

# Get unique files changed in commits today
FILES_CHANGED=$(git log --since="$TARGET_DATE 00:00" --until="$TARGET_DATE 23:59" \
    --name-only --pretty=format: | sort -u | grep -v '^$')

if [ -z "$FILES_CHANGED" ]; then
    echo "_No files changed in commits on $TARGET_DATE._" >> "$SUMMARY_FILE"
else
    FILE_COUNT=$(echo "$FILES_CHANGED" | wc -l)
    echo "**Total files**: $FILE_COUNT" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"

    # Group by category
    echo "**By Category**:" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"

    # Agents
    AGENT_FILES=$(echo "$FILES_CHANGED" | grep "^.claude/agents/" || true)
    if [ -n "$AGENT_FILES" ]; then
        echo "- **Agent definitions**: $(echo "$AGENT_FILES" | wc -l) files" >> "$SUMMARY_FILE"
    fi

    # Memory
    MEMORY_FILES=$(echo "$FILES_CHANGED" | grep "^.claude/memory/" || true)
    if [ -n "$MEMORY_FILES" ]; then
        echo "- **Memory entries**: $(echo "$MEMORY_FILES" | wc -l) files" >> "$SUMMARY_FILE"
    fi

    # Flows
    FLOW_FILES=$(echo "$FILES_CHANGED" | grep "^.claude/flows/" || true)
    if [ -n "$FLOW_FILES" ]; then
        echo "- **Flows**: $(echo "$FLOW_FILES" | wc -l) files" >> "$SUMMARY_FILE"
    fi

    # Tools
    TOOL_FILES=$(echo "$FILES_CHANGED" | grep "^tools/" || true)
    if [ -n "$TOOL_FILES" ]; then
        echo "- **Tools**: $(echo "$TOOL_FILES" | wc -l) files" >> "$SUMMARY_FILE"
    fi

    # To Corey
    TOCOREY_FILES=$(echo "$FILES_CHANGED" | grep "^to-corey/" || true)
    if [ -n "$TOCOREY_FILES" ]; then
        echo "- **Handoff docs**: $(echo "$TOCOREY_FILES" | wc -l) files" >> "$SUMMARY_FILE"
    fi

    # Other
    OTHER_FILES=$(echo "$FILES_CHANGED" | grep -v "^.claude/" | grep -v "^tools/" | grep -v "^to-corey/" || true)
    if [ -n "$OTHER_FILES" ]; then
        echo "- **Other**: $(echo "$OTHER_FILES" | wc -l) files" >> "$SUMMARY_FILE"
    fi

    echo "" >> "$SUMMARY_FILE"
fi

# Memory entries created today
cat >> "$SUMMARY_FILE" << EOF

---

## 🧠 Memory Entries Created Today

EOF

# Find memory entries created today
MEMORY_ENTRIES=$(find "$MEMORY_DIR/agent-learnings" -type f -name "*$TARGET_DATE*.md" 2>/dev/null | sort)

if [ -z "$MEMORY_ENTRIES" ]; then
    echo "_No memory entries created on $TARGET_DATE._" >> "$SUMMARY_FILE"
else
    ENTRY_COUNT=$(echo "$MEMORY_ENTRIES" | wc -l)
    echo "**Total entries**: $ENTRY_COUNT" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"

    # List by agent
    echo "$MEMORY_ENTRIES" | while read -r entry; do
        if [ -f "$entry" ]; then
            rel_path=$(realpath --relative-to="$REPO_ROOT" "$entry")
            agent_name=$(echo "$rel_path" | cut -d'/' -f4)
            filename=$(basename "$entry")

            # Extract topic from filename (format: YYYY-MM-DD--type-topic.md)
            topic=$(echo "$filename" | sed 's/^[0-9-]*--//' | sed 's/\.md$//' | tr '-' ' ')

            echo "- **$agent_name**: [\`$topic\`]($rel_path)" >> "$SUMMARY_FILE"
        fi
    done
fi

echo "" >> "$SUMMARY_FILE"

# Current status
cat >> "$SUMMARY_FILE" << EOF

---

## 📍 Current Status

**Branch**: $(git branch --show-current)

**Uncommitted changes**:
EOF

# Check for uncommitted changes
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "_Working tree clean._" >> "$SUMMARY_FILE"
else
    echo "" >> "$SUMMARY_FILE"
    git status --short >> "$SUMMARY_FILE"
fi

echo "" >> "$SUMMARY_FILE"

# Footer
cat >> "$SUMMARY_FILE" << EOF

---

## 📚 Next Session Checklist

When waking up cold, review:

1. **Critical handoffs** (see top of this document)
2. **Git commits** (what changed and why)
3. **Memory entries** (what was learned)
4. **Current status** (what's in progress)
5. **Roadmap**: \`INTEGRATION-ROADMAP.md\`
6. **Constitutional grounding**: \`CLAUDE.md\` → \`CLAUDE-CORE.md\` Books I-II

---

**End of Daily Summary**
EOF

# Update latest.md symlink
cd "$SUMMARY_DIR"
ln -sf "$TARGET_DATE-daily-summary.md" latest.md

echo "✅ Daily summary generated: $SUMMARY_FILE"
echo "   Symlink updated: $SUMMARY_DIR/latest.md"
