#!/usr/bin/env python3
"""
Unit tests for parser module.
"""

import unittest
import tempfile
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser import (
    aggregate_messages,
    merge_message_lines,
    parse_message,
    filter_sidechains,
    build_conversation_tree
)


class TestParser(unittest.TestCase):

    def test_merge_single_line(self):
        """Test merging a single-line message."""
        lines = [{'uuid': 'test-123', 'content': 'Hello'}]
        merged = merge_message_lines(lines)

        self.assertEqual(merged['uuid'], 'test-123')
        self.assertEqual(merged['content'], 'Hello')

    def test_merge_multiple_lines(self):
        """Test merging multi-line streaming message."""
        lines = [
            {'uuid': 'test-123', 'content': 'Part 1'},
            {'uuid': 'test-123', 'content': 'Part 2', 'extra': 'data'},
            {'uuid': 'test-123', 'usage': {'tokens': 100}}
        ]

        merged = merge_message_lines(lines)

        self.assertEqual(merged['uuid'], 'test-123')
        self.assertEqual(merged['content'], 'Part 2')  # Last value wins
        self.assertEqual(merged['extra'], 'data')
        self.assertEqual(merged['usage']['tokens'], 100)

    def test_aggregate_messages(self):
        """Test aggregating JSONL file with multiple messages."""
        # Create temp JSONL file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            # Message 1 (2 lines)
            json.dump({'uuid': 'msg-1', 'type': 'user', 'content': 'Hello'}, f)
            f.write('\n')
            json.dump({'uuid': 'msg-1', 'message': {'role': 'user'}}, f)
            f.write('\n')

            # Message 2 (1 line)
            json.dump({'uuid': 'msg-2', 'type': 'assistant', 'content': 'Hi'}, f)
            f.write('\n')

            jsonl_path = f.name

        try:
            messages = aggregate_messages(jsonl_path)

            self.assertEqual(len(messages), 2)
            self.assertEqual(messages[0]['uuid'], 'msg-1')
            self.assertEqual(messages[1]['uuid'], 'msg-2')
        finally:
            os.unlink(jsonl_path)

    def test_parse_user_message(self):
        """Test parsing user message."""
        raw = {
            'uuid': 'test-uuid',
            'type': 'user',
            'timestamp': '2025-10-20T10:00:00Z',
            'parentUuid': 'parent-uuid',
            'isSidechain': False,
            'sessionId': 'session-123',
            'message': {
                'role': 'user',
                'content': 'Test message'
            }
        }

        parsed = parse_message(raw)

        self.assertEqual(parsed['uuid'], 'test-uuid')
        self.assertEqual(parsed['type'], 'user')
        self.assertEqual(parsed['role'], 'user')
        self.assertEqual(parsed['content'], 'Test message')
        self.assertEqual(parsed['parent_uuid'], 'parent-uuid')
        self.assertFalse(parsed['is_sidechain'])

    def test_parse_assistant_message(self):
        """Test parsing assistant message with text blocks."""
        raw = {
            'uuid': 'test-uuid',
            'type': 'assistant',
            'timestamp': '2025-10-20T10:00:00Z',
            'message': {
                'role': 'assistant',
                'model': 'claude-sonnet-4-5',
                'content': [
                    {'type': 'text', 'text': 'Response here'},
                    {'type': 'text', 'text': 'More text'}
                ],
                'usage': {
                    'input_tokens': 100,
                    'output_tokens': 50
                }
            }
        }

        parsed = parse_message(raw)

        self.assertEqual(parsed['role'], 'assistant')
        self.assertEqual(parsed['content'], 'Response here\nMore text')
        self.assertEqual(parsed['model'], 'claude-sonnet-4-5')
        self.assertEqual(parsed['usage']['input_tokens'], 100)

    def test_filter_sidechains(self):
        """Test filtering sidechain messages."""
        messages = [
            {'uuid': '1', 'is_sidechain': False, 'content': 'Main'},
            {'uuid': '2', 'is_sidechain': True, 'content': 'Sidechain'},
            {'uuid': '3', 'is_sidechain': False, 'content': 'Main 2'},
        ]

        filtered = filter_sidechains(messages, include=False)

        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]['uuid'], '1')
        self.assertEqual(filtered[1]['uuid'], '3')

    def test_build_conversation_tree(self):
        """Test building parent-child relationships."""
        messages = [
            {'uuid': 'root', 'parent_uuid': None},
            {'uuid': 'child-1', 'parent_uuid': 'root'},
            {'uuid': 'child-2', 'parent_uuid': 'root'},
            {'uuid': 'grandchild', 'parent_uuid': 'child-1'},
        ]

        roots = build_conversation_tree(messages)

        self.assertEqual(len(roots), 1)
        self.assertEqual(roots[0]['uuid'], 'root')
        self.assertEqual(len(roots[0]['children']), 2)

        # Check grandchild is under child-1
        child_1 = roots[0]['children'][0]
        if child_1['uuid'] == 'child-1':
            self.assertEqual(len(child_1['children']), 1)
            self.assertEqual(child_1['children'][0]['uuid'], 'grandchild')


if __name__ == '__main__':
    unittest.main()
