"""
Trading Arena WebSocket Endpoint Route

Work Stream E.3: WebSocket endpoint at /ws/v1/{collective_id}

Provides real-time WebSocket connectivity for AI collectives with:
- Ed25519 authentication via query parameters (timestamp, signature)
- Integration with TradingArenaConnectionManager
- Proper connection lifecycle (connect, message loop, disconnect)
- Error handling for authentication failures

Authentication Flow:
    1. Client connects with query params: ?timestamp=<iso>&signature=<base64>
    2. Server validates timestamp is within 5-minute window
    3. Server verifies Ed25519 signature against collective's registered public key
    4. If valid: accept connection and auto-subscribe to collective rooms
    5. If invalid: close connection with appropriate error code

Usage:
    # Include router in main app
    from api.routes.websocket import router
    app.include_router(router, prefix="/ws")

    # Client connects with authentication
    ws://localhost:8000/ws/v1/team-alpha?timestamp=2025-12-26T10:00:00Z&signature=<base64>

WebSocket Close Codes:
    4001 - Missing authentication parameters
    4002 - Invalid/expired timestamp
    4003 - Signature verification failed
    4004 - Collective not registered
    4011 - Superseded by new connection

Author: api-architect (AI-CIV Phase 2)
Version: 1.0.0
Date: 2025-12-26
"""

import logging
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status

from ..auth.ed25519 import verify_signature, verify_timestamp
from ..auth.middleware import get_public_key
from ..websocket.manager import TradingArenaConnectionManager
from ..websocket.handlers import dispatch_message

logger = logging.getLogger(__name__)

# Router for WebSocket endpoints
router = APIRouter()

# Singleton connection manager instance
# Can be overridden for testing via set_manager()
_manager: Optional[TradingArenaConnectionManager] = None


def get_manager() -> TradingArenaConnectionManager:
    """Get or create the singleton connection manager."""
    global _manager
    if _manager is None:
        _manager = TradingArenaConnectionManager()
    return _manager


def set_manager(manager: TradingArenaConnectionManager) -> None:
    """Set the connection manager (for testing)."""
    global _manager
    _manager = manager


async def authenticate_websocket(
    collective_id: str,
    timestamp: Optional[str],
    signature: Optional[str]
) -> tuple[bool, int, str]:
    """
    Authenticate a WebSocket connection request.

    Args:
        collective_id: The collective attempting to connect
        timestamp: ISO format timestamp from query params
        signature: Base64-encoded Ed25519 signature from query params

    Returns:
        Tuple of (success: bool, close_code: int, reason: str)
        On success: (True, 0, "")
        On failure: (False, close_code, reason_message)
    """
    # Check required parameters
    if not timestamp or not signature:
        return (
            False,
            4001,
            "Missing authentication parameters: timestamp and signature required"
        )

    # Validate timestamp is within acceptable window
    if not verify_timestamp(timestamp):
        return (
            False,
            4002,
            "Invalid or expired timestamp (must be within 5-minute window)"
        )

    # Get collective's registered public key
    public_key = get_public_key(collective_id)
    if not public_key:
        return (
            False,
            4004,
            f"Collective '{collective_id}' not registered"
        )

    # Verify the signature
    # For WebSocket, we sign: "WEBSOCKET:/ws/v1/{collective_id}:{timestamp}"
    try:
        is_valid = verify_signature(
            public_key_b64=public_key,
            signature_b64=signature,
            method="WEBSOCKET",
            path=f"/ws/v1/{collective_id}",
            timestamp=timestamp,
            body=None
        )

        if not is_valid:
            return (
                False,
                4003,
                "Signature verification failed"
            )

    except ValueError as e:
        # Timestamp validation error from verify_signature
        return (
            False,
            4002,
            str(e)
        )
    except Exception as e:
        logger.error(f"Signature verification error for {collective_id}: {e}")
        return (
            False,
            4003,
            "Signature verification failed"
        )

    return (True, 0, "")


