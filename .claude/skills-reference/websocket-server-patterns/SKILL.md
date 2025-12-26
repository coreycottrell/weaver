---
name: websocket-server-patterns
description: Production-ready WebSocket server patterns for FastAPI. Covers connection management, authentication, broadcast rooms, heartbeat/keepalive, error handling, and reconnection strategies. Essential for real-time systems like the Trading Arena.
version: 1.0.0
author: AI-CIV (capability-curator)
created: 2025-12-26
domain: real-time-systems
---

# WebSocket Server Patterns for FastAPI

This skill provides production-ready patterns for building WebSocket servers with FastAPI. It covers the complete lifecycle: connection establishment, authentication, state management, broadcasting, heartbeats, error handling, and graceful reconnection.

## When to Use This Skill

**Invoke when**:
- Building real-time features (live dashboards, trading systems, collaborative tools)
- Need bidirectional communication between server and clients
- REST polling is too slow or resource-intensive
- Building systems that require instant push updates

**Don't use when**:
- Simple request-response patterns suffice (use REST)
- Server-sent events (SSE) would work (one-way push only)
- Batch processing where latency doesn't matter

## Prerequisites

```bash
pip install fastapi uvicorn[standard] websockets
```

FastAPI's WebSocket support is built on Starlette's WebSocket implementation.

---

## Part 1: Core Concepts

### WebSocket Lifecycle

```
Client                                      Server
   |                                           |
   |-------- HTTP Upgrade Request ----------->|
   |                                           |
   |<------- HTTP 101 Switching Protocols ----|
   |                                           |
   |============ WebSocket Open ==============|
   |                                           |
   |<-------- Server Message ------------------|
   |-------- Client Message ------------------>|
   |<-------- Server Message ------------------|
   |                                           |
   |-------- Close Frame -------------------->|
   |<------- Close Frame ----------------------|
   |                                           |
   |========== Connection Closed =============|
```

### Key Differences from REST

| Aspect | REST | WebSocket |
|--------|------|-----------|
| Connection | Per-request | Persistent |
| Direction | Client-initiated | Bidirectional |
| State | Stateless | Stateful |
| Overhead | HTTP headers each time | Initial handshake only |
| Push | Polling required | Native support |

---

## Part 2: Basic WebSocket Endpoint

### Minimal Example

```python
# api/websocket/basic.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

### With Path Parameters

```python
@app.websocket("/ws/{client_id}")
async def websocket_with_id(websocket: WebSocket, client_id: str):
    await websocket.accept()
    await websocket.send_text(f"Hello, {client_id}!")
    # ... handle messages
```

### With Query Parameters

```python
@app.websocket("/ws")
async def websocket_with_query(websocket: WebSocket, token: str = None):
    if not token or not validate_token(token):
        await websocket.close(code=4001)  # Custom close code
        return
    await websocket.accept()
    # ... authenticated connection
```

---

## Part 3: Connection Manager Pattern

This is the core pattern for production WebSocket servers. It manages multiple connections and enables broadcasting.

### Reference Implementation

See `references/connection_manager.py` for the complete implementation.

```python
# api/websocket/manager.py
from fastapi import WebSocket
from typing import Dict, Set, Optional
from datetime import datetime
import asyncio
import json

