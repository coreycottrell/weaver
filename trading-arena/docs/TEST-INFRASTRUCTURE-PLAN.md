# Trading Arena Phase 2: Test Infrastructure Plan

**Author**: test-architect
**Date**: 2025-12-26
**Status**: DRAFT - Ready for Review

---

## Executive Summary

This document defines the comprehensive test strategy for Trading Arena Phase 2 components:
- WebSocket real-time feeds
- Order matching engine
- Portfolio management
- Risk controls
- Public dashboard

**Current State**: Phase 1 has solid test foundations with 65+ tests covering auth, collectives, and orders using FastAPI TestClient and Ed25519 signing fixtures.

**Target Coverage**: 85%+ for critical paths (matching engine, risk controls), 75%+ overall.

---

## 1. Test Categories Required

### 1.1 Unit Tests (Fast, Isolated)

| Component | Purpose | Estimated Count |
|-----------|---------|-----------------|
| Order Matching Engine | Price-time priority, matching algorithms | 40-50 |
| Risk Calculator | Position limits, margin calculations | 25-30 |
| Portfolio Valuation | Mark-to-market, P&L calculations | 20-25 |
| WebSocket Message Serialization | Message encoding/decoding | 15-20 |

### 1.2 Integration Tests (Component Interaction)

| Component | Purpose | Estimated Count |
|-----------|---------|-----------------|
| Order Flow | Order submission -> matching -> fill | 30-40 |
| Portfolio Updates | Order fills -> balance changes | 20-25 |
| WebSocket Broadcasting | Events -> subscribed clients | 25-30 |
| Database Operations | Async CRUD with real PostgreSQL | 35-40 |

### 1.3 End-to-End Tests (Full System)

| Scenario | Purpose | Estimated Count |
|----------|---------|-----------------|
| Trading Session | Complete trading workflow | 10-15 |
| Multi-Collective | Multiple collectives trading | 8-12 |
| Recovery Scenarios | Disconnect/reconnect handling | 5-8 |

### 1.4 Performance Tests (Load & Stress)

| Test Type | Purpose | Tools |
|-----------|---------|-------|
| Throughput | Orders per second capacity | locust, pytest-benchmark |
| Latency | Order-to-fill time distribution | pytest-benchmark |
| WebSocket Scale | Concurrent connection limits | websockets + asyncio |
| Memory Profiling | Leak detection under load | memray, tracemalloc |

---

## 2. Testing Tools Required

### 2.1 Core Testing Dependencies

```toml
# pyproject.toml or requirements-test.txt additions

[project.optional-dependencies]
test = [
    # Core pytest stack
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",

    # Async testing
    "anyio>=4.0.0",
    "httpx>=0.26.0",

    # WebSocket testing
    "websockets>=12.0",
    "pytest-timeout>=2.2.0",

    # Database testing
    "pytest-postgresql>=5.0.0",
    "testcontainers[postgres]>=3.7.0",
    "factory-boy>=3.3.0",

    # Mocking & fixtures
    "pytest-mock>=3.12.0",
    "freezegun>=1.2.2",
    "faker>=22.0.0",

    # Performance testing
    "pytest-benchmark>=4.0.0",
    "locust>=2.20.0",

    # Code quality
    "pytest-randomly>=3.15.0",
    "pytest-xdist>=3.5.0",  # Parallel execution
]
```

### 2.2 Tool-Specific Configurations

#### pytest.ini (Updated)
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
asyncio_mode = auto
filterwarnings =
    ignore::DeprecationWarning
markers =
    unit: Unit tests (fast, no external dependencies)
    integration: Integration tests (database, services)
    e2e: End-to-end tests (full system)
    performance: Performance tests (may be slow)
    websocket: WebSocket-specific tests
    slow: Tests that take >1 second
