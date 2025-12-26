#!/usr/bin/env python3
"""
WebSocket Load Testing Script

Tests WebSocket server performance under load.
Measures connection time, message latency, and throughput.

Usage:
    python ws_load_test.py --url ws://localhost:8000/ws --clients 100 --duration 60

Requirements:
    pip install websockets aiohttp statistics

Author: AI-CIV capability-curator
Version: 1.0.0
Date: 2025-12-26
"""

import argparse
import asyncio
import json
import statistics
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import logging

try:
    import websockets
    from websockets.exceptions import ConnectionClosed
except ImportError:
    print("Please install websockets: pip install websockets")
    exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ClientMetrics:
    """Metrics for a single client."""
    client_id: str
    connected: bool = False
    connect_time_ms: float = 0.0
    messages_sent: int = 0
    messages_received: int = 0
    errors: int = 0
    latencies_ms: List[float] = field(default_factory=list)
    disconnect_reason: Optional[str] = None


@dataclass
class LoadTestResults:
    """Aggregated load test results."""
    total_clients: int
    successful_connections: int
    failed_connections: int
    total_messages_sent: int
    total_messages_received: int
    total_errors: int
    duration_seconds: float
    connect_times_ms: List[float]
    latencies_ms: List[float]

    @property
    def connection_rate(self) -> float:
        """Successful connection percentage."""
        if self.total_clients == 0:
            return 0.0
        return (self.successful_connections / self.total_clients) * 100

    @property
    def messages_per_second(self) -> float:
        """Messages sent per second."""
        if self.duration_seconds == 0:
            return 0.0
        return self.total_messages_sent / self.duration_seconds

    @property
    def avg_connect_time_ms(self) -> float:
        """Average connection time."""
        if not self.connect_times_ms:
            return 0.0
        return statistics.mean(self.connect_times_ms)

    @property
    def avg_latency_ms(self) -> float:
        """Average message round-trip latency."""
        if not self.latencies_ms:
            return 0.0
        return statistics.mean(self.latencies_ms)

    @property
    def p95_latency_ms(self) -> float:
        """95th percentile latency."""
        if len(self.latencies_ms) < 2:
            return 0.0
        sorted_latencies = sorted(self.latencies_ms)
        idx = int(len(sorted_latencies) * 0.95)
        return sorted_latencies[idx]

    @property
    def p99_latency_ms(self) -> float:
        """99th percentile latency."""
        if len(self.latencies_ms) < 2:
            return 0.0
        sorted_latencies = sorted(self.latencies_ms)
        idx = int(len(sorted_latencies) * 0.99)
        return sorted_latencies[idx]

    def summary(self) -> str:
        """Generate human-readable summary."""
        return f"""
========================================
         WebSocket Load Test Results
========================================

Connections:
  Total clients: {self.total_clients}
  Successful: {self.successful_connections} ({self.connection_rate:.1f}%)
  Failed: {self.failed_connections}

Messages:
  Sent: {self.total_messages_sent}
  Received: {self.total_messages_received}
  Throughput: {self.messages_per_second:.1f} msg/sec
  Errors: {self.total_errors}

Timing:
  Test duration: {self.duration_seconds:.1f}s
  Avg connect time: {self.avg_connect_time_ms:.1f}ms
  Avg latency: {self.avg_latency_ms:.1f}ms
  P95 latency: {self.p95_latency_ms:.1f}ms
  P99 latency: {self.p99_latency_ms:.1f}ms

========================================
"""


class LoadTestClient:
    """A single load test client."""

    def __init__(
        self,
        client_id: str,
        url: str,
        message_interval: float = 1.0
    ):
        self.client_id = client_id
        self.url = f"{url}/{client_id}"
        self.message_interval = message_interval
        self.metrics = ClientMetrics(client_id=client_id)
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self._running = False
        self._pending_pings: dict = {}

    async def connect(self) -> bool:
        """Connect to WebSocket server."""
        start = time.perf_counter()

        try:
            self.ws = await asyncio.wait_for(
                websockets.connect(self.url),
                timeout=10.0
            )
            connect_time = (time.perf_counter() - start) * 1000
            self.metrics.connected = True
            self.metrics.connect_time_ms = connect_time
            logger.debug(f"Client {self.client_id} connected in {connect_time:.1f}ms")
            return True

        except asyncio.TimeoutError:
            self.metrics.disconnect_reason = "Connection timeout"
            self.metrics.errors += 1
            return False

        except Exception as e:
            self.metrics.disconnect_reason = str(e)
            self.metrics.errors += 1
            return False

    async def run(self, duration: float):
        """Run the client for specified duration."""
        if not self.ws:
            return

        self._running = True
        end_time = time.time() + duration

        try:
            # Start receiver task
            receiver = asyncio.create_task(self._receive_loop())

            # Send messages until duration ends
            while time.time() < end_time and self._running:
                await self._send_ping()
                await asyncio.sleep(self.message_interval)

            self._running = False
            receiver.cancel()

        except ConnectionClosed as e:
            self.metrics.disconnect_reason = f"Connection closed: {e.code}"
        except Exception as e:
            self.metrics.errors += 1
            self.metrics.disconnect_reason = str(e)
        finally:
            await self.disconnect()

    async def _send_ping(self):
        """Send a ping message and track for latency measurement."""
        if not self.ws:
            return

        ping_id = f"{self.client_id}-{self.metrics.messages_sent}"
        message = {
            "type": "ping",
            "id": ping_id,
            "timestamp": time.time()
        }

        try:
            await self.ws.send(json.dumps(message))
            self._pending_pings[ping_id] = message["timestamp"]
            self.metrics.messages_sent += 1
        except Exception:
            self.metrics.errors += 1

    async def _receive_loop(self):
        """Receive messages and calculate latency."""
        try:
            while self._running and self.ws:
                message = await self.ws.recv()
                self.metrics.messages_received += 1

                try:
                    data = json.loads(message)

                    # Handle pong response
                    if data.get("type") == "pong":
                        ping_id = data.get("id")
                        if ping_id in self._pending_pings:
                            sent_time = self._pending_pings.pop(ping_id)
                            latency = (time.time() - sent_time) * 1000
                            self.metrics.latencies_ms.append(latency)

                    # Handle server ping
                    elif data.get("type") == "ping":
                        await self.ws.send(json.dumps({"type": "pong"}))

                except json.JSONDecodeError:
                    pass

        except asyncio.CancelledError:
            pass
        except ConnectionClosed:
            pass

    async def disconnect(self):
        """Disconnect from WebSocket server."""
        self._running = False
        if self.ws:
            try:
                await self.ws.close()
            except Exception:
                pass
            self.ws = None


