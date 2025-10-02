#!/usr/bin/env python3
"""
Flow Execution Dashboard Updater

Helper script to update flow test results after experiments.
Simplifies the process of recording test outcomes.

Usage:
    # Record a successful test
    python update_dashboard.py parallel-research \
        --status success \
        --duration 90 \
        --quality 9.5 \
        --scenario "Research AI communication protocols" \
        --notes "Excellent multi-perspective synthesis"

    # Record a failed test
    python update_dashboard.py emergency-response \
        --status failed \
        --duration 45 \
        --notes "Response too slow, needs optimization"

    # Mark flow as validated
    python update_dashboard.py specialist-consultation \
        --validate \
        --quality 8.5

    # Add strengths and improvements
    python update_dashboard.py parallel-research \
        --add-strength "Fast parallel execution" \
        --add-improvement "Need better synthesis"
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List


class DashboardUpdater:
    """Update flow dashboard with test results"""

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

    def _save_dashboard(self):
        """Save dashboard data to JSON file"""
        self.data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')

        with open(self.dashboard_path, 'w') as f:
            json.dump(self.data, f, indent=2)

        print(f"✅ Dashboard updated: {self.dashboard_path}")

    def record_test(
        self,
        flow_name: str,
        status: str,
        duration: int,
        quality_score: Optional[float] = None,
        scenario: str = "",
        notes: str = "",
        tester: str = "The Conductor"
    ):
        """Record a test execution"""

        if flow_name not in self.data['flows']:
            print(f"❌ Flow not found: {flow_name}")
            print(f"Available flows: {', '.join(self.data['flows'].keys())}")
            sys.exit(1)

        flow = self.data['flows'][flow_name]

        # Update test count
        flow['tests_run'] += 1

        # Update success/failure counts
        if status == 'success':
            flow['success_count'] += 1
        else:
            flow['failure_count'] += 1

        # Update success rate
        flow['success_rate'] = flow['success_count'] / flow['tests_run']

        # Update timing stats
        if flow['avg_time_seconds'] is None:
            flow['avg_time_seconds'] = duration
            flow['min_time_seconds'] = duration
            flow['max_time_seconds'] = duration
        else:
            # Update average
            total_time = flow['avg_time_seconds'] * (flow['tests_run'] - 1)
            flow['avg_time_seconds'] = int((total_time + duration) / flow['tests_run'])

            # Update min/max
            flow['min_time_seconds'] = min(flow['min_time_seconds'], duration)
            flow['max_time_seconds'] = max(flow['max_time_seconds'], duration)

        # Update quality score (running average)
        if quality_score is not None:
            if flow['quality_score'] is None:
                flow['quality_score'] = quality_score
            else:
                total_quality = flow['quality_score'] * (flow['tests_run'] - 1)
                flow['quality_score'] = round((total_quality + quality_score) / flow['tests_run'], 1)

        # Update last run date
        flow['last_run'] = datetime.now().strftime('%Y-%m-%d')

        # Update status if first test
        if flow['status'] == 'untested':
            flow['status'] = 'tested'

        # Add to notes if provided
        if notes:
            if flow['notes'] and not flow['notes'].endswith('.'):
                flow['notes'] += '. '
            flow['notes'] += notes

        # Add test scenario to list
        if scenario:
            if 'test_scenarios' not in flow:
                flow['test_scenarios'] = []
            flow['test_scenarios'].append(f"{scenario} - {status.title()}")

        # Add to test history
        history_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'flow': flow_name,
            'status': status,
            'duration_seconds': duration,
            'quality_score': quality_score,
            'scenario': scenario,
            'notes': notes,
            'tester': tester
        }

        if 'test_history' not in self.data:
            self.data['test_history'] = []
        self.data['test_history'].append(history_entry)

        # Update metadata
        tested_count = sum(1 for f in self.data['flows'].values() if f['status'] != 'untested')
        validated_count = sum(1 for f in self.data['flows'].values() if f['status'] == 'validated')
        self.data['metadata']['flows_tested'] = tested_count
        self.data['metadata']['flows_validated'] = validated_count

        self._save_dashboard()

        print(f"\n✅ Test recorded for: {flow_name}")
        print(f"   Status: {status}")
        print(f"   Duration: {duration}s")
        if quality_score:
            print(f"   Quality: {quality_score}/10")
        print(f"   Tests Run: {flow['tests_run']}")
        print(f"   Success Rate: {flow['success_rate']*100:.1f}%")

    def validate_flow(self, flow_name: str, quality_score: Optional[float] = None):
        """Mark a flow as validated"""

        if flow_name not in self.data['flows']:
            print(f"❌ Flow not found: {flow_name}")
            sys.exit(1)

        flow = self.data['flows'][flow_name]
        flow['status'] = 'validated'

        if quality_score is not None:
            flow['quality_score'] = quality_score

        # Update metadata
        validated_count = sum(1 for f in self.data['flows'].values() if f['status'] == 'validated')
        self.data['metadata']['flows_validated'] = validated_count

        self._save_dashboard()

        print(f"✅ Flow validated: {flow_name}")

    def add_strength(self, flow_name: str, strength: str):
        """Add a strength to a flow"""

        if flow_name not in self.data['flows']:
            print(f"❌ Flow not found: {flow_name}")
            sys.exit(1)

        flow = self.data['flows'][flow_name]

        if 'strengths' not in flow:
            flow['strengths'] = []

        flow['strengths'].append(strength)

        self._save_dashboard()

        print(f"✅ Strength added to {flow_name}: {strength}")

    def add_improvement(self, flow_name: str, improvement: str):
        """Add an area for improvement to a flow"""

        if flow_name not in self.data['flows']:
            print(f"❌ Flow not found: {flow_name}")
            sys.exit(1)

        flow = self.data['flows'][flow_name]

        if 'areas_for_improvement' not in flow:
            flow['areas_for_improvement'] = []

        flow['areas_for_improvement'].append(improvement)

        self._save_dashboard()

        print(f"✅ Improvement area added to {flow_name}: {improvement}")

    def update_next_test(self, flow_name: str, next_test: str):
        """Update the next test action for a flow"""

        if flow_name not in self.data['flows']:
            print(f"❌ Flow not found: {flow_name}")
            sys.exit(1)

        flow = self.data['flows'][flow_name]
        flow['next_test'] = next_test

        self._save_dashboard()

        print(f"✅ Next test updated for {flow_name}: {next_test}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Update AI-CIV Flow Execution Dashboard',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'flow',
        type=str,
        help='Flow name to update'
    )
    parser.add_argument(
        '--status',
        choices=['success', 'failed'],
        help='Test status (success or failed)'
    )
    parser.add_argument(
        '--duration',
        type=int,
        help='Test duration in seconds'
    )
    parser.add_argument(
        '--quality',
        type=float,
        help='Quality score (0-10)'
    )
    parser.add_argument(
        '--scenario',
        type=str,
        default='',
        help='Test scenario description'
    )
    parser.add_argument(
        '--notes',
        type=str,
        default='',
        help='Additional notes'
    )
    parser.add_argument(
        '--tester',
        type=str,
        default='The Conductor',
        help='Who ran the test'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Mark flow as validated'
    )
    parser.add_argument(
        '--add-strength',
        type=str,
        help='Add a strength to the flow'
    )
    parser.add_argument(
        '--add-improvement',
        type=str,
        help='Add an area for improvement'
    )
    parser.add_argument(
        '--next-test',
        type=str,
        help='Update next test action'
    )
    parser.add_argument(
        '--dashboard',
        type=str,
        default='flow_dashboard.json',
        help='Path to dashboard JSON file'
    )

    args = parser.parse_args()

    updater = DashboardUpdater(args.dashboard)

    if args.validate:
        updater.validate_flow(args.flow, args.quality)

    if args.status and args.duration is not None:
        updater.record_test(
            args.flow,
            args.status,
            args.duration,
            args.quality,
            args.scenario,
            args.notes,
            args.tester
        )

    if args.add_strength:
        updater.add_strength(args.flow, args.add_strength)

    if args.add_improvement:
        updater.add_improvement(args.flow, args.add_improvement)

    if args.next_test:
        updater.update_next_test(args.flow, args.next_test)

    if not any([args.status, args.validate, args.add_strength, args.add_improvement, args.next_test]):
        parser.print_help()
        print("\n❌ No action specified. Use --status, --validate, --add-strength, --add-improvement, or --next-test")


if __name__ == '__main__':
    main()
