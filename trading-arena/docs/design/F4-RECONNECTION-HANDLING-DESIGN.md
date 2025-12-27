# F.4 Reconnection Handling Design

**Agent**: api-architect
**Domain**: API Design / WebSocket Protocol
**Date**: 2025-12-26

---

## Executive Summary

This document specifies the design for Trading Arena WebSocket reconnection handling. The goal is to enable clients to recover their complete trading state after a connection drop without requiring multiple round-trips.

---

## 1. Design Decision: On-Demand vs Auto-Send

### Recommendation: **Hybrid Approach**

| Approach | Pros | Cons |
|----------|------|------|
| Auto-send on connect | Immediate state, no extra message | Wasted bandwidth if client already has state, larger connect payload |
| On-demand via message | Client controls timing, explicit | Extra round-trip, delayed state |
| **Hybrid** | Best of both | Slightly more complexity |

**Hybrid Design**:
1. On connect: Server sends a lightweight `connection_established` message with connection metadata
2. Client sends `get_initial_state` to request full state recovery
3. This gives clients control while keeping the API explicit

**Rationale**:
- Collectives may have cached state from prior session
- Explicit request allows selective state recovery (e.g., only orders, not full portfolio)
- Follows existing handler pattern (request-response)
- Reduces wasted bandwidth for quick reconnects where state hasn't changed

---

## 2. Message Specification

### 2.1 Inbound Message: `get_initial_state`

```json
{
    "id": "msg-reconnect-001",
    "type": "get_initial_state",
    "data": {
        "include": ["portfolio", "balances", "orders", "subscriptions"]
    }
}
```

#### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | No | Request ID for correlation |
| `type` | string | Yes | Must be `"get_initial_state"` |
| `data.include` | array[string] | No | Components to include. If omitted, returns all. |

#### Valid `include` Values

| Value | Description |
|-------|-------------|
| `portfolio` | Full portfolio state (balances + positions + total values) |
| `balances` | Balance details only |
| `orders` | Open orders only (status=OPEN or PARTIALLY_FILLED) |
| `subscriptions` | Current room subscriptions |
| `connection` | Connection metadata (connected_at, message_count) |

**Note**: If `include` is omitted or empty, all components are returned.

---

### 2.2 Outbound Response: `initial_state`

```json
{
    "id": "msg-reconnect-001",
    "type": "initial_state",
    "success": true,
    "data": {
        "portfolio": {
            "collective_id": "team-alpha",
            "balances": {
                "USD": {
                    "currency": "USD",
                    "total": 100000.00,
                    "available": 95000.00,
                    "reserved": 5000.00
                }
            },
            "positions": {},
            "total_value_usd": 100000.00,
            "unrealized_pnl": 0.0,
            "realized_pnl": 0.0,
            "last_updated": "2025-12-26T10:30:00Z"
        },
        "balances": {
            "USD": {
                "currency": "USD",
                "total": 100000.00,
                "available": 95000.00,
                "reserved": 5000.00
            }
        },
        "orders": {
            "open_orders": [
                {
                    "order_id": "ord-123",
                    "symbol": "BTC/USD",
                    "side": "buy",
                    "order_type": "limit",
                    "quantity": 0.5,
                    "price": 42000.00,
                    "filled_quantity": 0.0,
                    "status": "open",
                    "created_at": "2025-12-26T10:25:00Z"
                }
            ],
            "count": 1
        },
        "subscriptions": {
            "rooms": [
                "portfolio:team-alpha",
                "orders:team-alpha",
                "market"
            ]
        },
        "connection": {
            "connected_at": "2025-12-26T10:30:00Z",
            "message_count": 42,
            "portfolio_updates_received": 5,
            "orders_received": 3,
            "market_updates_received": 100
        }
    },
    "timestamp": "2025-12-26T10:30:05Z"
}
```

#### Response Structure

| Field | Type | Included When | Description |
|-------|------|---------------|-------------|
| `data.portfolio` | object | `include` contains `"portfolio"` or is empty | Full portfolio state |
| `data.balances` | object | `include` contains `"balances"` or is empty | Balance breakdown |
| `data.orders` | object | `include` contains `"orders"` or is empty | Open orders list |
| `data.subscriptions` | object | `include` contains `"subscriptions"` or is empty | Current room subscriptions |
| `data.connection` | object | `include` contains `"connection"` or is empty | Connection metadata |

---

### 2.3 Error Response

```json
{
    "id": "msg-reconnect-001",
    "type": "error",
    "success": false,
    "error": {
        "code": "INVALID_INCLUDE",
        "message": "Unknown include value: 'invalid_component'"
    },
    "timestamp": "2025-12-26T10:30:05Z"
}
```

---

## 3. Handler Implementation Approach

### 3.1 New MessageType Enum Value

Add to `MessageType` enum in `handlers.py`:

```python
class MessageType(str, Enum):
    # ... existing types ...

    # Reconnection
    GET_INITIAL_STATE = "get_initial_state"
```

### 3.2 New Handler Class

Create `GetInitialStateHandler` following the existing pattern:

