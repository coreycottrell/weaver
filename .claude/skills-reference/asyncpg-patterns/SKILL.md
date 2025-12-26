---
name: asyncpg-patterns
description: Production-ready asyncpg patterns for high-performance PostgreSQL in async Python. Covers connection pooling, prepared statements, transaction management, batch operations, error handling, and FastAPI integration. Essential for any async Python application with PostgreSQL, especially trading systems where database operations must not block.
version: 1.0.0
author: AI-CIV (capability-curator)
created: 2025-12-26
domain: database-infrastructure
priority: CRITICAL - database is the foundation; async patterns prevent blocking
---

# asyncpg Patterns for High-Performance PostgreSQL

This skill provides production-ready patterns for using asyncpg with PostgreSQL in async Python applications. It covers the complete database layer: connection pooling, prepared statements, transactions, batch operations, error handling, and FastAPI integration.

**Core Principle**: In async applications, blocking database operations defeat the purpose of async. asyncpg is a native async PostgreSQL driver that maintains non-blocking I/O throughout. This skill ensures you use it correctly.

## When to Use This Skill

**Invoke when**:
- Building async Python applications with PostgreSQL (FastAPI, aiohttp, etc.)
- High-throughput systems where database latency matters (trading, real-time)
- Need connection pooling for concurrent database access
- Batch operations on large datasets (COPY, executemany)
- Transaction management with savepoints

**Don't use when**:
- Using synchronous Python (use psycopg2/3 instead)
- Simple single-threaded scripts (asyncpg overhead not worth it)
- Using SQLAlchemy async (it wraps asyncpg but has own patterns)
- Non-PostgreSQL databases (asyncpg is PostgreSQL-only)

## Prerequisites

```bash
pip install asyncpg
```

asyncpg requires:
- Python 3.7+
- PostgreSQL 9.5+ (recommended: 14+)
- No libpq dependency (pure Python with C extension)

---

## Part 1: Core Concepts

### Why asyncpg?

asyncpg is **3x faster** than psycopg2 and **2x faster** than aiopg (async psycopg2 wrapper) in benchmarks. It achieves this through:

1. **Binary protocol**: Uses PostgreSQL's binary format (not text), reducing parsing overhead
2. **Native async**: Written from ground up for asyncio (not a wrapper)
3. **Prepared statements**: Automatic statement preparation and caching
4. **Connection pooling**: Built-in pool with proper async semantics
5. **Zero-copy**: Minimizes memory allocations

### asyncpg vs psycopg2/3

| Feature | asyncpg | psycopg2 | psycopg3 (async) |
|---------|---------|----------|------------------|
| Async native | Yes | No | Yes |
| Binary protocol | Yes | Optional | Optional |
| Connection pool | Built-in | External | Built-in |
| Prepared statements | Auto | Manual | Auto |
| Performance | Fastest | Medium | Fast |
| ORM support | Manual | SQLAlchemy | SQLAlchemy |

---

## Part 2: Connection Management

### Single Connection (Development/Testing)

```python
# database/connection.py
"""
Single connection pattern for development and testing.
DO NOT use in production - no pooling, no connection management.
"""

import asyncpg
from typing import Optional

async def get_connection() -> asyncpg.Connection:
    """
    Create a single database connection.

    Returns:
        asyncpg.Connection: Active database connection
    """
    return await asyncpg.connect(
        host='localhost',
        port=5432,
        user='trading_arena',
        password='your_password',
        database='trading_arena',
        # Connection timeout in seconds
        timeout=60,
        # Statement cache size (0 to disable)
        statement_cache_size=100,
    )


async def example_single_connection():
    """Example: single connection usage."""
    conn = await get_connection()
    try:
        result = await conn.fetch('SELECT * FROM users WHERE active = $1', True)
        for row in result:
            print(dict(row))  # asyncpg.Record is dict-like
    finally:
        await conn.close()
```

### Connection Pooling (Production)

Connection pooling is **essential** for production. Without it:
- Each request creates a new TCP connection (slow)
- PostgreSQL has connection limits (typically 100-500)
- Connection creation blocks async event loop briefly