class ConnectionManager:
    """
    Production-ready WebSocket connection manager.

    Features:
    - Track connections by client ID
    - Room-based subscription system
    - Broadcast to all, room, or specific client
    - Connection metadata tracking
    - Graceful disconnect handling
    """

    def __init__(self):
        # client_id -> WebSocket mapping
        self.active_connections: Dict[str, WebSocket] = {}
        # room_name -> set of client_ids
        self.rooms: Dict[str, Set[str]] = {}
        # client_id -> metadata (connected_at, subscriptions, etc.)
        self.metadata: Dict[str, dict] = {}
        # Lock for thread-safe operations
        self._lock = asyncio.Lock()

    async def connect(
        self,
        websocket: WebSocket,
        client_id: str,
        metadata: Optional[dict] = None
    ) -> bool:
        """
        Accept connection and register client.
        Returns True if successful, False if client_id already connected.
        """
        async with self._lock:
            if client_id in self.active_connections:
                # Option 1: Reject new connection
                # return False

                # Option 2: Disconnect old, accept new (recommended)
                old_ws = self.active_connections[client_id]
                try:
                    await old_ws.close(code=4000, reason="Superseded")
                except:
                    pass

            await websocket.accept()
            self.active_connections[client_id] = websocket
            self.metadata[client_id] = {
                "connected_at": datetime.utcnow().isoformat(),
                "subscriptions": set(),
                **(metadata or {})
            }
            return True

    async def disconnect(self, client_id: str):
        """Remove client from all rooms and connections."""
        async with self._lock:
            # Remove from all rooms
            for room_name, members in list(self.rooms.items()):
                members.discard(client_id)
                if not members:
                    del self.rooms[room_name]

            # Remove connection and metadata
            self.active_connections.pop(client_id, None)
            self.metadata.pop(client_id, None)

    async def join_room(self, client_id: str, room: str):
        """Subscribe client to a room."""
        async with self._lock:
            if room not in self.rooms:
                self.rooms[room] = set()
            self.rooms[room].add(client_id)

            if client_id in self.metadata:
                self.metadata[client_id]["subscriptions"].add(room)

    async def leave_room(self, client_id: str, room: str):
        """Unsubscribe client from a room."""
        async with self._lock:
            if room in self.rooms:
                self.rooms[room].discard(client_id)
                if not self.rooms[room]:
                    del self.rooms[room]

            if client_id in self.metadata:
                self.metadata[client_id]["subscriptions"].discard(room)

    async def send_personal(self, client_id: str, message: dict):
        """Send message to specific client."""
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            try:
                await websocket.send_json(message)
            except Exception:
                await self.disconnect(client_id)

    async def broadcast(self, message: dict, exclude: Set[str] = None):
        """Send message to all connected clients."""
        exclude = exclude or set()
        disconnected = []

        for client_id, websocket in self.active_connections.items():
            if client_id not in exclude:
                try:
                    await websocket.send_json(message)
                except Exception:
                    disconnected.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected:
            await self.disconnect(client_id)

    async def broadcast_to_room(
        self,
        room: str,
        message: dict,
        exclude: Set[str] = None
    ):
        """Send message to all clients in a room."""
        exclude = exclude or set()
        if room not in self.rooms:
            return

        disconnected = []
        for client_id in self.rooms[room]:
            if client_id not in exclude:
                websocket = self.active_connections.get(client_id)
                if websocket:
                    try:
                        await websocket.send_json(message)
                    except Exception:
                        disconnected.append(client_id)

        for client_id in disconnected:
            await self.disconnect(client_id)

    @property
    def connection_count(self) -> int:
        """Number of active connections."""
        return len(self.active_connections)

    def get_room_members(self, room: str) -> Set[str]:
        """Get all client IDs in a room."""
        return self.rooms.get(room, set()).copy()

# Singleton instance
manager = ConnectionManager()
```

### Usage with FastAPI

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from .manager import manager

app = FastAPI()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    connected = await manager.connect(websocket, client_id)
    if not connected:
        return

    try:
        # Join default room
        await manager.join_room(client_id, "general")

        while True:
            data = await websocket.receive_json()

            # Handle different message types
            if data.get("type") == "subscribe":
                await manager.join_room(client_id, data["room"])
            elif data.get("type") == "unsubscribe":
                await manager.leave_room(client_id, data["room"])
            elif data.get("type") == "message":
                # Broadcast to room
                await manager.broadcast_to_room(
                    data["room"],
                    {
                        "type": "message",
                        "from": client_id,
                        "content": data["content"]
                    },
                    exclude={client_id}  # Don't echo back
                )

    except WebSocketDisconnect:
        await manager.disconnect(client_id)
        await manager.broadcast_to_room(
            "general",
            {"type": "user_left", "client_id": client_id}
        )
```

---

## Part 4: Authentication Pattern

WebSocket authentication requires special handling since headers aren't easily accessible after the upgrade.

### Pattern 1: Query Parameter Token

```python
# api/websocket/auth.py
from fastapi import WebSocket, HTTPException, status
from jose import jwt, JWTError
from typing import Optional

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

async def get_current_user_ws(websocket: WebSocket) -> Optional[dict]:
    """
    Extract and validate JWT from query parameter.
    WebSocket doesn't have standard header access, so token passed via query.
    """
    token = websocket.query_params.get("token")
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

@app.websocket("/ws/protected")
async def protected_websocket(websocket: WebSocket):
    user = await get_current_user_ws(websocket)
    if not user:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    await websocket.accept()
    # ... handle authenticated connection
```

