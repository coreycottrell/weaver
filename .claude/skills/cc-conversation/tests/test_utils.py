#!/usr/bin/env python3
"""
Unit tests for utils module.
"""

import unittest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    extract_wrapped_messages,
    detect_session_switches,
    estimate_message_count
)


class TestUtils(unittest.TestCase):

    def test_estimate_message_count(self):
        """Test message count estimation."""
        # This would require a real JSONL file
        # For now, just verify it doesn't crash
        import tempfile

        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            # Write 16 lines = ~2 messages
            for i in range(16):
                f.write(f'{{"line": {i}}}\n')
            path = f.name

        try:
            count = estimate_message_count(path)
            self.assertGreater(count, 0)
        finally:
            os.unlink(path)


if __name__ == '__main__':
    unittest.main()
