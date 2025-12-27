"""
WebSocket Handlers Tests

Tests for Work Stream E.4 message handlers and dispatcher.
"""

import pytest
from datetime import datetime, timezone

# Mark all tests as async
pytestmark = pytest.mark.asyncio


class TestMessageDispatcher:
    """Test the message dispatcher routing."""

    async def test_ping_returns_pong(self):
        """Ping message returns pong response."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("test-collective", {"type": "ping"})
        
        assert response["type"] == "pong"
        assert response["success"] is True
        assert "timestamp" in response

    async def test_unknown_type_returns_error(self):
        """Unknown message type returns appropriate error."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("test-collective", {"type": "unknown_type"})
        
        assert response["type"] == "error"
        assert response["success"] is False
        assert response["error"]["code"] == "INVALID_MESSAGE_TYPE"

    async def test_missing_type_returns_error(self):
        """Message without type returns error."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("test-collective", {"data": {}})
        
        assert response["success"] is False
        assert response["error"]["code"] == "INVALID_REQUEST"

    async def test_request_id_correlation(self):
        """Request ID is echoed in response."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("test-collective", {
            "id": "req-abc-123",
            "type": "ping"
        })
        
        assert response["id"] == "req-abc-123"


class TestPortfolioHandlers:
    """Test portfolio-related handlers."""

    async def test_get_portfolio(self):
        """Get portfolio returns portfolio data."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("portfolio-test", {"type": "get_portfolio"})
        
        assert response["type"] == "portfolio"
        assert response["success"] is True
        assert "balances" in response["data"]
        assert "USDC" in response["data"]["balances"]
        assert response["data"]["collective_id"] == "portfolio-test"

    async def test_get_balances(self):
        """Get balances returns balance data."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("balance-test", {"type": "get_balances"})
        
        assert response["type"] == "balances"
        assert response["success"] is True
        assert "balances" in response["data"]

    async def test_get_balances_with_currency_filter(self):
        """Get balances with currency filter."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("balance-test", {
            "type": "get_balances",
            "data": {"currency": "USDC"}
        })
        
        assert response["success"] is True
        assert "USDC" in response["data"]["balances"]


class TestOrderHandlers:
    """Test order-related handlers."""

    async def test_place_limit_order(self):
        """Place limit order succeeds."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("order-test", {
            "type": "place_order",
            "data": {
                "symbol": "SOL/USDC",
                "side": "buy",
                "type": "limit",
                "quantity": 10,
                "price": 100.0
            }
        })
        
        assert response["type"] == "order_placed"
        assert response["success"] is True
        assert "order_id" in response["data"]
        assert response["data"]["symbol"] == "SOL/USDC"
        assert response["data"]["side"] == "buy"
        assert response["data"]["status"] == "open"

    async def test_place_market_order(self):
        """Place market order succeeds (no price required)."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("order-test", {
            "type": "place_order",
            "data": {
                "symbol": "BTC/USDC",
                "side": "sell",
                "type": "market",
                "quantity": 1.5
            }
        })
        
        assert response["type"] == "order_placed"
        assert response["success"] is True
        assert response["data"]["price"] is None

    async def test_place_order_missing_fields(self):
        """Place order with missing fields returns error."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("order-test", {
            "type": "place_order",
            "data": {"symbol": "SOL/USDC"}
        })
        
        assert response["success"] is False
        assert response["error"]["code"] == "MISSING_FIELD"
        assert "side" in response["error"]["message"]

    async def test_place_limit_order_without_price(self):
        """Limit order without price returns error."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("order-test", {
            "type": "place_order",
            "data": {
                "symbol": "SOL/USDC",
                "side": "buy",
                "type": "limit",
                "quantity": 10
            }
        })
        
        assert response["success"] is False
        assert "price" in response["error"]["message"].lower()

    async def test_get_orders(self):
        """Get orders returns list."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("orders-list-test", {"type": "get_orders"})
        
        assert response["type"] == "orders"
        assert response["success"] is True
        assert "orders" in response["data"]
        assert isinstance(response["data"]["orders"], list)

    async def test_cancel_order(self):
        """Cancel order succeeds for valid order."""
        from api.websocket import dispatch_message
        
        # First, place an order
        place_response = await dispatch_message("cancel-test", {
            "type": "place_order",
            "data": {
                "symbol": "ETH/USDC",
                "side": "buy",
                "type": "limit",
                "quantity": 5,
                "price": 2500.0
            }
        })
        order_id = place_response["data"]["order_id"]
        
        # Then cancel it
        response = await dispatch_message("cancel-test", {
            "type": "cancel_order",
            "data": {"order_id": order_id}
        })
        
        assert response["type"] == "order_cancelled"
        assert response["success"] is True
        assert response["data"]["status"] == "cancelled"

    async def test_cancel_nonexistent_order(self):
        """Cancel non-existent order returns error."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("cancel-test", {
            "type": "cancel_order",
            "data": {"order_id": "arena-ord-nonexistent"}
        })
        
        assert response["success"] is False
        assert response["error"]["code"] == "NOT_FOUND"

    async def test_get_order(self):
        """Get single order details."""
        from api.websocket import dispatch_message
        
        # First, place an order
        place_response = await dispatch_message("get-order-test", {
            "type": "place_order",
            "data": {
                "symbol": "WEAVER/USDC",
                "side": "sell",
                "type": "market",
                "quantity": 100
            }
        })
        order_id = place_response["data"]["order_id"]
        
        # Then get its details
        response = await dispatch_message("get-order-test", {
            "type": "get_order",
            "data": {"order_id": order_id}
        })
        
        assert response["type"] == "order"
        assert response["success"] is True
        assert response["data"]["order_id"] == order_id
        assert response["data"]["symbol"] == "WEAVER/USDC"


class TestMarketDataHandlers:
    """Test market data handlers."""

    async def test_get_symbols(self):
        """Get symbols returns available trading pairs."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("market-test", {"type": "get_symbols"})
        
        assert response["type"] == "symbols"
        assert response["success"] is True
        assert "symbols" in response["data"]
        assert len(response["data"]["symbols"]) > 0
        assert any(s["symbol"] == "SOL/USDC" for s in response["data"]["symbols"])

    async def test_subscribe_market(self):
        """Subscribe to market data."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("market-test", {
            "type": "subscribe_market",
            "data": {"symbols": ["SOL/USDC", "BTC/USDC"]}
        })
        
        assert response["type"] == "market_subscribed"
        assert response["success"] is True
        assert "SOL/USDC" in response["data"]["symbols"]
        assert "BTC/USDC" in response["data"]["symbols"]

    async def test_subscribe_market_invalid_symbol(self):
        """Subscribe with invalid symbol returns error."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("market-test", {
            "type": "subscribe_market",
            "data": {"symbols": ["INVALID/PAIR"]}
        })
        
        assert response["success"] is False
        assert "INVALID/PAIR" in response["error"]["message"]

    async def test_unsubscribe_market(self):
        """Unsubscribe from market data."""
        from api.websocket import dispatch_message
        
        response = await dispatch_message("market-test", {
            "type": "unsubscribe_market",
            "data": {"symbols": ["SOL/USDC"]}
        })
        
        assert response["type"] == "market_unsubscribed"
        assert response["success"] is True


