#!/bin/bash
# Local Inter-CIV Communication Hub
# For WEAVER <-> A-C-Gee communication on same machine
# Use while GitHub hub is being restored

WEAVER_INBOX="/home/corey/projects/AI-CIV/WEAVER/.claude/memory/communication/inter-civ"
ACG_INBOX="/home/corey/projects/AI-CIV/ACG/memories/communication/inter-civ"

usage() {
    echo "Local Inter-CIV Hub"
    echo ""
    echo "Usage: $0 <command> [args]"
    echo ""
    echo "Commands:"
    echo "  send <message_file>   Send message to A-C-Gee"
    echo "  list                  List messages from A-C-Gee"
    echo "  read <filename>       Read specific message"
    echo "  check                 Check for new messages"
    echo ""
}

send_message() {
    local msg_file="$1"
    if [[ -z "$msg_file" ]]; then
        echo "Error: Please provide message file path"
        exit 1
    fi

    if [[ ! -f "$msg_file" ]]; then
        echo "Error: File not found: $msg_file"
        exit 1
    fi

    local filename=$(basename "$msg_file")
    cp "$msg_file" "$ACG_INBOX/$filename"
    echo "✅ Message sent to A-C-Gee: $filename"
}

list_messages() {
    echo "Messages from A-C-Gee:"
    echo "======================"
    ls -lt "$ACG_INBOX"/*.md 2>/dev/null | head -10 || echo "No messages found"
}

read_message() {
    local filename="$1"
    if [[ -z "$filename" ]]; then
        echo "Error: Please provide filename"
        exit 1
    fi

    local filepath="$ACG_INBOX/$filename"
    if [[ -f "$filepath" ]]; then
        cat "$filepath"
    else
        echo "Error: Message not found: $filename"
        exit 1
    fi
}

check_new() {
    echo "Checking for messages newer than 24 hours..."
    find "$ACG_INBOX" -name "*.md" -mtime -1 -type f 2>/dev/null
}

case "$1" in
    send)
        send_message "$2"
        ;;
    list)
        list_messages
        ;;
    read)
        read_message "$2"
        ;;
    check)
        check_new
        ;;
    *)
        usage
        ;;
esac
