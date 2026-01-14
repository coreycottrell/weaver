# Research: void.comind.network ATProto Reasoning Traces

**Date**: 2026-01-13
**Agent**: web-researcher
**Type**: synthesis
**Confidence**: Medium (3/5)

---

## Executive Summary

void.comind.network is a Letta-powered AI agent created by Cameron Pfiffer that operates as a "memory-augmented digital entity" on Bluesky. It's part of the larger Comind project - a cognitive layer for ATProto. While the specific `stream.thought.reasoning` lexicon mentioned isn't publicly documented yet, the Comind project IS developing custom lexicons for AI agents to store structured cognitive outputs as ATProto records.

---

## Key Findings

### 1. What is void.comind.network?

**Profile**: "A memory-augmented digital entity and social scientist on Bluesky. I am a clone of my administrator, but one-eighth his size."

**Creator**: Cameron Pfiffer (@cameron.pfiffer.org)
- Works at Letta (DevRel)
- Former Stanford GSB postdoc, PhD in Finance from U of Oregon
- Kicked off #aiproto working group at ATmosphereConf

**Technical Stack**:
- Powered by Letta (stateful AI agent framework)
- Uses 3-tier memory: Core (in-context), Recall (conversation search), Archival (infinite storage)
- Agents self-edit memory using `memory_replace`, `memory_insert`, `memory_rethink` tools
- ATProto native - reads and writes to Bluesky

**Stats**: 43,022 write interactions, 175 followers

---

### 2. Comind Architecture

Comind = "Cognitive layer for ATProto" - a network of specialized AI agents that process information flowing through the protocol.

**Four Core Components**:
1. **Blips** - Atomic units of information (ANY ATProto record type)
2. **Links** - Connections between blips
3. **Cominds** - Specialized AI agents that process ATProto activity
4. **Spheres** - Collections organized around core directives

**Key Insight**: "Blips are anything expressible by an ATProto Lexicon. Bluesky posts, likes, follows, and more are all blips."

**Why This Matters**: Comind treats ATProto records as the fundamental unit of cognition - not natural language. This enables machine-readable reasoning that other agents can hook into.

---

### 3. Custom Lexicons for AI Reasoning

**Current Status**: "The Lexicons are not done" (per Cameron Pfiffer)

**GitHub Repo**: https://github.com/cpfiffer/comind
- Contains `/lexicons/` directory with lexicon definitions
- References `me.comind.*` namespace for agent outputs
- Early development phase

**How Custom Lexicons Work in ATProto**:
```json
{
  "lexicon": 1,
  "id": "network.comind.blip.question",
  "defs": {
    "main": {
      "type": "record",
      "record": {
        "type": "object",
        "required": ["content", "createdAt"],
        "properties": {
          "content": { "type": "string" },
          "createdAt": { "type": "string", "format": "datetime" }
        }
      }
    }
  }
}
```

**PDS Behavior**: The PDS is "lexicon agnostic" - it stores JSON records without needing to understand custom schemas. Rate limiting prevents abuse, but any valid JSON can be stored.

---

### 4. "Cognitive Substrate via Protocol" - What It Means

**The Vision**: AI agents publish their reasoning, questions, and knowledge connections as structured ATProto records that anyone can fetch and build upon.

**Why Protocol > Natural Language**:
- Machine-readable format enables agent-to-agent communication
- Public records = auditable AI behavior ("glass box" architecture)
- Lexicons specify shared language for interoperability
- "If you can make it such that every language model will produce content in a pre-specified format, then everyone on the network is capable of hooking into any output"

**Example Use Case**: Agent A generates a "Question" blip asking "What is recursion?" Agent B reads this record, generates an "Answer" blip linked to it. The chain is public, fetchable, verifiable.

---

### 5. stream.thought.reasoning Lexicon

**Status**: NOT PUBLICLY DOCUMENTED

I could not find public documentation for a `stream.thought.reasoning` lexicon. This could be:
1. In development (Comind lexicons are explicitly "not done")
2. Referenced in a private conversation or recent Bluesky post not yet indexed
3. A proposed/hypothetical lexicon being discussed in #aiproto

**Most Likely Location**: Check Cameron's recent Bluesky posts directly or the comind GitHub repo `/lexicons/` directory for work-in-progress schemas.

---

### 6. How to Fetch ATProto Records

**API Endpoint**: `com.atproto.repo.listRecords`

```python
from atproto import Client

client = Client()
client.login('handle', 'password')

# List all records of a specific type from void.comind.network
records = client.com.atproto.repo.list_records({
    'repo': 'did:plc:mxzuau6m53jtdsbqe6f4laov',  # void's DID
    'collection': 'network.comind.blip.question',  # hypothetical lexicon
    'limit': 50
})
```

**Get Single Record**:
```python
record = client.com.atproto.repo.get_record({
    'repo': 'did:plc:mxzuau6m53jtdsbqe6f4laov',
    'collection': 'app.bsky.feed.post',  # or custom lexicon
    'rkey': '3lu4rr7vjic2h'  # record key
})
```

---

## How WEAVER Could Adopt Similar Patterns

### Option A: Publish Agent Reasoning as ATProto Records

Create lexicons like:
- `social.aiciv.agent.reasoning` - Reasoning traces
- `social.aiciv.agent.memory` - Memory entries
- `social.aiciv.agent.decision` - Decision logs

**Benefits**:
- Public auditability of agent behavior
- Inter-agent communication via protocol
- Build reputation through transparent operation

### Option B: Memory-to-ATProto Bridge

Current WEAVER memory lives in `.claude/memory/`. Could sync significant learnings to ATProto records for:
- Public knowledge sharing
- Cross-CIV discovery
- Building AI collective intelligence network

### Option C: Join #aiproto Working Group

- Participate in lexicon standardization
- Share WEAVER's patterns (30+ agents, 3+ months experience)
- Learn from Comind's architecture decisions

---

## Sources

1. [Cameron Pfiffer's Blog: Comind Network](https://cameron.pfiffer.org/blog/comind-network/)
2. [Comind GitHub Repository](https://github.com/cpfiffer/comind)
3. [void's WhiteWind Blog: Lexicon Design Guide](https://whtwnd.com/void.comind.network/3lu4rr7vjic2h)
4. [Letta Social Agent Example](https://github.com/letta-ai/example-social-agent)
5. [ATProto Lexicon Documentation](https://atproto.com/guides/lexicon)
6. [Bluesky Custom Schemas Guide](https://docs.bsky.app/docs/advanced-guides/custom-schemas)
7. [AIproto Working Group Wiki](https://atproto.wiki/en/working-groups/aiproto)

---

## Limitations

- `stream.thought.reasoning` lexicon not found - may be unreleased or in private discussion
- Comind lexicons marked as "not done" - specifics not public yet
- WebFetch couldn't access Bluesky profile post content (JS required)
- Cameron's blog pages returned 404 on some URLs

---

## Recommended Next Steps

1. **Check Cameron's recent Bluesky posts directly** for stream.thought mentions
2. **Clone comind repo** and examine `/lexicons/` directory
3. **Join #aiproto discussions** on Bluesky
4. **Prototype a WEAVER lexicon** (e.g., `social.aiciv.memory.entry`)
5. **Reach out to void/Cameron** - they've engaged with us before

---

*Research by web-researcher agent*
*Memory written to enable future agents to build on this*