```python
# database/pool.py
"""
Production-ready connection pool with proper lifecycle management.
"""

import asyncpg
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DatabasePool:
    """
    Singleton connection pool manager.

    Usage:
        # At startup
        await DatabasePool.initialize(dsn="postgresql://...")

        # During request handling
        async with DatabasePool.acquire() as conn:
            await conn.fetch(...)

        # At shutdown
        await DatabasePool.close()
    """

    _pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def initialize(
        cls,
        dsn: Optional[str] = None,
        *,
        host: str = 'localhost',
        port: int = 5432,
        user: str = 'postgres',
        password: str = '',
        database: str = 'postgres',
        min_size: int = 5,
        max_size: int = 20,
        max_inactive_connection_lifetime: float = 300.0,
        command_timeout: float = 60.0,
    ) -> asyncpg.Pool:
        """
        Initialize the connection pool.

        Args:
            dsn: PostgreSQL connection string (overrides individual params)
            host: Database host
            port: Database port
            user: Database user
            password: Database password
            database: Database name
            min_size: Minimum pool connections (keep warm)
            max_size: Maximum pool connections (limit)
            max_inactive_connection_lifetime: Close idle connections after seconds
            command_timeout: Default query timeout in seconds

        Returns:
            Initialized connection pool

        Pool Sizing Guidelines:
            - min_size: 2-5 for most apps (keep connections warm)
            - max_size: 10-50 depending on PostgreSQL max_connections
            - Formula: max_size = (PostgreSQL max_connections - 10) / num_app_instances
        """
        if cls._pool is not None:
            logger.warning("Pool already initialized, returning existing pool")
            return cls._pool

        if dsn:
            cls._pool = await asyncpg.create_pool(
                dsn,
                min_size=min_size,
                max_size=max_size,
                max_inactive_connection_lifetime=max_inactive_connection_lifetime,
                command_timeout=command_timeout,
            )
        else:
            cls._pool = await asyncpg.create_pool(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                min_size=min_size,
                max_size=max_size,
                max_inactive_connection_lifetime=max_inactive_connection_lifetime,
                command_timeout=command_timeout,
            )

        logger.info(f"Database pool initialized: min={min_size}, max={max_size}")
        return cls._pool

    @classmethod
    async def close(cls):
        """Close the connection pool gracefully."""
        if cls._pool is not None:
            await cls._pool.close()
            cls._pool = None
            logger.info("Database pool closed")

    @classmethod
    def acquire(cls):
        """
        Acquire a connection from the pool.

        Usage:
            async with DatabasePool.acquire() as conn:
                await conn.fetch(...)

        The connection is automatically returned to pool when context exits.
        """
        if cls._pool is None:
            raise RuntimeError("Database pool not initialized. Call initialize() first.")
        return cls._pool.acquire()

    @classmethod
    def get_pool(cls) -> asyncpg.Pool:
        """Get the raw pool instance (for advanced usage)."""
        if cls._pool is None:
            raise RuntimeError("Database pool not initialized. Call initialize() first.")
        return cls._pool

    @classmethod
    async def health_check(cls) -> dict:
        """
        Check pool health and connection status.

        Returns:
            Dict with pool statistics and health status
        """
        if cls._pool is None:
            return {"status": "not_initialized", "healthy": False}

        try:
            # Test a simple query
            async with cls.acquire() as conn:
                await conn.fetchval("SELECT 1")

            return {
                "status": "healthy",
                "healthy": True,
                "pool_size": cls._pool.get_size(),
                "pool_free": cls._pool.get_idle_size(),
                "pool_used": cls._pool.get_size() - cls._pool.get_idle_size(),
                "pool_min": cls._pool.get_min_size(),
                "pool_max": cls._pool.get_max_size(),
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "healthy": False,
                "error": str(e),
            }


# Convenience functions for direct import
async def initialize_db(**kwargs):
    """Initialize database pool."""
    return await DatabasePool.initialize(**kwargs)

async def close_db():
    """Close database pool."""
    await DatabasePool.close()

def get_db():
    """Get connection context manager."""
    return DatabasePool.acquire()
```

### Pool Configuration Guidelines

| Application Type | min_size | max_size | max_inactive_lifetime |
|------------------|----------|----------|----------------------|
| Low traffic API | 2 | 10 | 300s |
| Medium traffic API | 5 | 20 | 300s |
| High traffic API | 10 | 50 | 120s |
| Background workers | 2 | 10 | 600s |
| Trading system | 10 | 30 | 60s |

**Critical**: Never set `max_size` higher than PostgreSQL's `max_connections` minus some buffer (10-20) for admin connections.

---

## Part 3: Prepared Statements

asyncpg automatically prepares statements for performance. Understanding this is key to optimal usage.

### How Prepared Statements Work

```python
# The first call prepares the statement and caches it
await conn.fetch("SELECT * FROM users WHERE id = $1", user_id)

# Subsequent calls with same SQL reuse the prepared statement
# (only sends parameter values, not the SQL)
await conn.fetch("SELECT * FROM users WHERE id = $1", other_id)
```

### Statement Cache Configuration

```python
# Per-connection cache size (default: 1024)
conn = await asyncpg.connect(
    ...,
    statement_cache_size=1024,  # 0 to disable
)

# Check cache status
print(f"Cached statements: {len(conn._stmt_cache)}")
```

### Explicit Prepared Statements

For queries executed many times (e.g., in loops), explicitly prepare:

```python
# database/prepared.py
"""
Patterns for explicit prepared statement management.
"""

import asyncpg
from typing import List, Any


async def bulk_user_lookup(
    conn: asyncpg.Connection,
    user_ids: List[int]
) -> List[dict]:
    """
    Look up many users efficiently with explicit prepared statement.

    This is ~20-30% faster than implicit preparation for large batches.
    """
    # Prepare once
    stmt = await conn.prepare("SELECT * FROM users WHERE id = $1")

    results = []
    for user_id in user_ids:
        # Execute prepared statement (no SQL parsing)
        row = await stmt.fetchrow(user_id)
        if row:
            results.append(dict(row))

    return results


async def prepared_statement_with_types(conn: asyncpg.Connection):
    """
    Prepared statements preserve type information for optimal transfer.
    """
    # asyncpg infers types from parameters and caches them
    stmt = await conn.prepare("""
        INSERT INTO orders (collective_id, symbol, side, quantity, price, status)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id, created_at
    """)

    # The statement knows $4 is numeric, $5 is numeric, etc.
    # Binary transfer uses optimal encoding per type
    result = await stmt.fetchrow(
        "collective-001",  # $1: text
        "BTC-USD",         # $2: text
        "buy",             # $3: text (or enum)
        "0.5",             # $4: will convert to numeric
        "45000.00",        # $5: will convert to numeric
        "pending",         # $6: text (or enum)
    )

    return result


async def statement_caching_gotcha():
    """
    GOTCHA: Dynamic SQL defeats prepared statement caching.
    """
    # BAD - each call has different SQL, no caching benefit
    async def bad_pattern(conn, table_name):
        return await conn.fetch(f"SELECT * FROM {table_name}")  # No caching!

    # GOOD - use a mapping of known tables with prepared statements
    async def good_pattern(conn, table_name):
        if table_name not in ['users', 'orders', 'positions']:
            raise ValueError("Unknown table")

        # These are all cached separately
        if table_name == 'users':
            return await conn.fetch("SELECT * FROM users")
        elif table_name == 'orders':
            return await conn.fetch("SELECT * FROM orders")
        # ...
```

---

## Part 4: Transaction Patterns

### Basic Transaction (Context Manager)

