"""
Export conversations to multiple formats.

Supports: JSON, Markdown, HTML, Plain Text
"""

import json
import os
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from datetime import datetime


class Exporter(ABC):
    """Base class for conversation exporters."""

    def __init__(self, include_metadata: bool = True):
        """
        Initialize exporter.

        Args:
            include_metadata: If True, include timestamps, UUIDs, usage stats.
        """
        self.include_metadata = include_metadata

    @abstractmethod
    def format_message(self, message: Dict[str, Any]) -> str:
        """Format a single message."""
        pass

    @abstractmethod
    def format_header(self, messages: List[Dict[str, Any]]) -> str:
        """Format document header."""
        pass

    @abstractmethod
    def format_footer(self, messages: List[Dict[str, Any]]) -> str:
        """Format document footer."""
        pass

    def export(self, messages: List[Dict[str, Any]], output_path: str):
        """
        Export messages to file.

        Args:
            messages: List of parsed messages.
            output_path: Output file path.
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write(self.format_header(messages))

            # Write messages
            for msg in messages:
                f.write(self.format_message(msg))

            # Write footer
            f.write(self.format_footer(messages))


class JSONExporter(Exporter):
    """Export to JSON format."""

    def format_header(self, messages: List[Dict[str, Any]]) -> str:
        return ""

    def format_footer(self, messages: List[Dict[str, Any]]) -> str:
        return ""

    def format_message(self, message: Dict[str, Any]) -> str:
        # Not used for JSON - we export in one go
        pass

    def export(self, messages: List[Dict[str, Any]], output_path: str):
        """Export to JSON (override to write all at once)."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, default=str)


class MarkdownExporter(Exporter):
    """Export to Markdown format."""

    def format_header(self, messages: List[Dict[str, Any]]) -> str:
        if not messages:
            return "# Conversation\n\nNo messages.\n"

        first = messages[0]
        last = messages[-1]

        header = "# Conversation Log\n\n"

        if self.include_metadata:
            header += f"**Session**: `{first.get('session_id', 'unknown')}`\n"
            header += f"**Started**: {first.get('timestamp', 'unknown')}\n"
            header += f"**Ended**: {last.get('timestamp', 'unknown')}\n"
            header += f"**Messages**: {len(messages)}\n"
            header += f"**Project**: `{first.get('cwd', 'unknown')}`\n"
            header += f"**Branch**: `{first.get('git_branch', 'unknown')}`\n"
            header += "\n---\n\n"

        return header

    def format_footer(self, messages: List[Dict[str, Any]]) -> str:
        if self.include_metadata and messages:
            total_input = sum(m.get('usage', {}).get('input_tokens', 0) for m in messages if m.get('usage'))
            total_output = sum(m.get('usage', {}).get('output_tokens', 0) for m in messages if m.get('usage'))

            return f"\n---\n\n**Total Tokens**: {total_input:,} input / {total_output:,} output\n"

        return ""

    def format_message(self, message: Dict[str, Any]) -> str:
        role = message.get('role', 'unknown')
        content = message.get('content', '')
        timestamp = message.get('timestamp', '')

        output = f"\n## {role.title()}"

        if self.include_metadata:
            output += f" `{timestamp}`"
            if message.get('model'):
                output += f" ({message['model']})"

        output += "\n\n"

        # Add content
        if content:
            output += content + "\n"

        # Add tool results if present
        if message.get('tool_results'):
            output += "\n**Tool Results**:\n"
            for tr in message['tool_results']:
                output += f"- `{tr.get('tool_use_id', 'unknown')}`: {tr.get('content', '')[:200]}\n"

        # Add metadata footer
        if self.include_metadata:
            meta_parts = []
            if message.get('uuid'):
                meta_parts.append(f"UUID: `{message['uuid']}`")
            if message.get('usage'):
                usage = message['usage']
                meta_parts.append(f"Tokens: {usage.get('input_tokens', 0)} in / {usage.get('output_tokens', 0)} out")
            if message.get('is_sidechain'):
                meta_parts.append("**[Sidechain]**")

            if meta_parts:
                output += f"\n*{' | '.join(meta_parts)}*\n"

        return output


