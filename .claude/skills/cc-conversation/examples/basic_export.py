#!/usr/bin/env python3
"""
Basic example: Export latest session to Markdown.
"""

from claude_code_conversation import get_active_session, export_conversation


def main():
    # Find active session
    session = get_active_session()

    print(f"Exporting session: {session['session_id']}")
    print(f"File size: {session['file_size']:,} bytes")
    print(f"Messages: ~{session['message_count']}")

    # Export to Markdown
    output_path = export_conversation(
        session_id=session['session_id'],
        format="markdown",
        include_metadata=True
    )

    print(f"\nExported to: {output_path}")


if __name__ == "__main__":
    main()
