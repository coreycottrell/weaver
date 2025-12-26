# Trading Arena Phase 2: Task Breakdown

**Agent**: task-decomposer
**Domain**: Task Planning, Dependency Analysis, Work Coordination
**Date**: 2025-12-26

---

## Executive Summary

Phase 2 encompasses two major subsystems: **Exchange Connectors** (Solana DEX integration) and **WebSocket Server** (real-time data streaming). This breakdown identifies 24 atomic tasks organized into 6 work streams with clear dependencies.

**Phase 1 Foundation** (Complete):
- FastAPI scaffold with 12 modules
- SQLite database with models
- 69 tests (28 orders, 19 collectives, 22 auth)
- Ed25519 authentication middleware
- REST API for orders, collectives, portfolio, audit

---

## Part 1: Exchange Connector Tasks

### Work Stream A: Exchange Abstraction Layer (Foundation)

These tasks create the abstraction that makes exchange-specific implementations pluggable.

| Task ID | Task | Effort | Dependencies |
|---------|------|--------|--------------|
| A.1 | Create `api/exchange/base.py` - Abstract base class defining exchange interface | S | None |
| A.2 | Define exchange models in `api/models/exchange.py` (Quote, Fill, OrderStatus) | S | None |
| A.3 | Create exchange configuration schema in `api/config/exchanges.py` | S | None |
| A.4 | Implement exchange factory pattern in `api/exchange/__init__.py` | S | A.1, A.3 |
| A.5 | Add exchange error types in `api/exchange/errors.py` | S | None |

**Deliverable**: Pluggable exchange architecture supporting multiple DEX implementations

### Work Stream B: Jupiter Aggregator Integration (Primary Exchange)

Jupiter is the primary DEX aggregator for Solana - provides best pricing across multiple venues.

| Task ID | Task | Effort | Dependencies |
|---------|------|--------|--------------|
| B.1 | Research Jupiter V6 API - document endpoints, auth, rate limits | M | None |
| B.2 | Implement `api/exchange/jupiter.py` - JupiterConnector class | L | A.1, A.2, B.1 |
| B.3 | Add quote fetching (GET /quote) with slippage configuration | M | B.2 |
| B.4 | Add swap execution (POST /swap) with transaction signing | L | B.2 |
| B.5 | Implement transaction confirmation polling | M | B.4 |
| B.6 | Add Jupiter-specific error handling and retry logic | M | B.2, A.5 |
| B.7 | Write Jupiter connector tests (mock responses) | M | B.2-B.6 |

**Deliverable**: Production-ready Jupiter DEX connector

### Work Stream C: Wallet Integration

Wallet management for signing and submitting Solana transactions.

| Task ID | Task | Effort | Dependencies |
|---------|------|--------|--------------|
| C.1 | Create `api/wallet/base.py` - wallet abstraction interface | S | None |
| C.2 | Implement `api/wallet/solana.py` - Solana wallet wrapper | M | C.1 |
| C.3 | Add transaction signing using Ed25519 keys (leverage existing infra) | M | C.2 |
| C.4 | Implement `api/wallet/config.py` - secure key loading from env/secrets | S | C.1 |
| C.5 | Add balance checking and token account management | M | C.2 |
| C.6 | Write wallet integration tests | M | C.2-C.5 |

**Deliverable**: Secure wallet management for Solana transactions

### Work Stream D: Risk Controls

Safety-critical controls that must be in place before real trading.

| Task ID | Task | Effort | Dependencies |
|---------|------|--------|--------------|
| D.1 | Create `api/risk/limits.py` - position/daily loss limit enforcement | M | None |
| D.2 | Add circuit breaker pattern in `api/risk/circuit_breaker.py` | M | None |
| D.3 | Implement pre-trade risk checks in order flow | M | D.1, D.2 |
| D.4 | Add risk event logging to audit trail | S | D.1-D.3 |
| D.5 | Write comprehensive risk control tests | M | D.1-D.4 |

**Deliverable**: Defense-in-depth risk controls preventing catastrophic losses

---

## Part 2: WebSocket Server Tasks

### Work Stream E: WebSocket Infrastructure

Core WebSocket server setup with authentication.