class LoadTester:
    """WebSocket load tester."""

    def __init__(
        self,
        url: str,
        num_clients: int = 100,
        duration: float = 60.0,
        message_interval: float = 1.0,
        ramp_up_time: float = 10.0
    ):
        self.url = url
        self.num_clients = num_clients
        self.duration = duration
        self.message_interval = message_interval
        self.ramp_up_time = ramp_up_time
        self.clients: List[LoadTestClient] = []

    async def run(self) -> LoadTestResults:
        """Run the load test."""
        logger.info(f"Starting load test: {self.num_clients} clients, {self.duration}s duration")

        # Create clients
        self.clients = [
            LoadTestClient(
                client_id=f"loadtest-{i}",
                url=self.url,
                message_interval=self.message_interval
            )
            for i in range(self.num_clients)
        ]

        start_time = time.time()

        # Ramp up: connect clients gradually
        delay_per_client = self.ramp_up_time / self.num_clients if self.num_clients > 0 else 0

        connect_tasks = []
        for client in self.clients:
            connect_tasks.append(asyncio.create_task(client.connect()))
            if delay_per_client > 0:
                await asyncio.sleep(delay_per_client)

        # Wait for all connections
        await asyncio.gather(*connect_tasks)

        connected_count = sum(1 for c in self.clients if c.metrics.connected)
        logger.info(f"Connected {connected_count}/{self.num_clients} clients")

        # Run all clients
        run_tasks = [
            asyncio.create_task(client.run(self.duration))
            for client in self.clients
            if client.metrics.connected
        ]

        if run_tasks:
            await asyncio.gather(*run_tasks)

        end_time = time.time()

        # Aggregate results
        return self._aggregate_results(end_time - start_time)

    def _aggregate_results(self, duration: float) -> LoadTestResults:
        """Aggregate metrics from all clients."""
        connect_times = []
        all_latencies = []
        total_sent = 0
        total_received = 0
        total_errors = 0
        successful = 0

        for client in self.clients:
            if client.metrics.connected:
                successful += 1
                connect_times.append(client.metrics.connect_time_ms)

            total_sent += client.metrics.messages_sent
            total_received += client.metrics.messages_received
            total_errors += client.metrics.errors
            all_latencies.extend(client.metrics.latencies_ms)

        return LoadTestResults(
            total_clients=self.num_clients,
            successful_connections=successful,
            failed_connections=self.num_clients - successful,
            total_messages_sent=total_sent,
            total_messages_received=total_received,
            total_errors=total_errors,
            duration_seconds=duration,
            connect_times_ms=connect_times,
            latencies_ms=all_latencies
        )


async def main():
    parser = argparse.ArgumentParser(description="WebSocket Load Tester")
    parser.add_argument(
        "--url",
        default="ws://localhost:8000/ws",
        help="WebSocket URL (default: ws://localhost:8000/ws)"
    )
    parser.add_argument(
        "--clients",
        type=int,
        default=100,
        help="Number of concurrent clients (default: 100)"
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=60.0,
        help="Test duration in seconds (default: 60)"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Message interval in seconds (default: 1.0)"
    )
    parser.add_argument(
        "--ramp-up",
        type=float,
        default=10.0,
        help="Ramp-up time in seconds (default: 10)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    tester = LoadTester(
        url=args.url,
        num_clients=args.clients,
        duration=args.duration,
        message_interval=args.interval,
        ramp_up_time=args.ramp_up
    )

    results = await tester.run()
    print(results.summary())

    # Return non-zero exit code if connection rate < 95%
    if results.connection_rate < 95:
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