```python
# database/transactions.py
"""
Transaction patterns for asyncpg.
"""

import asyncpg
from typing import Optional, TypeVar, Callable, Any
from functools import wraps
from decimal import Decimal


async def basic_transaction(conn: asyncpg.Connection):
    """
    Basic transaction with automatic commit/rollback.
    """
    async with conn.transaction():
        # All operations here are in a transaction
        await conn.execute(
            "UPDATE balances SET amount = amount - $1 WHERE collective_id = $2",
            Decimal("100.00"),
            "collective-001"
        )
        await conn.execute(
            "UPDATE balances SET amount = amount + $1 WHERE collective_id = $2",
            Decimal("100.00"),
            "collective-002"
        )
        # Transaction commits automatically if no exception
    # If exception raised, transaction is rolled back


async def transaction_with_return_value(conn: asyncpg.Connection) -> int:
    """
    Transaction that returns a value.
    """
    async with conn.transaction():
        result = await conn.fetchval("""
            INSERT INTO orders (collective_id, symbol, quantity)
            VALUES ($1, $2, $3)
            RETURNING id
        """, "collective-001", "BTC-USD", Decimal("0.5"))

        await conn.execute("""
            INSERT INTO order_audit (order_id, action)
            VALUES ($1, 'created')
        """, result)

        return result  # Transaction commits, then returns
```

### Savepoints (Nested Transactions)

```python
async def transaction_with_savepoints(conn: asyncpg.Connection):
    """
    Savepoints allow partial rollback within a transaction.

    Use case: Insert multiple items, skip failures, continue processing.
    """
    async with conn.transaction():
        # Main transaction starts

        for item in items_to_process:
            try:
                # Create savepoint
                async with conn.transaction():
                    await process_item(conn, item)
                    # If this succeeds, savepoint is released
            except Exception as e:
                # Savepoint is rolled back, but main transaction continues
                logger.warning(f"Skipping item due to error: {e}")

        # Main transaction commits (including successful items)


async def explicit_savepoint_control(conn: asyncpg.Connection):
    """
    Manual savepoint control for complex scenarios.
    """
    tr = conn.transaction()
    await tr.start()

    try:
        await conn.execute("INSERT INTO audit (event) VALUES ('start')")

        # Create named savepoint
        savepoint = await tr.savepoint()

        try:
            await conn.execute("INSERT INTO risky_table VALUES ($1)", dangerous_value)
        except Exception:
            # Rollback to savepoint only
            await tr.rollback_to(savepoint)
            await conn.execute("INSERT INTO audit (event) VALUES ('risky_failed')")

        await conn.execute("INSERT INTO audit (event) VALUES ('end')")
        await tr.commit()

    except Exception:
        await tr.rollback()
        raise
```

### Isolation Levels

```python
async def transaction_isolation_levels(conn: asyncpg.Connection):
    """
    PostgreSQL isolation levels via asyncpg.

    Levels (least to most strict):
    - read_committed (default): See committed changes from other transactions
    - repeatable_read: Snapshot at transaction start
    - serializable: Full serializability (may need retries)
    """
    from asyncpg.transaction import IsolationLevel

    # Read Committed (default) - each statement sees latest committed data
    async with conn.transaction():
        await conn.fetch("SELECT * FROM orders")

    # Repeatable Read - consistent snapshot throughout transaction
    async with conn.transaction(isolation='repeatable_read'):
        balance1 = await conn.fetchval("SELECT balance FROM accounts WHERE id = 1")
        # ... other work ...
        balance2 = await conn.fetchval("SELECT balance FROM accounts WHERE id = 1")
        # balance1 == balance2 guaranteed (even if changed by other transactions)

    # Serializable - strictest, transactions behave as if run sequentially
    # May raise SerializationError - must be prepared to retry
    async with conn.transaction(isolation='serializable'):
        await conn.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
        await conn.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")


async def serializable_with_retry(conn: asyncpg.Connection, max_retries: int = 3):
    """
    Serializable transactions may need retry on conflict.
    """
    for attempt in range(max_retries):
        try:
            async with conn.transaction(isolation='serializable'):
                await execute_critical_operation(conn)
                return  # Success
        except asyncpg.SerializationError:
            if attempt < max_retries - 1:
                logger.warning(f"Serialization conflict, retry {attempt + 1}")
                await asyncio.sleep(0.1 * (2 ** attempt))  # Exponential backoff
            else:
                raise
```

### Read-Only Transactions

```python
async def read_only_transaction(conn: asyncpg.Connection):
    """
    Read-only transactions for reporting/analytics.

    Benefits:
    - PostgreSQL can optimize (no write locks needed)
    - Prevents accidental writes
    - Can use standby replicas
    """
    async with conn.transaction(readonly=True):
        # Any write attempt will raise an error
        total = await conn.fetchval("SELECT SUM(amount) FROM transactions")
        count = await conn.fetchval("SELECT COUNT(*) FROM transactions")
        return {"total": total, "count": count}
```

---

## Part 5: Batch Operations

### executemany (Multiple Inserts)

```python
# database/batch.py
"""
Batch operation patterns for high-throughput scenarios.
"""

import asyncpg
from typing import List, Tuple
from decimal import Decimal


async def batch_insert(
    conn: asyncpg.Connection,
    orders: List[Tuple[str, str, str, Decimal, Decimal]]
) -> int:
    """
    Insert multiple rows efficiently with executemany.

    Args:
        orders: List of (collective_id, symbol, side, quantity, price)

    Returns:
        Number of rows inserted
    """
    # executemany prepares once, executes N times with different params
    await conn.executemany("""
        INSERT INTO orders (collective_id, symbol, side, quantity, price)
        VALUES ($1, $2, $3, $4, $5)
    """, orders)

    return len(orders)


async def batch_insert_with_returning(
    conn: asyncpg.Connection,
    orders: List[dict]
) -> List[int]:
    """
    Batch insert with RETURNING (get generated IDs).

    Note: executemany doesn't support RETURNING, so we use a single
    multi-row INSERT with unnest.
    """
    # Extract columns
    collective_ids = [o['collective_id'] for o in orders]
    symbols = [o['symbol'] for o in orders]
    sides = [o['side'] for o in orders]
    quantities = [o['quantity'] for o in orders]
    prices = [o['price'] for o in orders]

    # Single INSERT with unnest (PostgreSQL array expansion)
    ids = await conn.fetch("""
        INSERT INTO orders (collective_id, symbol, side, quantity, price)
        SELECT * FROM unnest($1::text[], $2::text[], $3::text[], $4::numeric[], $5::numeric[])
        RETURNING id
    """, collective_ids, symbols, sides, quantities, prices)

    return [row['id'] for row in ids]
```