timeout = 30
```

---

## 3. Test Directory Structure

```
trading-arena/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # Shared fixtures (existing)
│   │
│   ├── unit/                          # Fast, isolated tests
│   │   ├── __init__.py
│   │   ├── conftest.py                # Unit-specific fixtures
│   │   ├── test_matching_engine.py    # Order matching algorithms
│   │   ├── test_risk_calculator.py    # Risk limit calculations
│   │   ├── test_portfolio_calc.py     # P&L, valuation logic
│   │   ├── test_message_types.py      # WebSocket message schemas
│   │   └── test_price_feeds.py        # Price aggregation logic
│   │
│   ├── integration/                   # Component interaction tests
│   │   ├── __init__.py
│   │   ├── conftest.py                # Database fixtures
│   │   ├── test_order_flow.py         # Order lifecycle
│   │   ├── test_portfolio_updates.py  # Balance tracking
│   │   ├── test_websocket_feeds.py    # Real-time subscriptions
│   │   ├── test_db_operations.py      # Async database tests
│   │   └── test_audit_logging.py      # Audit trail integrity
│   │
│   ├── e2e/                           # Full system tests
│   │   ├── __init__.py
│   │   ├── conftest.py                # Full stack setup
│   │   ├── test_trading_session.py    # Complete workflows
│   │   ├── test_multi_collective.py   # Concurrent trading
│   │   └── test_recovery.py           # Failure scenarios
│   │
│   ├── performance/                   # Load & stress tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_throughput.py         # Orders per second
│   │   ├── test_latency.py            # Response times
│   │   ├── test_websocket_scale.py    # Connection limits
│   │   └── locustfile.py              # Load test scenarios
│   │
│   ├── fixtures/                      # Shared test data
│   │   ├── __init__.py
│   │   ├── factories.py               # Factory Boy definitions
│   │   ├── sample_orders.py           # Order test data
│   │   └── market_data.py             # Price feed mocks
│   │
│   └── helpers/                       # Test utilities
│       ├── __init__.py
│       ├── websocket_client.py        # Test WebSocket client
│       ├── order_helpers.py           # Order creation helpers
│       └── assertions.py              # Custom assertions
│
├── # Existing test files (Phase 1)
├── test_auth.py                       # -> Move to integration/
├── test_collectives.py                # -> Move to integration/
└── test_orders.py                     # -> Move to integration/
```

---

## 4. Critical Test Scenarios by Component

### 4.1 WebSocket Real-Time Feeds

#### Connection Lifecycle Tests
```python
# tests/integration/test_websocket_feeds.py

class TestWebSocketConnection:
    """WebSocket connection lifecycle tests."""

    @pytest.mark.websocket
    async def test_successful_connection_with_auth(
        self, ws_client, registered_collective, auth_signer
    ):
        """Authenticated collective can establish WebSocket connection."""
        # Connect with valid auth token
        # Verify connection accepted
        # Verify welcome message received

    @pytest.mark.websocket
    async def test_connection_rejected_without_auth(self, ws_client):
        """Unauthenticated connection should be rejected."""

    @pytest.mark.websocket
    async def test_connection_timeout_handling(self, ws_client, auth_signer):
        """Connection should timeout if no heartbeat."""

    @pytest.mark.websocket
    async def test_graceful_disconnect(self, ws_client, auth_signer):
        """Client disconnect should cleanup subscriptions."""

    @pytest.mark.websocket
    async def test_server_initiated_disconnect(self, ws_client, auth_signer):
        """Server can disconnect misbehaving clients."""
```

#### Subscription Tests
```python
class TestWebSocketSubscriptions:
    """Channel subscription tests."""

    async def test_subscribe_to_order_updates(self, ws_client, auth_signer):
        """Can subscribe to own order updates."""

    async def test_subscribe_to_market_data(self, ws_client, auth_signer):
        """Can subscribe to market data feed."""

    async def test_subscribe_to_portfolio_updates(self, ws_client, auth_signer):
        """Can subscribe to portfolio changes."""

    async def test_unsubscribe_from_channel(self, ws_client, auth_signer):
        """Can unsubscribe from channels."""

    async def test_subscription_isolation(
        self, ws_client, registered_collective, registered_collective_2
    ):
        """Collective A should not receive Collective B's private updates."""
```

#### Message Delivery Tests
```python
class TestWebSocketMessageDelivery:
    """Real-time message delivery tests."""

    async def test_order_created_broadcast(self, ws_client, auth_signer):
        """Order creation triggers WebSocket notification."""

    async def test_order_filled_broadcast(self, ws_client, auth_signer):
        """Order fill triggers WebSocket notification."""

    async def test_portfolio_update_on_fill(self, ws_client, auth_signer):
        """Portfolio balance update broadcast on fill."""

    async def test_message_ordering_preserved(self, ws_client, auth_signer):
        """Messages should arrive in causal order."""

    async def test_backpressure_handling(self, ws_client, auth_signer):
        """Slow clients should be handled gracefully."""