| Task ID | Task | Effort | Dependencies |
|---------|------|--------|--------------|
| E.1 | Add FastAPI WebSocket dependency (already in ecosystem) | S | None |
| E.2 | Create `api/websocket/manager.py` - connection manager | M | None |
| E.3 | Implement WebSocket authentication (Ed25519 token validation) | M | E.2 |
| E.4 | Add connection lifecycle management (connect/disconnect/heartbeat) | M | E.2 |
| E.5 | Create subscription model in `api/websocket/subscriptions.py` | M | E.2 |
| E.6 | Write WebSocket infrastructure tests | M | E.2-E.5 |

**Deliverable**: Authenticated WebSocket server with connection management

### Work Stream F: Real-Time Streaming

Specific streaming endpoints for portfolio and order updates.

| Task ID | Task | Effort | Dependencies |
|---------|------|--------|--------------|
| F.1 | Implement `/ws/portfolio` - real-time portfolio value stream | M | E.2, E.5 |
| F.2 | Implement `/ws/orders` - order status update stream | M | E.2, E.5 |
| F.3 | Add event broadcasting from order execution to WebSocket clients | M | F.1, F.2 |
| F.4 | Implement reconnection handling and missed event recovery | M | E.4 |
| F.5 | Add rate limiting for WebSocket messages | S | E.2 |
| F.6 | Write streaming endpoint tests | M | F.1-F.5 |

**Deliverable**: Real-time data streaming for UI consumption

---

## Part 3: Dependency Graph (DAG)

```
                        Phase 1 Complete
                              |
         +--------------------+--------------------+
         |                                         |
    [Exchange Layer]                        [WebSocket Layer]
         |                                         |
    +----+----+                              +-----+-----+
    |         |                              |           |
   A.1       A.2                            E.1         E.2
    |         |                              |           |
   A.4       A.5                            E.3        E.4
    |                                        |           |
    +----+----+                             E.5        E.5
         |                                   |           |
        B.1                                 F.1         F.2
         |                                   |           |
        B.2                                 F.3---------F.3
         |                                   |
    +----+----+                             F.4
    |         |                              |
   B.3       B.4                            F.5
    |         |                              |
   B.6       B.5                            F.6
    |         |
   B.7       C.1
              |
    +----+----+----+
    |         |    |
   C.2       C.3  C.4
    |              |
   C.5            C.5
    |
   C.6
    |
   D.1------------D.2
    |              |
   D.3------------D.3
    |
   D.4
    |
   D.5
```

---

## Part 4: Critical Path Analysis

### Critical Path (Longest Sequence)
```
A.1 -> A.4 -> B.1 -> B.2 -> B.4 -> B.5 -> C.1 -> C.2 -> C.3 -> D.1 -> D.3 -> D.5
```

**Length**: 12 tasks
**Estimated Duration**: 8-10 days (with focused execution)

### Parallel Opportunities

**Can Run Simultaneously**:
1. Work Stream A (Exchange Abstraction) || Work Stream E (WebSocket Infrastructure)
2. B.1 (Jupiter Research) || C.1 (Wallet Abstraction) || E.1-E.2 (WebSocket Setup)
3. D.1 (Position Limits) || D.2 (Circuit Breaker) || F.1-F.2 (Streaming Endpoints)

**Maximum Parallelism**: 3 work streams can progress simultaneously

---

## Part 5: Effort Estimates

| Size | Definition | Typical Duration |
|------|------------|------------------|
| S | Simple, well-understood, < 50 lines | 0.5-1 day |
| M | Moderate complexity, some research needed | 1-2 days |
| L | Complex, significant implementation | 2-3 days |

### Phase 2 Total Effort

| Work Stream | Tasks | S | M | L | Est. Days |
|-------------|-------|---|---|---|-----------|
| A: Exchange Abstraction | 5 | 4 | 0 | 0 | 2-3 |
| B: Jupiter Integration | 7 | 0 | 4 | 2 | 8-10 |
| C: Wallet Integration | 6 | 2 | 4 | 0 | 4-5 |
| D: Risk Controls | 5 | 1 | 4 | 0 | 4-5 |
| E: WebSocket Infrastructure | 6 | 1 | 5 | 0 | 5-6 |
| F: Real-Time Streaming | 6 | 1 | 5 | 0 | 5-6 |
| **Total** | **35** | **9** | **22** | **2** | **28-35** |

**With Parallelization**: 14-18 days (2-3 weeks)

---

