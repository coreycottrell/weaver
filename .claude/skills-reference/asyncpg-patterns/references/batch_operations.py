# database/batch_operations.py
"""
Batch operation patterns for high-throughput asyncpg usage.

Covers:
- executemany for multiple inserts
- COPY protocol for bulk loading (10-100x faster than INSERT)
- Batch updates with unnest
- Bulk delete patterns
- Streaming large result sets
"""

import asyncpg
from typing import List, Tuple, Any, Optional, AsyncIterator, Dict
from decimal import Decimal
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# executemany - Multiple Inserts
# =============================================================================

async def batch_insert_basic(
    conn: asyncpg.Connection,
    orders: List[Tuple[str, str, str, Decimal, Decimal]]
) -> int:
    """
    Basic batch insert with executemany.

    executemany prepares the statement once, then executes N times
    with different parameters. Efficient for moderate batch sizes (100-10000).

    Args:
        orders: List of (collective_id, symbol, side, quantity, price)

    Returns:
        Number of rows inserted
    """
    await conn.executemany("""
        INSERT INTO orders (collective_id, symbol, side, quantity, price)
        VALUES ($1, $2, $3, $4, $5)
    """, orders)

    return len(orders)


async def batch_insert_from_dicts(
    conn: asyncpg.Connection,
    orders: List[Dict[str, Any]]
) -> int:
    """
    Batch insert from list of dictionaries.

    Converts dict format to tuple format for executemany.
    """
    records = [
        (
            order['collective_id'],
            order['symbol'],
            order['side'],
            order['quantity'],
            order['price'],
        )
        for order in orders
    ]

    await conn.executemany("""
        INSERT INTO orders (collective_id, symbol, side, quantity, price)
        VALUES ($1, $2, $3, $4, $5)
    """, records)

    return len(records)


async def batch_insert_with_returning(
    conn: asyncpg.Connection,
    orders: List[Dict[str, Any]]
) -> List[int]:
    """
    Batch insert with RETURNING to get generated IDs.

    NOTE: executemany doesn't support RETURNING.
    Use single INSERT with unnest for this pattern.

    Args:
        orders: List of order dictionaries

    Returns:
        List of generated order IDs
    """
    if not orders:
        return []

    # Extract columns into arrays
    collective_ids = [o['collective_id'] for o in orders]
    symbols = [o['symbol'] for o in orders]
    sides = [o['side'] for o in orders]
    quantities = [o['quantity'] for o in orders]
    prices = [o['price'] for o in orders]

    # Single INSERT with unnest (PostgreSQL array expansion)
    rows = await conn.fetch("""
        INSERT INTO orders (collective_id, symbol, side, quantity, price)
        SELECT * FROM unnest(
            $1::text[],
            $2::text[],
            $3::text[],
            $4::numeric[],
            $5::numeric[]
        )
        RETURNING id
    """, collective_ids, symbols, sides, quantities, prices)

    return [row['id'] for row in rows]


async def batch_insert_with_conflict(
    conn: asyncpg.Connection,
    users: List[Tuple[str, str, str]]  # (id, email, name)
) -> Tuple[int, int]:
    """
    Batch upsert - insert or update on conflict.

    Returns:
        Tuple of (inserted_count, updated_count)

    Note: This uses a transaction with count comparison.
    """
    async with conn.transaction():
        # Count before
        before = await conn.fetchval("SELECT COUNT(*) FROM users")

        # Upsert all records
        await conn.executemany("""
            INSERT INTO users (id, email, name)
            VALUES ($1, $2, $3)
            ON CONFLICT (id) DO UPDATE
            SET email = EXCLUDED.email,
                name = EXCLUDED.name,
                updated_at = NOW()
        """, users)

        # Count after
        after = await conn.fetchval("SELECT COUNT(*) FROM users")

        inserted = after - before
        updated = len(users) - inserted

        return inserted, updated


# =============================================================================
# COPY Protocol - Bulk Loading (Fastest)
# =============================================================================

async def copy_records_basic(
    conn: asyncpg.Connection,
    table: str,
    records: List[Tuple],
    columns: List[str]
) -> int:
    """
    Bulk load using PostgreSQL COPY protocol.

    COPY is 10-100x faster than INSERT for large datasets.
    Uses binary protocol for optimal performance.

    Performance comparison (100K rows):
    - Individual INSERTs: ~60-120 seconds
    - executemany: ~10-30 seconds
    - COPY: ~0.5-2 seconds

    Args:
        table: Target table name
        records: List of tuples matching column order
        columns: List of column names

    Returns:
        Number of rows copied
    """
    result = await conn.copy_records_to_table(
        table,
        records=records,
        columns=columns,
    )
    return int(result.split()[-1])  # "COPY 1000" -> 1000