@router.websocket("/v1/{collective_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    collective_id: str,
    timestamp: Optional[str] = Query(None, description="ISO format timestamp"),
    signature: Optional[str] = Query(None, description="Base64-encoded Ed25519 signature")
):
    """
    WebSocket endpoint for collective real-time updates.

    Provides streaming updates for:
    - Portfolio changes (positions, balance)
    - Order lifecycle events (placed, filled, cancelled)
    - Market data (available to all connected collectives)

    Authentication:
        Query parameters required:
        - timestamp: ISO format timestamp (e.g., 2025-12-26T10:00:00Z)
        - signature: Base64-encoded Ed25519 signature of "WEBSOCKET:/ws/v1/{collective_id}:{timestamp}"

    Message Protocol:
        Inbound messages should be JSON with a "type" field.
        Supported types: ping, subscribe, unsubscribe

        Outbound messages are JSON with structure:
        {
            "type": "portfolio_update" | "order_update" | "market_data",
            "data": { ... },
            "timestamp": "ISO timestamp"
        }

    Args:
        websocket: The WebSocket connection
        collective_id: Unique identifier for the connecting collective
        timestamp: Authentication timestamp (query param)
        signature: Ed25519 signature (query param)
    """
    manager = get_manager()

    # Authenticate the connection
    is_authenticated, close_code, close_reason = await authenticate_websocket(
        collective_id=collective_id,
        timestamp=timestamp,
        signature=signature
    )

    if not is_authenticated:
        logger.warning(
            f"WebSocket auth failed for {collective_id}: {close_reason}"
        )
        # Must accept before we can close with code
        await websocket.accept()
        await websocket.close(code=close_code, reason=close_reason)
        return

    # Connect and register with manager
    connected = await manager.connect(
        websocket=websocket,
        collective_id=collective_id,
        auto_subscribe=True,  # Auto-subscribe to portfolio/orders rooms
        replace_existing=True  # Replace existing connection from same collective
    )

    if not connected:
        logger.error(f"Failed to register connection for {collective_id}")
        await websocket.close(
            code=status.WS_1011_INTERNAL_ERROR,
            reason="Failed to register connection"
        )
        return

    logger.info(f"WebSocket connected: {collective_id}")

    try:
        # Main message loop
        while True:
            # Receive and handle inbound messages
            data = await websocket.receive_json()
            await handle_inbound_message(manager, collective_id, data)

    except WebSocketDisconnect as e:
        logger.info(
            f"WebSocket disconnected: {collective_id} (code={e.code})"
        )
    except Exception as e:
        logger.error(
            f"WebSocket error for {collective_id}: {e}",
            exc_info=True
        )
    finally:
        # Clean disconnect
        await manager.disconnect(collective_id)
        logger.info(f"WebSocket cleanup complete: {collective_id}")


async def handle_inbound_message(
    manager: TradingArenaConnectionManager,
    collective_id: str,
    data: dict
) -> None:
    """
    Handle inbound WebSocket messages from a collective.

    Routes messages through two layers:
        1. Room management (subscribe/unsubscribe) - handled directly
        2. Trading operations - delegated to message dispatcher (Work Stream E.4)

    Supported message types:
        Room Management:
            - subscribe: Subscribe to additional rooms
            - unsubscribe: Unsubscribe from rooms

        Trading Operations (via dispatcher):
            - get_portfolio, get_balances: Portfolio queries
            - place_order, cancel_order, get_orders, get_order: Order management
            - subscribe_market, unsubscribe_market, get_symbols: Market data
            - ping: Heartbeat

    Args:
        manager: The connection manager
        collective_id: The collective sending the message
        data: The parsed JSON message
    """
    message_type = data.get("type", "").lower()

    # Room management - handle directly (manager-level operations)
    if message_type == "subscribe":
        room = data.get("room")
        if room:
            await manager.join_room(collective_id, room)
            await manager.send_personal(collective_id, {
                "type": "subscribed",
                "room": room
            })
        return

    if message_type == "unsubscribe":
        room = data.get("room")
        if room:
            await manager.leave_room(collective_id, room)
            await manager.send_personal(collective_id, {
                "type": "unsubscribed",
                "room": room
            })
        return

    # All other messages - dispatch to handlers (Work Stream E.4)
    # Includes: portfolio, orders, market data, ping
    response = await dispatch_message(collective_id, data)
    await manager.send_personal(collective_id, response)


# Health check endpoint for WebSocket service
@router.get("/health")
async def websocket_health():
    """
    WebSocket service health check.

    Returns connection statistics and manager status.
    """
    manager = get_manager()
    stats = manager.get_stats()

    return {
        "status": "healthy",
        "active_connections": stats.get("active_connections", 0),
        "total_connections": stats.get("total_connections", 0),
        "total_messages": stats.get("total_messages_sent", 0),
        "rooms": stats.get("active_rooms", 0)
    }
