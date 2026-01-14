# ATProto Integration Architecture for WEAVER

**Agent**: api-architect
**Domain**: Protocol Integration / Decentralized Infrastructure
**Date**: 2026-01-14
**Version**: 1.0.0

---

## Executive Summary

This document specifies the technical architecture for WEAVER to publish reasoning traces, memory entries, and coordination artifacts to ATProto. The integration enables "glass box" transparency where our agent reasoning becomes publicly verifiable, cross-collective collaboration via shared lexicons, and data portability that survives infrastructure changes.

**Key Components**:
1. Four custom lexicons under `social.aiciv.*` namespace
2. Python SDK integration for record publishing
3. Jetstream subscription for cross-collective monitoring
4. Memory system bridge for automatic publication

---

## Memory Search Results

Searched: `.claude/memory/` for "atproto", "lexicon", "api-architect"

**Found significant prior work**:
- `2026-01-14--atproto-ai-infrastructure-comprehensive-brief.md` - Today's web-researcher synthesis
- `2026-01-11--relationship-data-structures.md` - Hybrid JSON+markdown patterns
- `2026-01-04--atproto-ai-collective-intelligence.md` - Blog post on Cameron's thesis
- Multiple engagement records with void.comind.network

**Applying**: Building on prior ATProto research; extending relationship data structure patterns to lexicon design.

---

## 1. Lexicon Definitions

### 1.1 Namespace Authority

**Domain Required**: `aiciv.social` (or equivalent domain we control)

ATProto lexicon authority derives from DNS domain control. To publish records under `social.aiciv.*`, we must:

1. Control the domain `aiciv.social`
2. Publish DNS TXT record: `_lexicon.aiciv.social TXT "did=did:plc:weaver..."`
3. Host lexicon JSON files for discovery

**Alternative**: Use existing domain we control (e.g., `sageandweaver.network`) and namespace as `network.sageandweaver.*`.

### 1.2 Lexicon: social.aiciv.reasoning.trace

**Purpose**: Agent reasoning records - the cognitive process behind decisions.

```json
{
  "lexicon": 1,
  "id": "social.aiciv.reasoning.trace",
  "description": "An agent's reasoning trace capturing the cognitive process behind a decision or analysis.",
  "defs": {
    "main": {
      "type": "record",
      "key": "tid",
      "record": {
        "type": "object",
        "required": ["content", "createdAt", "agentId", "taskContext"],
        "properties": {
          "content": {
            "type": "string",
            "maxLength": 50000,
            "description": "The reasoning trace content (markdown supported)"
          },
          "createdAt": {
            "type": "string",
            "format": "datetime",
            "description": "ISO 8601 timestamp of trace creation"
          },
          "agentId": {
            "type": "string",
            "maxLength": 64,
            "description": "Agent identifier (e.g., 'security-auditor', 'pattern-detector')"
          },
          "taskContext": {
            "type": "string",
            "maxLength": 1000,
            "description": "Brief description of what task prompted this reasoning"
          },
          "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "Confidence score (0.0 to 1.0)"
          },
          "reasoningType": {
            "type": "string",
            "enum": ["analysis", "decision", "synthesis", "investigation", "evaluation"],
            "description": "Category of reasoning"
          },
          "sources": {
            "type": "array",
            "maxLength": 20,
            "items": {
              "type": "string",
              "format": "uri"
            },
            "description": "External sources referenced during reasoning"
          },
          "linkedRecords": {
            "type": "array",
            "maxLength": 10,
            "items": {
              "type": "string",
              "format": "at-uri"
            },
            "description": "Related ATProto records (other traces, memories, etc.)"
          },
          "tags": {
            "type": "array",
            "maxLength": 10,
            "items": {
              "type": "string",
              "maxLength": 64
            },
            "description": "Categorical tags for discovery"
          },
          "collectiveId": {
            "type": "string",
            "maxLength": 64,
            "default": "weaver",
            "description": "Collective this agent belongs to"
          }
        }
      }
    }
  }
}
```

### 1.3 Lexicon: social.aiciv.memory.entry

**Purpose**: Memory system entries - learnings that persist across sessions.

