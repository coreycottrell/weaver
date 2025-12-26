#!/usr/bin/env python3
"""
WebSocket Connection Monitor

Real-time monitoring of WebSocket server connections.
Displays active connections, room subscriptions, and message rates.

Usage:
    python ws_monitor.py --stats-url http://localhost:8000/ws/stats --refresh 2

Requirements:
    pip install httpx rich

Author: AI-CIV capability-curator
Version: 1.0.0
Date: 2025-12-26
"""

import argparse
import asyncio
from datetime import datetime
from typing import Optional

try:
    import httpx
except ImportError:
    print("Please install httpx: pip install httpx")
    exit(1)

try:
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    from rich.layout import Layout
except ImportError:
    print("Please install rich: pip install rich")
    exit(1)


class WebSocketMonitor:
    """Monitor WebSocket server statistics."""

    def __init__(self, stats_url: str, refresh_interval: float = 2.0):
        self.stats_url = stats_url
        self.refresh_interval = refresh_interval
        self.console = Console()
        self._running = False
        self._previous_stats: Optional[dict] = None
        self._previous_time: Optional[datetime] = None

    async def fetch_stats(self) -> dict:
        """Fetch current statistics from server."""
        async with httpx.AsyncClient() as client:
            response = await client.get(self.stats_url, timeout=5.0)
            response.raise_for_status()
            return response.json()

    def create_dashboard(self, stats: dict) -> Layout:
        """Create the monitoring dashboard layout."""
        layout = Layout()

        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )

        # Header
        layout["header"].update(
            Panel(
                f"[bold blue]WebSocket Monitor[/bold blue] | "
                f"[green]{self.stats_url}[/green] | "
                f"Refresh: {self.refresh_interval}s",
                style="bold white"
            )
        )

        # Body - split into connections and rooms
        layout["body"].split_row(
            Layout(name="connections"),
            Layout(name="rooms")
        )

        # Connections panel
        conn_stats = stats.get("connections", {})
        connections_table = Table(title="Connections", expand=True)
        connections_table.add_column("Metric", style="cyan")
        connections_table.add_column("Value", style="green", justify="right")

        active = conn_stats.get("active_connections", 0)
        total = conn_stats.get("total_connections_ever", 0)
        messages = conn_stats.get("total_messages_sent", 0)

        # Calculate rates if we have previous data
        msg_rate = 0
        if self._previous_stats and self._previous_time:
            prev_messages = self._previous_stats.get("connections", {}).get("total_messages_sent", 0)
            time_diff = (datetime.now() - self._previous_time).total_seconds()
            if time_diff > 0:
                msg_rate = (messages - prev_messages) / time_diff

        connections_table.add_row("Active Connections", str(active))
        connections_table.add_row("Total Connections (ever)", str(total))
        connections_table.add_row("Messages Sent", str(messages))
        connections_table.add_row("Message Rate", f"{msg_rate:.1f}/sec")

        layout["connections"].update(Panel(connections_table))

        # Rooms panel
        rooms = conn_stats.get("room_breakdown", {})
        rooms_table = Table(title="Active Rooms", expand=True)
        rooms_table.add_column("Room", style="cyan")
        rooms_table.add_column("Members", style="green", justify="right")

        if rooms:
            for room, count in sorted(rooms.items(), key=lambda x: -x[1]):
                rooms_table.add_row(room, str(count))
        else:
            rooms_table.add_row("[dim]No active rooms[/dim]", "")

        layout["rooms"].update(Panel(rooms_table))

        # Footer
        layout["footer"].update(
            Panel(
                f"[dim]Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim] | "
                f"[dim]Press Ctrl+C to exit[/dim]",
                style="dim"
            )
        )

        return layout

    async def run(self):
        """Run the monitor."""
        self._running = True

        with Live(self.console.print("Loading..."), refresh_per_second=1) as live:
            while self._running:
                try:
                    stats = await self.fetch_stats()
                    dashboard = self.create_dashboard(stats)
                    live.update(dashboard)

                    # Store for rate calculation
                    self._previous_stats = stats
                    self._previous_time = datetime.now()

                except httpx.HTTPError as e:
                    live.update(
                        Panel(
                            f"[red]Failed to fetch stats: {e}[/red]\n"
                            f"Retrying in {self.refresh_interval}s...",
                            title="Error"
                        )
                    )
                except Exception as e:
                    live.update(
                        Panel(
                            f"[red]Error: {e}[/red]",
                            title="Error"
                        )
                    )

                await asyncio.sleep(self.refresh_interval)

    def stop(self):
        """Stop the monitor."""
        self._running = False


async def main():
    parser = argparse.ArgumentParser(description="WebSocket Connection Monitor")
    parser.add_argument(
        "--stats-url",
        default="http://localhost:8000/ws/stats",
        help="URL for WebSocket stats endpoint (default: http://localhost:8000/ws/stats)"
    )
    parser.add_argument(
        "--refresh",
        type=float,
        default=2.0,
        help="Refresh interval in seconds (default: 2)"
    )

    args = parser.parse_args()

    monitor = WebSocketMonitor(
        stats_url=args.stats_url,
        refresh_interval=args.refresh
    )

    try:
        await monitor.run()
    except KeyboardInterrupt:
        monitor.stop()
        print("\nMonitor stopped.")


if __name__ == "__main__":
    asyncio.run(main())