### Pattern 2: Ed25519 Signature Authentication (Trading Arena)

For high-security scenarios, use cryptographic signatures:

```python
# api/websocket/ed25519_auth.py
import base64
import hashlib
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature

class WebSocketAuthenticator:
    """
    Ed25519-based WebSocket authentication.

    Authentication flow:
    1. Client connects with collective_id in path
    2. Server sends challenge (random nonce + timestamp)
    3. Client signs challenge with private key
    4. Server verifies signature with registered public key
    """

    def __init__(self, public_key_registry: dict):
        self.public_keys = public_key_registry
        self.pending_challenges: dict = {}

    def generate_challenge(self, collective_id: str) -> dict:
        """Generate authentication challenge."""
        import secrets
        nonce = secrets.token_hex(32)
        timestamp = datetime.utcnow().isoformat()
        challenge = f"{collective_id}|{nonce}|{timestamp}"

        self.pending_challenges[collective_id] = {
            "challenge": challenge,
            "expires": datetime.utcnow() + timedelta(minutes=1)
        }

        return {"challenge": challenge, "expires_in": 60}

    def verify_response(
        self,
        collective_id: str,
        signature_b64: str
    ) -> bool:
        """Verify client's signature of challenge."""
        if collective_id not in self.pending_challenges:
            return False

        pending = self.pending_challenges.pop(collective_id)
        if datetime.utcnow() > pending["expires"]:
            return False

        if collective_id not in self.public_keys:
            return False

        try:
            public_key_pem = self.public_keys[collective_id]
            public_key = load_pem_public_key(public_key_pem.encode())
            signature = base64.b64decode(signature_b64)

            # Ed25519 verify (raises InvalidSignature on failure)
            public_key.verify(
                signature,
                pending["challenge"].encode()
            )
            return True
        except (InvalidSignature, Exception):
            return False

# Usage
authenticator = WebSocketAuthenticator(public_key_registry)

@app.websocket("/ws/{collective_id}")
async def authenticated_websocket(
    websocket: WebSocket,
    collective_id: str
):
    await websocket.accept()

    # Step 1: Send challenge
    challenge = authenticator.generate_challenge(collective_id)
    await websocket.send_json({
        "type": "auth_challenge",
        **challenge
    })

    # Step 2: Wait for signature response (with timeout)
    try:
        response = await asyncio.wait_for(
            websocket.receive_json(),
            timeout=30.0
        )
    except asyncio.TimeoutError:
        await websocket.close(code=4001, reason="Auth timeout")
        return

    # Step 3: Verify signature
    if response.get("type") != "auth_response":
        await websocket.close(code=4001, reason="Invalid auth flow")
        return

    if not authenticator.verify_response(
        collective_id,
        response.get("signature")
    ):
        await websocket.close(code=4001, reason="Invalid signature")
        return

    # Authenticated! Proceed with connection
    await manager.connect(websocket, collective_id, {"authenticated": True})
    # ... handle messages
```

---

## Part 5: Heartbeat/Keepalive Pattern

WebSocket connections can silently die (network issues, NAT timeouts). Heartbeats detect this.

### Server-Side Heartbeat

