# database/transactions.py
"""
Transaction patterns for asyncpg.

Covers:
- Basic transactions with context managers
- Savepoints (nested transactions)
- Isolation levels
- Read-only transactions
- Retry logic for serialization conflicts
"""

import asyncpg
import asyncio
from typing import TypeVar, Callable, Optional, Any
from functools import wraps
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


# =============================================================================
# Basic Transaction Patterns
# =============================================================================

async def basic_transaction_example(conn: asyncpg.Connection):
    """
    Basic transaction with automatic commit/rollback.

    The context manager handles:
    - BEGIN on entry
    - COMMIT on successful exit
    - ROLLBACK on exception
    """
    async with conn.transaction():
        # All operations here are in a single transaction
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
        # Transaction commits automatically if no exception raised
    # At this point, transaction is committed


async def transaction_with_return_value(conn: asyncpg.Connection) -> int:
    """
    Transaction that returns a value.

    Return value is captured from inside the transaction context.
    """
    async with conn.transaction():
        order_id = await conn.fetchval("""
            INSERT INTO orders (collective_id, symbol, quantity)
            VALUES ($1, $2, $3)
            RETURNING id
        """, "collective-001", "BTC-USD", Decimal("0.5"))

        await conn.execute("""
            INSERT INTO order_audit (order_id, action)
            VALUES ($1, 'created')
        """, order_id)

        return order_id  # Transaction commits, then returns


# =============================================================================
# Savepoints (Nested Transactions)
# =============================================================================

async def savepoint_for_partial_failure(
    conn: asyncpg.Connection,
    items: list
) -> tuple[int, int]:
    """
    Process items with savepoints - skip failures, continue processing.

    Use case: Batch processing where some items may fail validation
    but we want to commit successful items.

    Returns:
        Tuple of (success_count, failure_count)
    """
    success = 0
    failed = 0

    async with conn.transaction():
        # Main transaction

        for item in items:
            try:
                # Create savepoint for each item
                async with conn.transaction():
                    # This is actually a savepoint, not a new transaction
                    await process_single_item(conn, item)
                    success += 1
                    # Savepoint released (committed to main transaction)

            except Exception as e:
                # Savepoint rolled back, main transaction continues
                logger.warning(f"Item failed, skipping: {e}")
                failed += 1

        # Main transaction commits all successful items

    return success, failed


async def explicit_savepoint_control(conn: asyncpg.Connection):
    """
    Manual savepoint control for complex scenarios.

    Use when you need fine-grained control over savepoint lifecycle.
    """
    tr = conn.transaction()
    await tr.start()

    try:
        await conn.execute("INSERT INTO audit (event) VALUES ('start')")

        # Create named savepoint
        sp1 = await tr.savepoint()

        try:
            # Risky operation
            await conn.execute("INSERT INTO risky_table VALUES ($1)", "dangerous")
        except Exception as e:
            # Rollback to savepoint only, preserve previous work
            await sp1.rollback()
            await conn.execute("INSERT INTO audit (event) VALUES ('risky_failed')")

        await conn.execute("INSERT INTO audit (event) VALUES ('end')")
        await tr.commit()

    except Exception:
        await tr.rollback()
        raise


# =============================================================================
# Isolation Levels
# =============================================================================

async def read_committed_example(conn: asyncpg.Connection):
    """
    Read Committed (PostgreSQL default).

    Each statement sees data committed before the statement began.
    Different statements in same transaction may see different snapshots.
    """
    async with conn.transaction():
        # This might see different data than...
        count1 = await conn.fetchval("SELECT COUNT(*) FROM orders")

        await asyncio.sleep(1)  # Another process inserts rows

        # ...this statement (if other transactions committed)
        count2 = await conn.fetchval("SELECT COUNT(*) FROM orders")
        # count2 may be > count1


async def repeatable_read_example(conn: asyncpg.Connection):
    """
    Repeatable Read isolation.

    Transaction sees a snapshot as of the first query.
    All subsequent reads see the same snapshot.
    """
    async with conn.transaction(isolation='repeatable_read'):
        # Snapshot taken at first query
        balance1 = await conn.fetchval(
            "SELECT balance FROM accounts WHERE id = 1"
        )

        await asyncio.sleep(1)  # Another process updates the balance

        # Same snapshot - will see original balance
        balance2 = await conn.fetchval(
            "SELECT balance FROM accounts WHERE id = 1"
        )

        assert balance1 == balance2  # Guaranteed!


