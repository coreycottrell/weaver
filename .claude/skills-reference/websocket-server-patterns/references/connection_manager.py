"""
Production-Ready WebSocket Connection Manager

This is the complete, copy-paste ready implementation of the
ConnectionManager pattern for FastAPI WebSocket applications.

Features:
- Client tracking by unique ID
- Room-based subscriptions (pub/sub pattern)
- Broadcast to all, room, or individual
- Connection metadata tracking
- Thread-safe async operations
- Graceful disconnect handling

Usage:
    from connection_manager import manager

    @app.websocket("/ws/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, client_id: str):
        await manager.connect(websocket, client_id)
        try:
            while True:
                data = await websocket.receive_json()
                await manager.broadcast_to_room("general", data)
        except WebSocketDisconnect:
            await manager.disconnect(client_id)

Author: AI-CIV capability-curator
Version: 1.0.0
Date: 2025-12-26
"""

from fastapi import WebSocket
from typing import Dict, Set, Optional, List, Any
from datetime import datetime
from dataclasses import dataclass, field
import asyncio
import logging

logger = logging.getLogger(__name__)


@dataclass
class ConnectionMetadata:
    """Metadata tracked for each WebSocket connection."""
    connected_at: datetime
    client_id: str
    subscriptions: Set[str] = field(default_factory=set)
    user_data: Dict[str, Any] = field(default_factory=dict)
    message_count: int = 0
    last_activity: datetime = field(default_factory=datetime.utcnow)


