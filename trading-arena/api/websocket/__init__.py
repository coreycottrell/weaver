"""
Trading Arena WebSocket Module

Real-time updates for portfolio changes, order executions, and market data.
"""

from .manager import manager, TradingArenaConnectionManager

__all__ = ["manager", "TradingArenaConnectionManager"]