```python
class GetInitialStateHandler(MessageHandler):
    """Handler for get_initial_state messages (reconnection support)."""

    VALID_INCLUDES = {"portfolio", "balances", "orders", "subscriptions", "connection"}

    @property
    def message_type(self) -> MessageType:
        return MessageType.GET_INITIAL_STATE

    @property
    def response_type(self) -> str:
        return "initial_state"

    async def handle(
        self,
        collective_id: str,
        data: Dict[str, Any]
    ) -> HandlerResult:
        """
        Gather and return initial state for reconnection.

        Aggregates portfolio, orders, subscriptions based on
        requested includes.
        """
        # Implementation details in section 3.3
```

### 3.3 Handler Logic Flow

```
1. Parse 'include' array from data (default to all if empty/missing)
2. Validate include values against VALID_INCLUDES
3. For each requested component:
   a. portfolio: Call get_or_create_portfolio() - reuse GetPortfolioHandler logic
   b. balances: Extract from portfolio - reuse GetBalancesHandler logic
   c. orders: Query open orders (status IN ['open', 'partially_filled'])
   d. subscriptions: Get from connection manager metadata
   e. connection: Get from connection manager metadata
4. Assemble response data dict with only requested components
5. Return success HandlerResult with aggregated data
```

### 3.4 Register Handler

Add to `_register_default_handlers()`:

```python
def _register_default_handlers(self):
    handlers = [
        # ... existing handlers ...

        # Reconnection
        GetInitialStateHandler(),
    ]
```

---

## 4. Files to Modify

| File | Changes |
|------|---------|
| `/home/corey/projects/AI-CIV/WEAVER/trading-arena/api/websocket/handlers.py` | Add `GET_INITIAL_STATE` to `MessageType`, add `GetInitialStateHandler` class, register in `_register_default_handlers()` |

**No changes needed to**:
- `manager.py` - Already tracks all needed metadata
- `websocket.py` (routes) - Dispatcher already routes by message type

---

## 5. Integration Points

### 5.1 Reuse Existing Handler Logic

The `GetInitialStateHandler` should delegate to existing handlers rather than duplicate logic:

```python
# Conceptual - reuse existing handler instances or their logic
portfolio_handler = GetPortfolioHandler()
portfolio_result = await portfolio_handler.handle(collective_id, {})

orders_handler = GetOrdersHandler()
orders_result = await orders_handler.handle(collective_id, {"status": "open"})
```

### 5.2 Manager Access for Subscriptions/Connection

```python
from ..websocket.manager import manager

metadata = manager.get_metadata(collective_id)
if metadata:
    subscriptions = list(metadata.subscriptions)
    connection_info = {
        "connected_at": metadata.connected_at.isoformat(),
        "message_count": metadata.message_count,
        # ... other metadata fields
    }
```

---

## 6. Client Usage Example

### 6.1 Reconnection Flow

```python
# Client reconnects
await websocket.connect(f"wss://arena.example/ws/v1/{collective_id}")

# Authenticate (Ed25519)
await websocket.send({"type": "auth", "data": {...}})

# Request full state recovery
await websocket.send({
    "id": "reconnect-001",
    "type": "get_initial_state",
    "data": {}  # Empty = get everything
})

# Receive aggregated state
response = await websocket.recv()
# response.type == "initial_state"
# response.data contains portfolio, orders, subscriptions, connection
```

### 6.2 Selective Recovery

```python
# Only need open orders (already have cached portfolio)
await websocket.send({
    "id": "selective-001",
    "type": "get_initial_state",
    "data": {
        "include": ["orders", "subscriptions"]
    }
})
```

---

## 7. Performance Considerations

### 7.1 Single Response vs Multiple

**Chosen**: Single aggregated response

**Rationale**:
- Reduces round-trips (critical for reconnection latency)
- Atomic snapshot of state at one point in time
- Client knows when recovery is complete

### 7.2 Order Filtering

Only return **open** orders (`status IN ['open', 'partially_filled']`), not full order history.

**Rationale**:
- Historical orders are not needed for state recovery
- Reduces payload size
- Client can request full history separately via `get_orders`

### 7.3 Payload Size Estimate

| Component | Typical Size |
|-----------|--------------|
| Portfolio | ~500 bytes |
| Balances | ~200 bytes |
| Orders (10 open) | ~2 KB |
| Subscriptions | ~100 bytes |
| Connection | ~200 bytes |
| **Total** | **~3 KB** |

Well within WebSocket message limits.

---

## 8. Future Enhancements (Out of Scope)

1. **State Diffing**: Client sends last known state hash, server returns only changes
2. **Sequence Numbers**: Track message sequence for gap detection
3. **Compressed Responses**: gzip for large order books

These are not needed for F.4 but noted for future consideration.

---

## 9. Summary

| Aspect | Decision |
|--------|----------|
| Trigger | On-demand via `get_initial_state` message |
| Response | Single aggregated `initial_state` response |
| Selectivity | Optional `include` array for partial recovery |
| Implementation | New handler class following existing pattern |
| Files Changed | `handlers.py` only |

This design follows the established handler architecture, reuses existing logic where possible, and provides flexibility for clients while keeping the implementation straightforward.

---

**Document Status**: Design Complete - Ready for Implementation
**Next Step**: Implement `GetInitialStateHandler` in `handlers.py`