async def copy_trades_example(
    conn: asyncpg.Connection,
    trades: List[Dict[str, Any]]
) -> int:
    """
    Example: Bulk load trades using COPY.

    Converts dict format and uses copy_records_to_table.
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

    columns = [
        'collective_id', 'symbol', 'side',
        'quantity', 'price', 'fee', 'executed_at'
    ]

    result = await conn.copy_records_to_table(
        'trades',
        records=records,
        columns=columns,
    )

    logger.info(f"Copied {len(trades)} trades")
    return len(trades)


async def copy_from_csv_file(
    conn: asyncpg.Connection,
    table: str,
    filepath: str,
    columns: Optional[List[str]] = None,
    has_header: bool = True,
    delimiter: str = ','
):
    """
    Load data from CSV file using COPY.

    Uses text format for CSV compatibility.
    """
    with open(filepath, 'rb') as f:
        await conn.copy_to_table(
            table,
            source=f,
            columns=columns,
            format='csv',
            header=has_header,
            delimiter=delimiter,
        )


async def copy_to_csv_file(
    conn: asyncpg.Connection,
    query: str,
    filepath: str,
    include_header: bool = True
):
    """
    Export query results to CSV file using COPY.

    Much faster than fetching and writing manually.
    """
    with open(filepath, 'wb') as f:
        await conn.copy_from_query(
            query,
            output=f,
            format='csv',
            header=include_header,
        )


async def copy_with_schema_types(
    conn: asyncpg.Connection,
    table: str,
    records: List[Tuple],
    columns: List[str],
    schema_name: str = 'public'
) -> int:
    """
    COPY with explicit schema reference.

    Use when working with non-public schemas.
    """
    return await conn.copy_records_to_table(
        table,
        records=records,
        columns=columns,
        schema_name=schema_name,
    )


# =============================================================================
# Batch Updates
# =============================================================================

async def batch_update_with_unnest(
    conn: asyncpg.Connection,
    updates: List[Tuple[int, Decimal]]  # (order_id, new_quantity)
) -> int:
    """
    Batch update using unnest for efficiency.

    Much faster than individual UPDATE statements.

    Args:
        updates: List of (id, new_value) tuples

    Returns:
        Number of rows updated
    """
    if not updates:
        return 0

    result = await conn.execute("""
        UPDATE orders o
        SET quantity = u.new_quantity,
            updated_at = NOW()
        FROM (
            SELECT * FROM unnest($1::int[], $2::numeric[])
            AS t(order_id, new_quantity)
        ) u
        WHERE o.id = u.order_id
    """,
        [u[0] for u in updates],  # order_ids
        [u[1] for u in updates]   # new_quantities
    )

    # Parse "UPDATE N" response
    return int(result.split()[-1])


async def batch_update_multiple_columns(
    conn: asyncpg.Connection,
    updates: List[Dict[str, Any]]  # [{id, status, quantity, price}, ...]
) -> int:
    """
    Batch update multiple columns at once.
    """
    if not updates:
        return 0

    ids = [u['id'] for u in updates]
    statuses = [u['status'] for u in updates]
    quantities = [u['quantity'] for u in updates]
    prices = [u['price'] for u in updates]

    result = await conn.execute("""
        UPDATE orders o
        SET status = u.status,
            quantity = u.quantity,
            price = u.price,
            updated_at = NOW()
        FROM (
            SELECT * FROM unnest($1::int[], $2::text[], $3::numeric[], $4::numeric[])
            AS t(id, status, quantity, price)
        ) u
        WHERE o.id = u.id
    """, ids, statuses, quantities, prices)

    return int(result.split()[-1])


async def conditional_batch_update(
    conn: asyncpg.Connection,
    order_ids: List[int],
    new_status: str,
    required_current_status: str
) -> int:
    """
    Batch update with condition - only update matching rows.

    Example: Cancel all pending orders (but not filled ones).
    """
    result = await conn.execute("""
        UPDATE orders
        SET status = $1, updated_at = NOW()
        WHERE id = ANY($2) AND status = $3
    """, new_status, order_ids, required_current_status)

    return int(result.split()[-1])


# =============================================================================
# Bulk Delete
# =============================================================================

async def batch_delete(
    conn: asyncpg.Connection,
    table: str,
    id_column: str,
    ids: List[int]
) -> int:
    """
    Delete multiple rows by ID.

    Args:
        table: Table name
        id_column: ID column name
        ids: List of IDs to delete

    Returns:
        Number of rows deleted
    """
    if not ids:
        return 0

    # Note: f-string for table/column names (not user input)
    # IDs are parameterized
    result = await conn.execute(
        f"DELETE FROM {table} WHERE {id_column} = ANY($1)",
        ids
    )

    return int(result.split()[-1])


async def delete_with_archive(
    conn: asyncpg.Connection,
    order_ids: List[int]
) -> int:
    """
    Delete with archival - move to archive table first.

    Useful for audit trails or soft delete patterns.
    """
    async with conn.transaction():
        # Copy to archive
        await conn.execute("""
            INSERT INTO orders_archive
            SELECT *, NOW() as archived_at
            FROM orders
            WHERE id = ANY($1)
        """, order_ids)

        # Delete from main table
        result = await conn.execute("""
            DELETE FROM orders WHERE id = ANY($1)
        """, order_ids)

        return int(result.split()[-1])


# =============================================================================
# Streaming Large Result Sets
# =============================================================================

async def stream_large_query(
    conn: asyncpg.Connection,
    query: str,
    *args,
    batch_size: int = 1000
) -> AsyncIterator[asyncpg.Record]:
    """
    Stream large query results using a cursor.

    Prevents loading entire result set into memory.
    Must be used within a transaction.

    Args:
        query: SQL query
        *args: Query parameters
        batch_size: Number of rows to fetch at a time

    Yields:
        Individual records
    """
    async with conn.transaction():
        async for record in conn.cursor(query, *args, prefetch=batch_size):
            yield record


async def stream_and_process(
    conn: asyncpg.Connection,
    table: str,
    process_func: callable,
    batch_size: int = 1000
) -> int:
    """
    Stream rows and process in batches.

    Example: Process all orders without loading into memory.
    """
    processed = 0

    async with conn.transaction():
        async for record in conn.cursor(
            f"SELECT * FROM {table} ORDER BY id",
            prefetch=batch_size
        ):
            await process_func(record)
            processed += 1

            if processed % batch_size == 0:
                logger.info(f"Processed {processed} rows...")

    return processed


async def paginated_query(
    conn: asyncpg.Connection,
    table: str,
    page: int,
    per_page: int = 50,
    order_by: str = 'id'
) -> List[asyncpg.Record]:
    """
    Paginated query using LIMIT/OFFSET.

    For large offsets, consider keyset pagination instead.
    """
    offset = (page - 1) * per_page

    return await conn.fetch(
        f"SELECT * FROM {table} ORDER BY {order_by} LIMIT $1 OFFSET $2",
        per_page,
        offset
    )


async def keyset_pagination(
    conn: asyncpg.Connection,
    table: str,
    last_id: Optional[int],
    limit: int = 50
) -> List[asyncpg.Record]:
    """
    Keyset (cursor) pagination - efficient for large datasets.

    Instead of OFFSET, uses WHERE id > last_seen_id.
    Doesn't slow down for large page numbers.

    Args:
        table: Table name
        last_id: Last seen ID (None for first page)
        limit: Number of rows to fetch

    Returns:
        List of records
    """
    if last_id is None:
        return await conn.fetch(
            f"SELECT * FROM {table} ORDER BY id LIMIT $1",
            limit
        )
    else:
        return await conn.fetch(
            f"SELECT * FROM {table} WHERE id > $1 ORDER BY id LIMIT $2",
            last_id,
            limit
        )


# =============================================================================
# Performance Comparison Helper
# =============================================================================

async def compare_insert_methods(
    conn: asyncpg.Connection,
    records: List[Tuple],
    table: str,
    columns: List[str]
) -> Dict[str, float]:
    """
    Compare performance of different insert methods.

    For benchmarking and choosing the right approach.
    """
    import time

    results = {}

    # Clear table for fair test
    await conn.execute(f"TRUNCATE {table}")

    # Method 1: Individual inserts
    start = time.perf_counter()
    for record in records[:100]:  # Limit for sanity
        placeholders = ', '.join(f'${i+1}' for i in range(len(columns)))
        await conn.execute(
            f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})",
            *record
        )
    results['individual_100'] = time.perf_counter() - start

    # Clear
    await conn.execute(f"TRUNCATE {table}")

    # Method 2: executemany
    start = time.perf_counter()
    placeholders = ', '.join(f'${i+1}' for i in range(len(columns)))
    await conn.executemany(
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})",
        records
    )
    results['executemany'] = time.perf_counter() - start

    # Clear
    await conn.execute(f"TRUNCATE {table}")

    # Method 3: COPY
    start = time.perf_counter()
    await conn.copy_records_to_table(table, records=records, columns=columns)
    results['copy'] = time.perf_counter() - start

    return results
