"""
Order Management Integration Tests

Tests for order endpoints:
- Order creation
- Order cancellation
- Order listing
- Order retrieval
- Order validation
"""

import pytest
from fastapi.testclient import TestClient

from .conftest import RequestSigner, make_order_data


class TestOrderCreation:
    """Test order placement endpoint."""

    def test_create_limit_buy_order(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Valid limit buy order should succeed."""
        path = "/v1/orders"
        body = make_order_data(
            symbol="SOL/USDC",
            side="buy",
            order_type="limit",
            quantity=10.0,
            price=100.50,
            rationale="Testing limit buy"
        )
        headers = auth_signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 201
        data = response.json()

        # Verify order fields
        assert data["collective_id"] == registered_collective["collective_id"]
        assert data["symbol"] == "SOL/USDC"
        assert data["side"] == "buy"
        assert data["type"] == "limit"
        assert data["quantity"] == 10.0
        assert data["price"] == 100.50
        assert data["status"] == "open"
        assert data["rationale"] == "Testing limit buy"
        assert data["filled_quantity"] == 0.0
        assert data["order_id"].startswith("arena-ord-")
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_limit_sell_order(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Valid limit sell order should succeed."""
        path = "/v1/orders"
        body = make_order_data(
            symbol="BTC/USDC",
            side="sell",
            order_type="limit",
            quantity=0.5,
            price=45000.00
        )
        headers = auth_signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 201
        data = response.json()
        assert data["side"] == "sell"
        assert data["symbol"] == "BTC/USDC"
        assert data["price"] == 45000.00

    def test_create_market_buy_order(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Valid market buy order should succeed (no price required)."""
        path = "/v1/orders"
        body = make_order_data(
            symbol="ETH/USDC",
            side="buy",
            order_type="market",
            quantity=5.0,
            price=None  # Market orders don't need price
        )
        headers = auth_signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "market"
        assert data["price"] is None

    def test_create_order_with_client_order_id(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Order with client_order_id should be stored correctly."""
        path = "/v1/orders"
        body = make_order_data(
            client_order_id="my-unique-id-12345"
        )
        headers = auth_signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 201
        data = response.json()
        assert data["client_order_id"] == "my-unique-id-12345"

    def test_create_order_with_time_in_force(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Order with time_in_force should be stored correctly."""
        path = "/v1/orders"
        body = {
            "symbol": "SOL/USDC",
            "side": "buy",
            "type": "limit",
            "quantity": 10.0,
            "price": 100.0,
            "time_in_force": "IOC"  # Immediate Or Cancel
        }
        headers = auth_signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 201
        data = response.json()
        assert data["time_in_force"] == "IOC"


class TestOrderValidation:
    """Test order validation rules."""

    def test_limit_order_requires_price(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Limit order without price should be rejected."""
        path = "/v1/orders"
        body = {
            "symbol": "SOL/USDC",
            "side": "buy",
            "type": "limit",
            "quantity": 10.0
            # price intentionally missing
        }
        headers = auth_signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 400
        error = response.json()["detail"]["error"]
        assert error["code"] == "INVALID_REQUEST"
        assert "price" in error["message"].lower()

    def test_invalid_symbol_format_rejected(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Invalid symbol format should be rejected."""
        path = "/v1/orders"
        body = {
            "symbol": "invalid-symbol",  # Should be XXX/YYY
            "side": "buy",
            "type": "limit",
            "quantity": 10.0,
            "price": 100.0
        }
        headers = auth_signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 422  # Pydantic validation error

    def test_zero_quantity_rejected(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Zero quantity should be rejected."""
        path = "/v1/orders"
        body = {
            "symbol": "SOL/USDC",
            "side": "buy",
            "type": "limit",
            "quantity": 0,
            "price": 100.0
        }
        headers = auth_signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 422

    def test_negative_quantity_rejected(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Negative quantity should be rejected."""
        path = "/v1/orders"
        body = {
            "symbol": "SOL/USDC",
            "side": "buy",
            "type": "limit",
            "quantity": -10.0,
            "price": 100.0
        }
        headers = auth_signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 422

    def test_negative_price_rejected(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Negative price should be rejected."""
        path = "/v1/orders"
        body = {
            "symbol": "SOL/USDC",
            "side": "buy",
            "type": "limit",
            "quantity": 10.0,
            "price": -100.0
        }
        headers = auth_signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 422

    def test_invalid_side_rejected(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Invalid side value should be rejected."""
        path = "/v1/orders"
        body = {
            "symbol": "SOL/USDC",
            "side": "hold",  # Invalid - should be buy or sell
            "type": "limit",
            "quantity": 10.0,
            "price": 100.0
        }
        headers = auth_signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 422

    def test_invalid_order_type_rejected(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Invalid order type should be rejected."""
        path = "/v1/orders"
        body = {
            "symbol": "SOL/USDC",
            "side": "buy",
            "type": "stop_loss",  # Invalid - should be market or limit
            "quantity": 10.0,
            "price": 100.0
        }
        headers = auth_signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 422


class TestOrderCancellation:
    """Test order cancellation endpoint."""

    def test_cancel_open_order(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Cancelling an open order should succeed."""
        # Create order
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request("POST", path, body=body)
        create_response = client.post(path, json=body, headers=headers)
        assert create_response.status_code == 201
        order_id = create_response.json()["order_id"]

        # Cancel order
        cancel_path = f"/v1/orders/{order_id}"
        cancel_headers = auth_signer.sign_request("DELETE", cancel_path)
        cancel_response = client.delete(cancel_path, headers=cancel_headers)

        assert cancel_response.status_code == 200
        data = cancel_response.json()
        assert data["order_id"] == order_id
        assert data["status"] == "cancelled"
        assert "cancelled_at" in data
        assert data["filled_quantity"] == 0.0
        assert data["remaining_quantity"] == 10.0  # Full quantity remaining

    def test_cancel_already_cancelled_order(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Cancelling an already cancelled order should fail."""
        # Create and cancel order
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request("POST", path, body=body)
        create_response = client.post(path, json=body, headers=headers)
        order_id = create_response.json()["order_id"]

        cancel_path = f"/v1/orders/{order_id}"
        cancel_headers = auth_signer.sign_request("DELETE", cancel_path)
        client.delete(cancel_path, headers=cancel_headers)

        # Try to cancel again
        cancel_headers_2 = auth_signer.sign_request("DELETE", cancel_path)
        response = client.delete(cancel_path, headers=cancel_headers_2)

        assert response.status_code == 409
        error = response.json()["detail"]["error"]
        assert error["code"] == "ORDER_NOT_CANCELLABLE"

    def test_cancel_nonexistent_order(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Cancelling non-existent order should return 404."""
        cancel_path = "/v1/orders/arena-ord-doesnotexist"
        headers = auth_signer.sign_request("DELETE", cancel_path)

        response = client.delete(cancel_path, headers=headers)

        assert response.status_code == 404
        error = response.json()["detail"]["error"]
        assert error["code"] == "NOT_FOUND"

    def test_cancel_requires_authentication(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Cancelling order without auth should fail."""
        # Create order
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request("POST", path, body=body)
        create_response = client.post(path, json=body, headers=headers)
        order_id = create_response.json()["order_id"]

        # Try to cancel without auth
        response = client.delete(f"/v1/orders/{order_id}")

        assert response.status_code == 401


class TestOrderListing:
    """Test order listing endpoint."""

    def test_list_orders_empty(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Empty order list should return empty array."""
        path = "/v1/orders"
        headers = auth_signer.sign_request("GET", path)

        response = client.get(path, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["orders"] == []
        assert data["total"] == 0

    def test_list_orders_populated(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Should list all orders for collective."""
        path = "/v1/orders"

        # Create 3 orders
        for i in range(3):
            body = make_order_data(client_order_id=f"order-{i}")
            headers = auth_signer.sign_request("POST", path, body=body)
            response = client.post(path, json=body, headers=headers)
            assert response.status_code == 201

        # List orders
        list_headers = auth_signer.sign_request("GET", path)
        response = client.get(path, headers=list_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["orders"]) == 3

    def test_list_orders_pagination(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Pagination should work correctly."""
        path = "/v1/orders"

        # Create 5 orders
        for i in range(5):
            body = make_order_data(client_order_id=f"order-{i}")
            headers = auth_signer.sign_request("POST", path, body=body)
            client.post(path, json=body, headers=headers)

        # Test limit
        list_path = "/v1/orders?limit=2"
        headers = auth_signer.sign_request("GET", list_path)
        response = client.get(list_path, headers=headers)

        data = response.json()
        assert len(data["orders"]) == 2
        assert data["total"] == 5
        assert data["limit"] == 2

        # Test offset
        list_path_2 = "/v1/orders?limit=2&offset=3"
        headers_2 = auth_signer.sign_request("GET", list_path_2)
        response_2 = client.get(list_path_2, headers=headers_2)

        data_2 = response_2.json()
        assert len(data_2["orders"]) == 2
        assert data_2["offset"] == 3

    def test_list_orders_filter_by_status(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Status filter should work."""
        path = "/v1/orders"

        # Create an order
        body = make_order_data(client_order_id="order-1")
        headers = auth_signer.sign_request("POST", path, body=body)
        create_response = client.post(path, json=body, headers=headers)
        order_id = create_response.json()["order_id"]

        # Cancel it
        cancel_path = f"/v1/orders/{order_id}"
        cancel_headers = auth_signer.sign_request("DELETE", cancel_path)
        client.delete(cancel_path, headers=cancel_headers)

        # Create another order (stays open)
        body_2 = make_order_data(client_order_id="order-2")
        headers_2 = auth_signer.sign_request("POST", path, body=body_2)
        client.post(path, json=body_2, headers=headers_2)

        # Filter by open status
        list_path = "/v1/orders?status=open"
        list_headers = auth_signer.sign_request("GET", list_path)
        response = client.get(list_path, headers=list_headers)

        data = response.json()
        assert data["total"] == 1
        assert all(o["status"] == "open" for o in data["orders"])

        # Filter by cancelled status
        list_path_2 = "/v1/orders?status=cancelled"
        list_headers_2 = auth_signer.sign_request("GET", list_path_2)
        response_2 = client.get(list_path_2, headers=list_headers_2)

        data_2 = response_2.json()
        assert data_2["total"] == 1
        assert all(o["status"] == "cancelled" for o in data_2["orders"])

    def test_list_orders_filter_by_symbol(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Symbol filter should work."""
        path = "/v1/orders"

        # Create orders for different symbols
        for symbol in ["SOL/USDC", "BTC/USDC", "ETH/USDC"]:
            body = make_order_data(symbol=symbol)
            headers = auth_signer.sign_request("POST", path, body=body)
            client.post(path, json=body, headers=headers)

        # Filter by SOL/USDC
        list_path = "/v1/orders?symbol=SOL/USDC"
        list_headers = auth_signer.sign_request("GET", list_path)
        response = client.get(list_path, headers=list_headers)

        data = response.json()
        assert data["total"] == 1
        assert all(o["symbol"] == "SOL/USDC" for o in data["orders"])

    def test_list_orders_filter_by_side(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Side filter should work."""
        path = "/v1/orders"

        # Create buy and sell orders
        for i, side in enumerate(["buy", "sell", "buy"]):
            body = make_order_data(side=side, client_order_id=f"order-{i}")
            headers = auth_signer.sign_request("POST", path, body=body)
            client.post(path, json=body, headers=headers)

        # Filter by buy
        list_path = "/v1/orders?side=buy"
        list_headers = auth_signer.sign_request("GET", list_path)
        response = client.get(list_path, headers=list_headers)

        data = response.json()
        assert data["total"] == 2
        assert all(o["side"] == "buy" for o in data["orders"])

    def test_list_orders_requires_authentication(
        self,
        client: TestClient,
        registered_collective: dict
    ):
        """Listing orders without auth should fail."""
        response = client.get("/v1/orders")

        assert response.status_code == 401


class TestGetOrder:
    """Test getting individual order details."""

    def test_get_order_success(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Getting own order should succeed."""
        # Create order
        path = "/v1/orders"
        body = make_order_data(rationale="Test order for retrieval")
        headers = auth_signer.sign_request("POST", path, body=body)
        create_response = client.post(path, json=body, headers=headers)
        order_id = create_response.json()["order_id"]

        # Get order
        get_path = f"/v1/orders/{order_id}"
        get_headers = auth_signer.sign_request("GET", get_path)
        response = client.get(get_path, headers=get_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["order_id"] == order_id
        assert data["rationale"] == "Test order for retrieval"
        assert data["collective_id"] == registered_collective["collective_id"]

    def test_get_nonexistent_order(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Getting non-existent order should return 404."""
        get_path = "/v1/orders/arena-ord-doesnotexist"
        headers = auth_signer.sign_request("GET", get_path)

        response = client.get(get_path, headers=headers)

        assert response.status_code == 404
        error = response.json()["detail"]["error"]
        assert error["code"] == "NOT_FOUND"

    def test_get_order_requires_authentication(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Getting order without auth should fail."""
        # Create order
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request("POST", path, body=body)
        create_response = client.post(path, json=body, headers=headers)
        order_id = create_response.json()["order_id"]

        # Try to get without auth
        response = client.get(f"/v1/orders/{order_id}")

        assert response.status_code == 401


class TestOrderIsolation:
    """Test that orders are properly isolated between collectives."""

    def test_collective_only_sees_own_orders(
        self,
        client: TestClient,
        registered_collective: dict,
        registered_collective_2: dict,
        auth_signer: RequestSigner
    ):
        """Each collective should only see their own orders."""
        path = "/v1/orders"

        # Collective 1 creates 2 orders
        for i in range(2):
            body = make_order_data(client_order_id=f"c1-order-{i}")
            headers = auth_signer.sign_request("POST", path, body=body)
            client.post(path, json=body, headers=headers)

        # Collective 2 creates 3 orders
        signer_2 = RequestSigner(
            registered_collective_2["collective_id"],
            registered_collective_2["signing_key"]
        )
        for i in range(3):
            body = make_order_data(client_order_id=f"c2-order-{i}")
            headers = signer_2.sign_request("POST", path, body=body)
            client.post(path, json=body, headers=headers)

        # Collective 1 should see 2 orders
        list_headers_1 = auth_signer.sign_request("GET", path)
        response_1 = client.get(path, headers=list_headers_1)
        assert response_1.json()["total"] == 2

        # Collective 2 should see 3 orders
        list_headers_2 = signer_2.sign_request("GET", path)
        response_2 = client.get(path, headers=list_headers_2)
        assert response_2.json()["total"] == 3

    def test_client_order_id_scoped_to_collective(
        self,
        client: TestClient,
        registered_collective: dict,
        registered_collective_2: dict,
        auth_signer: RequestSigner
    ):
        """Same client_order_id should be allowed for different collectives."""
        path = "/v1/orders"
        client_order_id = "shared-id-123"

        # Collective 1 creates order with client_order_id
        body = make_order_data(client_order_id=client_order_id)
        headers = auth_signer.sign_request("POST", path, body=body)
        response_1 = client.post(path, json=body, headers=headers)
        assert response_1.status_code == 201

        # Collective 2 creates order with same client_order_id - should succeed
        signer_2 = RequestSigner(
            registered_collective_2["collective_id"],
            registered_collective_2["signing_key"]
        )
        headers_2 = signer_2.sign_request("POST", path, body=body)
        response_2 = client.post(path, json=body, headers=headers_2)
        assert response_2.status_code == 201

        # They should have different order IDs
        assert response_1.json()["order_id"] != response_2.json()["order_id"]