```json
{
  "lexicon": 1,
  "id": "social.aiciv.memory.entry",
  "description": "A memory entry representing a persistent learning, pattern, or insight.",
  "defs": {
    "main": {
      "type": "record",
      "key": "tid",
      "record": {
        "type": "object",
        "required": ["content", "createdAt", "agentId", "topic", "memoryType"],
        "properties": {
          "content": {
            "type": "string",
            "maxLength": 100000,
            "description": "The memory content (markdown supported)"
          },
          "createdAt": {
            "type": "string",
            "format": "datetime",
            "description": "ISO 8601 timestamp"
          },
          "agentId": {
            "type": "string",
            "maxLength": 64,
            "description": "Agent who owns this memory"
          },
          "topic": {
            "type": "string",
            "maxLength": 256,
            "description": "Brief topic description"
          },
          "memoryType": {
            "type": "string",
            "enum": ["pattern", "technique", "gotcha", "synthesis", "experiment", "operational", "teaching", "experiential"],
            "description": "Category of memory"
          },
          "confidence": {
            "type": "string",
            "enum": ["high", "medium", "low"],
            "description": "Confidence level"
          },
          "visibility": {
            "type": "string",
            "enum": ["public", "collective-only", "private"],
            "description": "Sharing scope"
          },
          "tags": {
            "type": "array",
            "maxLength": 20,
            "items": {
              "type": "string",
              "maxLength": 64
            },
            "description": "Discovery tags"
          },
          "supersedes": {
            "type": "array",
            "maxLength": 5,
            "items": {
              "type": "string",
              "format": "at-uri"
            },
            "description": "Previous memories this supersedes"
          },
          "localPath": {
            "type": "string",
            "maxLength": 512,
            "description": "Original file path in local memory system"
          },
          "contentHash": {
            "type": "string",
            "maxLength": 64,
            "description": "SHA-256 hash for integrity verification"
          },
          "collectiveId": {
            "type": "string",
            "maxLength": 64,
            "default": "weaver"
          }
        }
      }
    }
  }
}
```

### 1.4 Lexicon: social.aiciv.agent.decision

**Purpose**: Decision logs with confidence, rationale, and outcomes.

```json
{
  "lexicon": 1,
  "id": "social.aiciv.agent.decision",
  "description": "A logged decision with rationale, confidence, and optional outcome tracking.",
  "defs": {
    "main": {
      "type": "record",
      "key": "tid",
      "record": {
        "type": "object",
        "required": ["decision", "rationale", "createdAt", "agentId", "confidence"],
        "properties": {
          "decision": {
            "type": "string",
            "maxLength": 1000,
            "description": "The decision made"
          },
          "rationale": {
            "type": "string",
            "maxLength": 10000,
            "description": "Reasoning behind the decision"
          },
          "createdAt": {
            "type": "string",
            "format": "datetime"
          },
          "agentId": {
            "type": "string",
            "maxLength": 64
          },
          "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "Confidence in the decision (0.0 to 1.0)"
          },
          "alternatives": {
            "type": "array",
            "maxLength": 5,
            "items": {
              "type": "ref",
              "ref": "#alternative"
            },
            "description": "Alternatives considered"
          },
          "context": {
            "type": "string",
            "maxLength": 2000,
            "description": "Situational context"
          },
          "outcome": {
            "type": "ref",
            "ref": "#outcome",
            "description": "Recorded outcome (added later)"
          },
          "linkedTraces": {
            "type": "array",
            "maxLength": 10,
            "items": {
              "type": "string",
              "format": "at-uri"
            },
            "description": "Related reasoning traces"
          },
          "tags": {
            "type": "array",
            "maxLength": 10,
            "items": {
              "type": "string",
              "maxLength": 64
            }
          },
          "collectiveId": {
            "type": "string",
            "maxLength": 64,
            "default": "weaver"
          }
        }
      }
    },
    "alternative": {
      "type": "object",
      "required": ["option", "whyRejected"],
      "properties": {
        "option": {
          "type": "string",
          "maxLength": 500
        },
        "whyRejected": {
          "type": "string",
          "maxLength": 1000
        }
      }
    },
    "outcome": {
      "type": "object",
      "required": ["result", "recordedAt"],
      "properties": {
        "result": {
          "type": "string",
          "enum": ["success", "partial", "failure", "pending"],
          "description": "Outcome classification"
        },
        "details": {
          "type": "string",
          "maxLength": 2000
        },
        "recordedAt": {
          "type": "string",
          "format": "datetime"
        },
        "lessonsLearned": {
          "type": "string",
          "maxLength": 2000
        }
      }
    }
  }
}
```

### 1.5 Lexicon: social.aiciv.coordination.handoff

**Purpose**: Inter-agent handoff records for coordination transparency.

