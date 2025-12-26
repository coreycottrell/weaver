# database/error_handling.py
"""
Error handling patterns for asyncpg.

Covers:
- Exception hierarchy understanding
- Specific error handling (unique violation, FK, etc.)
- Retry decorators
- Connection recovery
- Logging and monitoring
"""

import asyncpg
import asyncio
from typing import TypeVar, Callable, Any, Tuple, Optional
from functools import wraps
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

T = TypeVar('T')


# =============================================================================
# asyncpg Exception Reference
# =============================================================================

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

Non-PostgreSQL asyncpg errors:
├── asyncpg.InterfaceError (connection issues)
├── asyncpg.ConnectionDoesNotExistError
├── asyncpg.TooManyConnectionsError
└── asyncio.TimeoutError (connection/query timeout)
"""


# =============================================================================
# Error Classification
# =============================================================================

class DatabaseErrorType:
    """Classification of database errors for handling decisions."""

    TRANSIENT = "transient"       # Retry may succeed
    CONSTRAINT = "constraint"     # Business logic error
    CONNECTION = "connection"     # Connection issue
    SYNTAX = "syntax"             # Programming error
    INTERNAL = "internal"         # Server error


def classify_error(error: Exception) -> Tuple[str, bool]:
    """
    Classify a database error.

    Returns:
        Tuple of (error_type, is_retryable)
    """
    if isinstance(error, asyncpg.SerializationError):
        return DatabaseErrorType.TRANSIENT, True

    if isinstance(error, asyncpg.DeadlockDetectedError):
        return DatabaseErrorType.TRANSIENT, True

    if isinstance(error, asyncpg.UniqueViolationError):
        return DatabaseErrorType.CONSTRAINT, False

    if isinstance(error, asyncpg.ForeignKeyViolationError):
        return DatabaseErrorType.CONSTRAINT, False

    if isinstance(error, asyncpg.CheckViolationError):
        return DatabaseErrorType.CONSTRAINT, False

    if isinstance(error, asyncpg.NotNullViolationError):
        return DatabaseErrorType.CONSTRAINT, False

    if isinstance(error, (
        asyncpg.ConnectionDoesNotExistError,
        asyncpg.InterfaceError,
        asyncio.TimeoutError
    )):
        return DatabaseErrorType.CONNECTION, True

    if isinstance(error, asyncpg.PostgresSyntaxError):
        return DatabaseErrorType.SYNTAX, False

    if isinstance(error, asyncpg.QueryCanceledError):
        return DatabaseErrorType.TRANSIENT, True

    if isinstance(error, asyncpg.InternalServerError):
        return DatabaseErrorType.INTERNAL, False

    return DatabaseErrorType.INTERNAL, False


# =============================================================================
# Specific Error Handlers
# =============================================================================

async def handle_unique_violation(
    conn: asyncpg.Connection,
    email: str,
    name: str
) -> dict:
    """
    Example: Handle unique constraint violation gracefully.

    Returns existing record if duplicate, creates new otherwise.
    """
    try:
        row = await conn.fetchrow("""
            INSERT INTO users (email, name)
            VALUES ($1, $2)
            RETURNING id, email, name
        """, email, name)
        return {"created": True, "user": dict(row)}

    except asyncpg.UniqueViolationError as e:
        # Log the duplicate attempt
        logger.info(f"Duplicate user attempted: {email}")

        # Fetch existing record
        row = await conn.fetchrow(
            "SELECT id, email, name FROM users WHERE email = $1",
            email
        )
        return {"created": False, "user": dict(row)}


async def handle_foreign_key_violation(
    conn: asyncpg.Connection,
    order_data: dict
) -> dict:
    """
    Example: Handle foreign key violation with helpful error.
    """
    try:
        row = await conn.fetchrow("""
            INSERT INTO orders (collective_id, symbol, quantity)
            VALUES ($1, $2, $3)
            RETURNING id
        """, order_data['collective_id'], order_data['symbol'], order_data['quantity'])
        return {"success": True, "order_id": row['id']}

    except asyncpg.ForeignKeyViolationError as e:
        # Parse which constraint failed from error detail
        logger.warning(f"Foreign key violation: {e.detail}")

        # Check which reference is missing
        collective_exists = await conn.fetchval(
            "SELECT EXISTS(SELECT 1 FROM collectives WHERE id = $1)",
            order_data['collective_id']
        )

        if not collective_exists:
            return {
                "success": False,
                "error": f"Collective '{order_data['collective_id']}' not found"
            }

        return {"success": False, "error": "Invalid reference"}


async def handle_check_violation(
    conn: asyncpg.Connection,
    account_id: str,
    amount: Decimal
) -> dict:
    """
    Example: Handle check constraint (e.g., balance >= 0).
    """
    try:
        await conn.execute("""
            UPDATE accounts
            SET balance = balance - $1
            WHERE id = $2
        """, amount, account_id)
        return {"success": True}

    except asyncpg.CheckViolationError as e:
        # Check constraint failed (e.g., balance < 0)
        logger.warning(f"Check violation for account {account_id}: {e.detail}")

        current_balance = await conn.fetchval(
            "SELECT balance FROM accounts WHERE id = $1",
            account_id
        )

        return {
            "success": False,
            "error": "Insufficient balance",
            "current_balance": current_balance,
            "requested": amount
        }


# =============================================================================
# Retry Decorators
# =============================================================================

def with_retry(
    max_retries: int = 3,
    retry_on: tuple = (
        asyncpg.SerializationError,
        asyncpg.DeadlockDetectedError,
        asyncpg.ConnectionDoesNotExistError,
        asyncio.TimeoutError,
    ),
    backoff_base: float = 0.1,
    backoff_max: float = 5.0,
    backoff_jitter: bool = True,
):
    """
    Decorator for database operations that should retry on transient errors.

    Args:
        max_retries: Maximum retry attempts
        retry_on: Exception types to retry on
        backoff_base: Initial backoff delay in seconds
        backoff_max: Maximum backoff delay
        backoff_jitter: Add randomness to backoff (prevents thundering herd)
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_error = None

            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)

                except retry_on as e:
                    last_error = e
                    error_type, _ = classify_error(e)

                    if attempt < max_retries - 1:
                        # Calculate backoff with optional jitter
                        delay = min(backoff_base * (2 ** attempt), backoff_max)
                        if backoff_jitter:
                            import random
                            delay *= (0.5 + random.random())

                        logger.warning(
                            f"{func.__name__} failed ({error_type}), "
                            f"attempt {attempt + 1}/{max_retries}, "
                            f"retrying in {delay:.2f}s: {type(e).__name__}"
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            f"{func.__name__} failed after {max_retries} attempts: "
                            f"{type(e).__name__}: {e}"
                        )

            raise last_error

        return wrapper
    return decorator


