#!/bin/bash
# search-archive.sh - Quick search helper for CLAUDE-CODE-WEB archive
# Created: 2025-11-07 by refactoring-specialist

# Color codes for readable output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Archive directory (absolute path)
ARCHIVE_DIR="/home/user/weaver/CLAUDE-CODE-WEB"

# Function to display usage
show_help() {
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}search-archive.sh${NC} - Quick search helper for CLAUDE-CODE-WEB"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}USAGE:${NC}"
    echo "  $0 --topic <query>      Search for topic across all files"
    echo "  $0 --agent <name>       Find files related to specific agent"
    echo "  $0 --recent [N]         Show N most recently modified files (default: 10)"
    echo "  $0 --date <YYYY-MM-DD>  Find files modified on specific date"
    echo "  $0 --help               Show this help message"
    echo ""
    echo -e "${YELLOW}EXAMPLES:${NC}"
    echo "  $0 --topic \"memory system\""
    echo "  $0 --agent doc-synthesizer"
    echo "  $0 --recent 20"
    echo "  $0 --date 2025-11-07"
    echo ""
    echo -e "${YELLOW}NOTES:${NC}"
    echo "  - Topic search is case-insensitive"
    echo "  - Results limited to first 20 matches for readability"
    echo "  - Agent names use dash format (e.g., doc-synthesizer, not doc_synthesizer)"
    echo ""
}

# Function to check if archive directory exists
check_archive() {
    if [ ! -d "$ARCHIVE_DIR" ]; then
        echo -e "${RED}ERROR: Archive directory not found: $ARCHIVE_DIR${NC}" >&2
        exit 1
    fi
}

# Function for topic search
search_topic() {
    local query="$1"
    
    if [ -z "$query" ]; then
        echo -e "${RED}ERROR: No search query provided${NC}" >&2
        echo "Usage: $0 --topic <query>"
        exit 1
    fi
    
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Topic Search:${NC} \"${YELLOW}$query${NC}\""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Search with grep, case-insensitive, show line numbers and file names
    local results=$(grep -r -i -n --color=never "$query" "$ARCHIVE_DIR" 2>/dev/null | head -20)
    
    if [ -z "$results" ]; then
        echo -e "${YELLOW}No results found for:${NC} \"$query\""
        exit 0
    fi
    
    # Format output with colors
    echo "$results" | while IFS= read -r line; do
        # Extract file path and content
        local file_path=$(echo "$line" | cut -d: -f1)
        local line_num=$(echo "$line" | cut -d: -f2)
        local content=$(echo "$line" | cut -d: -f3-)
        
        # Get relative path from archive dir
        local rel_path="${file_path#$ARCHIVE_DIR/}"
        
        echo -e "${BLUE}$rel_path${NC}:${GREEN}$line_num${NC}: $content"
    done
    
    local total=$(grep -r -i -c "$query" "$ARCHIVE_DIR" 2>/dev/null | grep -v ":0$" | wc -l)
    echo ""
    echo -e "${CYAN}Found matches in ${YELLOW}$total${CYAN} files (showing first 20 lines)${NC}"
}