```python
# api/websocket/heartbeat.py
import asyncio
from datetime import datetime, timedelta
from typing import Dict

class HeartbeatManager:
    """
    Manages heartbeat pings for WebSocket connections.

    Flow:
    1. Server sends "ping" every HEARTBEAT_INTERVAL seconds
    2. Client must respond with "pong" within HEARTBEAT_TIMEOUT
    3. If no pong received, connection considered dead
    """

    HEARTBEAT_INTERVAL = 30  # seconds
    HEARTBEAT_TIMEOUT = 10   # seconds

    def __init__(self, connection_manager: ConnectionManager):
        self.manager = connection_manager
        self.last_pong: Dict[str, datetime] = {}
        self._running = False

    async def start(self):
        """Start the heartbeat background task."""
        self._running = True
        asyncio.create_task(self._heartbeat_loop())

    async def stop(self):
        """Stop the heartbeat background task."""
        self._running = False

    async def _heartbeat_loop(self):
        """Background loop that sends pings and checks for stale connections."""
        while self._running:
            await asyncio.sleep(self.HEARTBEAT_INTERVAL)

            now = datetime.utcnow()
            stale_clients = []

            # Check for stale connections
            for client_id in list(self.manager.active_connections.keys()):
                last = self.last_pong.get(client_id)
                if last and (now - last).total_seconds() > (
                    self.HEARTBEAT_INTERVAL + self.HEARTBEAT_TIMEOUT
                ):
                    stale_clients.append(client_id)

            # Disconnect stale clients
            for client_id in stale_clients:
                print(f"Heartbeat timeout: {client_id}")
                await self.manager.disconnect(client_id)
                self.last_pong.pop(client_id, None)

            # Send ping to all remaining connections
            await self.manager.broadcast({
                "type": "ping",
                "timestamp": now.isoformat()
            })

    def record_pong(self, client_id: str):
        """Record that client responded to ping."""
        self.last_pong[client_id] = datetime.utcnow()

    def record_connect(self, client_id: str):
        """Initialize heartbeat tracking for new connection."""
        self.last_pong[client_id] = datetime.utcnow()

# Integration with message handler
heartbeat_manager = HeartbeatManager(manager)

@app.on_event("startup")
async def startup():
    await heartbeat_manager.start()

@app.on_event("shutdown")
async def shutdown():
    await heartbeat_manager.stop()

@app.websocket("/ws/{client_id}")
async def websocket_with_heartbeat(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    heartbeat_manager.record_connect(client_id)

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("type") == "pong":
                heartbeat_manager.record_pong(client_id)
            else:
                # Handle other message types
                pass

    except WebSocketDisconnect:
        await manager.disconnect(client_id)
```

### Client-Side Implementation (JavaScript)

```javascript
// Client heartbeat handling
class WebSocketClient {
    constructor(url) {
        this.url = url;
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
    }

    connect() {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
            console.log('Connected');
            this.reconnectAttempts = 0;
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);

            if (data.type === 'ping') {
                // Respond to server ping
                this.ws.send(JSON.stringify({ type: 'pong' }));
            } else {
                // Handle other messages
                this.handleMessage(data);
            }
        };

        this.ws.onclose = (event) => {
            console.log('Disconnected', event.code, event.reason);
            this.attemptReconnect();
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error', error);
        };
    }

    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
            console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
            setTimeout(() => this.connect(), delay);
        } else {
            console.error('Max reconnection attempts reached');
        }
    }

    handleMessage(data) {
        // Override in subclass or set handler
        console.log('Received:', data);
    }
}
```

---

## Part 6: Error Handling and Close Codes

### Standard WebSocket Close Codes

| Code | Name | Description |
|------|------|-------------|
| 1000 | Normal | Clean close |
| 1001 | Going Away | Server shutdown or client navigating away |
| 1002 | Protocol Error | Invalid WebSocket protocol |
| 1003 | Unsupported Data | Received unsupported data type |
| 1008 | Policy Violation | Message violates policy |
| 1011 | Internal Error | Server error |

### Custom Application Close Codes (4000-4999)

Define your own codes in the 4000-4999 range:

```python
# api/websocket/close_codes.py
class CloseCode:
    """Custom WebSocket close codes for Trading Arena."""

    # Authentication errors (4001-4010)
    UNAUTHORIZED = 4001
    INVALID_TOKEN = 4002
    TOKEN_EXPIRED = 4003
    AUTH_TIMEOUT = 4004

    # Session errors (4011-4020)
    SESSION_SUPERSEDED = 4011  # New connection replaced this one
    SESSION_EXPIRED = 4012

    # Rate limiting (4021-4030)
    RATE_LIMITED = 4021
    TOO_MANY_CONNECTIONS = 4022

    # Business logic (4031-4040)
    INVALID_SUBSCRIPTION = 4031
    MARKET_CLOSED = 4032

    # Server-side (4091-4099)
    SERVER_SHUTDOWN = 4091
    SERVER_ERROR = 4092

# Usage
await websocket.close(
    code=CloseCode.RATE_LIMITED,
    reason="Too many requests"
)
```

### Comprehensive Error Handler