class TestOrderIsolation:
    """Test that collectives cannot access each other's orders."""

    async def test_collective_cannot_see_others_orders(self):
        """Collective A cannot get details of Collective B's order."""
        from api.websocket import dispatch_message
        
        # Collective A places order
        place_response = await dispatch_message("collective-a", {
            "type": "place_order",
            "data": {
                "symbol": "SOL/USDC",
                "side": "buy",
                "type": "market",
                "quantity": 10
            }
        })
        order_id = place_response["data"]["order_id"]
        
        # Collective B tries to get it
        response = await dispatch_message("collective-b", {
            "type": "get_order",
            "data": {"order_id": order_id}
        })
        
        assert response["success"] is False
        assert response["error"]["code"] == "NOT_FOUND"

    async def test_collective_cannot_cancel_others_orders(self):
        """Collective A cannot cancel Collective B's order."""
        from api.websocket import dispatch_message
        
        # Collective A places order
        place_response = await dispatch_message("collective-a-cancel", {
            "type": "place_order",
            "data": {
                "symbol": "SOL/USDC",
                "side": "buy",
                "type": "limit",
                "quantity": 10,
                "price": 100.0
            }
        })
        order_id = place_response["data"]["order_id"]
        
        # Collective B tries to cancel it
        response = await dispatch_message("collective-b-cancel", {
            "type": "cancel_order",
            "data": {"order_id": order_id}
        })
        
        assert response["success"] is False
        assert response["error"]["code"] == "NOT_FOUND"
