#!/usr/bin/env python3
"""
Search conversation history example.

Search for errors and large responses.
"""

from claude_code_conversation import search_history, find_large_responses, find_errors


def main():
    print("=" * 80)
    print("CONVERSATION HISTORY SEARCH")
    print("=" * 80)

    # Find recent errors
    print("\n1. Searching for errors in last 10 sessions...")
    errors = find_errors(session_limit=10)

    print(f"Found {len(errors)} error messages:\n")

    for error in errors[:5]:  # Show top 5
        print(f"[{error['timestamp']}] {error['role']}")
        print(f"Preview: {error['content_preview']}")
        print(f"Session: {error['session_id'][:16]}...")
        print()

    # Find large responses
    print("\n2. Searching for large responses (>1000 tokens)...")
    large = find_large_responses(min_output_tokens=1000, session_limit=10)

    print(f"Found {len(large)} large responses:\n")

    for resp in large[:5]:  # Show top 5
        print(f"[{resp['timestamp']}] {resp['output_tokens']:,} tokens")
        print(f"Preview: {resp['content_preview']}")
        print(f"Session: {resp['session_id'][:16]}...")
        print()

    # Custom search
    print("\n3. Searching for 'telegram wrapper protocol'...")
    results = search_history(
        query="telegram wrapper protocol",
        session_limit=20,
        case_sensitive=False
    )

    print(f"Found {len(results)} matches:\n")

    for result in results[:3]:  # Show top 3
        print(f"[{result['timestamp']}] {result['role']}")
        print(f"Highlights: {result['match_highlights']}")
        print()


if __name__ == "__main__":
    main()