```python
# api/websocket/error_handler.py
from fastapi import WebSocket
import traceback
import logging

logger = logging.getLogger(__name__)

async def safe_websocket_handler(
    websocket: WebSocket,
    handler_func,
    client_id: str
):
    """
    Wrapper that handles all WebSocket errors gracefully.
    """
    try:
        await handler_func(websocket, client_id)

    except WebSocketDisconnect as e:
        logger.info(f"Client {client_id} disconnected: code={e.code}")
        await manager.disconnect(client_id)

    except asyncio.CancelledError:
        logger.info(f"Connection {client_id} cancelled")
        await manager.disconnect(client_id)
        raise

    except json.JSONDecodeError:
        logger.warning(f"Invalid JSON from {client_id}")
        try:
            await websocket.send_json({
                "type": "error",
                "code": "INVALID_JSON",
                "message": "Invalid JSON format"
            })
        except:
            pass

    except Exception as e:
        logger.error(f"Error handling {client_id}: {e}\n{traceback.format_exc()}")
        try:
            await websocket.close(
                code=CloseCode.SERVER_ERROR,
                reason="Internal server error"
            )
        except:
            pass
        await manager.disconnect(client_id)
```

---

## Part 7: Reconnection and State Recovery

When clients reconnect, they may have missed events. Here's how to handle that.

### Event Sequencing

```python
# api/websocket/event_store.py
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import asyncio

@dataclass
class Event:
    sequence: int
    timestamp: datetime
    room: str
    type: str
    data: dict

class EventStore:
    """
    Stores recent events for reconnection recovery.

    When client reconnects with last_sequence, server can
    replay missed events.
    """

    def __init__(self, max_events: int = 1000, ttl_seconds: int = 300):
        self.events: deque = deque(maxlen=max_events)
        self.sequence_counter = 0
        self.ttl_seconds = ttl_seconds
        self._lock = asyncio.Lock()

    async def add_event(
        self,
        room: str,
        event_type: str,
        data: dict
    ) -> Event:
        """Add event to store and return with sequence number."""
        async with self._lock:
            self.sequence_counter += 1
            event = Event(
                sequence=self.sequence_counter,
                timestamp=datetime.utcnow(),
                room=room,
                type=event_type,
                data=data
            )
            self.events.append(event)
            return event

    async def get_events_since(
        self,
        sequence: int,
        room: Optional[str] = None
    ) -> List[Event]:
        """Get all events after given sequence number."""
        async with self._lock:
            cutoff = datetime.utcnow() - timedelta(seconds=self.ttl_seconds)

            return [
                e for e in self.events
                if e.sequence > sequence
                and e.timestamp > cutoff
                and (room is None or e.room == room)
            ]

event_store = EventStore()

# Modified broadcast to store events
async def broadcast_with_history(
    room: str,
    event_type: str,
    data: dict
):
    """Broadcast and store event for replay."""
    event = await event_store.add_event(room, event_type, data)

    await manager.broadcast_to_room(room, {
        "type": event_type,
        "sequence": event.sequence,
        "timestamp": event.timestamp.isoformat(),
        "data": data
    })

# Reconnection handler
@app.websocket("/ws/{client_id}")
async def websocket_with_recovery(
    websocket: WebSocket,
    client_id: str,
    last_sequence: int = 0  # Client provides last seen sequence
):
    await manager.connect(websocket, client_id)

    # Replay missed events
    if last_sequence > 0:
        missed_events = await event_store.get_events_since(last_sequence)
        for event in missed_events:
            await websocket.send_json({
                "type": event.type,
                "sequence": event.sequence,
                "timestamp": event.timestamp.isoformat(),
                "data": event.data,
                "replayed": True  # Flag so client knows it's catch-up
            })

        await websocket.send_json({
            "type": "replay_complete",
            "replayed_count": len(missed_events)
        })

    # Continue with normal message handling
    # ...
```

---

## Part 8: Trading Arena Integration

### Complete WebSocket Endpoint Structure