async def serializable_example(conn: asyncpg.Connection):
    """
    Serializable isolation (strictest).

    Transactions behave as if executed serially.
    May raise SerializationError - must be prepared to retry.
    """
    async with conn.transaction(isolation='serializable'):
        # Check current balance
        balance = await conn.fetchval(
            "SELECT balance FROM accounts WHERE id = 1"
        )

        if balance >= 100:
            # Deduct
            await conn.execute(
                "UPDATE accounts SET balance = balance - 100 WHERE id = 1"
            )

        # If another serializable transaction modifies the same row
        # concurrently, one will get SerializationError


async def read_only_transaction(conn: asyncpg.Connection) -> dict:
    """
    Read-only transaction for reporting.

    Benefits:
    - PostgreSQL can optimize (no write locks)
    - Prevents accidental writes
    - Can run on read replicas
    """
    async with conn.transaction(readonly=True):
        # Any write attempt will raise an error
        total = await conn.fetchval("SELECT SUM(amount) FROM transactions")
        count = await conn.fetchval("SELECT COUNT(*) FROM transactions")

        return {"total": total, "count": count}


# =============================================================================
# Retry Logic for Serialization Conflicts
# =============================================================================

def with_serializable_retry(
    max_retries: int = 3,
    backoff_base: float = 0.1,
    backoff_max: float = 2.0,
):
    """
    Decorator for functions that use serializable transactions.

    Automatically retries on SerializationError with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        backoff_base: Initial backoff delay in seconds
        backoff_max: Maximum backoff delay
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)

                except asyncpg.SerializationError as e:
                    last_error = e

                    if attempt < max_retries - 1:
                        delay = min(
                            backoff_base * (2 ** attempt),
                            backoff_max
                        )
                        logger.warning(
                            f"{func.__name__} serialization conflict "
                            f"(attempt {attempt + 1}/{max_retries}), "
                            f"retrying in {delay:.2f}s"
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            f"{func.__name__} failed after {max_retries} attempts"
                        )

            raise last_error

        return wrapper
    return decorator


@with_serializable_retry(max_retries=3)
async def transfer_funds(
    conn: asyncpg.Connection,
    from_id: str,
    to_id: str,
    amount: Decimal
) -> bool:
    """
    Transfer funds between accounts with serializable isolation.

    Uses retry decorator for automatic conflict handling.
    """
    async with conn.transaction(isolation='serializable'):
        # Check source balance
        source_balance = await conn.fetchval(
            "SELECT balance FROM accounts WHERE id = $1 FOR UPDATE",
            from_id
        )

        if source_balance is None:
            raise ValueError(f"Source account {from_id} not found")

        if source_balance < amount:
            raise ValueError(f"Insufficient balance: {source_balance} < {amount}")

        # Perform transfer
        await conn.execute(
            "UPDATE accounts SET balance = balance - $1 WHERE id = $2",
            amount, from_id
        )
        await conn.execute(
            "UPDATE accounts SET balance = balance + $1 WHERE id = $2",
            amount, to_id
        )

        return True


# =============================================================================
# Transaction with Deadlock Handling
# =============================================================================

async def with_deadlock_retry(
    coro_func: Callable,
    *args,
    max_retries: int = 3,
    **kwargs
) -> Any:
    """
    Execute coroutine with deadlock retry.

    Deadlocks can occur when multiple transactions try to lock
    the same rows in different orders. PostgreSQL detects and
    aborts one transaction.

    Args:
        coro_func: Async function to execute
        *args: Positional arguments for function
        max_retries: Maximum retry attempts
        **kwargs: Keyword arguments for function

    Returns:
        Result of successful execution
    """
    for attempt in range(max_retries):
        try:
            return await coro_func(*args, **kwargs)

        except asyncpg.DeadlockDetectedError as e:
            if attempt < max_retries - 1:
                # Random backoff to prevent immediate re-deadlock
                import random
                delay = random.uniform(0.1, 0.5) * (attempt + 1)
                logger.warning(
                    f"Deadlock detected (attempt {attempt + 1}), "
                    f"retrying in {delay:.2f}s"
                )
                await asyncio.sleep(delay)
            else:
                logger.error(f"Deadlock persisted after {max_retries} attempts")
                raise


# =============================================================================
# Utility: Process helper (not exported)
# =============================================================================

async def process_single_item(conn: asyncpg.Connection, item: dict):
    """Helper for savepoint example."""
    await conn.execute(
        "INSERT INTO processed_items (id, data) VALUES ($1, $2)",
        item.get('id'),
        item.get('data')
    )
