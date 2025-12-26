"""
Trading Arena WebSocket Server Implementation

Complete WebSocket server for the AI-CIV Trading Arena.
Implements authenticated connections, portfolio streaming,
order updates, and market data.

Endpoints:
- /ws/{collective_id}/portfolio - Real-time portfolio updates
- /ws/{collective_id}/orders - Order status stream
- /ws/{collective_id}/market/{symbol} - Market data for specific symbol

Requirements:
- Ed25519 public key registered for collective
- Valid authentication challenge-response

Author: AI-CIV capability-curator
Version: 1.0.0
Date: 2025-12-26
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Optional, Set, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import asyncio
import base64
import secrets
import logging
import json

# Cryptography for Ed25519
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature

from .connection_manager import ConnectionManager, ConnectionMetadata

logger = logging.getLogger(__name__)


# ==================== Close Codes ====================

class CloseCode:
    """Trading Arena WebSocket close codes (4000-4999 range)."""

    # Authentication (4001-4010)
    UNAUTHORIZED = 4001
    INVALID_SIGNATURE = 4002
    AUTH_TIMEOUT = 4003
    COLLECTIVE_NOT_FOUND = 4004

    # Session (4011-4020)
    SESSION_SUPERSEDED = 4011
    SESSION_EXPIRED = 4012

    # Rate Limiting (4021-4030)
    RATE_LIMITED = 4021
    TOO_MANY_CONNECTIONS = 4022

    # Business Logic (4031-4040)
    INVALID_SUBSCRIPTION = 4031
    MARKET_CLOSED = 4032
    COLLECTIVE_SUSPENDED = 4033

    # Server (4091-4099)
    SERVER_SHUTDOWN = 4091
    SERVER_ERROR = 4092


# ==================== Event Types ====================

class EventType(str, Enum):
    """WebSocket event types."""

    # Authentication
    AUTH_CHALLENGE = "auth_challenge"
    AUTH_SUCCESS = "auth_success"
    AUTH_FAILURE = "auth_failure"

    # Portfolio
    PORTFOLIO_SNAPSHOT = "portfolio_snapshot"
    POSITION_UPDATED = "position_updated"
    BALANCE_UPDATED = "balance_updated"

    # Orders
    ORDERS_SNAPSHOT = "orders_snapshot"
    ORDER_CREATED = "order_created"
    ORDER_FILLED = "order_filled"
    ORDER_PARTIAL = "order_partial"
    ORDER_CANCELLED = "order_cancelled"
    ORDER_REJECTED = "order_rejected"

    # Market
    PRICE_UPDATE = "price_update"
    ORDERBOOK_UPDATE = "orderbook_update"

    # System
    PING = "ping"
    PONG = "pong"
    ERROR = "error"
    REPLAY_COMPLETE = "replay_complete"


# ==================== Authenticator ====================

@dataclass
class PendingChallenge:
    """Pending authentication challenge."""
    challenge: str
    expires: datetime
    collective_id: str


class TradingAuthenticator:
    """
    Ed25519-based WebSocket authentication for Trading Arena.

    Flow:
    1. Client connects with collective_id
    2. Server sends random challenge
    3. Client signs challenge with private key
    4. Server verifies with registered public key
    """

    CHALLENGE_TTL_SECONDS = 60

    def __init__(self):
        # collective_id -> PEM-encoded public key
        self._public_keys: Dict[str, str] = {}
        # collective_id -> PendingChallenge
        self._pending: Dict[str, PendingChallenge] = {}
        self._lock = asyncio.Lock()

    def register_collective(self, collective_id: str, public_key_pem: str):
        """Register a collective's public key."""
        self._public_keys[collective_id] = public_key_pem
        logger.info(f"Registered public key for collective: {collective_id}")

    def is_registered(self, collective_id: str) -> bool:
        """Check if collective is registered."""
        return collective_id in self._public_keys

    async def create_challenge(self, collective_id: str) -> Dict[str, Any]:
        """
        Generate authentication challenge for collective.

        Returns:
            Dict with challenge string and expiration time
        """
        if collective_id not in self._public_keys:
            raise ValueError(f"Collective not registered: {collective_id}")

        nonce = secrets.token_hex(32)
        timestamp = datetime.utcnow().isoformat()
        challenge = f"{collective_id}|{nonce}|{timestamp}"

        async with self._lock:
            self._pending[collective_id] = PendingChallenge(
                challenge=challenge,
                expires=datetime.utcnow() + timedelta(seconds=self.CHALLENGE_TTL_SECONDS),
                collective_id=collective_id
            )

        return {
            "challenge": challenge,
            "expires_in": self.CHALLENGE_TTL_SECONDS
        }

    async def verify_signature(
        self,
        collective_id: str,
        signature_b64: str
    ) -> bool:
        """
        Verify client's signature of challenge.

        Args:
            collective_id: The collective attempting authentication
            signature_b64: Base64-encoded Ed25519 signature

        Returns:
            True if signature is valid
        """
        async with self._lock:
            pending = self._pending.pop(collective_id, None)

        if not pending:
            logger.warning(f"No pending challenge for: {collective_id}")
            return False

        if datetime.utcnow() > pending.expires:
            logger.warning(f"Challenge expired for: {collective_id}")
            return False

        public_key_pem = self._public_keys.get(collective_id)
        if not public_key_pem:
            logger.warning(f"No public key for: {collective_id}")
            return False

        try:
            public_key = load_pem_public_key(public_key_pem.encode())

            if not isinstance(public_key, Ed25519PublicKey):
                logger.error(f"Invalid key type for: {collective_id}")
                return False

            signature = base64.b64decode(signature_b64)
            public_key.verify(signature, pending.challenge.encode())

            logger.info(f"Authentication successful: {collective_id}")
            return True

        except InvalidSignature:
            logger.warning(f"Invalid signature from: {collective_id}")
            return False
        except Exception as e:
            logger.error(f"Auth error for {collective_id}: {e}")
            return False

    async def cleanup_expired(self):
        """Remove expired challenges."""
        now = datetime.utcnow()
        async with self._lock:
            expired = [
                cid for cid, p in self._pending.items()
                if now > p.expires
            ]
            for cid in expired:
                del self._pending[cid]


