#!/usr/bin/env python3
"""
Archive Scanner CLI - Quick interface for testing and querying
Usage:
    python tools/archive_cli.py scan              # Scan all sessions
    python tools/archive_cli.py stats             # Show statistics
    python tools/archive_cli.py agent <name>      # Agent details
    python tools/archive_cli.py session <id>      # Session details
"""

import sys
from tools.archive_scanner import ArchiveScanner


def cmd_scan(scanner, incremental=True):
    """Scan session logs."""
    print("Scanning session logs...")
    stats = scanner.scan_directory('memories/logs/sessions', incremental=incremental)

    print(f"\n✓ Scan complete")
    print(f"  Files scanned: {stats['files_scanned']}")
    print(f"  Files skipped: {stats['files_skipped']}")
    print(f"  Sessions: {stats['sessions']}")
    print(f"  Agent invocations: {stats['agent_invocations']}")
    print(f"  Tool calls: {stats['tool_calls']}")

    if stats['errors']:
        print(f"\n⚠ Errors: {len(stats['errors'])}")
        for error in stats['errors'][:3]:
            print(f"  - {error}")


def cmd_stats(scanner):
    """Show database statistics."""
    agents = scanner.all_agents()
    sessions = scanner.all_sessions()

    print("=== ARCHIVE STATISTICS ===\n")

    print(f"Sessions: {len(sessions)}")
    print(f"Unique agents: {len(agents)}")

    total_invocations = sum(a['total_invocations'] for a in agents)
    print(f"Total agent invocations: {total_invocations}")

    total_tokens = sum(s['total_tokens'] or 0 for s in sessions)
    print(f"Total tokens: {total_tokens:,}")

    print("\n=== TOP 10 AGENTS BY INVOCATIONS ===\n")
    for i, agent in enumerate(agents[:10], 1):
        name = agent['agent_name']
        invocations = agent['total_invocations']
        sessions_count = agent['sessions_participated']
        print(f"{i:2}. {name:25} {invocations:4} invocations, {sessions_count:2} sessions")

    if sessions:
        print("\n=== RECENT SESSIONS ===\n")
        for i, session in enumerate(sessions[:5], 1):
            sid = session['session_id'][:8]
            date = session['start_time'][:10] if session['start_time'] else 'N/A'
            msgs = session['total_messages']
            tokens = session['total_tokens'] or 0
            print(f"{i}. {date} [{sid}...] {msgs:3} msgs, {tokens:,} tokens")


def cmd_agent(scanner, agent_name):
    """Show agent details."""
    agent = scanner.agent(agent_name)

    metrics = agent.metrics()
    if not metrics:
        print(f"❌ Agent '{agent_name}' not found")
        return

    print(f"=== AGENT: {agent_name} ===\n")
    print(f"Total invocations: {metrics['total_invocations']}")
    print(f"Successful: {metrics['successful_invocations']}")
    print(f"Failed: {metrics['failed_invocations']}")
    print(f"Sessions participated: {metrics['sessions_participated']}")

    first = metrics['first_seen'][:10] if metrics['first_seen'] else 'N/A'
    last = metrics['last_seen'][:10] if metrics['last_seen'] else 'N/A'
    print(f"First seen: {first}")
    print(f"Last seen: {last}")

    print("\n=== RECENT INVOCATIONS ===\n")
    invocations = agent.invocations()
    for i, inv in enumerate(invocations[:10], 1):
        date = inv['invoked_at'][:10] if inv['invoked_at'] else 'N/A'
        desc = inv['description'] or '(no description)'
        desc_short = desc[:50] + '...' if len(desc) > 50 else desc
        print(f"{i:2}. {date} - {desc_short}")


def cmd_session(scanner, session_id):
    """Show session details."""
    session = scanner.session(session_id)

    metadata = session.metadata()
    if not metadata:
        print(f"❌ Session '{session_id}' not found")
        return

    print(f"=== SESSION: {session_id} ===\n")
    print(f"Start time: {metadata.get('start_time', 'N/A')[:19]}")
    print(f"End time: {metadata.get('end_time', 'N/A')[:19]}")
    print(f"Total messages: {metadata.get('total_messages', 0)}")
    print(f"Total tokens: {metadata.get('total_tokens', 0):,}")
    print(f"Input tokens: {metadata.get('input_tokens', 0):,}")
    print(f"Output tokens: {metadata.get('output_tokens', 0):,}")
    print(f"Cache read tokens: {metadata.get('cache_read_tokens', 0):,}")

    print("\n=== AGENTS INVOKED ===\n")
    agents = session.agents()
    agent_counts = {}
    for agent in agents:
        name = agent['agent_name']
        agent_counts[name] = agent_counts.get(name, 0) + 1

    for name, count in sorted(agent_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {name:25} {count:2}x")

    print("\n=== TOOL USAGE ===\n")
    tools = session.tools()
    tool_counts = {}
    for tool in tools:
        name = tool['tool_name']
        tool_counts[name] = tool_counts.get(name, 0) + 1

    for name, count in sorted(tool_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {name:15} {count:4}x")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    scanner = ArchiveScanner('.claude/analytics/archive.db')
    command = sys.argv[1]

    if command == 'scan':
        incremental = '--full' not in sys.argv
        cmd_scan(scanner, incremental=incremental)

    elif command == 'stats':
        cmd_stats(scanner)

    elif command == 'agent':
        if len(sys.argv) < 3:
            print("Usage: python tools/archive_cli.py agent <agent_name>")
            return
        cmd_agent(scanner, sys.argv[2])

    elif command == 'session':
        if len(sys.argv) < 3:
            print("Usage: python tools/archive_cli.py session <session_id>")
            return
        cmd_session(scanner, sys.argv[2])

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == '__main__':
    main()
