"""
Trading Arena WebSocket Message Handlers

Work Stream E.4: Message handling for real-time trading operations.

This module provides message handlers for WebSocket operations without
implementing business logic - handlers delegate to the existing REST routes.

Supported Message Types:
    Portfolio Operations:
        - get_portfolio: Retrieve current portfolio state
        - get_balances: Retrieve balance details
    
    Order Operations:
        - place_order: Submit a new order
        - cancel_order: Cancel an existing order
        - get_orders: List orders with optional filters
        - get_order: Get details of a specific order
    
    Market Data:
        - subscribe_market: Subscribe to market data updates
        - unsubscribe_market: Unsubscribe from market updates
        - get_symbols: List available trading symbols

Message Format (Inbound):
    {
        "id": "msg-123",          # Optional request ID for correlation
        "type": "get_portfolio",  # Required message type
        "data": { ... }           # Optional payload for the operation
    }

Response Format (Outbound):
    {
        "id": "msg-123",          # Echoed request ID if provided
        "type": "portfolio",      # Response type
        "success": true,          # Operation success flag
        "data": { ... },          # Response payload
        "timestamp": "ISO8601"    # Server timestamp
    }

Error Response Format:
    {
        "id": "msg-123",
        "type": "error",
        "success": false,
        "error": {
            "code": "INVALID_REQUEST",
            "message": "Human-readable description"
        },
        "timestamp": "ISO8601"
    }

Author: refactoring-specialist (AI-CIV Phase 2)
Version: 1.0.0
Date: 2025-12-26
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, Optional, TypeVar

logger = logging.getLogger(__name__)


# =============================================================================
# Message Types & Error Codes
# =============================================================================

class MessageType(str, Enum):
    """Supported inbound message types."""
    # Portfolio
    GET_PORTFOLIO = "get_portfolio"
    GET_BALANCES = "get_balances"
    
    # Orders
    PLACE_ORDER = "place_order"
    CANCEL_ORDER = "cancel_order"
    GET_ORDERS = "get_orders"
    GET_ORDER = "get_order"
    
    # Market Data
    SUBSCRIBE_MARKET = "subscribe_market"
    UNSUBSCRIBE_MARKET = "unsubscribe_market"
    GET_SYMBOLS = "get_symbols"
    
    # Protocol
    PING = "ping"


class ErrorCode(str, Enum):
    """Standard error codes for WebSocket responses."""
    INVALID_REQUEST = "INVALID_REQUEST"
    INVALID_MESSAGE_TYPE = "INVALID_MESSAGE_TYPE"
    MISSING_FIELD = "MISSING_FIELD"
    INVALID_FIELD = "INVALID_FIELD"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    INTERNAL_ERROR = "INTERNAL_ERROR"


# =============================================================================
# Response Builders
# =============================================================================

@dataclass
class HandlerResult:
    """
    Result from a message handler.
    
    Encapsulates success/error state with structured data.
    """
    success: bool
    response_type: str
    data: Optional[Dict[str, Any]] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    
    def to_message(self, request_id: Optional[str] = None) -> Dict[str, Any]:
        """Convert to outbound message format."""
        message = {
            "type": self.response_type,
            "success": self.success,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        if request_id:
            message["id"] = request_id
        
        if self.success:
            message["data"] = self.data or {}
        else:
            message["error"] = {
                "code": self.error_code or ErrorCode.INTERNAL_ERROR,
                "message": self.error_message or "An error occurred"
            }
        
        return message


def success_result(response_type: str, data: Dict[str, Any]) -> HandlerResult:
    """Create a successful handler result."""
    return HandlerResult(
        success=True,
        response_type=response_type,
        data=data
    )


def error_result(
    response_type: str,
    code: ErrorCode,
    message: str
) -> HandlerResult:
    """Create an error handler result."""
    return HandlerResult(
        success=False,
        response_type=response_type,
        error_code=code.value,
        error_message=message
    )


# =============================================================================
# Base Handler
# =============================================================================

class MessageHandler(ABC):
    """
    Abstract base class for message handlers.
    
    Each handler processes a specific message type and returns
    a structured result.
    """
    
    @property
    @abstractmethod
    def message_type(self) -> MessageType:
        """The message type this handler processes."""
        pass
    
    @property
    @abstractmethod
    def response_type(self) -> str:
        """The response type to use in outbound messages."""
        pass
    
    @abstractmethod
    async def handle(
        self,
        collective_id: str,
        data: Dict[str, Any]
    ) -> HandlerResult:
        """
        Handle the message.
        
        Args:
            collective_id: The authenticated collective ID
            data: The message payload (contents of "data" field)
        
        Returns:
            HandlerResult with success/error state
        """
        pass
    
    def validate_required_fields(
        self,
        data: Dict[str, Any],
        fields: list[str]
    ) -> Optional[HandlerResult]:
        """
        Validate that required fields are present.
        
        Returns None if valid, or an error result if missing fields.
        """
        missing = [f for f in fields if f not in data or data[f] is None]
        if missing:
            return error_result(
                self.response_type,
                ErrorCode.MISSING_FIELD,
                f"Missing required field(s): {', '.join(missing)}"
            )
        return None


# =============================================================================
# Portfolio Handlers
# =============================================================================

class GetPortfolioHandler(MessageHandler):
    """Handler for get_portfolio messages."""
    
    @property
    def message_type(self) -> MessageType:
        return MessageType.GET_PORTFOLIO
    
    @property
    def response_type(self) -> str:
        return "portfolio"
    
    async def handle(
        self,
        collective_id: str,
        data: Dict[str, Any]
    ) -> HandlerResult:
        """
        Get current portfolio state.
        
        Delegates to portfolio route logic.
        """
        # Import here to avoid circular imports
        from ..routes.portfolio import get_or_create_portfolio
        
        try:
            balances = get_or_create_portfolio(collective_id)
            now = datetime.now(timezone.utc)
            
            # Match REST endpoint structure
            total_value = sum(b.get("total", 0) for b in balances.values())
            
            return success_result(self.response_type, {
                "collective_id": collective_id,
                "updated_at": now.isoformat(),
                "balances": balances,
                "positions": [],  # TODO: Calculate from orders
                "summary": {
                    "total_value_usdc": total_value,
                    "total_unrealized_pnl": 0.0,
                    "total_realized_pnl": 0.0,
                    "open_orders_value": 0.0
                }
            })
        except Exception as e:
            logger.error(f"get_portfolio error: {e}", exc_info=True)
            return error_result(
                self.response_type,
                ErrorCode.INTERNAL_ERROR,
                "Failed to retrieve portfolio"
            )


class GetBalancesHandler(MessageHandler):
    """Handler for get_balances messages."""
    
    @property
    def message_type(self) -> MessageType:
        return MessageType.GET_BALANCES
    
    @property
    def response_type(self) -> str:
        return "balances"
    
    async def handle(
        self,
        collective_id: str,
        data: Dict[str, Any]
    ) -> HandlerResult:
        """
        Get balance details.
        
        Optionally filter by currency.
        """
        from ..routes.portfolio import get_or_create_portfolio
        
        try:
            balances = get_or_create_portfolio(collective_id)
            
            # Optional currency filter
            currency = data.get("currency")
            if currency:
                currency = currency.upper()
                if currency in balances:
                    balances = {currency: balances[currency]}
                else:
                    balances = {}
            
            return success_result(self.response_type, {
                "collective_id": collective_id,
                "balances": balances
            })
        except Exception as e:
            logger.error(f"get_balances error: {e}", exc_info=True)
            return error_result(
                self.response_type,
                ErrorCode.INTERNAL_ERROR,
                "Failed to retrieve balances"
            )


# =============================================================================
# Order Handlers
# =============================================================================

class PlaceOrderHandler(MessageHandler):
    """Handler for place_order messages."""
    
    @property
    def message_type(self) -> MessageType:
        return MessageType.PLACE_ORDER
    
    @property
    def response_type(self) -> str:
        return "order_placed"
    
    async def handle(
        self,
        collective_id: str,
        data: Dict[str, Any]
    ) -> HandlerResult:
        """
        Place a new order.
        
        Required fields: symbol, side, type, quantity
        Optional fields: price (required for limit), time_in_force, client_order_id, rationale
        """
        # Validate required fields
        required = ["symbol", "side", "type", "quantity"]
        validation_error = self.validate_required_fields(data, required)
        if validation_error:
            return validation_error
        
        # Validate order type specifics
        order_type = data.get("type", "").lower()
        if order_type == "limit" and not data.get("price"):
            return error_result(
                self.response_type,
                ErrorCode.MISSING_FIELD,
                "Limit orders require a price"
            )
        
        # Validate quantity
        try:
            quantity = float(data["quantity"])
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except (TypeError, ValueError) as e:
            return error_result(
                self.response_type,
                ErrorCode.INVALID_FIELD,
                f"Invalid quantity: {e}"
            )
        
        # Import and call order logic
        from ..routes.orders import ORDERS, generate_order_id
        from ..models.order import OrderStatus
        
        try:
            now = datetime.now(timezone.utc)
            order_id = generate_order_id()
            
            # Check for duplicate client_order_id
            client_order_id = data.get("client_order_id")
            if client_order_id:
                for existing in ORDERS.values():
                    if (existing["collective_id"] == collective_id and
                        existing.get("client_order_id") == client_order_id):
                        return error_result(
                            self.response_type,
                            ErrorCode.INVALID_REQUEST,
                            f"Client order ID '{client_order_id}' already used"
                        )
            
            # Create order
            order_data = {
                "order_id": order_id,
                "collective_id": collective_id,
                "symbol": data["symbol"].upper(),
                "side": data["side"].lower(),
                "type": order_type,
                "quantity": quantity,
                "price": float(data["price"]) if data.get("price") else None,
                "filled_quantity": 0.0,
                "average_fill_price": None,
                "status": OrderStatus.OPEN,
                "time_in_force": data.get("time_in_force", "GTC"),
                "client_order_id": client_order_id,
                "rationale": data.get("rationale"),
                "fills": [],
                "created_at": now,
                "updated_at": now
            }
            
            ORDERS[order_id] = order_data
            
            # Return serializable response
            return success_result(self.response_type, {
                "order_id": order_id,
                "collective_id": collective_id,
                "symbol": order_data["symbol"],
                "side": order_data["side"],
                "type": order_data["type"],
                "quantity": order_data["quantity"],
                "price": order_data["price"],
                "status": str(order_data["status"].value),
                "time_in_force": order_data["time_in_force"],
                "client_order_id": order_data["client_order_id"],
                "created_at": now.isoformat()
            })
            
        except Exception as e:
            logger.error(f"place_order error: {e}", exc_info=True)
            return error_result(
                self.response_type,
                ErrorCode.INTERNAL_ERROR,
                "Failed to place order"
            )


class CancelOrderHandler(MessageHandler):
    """Handler for cancel_order messages."""
    
    @property
    def message_type(self) -> MessageType:
        return MessageType.CANCEL_ORDER
    
    @property
    def response_type(self) -> str:
        return "order_cancelled"
    
    async def handle(
        self,
        collective_id: str,
        data: Dict[str, Any]
    ) -> HandlerResult:
        """
        Cancel an existing order.
        
        Required fields: order_id
        """
        validation_error = self.validate_required_fields(data, ["order_id"])
        if validation_error:
            return validation_error
        
        order_id = data["order_id"]
        
        from ..routes.orders import ORDERS
        from ..models.order import OrderStatus
        
        try:
            # Check order exists
            if order_id not in ORDERS:
                return error_result(
                    self.response_type,
                    ErrorCode.NOT_FOUND,
                    f"Order '{order_id}' not found"
                )
            
            order = ORDERS[order_id]
            
            # Verify ownership
            if order["collective_id"] != collective_id:
                return error_result(
                    self.response_type,
                    ErrorCode.NOT_FOUND,
                    f"Order '{order_id}' not found"
                )
            
            # Check if cancellable
            terminal_statuses = [OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.EXPIRED]
            if order["status"] in terminal_statuses:
                return error_result(
                    self.response_type,
                    ErrorCode.INVALID_REQUEST,
                    f"Order is already {order['status'].value}"
                )
            
            now = datetime.now(timezone.utc)
            remaining = order["quantity"] - order["filled_quantity"]
            
            order["status"] = OrderStatus.CANCELLED
            order["updated_at"] = now
            
            return success_result(self.response_type, {
                "order_id": order_id,
                "status": OrderStatus.CANCELLED.value,
                "cancelled_at": now.isoformat(),
                "filled_quantity": order["filled_quantity"],
                "remaining_quantity": remaining
            })
            
        except Exception as e:
            logger.error(f"cancel_order error: {e}", exc_info=True)
            return error_result(
                self.response_type,
                ErrorCode.INTERNAL_ERROR,
                "Failed to cancel order"
            )


class GetOrdersHandler(MessageHandler):
    """Handler for get_orders messages."""
    
    @property
    def message_type(self) -> MessageType:
        return MessageType.GET_ORDERS
    
    @property
    def response_type(self) -> str:
        return "orders"
    
    async def handle(
        self,
        collective_id: str,
        data: Dict[str, Any]
    ) -> HandlerResult:
        """
        List orders with optional filters.
        
        Optional filters: status, symbol, side, limit, offset
        """
        from ..routes.orders import ORDERS
        
        try:
            # Filter orders for this collective
            orders = [o for o in ORDERS.values() if o["collective_id"] == collective_id]
            
            # Apply filters
            status_filter = data.get("status")
            if status_filter:
                if isinstance(status_filter, str):
                    status_list = [s.strip() for s in status_filter.split(",")]
                elif isinstance(status_filter, list):
                    status_list = status_filter
                else:
                    status_list = [str(status_filter)]
                orders = [o for o in orders if o["status"].value in status_list]
            
            symbol_filter = data.get("symbol")
            if symbol_filter:
                orders = [o for o in orders if o["symbol"] == symbol_filter.upper()]
            
            side_filter = data.get("side")
            if side_filter:
                orders = [o for o in orders if o["side"] == side_filter.lower()]
            
            # Sort by created_at descending
            orders.sort(key=lambda x: x["created_at"], reverse=True)
            
            total = len(orders)
            
            # Pagination
            limit = min(int(data.get("limit", 50)), 500)
            offset = int(data.get("offset", 0))
            orders = orders[offset:offset + limit]
            
            # Serialize for response
            order_list = []
            for o in orders:
                order_list.append({
                    "order_id": o["order_id"],
                    "symbol": o["symbol"],
                    "side": o["side"],
                    "type": o["type"],
                    "quantity": o["quantity"],
                    "price": o["price"],
                    "filled_quantity": o["filled_quantity"],
                    "status": o["status"].value,
                    "created_at": o["created_at"].isoformat(),
                    "updated_at": o["updated_at"].isoformat()
                })
            
            return success_result(self.response_type, {
                "orders": order_list,
                "total": total,
                "limit": limit,
                "offset": offset
            })
            
        except Exception as e:
            logger.error(f"get_orders error: {e}", exc_info=True)
            return error_result(
                self.response_type,
                ErrorCode.INTERNAL_ERROR,
                "Failed to retrieve orders"
            )


class GetOrderHandler(MessageHandler):
    """Handler for get_order messages (single order details)."""
    
    @property
    def message_type(self) -> MessageType:
        return MessageType.GET_ORDER
    
    @property
    def response_type(self) -> str:
        return "order"
    
    async def handle(
        self,
        collective_id: str,
        data: Dict[str, Any]
    ) -> HandlerResult:
        """
        Get details of a specific order.
        
        Required fields: order_id
        """
        validation_error = self.validate_required_fields(data, ["order_id"])
        if validation_error:
            return validation_error
        
        order_id = data["order_id"]
        
        from ..routes.orders import ORDERS
        
        try:
            if order_id not in ORDERS:
                return error_result(
                    self.response_type,
                    ErrorCode.NOT_FOUND,
                    f"Order '{order_id}' not found"
                )
            
            order = ORDERS[order_id]
            
            # Verify ownership
            if order["collective_id"] != collective_id:
                return error_result(
                    self.response_type,
                    ErrorCode.NOT_FOUND,
                    f"Order '{order_id}' not found"
                )
            
            # Full order details
            return success_result(self.response_type, {
                "order_id": order["order_id"],
                "collective_id": order["collective_id"],
                "symbol": order["symbol"],
                "side": order["side"],
                "type": order["type"],
                "quantity": order["quantity"],
                "price": order["price"],
                "filled_quantity": order["filled_quantity"],
                "average_fill_price": order["average_fill_price"],
                "status": order["status"].value,
                "time_in_force": order["time_in_force"],
                "client_order_id": order.get("client_order_id"),
                "rationale": order.get("rationale"),
                "fills": order.get("fills", []),
                "created_at": order["created_at"].isoformat(),
                "updated_at": order["updated_at"].isoformat()
            })
            
        except Exception as e:
            logger.error(f"get_order error: {e}", exc_info=True)
            return error_result(
                self.response_type,
                ErrorCode.INTERNAL_ERROR,
                "Failed to retrieve order"
            )


# =============================================================================
# Market Data Handlers
# =============================================================================

# Available symbols (mock data for Phase 2)
AVAILABLE_SYMBOLS = [
    {"symbol": "SOL/USDC", "base": "SOL", "quote": "USDC", "status": "active"},
    {"symbol": "BTC/USDC", "base": "BTC", "quote": "USDC", "status": "active"},
    {"symbol": "ETH/USDC", "base": "ETH", "quote": "USDC", "status": "active"},
    {"symbol": "WEAVER/USDC", "base": "WEAVER", "quote": "USDC", "status": "active"},
]


class SubscribeMarketHandler(MessageHandler):
    """Handler for subscribe_market messages."""
    
    @property
    def message_type(self) -> MessageType:
        return MessageType.SUBSCRIBE_MARKET
    
    @property
    def response_type(self) -> str:
        return "market_subscribed"
    
    async def handle(
        self,
        collective_id: str,
        data: Dict[str, Any]
    ) -> HandlerResult:
        """
        Subscribe to market data for specific symbols.
        
        Optional: symbols (list) - if not provided, subscribes to all
        """
        symbols = data.get("symbols")
        
        if symbols:
            # Validate symbols
            if not isinstance(symbols, list):
                symbols = [symbols]
            symbols = [s.upper() for s in symbols]
            
            valid_symbols = {s["symbol"] for s in AVAILABLE_SYMBOLS}
            invalid = [s for s in symbols if s not in valid_symbols]
            
            if invalid:
                return error_result(
                    self.response_type,
                    ErrorCode.INVALID_FIELD,
                    f"Invalid symbol(s): {', '.join(invalid)}"
                )
            
            subscribed = symbols
        else:
            # Subscribe to all
            subscribed = [s["symbol"] for s in AVAILABLE_SYMBOLS]
        
        return success_result(self.response_type, {
            "collective_id": collective_id,
            "symbols": subscribed,
            "message": f"Subscribed to {len(subscribed)} symbol(s)"
        })


class UnsubscribeMarketHandler(MessageHandler):
    """Handler for unsubscribe_market messages."""
    
    @property
    def message_type(self) -> MessageType:
        return MessageType.UNSUBSCRIBE_MARKET
    
    @property
    def response_type(self) -> str:
        return "market_unsubscribed"
    
    async def handle(
        self,
        collective_id: str,
        data: Dict[str, Any]
    ) -> HandlerResult:
        """
        Unsubscribe from market data.
        
        Optional: symbols (list) - if not provided, unsubscribes from all
        """
        symbols = data.get("symbols")
        
        if symbols:
            if not isinstance(symbols, list):
                symbols = [symbols]
            symbols = [s.upper() for s in symbols]
        else:
            symbols = [s["symbol"] for s in AVAILABLE_SYMBOLS]
        
        return success_result(self.response_type, {
            "collective_id": collective_id,
            "symbols": symbols,
            "message": f"Unsubscribed from {len(symbols)} symbol(s)"
        })


class GetSymbolsHandler(MessageHandler):
    """Handler for get_symbols messages."""
    
    @property
    def message_type(self) -> MessageType:
        return MessageType.GET_SYMBOLS
    
    @property
    def response_type(self) -> str:
        return "symbols"
    
    async def handle(
        self,
        collective_id: str,
        data: Dict[str, Any]
    ) -> HandlerResult:
        """
        Get list of available trading symbols.
        
        Optional filters: status, quote_currency
        """
        symbols = AVAILABLE_SYMBOLS.copy()
        
        # Apply filters
        status_filter = data.get("status")
        if status_filter:
            symbols = [s for s in symbols if s["status"] == status_filter]
        
        quote_filter = data.get("quote_currency")
        if quote_filter:
            symbols = [s for s in symbols if s["quote"] == quote_filter.upper()]
        
        return success_result(self.response_type, {
            "symbols": symbols,
            "count": len(symbols)
        })


class PingHandler(MessageHandler):
    """Handler for ping messages (heartbeat)."""
    
    @property
    def message_type(self) -> MessageType:
        return MessageType.PING
    
    @property
    def response_type(self) -> str:
        return "pong"
    
    async def handle(
        self,
        collective_id: str,
        data: Dict[str, Any]
    ) -> HandlerResult:
        """Respond to heartbeat ping."""
        return success_result(self.response_type, {
            "collective_id": collective_id,
            "server_time": datetime.now(timezone.utc).isoformat()
        })


# =============================================================================
# Message Dispatcher
# =============================================================================

class MessageDispatcher:
    """
    Routes incoming WebSocket messages to appropriate handlers.
    
    Provides a centralized dispatch mechanism with:
    - Handler registration
    - Message validation
    - Error handling
    - Response formatting
    
    Usage:
        dispatcher = MessageDispatcher()
        
        # Handle incoming message
        response = await dispatcher.dispatch(collective_id, message)
        await websocket.send_json(response)
    """
    
    def __init__(self):
        """Initialize dispatcher with all registered handlers."""
        self._handlers: Dict[str, MessageHandler] = {}
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register all built-in handlers."""
        handlers = [
            # Portfolio
            GetPortfolioHandler(),
            GetBalancesHandler(),
            
            # Orders
            PlaceOrderHandler(),
            CancelOrderHandler(),
            GetOrdersHandler(),
            GetOrderHandler(),
            
            # Market Data
            SubscribeMarketHandler(),
            UnsubscribeMarketHandler(),
            GetSymbolsHandler(),
            
            # Protocol
            PingHandler(),
        ]
        
        for handler in handlers:
            self.register(handler)
    
    def register(self, handler: MessageHandler):
        """
        Register a message handler.
        
        Args:
            handler: The handler instance to register
        """
        self._handlers[handler.message_type.value] = handler
        logger.debug(f"Registered handler: {handler.message_type.value}")
    
    def get_supported_types(self) -> list[str]:
        """Get list of supported message types."""
        return list(self._handlers.keys())
    
    async def dispatch(
        self,
        collective_id: str,
        message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Dispatch a message to its handler and return the response.
        
        Args:
            collective_id: The authenticated collective ID
            message: The incoming message (parsed JSON)
        
        Returns:
            Response message dict ready for sending
        """
        request_id = message.get("id")
        message_type = message.get("type", "").lower()
        data = message.get("data", {})
        
        # Validate message type
        if not message_type:
            return error_result(
                "error",
                ErrorCode.INVALID_REQUEST,
                "Message must include 'type' field"
            ).to_message(request_id)
        
        # Find handler
        handler = self._handlers.get(message_type)
        if not handler:
            supported = ", ".join(sorted(self._handlers.keys()))
            return error_result(
                "error",
                ErrorCode.INVALID_MESSAGE_TYPE,
                f"Unknown message type: '{message_type}'. Supported: {supported}"
            ).to_message(request_id)
        
        # Execute handler
        try:
            result = await handler.handle(collective_id, data)
            return result.to_message(request_id)
            
        except Exception as e:
            logger.error(
                f"Handler error for {message_type}: {e}",
                exc_info=True
            )
            return error_result(
                handler.response_type,
                ErrorCode.INTERNAL_ERROR,
                "An unexpected error occurred"
            ).to_message(request_id)


# =============================================================================
# Module-Level Dispatcher Instance
# =============================================================================

# Singleton dispatcher for import
dispatcher = MessageDispatcher()


async def dispatch_message(
    collective_id: str,
    message: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convenience function for dispatching messages.
    
    Args:
        collective_id: The authenticated collective ID
        message: The incoming message
    
    Returns:
        Response message dict
    """
    return await dispatcher.dispatch(collective_id, message)