class ConnectionManager:
    """
    Production-ready WebSocket connection manager.

    Thread-safe management of WebSocket connections with support for:
    - Unique client identification
    - Room-based subscriptions
    - Targeted and broadcast messaging
    - Connection lifecycle management

    Example:
        manager = ConnectionManager()

        # In your WebSocket endpoint:
        await manager.connect(websocket, "user-123")
        await manager.join_room("user-123", "trading-room")
        await manager.broadcast_to_room("trading-room", {"price": 100})
    """

    def __init__(self):
        # Core state
        self._connections: Dict[str, WebSocket] = {}
        self._metadata: Dict[str, ConnectionMetadata] = {}
        self._rooms: Dict[str, Set[str]] = {}

        # Thread safety
        self._lock = asyncio.Lock()

        # Statistics
        self._total_connections = 0
        self._total_messages_sent = 0

    # ==================== Connection Lifecycle ====================

    async def connect(
        self,
        websocket: WebSocket,
        client_id: str,
        user_data: Optional[Dict[str, Any]] = None,
        replace_existing: bool = True
    ) -> bool:
        """
        Accept WebSocket connection and register client.

        Args:
            websocket: The WebSocket connection
            client_id: Unique identifier for this client
            user_data: Optional metadata to associate with connection
            replace_existing: If True, disconnect existing connection with same ID

        Returns:
            True if connection accepted, False if rejected

        Example:
            @app.websocket("/ws/{client_id}")
            async def ws(websocket: WebSocket, client_id: str):
                if await manager.connect(websocket, client_id):
                    # Connected successfully
                    pass
        """
        async with self._lock:
            # Handle existing connection with same ID
            if client_id in self._connections:
                if replace_existing:
                    await self._disconnect_internal(client_id, code=4011, reason="Superseded")
                else:
                    logger.warning(f"Rejected duplicate connection: {client_id}")
                    return False

            # Accept the new connection
            await websocket.accept()

            # Register connection
            self._connections[client_id] = websocket
            self._metadata[client_id] = ConnectionMetadata(
                connected_at=datetime.utcnow(),
                client_id=client_id,
                user_data=user_data or {}
            )

            self._total_connections += 1

            logger.info(f"Client connected: {client_id} (total: {len(self._connections)})")
            return True

    async def disconnect(self, client_id: str):
        """
        Disconnect client and clean up all associated state.

        Removes client from all rooms and cleans up metadata.

        Args:
            client_id: The client to disconnect
        """
        async with self._lock:
            await self._disconnect_internal(client_id)

    async def _disconnect_internal(
        self,
        client_id: str,
        code: int = 1000,
        reason: str = "Normal closure"
    ):
        """Internal disconnect without acquiring lock (caller must hold lock)."""
        if client_id not in self._connections:
            return

        # Try to close the WebSocket gracefully
        websocket = self._connections[client_id]
        try:
            await websocket.close(code=code, reason=reason)
        except Exception:
            pass  # Connection may already be closed

        # Remove from all rooms
        for room_name in list(self._rooms.keys()):
            self._rooms[room_name].discard(client_id)
            if not self._rooms[room_name]:
                del self._rooms[room_name]

        # Clean up connection and metadata
        del self._connections[client_id]
        del self._metadata[client_id]

        logger.info(f"Client disconnected: {client_id} (remaining: {len(self._connections)})")

    # ==================== Room Management ====================

    async def join_room(self, client_id: str, room: str):
        """
        Subscribe client to a room.

        Args:
            client_id: The client joining the room
            room: Room name to join

        Example:
            await manager.join_room("user-123", "trading:SOL-USD")
        """
        async with self._lock:
            if client_id not in self._connections:
                logger.warning(f"Cannot join room: client {client_id} not connected")
                return

            if room not in self._rooms:
                self._rooms[room] = set()

            self._rooms[room].add(client_id)
            self._metadata[client_id].subscriptions.add(room)

            logger.debug(f"Client {client_id} joined room {room}")

    async def leave_room(self, client_id: str, room: str):
        """
        Unsubscribe client from a room.

        Args:
            client_id: The client leaving the room
            room: Room name to leave
        """
        async with self._lock:
            if room in self._rooms:
                self._rooms[room].discard(client_id)
                if not self._rooms[room]:
                    del self._rooms[room]

            if client_id in self._metadata:
                self._metadata[client_id].subscriptions.discard(room)

            logger.debug(f"Client {client_id} left room {room}")

    async def leave_all_rooms(self, client_id: str):
        """Remove client from all rooms."""
        async with self._lock:
            if client_id not in self._metadata:
                return

            rooms_to_leave = list(self._metadata[client_id].subscriptions)
            for room in rooms_to_leave:
                if room in self._rooms:
                    self._rooms[room].discard(client_id)
                    if not self._rooms[room]:
                        del self._rooms[room]

            self._metadata[client_id].subscriptions.clear()

    # ==================== Messaging ====================

    async def send_personal(
        self,
        client_id: str,
        message: Dict[str, Any]
    ) -> bool:
        """
        Send message to specific client.

        Args:
            client_id: Target client ID
            message: JSON-serializable message

        Returns:
            True if sent successfully, False if client disconnected

        Example:
            await manager.send_personal("user-123", {"type": "notification", "text": "Hello!"})
        """
        if client_id not in self._connections:
            return False

        websocket = self._connections[client_id]
        try:
            await websocket.send_json(message)
            self._total_messages_sent += 1

            if client_id in self._metadata:
                self._metadata[client_id].message_count += 1
                self._metadata[client_id].last_activity = datetime.utcnow()

            return True
        except Exception as e:
            logger.warning(f"Failed to send to {client_id}: {e}")
            await self.disconnect(client_id)
            return False

    async def broadcast(
        self,
        message: Dict[str, Any],
        exclude: Optional[Set[str]] = None
    ) -> int:
        """
        Send message to all connected clients.

        Args:
            message: JSON-serializable message
            exclude: Set of client IDs to skip

        Returns:
            Number of clients message was sent to

        Example:
            await manager.broadcast({"type": "system", "text": "Server restarting"})
        """
        exclude = exclude or set()
        sent_count = 0
        disconnected = []

        for client_id, websocket in list(self._connections.items()):
            if client_id in exclude:
                continue

            try:
                await websocket.send_json(message)
                sent_count += 1
                self._total_messages_sent += 1
            except Exception:
                disconnected.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected:
            await self.disconnect(client_id)

        return sent_count

    async def broadcast_to_room(
        self,
        room: str,
        message: Dict[str, Any],
        exclude: Optional[Set[str]] = None
    ) -> int:
        """
        Send message to all clients in a room.

        Args:
            room: Target room name
            message: JSON-serializable message
            exclude: Set of client IDs to skip

        Returns:
            Number of clients message was sent to

        Example:
            await manager.broadcast_to_room(
                "trading:SOL-USD",
                {"type": "price_update", "price": 150.25}
            )
        """
        if room not in self._rooms:
            return 0

        exclude = exclude or set()
        sent_count = 0
        disconnected = []

        for client_id in list(self._rooms.get(room, set())):
            if client_id in exclude:
                continue

            websocket = self._connections.get(client_id)
            if not websocket:
                continue

            try:
                await websocket.send_json(message)
                sent_count += 1
                self._total_messages_sent += 1
            except Exception:
                disconnected.append(client_id)

        for client_id in disconnected:
            await self.disconnect(client_id)

        return sent_count

    async def broadcast_to_rooms(
        self,
        rooms: List[str],
        message: Dict[str, Any],
        exclude: Optional[Set[str]] = None
    ) -> int:
        """Send message to multiple rooms (deduplicates clients in multiple rooms)."""
        exclude = exclude or set()

        # Collect unique client IDs across all rooms
        target_clients: Set[str] = set()
        for room in rooms:
            target_clients.update(self._rooms.get(room, set()))

        target_clients -= exclude

        sent_count = 0
        disconnected = []

        for client_id in target_clients:
            websocket = self._connections.get(client_id)
            if not websocket:
                continue

            try:
                await websocket.send_json(message)
                sent_count += 1
            except Exception:
                disconnected.append(client_id)

        for client_id in disconnected:
            await self.disconnect(client_id)

        return sent_count

    # ==================== Queries ====================

    @property
    def connection_count(self) -> int:
        """Number of active connections."""
        return len(self._connections)

    def is_connected(self, client_id: str) -> bool:
        """Check if a client is currently connected."""
        return client_id in self._connections

    def get_client_ids(self) -> List[str]:
        """Get list of all connected client IDs."""
        return list(self._connections.keys())

    def get_room_members(self, room: str) -> Set[str]:
        """Get all client IDs in a room (copy to prevent modification)."""
        return self._rooms.get(room, set()).copy()

    def get_room_count(self, room: str) -> int:
        """Get number of clients in a room."""
        return len(self._rooms.get(room, set()))

    def get_rooms(self) -> List[str]:
        """Get list of all active rooms."""
        return list(self._rooms.keys())

    def get_client_rooms(self, client_id: str) -> Set[str]:
        """Get all rooms a client has joined."""
        if client_id not in self._metadata:
            return set()
        return self._metadata[client_id].subscriptions.copy()

    def get_metadata(self, client_id: str) -> Optional[ConnectionMetadata]:
        """Get metadata for a specific client."""
        return self._metadata.get(client_id)

    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics."""
        return {
            "active_connections": len(self._connections),
            "total_connections_ever": self._total_connections,
            "total_messages_sent": self._total_messages_sent,
            "active_rooms": len(self._rooms),
            "room_breakdown": {
                room: len(members)
                for room, members in self._rooms.items()
            }
        }

    # ==================== Utilities ====================

    async def close_all(self, code: int = 1001, reason: str = "Server shutdown"):
        """
        Close all connections (for graceful shutdown).

        Args:
            code: WebSocket close code
            reason: Close reason message
        """
        async with self._lock:
            for client_id in list(self._connections.keys()):
                await self._disconnect_internal(client_id, code=code, reason=reason)

            self._rooms.clear()

        logger.info("All WebSocket connections closed")


# Singleton instance for import
manager = ConnectionManager()


# ==================== FastAPI Integration ====================

def create_websocket_router():
    """
    Create a FastAPI router with basic WebSocket endpoints.

    Returns configured APIRouter for WebSocket handling.

    Example:
        from fastapi import FastAPI
        from connection_manager import create_websocket_router

        app = FastAPI()
        app.include_router(create_websocket_router(), prefix="/ws")
    """
    from fastapi import APIRouter, WebSocket, WebSocketDisconnect

    router = APIRouter()

    @router.websocket("/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, client_id: str):
        """Basic WebSocket endpoint with room support."""
        if not await manager.connect(websocket, client_id):
            return

        try:
            while True:
                data = await websocket.receive_json()
                message_type = data.get("type")

                if message_type == "join":
                    room = data.get("room")
                    if room:
                        await manager.join_room(client_id, room)
                        await manager.send_personal(client_id, {
                            "type": "joined",
                            "room": room
                        })

                elif message_type == "leave":
                    room = data.get("room")
                    if room:
                        await manager.leave_room(client_id, room)
                        await manager.send_personal(client_id, {
                            "type": "left",
                            "room": room
                        })

                elif message_type == "message":
                    room = data.get("room", "general")
                    content = data.get("content")
                    await manager.broadcast_to_room(room, {
                        "type": "message",
                        "from": client_id,
                        "room": room,
                        "content": content
                    }, exclude={client_id})

                elif message_type == "pong":
                    # Heartbeat response - handled by heartbeat manager
                    pass

        except WebSocketDisconnect:
            pass
        finally:
            await manager.disconnect(client_id)

    return router


if __name__ == "__main__":
    # Quick test
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(create_websocket_router(), prefix="/ws")

    uvicorn.run(app, host="0.0.0.0", port=8000)
