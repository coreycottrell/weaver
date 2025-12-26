#!/usr/bin/env python3
"""
asyncpg Skill Validation Script

Validates that asyncpg patterns are correctly implemented.
Run this after setting up a PostgreSQL database.

Usage:
    # Set DATABASE_URL or use defaults
    export DATABASE_URL="postgresql://user:pass@localhost:5432/dbname"
    python validate_asyncpg.py

    # Or run specific tests
    python validate_asyncpg.py --test connection
    python validate_asyncpg.py --test pool
    python validate_asyncpg.py --test transactions
"""

import asyncio
import asyncpg
import os
import sys
from decimal import Decimal
from datetime import datetime
from typing import Optional
import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Test configuration
DEFAULT_DSN = "postgresql://postgres:postgres@localhost:5432/test_asyncpg"


class AsyncpgValidator:
    """Validates asyncpg patterns work correctly."""

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None
        self.passed = 0
        self.failed = 0
        self.errors = []

    async def setup(self):
        """Initialize connection pool and test tables."""
        logger.info("Setting up test environment...")

        try:
            self.pool = await asyncpg.create_pool(
                self.dsn,
                min_size=2,
                max_size=10,
                command_timeout=30,
            )
            logger.info(f"Pool created: min=2, max=10")

            # Create test tables
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    DROP TABLE IF EXISTS test_orders CASCADE;
                    DROP TABLE IF EXISTS test_accounts CASCADE;
                    DROP TABLE IF EXISTS test_audit CASCADE;

                    CREATE TABLE test_accounts (
                        id TEXT PRIMARY KEY,
                        balance NUMERIC(20, 8) NOT NULL DEFAULT 0,
                        CHECK (balance >= 0)
                    );

                    CREATE TABLE test_orders (
                        id SERIAL PRIMARY KEY,
                        account_id TEXT REFERENCES test_accounts(id),
                        symbol TEXT NOT NULL,
                        quantity NUMERIC(20, 8) NOT NULL,
                        price NUMERIC(20, 8) NOT NULL,
                        status TEXT DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT NOW()
                    );

                    CREATE TABLE test_audit (
                        id SERIAL PRIMARY KEY,
                        event TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT NOW()
                    );

                    INSERT INTO test_accounts (id, balance) VALUES
                        ('account-1', 10000.00),
                        ('account-2', 5000.00);
                """)
                logger.info("Test tables created")

            return True

        except Exception as e:
            logger.error(f"Setup failed: {e}")
            return False

    async def teardown(self):
        """Clean up test environment."""
        if self.pool:
            async with self.pool.acquire() as conn:
                await conn.execute("DROP TABLE IF EXISTS test_orders CASCADE")
                await conn.execute("DROP TABLE IF EXISTS test_accounts CASCADE")
                await conn.execute("DROP TABLE IF EXISTS test_audit CASCADE")

            await self.pool.close()
            logger.info("Cleanup complete")

    def record_result(self, test_name: str, passed: bool, error: str = None):
        """Record test result."""
        if passed:
            self.passed += 1
            logger.info(f"PASS: {test_name}")
        else:
            self.failed += 1
            self.errors.append((test_name, error))
            logger.error(f"FAIL: {test_name} - {error}")

    # =========================================================================
    # Connection Tests
    # =========================================================================

    async def test_basic_connection(self):
        """Test basic connection works."""
        try:
            conn = await asyncpg.connect(self.dsn)
            result = await conn.fetchval("SELECT 1")
            await conn.close()
            self.record_result("basic_connection", result == 1)
        except Exception as e:
            self.record_result("basic_connection", False, str(e))

    async def test_pool_acquire(self):
        """Test pool connection acquisition."""
        try:
            async with self.pool.acquire() as conn:
                result = await conn.fetchval("SELECT 1")
            self.record_result("pool_acquire", result == 1)
        except Exception as e:
            self.record_result("pool_acquire", False, str(e))

    async def test_pool_stats(self):
        """Test pool statistics."""
        try:
            size = self.pool.get_size()
            idle = self.pool.get_idle_size()
            min_size = self.pool.get_min_size()
            max_size = self.pool.get_max_size()

            valid = (
                size >= min_size and
                size <= max_size and
                idle <= size
            )
            self.record_result("pool_stats", valid)
        except Exception as e:
            self.record_result("pool_stats", False, str(e))

    # =========================================================================
    # Query Tests
    # =========================================================================

    async def test_fetch(self):
        """Test fetch (multiple rows)."""
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch("SELECT * FROM test_accounts")
            self.record_result("fetch", len(rows) == 2)
        except Exception as e:
            self.record_result("fetch", False, str(e))

    async def test_fetchrow(self):
        """Test fetchrow (single row)."""
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT * FROM test_accounts WHERE id = $1",
                    "account-1"
                )
            self.record_result("fetchrow", row['id'] == "account-1")
        except Exception as e:
            self.record_result("fetchrow", False, str(e))

    async def test_fetchval(self):
        """Test fetchval (single value)."""
        try:
            async with self.pool.acquire() as conn:
                balance = await conn.fetchval(
                    "SELECT balance FROM test_accounts WHERE id = $1",
                    "account-1"
                )
            self.record_result("fetchval", balance == Decimal("10000.00"))
        except Exception as e:
            self.record_result("fetchval", False, str(e))

    async def test_execute(self):
        """Test execute (no return)."""
        try:
            async with self.pool.acquire() as conn:
                result = await conn.execute(
                    "UPDATE test_accounts SET balance = balance WHERE id = $1",
                    "account-1"
                )
            self.record_result("execute", result == "UPDATE 1")
        except Exception as e:
            self.record_result("execute", False, str(e))

    async def test_decimal_precision(self):
        """Test Decimal precision is preserved."""
        try:
            async with self.pool.acquire() as conn:
                # Insert precise decimal
                await conn.execute(
                    "UPDATE test_accounts SET balance = $1 WHERE id = $2",
                    Decimal("12345.67891234"),
                    "account-1"
                )

                # Read back
                balance = await conn.fetchval(
                    "SELECT balance FROM test_accounts WHERE id = $1",
                    "account-1"
                )

                # Restore original
                await conn.execute(
                    "UPDATE test_accounts SET balance = 10000 WHERE id = $1",
                    "account-1"
                )

            self.record_result(
                "decimal_precision",
                balance == Decimal("12345.67891234")
            )
        except Exception as e:
            self.record_result("decimal_precision", False, str(e))

    # =========================================================================
    # Transaction Tests
    # =========================================================================

    async def test_basic_transaction(self):
        """Test basic transaction commit."""
        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(
                        "INSERT INTO test_audit (event) VALUES ($1)",
                        "test_basic_transaction"
                    )

                # Should be committed
                count = await conn.fetchval(
                    "SELECT COUNT(*) FROM test_audit WHERE event = $1",
                    "test_basic_transaction"
                )

            self.record_result("basic_transaction", count == 1)
        except Exception as e:
            self.record_result("basic_transaction", False, str(e))

    async def test_transaction_rollback(self):
        """Test transaction rollback on exception."""
        try:
            async with self.pool.acquire() as conn:
                try:
                    async with conn.transaction():
                        await conn.execute(
                            "INSERT INTO test_audit (event) VALUES ($1)",
                            "should_rollback"
                        )
                        raise ValueError("Force rollback")
                except ValueError:
                    pass

                # Should be rolled back
                count = await conn.fetchval(
                    "SELECT COUNT(*) FROM test_audit WHERE event = $1",
                    "should_rollback"
                )

            self.record_result("transaction_rollback", count == 0)
        except Exception as e:
            self.record_result("transaction_rollback", False, str(e))

    async def test_savepoint(self):
        """Test savepoint (nested transaction)."""
        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(
                        "INSERT INTO test_audit (event) VALUES ($1)",
                        "outer_event"
                    )

                    try:
                        async with conn.transaction():
                            await conn.execute(
                                "INSERT INTO test_audit (event) VALUES ($1)",
                                "inner_event"
                            )
                            raise ValueError("Force inner rollback")
                    except ValueError:
                        pass

                    await conn.execute(
                        "INSERT INTO test_audit (event) VALUES ($1)",
                        "after_inner"
                    )

                # outer_event and after_inner should exist, inner_event should not
                outer = await conn.fetchval(
                    "SELECT COUNT(*) FROM test_audit WHERE event = $1",
                    "outer_event"
                )
                inner = await conn.fetchval(
                    "SELECT COUNT(*) FROM test_audit WHERE event = $1",
                    "inner_event"
                )
                after = await conn.fetchval(
                    "SELECT COUNT(*) FROM test_audit WHERE event = $1",
                    "after_inner"
                )

            self.record_result(
                "savepoint",
                outer == 1 and inner == 0 and after == 1
            )
        except Exception as e:
            self.record_result("savepoint", False, str(e))

    async def test_read_only_transaction(self):
        """Test read-only transaction prevents writes."""
        try:
            async with self.pool.acquire() as conn:
                try:
                    async with conn.transaction(readonly=True):
                        await conn.execute(
                            "INSERT INTO test_audit (event) VALUES ($1)",
                            "readonly_test"
                        )
                    # Should have raised an error
                    self.record_result("read_only_transaction", False, "Write succeeded in readonly")
                except asyncpg.ReadOnlySQLTransactionError:
                    self.record_result("read_only_transaction", True)
        except Exception as e:
            self.record_result("read_only_transaction", False, str(e))

    # =========================================================================
    # Batch Operation Tests
    # =========================================================================

    async def test_executemany(self):
        """Test executemany batch insert."""
        try:
            orders = [
                ("account-1", "BTC-USD", Decimal("0.5"), Decimal("45000")),
                ("account-1", "ETH-USD", Decimal("2.0"), Decimal("3000")),
                ("account-2", "BTC-USD", Decimal("0.1"), Decimal("45100")),
            ]

            async with self.pool.acquire() as conn:
                await conn.executemany("""
                    INSERT INTO test_orders (account_id, symbol, quantity, price)
                    VALUES ($1, $2, $3, $4)
                """, orders)

                count = await conn.fetchval("SELECT COUNT(*) FROM test_orders")

            self.record_result("executemany", count == 3)
        except Exception as e:
            self.record_result("executemany", False, str(e))

    async def test_copy_records(self):
        """Test COPY protocol for bulk insert."""
        try:
            records = [
                ("account-1", "COPY-1", Decimal("1.0"), Decimal("100")),
                ("account-2", "COPY-2", Decimal("2.0"), Decimal("200")),
            ]

            async with self.pool.acquire() as conn:
                before = await conn.fetchval("SELECT COUNT(*) FROM test_orders")

                await conn.copy_records_to_table(
                    "test_orders",
                    records=records,
                    columns=["account_id", "symbol", "quantity", "price"]
                )

                after = await conn.fetchval("SELECT COUNT(*) FROM test_orders")

            self.record_result("copy_records", after - before == 2)
        except Exception as e:
            self.record_result("copy_records", False, str(e))

    # =========================================================================
    # Error Handling Tests
    # =========================================================================

    async def test_unique_violation(self):
        """Test unique constraint violation."""
        try:
            async with self.pool.acquire() as conn:
                try:
                    await conn.execute(
                        "INSERT INTO test_accounts (id, balance) VALUES ($1, $2)",
                        "account-1",  # Already exists
                        100
                    )
                    self.record_result("unique_violation", False, "Insert succeeded")
                except asyncpg.UniqueViolationError:
                    self.record_result("unique_violation", True)
        except Exception as e:
            self.record_result("unique_violation", False, str(e))

    async def test_foreign_key_violation(self):
        """Test foreign key constraint violation."""
        try:
            async with self.pool.acquire() as conn:
                try:
                    await conn.execute("""
                        INSERT INTO test_orders (account_id, symbol, quantity, price)
                        VALUES ($1, $2, $3, $4)
                    """, "nonexistent-account", "BTC-USD", Decimal("1.0"), Decimal("100"))
                    self.record_result("foreign_key_violation", False, "Insert succeeded")
                except asyncpg.ForeignKeyViolationError:
                    self.record_result("foreign_key_violation", True)
        except Exception as e:
            self.record_result("foreign_key_violation", False, str(e))

    async def test_check_violation(self):
        """Test check constraint violation (balance >= 0)."""
        try:
            async with self.pool.acquire() as conn:
                try:
                    await conn.execute(
                        "UPDATE test_accounts SET balance = $1 WHERE id = $2",
                        Decimal("-100"),  # Violates CHECK
                        "account-1"
                    )
                    self.record_result("check_violation", False, "Update succeeded")
                except asyncpg.CheckViolationError:
                    self.record_result("check_violation", True)
        except Exception as e:
            self.record_result("check_violation", False, str(e))

    async def test_query_timeout(self):
        """Test query timeout handling."""
        try:
            async with self.pool.acquire() as conn:
                try:
                    await conn.execute(
                        "SELECT pg_sleep(5)",
                        timeout=0.1  # 100ms timeout
                    )
                    self.record_result("query_timeout", False, "Query didn't timeout")
                except asyncio.TimeoutError:
                    self.record_result("query_timeout", True)
        except Exception as e:
            self.record_result("query_timeout", False, str(e))

    # =========================================================================
    # Run All Tests
    # =========================================================================

    async def run_all(self):
        """Run all validation tests."""
        logger.info("=" * 60)
        logger.info("asyncpg Pattern Validation")
        logger.info("=" * 60)

        if not await self.setup():
            logger.error("Setup failed, cannot continue")
            return False

        try:
            # Connection tests
            await self.test_basic_connection()
            await self.test_pool_acquire()
            await self.test_pool_stats()

            # Query tests
            await self.test_fetch()
            await self.test_fetchrow()
            await self.test_fetchval()
            await self.test_execute()
            await self.test_decimal_precision()

            # Transaction tests
            await self.test_basic_transaction()
            await self.test_transaction_rollback()
            await self.test_savepoint()
            await self.test_read_only_transaction()

            # Batch operation tests
            await self.test_executemany()
            await self.test_copy_records()

            # Error handling tests
            await self.test_unique_violation()
            await self.test_foreign_key_violation()
            await self.test_check_violation()
            await self.test_query_timeout()

        finally:
            await self.teardown()

        # Report results
        logger.info("=" * 60)
        logger.info("Results")
        logger.info("=" * 60)
        logger.info(f"Passed: {self.passed}")
        logger.info(f"Failed: {self.failed}")

        if self.errors:
            logger.info("\nFailed tests:")
            for test, error in self.errors:
                logger.info(f"  - {test}: {error}")

        return self.failed == 0


async def main():
    parser = argparse.ArgumentParser(description="Validate asyncpg patterns")
    parser.add_argument(
        "--dsn",
        default=os.environ.get("DATABASE_URL", DEFAULT_DSN),
        help="PostgreSQL connection string"
    )
    parser.add_argument(
        "--test",
        help="Run specific test (connection, pool, transactions, batch, errors)"
    )

    args = parser.parse_args()

    validator = AsyncpgValidator(args.dsn)
    success = await validator.run_all()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