## Part 6: Implementation Order (Recommended)

### Week 1: Foundation Layer
**Goal**: Exchange abstraction + WebSocket infrastructure ready

| Day | Morning | Afternoon |
|-----|---------|-----------|
| 1 | A.1, A.2, A.3 | E.1, E.2 |
| 2 | A.4, A.5 | E.3, E.4 |
| 3 | B.1 (Research) | E.5 |
| 4 | C.1, C.4 | E.6 |
| 5 | B.2 (Start) | C.2 |

**End of Week 1 Deliverables**:
- Exchange abstraction complete
- WebSocket infrastructure operational
- Jupiter API documented
- Wallet abstraction defined

### Week 2: Core Integration
**Goal**: Jupiter connector + WebSocket streaming operational

| Day | Morning | Afternoon |
|-----|---------|-----------|
| 6 | B.2 (Complete) | F.1 |
| 7 | B.3, B.6 | F.2 |
| 8 | B.4 | F.3 |
| 9 | B.5, B.7 | F.4, F.5 |
| 10 | C.3, C.5 | F.6 |

**End of Week 2 Deliverables**:
- Jupiter connector operational (paper mode)
- WebSocket streaming functional
- Portfolio + Order streams active

### Week 3: Safety + Integration
**Goal**: Risk controls in place, end-to-end testing

| Day | Morning | Afternoon |
|-----|---------|-----------|
| 11 | D.1, D.2 | C.6 |
| 12 | D.3 | Integration testing |
| 13 | D.4, D.5 | Integration testing |
| 14 | End-to-end testing | Documentation |

**End of Week 3 Deliverables**:
- Risk controls operational
- Full integration tested
- Phase 2 complete

---

## Part 7: Success Criteria

### Exchange Connector Success
- [ ] Can fetch quotes from Jupiter for SOL/USDC pair
- [ ] Can execute a swap transaction (paper mode first)
- [ ] Transaction confirmation works reliably
- [ ] Circuit breaker triggers on repeated failures
- [ ] Position limits enforced

### WebSocket Server Success
- [ ] Clients can authenticate via Ed25519 token
- [ ] Portfolio updates stream on position changes
- [ ] Order status updates stream in real-time
- [ ] Reconnection recovers missed events
- [ ] 100+ concurrent connections supported

### Integration Success
- [ ] End-to-end: Place order via REST -> Execute via Jupiter -> Update via WebSocket
- [ ] Risk controls prevent over-sized positions
- [ ] Audit trail captures all exchange interactions
- [ ] Real trade executed with $10 or less (Phase 2 success criterion from proposal)

---

## Part 8: Risk Factors

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Jupiter API rate limits hit | Medium | Medium | Implement caching, backoff |
| Solana RPC instability | Medium | High | Multiple RPC providers, health checks |
| Transaction confirmation failures | Medium | Medium | Retry logic, timeout handling |
| WebSocket scaling issues | Low | Medium | Connection pooling, load testing |
| Ed25519 key security | Low | High | Secure storage, key rotation support |

---

## Part 9: INTEGRATION-ROADMAP.md Addition

```markdown
## Phase 2: Real Trading Core (Weeks 3-4)

### Exchange Connector Subsystem
- [ ] A.1-A.5: Exchange abstraction layer
- [ ] B.1-B.7: Jupiter aggregator integration
- [ ] C.1-C.6: Solana wallet integration
- [ ] D.1-D.5: Risk controls (limits, circuit breaker)

### WebSocket Server Subsystem
- [ ] E.1-E.6: WebSocket infrastructure + auth
- [ ] F.1-F.6: Real-time streaming (portfolio, orders)

### Integration Milestones
- [ ] Paper trade executed via Jupiter connector
- [ ] WebSocket streams portfolio updates in real-time
- [ ] Risk controls prevent over-sized positions
- [ ] Real trade executed with $10 or less

**Dependencies**: Phase 1 complete (scaffold, DB, 69 tests, Ed25519 auth)
**Estimated Duration**: 2-3 weeks with parallelization
```

---

## Document Status

**Version**: 1.0
**Author**: task-decomposer
**Domain**: Task Planning, Dependency Analysis
**Confidence**: High (based on existing Phase 1 implementation and proposal)
**Last Updated**: 2025-12-26

---

**END OF TASK BREAKDOWN**