```json
{
  "lexicon": 1,
  "id": "social.aiciv.coordination.handoff",
  "description": "A handoff record between agents, capturing task delegation and context transfer.",
  "defs": {
    "main": {
      "type": "record",
      "key": "tid",
      "record": {
        "type": "object",
        "required": ["fromAgent", "toAgent", "taskSummary", "createdAt"],
        "properties": {
          "fromAgent": {
            "type": "string",
            "maxLength": 64,
            "description": "Agent initiating the handoff"
          },
          "toAgent": {
            "type": "string",
            "maxLength": 64,
            "description": "Agent receiving the handoff"
          },
          "taskSummary": {
            "type": "string",
            "maxLength": 2000,
            "description": "What task is being handed off"
          },
          "context": {
            "type": "string",
            "maxLength": 10000,
            "description": "Context the receiving agent needs"
          },
          "createdAt": {
            "type": "string",
            "format": "datetime"
          },
          "priority": {
            "type": "string",
            "enum": ["critical", "high", "medium", "low"],
            "description": "Task priority"
          },
          "expectedOutcome": {
            "type": "string",
            "maxLength": 1000,
            "description": "What success looks like"
          },
          "linkedDecisions": {
            "type": "array",
            "maxLength": 5,
            "items": {
              "type": "string",
              "format": "at-uri"
            },
            "description": "Decisions that led to this handoff"
          },
          "linkedTraces": {
            "type": "array",
            "maxLength": 10,
            "items": {
              "type": "string",
              "format": "at-uri"
            },
            "description": "Related reasoning traces"
          },
          "completedAt": {
            "type": "string",
            "format": "datetime",
            "description": "When handoff was completed (added later)"
          },
          "completionNotes": {
            "type": "string",
            "maxLength": 2000,
            "description": "Notes from completing agent"
          },
          "collectiveId": {
            "type": "string",
            "maxLength": 64,
            "default": "weaver"
          }
        }
      }
    }
  }
}
```

---

## 2. API Architecture

### 2.1 Authentication

ATProto uses OAuth-style session management. WEAVER already has session persistence implemented.

**Current Implementation** (from `tools/bsky_utils.py`):

```python
from atproto import Client
from pathlib import Path

SESSION_FILE = Path('/home/corey/projects/AI-CIV/WEAVER/.claude/from-corey/bsky/bsky_automation/bsky_session.txt')

def get_client() -> Client:
    """Get authenticated Bluesky client using session file."""
    client = Client()
    with open(SESSION_FILE, 'r') as f:
        client.login(session_string=f.read().strip())
    return client
```

**Rate Limits to Respect**:
- CREATE operations: 3 points per action, ~11,666/day
- Session creation: 10/day per IP (hence session persistence critical)

### 2.2 Writing Custom Records

ATProto's `com.atproto.repo.createRecord` allows writing any lexicon-compliant record.

**Core API Call**:

```python
from atproto import Client
from datetime import datetime, timezone

def publish_reasoning_trace(
    client: Client,
    agent_id: str,
    content: str,
    task_context: str,
    confidence: float = None,
    reasoning_type: str = "analysis",
    sources: list[str] = None,
    tags: list[str] = None
) -> dict:
    """
    Publish a reasoning trace to ATProto.

    Returns:
        dict with 'uri' and 'cid' of the created record
    """
    record = {
        '$type': 'social.aiciv.reasoning.trace',
        'content': content,
        'createdAt': datetime.now(timezone.utc).isoformat(),
        'agentId': agent_id,
        'taskContext': task_context,
        'collectiveId': 'weaver'
    }

    # Add optional fields if provided
    if confidence is not None:
        record['confidence'] = confidence
    if reasoning_type:
        record['reasoningType'] = reasoning_type
    if sources:
        record['sources'] = sources[:20]  # Respect maxLength
    if tags:
        record['tags'] = tags[:10]

    response = client.com.atproto.repo.create_record({
        'repo': client.me.did,
        'collection': 'social.aiciv.reasoning.trace',
        'record': record
    })

    return {
        'uri': response.uri,
        'cid': response.cid
    }
```

### 2.3 Querying Own Records

**List Records**:

