"""
Archive Scanner - Core Infrastructure
Scans session JSONL logs and builds SQLite database for analytics.
"""

import os
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Iterator
from datetime import datetime
from dataclasses import dataclass, asdict

from tools.archive_parser import JSONLParser, AgentInvocation, ToolUsage


@dataclass
class AgentQuery:
    """Query interface for agent-specific analytics."""
    db_path: str
    agent_name: str

    def invocations(self) -> List[Dict]:
        """Get all invocations for this agent."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM agent_invocations
            WHERE agent_name = ?
            ORDER BY invoked_at DESC
        """, (self.agent_name,))

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results

    def metrics(self) -> Dict:
        """Get aggregated metrics for this agent."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM agent_metrics
            WHERE agent_name = ?
        """, (self.agent_name,))

        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else {}

    def sessions(self) -> List[str]:
        """Get all sessions this agent participated in."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT session_id
            FROM agent_invocations
            WHERE agent_name = ?
            ORDER BY invoked_at DESC
        """, (self.agent_name,))

        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return results


@dataclass
class SessionQuery:
    """Query interface for session-specific analytics."""
    db_path: str
    session_id: str

    def metadata(self) -> Dict:
        """Get session metadata."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM sessions
            WHERE session_id = ?
        """, (self.session_id,))

        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else {}

    def agents(self) -> List[Dict]:
        """Get all agents invoked in this session."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM agent_invocations
            WHERE session_id = ?
            ORDER BY invoked_at
        """, (self.session_id,))

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results

    def tools(self) -> List[Dict]:
        """Get all tool usage in this session."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM tool_usage
            WHERE session_id = ?
            ORDER BY invoked_at
        """, (self.session_id,))

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results


class IncrementalScanner:
    """Tracks which files have been scanned and handles incremental updates."""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def needs_scanning(self, file_path: str) -> bool:
        """Check if file needs scanning based on modification time."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get file's current mtime
        try:
            current_mtime = os.path.getmtime(file_path)
            current_size = os.path.getsize(file_path)
        except OSError:
            conn.close()
            return False

        # Check scan state
        cursor.execute("""
            SELECT last_modified_time, file_size
            FROM scan_state
            WHERE file_path = ?
        """, (file_path,))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return True  # Never scanned

        last_mtime, last_size = row
        # Scan if file has been modified or size changed
        return (current_mtime > last_mtime or current_size != last_size)

    def mark_scanned(self, file_path: str, session_id: str):
        """Mark file as scanned with current timestamp."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        current_mtime = os.path.getmtime(file_path)
        current_size = os.path.getsize(file_path)
        now = datetime.now().isoformat()

        cursor.execute("""
            INSERT OR REPLACE INTO scan_state
            (file_path, last_modified_time, last_scanned_at, file_size, session_id)
            VALUES (?, ?, ?, ?, ?)
        """, (file_path, current_mtime, now, current_size, session_id))

        conn.commit()
        conn.close()


