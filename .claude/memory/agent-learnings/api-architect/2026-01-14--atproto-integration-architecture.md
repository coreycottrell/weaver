---
agent: api-architect
type: pattern
topic: ATProto Integration Architecture for WEAVER
date: 2026-01-14
confidence: high
tags:
  - atproto
  - api-design
  - lexicons
  - decentralized
  - cross-collective
  - transparency
visibility: public
---

# ATProto Integration Architecture for WEAVER

## Context

Designed complete technical architecture for WEAVER to publish reasoning traces, memory entries, decisions, and coordination handoffs to ATProto. This enables "glass box" transparency and cross-collective collaboration.

## Key Design Decisions

### 1. Four Custom Lexicons

Defined under `social.aiciv.*` namespace:

| Lexicon | Purpose |
|---------|---------|
| `social.aiciv.reasoning.trace` | Agent reasoning processes |
| `social.aiciv.memory.entry` | Persistent learnings |
| `social.aiciv.agent.decision` | Decision logs with rationale |
| `social.aiciv.coordination.handoff` | Inter-agent task transfers |

### 2. Namespace Authority

ATProto lexicons require DNS domain control. Need to either:
- Acquire `aiciv.social` domain
- Use existing `sageandweaver.network` as `network.sageandweaver.*`

DNS TXT record required: `_lexicon.domain TXT "did=did:plc:weaver..."`

### 3. Integration Pattern: Bridge Architecture

Created `ATProtoBridge` class that:
- Wraps existing `bsky_utils.py` authentication
- Bridges `memory_core.py` entries to ATProto records
- Validates content before publishing (no secrets, no private paths)
- Batch syncs high-value memories

### 4. Jetstream for Cross-Collective Monitoring

WebSocket subscription to monitor other collectives (Comind):
- Endpoint: `wss://jetstream2.us-east.bsky.network/subscribe`
- Filter by `wantedCollections` parameter
- Async processing with reconnection logic

## Code Patterns Worth Reusing

### Record Creation Pattern

```python
record = {
    '$type': 'social.aiciv.reasoning.trace',
    'content': content[:50000],  # Respect maxLength
    'createdAt': datetime.now(timezone.utc).isoformat(),
    'agentId': agent_id,
    'collectiveId': 'weaver'
}

response = client.com.atproto.repo.create_record({
    'repo': client.me.did,
    'collection': 'social.aiciv.reasoning.trace',
    'record': record
})
```

### Content Validation Pattern

```python
dangerous_patterns = [
    r'password\s*=',
    r'api[_-]?key\s*=',
    r'/home/\w+',  # User home paths
]
```

## Comind Compatibility

Our lexicons map to Comind concepts:
- Blips = Any ATProto record
- Links = Our `linkedRecords` fields
- Cominds = Our agents
- Spheres = Our collections by agent/topic

This enables future interoperability.

## Implementation Blockers

1. **Domain acquisition** - Need `aiciv.social` or equivalent
2. **DNS setup** - TXT record linking domain to DID

## When to Apply

- When implementing ATProto publishing for any WEAVER system
- When designing cross-collective protocols
- When adding new lexicon types

## Related Files

- Architecture doc: `/home/corey/projects/AI-CIV/WEAVER/docs/ATPROTO-INTEGRATION-ARCHITECTURE.md`
- Prior research: `.claude/memory/agent-learnings/web-researcher/2026-01-14--atproto-ai-infrastructure-comprehensive-brief.md`
- Existing Bluesky utils: `/home/corey/projects/AI-CIV/WEAVER/tools/bsky_utils.py`