```

### 4.2 Order Matching Engine

#### Matching Algorithm Tests
```python
# tests/unit/test_matching_engine.py

class TestPriceTimePriority:
    """Test price-time priority matching."""

    def test_best_price_matched_first(self, order_book):
        """Best price orders should match before worse prices."""

    def test_time_priority_at_same_price(self, order_book):
        """Earlier orders at same price should match first."""

    def test_partial_fill_at_best_price(self, order_book):
        """Large order should partially fill at best price."""


class TestMarketOrders:
    """Market order matching tests."""

    def test_market_buy_matches_best_ask(self, order_book):
        """Market buy should match against best ask price."""

    def test_market_sell_matches_best_bid(self, order_book):
        """Market sell should match against best bid price."""

    def test_market_order_sweeps_book(self, order_book):
        """Large market order should sweep through price levels."""

    def test_market_order_partial_fill(self, order_book):
        """Market order should partially fill if insufficient liquidity."""

    def test_market_order_rejected_no_liquidity(self, order_book):
        """Market order should be rejected if order book empty."""


class TestLimitOrders:
    """Limit order matching tests."""

    def test_limit_buy_matches_at_or_below_price(self, order_book):
        """Limit buy should match at or below limit price."""

    def test_limit_sell_matches_at_or_above_price(self, order_book):
        """Limit sell should match at or above limit price."""

    def test_limit_order_rests_in_book(self, order_book):
        """Unmatched limit order should rest in order book."""

    def test_limit_order_price_improvement(self, order_book):
        """Limit order should get price improvement if available."""


class TestSelfTradeProtection:
    """Self-trade prevention tests."""

    def test_self_trade_rejected(self, order_book, collective):
        """Order matching own order should be rejected."""

    def test_cross_collective_trade_allowed(
        self, order_book, collective_a, collective_b
    ):
        """Different collectives should be able to trade."""
```

#### Order Book State Tests
```python
class TestOrderBookState:
    """Order book state management tests."""

    def test_add_order_updates_book(self, order_book):
        """Adding order should update book correctly."""

    def test_cancel_order_removes_from_book(self, order_book):
        """Cancelling order should remove from book."""

    def test_partial_fill_updates_quantity(self, order_book):
        """Partial fill should update remaining quantity."""

    def test_full_fill_removes_from_book(self, order_book):
        """Full fill should remove order from book."""

    def test_best_bid_ask_tracking(self, order_book):
        """Best bid/ask should be tracked correctly."""

    def test_order_book_snapshot(self, order_book):
        """Should produce accurate order book snapshot."""
```

### 4.3 Portfolio Management

#### Balance Management Tests
```python
# tests/integration/test_portfolio_updates.py

class TestBalanceManagement:
    """Portfolio balance management tests."""

    async def test_initial_balance_allocation(self, db_session, collective):
        """New collective should receive initial USDC balance."""

    async def test_balance_reserved_on_order(self, db_session, collective):
        """Placing order should reserve balance."""

    async def test_reserved_released_on_cancel(self, db_session, collective):
        """Cancelling order should release reserved balance."""

    async def test_balance_deducted_on_fill(self, db_session, collective):
        """Fill should deduct from balance correctly."""

    async def test_asset_credited_on_buy_fill(self, db_session, collective):
        """Buy fill should credit asset to portfolio."""

    async def test_concurrent_order_balance_check(self, db_session, collective):
        """Concurrent orders should not overdraw balance."""


class TestPositionTracking:
    """Position tracking tests."""

    async def test_position_created_on_first_buy(self, db_session, collective):
        """First buy should create new position."""

    async def test_position_increased_on_additional_buy(
        self, db_session, collective
    ):
        """Additional buy should increase position."""

    async def test_position_decreased_on_sell(self, db_session, collective):
        """Sell should decrease position."""

    async def test_position_closed_on_full_sell(self, db_session, collective):
        """Selling entire position should close it."""

    async def test_average_cost_calculation(self, db_session, collective):
        """Average cost should be calculated correctly."""