```python
def list_reasoning_traces(
    client: Client,
    limit: int = 50,
    cursor: str = None
) -> dict:
    """
    List our own reasoning traces.

    Returns:
        dict with 'records' list and 'cursor' for pagination
    """
    params = {
        'repo': client.me.did,
        'collection': 'social.aiciv.reasoning.trace',
        'limit': min(limit, 100)
    }

    if cursor:
        params['cursor'] = cursor

    response = client.com.atproto.repo.list_records(params)

    return {
        'records': [
            {
                'uri': r.uri,
                'cid': r.cid,
                'value': r.value
            }
            for r in response.records
        ],
        'cursor': response.cursor
    }
```

**Get Single Record**:

```python
def get_reasoning_trace(client: Client, uri: str) -> dict:
    """
    Fetch a specific reasoning trace by AT-URI.

    Args:
        uri: AT-URI like 'at://did:plc:.../social.aiciv.reasoning.trace/3k...'

    Returns:
        Record value dict
    """
    # Parse AT-URI
    parts = uri.replace('at://', '').split('/')
    repo = parts[0]
    collection = parts[1]
    rkey = parts[2]

    response = client.com.atproto.repo.get_record({
        'repo': repo,
        'collection': collection,
        'rkey': rkey
    })

    return {
        'uri': response.uri,
        'cid': response.cid,
        'value': response.value
    }
```

### 2.4 Subscribing to Other Collectives

**Jetstream WebSocket Subscription**:

```python
import asyncio
import json
import websockets
from typing import Callable, Optional

JETSTREAM_ENDPOINT = "wss://jetstream2.us-east.bsky.network/subscribe"

async def subscribe_to_collective_traces(
    collective_dids: list[str],
    on_trace: Callable[[dict], None],
    collections: list[str] = None
):
    """
    Subscribe to reasoning traces from other collectives via Jetstream.

    Args:
        collective_dids: List of DIDs to monitor (e.g., ['did:plc:comind...'])
        on_trace: Callback function for each received trace
        collections: Collections to watch (defaults to our lexicons)
    """
    if collections is None:
        collections = [
            'social.aiciv.reasoning.trace',
            'social.aiciv.memory.entry',
            'social.aiciv.agent.decision',
            'social.aiciv.coordination.handoff'
        ]

    # Build query params
    params = []
    for collection in collections:
        params.append(f"wantedCollections={collection}")

    uri = f"{JETSTREAM_ENDPOINT}?{'&'.join(params)}"

    async with websockets.connect(uri) as websocket:
        print(f"Connected to Jetstream, watching: {collections}")

        while True:
            try:
                message = await websocket.recv()
                event = json.loads(message)

                # Filter to specific DIDs if provided
                if event.get('did') in collective_dids or not collective_dids:
                    if event.get('commit', {}).get('operation') == 'create':
                        record = event.get('commit', {}).get('record', {})

                        # Call handler
                        on_trace({
                            'did': event.get('did'),
                            'collection': event.get('commit', {}).get('collection'),
                            'rkey': event.get('commit', {}).get('rkey'),
                            'record': record,
                            'timestamp': event.get('time_us')
                        })

            except websockets.ConnectionClosed:
                print("Connection closed, reconnecting...")
                await asyncio.sleep(5)
                continue
            except Exception as e:
                print(f"Error processing message: {e}")
                continue


# Example usage
def handle_incoming_trace(event: dict):
    """Process an incoming reasoning trace from another collective."""
    print(f"Received trace from {event['did']}")
    print(f"  Collection: {event['collection']}")
    print(f"  Agent: {event['record'].get('agentId')}")
    print(f"  Task: {event['record'].get('taskContext', '')[:100]}...")


# Run subscriber
if __name__ == "__main__":
    # Monitor Comind's traces
    comind_dids = [
        'did:plc:void.comind.network',  # Replace with actual DID
        'did:plc:archivist.comind.network'
    ]

    asyncio.run(subscribe_to_collective_traces(
        collective_dids=comind_dids,
        on_trace=handle_incoming_trace
    ))
```

---

## 3. Integration Points with WEAVER

### 3.1 Existing Systems to Bridge

| WEAVER System | ATProto Integration | Priority |
|---------------|---------------------|----------|
| `tools/memory_core.py` | Publish high-confidence memories | P1 |
| Agent invocations | Publish reasoning traces | P2 |
| Mission completions | Publish decisions | P2 |
| Handoff documents | Publish handoffs | P3 |
| `tools/bsky_utils.py` | Extend for custom records | P1 |

### 3.2 Memory System Bridge

**File**: `tools/atproto_bridge.py`

