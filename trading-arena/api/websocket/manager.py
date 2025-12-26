"""
Trading Arena WebSocket Connection Manager

Adapted from AI-CIV websocket-server-patterns skill for Trading Arena needs.

Features:
- Collective-aware connections (tracks collective_id per connection)
- Trading Arena room subscriptions:
  - portfolio:{collective_id} - Portfolio updates for a collective
  - orders:{collective_id} - Order execution updates for a collective
  - market - Global market data (prices, volume)
- Enhanced statistics for monitoring
- Thread-safe async operations

Usage:
    from api.websocket import manager

    @app.websocket("/ws/v1/{collective_id}")
    async def websocket_endpoint(websocket: WebSocket, collective_id: str):
        await manager.connect(websocket, collective_id)
        try:
            while True:
                data = await websocket.receive_json()
                await manager.handle_message(collective_id, data)
        except WebSocketDisconnect:
            await manager.disconnect(collective_id)

Skill Source: .claude/skills-reference/websocket-server-patterns/
Author: AI-CIV refactoring-specialist (adapted from capability-curator pattern)
Version: 1.0.0
Date: 2025-12-26
"""

from fastapi import WebSocket
from typing import Dict, Set, Optional, List, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import logging

logger = logging.getLogger(__name__)


class RoomType(Enum):
    """Trading Arena room types for subscription management."""
    PORTFOLIO = "portfolio"  # portfolio:{collective_id}
    ORDERS = "orders"        # orders:{collective_id}
    MARKET = "market"        # market (global)


@dataclass
class CollectiveConnectionMetadata:
    """
    Extended metadata for Trading Arena connections.
    
    Tracks collective identity and trading-specific activity.
    """
    connected_at: datetime
    collective_id: str
    subscriptions: Set[str] = field(default_factory=set)
    
    # Trading-specific tracking
    orders_received: int = 0
    portfolio_updates_received: int = 0
    market_updates_received: int = 0
    
    # General tracking
    message_count: int = 0
    last_activity: datetime = field(default_factory=datetime.utcnow)
    
    # Authentication state
    is_authenticated: bool = False
    auth_method: Optional[str] = None  # "ed25519" or None