# Function for agent search
search_agent() {
    local agent_name="$1"
    
    if [ -z "$agent_name" ]; then
        echo -e "${RED}ERROR: No agent name provided${NC}" >&2
        echo "Usage: $0 --agent <agent-name>"
        exit 1
    fi
    
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Agent Search:${NC} ${YELLOW}$agent_name${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Search for agent name in filenames and content
    local file_matches=$(find "$ARCHIVE_DIR" -type f -iname "*$agent_name*" 2>/dev/null)
    local content_matches=$(grep -r -l -i "$agent_name" "$ARCHIVE_DIR" 2>/dev/null | head -20)
    
    if [ -z "$file_matches" ] && [ -z "$content_matches" ]; then
        echo -e "${YELLOW}No files found related to agent:${NC} \"$agent_name\""
        exit 0
    fi
    
    # Show filename matches first
    if [ -n "$file_matches" ]; then
        echo -e "${GREEN}Files with agent name in filename:${NC}"
        echo "$file_matches" | while read -r file; do
            local rel_path="${file#$ARCHIVE_DIR/}"
            echo -e "  ${BLUE}$rel_path${NC}"
        done
        echo ""
    fi
    
    # Show content matches
    if [ -n "$content_matches" ]; then
        echo -e "${GREEN}Files mentioning agent in content:${NC}"
        echo "$content_matches" | while read -r file; do
            local rel_path="${file#$ARCHIVE_DIR/}"
            local match_count=$(grep -i -c "$agent_name" "$file" 2>/dev/null)
            echo -e "  ${BLUE}$rel_path${NC} (${YELLOW}$match_count${NC} mentions)"
        done
    fi
    
    local total=$(echo -e "$file_matches\n$content_matches" | sort -u | grep -v "^$" | wc -l)
    echo ""
    echo -e "${CYAN}Found ${YELLOW}$total${CYAN} unique files related to agent${NC}"
}

# Function for recent files
show_recent() {
    local count="${1:-10}"
    
    # Validate count is a number
    if ! [[ "$count" =~ ^[0-9]+$ ]]; then
        echo -e "${RED}ERROR: Invalid count: $count (must be a number)${NC}" >&2
        exit 1
    fi
    
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Recent Files:${NC} ${YELLOW}$count${NC} most recently modified"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Find and sort by modification time
    find "$ARCHIVE_DIR" -type f -printf "%T+ %p\n" 2>/dev/null | \
        sort -r | \
        head -n "$count" | \
        while read -r timestamp file; do
            local rel_path="${file#$ARCHIVE_DIR/}"
            local date_only=$(echo "$timestamp" | cut -d+ -f1)
            echo -e "${GREEN}$date_only${NC} ${BLUE}$rel_path${NC}"
        done
}

# Function for date range search
search_date() {
    local target_date="$1"
    
    if [ -z "$target_date" ]; then
        echo -e "${RED}ERROR: No date provided${NC}" >&2
        echo "Usage: $0 --date <YYYY-MM-DD>"
        exit 1
    fi
    
    # Validate date format
    if ! [[ "$target_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo -e "${RED}ERROR: Invalid date format: $target_date${NC}" >&2
        echo "Expected format: YYYY-MM-DD (e.g., 2025-11-07)"
        exit 1
    fi
    
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Files Modified On:${NC} ${YELLOW}$target_date${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Find files modified on specific date
    local results=$(find "$ARCHIVE_DIR" -type f -newermt "$target_date 00:00:00" ! -newermt "$target_date 23:59:59" -printf "%T+ %p\n" 2>/dev/null | sort -r)
    
    if [ -z "$results" ]; then
        echo -e "${YELLOW}No files found modified on:${NC} $target_date"
        exit 0
    fi
    
    echo "$results" | while read -r timestamp file; do
        local rel_path="${file#$ARCHIVE_DIR/}"
        local time_only=$(echo "$timestamp" | cut -d+ -f1 | cut -dT -f2 | cut -d. -f1)
        echo -e "${GREEN}$time_only${NC} ${BLUE}$rel_path${NC}"
    done
    
    local total=$(echo "$results" | wc -l)
    echo ""
    echo -e "${CYAN}Found ${YELLOW}$total${CYAN} files modified on $target_date${NC}"
}

# Main script logic
main() {
    # Check if archive exists
    check_archive
    
    # Parse command line arguments
    case "$1" in
        --topic)
            shift
            search_topic "$*"
            ;;
        --agent)
            shift
            search_agent "$1"
            ;;
        --recent)
            shift
            show_recent "$1"
            ;;
        --date)
            shift
            search_date "$1"
            ;;
        --help|"")
            show_help
            ;;
        *)
            echo -e "${RED}ERROR: Unknown option: $1${NC}" >&2
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"