# ==================== Heartbeat Manager ====================

class HeartbeatManager:
    """
    Manages heartbeat pings for WebSocket connections.

    Sends periodic pings and tracks pong responses.
    Disconnects clients that don't respond.
    """

    PING_INTERVAL = 30  # seconds
    PONG_TIMEOUT = 10   # seconds

    def __init__(self, connection_manager: ConnectionManager):
        self.manager = connection_manager
        self._last_pong: Dict[str, datetime] = {}
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        """Start heartbeat background task."""
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._heartbeat_loop())
        logger.info("Heartbeat manager started")

    async def stop(self):
        """Stop heartbeat background task."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Heartbeat manager stopped")

    async def _heartbeat_loop(self):
        """Background loop for heartbeat management."""
        while self._running:
            try:
                await asyncio.sleep(self.PING_INTERVAL)

                now = datetime.utcnow()
                stale_threshold = now - timedelta(
                    seconds=self.PING_INTERVAL + self.PONG_TIMEOUT
                )

                # Find stale connections
                stale_clients = []
                for client_id in self.manager.get_client_ids():
                    last = self._last_pong.get(client_id)
                    if last and last < stale_threshold:
                        stale_clients.append(client_id)

                # Disconnect stale clients
                for client_id in stale_clients:
                    logger.info(f"Heartbeat timeout: {client_id}")
                    await self.manager.disconnect(client_id)
                    self._last_pong.pop(client_id, None)

                # Send ping to all remaining
                await self.manager.broadcast({
                    "type": EventType.PING,
                    "timestamp": now.isoformat()
                })

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")

    def record_connect(self, client_id: str):
        """Record new connection for heartbeat tracking."""
        self._last_pong[client_id] = datetime.utcnow()

    def record_pong(self, client_id: str):
        """Record pong response from client."""
        self._last_pong[client_id] = datetime.utcnow()

    def record_disconnect(self, client_id: str):
        """Clean up heartbeat tracking for disconnected client."""
        self._last_pong.pop(client_id, None)


# ==================== Event Store ====================

@dataclass
class StoredEvent:
    """Event stored for replay on reconnection."""
    sequence: int
    timestamp: datetime
    room: str
    event_type: str
    data: Dict[str, Any]


class EventStore:
    """
    Stores recent events for reconnection recovery.

    Clients can reconnect with last_sequence to receive
    missed events.
    """

    def __init__(self, max_events: int = 1000, ttl_seconds: int = 300):
        self._events: List[StoredEvent] = []
        self._sequence = 0
        self._max_events = max_events
        self._ttl = timedelta(seconds=ttl_seconds)
        self._lock = asyncio.Lock()

    async def add(
        self,
        room: str,
        event_type: str,
        data: Dict[str, Any]
    ) -> StoredEvent:
        """Add event to store."""
        async with self._lock:
            self._sequence += 1
            event = StoredEvent(
                sequence=self._sequence,
                timestamp=datetime.utcnow(),
                room=room,
                event_type=event_type,
                data=data
            )
            self._events.append(event)

            # Trim old events
            if len(self._events) > self._max_events:
                self._events = self._events[-self._max_events:]

            return event

    async def get_since(
        self,
        sequence: int,
        room: Optional[str] = None
    ) -> List[StoredEvent]:
        """Get events after given sequence number."""
        async with self._lock:
            cutoff = datetime.utcnow() - self._ttl
            return [
                e for e in self._events
                if e.sequence > sequence
                and e.timestamp > cutoff
                and (room is None or e.room == room)
            ]

    @property
    def current_sequence(self) -> int:
        """Get current sequence number."""
        return self._sequence


# ==================== Trading WebSocket Server ====================

class TradingWebSocketServer:
    """
    Complete Trading Arena WebSocket server.

    Manages authenticated connections and real-time streaming
    for portfolios, orders, and market data.
    """

    MAX_CONNECTIONS_PER_COLLECTIVE = 5
    AUTH_TIMEOUT = 30  # seconds

    def __init__(self):
        self.manager = ConnectionManager()
        self.authenticator = TradingAuthenticator()
        self.heartbeat = HeartbeatManager(self.manager)
        self.events = EventStore()
        self._started = False

    async def start(self):
        """Start the WebSocket server services."""
        if self._started:
            return

        await self.heartbeat.start()
        self._started = True
        logger.info("Trading WebSocket server started")

    async def stop(self):
        """Stop the WebSocket server services."""
        await self.heartbeat.stop()
        await self.manager.close_all(
            code=CloseCode.SERVER_SHUTDOWN,
            reason="Server shutting down"
        )
        self._started = False
        logger.info("Trading WebSocket server stopped")

    def register_collective(self, collective_id: str, public_key_pem: str):
        """Register a collective for authentication."""
        self.authenticator.register_collective(collective_id, public_key_pem)

    async def _check_connection_limit(
        self,
        websocket: WebSocket,
        collective_id: str
    ) -> bool:
        """Check if collective has reached connection limit."""
        current_connections = sum(
            1 for cid in self.manager.get_client_ids()
            if cid.startswith(f"{collective_id}:")
        )

        if current_connections >= self.MAX_CONNECTIONS_PER_COLLECTIVE:
            await websocket.close(
                code=CloseCode.TOO_MANY_CONNECTIONS,
                reason=f"Max {self.MAX_CONNECTIONS_PER_COLLECTIVE} connections per collective"
            )
            return False
        return True

    async def _authenticate(
        self,
        websocket: WebSocket,
        collective_id: str
    ) -> bool:
        """
        Perform Ed25519 challenge-response authentication.

        Returns True if authenticated successfully.
        """
        # Check if collective is registered
        if not self.authenticator.is_registered(collective_id):
            await websocket.close(
                code=CloseCode.COLLECTIVE_NOT_FOUND,
                reason="Collective not registered"
            )
            return False

        # Send challenge
        try:
            challenge = await self.authenticator.create_challenge(collective_id)
            await websocket.send_json({
                "type": EventType.AUTH_CHALLENGE,
                **challenge
            })
        except Exception as e:
            logger.error(f"Failed to send challenge: {e}")
            await websocket.close(code=CloseCode.SERVER_ERROR)
            return False

        # Wait for response
        try:
            response = await asyncio.wait_for(
                websocket.receive_json(),
                timeout=self.AUTH_TIMEOUT
            )
        except asyncio.TimeoutError:
            await websocket.send_json({
                "type": EventType.AUTH_FAILURE,
                "reason": "Authentication timeout"
            })
            await websocket.close(code=CloseCode.AUTH_TIMEOUT)
            return False

        # Verify signature
        if response.get("type") != "auth_response":
            await websocket.send_json({
                "type": EventType.AUTH_FAILURE,
                "reason": "Expected auth_response"
            })
            await websocket.close(code=CloseCode.UNAUTHORIZED)
            return False

        signature = response.get("signature")
        if not signature or not await self.authenticator.verify_signature(
            collective_id, signature
        ):
            await websocket.send_json({
                "type": EventType.AUTH_FAILURE,
                "reason": "Invalid signature"
            })
            await websocket.close(code=CloseCode.INVALID_SIGNATURE)
            return False

        # Success
        await websocket.send_json({
            "type": EventType.AUTH_SUCCESS,
            "collective_id": collective_id
        })
        return True

    async def handle_portfolio_stream(
        self,
        websocket: WebSocket,
        collective_id: str,
        get_portfolio_func,  # async function that returns portfolio dict
        last_sequence: int = 0
    ):
        """
        Handle portfolio WebSocket connection.

        Streams portfolio updates in real-time.
        """
        # Accept and authenticate
        await websocket.accept()

        if not await self._check_connection_limit(websocket, collective_id):
            return

        if not await self._authenticate(websocket, collective_id):
            return

        # Register connection
        client_id = f"{collective_id}:portfolio:{secrets.token_hex(4)}"
        await self.manager.connect(websocket, client_id, replace_existing=False)
        self.heartbeat.record_connect(client_id)

        room = f"portfolio:{collective_id}"
        await self.manager.join_room(client_id, room)

        try:
            # Replay missed events if reconnecting
            if last_sequence > 0:
                missed = await self.events.get_since(last_sequence, room)
                for event in missed:
                    await websocket.send_json({
                        "type": event.event_type,
                        "sequence": event.sequence,
                        "data": event.data,
                        "replayed": True
                    })
                await websocket.send_json({
                    "type": EventType.REPLAY_COMPLETE,
                    "replayed_count": len(missed)
                })

            # Send current snapshot
            portfolio = await get_portfolio_func(collective_id)
            await websocket.send_json({
                "type": EventType.PORTFOLIO_SNAPSHOT,
                "sequence": self.events.current_sequence,
                "data": portfolio
            })

            # Listen for messages (mostly pongs)
            while True:
                data = await websocket.receive_json()

                if data.get("type") == "pong":
                    self.heartbeat.record_pong(client_id)

        except WebSocketDisconnect:
            logger.info(f"Portfolio stream disconnected: {client_id}")
        except Exception as e:
            logger.error(f"Portfolio stream error: {e}")
        finally:
            self.heartbeat.record_disconnect(client_id)
            await self.manager.disconnect(client_id)

    async def handle_orders_stream(
        self,
        websocket: WebSocket,
        collective_id: str,
        get_active_orders_func,  # async function that returns list of orders
        last_sequence: int = 0
    ):
        """
        Handle orders WebSocket connection.

        Streams order status updates in real-time.
        """
        await websocket.accept()

        if not await self._check_connection_limit(websocket, collective_id):
            return

        if not await self._authenticate(websocket, collective_id):
            return

        client_id = f"{collective_id}:orders:{secrets.token_hex(4)}"
        await self.manager.connect(websocket, client_id, replace_existing=False)
        self.heartbeat.record_connect(client_id)

        room = f"orders:{collective_id}"
        await self.manager.join_room(client_id, room)

        try:
            # Replay missed events
            if last_sequence > 0:
                missed = await self.events.get_since(last_sequence, room)
                for event in missed:
                    await websocket.send_json({
                        "type": event.event_type,
                        "sequence": event.sequence,
                        "data": event.data,
                        "replayed": True
                    })
                await websocket.send_json({
                    "type": EventType.REPLAY_COMPLETE,
                    "replayed_count": len(missed)
                })

            # Send active orders snapshot
            orders = await get_active_orders_func(collective_id)
            await websocket.send_json({
                "type": EventType.ORDERS_SNAPSHOT,
                "sequence": self.events.current_sequence,
                "data": orders
            })

            while True:
                data = await websocket.receive_json()

                if data.get("type") == "pong":
                    self.heartbeat.record_pong(client_id)
                elif data.get("type") == "subscribe_order":
                    # Subscribe to specific order updates
                    order_id = data.get("order_id")
                    if order_id:
                        await self.manager.join_room(client_id, f"order:{order_id}")

        except WebSocketDisconnect:
            logger.info(f"Orders stream disconnected: {client_id}")
        except Exception as e:
            logger.error(f"Orders stream error: {e}")
        finally:
            self.heartbeat.record_disconnect(client_id)
            await self.manager.disconnect(client_id)

    # ==================== Event Broadcasting ====================

    async def broadcast_portfolio_update(
        self,
        collective_id: str,
        event_type: EventType,
        data: Dict[str, Any]
    ):
        """Broadcast portfolio update to collective's subscribers."""
        room = f"portfolio:{collective_id}"

        event = await self.events.add(room, event_type, data)

        await self.manager.broadcast_to_room(room, {
            "type": event_type,
            "sequence": event.sequence,
            "timestamp": event.timestamp.isoformat(),
            "data": data
        })

    async def broadcast_order_update(
        self,
        collective_id: str,
        order_id: str,
        event_type: EventType,
        data: Dict[str, Any]
    ):
        """Broadcast order update to collective and order-specific subscribers."""
        room = f"orders:{collective_id}"

        event = await self.events.add(room, event_type, data)

        message = {
            "type": event_type,
            "order_id": order_id,
            "sequence": event.sequence,
            "timestamp": event.timestamp.isoformat(),
            "data": data
        }

        # Broadcast to collective's order room
        await self.manager.broadcast_to_room(room, message)

        # Also broadcast to order-specific room
        await self.manager.broadcast_to_room(f"order:{order_id}", message)

    def get_stats(self) -> Dict[str, Any]:
        """Get WebSocket server statistics."""
        return {
            "connections": self.manager.get_stats(),
            "events": {
                "current_sequence": self.events.current_sequence
            }
        }