class TradingArenaConnectionManager:
    """
    Trading Arena WebSocket connection manager.
    
    Extended from base ConnectionManager pattern with:
    - Collective identity tracking
    - Trading-specific room types (portfolio, orders, market)
    - Enhanced statistics for arena monitoring
    
    Room naming conventions:
        portfolio:{collective_id} - Portfolio changes (positions, balance)
        orders:{collective_id} - Order lifecycle (placed, filled, cancelled)
        market - Global market data (available to all)
    
    Example:
        manager = TradingArenaConnectionManager()
        
        # Connect a collective
        await manager.connect(websocket, "team-alpha")
        
        # Auto-subscribe to collective's rooms
        await manager.subscribe_collective_rooms("team-alpha")
        
        # Broadcast portfolio update
        await manager.broadcast_portfolio_update("team-alpha", {
            "type": "position_update",
            "symbol": "SOL-USD",
            "quantity": 10
        })
    """
    
    def __init__(self):
        # Core state - keyed by collective_id
        self._connections: Dict[str, WebSocket] = {}
        self._metadata: Dict[str, CollectiveConnectionMetadata] = {}
        self._rooms: Dict[str, Set[str]] = {}
        
        # Thread safety
        self._lock = asyncio.Lock()
        
        # Statistics
        self._total_connections = 0
        self._total_messages_sent = 0
        self._total_portfolio_broadcasts = 0
        self._total_order_broadcasts = 0
        self._total_market_broadcasts = 0
        
        # Initialize market room (always exists)
        self._rooms["market"] = set()
    
    # ==================== Room Name Helpers ====================
    
    @staticmethod
    def portfolio_room(collective_id: str) -> str:
        """Get portfolio room name for a collective."""
        return f"portfolio:{collective_id}"
    
    @staticmethod
    def orders_room(collective_id: str) -> str:
        """Get orders room name for a collective."""
        return f"orders:{collective_id}"
    
    @staticmethod
    def market_room() -> str:
        """Get global market room name."""
        return "market"
    
    # ==================== Connection Lifecycle ====================
    
    async def connect(
        self,
        websocket: WebSocket,
        collective_id: str,
        auto_subscribe: bool = True,
        replace_existing: bool = True
    ) -> bool:
        """
        Accept WebSocket connection and register collective.
        
        Args:
            websocket: The WebSocket connection
            collective_id: The collective's unique identifier
            auto_subscribe: If True, auto-subscribe to collective's rooms
            replace_existing: If True, disconnect existing connection with same ID
            
        Returns:
            True if connection accepted, False if rejected
        """
        async with self._lock:
            # Handle existing connection with same collective
            if collective_id in self._connections:
                if replace_existing:
                    await self._disconnect_internal(
                        collective_id, 
                        code=4011, 
                        reason="Superseded by new connection"
                    )
                else:
                    logger.warning(f"Rejected duplicate connection: {collective_id}")
                    return False
            
            # Accept the new connection
            await websocket.accept()
            
            # Register connection
            self._connections[collective_id] = websocket
            self._metadata[collective_id] = CollectiveConnectionMetadata(
                connected_at=datetime.utcnow(),
                collective_id=collective_id
            )
            
            self._total_connections += 1
            
            logger.info(
                f"Collective connected: {collective_id} "
                f"(total: {len(self._connections)})"
            )
            
        # Auto-subscribe to collective's rooms (outside lock to avoid deadlock)
        if auto_subscribe:
            await self.subscribe_collective_rooms(collective_id)
        
        return True
    
    async def disconnect(self, collective_id: str):
        """
        Disconnect collective and clean up all associated state.
        
        Removes collective from all rooms and cleans up metadata.
        """
        async with self._lock:
            await self._disconnect_internal(collective_id)
    
    async def _disconnect_internal(
        self,
        collective_id: str,
        code: int = 1000,
        reason: str = "Normal closure"
    ):
        """Internal disconnect without acquiring lock (caller must hold lock)."""
        if collective_id not in self._connections:
            return
        
        # Try to close the WebSocket gracefully
        websocket = self._connections[collective_id]
        try:
            await websocket.close(code=code, reason=reason)
        except Exception:
            pass  # Connection may already be closed
        
        # Remove from all rooms
        for room_name in list(self._rooms.keys()):
            self._rooms[room_name].discard(collective_id)
            # Don't delete market room even if empty
            if not self._rooms[room_name] and room_name != "market":
                del self._rooms[room_name]
        
        # Clean up connection and metadata
        del self._connections[collective_id]
        del self._metadata[collective_id]
        
        logger.info(
            f"Collective disconnected: {collective_id} "
            f"(remaining: {len(self._connections)})"
        )
    
    # ==================== Room Management ====================
    
    async def subscribe_collective_rooms(self, collective_id: str):
        """
        Subscribe collective to their standard rooms.
        
        Subscribes to:
        - portfolio:{collective_id}
        - orders:{collective_id}
        - market (global)
        """
        await self.join_room(collective_id, self.portfolio_room(collective_id))
        await self.join_room(collective_id, self.orders_room(collective_id))
        await self.join_room(collective_id, self.market_room())
    
    async def join_room(self, collective_id: str, room: str):
        """Subscribe collective to a room."""
        async with self._lock:
            if collective_id not in self._connections:
                logger.warning(
                    f"Cannot join room: collective {collective_id} not connected"
                )
                return
            
            if room not in self._rooms:
                self._rooms[room] = set()
            
            self._rooms[room].add(collective_id)
            self._metadata[collective_id].subscriptions.add(room)
            
            logger.debug(f"Collective {collective_id} joined room {room}")
    
    async def leave_room(self, collective_id: str, room: str):
        """Unsubscribe collective from a room."""
        async with self._lock:
            if room in self._rooms:
                self._rooms[room].discard(collective_id)
                # Don't delete market room even if empty
                if not self._rooms[room] and room != "market":
                    del self._rooms[room]
            
            if collective_id in self._metadata:
                self._metadata[collective_id].subscriptions.discard(room)
            
            logger.debug(f"Collective {collective_id} left room {room}")
    
    # ==================== Trading Arena Messaging ====================
    
    async def broadcast_portfolio_update(
        self,
        collective_id: str,
        update: Dict[str, Any]
    ) -> int:
        """
        Broadcast portfolio update to a collective.
        
        Args:
            collective_id: Target collective
            update: Portfolio update data
            
        Returns:
            Number of connections that received the message
        """
        message = {
            "type": "portfolio_update",
            "collective_id": collective_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": update
        }
        
        count = await self.broadcast_to_room(
            self.portfolio_room(collective_id),
            message
        )
        
        self._total_portfolio_broadcasts += 1
        
        # Update metadata for recipients
        async with self._lock:
            if collective_id in self._metadata:
                self._metadata[collective_id].portfolio_updates_received += 1
        
        return count
    
    async def broadcast_order_update(
        self,
        collective_id: str,
        update: Dict[str, Any]
    ) -> int:
        """
        Broadcast order update to a collective.
        
        Args:
            collective_id: Target collective
            update: Order update data (placed, filled, cancelled, etc.)
            
        Returns:
            Number of connections that received the message
        """
        message = {
            "type": "order_update",
            "collective_id": collective_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": update
        }
        
        count = await self.broadcast_to_room(
            self.orders_room(collective_id),
            message
        )
        
        self._total_order_broadcasts += 1
        
        # Update metadata for recipients
        async with self._lock:
            if collective_id in self._metadata:
                self._metadata[collective_id].orders_received += 1
        
        return count
    
    async def broadcast_market_update(
        self,
        update: Dict[str, Any]
    ) -> int:
        """
        Broadcast market data to all connected collectives.
        
        Args:
            update: Market data (prices, volume, etc.)
            
        Returns:
            Number of connections that received the message
        """
        message = {
            "type": "market_update",
            "timestamp": datetime.utcnow().isoformat(),
            "data": update
        }
        
        count = await self.broadcast_to_room(self.market_room(), message)
        self._total_market_broadcasts += 1
        
        # Update metadata for all recipients
        async with self._lock:
            for collective_id in self._rooms.get("market", set()):
                if collective_id in self._metadata:
                    self._metadata[collective_id].market_updates_received += 1
        
        return count
    
    # ==================== Base Messaging ====================
    
    async def send_personal(
        self,
        collective_id: str,
        message: Dict[str, Any]
    ) -> bool:
        """
        Send message to specific collective.
        
        Args:
            collective_id: Target collective ID
            message: JSON-serializable message
            
        Returns:
            True if sent successfully, False if collective disconnected
        """
        if collective_id not in self._connections:
            return False
        
        websocket = self._connections[collective_id]
        try:
            await websocket.send_json(message)
            self._total_messages_sent += 1
            
            async with self._lock:
                if collective_id in self._metadata:
                    self._metadata[collective_id].message_count += 1
                    self._metadata[collective_id].last_activity = datetime.utcnow()
            
            return True
        except Exception as e:
            logger.warning(f"Failed to send to {collective_id}: {e}")
            await self.disconnect(collective_id)
            return False
    
    async def broadcast(
        self,
        message: Dict[str, Any],
        exclude: Optional[Set[str]] = None
    ) -> int:
        """
        Send message to all connected collectives.
        
        Args:
            message: JSON-serializable message
            exclude: Set of collective IDs to skip
            
        Returns:
            Number of collectives message was sent to
        """
        exclude = exclude or set()
        sent_count = 0
        disconnected = []
        
        for collective_id, websocket in list(self._connections.items()):
            if collective_id in exclude:
                continue
            
            try:
                await websocket.send_json(message)
                sent_count += 1
                self._total_messages_sent += 1
            except Exception:
                disconnected.append(collective_id)
        
        # Clean up disconnected collectives
        for collective_id in disconnected:
            await self.disconnect(collective_id)
        
        return sent_count
    
    async def broadcast_to_room(
        self,
        room: str,
        message: Dict[str, Any],
        exclude: Optional[Set[str]] = None
    ) -> int:
        """
        Send message to all collectives in a room.
        
        Args:
            room: Target room name
            message: JSON-serializable message
            exclude: Set of collective IDs to skip
            
        Returns:
            Number of collectives message was sent to
        """
        if room not in self._rooms:
            return 0
        
        exclude = exclude or set()
        sent_count = 0
        disconnected = []
        
        for collective_id in list(self._rooms.get(room, set())):
            if collective_id in exclude:
                continue
            
            websocket = self._connections.get(collective_id)
            if not websocket:
                continue
            
            try:
                await websocket.send_json(message)
                sent_count += 1
                self._total_messages_sent += 1
            except Exception:
                disconnected.append(collective_id)
        
        for collective_id in disconnected:
            await self.disconnect(collective_id)
        
        return sent_count
    
    # ==================== Queries ====================
    
    @property
    def connection_count(self) -> int:
        """Number of active connections."""
        return len(self._connections)
    
    def is_connected(self, collective_id: str) -> bool:
        """Check if a collective is currently connected."""
        return collective_id in self._connections
    
    def get_connected_collectives(self) -> List[str]:
        """Get list of all connected collective IDs."""
        return list(self._connections.keys())
    
    def get_room_members(self, room: str) -> Set[str]:
        """Get all collective IDs in a room (copy to prevent modification)."""
        return self._rooms.get(room, set()).copy()
    
    def get_metadata(self, collective_id: str) -> Optional[CollectiveConnectionMetadata]:
        """Get metadata for a specific collective."""
        return self._metadata.get(collective_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive manager statistics.
        
        Returns statistics suitable for monitoring dashboard.
        """
        # Count room types
        portfolio_rooms = sum(1 for r in self._rooms if r.startswith("portfolio:"))
        orders_rooms = sum(1 for r in self._rooms if r.startswith("orders:"))
        
        return {
            # Connection stats
            "active_connections": len(self._connections),
            "total_connections_ever": self._total_connections,
            
            # Message stats
            "total_messages_sent": self._total_messages_sent,
            "portfolio_broadcasts": self._total_portfolio_broadcasts,
            "order_broadcasts": self._total_order_broadcasts,
            "market_broadcasts": self._total_market_broadcasts,
            
            # Room stats
            "active_rooms": len(self._rooms),
            "portfolio_rooms": portfolio_rooms,
            "orders_rooms": orders_rooms,
            "market_subscribers": len(self._rooms.get("market", set())),
            
            # Room breakdown
            "room_breakdown": {
                room: len(members)
                for room, members in self._rooms.items()
            },
            
            # Per-collective stats
            "collective_stats": {
                cid: {
                    "connected_at": meta.connected_at.isoformat(),
                    "subscriptions": list(meta.subscriptions),
                    "message_count": meta.message_count,
                    "portfolio_updates": meta.portfolio_updates_received,
                    "order_updates": meta.orders_received,
                    "market_updates": meta.market_updates_received,
                    "last_activity": meta.last_activity.isoformat()
                }
                for cid, meta in self._metadata.items()
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
            for collective_id in list(self._connections.keys()):
                await self._disconnect_internal(
                    collective_id, 
                    code=code, 
                    reason=reason
                )
            
            # Reset rooms but keep market
            self._rooms = {"market": set()}
        
        logger.info("All WebSocket connections closed")
    
    async def handle_message(
        self,
        collective_id: str,
        data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Handle incoming WebSocket message from collective.
        
        Processes subscription management and returns response if needed.
        
        Args:
            collective_id: The sending collective
            data: Parsed JSON message
            
        Returns:
            Response dict if message requires response, None otherwise
        """
        message_type = data.get("type")
        
        if message_type == "subscribe":
            room = data.get("room")
            if room:
                await self.join_room(collective_id, room)
                return {"type": "subscribed", "room": room}
        
        elif message_type == "unsubscribe":
            room = data.get("room")
            if room:
                await self.leave_room(collective_id, room)
                return {"type": "unsubscribed", "room": room}
        
        elif message_type == "ping":
            return {"type": "pong", "timestamp": datetime.utcnow().isoformat()}
        
        elif message_type == "stats":
            # Return collective-specific stats
            meta = self.get_metadata(collective_id)
            if meta:
                return {
                    "type": "stats",
                    "subscriptions": list(meta.subscriptions),
                    "message_count": meta.message_count,
                    "connected_at": meta.connected_at.isoformat()
                }
        
        return None


# Singleton instance for import
manager = TradingArenaConnectionManager()