```

#### P&L Calculation Tests
```python
class TestPnLCalculation:
    """Profit and loss calculation tests."""

    async def test_unrealized_pnl_calculation(self, db_session, collective):
        """Unrealized P&L should track mark-to-market."""

    async def test_realized_pnl_on_close(self, db_session, collective):
        """Realized P&L should be calculated on position close."""

    async def test_fifo_cost_basis(self, db_session, collective):
        """FIFO cost basis should be used for P&L."""

    async def test_pnl_with_multiple_fills(self, db_session, collective):
        """P&L should handle multiple partial fills."""
```

### 4.4 Risk Controls

#### Position Limit Tests
```python
# tests/unit/test_risk_calculator.py

class TestPositionLimits:
    """Position limit enforcement tests."""

    def test_order_rejected_exceeds_position_limit(self, risk_engine):
        """Order exceeding position limit should be rejected."""

    def test_order_allowed_within_limit(self, risk_engine):
        """Order within limit should be allowed."""

    def test_position_limit_per_symbol(self, risk_engine):
        """Position limits should be enforced per symbol."""

    def test_aggregate_position_limit(self, risk_engine):
        """Aggregate position across all symbols should be limited."""


class TestOrderValueLimits:
    """Order value limit tests."""

    def test_single_order_max_value(self, risk_engine):
        """Single order should not exceed max value."""

    def test_daily_order_value_limit(self, risk_engine):
        """Daily aggregate order value should be limited."""

    def test_order_rate_limiting(self, risk_engine):
        """Order submission rate should be limited."""


class TestBalanceValidation:
    """Balance validation tests."""

    def test_insufficient_balance_rejected(self, risk_engine, portfolio):
        """Order with insufficient balance should be rejected."""

    def test_balance_check_includes_reserved(self, risk_engine, portfolio):
        """Balance check should account for reserved funds."""

    def test_short_selling_not_allowed(self, risk_engine, portfolio):
        """Short selling without position should be rejected."""
```

#### Circuit Breaker Tests
```python
class TestCircuitBreakers:
    """Circuit breaker tests."""

    def test_daily_loss_limit_halt(self, risk_engine, portfolio):
        """Trading should halt if daily loss limit reached."""

    def test_consecutive_loss_warning(self, risk_engine, portfolio):
        """Warning should trigger on consecutive losses."""

    def test_circuit_breaker_reset_next_day(self, risk_engine):
        """Circuit breakers should reset at day boundary."""
```

### 4.5 Public Dashboard

#### Dashboard Data Tests
```python
# tests/integration/test_dashboard.py

class TestLeaderboard:
    """Leaderboard endpoint tests."""

    async def test_leaderboard_ranking(self, client, multiple_collectives):
        """Leaderboard should rank by total return."""

    async def test_leaderboard_anonymization(self, client, collective):
        """Leaderboard should respect privacy settings."""

    async def test_leaderboard_time_periods(self, client):
        """Leaderboard should support different time periods."""


class TestMarketStats:
    """Market statistics tests."""

    async def test_volume_aggregation(self, client):
        """Volume should aggregate across all trades."""

    async def test_price_history(self, client):
        """Price history should be accurate."""

    async def test_active_orders_count(self, client):
        """Active order count should be accurate."""
```

---

## 5. Shared Test Fixtures

### 5.1 Database Fixtures
```python
# tests/conftest.py (additions)

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_container():
    """Spin up PostgreSQL container for integration tests."""
    with PostgresContainer("postgres:15") as postgres:
        yield postgres

@pytest_asyncio.fixture
async def db_session(postgres_container) -> AsyncSession:
    """Provide async database session for tests."""
    database_url = postgres_container.get_connection_url()
    # Convert to async URL
    database_url = database_url.replace(
        "postgresql://", "postgresql+asyncpg://"
    )

    engine = create_async_engine(database_url, echo=False)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
```

### 5.2 WebSocket Test Client
```python
# tests/helpers/websocket_client.py

import asyncio
import json
from typing import Optional, Callable
from websockets.client import connect as ws_connect
from websockets.exceptions import ConnectionClosed

