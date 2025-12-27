"""
Trading Arena WebSocket Module

Real-time updates for portfolio changes, order executions, and market data.

Components:
    - manager: Connection lifecycle and room management
    - handlers: Message handling and dispatch

Usage:
    from api.websocket import manager, dispatcher, dispatch_message

    # Handle incoming message
    response = await dispatch_message(collective_id, message)
    await manager.send_personal(collective_id, response)
"""

from .manager import manager, TradingArenaConnectionManager
from .handlers import (
    dispatcher,
    dispatch_message,
    MessageDispatcher,
    MessageType,
    ErrorCode,
    HandlerResult,
)

__all__ = [
    # Manager
    "manager",
    "TradingArenaConnectionManager",
    # Handlers
    "dispatcher",
    "dispatch_message",
    "MessageDispatcher",
    "MessageType",
    "ErrorCode",
    "HandlerResult",
]
