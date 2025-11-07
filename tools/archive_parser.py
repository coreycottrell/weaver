"""
JSONL Archive Parser
Extracts agent invocations and tool usage from session JSONL logs.
"""

import json
from typing import Iterator, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AgentInvocation:
    """Represents a single agent invocation from Task tool."""
    session_id: str
    agent_name: str
    invoked_at: str
    tool_use_id: str
    description: Optional[str]
    prompt_length: int
    tool_result_id: Optional[str] = None
    success: Optional[bool] = None
    error_message: Optional[str] = None
    response_length: Optional[int] = None


@dataclass
class ToolUsage:
    """Represents a single tool call."""
    session_id: str
    tool_name: str
    tool_use_id: str
    invoked_at: str
    tool_result_id: Optional[str] = None
    success: Optional[bool] = None
    error_message: Optional[str] = None
    input_size: Optional[int] = None
    output_size: Optional[int] = None


class JSONLParser:
    """Parses session JSONL files to extract structured data."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.session_id = None
        self.tool_results = {}  # Map tool_use_id -> result data

    def parse_session(self) -> Iterator[Dict]:
        """Parse JSONL file line by line, yielding structured records."""
        with open(self.file_path, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    yield data
                except json.JSONDecodeError:
                    continue

    def extract_session_metadata(self) -> Dict[str, Any]:
        """Extract session-level metadata."""
        total_messages = 0
        total_tokens = 0
        input_tokens = 0
        output_tokens = 0
        cache_read_tokens = 0
        start_time = None
        end_time = None
        session_id = None

        for record in self.parse_session():
            # Extract session ID from any record
            if 'sessionId' in record and not session_id:
                session_id = record['sessionId']

            # Track timestamps
            timestamp = record.get('timestamp')
            if timestamp:
                if not start_time or timestamp < start_time:
                    start_time = timestamp
                if not end_time or timestamp > end_time:
                    end_time = timestamp

            # Count messages
            if record.get('type') in ['user', 'assistant']:
                total_messages += 1

            # Aggregate token usage
            if 'message' in record and 'usage' in record['message']:
                usage = record['message']['usage']
                input_tokens += usage.get('input_tokens', 0)
                output_tokens += usage.get('output_tokens', 0)
                cache_read_tokens += usage.get('cache_read_input_tokens', 0)
                total_tokens += (usage.get('input_tokens', 0) +
                               usage.get('output_tokens', 0))

        return {
            'session_id': session_id,
            'start_time': start_time,
            'end_time': end_time,
            'total_messages': total_messages,
            'total_tokens': total_tokens,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'cache_read_tokens': cache_read_tokens
        }

    def extract_agent_invocations(self) -> Iterator[AgentInvocation]:
        """Extract agent invocations from Task tool calls."""
        # First pass: collect all tool results
        tool_results = {}
        for record in self.parse_session():
            if record.get('type') == 'tool_result':
                tool_use_id = record.get('tool_use_id')
                if tool_use_id:
                    tool_results[tool_use_id] = record

        # Second pass: extract Task tool calls and match with results
        for record in self.parse_session():
            if record.get('type') != 'assistant':
                continue

            session_id = record.get('sessionId')
            timestamp = record.get('timestamp')

            message = record.get('message', {})
            content = message.get('content', [])

            for item in content:
                if item.get('type') != 'tool_use':
                    continue
                if item.get('name') != 'Task':
                    continue

                tool_use_id = item.get('id')
                input_data = item.get('input', {})
                agent_name = input_data.get('subagent_type', 'unknown')
                description = input_data.get('description', '')
                prompt = input_data.get('prompt', '')

                # Match with tool result
                result = tool_results.get(tool_use_id)
                tool_result_id = None
                success = None
                error_message = None
                response_length = None

                if result:
                    tool_result_id = result.get('id')
                    is_error = result.get('is_error', False)
                    success = not is_error

                    if is_error:
                        error_message = result.get('content', '')
                    else:
                        content_data = result.get('content', '')
                        response_length = len(str(content_data))

                yield AgentInvocation(
                    session_id=session_id,
                    agent_name=agent_name,
                    invoked_at=timestamp,
                    tool_use_id=tool_use_id,
                    description=description,
                    prompt_length=len(prompt),
                    tool_result_id=tool_result_id,
                    success=success,
                    error_message=error_message,
                    response_length=response_length
                )

    def extract_tool_usage(self) -> Iterator[ToolUsage]:
        """Extract all tool usage (not just Task)."""
        # First pass: collect all tool results
        tool_results = {}
        for record in self.parse_session():
            if record.get('type') == 'tool_result':
                tool_use_id = record.get('tool_use_id')
                if tool_use_id:
                    tool_results[tool_use_id] = record

        # Second pass: extract tool calls and match with results
        for record in self.parse_session():
            if record.get('type') != 'assistant':
                continue

            session_id = record.get('sessionId')
            timestamp = record.get('timestamp')

            message = record.get('message', {})
            content = message.get('content', [])

            for item in content:
                if item.get('type') != 'tool_use':
                    continue

                tool_use_id = item.get('id')
                tool_name = item.get('name')
                input_data = item.get('input', {})

                # Match with tool result
                result = tool_results.get(tool_use_id)
                tool_result_id = None
                success = None
                error_message = None
                output_size = None

                if result:
                    tool_result_id = result.get('id')
                    is_error = result.get('is_error', False)
                    success = not is_error

                    if is_error:
                        error_message = result.get('content', '')
                    else:
                        content_data = result.get('content', '')
                        output_size = len(str(content_data))

                yield ToolUsage(
                    session_id=session_id,
                    tool_name=tool_name,
                    tool_use_id=tool_use_id,
                    invoked_at=timestamp,
                    tool_result_id=tool_result_id,
                    success=success,
                    error_message=error_message,
                    input_size=len(str(input_data)),
                    output_size=output_size
                )