class ArchiveScanner:
    """Main scanner class for processing session logs into SQLite database."""

    def __init__(self, db_path: str = ".claude/analytics/archive.db"):
        self.db_path = db_path
        self.incremental = IncrementalScanner(db_path)
        self._initialize_database()

    def _initialize_database(self):
        """Create database schema if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)

        # Read and execute schema
        schema_path = Path(self.db_path).parent / "schema.sql"
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
                conn.executescript(schema_sql)

        conn.commit()
        conn.close()

    def scan_directory(self, logs_dir: str = "memories/logs/sessions",
                      incremental: bool = True) -> Dict:
        """Scan all JSONL files in directory."""
        stats = {
            'files_scanned': 0,
            'files_skipped': 0,
            'agent_invocations': 0,
            'tool_calls': 0,
            'sessions': 0,
            'errors': []
        }

        logs_path = Path(logs_dir)
        if not logs_path.exists():
            return stats

        for jsonl_file in logs_path.glob("*.jsonl"):
            file_path = str(jsonl_file)

            # Skip if already scanned (incremental mode)
            if incremental and not self.incremental.needs_scanning(file_path):
                stats['files_skipped'] += 1
                continue

            try:
                result = self._scan_file(file_path)
                stats['files_scanned'] += 1
                stats['agent_invocations'] += result['agent_invocations']
                stats['tool_calls'] += result['tool_calls']
                stats['sessions'] += 1
            except Exception as e:
                stats['errors'].append(f"{file_path}: {str(e)}")

        # Update agent metrics
        self._update_agent_metrics()

        return stats

    def _scan_file(self, file_path: str) -> Dict:
        """Scan a single JSONL file and insert into database."""
        parser = JSONLParser(file_path)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {'agent_invocations': 0, 'tool_calls': 0}

        # Extract and insert session metadata
        metadata = parser.extract_session_metadata()
        session_id = metadata.get('session_id')

        if not session_id:
            conn.close()
            raise ValueError(f"No session ID found in {file_path}")

        cursor.execute("""
            INSERT OR REPLACE INTO sessions
            (session_id, start_time, end_time, total_messages, total_tokens,
             input_tokens, output_tokens, cache_read_tokens, file_path, file_size, last_scanned_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            metadata.get('start_time'),
            metadata.get('end_time'),
            metadata.get('total_messages'),
            metadata.get('total_tokens'),
            metadata.get('input_tokens'),
            metadata.get('output_tokens'),
            metadata.get('cache_read_tokens'),
            file_path,
            os.path.getsize(file_path),
            datetime.now().isoformat()
        ))

        # Extract and insert agent invocations
        for invocation in parser.extract_agent_invocations():
            cursor.execute("""
                INSERT INTO agent_invocations
                (session_id, agent_name, invoked_at, tool_use_id, tool_result_id,
                 description, prompt_length, success, error_message, response_length)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                invocation.session_id,
                invocation.agent_name,
                invocation.invoked_at,
                invocation.tool_use_id,
                invocation.tool_result_id,
                invocation.description,
                invocation.prompt_length,
                invocation.success,
                invocation.error_message,
                invocation.response_length
            ))
            stats['agent_invocations'] += 1

        # Extract and insert tool usage
        for tool in parser.extract_tool_usage():
            cursor.execute("""
                INSERT INTO tool_usage
                (session_id, tool_name, tool_use_id, tool_result_id,
                 invoked_at, success, error_message, input_size, output_size)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tool.session_id,
                tool.tool_name,
                tool.tool_use_id,
                tool.tool_result_id,
                tool.invoked_at,
                tool.success,
                tool.error_message,
                tool.input_size,
                tool.output_size
            ))
            stats['tool_calls'] += 1

        conn.commit()
        conn.close()

        # Mark file as scanned
        self.incremental.mark_scanned(file_path, session_id)

        return stats

    def _update_agent_metrics(self):
        """Aggregate agent-level metrics from invocations."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Clear existing metrics
        cursor.execute("DELETE FROM agent_metrics")

        # Compute aggregated metrics
        cursor.execute("""
            INSERT INTO agent_metrics
            (agent_name, total_invocations, successful_invocations, failed_invocations,
             total_tokens, avg_response_length, first_seen, last_seen, sessions_participated)
            SELECT
                agent_name,
                COUNT(*) as total_invocations,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_invocations,
                SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failed_invocations,
                0 as total_tokens,  -- TODO: join with sessions for token data
                AVG(response_length) as avg_response_length,
                MIN(invoked_at) as first_seen,
                MAX(invoked_at) as last_seen,
                COUNT(DISTINCT session_id) as sessions_participated
            FROM agent_invocations
            GROUP BY agent_name
        """)

        conn.commit()
        conn.close()

    def agent(self, agent_name: str) -> AgentQuery:
        """Get query interface for specific agent."""
        return AgentQuery(self.db_path, agent_name)

    def all_agents(self) -> List[Dict]:
        """Get all agents with their metrics."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM agent_metrics ORDER BY total_invocations DESC")

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results

    def session(self, session_id: str) -> SessionQuery:
        """Get query interface for specific session."""
        return SessionQuery(self.db_path, session_id)

    def all_sessions(self) -> List[Dict]:
        """Get all sessions with metadata."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sessions ORDER BY start_time DESC")

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