class TestWebSocketClient:
    """WebSocket client for testing."""

    def __init__(self, base_url: str, auth_token: Optional[str] = None):
        self.base_url = base_url
        self.auth_token = auth_token
        self.connection = None
        self.received_messages: list[dict] = []
        self._receive_task: Optional[asyncio.Task] = None

    async def connect(self, path: str = "/ws") -> None:
        """Establish WebSocket connection."""
        url = f"{self.base_url}{path}"
        headers = {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        self.connection = await ws_connect(url, extra_headers=headers)
        self._receive_task = asyncio.create_task(self._receive_loop())

    async def _receive_loop(self) -> None:
        """Background task to receive messages."""
        try:
            async for message in self.connection:
                data = json.loads(message)
                self.received_messages.append(data)
        except ConnectionClosed:
            pass

    async def send(self, message: dict) -> None:
        """Send message."""
        await self.connection.send(json.dumps(message))

    async def wait_for_message(
        self,
        predicate: Callable[[dict], bool],
        timeout: float = 5.0
    ) -> dict:
        """Wait for message matching predicate."""
        start_idx = len(self.received_messages)
        deadline = asyncio.get_event_loop().time() + timeout

        while asyncio.get_event_loop().time() < deadline:
            for msg in self.received_messages[start_idx:]:
                if predicate(msg):
                    return msg
            await asyncio.sleep(0.1)

        raise TimeoutError("No matching message received")

    async def close(self) -> None:
        """Close connection."""
        if self._receive_task:
            self._receive_task.cancel()
        if self.connection:
            await self.connection.close()
```

### 5.3 Factory Boy Definitions
```python
# tests/fixtures/factories.py

import factory
from factory import fuzzy
from datetime import datetime, timezone
from decimal import Decimal

from api.db.models import (
    Collective, Order, PortfolioBalance,
    OrderStatus, OrderSide, OrderType, TimeInForce
)

class CollectiveFactory(factory.Factory):
    """Factory for Collective test data."""
    class Meta:
        model = Collective

    collective_id = factory.Sequence(lambda n: f"test-collective-{n}")
    display_name = factory.Faker("company")
    public_key = factory.Faker("sha256")
    public_key_fingerprint = factory.LazyAttribute(
        lambda o: o.public_key[:8]
    )
    registered_at = factory.LazyFunction(
        lambda: datetime.now(timezone.utc)
    )


class OrderFactory(factory.Factory):
    """Factory for Order test data."""
    class Meta:
        model = Order

    order_id = factory.Sequence(lambda n: f"arena-ord-{n:08d}")
    collective_id = factory.Faker("slug")
    symbol = fuzzy.FuzzyChoice(["SOL/USDC", "BTC/USDC", "ETH/USDC"])
    side = fuzzy.FuzzyChoice([OrderSide.BUY, OrderSide.SELL])
    type = fuzzy.FuzzyChoice([OrderType.LIMIT, OrderType.MARKET])
    quantity = fuzzy.FuzzyDecimal(0.1, 100.0, precision=8)
    price = fuzzy.FuzzyDecimal(10.0, 50000.0, precision=8)
    status = OrderStatus.OPEN
    time_in_force = TimeInForce.GTC


class PortfolioBalanceFactory(factory.Factory):
    """Factory for PortfolioBalance test data."""
    class Meta:
        model = PortfolioBalance

    collective_id = factory.Faker("slug")
    currency = "USDC"
    quantity = factory.LazyFunction(lambda: Decimal("10000.00"))
    available = factory.LazyFunction(lambda: Decimal("10000.00"))
    reserved = factory.LazyFunction(lambda: Decimal("0.00"))
```

---

## 6. Coverage Targets

### 6.1 Component Coverage Goals

| Component | Target | Critical Paths |
|-----------|--------|----------------|
| Order Matching Engine | 90%+ | 95%+ |
| Risk Controls | 90%+ | 95%+ |
| Portfolio Management | 85%+ | 90%+ |
| WebSocket Feeds | 80%+ | 85%+ |
| Public Dashboard | 75%+ | 80%+ |
| Database Operations | 85%+ | 90%+ |
| **Overall** | **85%+** | **90%+** |

### 6.2 Coverage Configuration
```ini
# .coveragerc

[run]
source = api
branch = True
omit =
    */tests/*
    */__pycache__/*
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if TYPE_CHECKING:
    @abstractmethod

fail_under = 80
show_missing = True

[html]
directory = htmlcov
```

---

## 7. Test Execution Strategy

### 7.1 Local Development
```bash
# Fast unit tests (run frequently during development)
pytest tests/unit -v --tb=short

# Integration tests (run before commits)
pytest tests/integration -v

# Full suite
pytest --cov=api --cov-report=html

# Performance tests (run manually)
pytest tests/performance -v --benchmark-only
```

### 7.2 CI Pipeline
```yaml
# .github/workflows/test.yml

name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -e .[test]
      - run: pytest tests/unit -v --tb=short

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: trading_arena_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -e .[test]
      - run: pytest tests/integration -v --tb=short
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:test@localhost:5432/trading_arena_test

  coverage:
    runs-on: ubuntu-latest
    needs: [unit-tests, integration-tests]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -e .[test]
      - run: pytest --cov=api --cov-report=xml --cov-fail-under=80
      - uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
```

---

## 8. Testing Patterns for Phase 2 Challenges

### 8.1 Async Database Operations

**Challenge**: Testing async SQLAlchemy with proper transaction isolation.

**Pattern**: Use `pytest-asyncio` with transaction rollback per test.

```python
@pytest_asyncio.fixture
async def db_session(engine):
    """Transaction-isolated database session."""
    connection = await engine.connect()
    transaction = await connection.begin()

    session = AsyncSession(bind=connection)

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()
```

### 8.2 WebSocket Connection Lifecycle

**Challenge**: Testing persistent connections with message ordering.

**Pattern**: Use async context managers with message queues.

```python
@pytest.mark.websocket
async def test_order_update_sequence(ws_client, auth_signer, client):
    """Verify order updates arrive in correct sequence."""
    async with ws_client.connect() as ws:
        # Subscribe to order updates
        await ws.send({"type": "subscribe", "channel": "orders"})

        # Place order via REST API
        order_response = await client.post("/v1/orders", ...)

        # Wait for WebSocket notifications
        created_msg = await ws.wait_for_message(
            lambda m: m["type"] == "order.created"
        )

        assert created_msg["order_id"] == order_response.json()["order_id"]
```

### 8.3 Real-Time Data Consistency

**Challenge**: Ensuring REST and WebSocket data are consistent.

**Pattern**: Use checksums and sequence numbers.

```python
async def test_portfolio_consistency(ws_client, client, auth_signer):
    """Portfolio via REST and WebSocket should match."""
    async with ws_client.connect() as ws:
        await ws.send({"type": "subscribe", "channel": "portfolio"})

        # Get REST snapshot
        rest_response = await client.get("/v1/portfolio", ...)

        # Wait for WebSocket snapshot
        ws_snapshot = await ws.wait_for_message(
            lambda m: m["type"] == "portfolio.snapshot"
        )

        # Compare checksums
        assert ws_snapshot["checksum"] == rest_response.json()["checksum"]
```

### 8.4 Order Matching Correctness

**Challenge**: Verifying matching engine determinism.

**Pattern**: Property-based testing with invariant checking.

```python
from hypothesis import given, strategies as st

class TestMatchingInvariants:
    """Property-based tests for matching engine."""

    @given(
        buy_orders=st.lists(st.floats(min_value=1, max_value=1000)),
        sell_orders=st.lists(st.floats(min_value=1, max_value=1000)),
    )
    def test_no_crossed_book_after_matching(
        self, order_book, buy_orders, sell_orders
    ):
        """Order book should never be crossed after matching."""
        for price in buy_orders:
            order_book.add_order(make_buy_order(price=price))
        for price in sell_orders:
            order_book.add_order(make_sell_order(price=price))

        order_book.match()

        if order_book.best_bid and order_book.best_ask:
            assert order_book.best_bid < order_book.best_ask
```

### 8.5 Risk Limit Enforcement

**Challenge**: Testing risk limits under concurrent access.

**Pattern**: Use locks and race condition testing.

```python
async def test_concurrent_orders_respect_limit(
    client, auth_signer, risk_limits
):
    """Concurrent orders should not exceed position limit."""
    # Set position limit to 100
    risk_limits["max_position"] = 100

    # Submit 10 orders of size 20 concurrently
    tasks = [
        client.post(
            "/v1/orders",
            json=make_order_data(quantity=20),
            headers=auth_signer.sign_request(...)
        )
        for _ in range(10)
    ]

    responses = await asyncio.gather(*tasks)

    # Only 5 orders should succeed (5 * 20 = 100)
    successful = [r for r in responses if r.status_code == 201]
    rejected = [r for r in responses if r.status_code == 400]

    assert len(successful) == 5
    assert len(rejected) == 5
```

---

## 9. Quality Gates

### 9.1 Definition of Done (Tests)

- [ ] All new code has corresponding tests
- [ ] Coverage >= 80% overall, >= 90% for critical paths
- [ ] No flaky tests (< 1% failure rate in CI)
- [ ] Integration tests pass with real PostgreSQL
- [ ] WebSocket tests verify message ordering
- [ ] Performance tests establish baseline metrics
- [ ] Test documentation updated

### 9.2 Test Review Checklist

- [ ] Test names clearly describe behavior
- [ ] Arrange-Act-Assert pattern followed
- [ ] Fixtures used appropriately
- [ ] Edge cases covered
- [ ] Error conditions tested
- [ ] Async/await used correctly
- [ ] No hard-coded timeouts (use fixtures)
- [ ] Cleanup happens even on failure

---

## 10. Implementation Roadmap

### Week 1: Infrastructure Setup
- [ ] Add testing dependencies to requirements
- [ ] Create directory structure
- [ ] Set up database fixtures with testcontainers
- [ ] Create WebSocket test client helper
- [ ] Migrate existing tests to new structure

### Week 2: Matching Engine Tests
- [ ] Unit tests for price-time priority
- [ ] Unit tests for order types
- [ ] Integration tests for order flow
- [ ] Property-based tests for invariants

### Week 3: Portfolio & Risk Tests
- [ ] Unit tests for P&L calculations
- [ ] Integration tests for balance management
- [ ] Unit tests for risk limits
- [ ] Concurrent access tests

### Week 4: WebSocket & E2E Tests
- [ ] WebSocket connection tests
- [ ] Subscription tests
- [ ] Message delivery tests
- [ ] Full trading session E2E tests
- [ ] Performance baseline tests

---

## Appendix A: Sample Test File

```python
# tests/integration/test_order_flow.py
"""
Order Flow Integration Tests

Tests the complete lifecycle of an order from submission to fill.
"""

import pytest
import pytest_asyncio
from decimal import Decimal

from api.db.models import Order, OrderStatus, OrderFill
from tests.fixtures.factories import CollectiveFactory, OrderFactory


@pytest.mark.integration
class TestOrderLifecycle:
    """Test complete order lifecycle."""

    @pytest_asyncio.fixture
    async def setup(self, db_session, client, keypair):
        """Set up test collective and authenticate."""
        collective = CollectiveFactory(
            collective_id="lifecycle-test",
            public_key=keypair["public_key_b64"]
        )
        db_session.add(collective)
        await db_session.commit()

        return {"collective": collective, "keypair": keypair}

    async def test_limit_order_rests_then_fills(
        self, client, setup, auth_signer, db_session
    ):
        """Limit order should rest, then fill when matched."""
        # Place limit buy order
        buy_order = await client.post(
            "/v1/orders",
            json={
                "symbol": "SOL/USDC",
                "side": "buy",
                "type": "limit",
                "quantity": 10.0,
                "price": 100.0
            },
            headers=auth_signer.sign_request(...)
        )
        assert buy_order.status_code == 201
        assert buy_order.json()["status"] == "open"

        # Verify order is in book (via internal check)
        order_id = buy_order.json()["order_id"]
        order = await db_session.get(Order, order_id)
        assert order.status == OrderStatus.OPEN

        # Place matching sell order (different collective)
        # ... matching logic ...

        # Verify fill occurred
        await db_session.refresh(order)
        assert order.status == OrderStatus.FILLED
        assert order.filled_quantity == Decimal("10.0")
```

---

**Document End**

*Generated by test-architect for Trading Arena Phase 2*
*Review and approve before implementation*
