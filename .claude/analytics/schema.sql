-- Archive Scanner Database Schema
-- Created: 2025-10-29
-- Purpose: Track agent invocations, tool usage, and session metrics from JSONL logs

-- Session-level metadata
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    start_time TEXT,
    end_time TEXT,
    total_messages INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    cache_read_tokens INTEGER DEFAULT 0,
    file_path TEXT NOT NULL,
    file_size INTEGER,
    last_scanned_at TEXT,
    UNIQUE(session_id)
);

-- Agent invocation tracking (from Task tool calls)
CREATE TABLE IF NOT EXISTS agent_invocations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    invoked_at TEXT,
    tool_use_id TEXT,
    tool_result_id TEXT,
    description TEXT,
    prompt_length INTEGER,
    success BOOLEAN,
    error_message TEXT,
    response_length INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- Tool usage tracking (all tool calls)
CREATE TABLE IF NOT EXISTS tool_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    tool_use_id TEXT,
    tool_result_id TEXT,
    invoked_at TEXT,
    success BOOLEAN,
    error_message TEXT,
    input_size INTEGER,
    output_size INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- Agent-level aggregated metrics
CREATE TABLE IF NOT EXISTS agent_metrics (
    agent_name TEXT PRIMARY KEY,
    total_invocations INTEGER DEFAULT 0,
    successful_invocations INTEGER DEFAULT 0,
    failed_invocations INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    avg_response_length INTEGER DEFAULT 0,
    first_seen TEXT,
    last_seen TEXT,
    sessions_participated INTEGER DEFAULT 0
);

-- Incremental scan state tracking
CREATE TABLE IF NOT EXISTS scan_state (
    file_path TEXT PRIMARY KEY,
    last_modified_time REAL,
    last_scanned_at TEXT,
    file_size INTEGER,
    session_id TEXT
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_agent_invocations_session ON agent_invocations(session_id);
CREATE INDEX IF NOT EXISTS idx_agent_invocations_agent ON agent_invocations(agent_name);
CREATE INDEX IF NOT EXISTS idx_agent_invocations_time ON agent_invocations(invoked_at);
CREATE INDEX IF NOT EXISTS idx_tool_usage_session ON tool_usage(session_id);
CREATE INDEX IF NOT EXISTS idx_tool_usage_tool ON tool_usage(tool_name);
CREATE INDEX IF NOT EXISTS idx_tool_usage_time ON tool_usage(invoked_at);
CREATE INDEX IF NOT EXISTS idx_sessions_time ON sessions(start_time);
