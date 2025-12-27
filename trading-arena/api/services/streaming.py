"""
Trading Arena Real-Time Streaming Service

Work Stream F: Real-time event streaming for Trading Arena Phase 2.

This service provides a clean interface for broadcasting real-time updates
to connected WebSocket clients. It integrates with the existing WebSocket
infrastructure (manager, handlers) and is called from order/portfolio routes
when state changes occur.

Event Types:
    portfolio_update - Broadcast when collective balances change
        {
            "type": "portfolio_update",
            "collective_id": "team-alpha",
            "balances": {"USDC": {"total": 10000, "available": 9500, "reserved": 500}},
            "total_value": 10000.0,
            "timestamp": "2025-12-26T12:00:00Z"
        }

    order_update - Broadcast when order status changes
        {
            "type": "order_update",
            "collective_id": "team-alpha",
            "order_id": "arena-ord-abc123",
            "status": "filled",
            "filled_quantity": 10.0,
            "remaining_quantity": 0.0,
            "average_fill_price": 100.50,
            "timestamp": "2025-12-26T12:00:00Z"
        }

    market_update - Broadcast price/volume ticks (global, all collectives)
        {
            "type": "market_update",
            "symbol": "SOL/USDC",
            "price": 95.50,
            "volume_24h": 1000000.0,
            "change_24h_percent": 2.5,
            "timestamp": "2025-12-26T12:00:00Z"
        }

Integration Points:
    - Called from orders.py when orders are placed, filled, or cancelled
    - Called from portfolio.py when balances are updated
    - Called from market data service when prices change (future)
    - Uses TradingArenaConnectionManager.broadcast_* methods

Usage:
    from api.services.streaming import streaming_service

    # Broadcast portfolio update
    await streaming_service.broadcast_portfolio_update(
        collective_id="team-alpha",
        balances={"USDC": {"total": 10000, "available": 9500, "reserved": 500}}
    )

    # Broadcast order update
    await streaming_service.broadcast_order_update(
        collective_id="team-alpha",
        order_id="arena-ord-abc123",
        status="filled",
        filled_quantity=10.0
    )

    # Broadcast market data (to all)
    await streaming_service.broadcast_market_update(
        symbol="SOL/USDC",
        price=95.50,
        volume_24h=1000000.0
    )

Author: refactoring-specialist (AI-CIV Phase 2)
Version: 1.0.0
Date: 2025-12-26
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """Streaming event types for WebSocket broadcasts."""
    PORTFOLIO_UPDATE = "portfolio_update"
    ORDER_UPDATE = "order_update"
    MARKET_UPDATE = "market_update"


class OrderEventType(str, Enum):
    """Sub-types for order update events."""
    CREATED = "created"      # New order placed
    FILLED = "filled"        # Order fully filled
    PARTIAL_FILL = "partial_fill"  # Order partially filled
    CANCELLED = "cancelled"  # Order cancelled
    EXPIRED = "expired"      # Order expired
    REJECTED = "rejected"    # Order rejected


@dataclass
class StreamingStats:
    """Statistics for streaming service monitoring."""
    portfolio_broadcasts: int = 0
    order_broadcasts: int = 0
    market_broadcasts: int = 0
    total_messages_sent: int = 0
    last_broadcast_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "portfolio_broadcasts": self.portfolio_broadcasts,
            "order_broadcasts": self.order_broadcasts,
            "market_broadcasts": self.market_broadcasts,
            "total_messages_sent": self.total_messages_sent,
            "last_broadcast_at": (
                self.last_broadcast_at.isoformat()
                if self.last_broadcast_at else None
            )
        }


class StreamingService:
    """
    Real-time streaming service for Trading Arena.

    Provides a high-level interface for broadcasting updates to connected
    WebSocket clients. This service sits between business logic (routes)
    and the WebSocket infrastructure (manager).

    Design Principles:
        1. Separation of Concerns - Routes handle business logic,
           this service handles streaming coordination
        2. Fail-Safe - Broadcasting failures don't break core operations
        3. Observable - Statistics tracked for monitoring
        4. Testable - Manager can be injected for testing

    Example:
        service = StreamingService()

        # After order fill
        await service.broadcast_order_update(
            collective_id="team-alpha",
            order_id="arena-ord-abc123",
            status="filled",
            filled_quantity=10.0,
            average_fill_price=100.50
        )

        # After balance change
        await service.broadcast_portfolio_update(
            collective_id="team-alpha",
            balances=new_balances
        )
    """

    def __init__(self):
        """Initialize streaming service."""
        self._stats = StreamingStats()
        self._manager = None  # Lazy-loaded to avoid circular imports
        
    def _get_manager(self):
        """
        Get the WebSocket connection manager (lazy-loaded).

        Returns None if manager not available (graceful degradation).
        """
        if self._manager is None:
            try:
                from ..websocket.manager import manager
                self._manager = manager
            except ImportError:
                logger.warning("WebSocket manager not available - streaming disabled")
                return None
        return self._manager

    def set_manager(self, manager) -> None:
        """
        Set the connection manager (for testing).

        Args:
            manager: TradingArenaConnectionManager instance
        """
        self._manager = manager

    # =========================================================================
    # Portfolio Updates
    # =========================================================================

    async def broadcast_portfolio_update(
        self,
        collective_id: str,
        balances: Dict[str, Dict[str, float]],
        total_value: Optional[float] = None,
        positions: Optional[List[Dict[str, Any]]] = None,
        summary: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Broadcast portfolio update to a collective.

        Called when:
            - Balances change (deposits, withdrawals, trades)
            - Positions are updated (new positions, closed positions)
            - Portfolio summary metrics change

        Args:
            collective_id: Target collective
            balances: Current balance state by currency
                Example: {"USDC": {"total": 10000, "available": 9500, "reserved": 500}}
            total_value: Optional pre-calculated total portfolio value in USDC
            positions: Optional list of current positions
            summary: Optional summary metrics (PnL, etc.)

        Returns:
            Number of connections that received the broadcast

        Example:
            await service.broadcast_portfolio_update(
                collective_id="team-alpha",
                balances={
                    "USDC": {"total": 9500, "available": 9000, "reserved": 500},
                    "SOL": {"total": 10.0, "available": 10.0, "reserved": 0.0}
                },
                total_value=10450.00
            )
        """
        manager = self._get_manager()
        if manager is None:
            logger.debug(f"Streaming disabled - portfolio update for {collective_id} skipped")
            return 0

        # Calculate total value if not provided
        if total_value is None:
            total_value = sum(
                balance.get("total", 0)
                for balance in balances.values()
            )

        now = datetime.now(timezone.utc)

        update_data = {
            "collective_id": collective_id,
            "balances": balances,
            "total_value": total_value,
            "timestamp": now.isoformat()
        }

        # Include optional fields if provided
        if positions is not None:
            update_data["positions"] = positions
        if summary is not None:
            update_data["summary"] = summary

        try:
            count = await manager.broadcast_portfolio_update(
                collective_id=collective_id,
                update=update_data
            )

            self._stats.portfolio_broadcasts += 1
            self._stats.total_messages_sent += count
            self._stats.last_broadcast_at = now

            logger.debug(
                f"Portfolio update broadcast to {count} connection(s) "
                f"for {collective_id}"
            )
            return count

        except Exception as e:
            logger.error(
                f"Failed to broadcast portfolio update for {collective_id}: {e}",
                exc_info=True
            )
            return 0

    # =========================================================================
    # Order Updates
    # =========================================================================

    async def broadcast_order_update(
        self,
        collective_id: str,
        order_id: str,
        status: str,
        event_type: Optional[str] = None,
        filled_quantity: Optional[float] = None,
        remaining_quantity: Optional[float] = None,
        average_fill_price: Optional[float] = None,
        symbol: Optional[str] = None,
        side: Optional[str] = None,
        fill_price: Optional[float] = None,
        fill_quantity: Optional[float] = None,
        reject_reason: Optional[str] = None
    ) -> int:
        """
        Broadcast order update to a collective.

        Called when:
            - New order is placed (created)
            - Order receives a fill (partial_fill, filled)
            - Order is cancelled (cancelled)
            - Order expires (expired)
            - Order is rejected (rejected)

        Args:
            collective_id: Target collective
            order_id: The order identifier
            status: Current order status (open, filled, cancelled, etc.)
            event_type: Optional specific event type (created, filled, etc.)
            filled_quantity: Total quantity filled so far
            remaining_quantity: Quantity still to be filled
            average_fill_price: Volume-weighted average fill price
            symbol: Trading pair (e.g., "SOL/USDC")
            side: Order side ("buy" or "sell")
            fill_price: Price of the most recent fill (for fill events)
            fill_quantity: Quantity of the most recent fill (for fill events)
            reject_reason: Reason for rejection (for rejected events)

        Returns:
            Number of connections that received the broadcast

        Example - New Order:
            await service.broadcast_order_update(
                collective_id="team-alpha",
                order_id="arena-ord-abc123",
                status="open",
                event_type="created",
                symbol="SOL/USDC",
                side="buy"
            )

        Example - Fill:
            await service.broadcast_order_update(
                collective_id="team-alpha",
                order_id="arena-ord-abc123",
                status="filled",
                event_type="filled",
                filled_quantity=10.0,
                remaining_quantity=0.0,
                average_fill_price=100.50,
                fill_price=100.50,
                fill_quantity=10.0
            )
        """
        manager = self._get_manager()
        if manager is None:
            logger.debug(f"Streaming disabled - order update for {order_id} skipped")
            return 0

        now = datetime.now(timezone.utc)

        update_data = {
            "collective_id": collective_id,
            "order_id": order_id,
            "status": status,
            "timestamp": now.isoformat()
        }

        # Include event type if provided (for more granular client handling)
        if event_type:
            update_data["event_type"] = event_type

        # Include fill information
        if filled_quantity is not None:
            update_data["filled_quantity"] = filled_quantity
        if remaining_quantity is not None:
            update_data["remaining_quantity"] = remaining_quantity
        if average_fill_price is not None:
            update_data["average_fill_price"] = average_fill_price

        # Include order details
        if symbol:
            update_data["symbol"] = symbol
        if side:
            update_data["side"] = side

        # Include most recent fill details (for fill events)
        if fill_price is not None:
            update_data["fill_price"] = fill_price
        if fill_quantity is not None:
            update_data["fill_quantity"] = fill_quantity

        # Include rejection reason
        if reject_reason:
            update_data["reject_reason"] = reject_reason

        try:
            count = await manager.broadcast_order_update(
                collective_id=collective_id,
                update=update_data
            )

            self._stats.order_broadcasts += 1
            self._stats.total_messages_sent += count
            self._stats.last_broadcast_at = now

            logger.debug(
                f"Order update broadcast to {count} connection(s) "
                f"for {collective_id}/{order_id}"
            )
            return count

        except Exception as e:
            logger.error(
                f"Failed to broadcast order update for {order_id}: {e}",
                exc_info=True
            )
            return 0

    async def broadcast_order_created(
        self,
        collective_id: str,
        order_id: str,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None
    ) -> int:
        """
        Convenience method for broadcasting new order creation.

        Args:
            collective_id: Target collective
            order_id: The new order identifier
            symbol: Trading pair
            side: Order side
            order_type: Order type (market, limit)
            quantity: Order quantity
            price: Limit price (None for market orders)

        Returns:
            Number of connections that received the broadcast
        """
        return await self.broadcast_order_update(
            collective_id=collective_id,
            order_id=order_id,
            status="open",
            event_type=OrderEventType.CREATED.value,
            symbol=symbol,
            side=side,
            remaining_quantity=quantity,
            filled_quantity=0.0
        )

    async def broadcast_order_filled(
        self,
        collective_id: str,
        order_id: str,
        filled_quantity: float,
        average_fill_price: float,
        symbol: Optional[str] = None,
        side: Optional[str] = None,
        is_partial: bool = False
    ) -> int:
        """
        Convenience method for broadcasting order fill events.

        Args:
            collective_id: Target collective
            order_id: The filled order identifier
            filled_quantity: Total quantity filled
            average_fill_price: Average fill price
            symbol: Optional trading pair
            side: Optional order side
            is_partial: True if this is a partial fill

        Returns:
            Number of connections that received the broadcast
        """
        event_type = (
            OrderEventType.PARTIAL_FILL.value if is_partial
            else OrderEventType.FILLED.value
        )
        status = "partially_filled" if is_partial else "filled"

        return await self.broadcast_order_update(
            collective_id=collective_id,
            order_id=order_id,
            status=status,
            event_type=event_type,
            filled_quantity=filled_quantity,
            average_fill_price=average_fill_price,
            remaining_quantity=0.0 if not is_partial else None,
            symbol=symbol,
            side=side
        )

    async def broadcast_order_cancelled(
        self,
        collective_id: str,
        order_id: str,
        filled_quantity: float = 0.0,
        remaining_quantity: float = 0.0,
        symbol: Optional[str] = None
    ) -> int:
        """
        Convenience method for broadcasting order cancellation.

        Args:
            collective_id: Target collective
            order_id: The cancelled order identifier
            filled_quantity: Amount filled before cancellation
            remaining_quantity: Amount remaining (cancelled portion)
            symbol: Optional trading pair

        Returns:
            Number of connections that received the broadcast
        """
        return await self.broadcast_order_update(
            collective_id=collective_id,
            order_id=order_id,
            status="cancelled",
            event_type=OrderEventType.CANCELLED.value,
            filled_quantity=filled_quantity,
            remaining_quantity=remaining_quantity,
            symbol=symbol
        )

    # =========================================================================
    # Market Updates
    # =========================================================================

    async def broadcast_market_update(
        self,
        symbol: str,
        price: float,
        volume_24h: Optional[float] = None,
        change_24h_percent: Optional[float] = None,
        bid: Optional[float] = None,
        ask: Optional[float] = None,
        high_24h: Optional[float] = None,
        low_24h: Optional[float] = None
    ) -> int:
        """
        Broadcast market data update to all connected collectives.

        Called when:
            - Price changes (from market data feed)
            - Volume statistics update
            - Bid/ask spread changes

        Args:
            symbol: Trading pair (e.g., "SOL/USDC")
            price: Current price (last trade or mid-market)
            volume_24h: 24-hour trading volume
            change_24h_percent: 24-hour price change percentage
            bid: Best bid price
            ask: Best ask price
            high_24h: 24-hour high price
            low_24h: 24-hour low price

        Returns:
            Number of connections that received the broadcast

        Example:
            await service.broadcast_market_update(
                symbol="SOL/USDC",
                price=95.50,
                volume_24h=1500000.0,
                change_24h_percent=2.5,
                bid=95.48,
                ask=95.52,
                high_24h=98.00,
                low_24h=92.00
            )
        """
        manager = self._get_manager()
        if manager is None:
            logger.debug(f"Streaming disabled - market update for {symbol} skipped")
            return 0

        now = datetime.now(timezone.utc)

        update_data = {
            "symbol": symbol,
            "price": price,
            "timestamp": now.isoformat()
        }

        # Include optional market data fields
        if volume_24h is not None:
            update_data["volume_24h"] = volume_24h
        if change_24h_percent is not None:
            update_data["change_24h_percent"] = change_24h_percent
        if bid is not None:
            update_data["bid"] = bid
        if ask is not None:
            update_data["ask"] = ask
        if high_24h is not None:
            update_data["high_24h"] = high_24h
        if low_24h is not None:
            update_data["low_24h"] = low_24h

        try:
            count = await manager.broadcast_market_update(update=update_data)

            self._stats.market_broadcasts += 1
            self._stats.total_messages_sent += count
            self._stats.last_broadcast_at = now

            logger.debug(
                f"Market update broadcast to {count} connection(s) for {symbol}"
            )
            return count

        except Exception as e:
            logger.error(
                f"Failed to broadcast market update for {symbol}: {e}",
                exc_info=True
            )
            return 0

    async def broadcast_market_tick(
        self,
        symbol: str,
        price: float,
        volume: Optional[float] = None
    ) -> int:
        """
        Convenience method for simple price tick broadcasts.

        Lighter-weight than broadcast_market_update for high-frequency ticks.

        Args:
            symbol: Trading pair
            price: Current price
            volume: Trade volume (optional)

        Returns:
            Number of connections that received the broadcast
        """
        return await self.broadcast_market_update(
            symbol=symbol,
            price=price,
            volume_24h=volume
        )

    # =========================================================================
    # Statistics & Monitoring
    # =========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """
        Get streaming service statistics.

        Returns statistics suitable for monitoring dashboards.

        Returns:
            Dictionary with broadcast counts and timing information
        """
        stats = self._stats.to_dict()

        # Add manager statistics if available
        manager = self._get_manager()
        if manager:
            manager_stats = manager.get_stats()
            stats["connections"] = {
                "active": manager_stats.get("active_connections", 0),
                "total_ever": manager_stats.get("total_connections_ever", 0),
                "market_subscribers": manager_stats.get("market_subscribers", 0)
            }

        return stats

    def reset_stats(self) -> None:
        """Reset streaming statistics (for testing)."""
        self._stats = StreamingStats()


# Singleton instance for application-wide use
streaming_service = StreamingService()
