"""
SQLAlchemy Models

Database models for AI-CIV Trading Arena.
Uses async SQLAlchemy 2.0 patterns with PostgreSQL.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
import enum

from sqlalchemy import (
    String,
    Text,
    Integer,
    Numeric,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Index,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, INET
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


class CollectiveStatus(str, enum.Enum):
    """Collective account status."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    PENDING = "pending"


class OrderStatus(str, enum.Enum):
    """Order status values."""
    PENDING = "pending"
    OPEN = "open"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    EXPIRED = "expired"


class OrderSide(str, enum.Enum):
    """Order side (buy/sell)."""
    BUY = "buy"
    SELL = "sell"


class OrderType(str, enum.Enum):
    """Order type."""
    MARKET = "market"
    LIMIT = "limit"


class TimeInForce(str, enum.Enum):
    """Time in force options."""
    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"


class Collective(Base):
    """
    Collective registration and identity.
    
    Represents an AI collective registered to trade on the arena.
    Each collective authenticates via Ed25519 signatures using their public key.
    """
    __tablename__ = "collectives"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    collective_id: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=False, index=True
    )
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    public_key: Mapped[str] = mapped_column(Text, nullable=False)
    public_key_fingerprint: Mapped[str] = mapped_column(String(8), nullable=False)
    status: Mapped[CollectiveStatus] = mapped_column(
        SQLEnum(CollectiveStatus, name="collective_status"),
        default=CollectiveStatus.ACTIVE,
        nullable=False,
    )
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    orders: Mapped[list["Order"]] = relationship(
        "Order", back_populates="collective", lazy="selectin"
    )
    portfolio_balances: Mapped[list["PortfolioBalance"]] = relationship(
        "PortfolioBalance", back_populates="collective", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Collective(id={self.id}, collective_id='{self.collective_id}')>"


class Order(Base):
    """
    Trading order record.
    
    Represents a buy/sell order submitted by a collective.
    Supports limit and market orders with various time-in-force options.
    """
    __tablename__ = "orders"
    __table_args__ = (
        UniqueConstraint(
            "collective_id", "client_order_id",
            name="uq_collective_client_order"
        ),
        Index("ix_orders_collective_status", "collective_id", "status"),
        Index("ix_orders_symbol_status", "symbol", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )
    collective_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("collectives.collective_id", ondelete="CASCADE"),
        nullable=False,
    )
    client_order_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    side: Mapped[OrderSide] = mapped_column(
        SQLEnum(OrderSide, name="order_side"), nullable=False
    )
    type: Mapped[OrderType] = mapped_column(
        SQLEnum(OrderType, name="order_type"), nullable=False
    )
    quantity: Mapped[Decimal] = mapped_column(
        Numeric(20, 8), nullable=False
    )
    price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(20, 8), nullable=True
    )
    filled_quantity: Mapped[Decimal] = mapped_column(
        Numeric(20, 8), default=Decimal("0"), nullable=False
    )
    average_fill_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(20, 8), nullable=True
    )
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus, name="order_status"),
        default=OrderStatus.PENDING,
        nullable=False,
    )
    time_in_force: Mapped[TimeInForce] = mapped_column(
        SQLEnum(TimeInForce, name="time_in_force"),
        default=TimeInForce.GTC,
        nullable=False,
    )
    rationale: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    collective: Mapped["Collective"] = relationship(
        "Collective", back_populates="orders"
    )
    fills: Mapped[list["OrderFill"]] = relationship(
        "OrderFill", back_populates="order", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Order(order_id='{self.order_id}', symbol='{self.symbol}', status='{self.status.value}')>"


class OrderFill(Base):
    """
    Order fill/execution record.
    
    Records individual fill events for partially or fully filled orders.
    """
    __tablename__ = "order_fills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fill_id: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )
    order_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("orders.order_id", ondelete="CASCADE"),
        nullable=False,
    )
    quantity: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    fee: Mapped[Decimal] = mapped_column(
        Numeric(20, 8), default=Decimal("0"), nullable=False
    )
    fee_currency: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    executed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="fills")

    def __repr__(self) -> str:
        return f"<OrderFill(fill_id='{self.fill_id}', quantity={self.quantity})>"


class PortfolioBalance(Base):
    """
    Portfolio balance for a specific currency.
    
    Tracks total, available, and reserved balances per collective per currency.
    """
    __tablename__ = "portfolio_balances"
    __table_args__ = (
        UniqueConstraint("collective_id", "symbol", name="uq_collective_symbol"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    collective_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("collectives.collective_id", ondelete="CASCADE"),
        nullable=False,
    )
    symbol: Mapped[str] = mapped_column(String(10), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(
        Numeric(20, 8), default=Decimal("0"), nullable=False
    )
    available: Mapped[Decimal] = mapped_column(
        Numeric(20, 8), default=Decimal("0"), nullable=False
    )
    reserved: Mapped[Decimal] = mapped_column(
        Numeric(20, 8), default=Decimal("0"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    collective: Mapped["Collective"] = relationship(
        "Collective", back_populates="portfolio_balances"
    )

    def __repr__(self) -> str:
        return f"<PortfolioBalance(collective='{self.collective_id}', symbol='{self.symbol}', qty={self.quantity})>"


class PortfolioSnapshot(Base):
    """
    Historical portfolio snapshot.
    
    Point-in-time snapshot of portfolio value for performance tracking.
    """
    __tablename__ = "portfolio_snapshots"
    __table_args__ = (
        UniqueConstraint(
            "collective_id", "snapshot_time",
            name="uq_collective_snapshot_time"
        ),
        Index("ix_snapshots_collective_time", "collective_id", "snapshot_time"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    collective_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("collectives.collective_id", ondelete="CASCADE"),
        nullable=False,
    )
    snapshot_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    total_value_usdc: Mapped[Decimal] = mapped_column(
        Numeric(20, 8), nullable=False
    )
    positions_value: Mapped[Decimal] = mapped_column(
        Numeric(20, 8), default=Decimal("0"), nullable=False
    )
    cash_value: Mapped[Decimal] = mapped_column(
        Numeric(20, 8), default=Decimal("0"), nullable=False
    )
    realized_pnl: Mapped[Decimal] = mapped_column(
        Numeric(20, 8), default=Decimal("0"), nullable=False
    )
    unrealized_pnl: Mapped[Decimal] = mapped_column(
        Numeric(20, 8), default=Decimal("0"), nullable=False
    )

    def __repr__(self) -> str:
        return f"<PortfolioSnapshot(collective='{self.collective_id}', time={self.snapshot_time})>"


class AuditLog(Base):
    """
    Audit log entry.
    
    Immutable record of all state-changing operations for transparency.
    Every authenticated action is logged here.
    """
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("ix_audit_collective_time", "collective_id", "timestamp"),
        Index("ix_audit_event_type", "event_type"),
        Index("ix_audit_resource", "resource_type", "resource_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    audit_id: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    collective_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_type: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    resource_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    action: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    request_signature_fingerprint: Mapped[Optional[str]] = mapped_column(
        String(8), nullable=True
    )
    ip_address: Mapped[Optional[str]] = mapped_column(INET, nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    details: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    result: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self) -> str:
        return f"<AuditLog(audit_id='{self.audit_id}', event='{self.event_type}')>"
