# database/pool.py
"""
Production-ready connection pool for asyncpg.

This is the foundation for all database operations in async applications.
Use DatabasePool as a singleton - initialize once at startup, close at shutdown.

Usage:
    # Startup
    await DatabasePool.initialize(dsn="postgresql://...")

    # During requests
    async with DatabasePool.acquire() as conn:
        await conn.fetch(...)

    # Shutdown
    await DatabasePool.close()
"""

import asyncpg
from typing import Optional, Dict, Any
import logging
import os

logger = logging.getLogger(__name__)


class DatabasePool:
    """
    Singleton connection pool manager.

    Features:
    - Automatic connection lifecycle management
    - Health checking with statistics
    - Configuration from environment or explicit params
    - Thread-safe pool access
    """

    _pool: Optional[asyncpg.Pool] = None
    _config: Dict[str, Any] = {}

    @classmethod
    async def initialize(
        cls,
        dsn: Optional[str] = None,
        *,
        host: Optional[str] = None,
        port: Optional[int] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        min_size: int = 5,
        max_size: int = 20,
        max_inactive_connection_lifetime: float = 300.0,
        command_timeout: float = 60.0,
        max_queries: int = 50000,
        setup: Optional[callable] = None,
    ) -> asyncpg.Pool:
        """
        Initialize the connection pool.

        Args:
            dsn: PostgreSQL connection string (overrides individual params)
                 If not provided, builds from other params or environment
            host: Database host (default: DB_HOST env or 'localhost')
            port: Database port (default: DB_PORT env or 5432)
            user: Database user (default: DB_USER env)
            password: Database password (default: DB_PASSWORD env)
            database: Database name (default: DB_NAME env)
            min_size: Minimum pool connections (keep warm)
            max_size: Maximum pool connections (limit)
            max_inactive_connection_lifetime: Close idle connections after N seconds
            command_timeout: Default query timeout in seconds
            max_queries: Recycle connection after N queries (prevent memory leaks)
            setup: Async function called for each new connection (e.g., SET search_path)

        Returns:
            Initialized connection pool

        Environment Variables:
            DATABASE_URL: Full DSN (highest priority)
            DB_HOST: Database host
            DB_PORT: Database port
            DB_USER: Database user
            DB_PASSWORD: Database password
            DB_NAME: Database name
        """
        if cls._pool is not None:
            logger.warning("Pool already initialized, returning existing pool")
            return cls._pool

        # Build DSN from environment or params
        if dsn is None:
            dsn = os.environ.get('DATABASE_URL')

        if dsn is None:
            # Build from components
            _host = host or os.environ.get('DB_HOST', 'localhost')
            _port = port or int(os.environ.get('DB_PORT', '5432'))
            _user = user or os.environ.get('DB_USER', 'postgres')
            _password = password or os.environ.get('DB_PASSWORD', '')
            _database = database or os.environ.get('DB_NAME', 'postgres')

            dsn = f"postgresql://{_user}:{_password}@{_host}:{_port}/{_database}"

        # Store config for health checks
        cls._config = {
            'min_size': min_size,
            'max_size': max_size,
            'max_inactive_connection_lifetime': max_inactive_connection_lifetime,
            'command_timeout': command_timeout,
        }

        # Create pool
        cls._pool = await asyncpg.create_pool(
            dsn,
            min_size=min_size,
            max_size=max_size,
            max_inactive_connection_lifetime=max_inactive_connection_lifetime,
            command_timeout=command_timeout,
            max_queries=max_queries,
            setup=setup,
        )

        logger.info(
            f"Database pool initialized: min={min_size}, max={max_size}, "
            f"timeout={command_timeout}s"
        )

        return cls._pool

    @classmethod
    async def close(cls):
        """
        Close the connection pool gracefully.

        Should be called at application shutdown.
        """
        if cls._pool is not None:
            await cls._pool.close()
            cls._pool = None
            cls._config = {}
            logger.info("Database pool closed")

    @classmethod
    def acquire(cls):
        """
        Acquire a connection from the pool.

        Usage:
            async with DatabasePool.acquire() as conn:
                await conn.fetch(...)

        The connection is automatically returned to pool when context exits.

        Raises:
            RuntimeError: If pool not initialized
        """
        if cls._pool is None:
            raise RuntimeError(
                "Database pool not initialized. Call DatabasePool.initialize() first."
            )
        return cls._pool.acquire()

    @classmethod
    def get_pool(cls) -> asyncpg.Pool:
        """
        Get the raw pool instance.

        For advanced operations like executemany with custom timeout.

        Raises:
            RuntimeError: If pool not initialized
        """
        if cls._pool is None:
            raise RuntimeError(
                "Database pool not initialized. Call DatabasePool.initialize() first."
            )
        return cls._pool

    @classmethod
    async def health_check(cls) -> Dict[str, Any]:
        """
        Check pool health and connection status.

        Returns:
            Dict with pool statistics and health status:
            - status: "healthy", "unhealthy", or "not_initialized"
            - healthy: Boolean
            - pool_size: Current pool size
            - pool_free: Idle connections
            - pool_used: Active connections
            - pool_min: Configured minimum
            - pool_max: Configured maximum
            - error: Error message if unhealthy
        """
        if cls._pool is None:
            return {
                "status": "not_initialized",
                "healthy": False,
                "error": "Pool not initialized"
            }

        try:
            # Test actual database connectivity
            async with cls.acquire() as conn:
                await conn.fetchval("SELECT 1")

            pool = cls._pool
            return {
                "status": "healthy",
                "healthy": True,
                "pool_size": pool.get_size(),
                "pool_free": pool.get_idle_size(),
                "pool_used": pool.get_size() - pool.get_idle_size(),
                "pool_min": pool.get_min_size(),
                "pool_max": pool.get_max_size(),
            }

        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "healthy": False,
                "error": str(e),
            }

    @classmethod
    async def execute(cls, query: str, *args, timeout: float = None):
        """
        Execute a query without returning rows.

        Convenience method for simple operations.

        Args:
            query: SQL query with $1, $2, ... placeholders
            *args: Query parameters
            timeout: Override default timeout

        Returns:
            Status string like "UPDATE 1"
        """
        async with cls.acquire() as conn:
            return await conn.execute(query, *args, timeout=timeout)

    @classmethod
    async def fetch(cls, query: str, *args, timeout: float = None):
        """
        Execute a query and return all rows.

        Convenience method for simple operations.

        Args:
            query: SQL query with $1, $2, ... placeholders
            *args: Query parameters
            timeout: Override default timeout

        Returns:
            List of asyncpg.Record objects
        """
        async with cls.acquire() as conn:
            return await conn.fetch(query, *args, timeout=timeout)

    @classmethod
    async def fetchrow(cls, query: str, *args, timeout: float = None):
        """
        Execute a query and return first row.

        Convenience method for simple operations.

        Args:
            query: SQL query with $1, $2, ... placeholders
            *args: Query parameters
            timeout: Override default timeout

        Returns:
            asyncpg.Record or None
        """
        async with cls.acquire() as conn:
            return await conn.fetchrow(query, *args, timeout=timeout)

    @classmethod
    async def fetchval(cls, query: str, *args, column: int = 0, timeout: float = None):
        """
        Execute a query and return a single value.

        Convenience method for simple operations.

        Args:
            query: SQL query with $1, $2, ... placeholders
            *args: Query parameters
            column: Column index to return (default: 0)
            timeout: Override default timeout

        Returns:
            Single value from first row
        """
        async with cls.acquire() as conn:
            return await conn.fetchval(query, *args, column=column, timeout=timeout)


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


async def db_health():
    """Get database health status."""
    return await DatabasePool.health_check()