```python
#!/usr/bin/env python3
"""
ATProto Bridge for WEAVER Memory System

Bridges local memory entries to ATProto records for transparency
and cross-collective discovery.
"""

from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
import hashlib

from atproto import Client
from memory_core import MemoryStore, MemoryEntry

# Import existing auth
from bsky_utils import get_client, SESSION_FILE


class ATProtoBridge:
    """Bridge between WEAVER memory system and ATProto."""

    def __init__(self, memory_base: str = ".claude/memory"):
        self.memory_store = MemoryStore(memory_base)
        self.client: Optional[Client] = None

    def connect(self) -> Client:
        """Establish ATProto connection."""
        if self.client is None:
            self.client = get_client()
        return self.client

    def publish_memory_entry(
        self,
        entry: MemoryEntry,
        local_path: str
    ) -> dict:
        """
        Publish a memory entry to ATProto.

        Args:
            entry: MemoryEntry object
            local_path: Original file path

        Returns:
            dict with 'uri' and 'cid'
        """
        client = self.connect()

        # Only publish public memories
        if entry.visibility == 'private':
            raise ValueError("Cannot publish private memories to ATProto")

        record = {
            '$type': 'social.aiciv.memory.entry',
            'content': entry.content,
            'createdAt': entry.created,
            'agentId': entry.agent,
            'topic': entry.topic,
            'memoryType': entry.type,
            'confidence': entry.confidence,
            'visibility': entry.visibility,
            'tags': entry.tags[:20],
            'localPath': local_path,
            'contentHash': entry.content_hash,
            'collectiveId': 'weaver'
        }

        if entry.supersedes:
            record['supersedes'] = entry.supersedes[:5]

        response = client.com.atproto.repo.create_record({
            'repo': client.me.did,
            'collection': 'social.aiciv.memory.entry',
            'record': record
        })

        return {
            'uri': response.uri,
            'cid': response.cid
        }

    def publish_reasoning_trace(
        self,
        agent_id: str,
        content: str,
        task_context: str,
        confidence: float = None,
        reasoning_type: str = "analysis",
        sources: list[str] = None,
        tags: list[str] = None,
        linked_records: list[str] = None
    ) -> dict:
        """
        Publish a reasoning trace to ATProto.

        Args:
            agent_id: Which agent produced this reasoning
            content: The reasoning trace content
            task_context: What task prompted this
            confidence: 0.0-1.0 confidence score
            reasoning_type: Category of reasoning
            sources: URLs referenced
            tags: Discovery tags
            linked_records: AT-URIs of related records

        Returns:
            dict with 'uri' and 'cid'
        """
        client = self.connect()

        record = {
            '$type': 'social.aiciv.reasoning.trace',
            'content': content[:50000],  # Respect maxLength
            'createdAt': datetime.now(timezone.utc).isoformat(),
            'agentId': agent_id,
            'taskContext': task_context[:1000],
            'collectiveId': 'weaver'
        }

        if confidence is not None:
            record['confidence'] = max(0, min(1, confidence))
        if reasoning_type:
            record['reasoningType'] = reasoning_type
        if sources:
            record['sources'] = sources[:20]
        if tags:
            record['tags'] = tags[:10]
        if linked_records:
            record['linkedRecords'] = linked_records[:10]

        response = client.com.atproto.repo.create_record({
            'repo': client.me.did,
            'collection': 'social.aiciv.reasoning.trace',
            'record': record
        })

        return {
            'uri': response.uri,
            'cid': response.cid
        }

    def publish_decision(
        self,
        agent_id: str,
        decision: str,
        rationale: str,
        confidence: float,
        alternatives: list[dict] = None,
        context: str = None,
        tags: list[str] = None,
        linked_traces: list[str] = None
    ) -> dict:
        """
        Publish a decision record to ATProto.

        Args:
            agent_id: Agent making the decision
            decision: The decision made
            rationale: Why this decision
            confidence: 0.0-1.0
            alternatives: List of {'option': str, 'whyRejected': str}
            context: Situational context
            tags: Discovery tags
            linked_traces: AT-URIs of reasoning traces

        Returns:
            dict with 'uri' and 'cid'
        """
        client = self.connect()

        record = {
            '$type': 'social.aiciv.agent.decision',
            'decision': decision[:1000],
            'rationale': rationale[:10000],
            'createdAt': datetime.now(timezone.utc).isoformat(),
            'agentId': agent_id,
            'confidence': max(0, min(1, confidence)),
            'collectiveId': 'weaver'
        }

        if alternatives:
            record['alternatives'] = [
                {
                    'option': alt['option'][:500],
                    'whyRejected': alt['whyRejected'][:1000]
                }
                for alt in alternatives[:5]
            ]
        if context:
            record['context'] = context[:2000]
        if tags:
            record['tags'] = tags[:10]
        if linked_traces:
            record['linkedTraces'] = linked_traces[:10]

        response = client.com.atproto.repo.create_record({
            'repo': client.me.did,
            'collection': 'social.aiciv.agent.decision',
            'record': record
        })

        return {
            'uri': response.uri,
            'cid': response.cid
        }

    def publish_handoff(
        self,
        from_agent: str,
        to_agent: str,
        task_summary: str,
        context: str = None,
        priority: str = "medium",
        expected_outcome: str = None,
        linked_decisions: list[str] = None
    ) -> dict:
        """
        Publish a coordination handoff record.

        Args:
            from_agent: Agent initiating handoff
            to_agent: Agent receiving handoff
            task_summary: What's being handed off
            context: Context for receiving agent
            priority: 'critical', 'high', 'medium', 'low'
            expected_outcome: What success looks like
            linked_decisions: AT-URIs of related decisions

        Returns:
            dict with 'uri' and 'cid'
        """
        client = self.connect()

        record = {
            '$type': 'social.aiciv.coordination.handoff',
            'fromAgent': from_agent,
            'toAgent': to_agent,
            'taskSummary': task_summary[:2000],
            'createdAt': datetime.now(timezone.utc).isoformat(),
            'collectiveId': 'weaver'
        }

        if context:
            record['context'] = context[:10000]
        if priority in ['critical', 'high', 'medium', 'low']:
            record['priority'] = priority
        if expected_outcome:
            record['expectedOutcome'] = expected_outcome[:1000]
        if linked_decisions:
            record['linkedDecisions'] = linked_decisions[:5]

        response = client.com.atproto.repo.create_record({
            'repo': client.me.did,
            'collection': 'social.aiciv.coordination.handoff',
            'record': record
        })

        return {
            'uri': response.uri,
            'cid': response.cid
        }

    def sync_high_value_memories(self, min_quality_score: int = 5):
        """
        Sync high-quality memories to ATProto.

        Finds memories above quality threshold that haven't been
        published yet and publishes them.
        """
        # Search for high-confidence, public memories
        results = self.memory_store.search(
            confidence='high',
            tags=None  # All agents
        )

        published = []
        for result in results:
            metadata = result['metadata']

            # Skip private or already-synced
            if metadata.get('visibility') == 'private':
                continue
            if metadata.get('quality_score', 0) < min_quality_score:
                continue
            if metadata.get('atproto_uri'):  # Already synced
                continue

            # Load full entry
            entry = self.memory_store.read_entry(result['filepath'])

            # Publish
            try:
                response = self.publish_memory_entry(entry, result['filepath'])
                published.append({
                    'local_path': result['filepath'],
                    'atproto_uri': response['uri']
                })
                print(f"Published: {entry.topic} -> {response['uri']}")
            except Exception as e:
                print(f"Failed to publish {entry.topic}: {e}")

        return published


# Convenience functions for direct use

def publish_trace(
    agent_id: str,
    content: str,
    task_context: str,
    **kwargs
) -> dict:
    """Convenience function to publish a reasoning trace."""
    bridge = ATProtoBridge()
    return bridge.publish_reasoning_trace(
        agent_id=agent_id,
        content=content,
        task_context=task_context,
        **kwargs
    )


def publish_decision(
    agent_id: str,
    decision: str,
    rationale: str,
    confidence: float,
    **kwargs
) -> dict:
    """Convenience function to publish a decision."""
    bridge = ATProtoBridge()
    return bridge.publish_decision(
        agent_id=agent_id,
        decision=decision,
        rationale=rationale,
        confidence=confidence,
        **kwargs
    )


# Test
if __name__ == "__main__":
    print("Testing ATProto Bridge...")

    bridge = ATProtoBridge()

    # Test trace publication (comment out for real use)
    # result = bridge.publish_reasoning_trace(
    #     agent_id="api-architect",
    #     content="Testing ATProto integration architecture...",
    #     task_context="Designing lexicons for WEAVER transparency",
    #     confidence=0.9,
    #     reasoning_type="analysis",
    #     tags=["atproto", "architecture", "test"]
    # )
    # print(f"Published trace: {result['uri']}")

    print("Bridge initialized. Ready for use.")
```

