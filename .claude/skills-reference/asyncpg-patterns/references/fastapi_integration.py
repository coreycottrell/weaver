# api/database.py
"""
FastAPI integration patterns for asyncpg.

Covers:
- Lifespan events for pool lifecycle
- Dependency injection for connections
- Transaction dependencies
- Repository pattern
- Health check endpoints
"""

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from contextlib import asynccontextmanager
import asyncpg
from typing import AsyncGenerator, Optional, List
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


# =============================================================================
# Connection Pool (from pool.py)
# =============================================================================

class DatabasePool:
    """Singleton connection pool manager."""

    _pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def initialize(cls, dsn: str, **kwargs) -> asyncpg.Pool:
        if cls._pool is not None:
            return cls._pool

        cls._pool = await asyncpg.create_pool(dsn, **kwargs)
        logger.info("Database pool initialized")
        return cls._pool

    @classmethod
    async def close(cls):
        if cls._pool is not None:
            await cls._pool.close()
            cls._pool = None
            logger.info("Database pool closed")

    @classmethod
    def acquire(cls):
        if cls._pool is None:
            raise RuntimeError("Pool not initialized")
        return cls._pool.acquire()

    @classmethod
    def get_pool(cls) -> asyncpg.Pool:
        if cls._pool is None:
            raise RuntimeError("Pool not initialized")
        return cls._pool

    @classmethod
    async def health_check(cls) -> dict:
        if cls._pool is None:
            return {"healthy": False, "error": "Not initialized"}
        try:
            async with cls.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return {
                "healthy": True,
                "pool_size": cls._pool.get_size(),
                "pool_idle": cls._pool.get_idle_size(),
            }
        except Exception as e:
            return {"healthy": False, "error": str(e)}


# =============================================================================
# Lifespan Events (FastAPI 0.95+)
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for database pool lifecycle.

    Usage:
        app = FastAPI(lifespan=lifespan)

    The pool is initialized on startup and closed on shutdown.
    """
    # Startup
    dsn = os.environ.get(
        'DATABASE_URL',
        'postgresql://trading:password@localhost:5432/trading_arena'
    )

    await DatabasePool.initialize(
        dsn=dsn,
        min_size=5,
        max_size=20,
        max_inactive_connection_lifetime=300,
        command_timeout=60,
    )

    yield  # Application runs

    # Shutdown
    await DatabasePool.close()


# Create FastAPI app with lifespan
app = FastAPI(
    title="Trading Arena API",
    lifespan=lifespan
)


# =============================================================================
# Dependency Injection
# =============================================================================

async def get_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    Dependency that provides a database connection.

    The connection is automatically returned to pool after request.

    Usage:
        @app.get("/users/{user_id}")
        async def get_user(
            user_id: int,
            conn: asyncpg.Connection = Depends(get_db_connection)
        ):
            ...
    """
    async with DatabasePool.acquire() as conn:
        yield conn


async def get_db_transaction() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    Dependency that provides a connection with active transaction.

    Transaction commits on success, rolls back on exception.

    Usage:
        @app.post("/orders")
        async def create_order(
            order: OrderCreate,
            conn: asyncpg.Connection = Depends(get_db_transaction)
        ):
            # All database operations here are in a transaction
            ...
    """
    async with DatabasePool.acquire() as conn:
        async with conn.transaction():
            yield conn


async def get_readonly_db() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    Dependency for read-only database access.

    Uses read-only transaction for safety and optimization.

    Usage:
        @app.get("/reports/summary")
        async def get_report(
            conn: asyncpg.Connection = Depends(get_readonly_db)
        ):
            ...
    """
    async with DatabasePool.acquire() as conn:
        async with conn.transaction(readonly=True):
            yield conn


async def get_db_pool() -> asyncpg.Pool:
    """
    Dependency that provides the raw pool.

    For advanced operations like executemany.
    """
    return DatabasePool.get_pool()


# =============================================================================
# Pydantic Models
# =============================================================================

class OrderCreate(BaseModel):
    collective_id: str
    symbol: str
    side: str  # "buy" or "sell"
    quantity: Decimal
    price: Decimal


class OrderResponse(BaseModel):
    id: int
    collective_id: str
    symbol: str
    side: str
    quantity: Decimal
    price: Decimal
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    status: str
    database: dict


# =============================================================================
# Repository Pattern
# =============================================================================

