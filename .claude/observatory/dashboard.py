#!/usr/bin/env python3
"""
Collective Observatory - Terminal Dashboard
Real-time visualization of agent deployments
"""

import sys
import time
from datetime import datetime
from typing import Optional, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich import box

# Import state management
from observatory import (
    load_state,
    get_active_deployment,
    get_deployment_history,
    get_stats
)


def format_timestamp(iso_timestamp: Optional[str]) -> str:
    """Format ISO timestamp to human-readable string"""
    if not iso_timestamp:
        return "N/A"

    try:
        dt = datetime.fromisoformat(iso_timestamp)
        now = datetime.now()
        delta = now - dt

        # Less than 1 minute
        if delta.total_seconds() < 60:
            return f"{int(delta.total_seconds())}s ago"

        # Less than 1 hour
        if delta.total_seconds() < 3600:
            return f"{int(delta.total_seconds() / 60)}m ago"

        # Less than 24 hours
        if delta.total_seconds() < 86400:
            return f"{int(delta.total_seconds() / 3600)}h ago"

        # Format as date
        return dt.strftime("%Y-%m-%d %H:%M")

    except Exception:
        return iso_timestamp


def get_status_icon(status: str) -> str:
    """Get emoji/symbol for status"""
    icons = {
        'working': '⟳',
        'completed': '✓',
        'failed': '✗',
        'pending': '○',
        'active': '▶'
    }
    return icons.get(status, '?')


def render_progress_bar(progress: int, width: int = 20) -> str:
    """Render ASCII progress bar"""
    if progress < 0:
        progress = 0
    if progress > 100:
        progress = 100

    filled = int(progress / 100 * width)
    empty = width - filled

    return f"[{'█' * filled}{'░' * empty}] {progress}%"


def render_header(stats: Dict[str, int]) -> Panel:
    """Render dashboard header"""
    header_text = Text()
    header_text.append("AI-CIV Collective Observatory\n", style="bold cyan")
    header_text.append(f"Total Deployments: {stats.get('totalDeployments', 0)} | ", style="dim")
    header_text.append(f"Agents Deployed: {stats.get('totalAgentsDeployed', 0)} | ", style="dim")
    header_text.append(f"Findings: {stats.get('totalFindings', 0)}", style="dim")

    return Panel(header_text, box=box.ROUNDED, border_style="cyan")


def render_active_deployment(deployment: Optional[Dict[str, Any]]) -> Panel:
    """Render current active deployment"""
    if not deployment:
        empty_text = Text("No active deployments", style="dim italic")
        return Panel(empty_text, title="Active Deployment", box=box.ROUNDED, border_style="yellow")

    # Create content
    content = Text()
    content.append(f"Task: ", style="bold")
    content.append(f"{deployment['task']}\n", style="white")
    content.append(f"Started: ", style="bold")
    content.append(f"{format_timestamp(deployment['startTime'])}\n\n", style="dim")

    # Agent table
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold magenta")
    table.add_column("Agent", style="cyan", no_wrap=True)
    table.add_column("Status", style="magenta", width=12)
    table.add_column("Progress", width=28)
    table.add_column("Activity", style="yellow")

    for agent in deployment.get('agents', []):
        status_icon = get_status_icon(agent.get('status', 'pending'))
        status_text = f"{status_icon} {agent.get('status', 'unknown')}"
        progress_bar = render_progress_bar(agent.get('progress', 0))
        activity = agent.get('currentActivity', 'Waiting...')

        # Truncate activity if too long
        if len(activity) > 40:
            activity = activity[:37] + "..."

        table.add_row(
            agent['name'],
            status_text,
            progress_bar,
            activity
        )

    return Panel(table, title=f"[bold]Active Deployment - {deployment['id']}[/bold]", box=box.ROUNDED, border_style="green")


def render_history(history: list, limit: int = 5) -> Panel:
    """Render deployment history"""
    if not history:
        empty_text = Text("No deployment history", style="dim italic")
        return Panel(empty_text, title="Recent History", box=box.ROUNDED, border_style="blue")

    table = Table(box=box.SIMPLE, show_header=True, header_style="bold blue")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Task", style="white")
    table.add_column("Agents", style="magenta", justify="center")
    table.add_column("Status", style="green", width=12)
    table.add_column("Completed", style="dim")

    for dep in history[:limit]:
        dep_id = dep.get('id', 'unknown')
        task = dep.get('task', 'N/A')
        agent_count = len(dep.get('agents', []))
        status_icon = get_status_icon(dep.get('status', 'unknown'))
        status = f"{status_icon} {dep.get('status', 'unknown')}"
        completed = format_timestamp(dep.get('completedAt'))

        # Truncate task if too long
        if len(task) > 50:
            task = task[:47] + "..."

        table.add_row(
            dep_id,
            task,
            str(agent_count),
            status,
            completed
        )

    return Panel(table, title="Recent Deployment History", box=box.ROUNDED, border_style="blue")


def render_footer() -> Panel:
    """Render dashboard footer"""
    footer_text = Text()
    footer_text.append("Press ", style="dim")
    footer_text.append("Ctrl+C", style="bold yellow")
    footer_text.append(" to exit | Updates every 1s", style="dim")

    return Panel(footer_text, box=box.ROUNDED, border_style="dim")


def render_dashboard() -> Layout:
    """Render complete dashboard layout"""
    state = load_state()
    stats = get_stats()
    active = get_active_deployment()
    history = get_deployment_history(limit=5)

    layout = Layout()

    layout.split_column(
        Layout(render_header(stats), size=5),
        Layout(render_active_deployment(active), size=15),
        Layout(render_history(history), size=12),
        Layout(render_footer(), size=3)
    )

    return layout


def launch_dashboard():
    """Launch live dashboard with auto-refresh"""
    console = Console()

    try:
        with Live(render_dashboard(), console=console, refresh_per_second=1, screen=False) as live:
            while True:
                live.update(render_dashboard())
                time.sleep(1)

    except KeyboardInterrupt:
        console.print("\n[dim]Observatory closed.[/dim]")
        sys.exit(0)


if __name__ == "__main__":
    launch_dashboard()