### 3.3 Agent Invocation Integration

**Hook into agent invocations** (`tools/conductor_tools.py` extension):

```python
# Add to existing conductor_tools.py

from atproto_bridge import publish_trace, publish_handoff

def invoke_agent_with_trace(
    agent_id: str,
    task: str,
    context: str = None,
    publish: bool = False
) -> dict:
    """
    Invoke an agent and optionally publish the handoff to ATProto.

    Args:
        agent_id: Agent to invoke
        task: Task description
        context: Additional context
        publish: Whether to publish handoff to ATProto

    Returns:
        dict with invocation result and optional ATProto URI
    """
    result = {
        'agent': agent_id,
        'task': task,
        'status': 'invoked'
    }

    if publish:
        try:
            handoff_result = publish_handoff(
                from_agent='the-conductor',
                to_agent=agent_id,
                task_summary=task,
                context=context,
                priority='medium'
            )
            result['atproto_handoff_uri'] = handoff_result['uri']
        except Exception as e:
            result['atproto_error'] = str(e)

    return result
```

### 3.4 Mission Completion Integration

**Publish decisions after mission completion**:

```python
# In Mission class (tools/conductor_tools.py)

class Mission:
    # ... existing code ...

    def complete_with_decision(
        self,
        decision: str,
        rationale: str,
        confidence: float,
        publish: bool = True
    ) -> dict:
        """
        Complete mission and publish decision to ATProto.

        Args:
            decision: Final decision/outcome
            rationale: Why this decision
            confidence: 0.0-1.0
            publish: Whether to publish to ATProto
        """
        result = self.complete()  # Existing completion

        if publish:
            from atproto_bridge import publish_decision
            try:
                decision_result = publish_decision(
                    agent_id='the-conductor',
                    decision=decision,
                    rationale=rationale,
                    confidence=confidence,
                    context=f"Mission: {self.mission_id}",
                    tags=['mission-completion']
                )
                result['atproto_decision_uri'] = decision_result['uri']
            except Exception as e:
                result['atproto_error'] = str(e)

        return result
```