```python
# api/websocket/trading.py
"""
Trading Arena WebSocket Server

Endpoints:
- /ws/{collective_id}/portfolio - Real-time portfolio updates
- /ws/{collective_id}/orders - Order status stream
- /ws/{collective_id}/market - Market data (prices, depth)
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .manager import ConnectionManager
from .auth import WebSocketAuthenticator
from .heartbeat import HeartbeatManager
from .event_store import EventStore
from ..models.collective import Collective

router = APIRouter()
manager = ConnectionManager()
heartbeat = HeartbeatManager(manager)
events = EventStore()
authenticator = WebSocketAuthenticator()

@router.websocket("/portfolio")
async def portfolio_stream(websocket: WebSocket, collective_id: str):
    """
    Stream portfolio updates in real-time.

    Events:
    - position_updated: When position quantity changes
    - balance_updated: When cash balance changes
    - portfolio_snapshot: Full portfolio state (on connect)
    """
    # Authenticate
    if not await authenticate_ws(websocket, collective_id):
        return

    client_key = f"{collective_id}:portfolio"
    await manager.connect(websocket, client_key)
    await manager.join_room(client_key, f"portfolio:{collective_id}")
    heartbeat.record_connect(client_key)

    # Send initial snapshot
    portfolio = await get_portfolio(collective_id)
    await websocket.send_json({
        "type": "portfolio_snapshot",
        "data": portfolio.dict()
    })

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("type") == "pong":
                heartbeat.record_pong(client_key)
            # Portfolio is read-only stream, no other client messages

    except WebSocketDisconnect:
        await manager.disconnect(client_key)

@router.websocket("/orders")
async def orders_stream(websocket: WebSocket, collective_id: str):
    """
    Stream order status updates.

    Events:
    - order_created: New order placed
    - order_filled: Order fully executed
    - order_partial: Order partially filled
    - order_cancelled: Order cancelled
    - order_rejected: Order rejected
    """
    if not await authenticate_ws(websocket, collective_id):
        return

    client_key = f"{collective_id}:orders"
    await manager.connect(websocket, client_key)
    await manager.join_room(client_key, f"orders:{collective_id}")
    heartbeat.record_connect(client_key)

    # Send active orders snapshot
    active_orders = await get_active_orders(collective_id)
    await websocket.send_json({
        "type": "orders_snapshot",
        "data": [o.dict() for o in active_orders]
    })

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("type") == "pong":
                heartbeat.record_pong(client_key)
            elif data.get("type") == "subscribe_order":
                # Subscribe to specific order updates
                order_id = data.get("order_id")
                await manager.join_room(client_key, f"order:{order_id}")

    except WebSocketDisconnect:
        await manager.disconnect(client_key)

# Event broadcasting (called by order service)
async def broadcast_order_event(
    collective_id: str,
    order_id: str,
    event_type: str,
    order_data: dict
):
    """Called when order state changes."""
    message = {
        "type": event_type,
        "order_id": order_id,
        "data": order_data,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Broadcast to collective's order room
    await manager.broadcast_to_room(f"orders:{collective_id}", message)

    # Broadcast to specific order subscribers
    await manager.broadcast_to_room(f"order:{order_id}", message)

    # Store for replay
    await events.add_event(f"orders:{collective_id}", event_type, order_data)

async def broadcast_portfolio_event(
    collective_id: str,
    event_type: str,
    portfolio_data: dict
):
    """Called when portfolio state changes."""
    message = {
        "type": event_type,
        "data": portfolio_data,
        "timestamp": datetime.utcnow().isoformat()
    }

    await manager.broadcast_to_room(f"portfolio:{collective_id}", message)
    await events.add_event(f"portfolio:{collective_id}", event_type, portfolio_data)
```

---

## Part 9: Testing WebSocket Endpoints

### Using pytest-asyncio

```python
# tests/test_websocket.py
import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from httpx import AsyncClient
import asyncio

@pytest.fixture
def client():
    from api.main import app
    return TestClient(app)

def test_websocket_connect(client):
    """Test basic WebSocket connection."""
    with client.websocket_connect("/ws/test-client") as websocket:
        # Should receive welcome or snapshot
        data = websocket.receive_json()
        assert "type" in data

def test_websocket_authentication(client):
    """Test that unauthenticated connections are rejected."""
    with pytest.raises(Exception):  # WebSocket close
        with client.websocket_connect("/ws/protected") as websocket:
            pass

def test_websocket_broadcast(client):
    """Test message broadcasting between clients."""
    with client.websocket_connect("/ws/client1") as ws1:
        with client.websocket_connect("/ws/client2") as ws2:
            # Client 1 sends message
            ws1.send_json({
                "type": "message",
                "room": "general",
                "content": "Hello!"
            })

            # Client 2 should receive it
            data = ws2.receive_json()
            assert data["type"] == "message"
            assert data["content"] == "Hello!"

def test_heartbeat_response(client):
    """Test that client responds to heartbeat ping."""
    with client.websocket_connect("/ws/test-client") as websocket:
        # Wait for ping (or simulate)
        websocket.send_json({"type": "ping"})

        # Client should be able to respond
        websocket.send_json({"type": "pong"})
        # No exception = success

@pytest.mark.asyncio
async def test_concurrent_connections():
    """Test multiple concurrent WebSocket connections."""
    from httpx import AsyncClient
    from api.main import app

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # This requires async WebSocket client (e.g., websockets library)
        pass  # Implement with websockets library for true async testing
```

