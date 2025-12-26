"""
Order Models

Pydantic models for order management.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    """Order status values."""
    PENDING = "pending"
    OPEN = "open"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    EXPIRED = "expired"


class OrderSide(str, Enum):
    """Order side (buy/sell)."""
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    """Order type."""
    MARKET = "market"
    LIMIT = "limit"


class TimeInForce(str, Enum):
    """Time in force options."""
    GTC = "GTC"  # Good Till Cancelled
    IOC = "IOC"  # Immediate Or Cancel
    FOK = "FOK"  # Fill Or Kill


class OrderCreate(BaseModel):
    """Request model for order creation."""
    symbol: str = Field(
        ...,
        pattern=r"^[A-Z]+/[A-Z]+$",
        description="Trading pair (e.g., SOL/USDC)"
    )
    side: OrderSide
    type: OrderType
    quantity: float = Field(..., gt=0, description="Order size in base currency")
    price: Optional[float] = Field(None, gt=0, description="Limit price")
    time_in_force: TimeInForce = TimeInForce.GTC
    client_order_id: Optional[str] = Field(None, max_length=64)
    rationale: Optional[str] = Field(None, max_length=1000)


class OrderFill(BaseModel):
    """Model for order fill details."""
    fill_id: str
    quantity: float
    price: float
    fee: float = 0.0
    fee_currency: Optional[str] = None
    executed_at: datetime


class OrderResponse(BaseModel):
    """Response model for order details."""
    order_id: str
    collective_id: str
    symbol: str
    side: OrderSide
    type: OrderType
    quantity: float
    price: Optional[float]
    filled_quantity: float = 0.0
    average_fill_price: Optional[float] = None
    status: OrderStatus
    time_in_force: TimeInForce = TimeInForce.GTC
    client_order_id: Optional[str] = None
    rationale: Optional[str] = None
    fills: list[OrderFill] = []
    created_at: datetime
    updated_at: datetime


class OrderListResponse(BaseModel):
    """Response model for listing orders."""
    orders: list[OrderResponse]
    total: int
    limit: int
    offset: int