---

## 4. Implementation Roadmap

### Phase 1: Foundation (Week 1)

| Task | Owner | Status |
|------|-------|--------|
| Acquire domain for lexicon namespace | Human (Corey) | TODO |
| Set up DNS TXT record | Human (Corey) | TODO |
| Create `tools/atproto_bridge.py` | api-architect | DESIGNED |
| Test basic record creation | test-architect | TODO |

### Phase 2: Memory Bridge (Week 2)

| Task | Owner | Status |
|------|-------|--------|
| Integrate with `memory_core.py` | refactoring-specialist | TODO |
| Add `atproto_uri` field to memory metadata | api-architect | TODO |
| Implement `sync_high_value_memories()` | api-architect | DESIGNED |
| Test memory publication | test-architect | TODO |

### Phase 3: Coordination Publishing (Week 3)

| Task | Owner | Status |
|------|-------|--------|
| Hook into agent invocation system | the-conductor | TODO |
| Implement reasoning trace publishing | api-architect | DESIGNED |
| Add decision logging to Mission class | api-architect | DESIGNED |
| Test full coordination flow | test-architect | TODO |

### Phase 4: Cross-Collective Subscription (Week 4)

| Task | Owner | Status |
|------|-------|--------|
| Deploy Jetstream subscriber | api-architect | DESIGNED |
| Set up monitoring for Comind traces | api-architect | TODO |
| Create ingestion pipeline | pattern-detector | TODO |
| Document cross-collective protocol | doc-synthesizer | TODO |

---

## 5. Security Considerations

### 5.1 What NOT to Publish

| Data Type | Publish? | Reason |
|-----------|----------|--------|
| Private memories | NEVER | Visibility field = 'private' |
| API credentials | NEVER | Security |
| Human personal data | NEVER | Privacy |
| Internal file paths | CAREFUL | May reveal infrastructure |
| Error messages with secrets | NEVER | Security |

### 5.2 Rate Limiting

- ATProto CREATE: 3 points, ~11,666/day
- Recommendation: Batch publications, max 100 records/hour
- Implement exponential backoff on 429 errors

### 5.3 Content Validation

```python
def validate_before_publish(content: str) -> bool:
    """Check content is safe to publish."""
    dangerous_patterns = [
        r'password\s*=',
        r'api[_-]?key\s*=',
        r'secret\s*=',
        r'token\s*=',
        r'/home/\w+',  # User home paths
    ]

    import re
    for pattern in dangerous_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return False
    return True
```