class HTMLExporter(Exporter):
    """Export to HTML format."""

    def __init__(self, include_metadata: bool = True, style: str = "github"):
        """
        Initialize HTML exporter.

        Args:
            include_metadata: Include timestamps, UUIDs, etc.
            style: CSS style preset ("github", "minimal", "custom").
        """
        super().__init__(include_metadata)
        self.style = style

    def format_header(self, messages: List[Dict[str, Any]]) -> str:
        first = messages[0] if messages else {}

        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conversation Log</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
            color: #24292e;
        }
        .header {
            border-bottom: 1px solid #e1e4e8;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .message {
            margin-bottom: 30px;
            padding: 15px;
            border-left: 3px solid #0366d6;
            background: #f6f8fa;
        }
        .message.user {
            border-left-color: #28a745;
        }
        .message.assistant {
            border-left-color: #0366d6;
        }
        .message-header {
            font-weight: 600;
            margin-bottom: 10px;
            color: #24292e;
        }
        .message-meta {
            font-size: 0.85em;
            color: #586069;
            margin-top: 10px;
        }
        .content {
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .tool-results {
            background: #fff;
            padding: 10px;
            margin-top: 10px;
            border: 1px solid #e1e4e8;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Conversation Log</h1>
"""

        if self.include_metadata:
            html += f"""
        <p>
            <strong>Session:</strong> <code>{first.get('session_id', 'unknown')}</code><br>
            <strong>Project:</strong> <code>{first.get('cwd', 'unknown')}</code><br>
            <strong>Branch:</strong> <code>{first.get('git_branch', 'unknown')}</code><br>
            <strong>Messages:</strong> {len(messages)}
        </p>
"""

        html += "    </div>\n"
        return html

    def format_footer(self, messages: List[Dict[str, Any]]) -> str:
        return "</body>\n</html>\n"

    def format_message(self, message: Dict[str, Any]) -> str:
        role = message.get('role', 'unknown')
        content = message.get('content', '')
        timestamp = message.get('timestamp', '')

        html = f'    <div class="message {role}">\n'
        html += f'        <div class="message-header">{role.title()}'

        if self.include_metadata and message.get('model'):
            html += f' <span style="font-weight:normal;color:#586069;">({message["model"]})</span>'

        html += '</div>\n'

        # Content
        content_safe = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html += f'        <div class="content">{content_safe}</div>\n'

        # Tool results
        if message.get('tool_results'):
            html += '        <div class="tool-results">\n'
            html += '            <strong>Tool Results:</strong><br>\n'
            for tr in message['tool_results']:
                tr_content = str(tr.get('content', ''))[:200].replace('&', '&amp;').replace('<', '&lt;')
                html += f'            <code>{tr.get("tool_use_id", "unknown")}</code>: {tr_content}<br>\n'
            html += '        </div>\n'

        # Metadata
        if self.include_metadata:
            meta_parts = [timestamp]
            if message.get('usage'):
                usage = message['usage']
                meta_parts.append(f"Tokens: {usage.get('input_tokens', 0)} in / {usage.get('output_tokens', 0)} out")

            html += f'        <div class="message-meta">{" | ".join(meta_parts)}</div>\n'

        html += '    </div>\n'
        return html


class TextExporter(Exporter):
    """Export to plain text format."""

    def format_header(self, messages: List[Dict[str, Any]]) -> str:
        if not messages:
            return "CONVERSATION LOG\n\nNo messages.\n"

        header = "=" * 80 + "\n"
        header += "CONVERSATION LOG\n"
        header += "=" * 80 + "\n\n"

        if self.include_metadata and messages:
            first = messages[0]
            header += f"Session:  {first.get('session_id', 'unknown')}\n"
            header += f"Project:  {first.get('cwd', 'unknown')}\n"
            header += f"Branch:   {first.get('git_branch', 'unknown')}\n"
            header += f"Messages: {len(messages)}\n"
            header += "\n" + "-" * 80 + "\n\n"

        return header

    def format_footer(self, messages: List[Dict[str, Any]]) -> str:
        return "\n" + "=" * 80 + "\n"

    def format_message(self, message: Dict[str, Any]) -> str:
        role = message.get('role', 'unknown').upper()
        content = message.get('content', '')
        timestamp = message.get('timestamp', '')

        output = f"[{role}]"

        if self.include_metadata:
            output += f" {timestamp}"

        output += "\n" + "-" * 80 + "\n"
        output += content + "\n\n"

        return output


def export_conversation(
    session_id: Optional[str] = None,
    project_path: Optional[str] = None,
    output_path: Optional[str] = None,
    format: str = "markdown",
    include_metadata: bool = True,
    filter_sidechains: bool = False,
    filter_snapshots: bool = True,
    style: str = "github"
) -> str:
    """
    Export conversation to file.

    Args:
        session_id: Session UUID. If None, uses most recent.
        project_path: Project path. If None, auto-detects.
        output_path: Output file path. If None, auto-generates.
        format: Export format ("json", "markdown", "html", "text").
        include_metadata: Include timestamps, UUIDs, token usage.
        filter_sidechains: Skip sidechain messages.
        filter_snapshots: Skip file-history-snapshot entries.
        style: HTML style preset (for format="html").

    Returns:
        Path to exported file.
    """
    from .parser import read_conversation

    # Read conversation
    messages = read_conversation(
        session_id=session_id,
        project_path=project_path,
        filter_sidechains=filter_sidechains,
        filter_snapshots=filter_snapshots
    )

    # Auto-generate output path if needed
    if not output_path:
        session_id = messages[0]['session_id'] if messages else 'unknown'
        extensions = {'json': 'json', 'markdown': 'md', 'html': 'html', 'text': 'txt'}
        ext = extensions.get(format, 'txt')
        output_path = f"/tmp/conversation_{session_id}.{ext}"

    # Choose exporter
    if format == "json":
        exporter = JSONExporter(include_metadata=include_metadata)
    elif format == "markdown":
        exporter = MarkdownExporter(include_metadata=include_metadata)
    elif format == "html":
        exporter = HTMLExporter(include_metadata=include_metadata, style=style)
    elif format == "text":
        exporter = TextExporter(include_metadata=include_metadata)
    else:
        raise ValueError(f"Unknown format: {format}")

    # Export
    exporter.export(messages, output_path)

    return output_path