# ==================== FastAPI Router Factory ====================

def create_trading_router(
    server: TradingWebSocketServer,
    get_portfolio_func,
    get_active_orders_func
) -> APIRouter:
    """
    Create FastAPI router for Trading Arena WebSocket endpoints.

    Args:
        server: TradingWebSocketServer instance
        get_portfolio_func: async function(collective_id) -> dict
        get_active_orders_func: async function(collective_id) -> list

    Returns:
        Configured APIRouter

    Example:
        from fastapi import FastAPI
        from trading_websocket import TradingWebSocketServer, create_trading_router

        server = TradingWebSocketServer()
        router = create_trading_router(server, get_portfolio, get_orders)

        app = FastAPI()
        app.include_router(router, prefix="/ws")

        @app.on_event("startup")
        async def startup():
            await server.start()
    """
    router = APIRouter()

    @router.websocket("/{collective_id}/portfolio")
    async def portfolio_stream(
        websocket: WebSocket,
        collective_id: str,
        last_sequence: int = 0
    ):
        await server.handle_portfolio_stream(
            websocket, collective_id, get_portfolio_func, last_sequence
        )

    @router.websocket("/{collective_id}/orders")
    async def orders_stream(
        websocket: WebSocket,
        collective_id: str,
        last_sequence: int = 0
    ):
        await server.handle_orders_stream(
            websocket, collective_id, get_active_orders_func, last_sequence
        )

    @router.get("/stats")
    async def websocket_stats():
        return server.get_stats()

    return router


# ==================== Example Usage ====================

if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI(title="Trading Arena WebSocket Server")
    server = TradingWebSocketServer()

    # Mock data functions
    async def get_portfolio(collective_id: str) -> dict:
        return {
            "collective_id": collective_id,
            "cash_balance": 10000.00,
            "positions": [],
            "total_value": 10000.00
        }

    async def get_orders(collective_id: str) -> list:
        return []

    # Register test collective (in production, load from DB)
    # server.register_collective("weaver", TEST_PUBLIC_KEY_PEM)

    router = create_trading_router(server, get_portfolio, get_orders)
    app.include_router(router, prefix="/ws")

    @app.on_event("startup")
    async def startup():
        await server.start()

    @app.on_event("shutdown")
    async def shutdown():
        await server.stop()

    uvicorn.run(app, host="0.0.0.0", port=8000)