### COPY Protocol (Bulk Loading)

For truly massive data loads (100K+ rows), COPY is **10-100x faster** than INSERT:

```python
async def copy_from_records(
    conn: asyncpg.Connection,
    table: str,
    records: List[Tuple],
    columns: List[str]
) -> int:
    """
    Bulk load using PostgreSQL COPY protocol.

    Performance comparison (100K rows):
    - executemany: ~10-30 seconds
    - COPY: ~0.5-2 seconds
    """
    # copy_records_to_table uses PostgreSQL's binary COPY
    return await conn.copy_records_to_table(
        table,
        records=records,
        columns=columns,
    )


async def copy_trades_example(conn: asyncpg.Connection, trades: List[dict]) -> int:
    """
    Example: Bulk load trades using COPY.
    """
    records = [
        (
            t['collective_id'],
            t['symbol'],
            t['side'],
            t['quantity'],
            t['price'],
            t['fee'],
            t['executed_at'],
        )
        for t in trades
    ]

    columns = ['collective_id', 'symbol', 'side', 'quantity', 'price', 'fee', 'executed_at']

    return await conn.copy_records_to_table(
        'trades',
        records=records,
        columns=columns,
    )


async def copy_from_csv(conn: asyncpg.Connection, filepath: str):
    """
    Load data from CSV file using COPY.
    """
    with open(filepath, 'rb') as f:
        # copy_to_table reads from file-like object
        await conn.copy_to_table(
            'trades',
            source=f,
            format='csv',
            header=True,
            delimiter=',',
        )


async def copy_to_file(conn: asyncpg.Connection, query: str, filepath: str):
    """
    Export query results to file using COPY.
    """
    with open(filepath, 'wb') as f:
        await conn.copy_from_query(
            query,
            output=f,
            format='csv',
            header=True,
        )
```

### Batch Updates

```python
async def batch_update(
    conn: asyncpg.Connection,
    updates: List[Tuple[int, Decimal]]  # (order_id, new_quantity)
) -> int:
    """
    Batch update using VALUES and UPDATE FROM.

    This is more efficient than multiple UPDATE statements.
    """
    if not updates:
        return 0

    # Use a CTE with VALUES for batch update
    result = await conn.execute("""
        UPDATE orders
        SET quantity = updates.new_quantity,
            updated_at = NOW()
        FROM (
            SELECT * FROM unnest($1::int[], $2::numeric[])
            AS t(order_id, new_quantity)
        ) AS updates
        WHERE orders.id = updates.order_id
    """,
        [u[0] for u in updates],
        [u[1] for u in updates]
    )

    # Parse "UPDATE N" response
    return int(result.split()[-1])
```

---

## Part 6: Error Handling

### asyncpg Exception Hierarchy

```python
# database/errors.py
"""
Error handling patterns for asyncpg.
"""

import asyncpg
import asyncio
from typing import TypeVar, Callable, Any
from functools import wraps
import logging

logger = logging.getLogger(__name__)


"""
asyncpg Exception Hierarchy:

asyncpg.PostgresError (base for all PostgreSQL errors)
├── asyncpg.InterfaceError (driver/connection issues)
├── asyncpg.PostgresSyntaxError (SQL syntax error)
├── asyncpg.DataError (invalid data type/format)
├── asyncpg.IntegrityConstraintViolationError
│   ├── asyncpg.UniqueViolationError (duplicate key)
│   ├── asyncpg.ForeignKeyViolationError (FK constraint)
│   ├── asyncpg.NotNullViolationError (NULL in NOT NULL column)
│   └── asyncpg.CheckViolationError (CHECK constraint)
├── asyncpg.TransactionRollbackError
│   ├── asyncpg.SerializationError (serializable isolation conflict)
│   └── asyncpg.DeadlockDetectedError (deadlock)
├── asyncpg.OperationalError
│   └── asyncpg.QueryCanceledError (timeout)
└── asyncpg.InternalServerError (PostgreSQL internal error)

Non-PostgreSQL errors:
├── asyncpg.InterfaceError (connection issues)
├── asyncpg.ConnectionDoesNotExistError
├── asyncpg.TooManyConnectionsError
└── asyncio.TimeoutError (connection/query timeout)
"""


async def handle_database_errors(conn: asyncpg.Connection):
    """
    Comprehensive error handling example.
    """
    try:
        await conn.execute("""
            INSERT INTO users (email, collective_id)
            VALUES ($1, $2)
        """, "test@example.com", "collective-001")

    except asyncpg.UniqueViolationError as e:
        # Duplicate key - safe to handle gracefully
        logger.warning(f"Duplicate entry: {e.detail}")
        raise ValueError("User already exists") from e

    except asyncpg.ForeignKeyViolationError as e:
        # Referenced row doesn't exist
        logger.warning(f"Foreign key violation: {e.detail}")
        raise ValueError("Collective not found") from e

    except asyncpg.CheckViolationError as e:
        # Value failed CHECK constraint
        logger.warning(f"Check constraint violated: {e.detail}")
        raise ValueError("Invalid data") from e

    except asyncpg.SerializationError:
        # Serializable transaction conflict - retry
        logger.warning("Serialization conflict - retrying")
        raise  # Let caller retry

    except asyncpg.DeadlockDetectedError:
        # Deadlock - PostgreSQL chose this transaction to abort
        logger.error("Deadlock detected")
        raise  # Let caller decide

    except asyncpg.QueryCanceledError:
        # Query exceeded timeout
        logger.error("Query timeout")
        raise TimeoutError("Database query timed out")

    except asyncpg.ConnectionDoesNotExistError:
        # Connection was closed
        logger.error("Connection lost")
        raise RuntimeError("Database connection lost")

    except asyncpg.PostgresError as e:
        # Catch-all for other PostgreSQL errors
        logger.error(f"Database error: {e}")
        raise
```

