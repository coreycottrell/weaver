"""
Order Management Endpoints

POST   /v1/orders - Place new order
GET    /v1/orders - List orders
GET    /v1/orders/{order_id} - Get order details
DELETE /v1/orders/{order_id} - Cancel order
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query

from ..models.order import (
    OrderCreate,
    OrderResponse,
    OrderListResponse,
    OrderStatus
)
from ..auth.middleware import require_auth
from ..services.streaming import streaming_service

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory storage (TODO: Replace with database)
ORDERS: dict[str, dict] = {}


def generate_order_id() -> str:
    """Generate unique order ID."""
    return f"arena-ord-{uuid.uuid4().hex[:12]}"


@router.post("", status_code=201)
async def place_order(
    order: OrderCreate,
    collective_id: str = Depends(require_auth)
) -> OrderResponse:
    """
    Place a new order.
    
    Requires Ed25519 authentication.
    """
    now = datetime.now(timezone.utc)
    order_id = generate_order_id()
    
    # Validate limit orders have price
    if order.type == "limit" and order.price is None:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "Limit orders require a price"
                }
            }
        )
    
    # Check for duplicate client_order_id
    if order.client_order_id:
        for existing in ORDERS.values():
            if (existing["collective_id"] == collective_id and 
                existing.get("client_order_id") == order.client_order_id):
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": {
                            "code": "DUPLICATE_ORDER",
                            "message": f"Client order ID '{order.client_order_id}' already used"
                        }
                    }
                )
    
    # Create order
    order_data = {
        "order_id": order_id,
        "collective_id": collective_id,
        "symbol": order.symbol,
        "side": order.side,
        "type": order.type,
        "quantity": order.quantity,
        "price": order.price,
        "filled_quantity": 0.0,
        "average_fill_price": None,
        "status": OrderStatus.PENDING,
        "time_in_force": order.time_in_force,
        "client_order_id": order.client_order_id,
        "rationale": order.rationale,
        "fills": [],
        "created_at": now,
        "updated_at": now
    }
    
    ORDERS[order_id] = order_data

    # TODO: Submit to order matching engine
    # For now, immediately mark as open
    order_data["status"] = OrderStatus.OPEN

    # Broadcast order creation via streaming service (non-blocking)
    try:
        await streaming_service.broadcast_order_created(
            collective_id=collective_id,
            order_id=order_id,
            symbol=order.symbol,
            side=order.side,
            order_type=order.type,
            quantity=order.quantity,
            price=order.price
        )
    except Exception as e:
        # Log but don't fail the request - streaming is non-critical
        logger.warning(f"Failed to broadcast order creation for {order_id}: {e}")

    return OrderResponse(**order_data)


@router.get("")
async def list_orders(
    collective_id: str = Depends(require_auth),
    status: Optional[str] = Query(None, description="Filter by status (comma-separated)"),
    symbol: Optional[str] = Query(None, description="Filter by symbol"),
    side: Optional[str] = Query(None, description="Filter by side"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0)
) -> OrderListResponse:
    """
    List orders for authenticated collective.
    """
    # Filter orders for this collective
    orders = [o for o in ORDERS.values() if o["collective_id"] == collective_id]
    
    # Apply filters
    if status:
        status_list = [s.strip() for s in status.split(",")]
        orders = [o for o in orders if o["status"] in status_list]
    if symbol:
        orders = [o for o in orders if o["symbol"] == symbol]
    if side:
        orders = [o for o in orders if o["side"] == side]
    
    # Sort by created_at descending
    orders.sort(key=lambda x: x["created_at"], reverse=True)
    
    total = len(orders)
    orders = orders[offset:offset + limit]
    
    return OrderListResponse(
        orders=[OrderResponse(**o) for o in orders],
        total=total,
        limit=limit,
        offset=offset
    )


@router.get("/{order_id}")
async def get_order(
    order_id: str,
    collective_id: str = Depends(require_auth)
) -> OrderResponse:
    """
    Get details of a specific order.
    
    Must be authenticated as the order owner.
    """
    if order_id not in ORDERS:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Order '{order_id}' not found"
                }
            }
        )
    
    order = ORDERS[order_id]
    
    # Verify ownership
    if order["collective_id"] != collective_id:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Order '{order_id}' not found"
                }
            }
        )
    
    return OrderResponse(**order)


@router.delete("/{order_id}")
async def cancel_order(
    order_id: str,
    collective_id: str = Depends(require_auth)
) -> dict:
    """
    Cancel an open order.
    
    Must be authenticated as the order owner.
    """
    if order_id not in ORDERS:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Order '{order_id}' not found"
                }
            }
        )
    
    order = ORDERS[order_id]
    
    # Verify ownership
    if order["collective_id"] != collective_id:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Order '{order_id}' not found"
                }
            }
        )
    
    # Check if cancellable
    if order["status"] in [OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.EXPIRED]:
        raise HTTPException(
            status_code=409,
            detail={
                "error": {
                    "code": "ORDER_NOT_CANCELLABLE",
                    "message": f"Order is already {order['status']}"
                }
            }
        )
    
    now = datetime.now(timezone.utc)
    remaining = order["quantity"] - order["filled_quantity"]

    order["status"] = OrderStatus.CANCELLED
    order["updated_at"] = now

    # Broadcast order cancellation via streaming service (non-blocking)
    try:
        await streaming_service.broadcast_order_cancelled(
            collective_id=collective_id,
            order_id=order_id,
            filled_quantity=order["filled_quantity"],
            remaining_quantity=remaining,
            symbol=order["symbol"]
        )
    except Exception as e:
        # Log but don't fail the request - streaming is non-critical
        logger.warning(f"Failed to broadcast order cancellation for {order_id}: {e}")

    return {
        "order_id": order_id,
        "status": OrderStatus.CANCELLED,
        "cancelled_at": now.isoformat(),
        "filled_quantity": order["filled_quantity"],
        "remaining_quantity": remaining
    }
