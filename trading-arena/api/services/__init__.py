"""
Trading Arena Services

Business logic services for the Trading Arena API.

Services:
    - streaming: Real-time WebSocket streaming for portfolio, orders, and market data
"""

from .streaming import StreamingService, streaming_service

__all__ = ["StreamingService", "streaming_service"]