### Retry Decorator

```python
T = TypeVar('T')


def with_retry(
    max_retries: int = 3,
    retry_on: tuple = (asyncpg.SerializationError, asyncpg.DeadlockDetectedError),
    backoff_base: float = 0.1,
):
    """
    Decorator for database operations that should be retried on transient errors.

    Args:
        max_retries: Maximum retry attempts
        retry_on: Exception types to retry on
        backoff_base: Base delay for exponential backoff
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except retry_on as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        delay = backoff_base * (2 ** attempt)
                        logger.warning(
                            f"{func.__name__} failed (attempt {attempt + 1}), "
                            f"retrying in {delay}s: {e}"
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger.error(f"{func.__name__} failed after {max_retries} attempts")
            raise last_error
        return wrapper
    return decorator


# Usage
@with_retry(max_retries=3, retry_on=(asyncpg.SerializationError,))
async def transfer_funds(conn: asyncpg.Connection, from_id: str, to_id: str, amount: Decimal):
    async with conn.transaction(isolation='serializable'):
        await conn.execute(
            "UPDATE balances SET amount = amount - $1 WHERE collective_id = $2",
            amount, from_id
        )
        await conn.execute(
            "UPDATE balances SET amount = amount + $1 WHERE collective_id = $2",
            amount, to_id
        )
```

### Connection Error Recovery

```python
class ResilientDatabasePool:
    """
    Connection pool with automatic recovery from connection errors.
    """

    def __init__(self, dsn: str, **pool_kwargs):
        self.dsn = dsn
        self.pool_kwargs = pool_kwargs
        self._pool: Optional[asyncpg.Pool] = None
        self._lock = asyncio.Lock()

    async def get_pool(self) -> asyncpg.Pool:
        """Get or recreate the connection pool."""
        if self._pool is None or self._pool._closed:
            async with self._lock:
                if self._pool is None or self._pool._closed:
                    self._pool = await asyncpg.create_pool(
                        self.dsn,
                        **self.pool_kwargs
                    )
        return self._pool

    async def execute_with_recovery(self, query: str, *args, max_retries: int = 2):
        """
        Execute query with automatic connection recovery.
        """
        for attempt in range(max_retries):
            try:
                pool = await self.get_pool()
                async with pool.acquire() as conn:
                    return await conn.fetch(query, *args)

            except (asyncpg.ConnectionDoesNotExistError,
                    asyncpg.InterfaceError,
                    asyncio.TimeoutError) as e:
                logger.warning(f"Connection error (attempt {attempt + 1}): {e}")

                # Force pool recreation on next attempt
                if self._pool:
                    try:
                        await self._pool.close()
                    except:
                        pass
                    self._pool = None

                if attempt >= max_retries - 1:
                    raise

                await asyncio.sleep(0.5 * (attempt + 1))
```

---

## Part 7: FastAPI Integration

### Lifespan Events (Recommended)

```python
# main.py
"""
FastAPI integration with asyncpg connection pool.
Uses lifespan context manager (recommended for FastAPI 0.95+).
"""

from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
import asyncpg
from typing import AsyncGenerator

from database.pool import DatabasePool


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for database pool lifecycle.

    - Startup: Initialize connection pool
    - Shutdown: Close connection pool gracefully
    """
    # Startup
    await DatabasePool.initialize(
        dsn="postgresql://trading:password@localhost:5432/trading_arena",
        min_size=5,
        max_size=20,
    )

    yield

    # Shutdown
    await DatabasePool.close()


app = FastAPI(lifespan=lifespan)


# Dependency for getting database connection
async def get_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    FastAPI dependency that provides a database connection.

    Connection is acquired from pool and automatically released.
    """
    async with DatabasePool.acquire() as conn:
        yield conn


# Alternative: get pool directly
async def get_db_pool() -> asyncpg.Pool:
    """Get the raw pool for advanced operations."""
    return DatabasePool.get_pool()


# Usage in route
@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    """Example endpoint using database connection."""
    row = await conn.fetchrow(
        "SELECT * FROM users WHERE id = $1",
        user_id
    )
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(row)


@app.get("/health/db")
async def health_check():
    """Database health check endpoint."""
    health = await DatabasePool.health_check()
    if not health["healthy"]:
        raise HTTPException(status_code=503, detail=health)
    return health
```

### Transaction Dependency

```python
# dependencies/database.py
"""
Advanced FastAPI dependencies for database transactions.
"""

from fastapi import Depends
import asyncpg
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from database.pool import DatabasePool


@asynccontextmanager
async def get_transaction() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    Context manager that provides a connection with active transaction.

    Commits on success, rolls back on exception.
    """
    async with DatabasePool.acquire() as conn:
        async with conn.transaction():
            yield conn


async def get_db_transaction() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    FastAPI dependency for transactional database access.

    Usage:
        @app.post("/orders")
        async def create_order(
            order: OrderCreate,
            conn: asyncpg.Connection = Depends(get_db_transaction)
        ):
            # All operations in this handler are in a transaction
            ...
    """
    async with DatabasePool.acquire() as conn:
        async with conn.transaction():
            yield conn


async def get_readonly_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    FastAPI dependency for read-only database access.

    Uses read-only transaction for safety.
    """
    async with DatabasePool.acquire() as conn:
        async with conn.transaction(readonly=True):
            yield conn


# Usage
@app.post("/orders")
async def create_order(
    order: OrderCreate,
    conn: asyncpg.Connection = Depends(get_db_transaction)
):
    """Create order within a transaction."""
    order_id = await conn.fetchval("""
        INSERT INTO orders (collective_id, symbol, quantity, price)
        VALUES ($1, $2, $3, $4)
        RETURNING id
    """, order.collective_id, order.symbol, order.quantity, order.price)

    await conn.execute("""
        INSERT INTO order_audit (order_id, action, details)
        VALUES ($1, 'created', $2)
    """, order_id, order.json())

    return {"id": order_id}
    # Transaction commits automatically if no exception


@app.get("/orders")
async def list_orders(
    conn: asyncpg.Connection = Depends(get_readonly_connection)
):
    """List orders (read-only)."""
    rows = await conn.fetch("SELECT * FROM orders ORDER BY created_at DESC LIMIT 100")
    return [dict(row) for row in rows]
```