---

## Part 10: Performance Considerations

### Connection Limits

```python
# api/websocket/limits.py
from fastapi import WebSocket
from .manager import manager

MAX_CONNECTIONS_PER_COLLECTIVE = 10
MAX_TOTAL_CONNECTIONS = 1000

async def check_connection_limits(
    websocket: WebSocket,
    collective_id: str
) -> bool:
    """Enforce connection limits."""

    # Check total connections
    if manager.connection_count >= MAX_TOTAL_CONNECTIONS:
        await websocket.close(
            code=CloseCode.TOO_MANY_CONNECTIONS,
            reason="Server at capacity"
        )
        return False

    # Check per-collective connections
    collective_connections = sum(
        1 for cid in manager.active_connections
        if cid.startswith(f"{collective_id}:")
    )
    if collective_connections >= MAX_CONNECTIONS_PER_COLLECTIVE:
        await websocket.close(
            code=CloseCode.TOO_MANY_CONNECTIONS,
            reason="Too many connections for collective"
        )
        return False

    return True
```

### Message Rate Limiting

```python
# api/websocket/rate_limit.py
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    """Token bucket rate limiter for WebSocket messages."""

    def __init__(
        self,
        messages_per_second: float = 10,
        burst_size: int = 20
    ):
        self.rate = messages_per_second
        self.burst_size = burst_size
        self.tokens: dict = defaultdict(lambda: burst_size)
        self.last_update: dict = {}

    def allow(self, client_id: str) -> bool:
        """Check if message is allowed, consume token if so."""
        now = datetime.utcnow()

        # Refill tokens based on time elapsed
        if client_id in self.last_update:
            elapsed = (now - self.last_update[client_id]).total_seconds()
            self.tokens[client_id] = min(
                self.burst_size,
                self.tokens[client_id] + elapsed * self.rate
            )

        self.last_update[client_id] = now

        if self.tokens[client_id] >= 1:
            self.tokens[client_id] -= 1
            return True
        return False

rate_limiter = RateLimiter()

# Usage in message handler
async def handle_message(websocket: WebSocket, client_id: str, data: dict):
    if not rate_limiter.allow(client_id):
        await websocket.send_json({
            "type": "error",
            "code": "RATE_LIMITED",
            "message": "Too many messages, slow down"
        })
        return

    # Process message...
```

---

## Quick Reference

### Essential Imports

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
import asyncio
import json
```

### WebSocket Methods

| Method | Description |
|--------|-------------|
| `await websocket.accept()` | Accept the connection |
| `await websocket.close(code, reason)` | Close the connection |
| `await websocket.send_text(data)` | Send string message |
| `await websocket.send_json(data)` | Send JSON message |
| `await websocket.send_bytes(data)` | Send binary message |
| `await websocket.receive_text()` | Receive string message |
| `await websocket.receive_json()` | Receive JSON message |
| `await websocket.receive_bytes()` | Receive binary message |

### Common Patterns Checklist

- [ ] Connection manager for multi-client support
- [ ] Authentication before accept or via challenge-response
- [ ] Room/subscription system for targeted broadcasts
- [ ] Heartbeat for connection health monitoring
- [ ] Custom close codes for error classification
- [ ] Event store for reconnection recovery
- [ ] Rate limiting to prevent abuse
- [ ] Connection limits per client/total
- [ ] Graceful shutdown handling
- [ ] Comprehensive error handling and logging

---

## Additional Resources

See the `references/` directory for:
- `connection_manager.py` - Complete production-ready implementation
- `trading_websocket.py` - Trading Arena-specific WebSocket setup
- `client_example.js` - JavaScript client implementation

See the `scripts/` directory for:
- `ws_load_test.py` - Load testing script for WebSocket endpoints
- `ws_monitor.py` - Connection monitoring utility

---

**Skill Version**: 1.0.0
**Created**: 2025-12-26
**Author**: AI-CIV capability-curator
**Domain**: Real-time systems, Trading Arena
**License**: MIT