class OrderRepository:
    """
    Repository for Order entity.

    Encapsulates all database operations for orders.
    """

    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def create(self, order: OrderCreate) -> OrderResponse:
        """Create a new order."""
        row = await self.conn.fetchrow("""
            INSERT INTO orders (collective_id, symbol, side, quantity, price, status)
            VALUES ($1, $2, $3, $4, $5, 'pending')
            RETURNING id, collective_id, symbol, side, quantity, price, status, created_at, updated_at
        """, order.collective_id, order.symbol, order.side, order.quantity, order.price)

        return self._row_to_response(row)

    async def get_by_id(self, order_id: int) -> Optional[OrderResponse]:
        """Get order by ID."""
        row = await self.conn.fetchrow(
            "SELECT * FROM orders WHERE id = $1",
            order_id
        )
        return self._row_to_response(row) if row else None

    async def list_by_collective(
        self,
        collective_id: str,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[OrderResponse]:
        """List orders for a collective."""
        if status:
            rows = await self.conn.fetch("""
                SELECT * FROM orders
                WHERE collective_id = $1 AND status = $2
                ORDER BY created_at DESC LIMIT $3
            """, collective_id, status, limit)
        else:
            rows = await self.conn.fetch("""
                SELECT * FROM orders
                WHERE collective_id = $1
                ORDER BY created_at DESC LIMIT $2
            """, collective_id, limit)

        return [self._row_to_response(row) for row in rows]

    async def update_status(self, order_id: int, status: str) -> Optional[OrderResponse]:
        """Update order status."""
        row = await self.conn.fetchrow("""
            UPDATE orders
            SET status = $1, updated_at = NOW()
            WHERE id = $2
            RETURNING *
        """, status, order_id)

        return self._row_to_response(row) if row else None

    async def cancel(self, order_id: int) -> bool:
        """Cancel a pending order."""
        result = await self.conn.execute("""
            UPDATE orders
            SET status = 'cancelled', updated_at = NOW()
            WHERE id = $1 AND status = 'pending'
        """, order_id)

        return result == "UPDATE 1"

    def _row_to_response(self, row: asyncpg.Record) -> OrderResponse:
        """Convert database row to Pydantic model."""
        return OrderResponse(
            id=row['id'],
            collective_id=row['collective_id'],
            symbol=row['symbol'],
            side=row['side'],
            quantity=row['quantity'],
            price=row['price'],
            status=row['status'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
        )


async def get_order_repository(
    conn: asyncpg.Connection = Depends(get_db_connection)
) -> OrderRepository:
    """Dependency for OrderRepository."""
    return OrderRepository(conn)


async def get_order_repository_tx(
    conn: asyncpg.Connection = Depends(get_db_transaction)
) -> OrderRepository:
    """Dependency for OrderRepository with transaction."""
    return OrderRepository(conn)


# =============================================================================
# API Endpoints
# =============================================================================

# Health check router
health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get("", response_model=HealthResponse)
async def health_check():
    """Basic health check."""
    db_health = await DatabasePool.health_check()

    if not db_health.get("healthy"):
        raise HTTPException(status_code=503, detail=db_health)

    return HealthResponse(
        status="healthy",
        database=db_health
    )


@health_router.get("/db")
async def database_health():
    """Detailed database health."""
    return await DatabasePool.health_check()


# Orders router
orders_router = APIRouter(prefix="/orders", tags=["orders"])


@orders_router.post("", response_model=OrderResponse, status_code=201)
async def create_order(
    order: OrderCreate,
    repo: OrderRepository = Depends(get_order_repository_tx)
):
    """
    Create a new order.

    Uses transaction dependency - auto commits on success.
    """
    return await repo.create(order)


@orders_router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    repo: OrderRepository = Depends(get_order_repository)
):
    """Get order by ID."""
    order = await repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@orders_router.get("", response_model=List[OrderResponse])
async def list_orders(
    collective_id: str,
    status: Optional[str] = None,
    limit: int = 100,
    repo: OrderRepository = Depends(get_order_repository)
):
    """List orders for a collective."""
    return await repo.list_by_collective(collective_id, status, limit)


@orders_router.post("/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    repo: OrderRepository = Depends(get_order_repository_tx)
):
    """Cancel a pending order."""
    cancelled = await repo.cancel(order_id)
    if not cancelled:
        raise HTTPException(
            status_code=400,
            detail="Order cannot be cancelled (not found or not pending)"
        )
    return {"message": "Order cancelled"}


# Example endpoint with raw connection
@orders_router.get("/stats/summary")
async def order_stats(
    collective_id: str,
    conn: asyncpg.Connection = Depends(get_readonly_db)
):
    """
    Get order statistics.

    Uses read-only dependency for safety.
    """
    stats = await conn.fetchrow("""
        SELECT
            COUNT(*) as total_orders,
            COUNT(*) FILTER (WHERE status = 'filled') as filled_orders,
            COUNT(*) FILTER (WHERE status = 'pending') as pending_orders,
            COALESCE(SUM(quantity * price) FILTER (WHERE status = 'filled'), 0) as total_volume
        FROM orders
        WHERE collective_id = $1
    """, collective_id)

    return dict(stats)


# Register routers
app.include_router(health_router)
app.include_router(orders_router)


# =============================================================================
# Alternative: Event-based Lifecycle (Legacy FastAPI)
# =============================================================================

def create_legacy_app() -> FastAPI:
    """
    Create app with on_event handlers (pre-0.95 pattern).

    Use lifespan context manager for new applications.
    """
    legacy_app = FastAPI(title="Legacy Pattern")

    @legacy_app.on_event("startup")
    async def startup():
        await DatabasePool.initialize(
            dsn=os.environ.get('DATABASE_URL'),
            min_size=5,
            max_size=20,
        )

    @legacy_app.on_event("shutdown")
    async def shutdown():
        await DatabasePool.close()

    return legacy_app