### Repository Pattern

```python
# repositories/orders.py
"""
Repository pattern for database access with asyncpg.
"""

import asyncpg
from typing import List, Optional
from decimal import Decimal
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Order:
    id: int
    collective_id: str
    symbol: str
    side: str
    quantity: Decimal
    price: Decimal
    status: str
    created_at: datetime
    updated_at: datetime


class OrderRepository:
    """
    Repository for Order entity database operations.

    Encapsulates all SQL for order operations.
    """

    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def create(
        self,
        collective_id: str,
        symbol: str,
        side: str,
        quantity: Decimal,
        price: Decimal,
    ) -> Order:
        """Create a new order."""
        row = await self.conn.fetchrow("""
            INSERT INTO orders (collective_id, symbol, side, quantity, price, status)
            VALUES ($1, $2, $3, $4, $5, 'pending')
            RETURNING *
        """, collective_id, symbol, side, quantity, price)

        return self._row_to_order(row)

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        """Get order by ID."""
        row = await self.conn.fetchrow(
            "SELECT * FROM orders WHERE id = $1",
            order_id
        )
        return self._row_to_order(row) if row else None

    async def list_by_collective(
        self,
        collective_id: str,
        status: Optional[str] = None,
        limit: int = 100,
    ) -> List[Order]:
        """List orders for a collective."""
        if status:
            rows = await self.conn.fetch("""
                SELECT * FROM orders
                WHERE collective_id = $1 AND status = $2
                ORDER BY created_at DESC
                LIMIT $3
            """, collective_id, status, limit)
        else:
            rows = await self.conn.fetch("""
                SELECT * FROM orders
                WHERE collective_id = $1
                ORDER BY created_at DESC
                LIMIT $2
            """, collective_id, limit)

        return [self._row_to_order(row) for row in rows]

    async def update_status(
        self,
        order_id: int,
        status: str,
    ) -> Optional[Order]:
        """Update order status."""
        row = await self.conn.fetchrow("""
            UPDATE orders
            SET status = $1, updated_at = NOW()
            WHERE id = $2
            RETURNING *
        """, status, order_id)

        return self._row_to_order(row) if row else None

    async def cancel(self, order_id: int) -> bool:
        """Cancel an order if it's still pending."""
        result = await self.conn.execute("""
            UPDATE orders
            SET status = 'cancelled', updated_at = NOW()
            WHERE id = $1 AND status = 'pending'
        """, order_id)

        return result == "UPDATE 1"

    def _row_to_order(self, row: asyncpg.Record) -> Order:
        """Convert database row to Order dataclass."""
        return Order(
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


# FastAPI integration
async def get_order_repository(
    conn: asyncpg.Connection = Depends(get_db_connection)
) -> OrderRepository:
    """FastAPI dependency for OrderRepository."""
    return OrderRepository(conn)


@app.post("/orders")
async def create_order(
    order: OrderCreate,
    repo: OrderRepository = Depends(get_order_repository)
):
    """Create order using repository."""
    created = await repo.create(
        collective_id=order.collective_id,
        symbol=order.symbol,
        side=order.side,
        quantity=order.quantity,
        price=order.price,
    )
    return created
```

---

## Part 8: Connection Health Checks

### Health Check Endpoint

```python
# api/health.py
"""
Database health check endpoints.
"""

from fastapi import APIRouter, HTTPException
from database.pool import DatabasePool
import asyncio

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/db")
async def database_health():
    """
    Comprehensive database health check.

    Returns pool statistics and connection health.
    """
    health = await DatabasePool.health_check()

    if not health["healthy"]:
        raise HTTPException(status_code=503, detail=health)

    return health


@router.get("/db/deep")
async def database_deep_health():
    """
    Deep health check - verifies actual query execution.

    More expensive, use sparingly (e.g., every 30s).
    """
    try:
        async with DatabasePool.acquire() as conn:
            # Test basic connectivity
            version = await conn.fetchval("SELECT version()")

            # Test a simple table query
            start = asyncio.get_event_loop().time()
            await conn.fetchval("SELECT COUNT(*) FROM orders")
            query_time = asyncio.get_event_loop().time() - start

            # Test write (if needed)
            # await conn.execute("SELECT pg_advisory_lock(12345)")
            # await conn.execute("SELECT pg_advisory_unlock(12345)")

            return {
                "status": "healthy",
                "postgres_version": version.split()[1] if version else "unknown",
                "query_latency_ms": round(query_time * 1000, 2),
                "pool": {
                    "size": DatabasePool.get_pool().get_size(),
                    "free": DatabasePool.get_pool().get_idle_size(),
                },
            }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
            }
        )
```

### Connection Pool Monitoring