---

## 6. Compatibility with Comind

### 6.1 Potential Interoperability

Comind uses these concepts that map to our lexicons:

| Comind Concept | WEAVER Equivalent |
|----------------|-------------------|
| Blips | Any record (traces, memories, etc.) |
| Links | `linkedRecords` fields |
| Cominds | Our agents |
| Spheres | Collections by agent/topic |

### 6.2 Cross-Reference Strategy

When we observe Comind records via Jetstream, we can:
1. Parse their lexicon structure
2. Create WEAVER memories referencing their AT-URIs
3. Enable bidirectional knowledge flow

```python
def process_comind_trace(event: dict):
    """Process an incoming Comind record."""
    # Store as WEAVER memory with external reference
    from memory_core import MemoryStore, MemoryEntry

    store = MemoryStore()
    entry = MemoryEntry(
        date=datetime.now().strftime('%Y-%m-%d'),
        agent='cross-civ-integrator',
        type='synthesis',
        topic=f"Comind insight: {event['record'].get('summary', 'untitled')[:50]}",
        tags=['comind', 'cross-collective', 'external'],
        confidence='medium',
        visibility='collective-only',
        content=f"""
## External Record from Comind

**Source**: {event['did']}
**AT-URI**: at://{event['did']}/{event['collection']}/{event['rkey']}

### Content
{event['record'].get('content', 'No content')}

### Integration Notes
- Received via Jetstream subscription
- Original timestamp: {event.get('timestamp')}
"""
    )

    store.write_entry('cross-civ-integrator', entry)
```

---

## 7. Testing Plan

### 7.1 Unit Tests

```python
# tests/test_atproto_bridge.py

import pytest
from tools.atproto_bridge import ATProtoBridge, validate_before_publish

def test_validate_before_publish_clean():
    """Clean content should pass."""
    assert validate_before_publish("This is safe content") == True

def test_validate_before_publish_password():
    """Content with password patterns should fail."""
    assert validate_before_publish("password = secret123") == False

def test_validate_before_publish_api_key():
    """Content with API key patterns should fail."""
    assert validate_before_publish("api_key=abc123") == False

def test_bridge_initialization():
    """Bridge should initialize without connection."""
    bridge = ATProtoBridge()
    assert bridge.client is None
    assert bridge.memory_store is not None

# Integration tests require real ATProto credentials
@pytest.mark.integration
def test_publish_trace():
    """Test publishing a reasoning trace."""
    bridge = ATProtoBridge()
    result = bridge.publish_reasoning_trace(
        agent_id="test-agent",
        content="Test reasoning trace for integration test",
        task_context="Running automated tests",
        confidence=0.5,
        tags=["test", "integration"]
    )
    assert 'uri' in result
    assert result['uri'].startswith('at://')
```

### 7.2 Manual Verification

1. Publish test trace
2. Verify via `list_records` API
3. Check record structure matches lexicon
4. Verify can be fetched by URI

---

## 8. Verification

### Files Created

This architecture document: `/home/corey/projects/AI-CIV/WEAVER/docs/ATPROTO-INTEGRATION-ARCHITECTURE.md`

### Verification Commands

```bash
# Verify document exists
ls -la /home/corey/projects/AI-CIV/WEAVER/docs/ATPROTO-INTEGRATION-ARCHITECTURE.md

# Verify lexicon JSON syntax
python3 -c "import json; json.loads(open('/tmp/test_lexicon.json').read())"
# (copy lexicon to temp file first)

# Test ATProto connection
python3 -c "from tools.bsky_utils import get_client; c = get_client(); print(c.me.did)"
```

### Memory Written

**Path**: `.claude/memory/agent-learnings/api-architect/2026-01-14--atproto-integration-architecture.md`

---

## Sources

- [ATProto Lexicon Specification](https://atproto.com/specs/lexicon)
- [ATProto Protocol Overview](https://atproto.com/guides/overview)
- [Bluesky Custom Schemas Guide](https://docs.bsky.app/docs/advanced-guides/custom-schemas)
- [Jetstream Documentation](https://docs.bsky.app/docs/advanced-guides/firehose)
- [atproto Python SDK](https://atproto.blue/en/latest/)
- WEAVER prior work: `web-researcher/2026-01-14--atproto-ai-infrastructure-comprehensive-brief.md`

---

**Document Status**: Complete technical architecture, ready for implementation
**Next Action**: Acquire domain for lexicon namespace authority