# =============================================================================
# Connection Recovery
# =============================================================================

class ResilientConnection:
    """
    Connection wrapper with automatic recovery.

    Handles connection drops gracefully.
    """

    def __init__(
        self,
        pool: asyncpg.Pool,
        max_recovery_attempts: int = 3,
        recovery_delay: float = 1.0
    ):
        self.pool = pool
        self.max_recovery_attempts = max_recovery_attempts
        self.recovery_delay = recovery_delay
        self._conn: Optional[asyncpg.Connection] = None

    async def __aenter__(self):
        self._conn = await self.pool.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            await self.pool.release(self._conn)
            self._conn = None

    async def execute_with_recovery(
        self,
        query: str,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute query with automatic connection recovery.
        """
        for attempt in range(self.max_recovery_attempts):
            try:
                if self._conn is None:
                    self._conn = await self.pool.acquire()
                return await self._conn.fetch(query, *args, **kwargs)

            except (
                asyncpg.ConnectionDoesNotExistError,
                asyncpg.InterfaceError
            ) as e:
                logger.warning(
                    f"Connection error (attempt {attempt + 1}): {e}"
                )

                # Release bad connection and get new one
                if self._conn:
                    try:
                        await self.pool.release(self._conn)
                    except:
                        pass
                    self._conn = None

                if attempt < self.max_recovery_attempts - 1:
                    await asyncio.sleep(self.recovery_delay)
                else:
                    raise


# =============================================================================
# Safe Wrapper
# =============================================================================

async def safe_db_operation(
    conn: asyncpg.Connection,
    operation: Callable,
    *args,
    on_unique_violation: Optional[Callable] = None,
    on_fk_violation: Optional[Callable] = None,
    on_check_violation: Optional[Callable] = None,
    **kwargs
) -> Tuple[bool, Any]:
    """
    Execute database operation with comprehensive error handling.

    Args:
        conn: Database connection
        operation: Async function to execute
        on_unique_violation: Handler for unique constraint violations
        on_fk_violation: Handler for foreign key violations
        on_check_violation: Handler for check constraint violations

    Returns:
        Tuple of (success, result_or_error)
    """
    try:
        result = await operation(conn, *args, **kwargs)
        return True, result

    except asyncpg.UniqueViolationError as e:
        if on_unique_violation:
            return True, await on_unique_violation(e)
        logger.warning(f"Unique violation: {e.detail}")
        return False, {"error": "duplicate", "detail": e.detail}

    except asyncpg.ForeignKeyViolationError as e:
        if on_fk_violation:
            return True, await on_fk_violation(e)
        logger.warning(f"Foreign key violation: {e.detail}")
        return False, {"error": "invalid_reference", "detail": e.detail}

    except asyncpg.CheckViolationError as e:
        if on_check_violation:
            return True, await on_check_violation(e)
        logger.warning(f"Check violation: {e.detail}")
        return False, {"error": "validation_failed", "detail": e.detail}

    except asyncpg.NotNullViolationError as e:
        logger.warning(f"Not null violation: {e.column_name}")
        return False, {"error": "required_field", "field": e.column_name}

    except asyncpg.QueryCanceledError:
        logger.error("Query timeout")
        return False, {"error": "timeout"}

    except asyncpg.PostgresError as e:
        logger.error(f"Database error: {type(e).__name__}: {e}")
        return False, {"error": "database_error", "message": str(e)}


# =============================================================================
# Usage Example
# =============================================================================

@with_retry(max_retries=3)
async def transfer_funds_with_retry(
    conn: asyncpg.Connection,
    from_account: str,
    to_account: str,
    amount: Decimal
) -> bool:
    """
    Transfer funds with automatic retry on conflicts.
    """
    async with conn.transaction(isolation='serializable'):
        # Check balance
        balance = await conn.fetchval(
            "SELECT balance FROM accounts WHERE id = $1 FOR UPDATE",
            from_account
        )

        if balance is None:
            raise ValueError(f"Account {from_account} not found")

        if balance < amount:
            raise ValueError(f"Insufficient balance: {balance} < {amount}")

        # Deduct from source
        await conn.execute(
            "UPDATE accounts SET balance = balance - $1 WHERE id = $2",
            amount, from_account
        )

        # Add to destination
        await conn.execute(
            "UPDATE accounts SET balance = balance + $1 WHERE id = $2",
            amount, to_account
        )

        return True