```python
# monitoring/database.py
"""
Database monitoring and metrics collection.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
import logging

from database.pool import DatabasePool

logger = logging.getLogger(__name__)


@dataclass
class PoolMetrics:
    timestamp: datetime
    total_connections: int
    idle_connections: int
    active_connections: int
    waiting_requests: int


class DatabaseMonitor:
    """
    Monitor database pool health and collect metrics.
    """

    def __init__(self, collect_interval: float = 10.0):
        self.collect_interval = collect_interval
        self._metrics_history: List[PoolMetrics] = []
        self._max_history = 360  # 1 hour at 10s intervals
        self._running = False

    async def start(self):
        """Start background metrics collection."""
        self._running = True
        asyncio.create_task(self._collect_loop())
        logger.info("Database monitor started")

    async def stop(self):
        """Stop metrics collection."""
        self._running = False

    async def _collect_loop(self):
        """Background loop to collect metrics."""
        while self._running:
            try:
                pool = DatabasePool.get_pool()

                metrics = PoolMetrics(
                    timestamp=datetime.utcnow(),
                    total_connections=pool.get_size(),
                    idle_connections=pool.get_idle_size(),
                    active_connections=pool.get_size() - pool.get_idle_size(),
                    waiting_requests=0,  # Not directly available in asyncpg
                )

                self._metrics_history.append(metrics)

                # Trim history
                if len(self._metrics_history) > self._max_history:
                    self._metrics_history = self._metrics_history[-self._max_history:]

                # Alert on concerning patterns
                if metrics.active_connections == pool.get_max_size():
                    logger.warning(
                        f"Database pool exhausted: {metrics.active_connections}/"
                        f"{pool.get_max_size()} connections in use"
                    )

                if metrics.idle_connections == 0 and metrics.total_connections > 5:
                    logger.warning("No idle database connections available")

            except Exception as e:
                logger.error(f"Error collecting database metrics: {e}")

            await asyncio.sleep(self.collect_interval)

    def get_current_metrics(self) -> Optional[PoolMetrics]:
        """Get most recent metrics."""
        return self._metrics_history[-1] if self._metrics_history else None

    def get_metrics_history(self, minutes: int = 10) -> List[PoolMetrics]:
        """Get metrics history for last N minutes."""
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        return [m for m in self._metrics_history if m.timestamp > cutoff]
```

---

## Part 9: Common Pitfalls

### Pitfall 1: Connection Exhaustion

**Problem**: All pool connections are in use, new requests wait/timeout.

```python
# BAD - Connection held too long
async def bad_example(pool: asyncpg.Pool):
    async with pool.acquire() as conn:
        result = await conn.fetch("SELECT * FROM large_table")
        # Processing takes 30 seconds while holding connection
        await slow_processing(result)  # DON'T DO THIS
        # Connection blocked for 30+ seconds


# GOOD - Release connection before processing
async def good_example(pool: asyncpg.Pool):
    async with pool.acquire() as conn:
        result = await conn.fetch("SELECT * FROM large_table")
    # Connection released immediately

    # Process outside connection context
    await slow_processing(result)  # Connection is free for others
```

### Pitfall 2: Transaction Leaks

**Problem**: Transaction started but never committed/rolled back.

```python
# BAD - Manual transaction without proper cleanup
async def bad_transaction(conn: asyncpg.Connection):
    tr = conn.transaction()
    await tr.start()

    await conn.execute("INSERT INTO ...")
    # If exception here, transaction is never closed!
    await conn.execute("INSERT INTO ...")

    await tr.commit()


# GOOD - Use context manager
async def good_transaction(conn: asyncpg.Connection):
    async with conn.transaction():
        await conn.execute("INSERT INTO ...")
        await conn.execute("INSERT INTO ...")
    # Automatically committed or rolled back
```

### Pitfall 3: N+1 Query Problem

**Problem**: Querying related data in a loop.

```python
# BAD - N+1 queries
async def bad_n_plus_one(conn: asyncpg.Connection):
    orders = await conn.fetch("SELECT * FROM orders LIMIT 100")

    for order in orders:
        # 100 additional queries!
        trades = await conn.fetch(
            "SELECT * FROM trades WHERE order_id = $1",
            order['id']
        )
        order['trades'] = trades


# GOOD - Single query with JOIN or subquery
async def good_joined(conn: asyncpg.Connection):
    orders = await conn.fetch("""
        SELECT o.*,
               COALESCE(
                   json_agg(t.*) FILTER (WHERE t.id IS NOT NULL),
                   '[]'
               ) as trades
        FROM orders o
        LEFT JOIN trades t ON t.order_id = o.id
        GROUP BY o.id
        LIMIT 100
    """)
    return orders


# GOOD - Batch query with IN clause
async def good_batch(conn: asyncpg.Connection):
    orders = await conn.fetch("SELECT * FROM orders LIMIT 100")
    order_ids = [o['id'] for o in orders]

    # Single query for all trades
    trades = await conn.fetch(
        "SELECT * FROM trades WHERE order_id = ANY($1)",
        order_ids
    )

    # Group trades by order_id
    trades_by_order = {}
    for t in trades:
        trades_by_order.setdefault(t['order_id'], []).append(t)

    # Attach to orders
    for order in orders:
        order['trades'] = trades_by_order.get(order['id'], [])

    return orders
```

### Pitfall 4: Float Precision in Financial Data

**Problem**: Using Python floats for financial calculations.

```python
# BAD - Float precision loss
async def bad_precision(conn: asyncpg.Connection):
    # PostgreSQL numeric comes back as Decimal, but...
    balance = await conn.fetchval(
        "SELECT balance FROM accounts WHERE id = $1",
        account_id
    )

    # DON'T convert to float!
    new_balance = float(balance) + 0.01  # Precision loss!

    await conn.execute(
        "UPDATE accounts SET balance = $1 WHERE id = $2",
        new_balance,  # Float goes back to PostgreSQL
        account_id
    )


# GOOD - Keep as Decimal
from decimal import Decimal

async def good_precision(conn: asyncpg.Connection):
    balance = await conn.fetchval(
        "SELECT balance FROM accounts WHERE id = $1",
        account_id
    )  # Returns Decimal

    new_balance = balance + Decimal("0.01")  # Exact arithmetic

    await conn.execute(
        "UPDATE accounts SET balance = $1 WHERE id = $2",
        new_balance,  # Decimal preserved
        account_id
    )
```

### Pitfall 5: Forgetting to Close Pool on Shutdown

**Problem**: Not closing pool leaves connections open, can exhaust PostgreSQL limits.

```python
# BAD - No cleanup on shutdown
app = FastAPI()

@app.on_event("startup")
async def startup():
    await DatabasePool.initialize()
# Missing shutdown handler!


# GOOD - Proper cleanup
@asynccontextmanager
async def lifespan(app: FastAPI):
    await DatabasePool.initialize()
    yield
    await DatabasePool.close()  # Critical!

app = FastAPI(lifespan=lifespan)
```

