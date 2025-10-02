#!/usr/bin/env python3
"""
Flow Execution Dashboard Viewer

Simple CLI tool to view the status of all AI-CIV coordination flows.
Provides multiple views: summary, detailed, by-category, and history.

Usage:
    python view_dashboard.py              # Summary view
    python view_dashboard.py --detailed   # Detailed view
    python view_dashboard.py --category governance  # Filter by category
    python view_dashboard.py --history    # Test history
    python view_dashboard.py --untested   # Show only untested flows
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class FlowDashboard:
    """Flow execution dashboard viewer"""

    def __init__(self, dashboard_path: str = "flow_dashboard.json"):
        self.dashboard_path = Path(dashboard_path)
        self.data = self._load_dashboard()

    def _load_dashboard(self) -> dict:
        """Load dashboard data from JSON file"""
        if not self.dashboard_path.exists():
            print(f"❌ Dashboard file not found: {self.dashboard_path}")
            sys.exit(1)

        with open(self.dashboard_path, 'r') as f:
            return json.load(f)

    def _get_status_emoji(self, status: str) -> str:
        """Get emoji for flow status"""
        status_map = {
            'validated': '✅',
            'tested': '🧪',
            'untested': '⚪',
            'failed': '❌',
            'in-progress': '🔄'
        }
        return status_map.get(status, '❓')

    def _get_complexity_emoji(self, complexity: str) -> str:
        """Get emoji for complexity level"""
        complexity_map = {
            'low': '🟢',
            'medium': '🟡',
            'high': '🔴'
        }
        return complexity_map.get(complexity, '⚪')

    def print_summary(self):
        """Print summary overview of all flows"""
        meta = self.data['metadata']
        flows = self.data['flows']

        print("\n" + "="*70)
        print("🎯 AI-CIV Flow Execution Dashboard")
        print("="*70)

        print(f"\n📊 Overview:")
        print(f"   Total Flows: {meta['total_flows']}")
        print(f"   Tested: {meta['flows_tested']}")
        print(f"   Validated: {meta['flows_validated']}")
        print(f"   Untested: {meta['total_flows'] - meta['flows_tested']}")
        print(f"   Last Updated: {meta['last_updated']}")

        # Status breakdown
        status_counts = {}
        for flow_data in flows.values():
            status = flow_data['status']
            status_counts[status] = status_counts.get(status, 0) + 1

        print(f"\n📈 Status Breakdown:")
        for status, count in sorted(status_counts.items()):
            emoji = self._get_status_emoji(status)
            print(f"   {emoji} {status.title()}: {count}")

        # Category breakdown
        print(f"\n🏷️  Categories:")
        categories = self.data['categories']
        for cat_name, cat_data in categories.items():
            flow_count = len(cat_data['flows'])
            print(f"   • {cat_name.title()}: {flow_count} flows - {cat_data['description']}")

        print("\n" + "="*70)
        print("\n💡 Tip: Use --detailed for full flow information")
        print("         Use --category <name> to filter by category")
        print("         Use --untested to see flows needing testing\n")

    def print_detailed(self, category: Optional[str] = None, untested_only: bool = False):
        """Print detailed view of flows"""
        flows = self.data['flows']

        # Filter by category if specified
        if category:
            cat_flows = self.data['categories'].get(category, {}).get('flows', [])
            flows = {k: v for k, v in flows.items() if k in cat_flows}
            if not flows:
                print(f"❌ No flows found in category: {category}")
                return

        # Filter untested if specified
        if untested_only:
            flows = {k: v for k, v in flows.items() if v['status'] == 'untested'}

        print("\n" + "="*70)
        if category:
            print(f"📋 Flows in Category: {category.title()}")
        elif untested_only:
            print("📋 Untested Flows")
        else:
            print("📋 All Flows - Detailed View")
        print("="*70)

        for flow_name, flow_data in flows.items():
            self._print_flow_detail(flow_name, flow_data)

        print("="*70 + "\n")

    def _print_flow_detail(self, flow_name: str, flow_data: dict):
        """Print detailed information for a single flow"""
        status_emoji = self._get_status_emoji(flow_data['status'])
        complexity_emoji = self._get_complexity_emoji(flow_data['complexity'])

        print(f"\n{status_emoji} {flow_name.upper().replace('-', ' ')}")
        print(f"   ID: {flow_data['id']} | Category: {flow_data['category']} | Complexity: {complexity_emoji} {flow_data['complexity']}")
        print(f"   Status: {flow_data['status'].title()}")
        print(f"   Agents Involved: {flow_data['agents_involved']}")

        if flow_data['tests_run'] > 0:
            print(f"\n   📊 Test Statistics:")
            print(f"      Tests Run: {flow_data['tests_run']}")
            print(f"      Success Rate: {flow_data['success_rate']*100:.1f}%")
            print(f"      Avg Time: {flow_data['avg_time_seconds']}s")
            if flow_data['quality_score']:
                print(f"      Quality Score: {flow_data['quality_score']}/10")
            print(f"      Last Run: {flow_data['last_run']}")

        print(f"\n   📝 Notes: {flow_data['notes']}")

        if flow_data['status'] == 'validated' and flow_data.get('strengths'):
            print(f"\n   ✨ Strengths:")
            for strength in flow_data['strengths']:
                print(f"      • {strength}")

        if flow_data.get('areas_for_improvement'):
            print(f"\n   🔧 Areas for Improvement:")
            for area in flow_data['areas_for_improvement']:
                print(f"      • {area}")

        if flow_data.get('planned_test'):
            print(f"\n   🎯 Planned Test: {flow_data['planned_test']}")

        if flow_data.get('next_test'):
            print(f"   ⏭️  Next Action: {flow_data['next_test']}")

        print()

    def print_history(self):
        """Print test execution history"""
        history = self.data.get('test_history', [])

        print("\n" + "="*70)
        print("📜 Test Execution History")
        print("="*70)

        if not history:
            print("\n   No tests executed yet.\n")
            return

        for i, test in enumerate(history, 1):
            status_emoji = '✅' if test['status'] == 'success' else '❌'
            print(f"\n{i}. {status_emoji} {test['flow'].upper().replace('-', ' ')}")
            print(f"   Date: {test['date']}")
            print(f"   Duration: {test['duration_seconds']}s")
            print(f"   Quality Score: {test.get('quality_score', 'N/A')}")
            print(f"   Scenario: {test['scenario']}")
            print(f"   Tester: {test['tester']}")
            print(f"   Notes: {test['notes']}")

        print("\n" + "="*70 + "\n")

    def print_by_category(self):
        """Print flows organized by category"""
        categories = self.data['categories']
        flows = self.data['flows']

        print("\n" + "="*70)
        print("🏷️  Flows by Category")
        print("="*70)

        for cat_name, cat_data in categories.items():
            print(f"\n📁 {cat_name.upper()}")
            print(f"   {cat_data['description']}")
            print()

            for flow_name in cat_data['flows']:
                flow_data = flows[flow_name]
                status_emoji = self._get_status_emoji(flow_data['status'])
                complexity_emoji = self._get_complexity_emoji(flow_data['complexity'])

                print(f"   {status_emoji} {flow_name}")
                print(f"      {complexity_emoji} {flow_data['complexity']} complexity | {flow_data['agents_involved']} agents")

                if flow_data['tests_run'] > 0:
                    print(f"      ✓ Tested {flow_data['tests_run']}x | Success: {flow_data['success_rate']*100:.0f}% | Quality: {flow_data['quality_score']}/10")
                else:
                    print(f"      ⚪ Not yet tested")
                print()

        print("="*70 + "\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='View AI-CIV Flow Execution Dashboard',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--detailed', '-d',
        action='store_true',
        help='Show detailed view of all flows'
    )
    parser.add_argument(
        '--category', '-c',
        type=str,
        help='Filter by category (governance, research, quality, etc.)'
    )
    parser.add_argument(
        '--history', '-H',
        action='store_true',
        help='Show test execution history'
    )
    parser.add_argument(
        '--untested', '-u',
        action='store_true',
        help='Show only untested flows'
    )
    parser.add_argument(
        '--by-category',
        action='store_true',
        help='Organize view by category'
    )
    parser.add_argument(
        '--dashboard',
        type=str,
        default='flow_dashboard.json',
        help='Path to dashboard JSON file (default: flow_dashboard.json)'
    )

    args = parser.parse_args()

    dashboard = FlowDashboard(args.dashboard)

    if args.history:
        dashboard.print_history()
    elif args.by_category:
        dashboard.print_by_category()
    elif args.detailed or args.category or args.untested:
        dashboard.print_detailed(category=args.category, untested_only=args.untested)
    else:
        dashboard.print_summary()


if __name__ == '__main__':
    main()
