"""
Database Session Management

Async SQLAlchemy session factory and dependency injection for FastAPI.
Uses environment variable DATABASE_URL for connection configuration.
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from .models import Base


# Global engine and session factory
_engine: Optional[AsyncEngine] = None
_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


def get_database_url() -> str:
    """
    Get database URL from environment.
    
    Returns:
        PostgreSQL connection URL (async driver format)
        
    Raises:
        ValueError: If DATABASE_URL is not set
        
    Example URLs:
        - postgresql+asyncpg://user:pass@localhost:5432/trading_arena
        - postgresql+asyncpg://user:pass@localhost:5432/trading_arena_test
    """
    url = os.environ.get("DATABASE_URL")
    
    if not url:
        raise ValueError(
            "DATABASE_URL environment variable is required. "
            "Example: postgresql+asyncpg://user:pass@localhost:5432/trading_arena"
        )
    
    # Convert postgres:// to postgresql+asyncpg:// if needed
    # (some cloud providers use postgres:// which SQLAlchemy doesn't accept)
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgresql://") and "+asyncpg" not in url:
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    return url


def create_engine(
    database_url: Optional[str] = None,
    echo: bool = False,
    pool_size: int = 5,
    max_overflow: int = 10,
    pool_pre_ping: bool = True,
    use_null_pool: bool = False,
) -> AsyncEngine:
    """
    Create async SQLAlchemy engine.
    
    Args:
        database_url: PostgreSQL connection URL (uses env var if not provided)
        echo: Enable SQL statement logging
        pool_size: Connection pool size
        max_overflow: Max connections beyond pool_size
        pool_pre_ping: Test connections before use
        use_null_pool: Disable pooling (useful for testing)
        
    Returns:
        Configured AsyncEngine instance
    """
    url = database_url or get_database_url()
    
    # Pool configuration
    pool_kwargs = {}
    if use_null_pool:
        # NullPool is useful for testing - creates fresh connection each time
        pool_kwargs["poolclass"] = NullPool
    else:
        pool_kwargs.update({
            "pool_size": pool_size,
            "max_overflow": max_overflow,
            "pool_pre_ping": pool_pre_ping,
        })
    
    engine = create_async_engine(
        url,
        echo=echo,
        **pool_kwargs,
    )
    
    return engine


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """
    Create async session factory.
    
    Args:
        engine: SQLAlchemy AsyncEngine
        
    Returns:
        Configured async_sessionmaker
    """
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,  # Prevent lazy loading issues after commit
        autocommit=False,
        autoflush=False,
    )


async def init_db(
    database_url: Optional[str] = None,
    create_tables: bool = False,
    echo: bool = False,
) -> None:
    """
    Initialize database connection.
    
    Should be called during application startup.
    
    Args:
        database_url: PostgreSQL connection URL (uses env var if not provided)
        create_tables: Whether to create all tables (dev/test only)
        echo: Enable SQL logging
    """
    global _engine, _session_factory
    
    _engine = create_engine(database_url=database_url, echo=echo)
    _session_factory = create_session_factory(_engine)
    
    if create_tables:
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    Close database connections.
    
    Should be called during application shutdown.
    """
    global _engine, _session_factory
    
    if _engine:
        await _engine.dispose()
        _engine = None
        _session_factory = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database sessions.
    
    Yields a database session and handles cleanup.
    
    Usage:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    if _session_factory is None:
        raise RuntimeError(
            "Database not initialized. Call init_db() during application startup."
        )
    
    async with _session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def DatabaseSession() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database sessions outside of FastAPI.
    
    Useful for background tasks, scripts, and testing.
    
    Usage:
        async with DatabaseSession() as db:
            result = await db.execute(select(Item))
            items = result.scalars().all()
    """
    if _session_factory is None:
        raise RuntimeError(
            "Database not initialized. Call init_db() during application startup."
        )
    
    async with _session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


class DatabaseManager:
    """
    Database manager for standalone usage.
    
    Useful for scripts, migrations, and testing where you need
    explicit control over the database lifecycle.
    
    Usage:
        async with DatabaseManager(database_url) as db_manager:
            async with db_manager.session() as session:
                # Use session
                pass
    """
    
    def __init__(
        self,
        database_url: Optional[str] = None,
        echo: bool = False,
        use_null_pool: bool = False,
    ):
        self.database_url = database_url
        self.echo = echo
        self.use_null_pool = use_null_pool
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker[AsyncSession]] = None
    
    async def __aenter__(self) -> "DatabaseManager":
        self._engine = create_engine(
            database_url=self.database_url,
            echo=self.echo,
            use_null_pool=self.use_null_pool,
        )
        self._session_factory = create_session_factory(self._engine)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._engine:
            await self._engine.dispose()
    
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session."""
        if self._session_factory is None:
            raise RuntimeError("DatabaseManager not initialized")
        
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
    
    async def create_tables(self) -> None:
        """Create all database tables."""
        if self._engine is None:
            raise RuntimeError("DatabaseManager not initialized")
        
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def drop_tables(self) -> None:
        """Drop all database tables (use with caution!)."""
        if self._engine is None:
            raise RuntimeError("DatabaseManager not initialized")
        
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