### Pitfall 6: Blocking the Event Loop

**Problem**: Using synchronous database operations.

```python
# BAD - Blocking call
import psycopg2

def bad_blocking(query):
    conn = psycopg2.connect(...)  # Blocks event loop!
    cursor = conn.cursor()
    cursor.execute(query)  # Blocks!
    return cursor.fetchall()


# GOOD - asyncpg is fully async
async def good_async(query):
    async with DatabasePool.acquire() as conn:
        return await conn.fetch(query)  # Non-blocking
```

---

## Part 10: Performance Optimization

### Query Optimization Tips

```python
# Efficient query patterns

# 1. Use LIMIT for pagination
async def paginated_query(conn, page: int, per_page: int = 50):
    offset = (page - 1) * per_page
    return await conn.fetch("""
        SELECT * FROM orders
        ORDER BY created_at DESC
        LIMIT $1 OFFSET $2
    """, per_page, offset)


# 2. Use cursor for large result sets
async def streaming_query(conn: asyncpg.Connection):
    async with conn.transaction():
        # Cursor allows streaming without loading all rows
        async for record in conn.cursor("SELECT * FROM large_table"):
            yield dict(record)


# 3. Use indexes - check EXPLAIN
async def explain_query(conn: asyncpg.Connection, query: str):
    plan = await conn.fetch(f"EXPLAIN ANALYZE {query}")
    for row in plan:
        print(row[0])


# 4. Batch inserts instead of individual inserts
async def batch_vs_individual(conn: asyncpg.Connection, items: List[dict]):
    # SLOW: Individual inserts
    for item in items:
        await conn.execute("INSERT INTO items VALUES ($1, $2)", item['a'], item['b'])

    # FAST: executemany
    await conn.executemany(
        "INSERT INTO items VALUES ($1, $2)",
        [(item['a'], item['b']) for item in items]
    )

    # FASTEST: COPY
    await conn.copy_records_to_table(
        'items',
        records=[(item['a'], item['b']) for item in items],
        columns=['a', 'b']
    )
```

### Connection Pool Tuning

```python
# Pool tuning for different scenarios

# High-throughput API
pool = await asyncpg.create_pool(
    dsn,
    min_size=10,          # Keep 10 connections warm
    max_size=50,          # Scale up to 50 under load
    max_inactive_connection_lifetime=60,  # Recycle frequently
    command_timeout=30,   # Fail fast on slow queries
)

# Background workers
pool = await asyncpg.create_pool(
    dsn,
    min_size=2,           # Low baseline
    max_size=10,          # Limited concurrency
    max_inactive_connection_lifetime=300,  # Longer lifetime OK
    command_timeout=300,  # Long-running queries OK
)

# Trading system
pool = await asyncpg.create_pool(
    dsn,
    min_size=10,          # Keep connections ready
    max_size=30,          # Control max concurrency
    max_inactive_connection_lifetime=30,  # Fresh connections
    command_timeout=10,   # Fast timeout for trading
    max_queries=50000,    # Connection recycling after N queries
)
```

---

## Quick Reference

### Common Operations

```python
# Fetch all rows
rows = await conn.fetch("SELECT * FROM users")

# Fetch one row
row = await conn.fetchrow("SELECT * FROM users WHERE id = $1", 1)

# Fetch single value
count = await conn.fetchval("SELECT COUNT(*) FROM users")

# Execute (no return)
await conn.execute("DELETE FROM users WHERE inactive = true")

# Execute with row count
result = await conn.execute("UPDATE users SET active = true WHERE id = $1", 1)
# result = "UPDATE 1"

# Transaction
async with conn.transaction():
    await conn.execute(...)

# Prepared statement
stmt = await conn.prepare("SELECT * FROM users WHERE id = $1")
row = await stmt.fetchrow(1)

# Batch insert
await conn.executemany(
    "INSERT INTO users (name, email) VALUES ($1, $2)",
    [("Alice", "alice@example.com"), ("Bob", "bob@example.com")]
)

# COPY bulk load
await conn.copy_records_to_table("users", records=records, columns=columns)
```

### Parameter Binding

```python
# Positional parameters ($1, $2, ...)
await conn.fetch("SELECT * FROM users WHERE id = $1 AND status = $2", 1, "active")

# Array parameters
await conn.fetch("SELECT * FROM users WHERE id = ANY($1)", [1, 2, 3])

# JSON parameters
import json
await conn.execute(
    "INSERT INTO events (data) VALUES ($1)",
    json.dumps({"type": "order", "value": 100})
)

# Decimal (important for finance)
from decimal import Decimal
await conn.execute(
    "UPDATE accounts SET balance = $1 WHERE id = $2",
    Decimal("1234.56"),
    account_id
)
```

### Type Mapping

| PostgreSQL Type | Python Type |
|-----------------|-------------|
| integer, bigint | int |
| numeric, decimal | Decimal |
| real, double precision | float |
| text, varchar, char | str |
| boolean | bool |
| timestamp, timestamptz | datetime |
| date | date |
| time, timetz | time |
| uuid | uuid.UUID |
| json, jsonb | dict/list (via codec) |
| bytea | bytes |
| array | list |

---

## References

- [asyncpg Documentation](https://magicstack.github.io/asyncpg/)
- [asyncpg GitHub](https://github.com/MagicStack/asyncpg)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [FastAPI Database Documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/)

---

## Skill Validation Checklist

When applying this skill, verify:

- [ ] Connection pool initialized at startup
- [ ] Connection pool closed at shutdown
- [ ] All database operations use async/await
- [ ] Transactions use context managers
- [ ] Financial calculations use Decimal
- [ ] Health check endpoint available
- [ ] Error handling covers common exceptions
- [ ] No N+1 query patterns
- [ ] Pool size appropriate for workload
- [ ] Queries use parameterized values ($1, $2, ...)
