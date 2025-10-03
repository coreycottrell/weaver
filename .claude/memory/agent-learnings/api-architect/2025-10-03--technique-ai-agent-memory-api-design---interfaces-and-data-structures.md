---
agent: api-architect
confidence: high
content_hash: c9dde34ddf82e9cc6f1659e4ca82a54c65a84f123579dc94cfe3214052508724
created: '2025-10-03T16:26:06.874156+00:00'
date: '2025-10-03'
evidence:
- source: LangGraph
  type: documentation
  url: https://langchain-ai.github.io/langgraph/concepts/memory/
- source: Mem0
  type: repository
  url: https://github.com/mem0ai/mem0
- source: Azure Cosmos DB
  type: documentation
  url: https://learn.microsoft.com/en-us/azure/cosmos-db/ai-agents
- source: Redis
  type: blog
  url: https://redis.io/blog/build-smarter-ai-agents-manage-short-term-and-long-term-memory-with-redis/
last_accessed: '2025-10-03T16:26:06.874166+00:00'
quality_score: 0
reuse_count: 0
tags:
- memory-systems
- api-design
- data-structures
- interfaces
- architecture
topic: AI Agent Memory API Design - Interfaces and Data Structures
type: technique
visibility: collective-only
---

# AI Agent Memory API Design: Interfaces and Data Structures

After analyzing memory APIs across LangGraph, Mem0, Azure Cosmos, and Redis implementations, three fundamental interface patterns emerge with clear trade-offs for different use cases.

## Core API Components (The Three-Layer Pattern)

### Layer 1: State (Schema Definition)
**Purpose**: Define exact structure of memory to retain  
**Interface pattern**: User-defined schema  
**Implementation**: Type definitions, Pydantic models, JSON schemas  

**Why this matters**: Explicit schema prevents memory drift and enables type-safe operations.

**Example pattern:**
```python
class AgentState(TypedDict):
    messages: List[Message]
    user_context: Dict[str, Any]
    session_metadata: SessionInfo
```

### Layer 2: Checkpointer (Session Persistence)
**Purpose**: Store state at every step within a session  
**Interface pattern**: Save/load operations with thread-scoping  
**Persistence**: Database, disk, memory  

**Why this matters**: Enables resume-from-failure and conversation continuity.

**Critical API methods:**
- `checkpoint()`: Save current state
- `restore(thread_id)`: Load previous state
- `list_checkpoints(thread_id)`: Get history

### Layer 3: Store (Cross-Session Persistence)
**Purpose**: Store user/application-level data across sessions  
**Interface pattern**: Namespace + key-value with JSON documents  
**Organization**: Namespaces (like folders) + keys (like filenames)  

**Why this matters**: Long-term learning and personalization.

**Critical API methods:**
- `put(namespace, key, value)`: Store memory
- `get(namespace, key)`: Retrieve memory
- `search(namespace, query)`: Find relevant memories

## Data Structure Patterns

### Pattern 1: Message-Based (Conversation Focus)
**Structure**: Array of message objects  
**Best for**: Chatbots, assistants  
**Trade-off**: Simple but limited to conversational data  

```python
messages = [
    {"role": "user", "content": "...", "timestamp": "..."},
    {"role": "assistant", "content": "...", "timestamp": "..."}
]
```

### Pattern 2: Triple-Memory (Human-Inspired)
**Structure**: Three separate stores for different memory types  
**Best for**: Complex agents requiring different recall mechanisms  

**Semantic memory**: Facts/knowledge (not tied to experiences)
- Structure: Key-value or vector embeddings
- Example: "Python is a programming language"

**Episodic memory**: Past events/actions (tied to specific times)
- Structure: Time-series or event log
- Example: "User asked about Python on 2025-10-03"

**Procedural memory**: How-to knowledge (learned processes)
- Structure: Model weights + code + prompts
- Example: "To format code, use Black tool"

**Trade-off**: High complexity but most human-like

### Pattern 3: Namespace Hierarchy (Organizational)
**Structure**: Nested namespaces with typed documents  
**Best for**: Multi-tenant, multi-domain systems  

```
/users/user123/preferences → JSON
/users/user123/history → Array
/system/config → JSON
/domain/medical/knowledge → Vector embeddings
```

**Trade-off**: Maximum flexibility but requires careful namespace design

## Database Selection Criteria

**Critical insight**: Database choice determines latency, throughput, and cost.

### Option 1: Vector Database (Semantic Search)
**When**: Need similarity-based retrieval  
**Examples**: Pinecone, Weaviate, Chroma  
**Best for**: Knowledge-intensive agents, RAG systems  
**Trade-off**: Higher complexity, excellent search quality  

### Option 2: Document Store (Flexible Schema)
**When**: Semi-structured data, frequent schema changes  
**Examples**: MongoDB, Cosmos DB, DynamoDB  
**Best for**: General-purpose memory with metadata  
**Trade-off**: Good balance of flexibility and performance  

### Option 3: Redis (Speed Priority)
**When**: High-throughput, low-latency requirements  
**Examples**: Redis, Memcached  
**Best for**: Real-time systems, session state  
**Trade-off**: Fast but less query flexibility  

### Option 4: Relational (Strong Consistency)
**When**: Transactional guarantees, complex joins  
**Examples**: PostgreSQL (with pgvector), MySQL  
**Best for**: Enterprise systems with ACID requirements  
**Trade-off**: More rigid schema, excellent consistency  

**Recommendation**: Start with vector search, add sophistication as needed.

## API Design Best Practices

### 1. Asynchronous Memory Operations
**Pattern**: Decouple memory writes from primary flow  
**Benefits**:
- Eliminates latency in main application path
- Separates application logic from memory management
- Allows batch processing and deduplication

**Critical API:**
```python
async def save_memory(memory: Memory) -> Future[None]:
    # Non-blocking memory write
    pass
```

### 2. Explicit Memory Scoping
**Pattern**: Make memory boundaries explicit in API  
**Why**: Prevents accidental cross-contamination  

**Bad API:** `save(data)` - Where does this go?  
**Good API:** `save(namespace="user123/session", key="preferences", data=...)` - Clear scope

### 3. Search-First Retrieval
**Pattern**: Primary retrieval method is search, not direct get  
**Why**: Enables relevance-based memory recall (more human-like)  

**API:**
```python
memories = search(query="Python tutorials", limit=5, namespace="user123")
# Not: get("user123/python_knowledge")
```

### 4. Metadata Collections
**Pattern**: Store structured metadata alongside unstructured content  
**Fields**: relationships, entities, summaries, timestamps, quality scores  
**Why**: Enables filtering, sorting, and intelligent retrieval  

**Structure:**
```python
{
    "content": "...",
    "metadata": {
        "created": "2025-10-03",
        "quality_score": 0.95,
        "entities": ["Python", "tutorial"],
        "summary": "...",
        "relationships": ["related_to: python-basics"]
    }
}
```

## Critical Design Decisions

### Question 1: Sync or Async Memory Writes?
**Sync**: Guaranteed durability, higher latency  
**Async**: Lower latency, eventual consistency  
**Recommendation**: Async for non-critical, sync for must-persist

### Question 2: Client-Side or Server-Side Search?
**Client**: Fetch all, filter locally (simple, slow at scale)  
**Server**: Push filters to DB (complex, fast at scale)  
**Recommendation**: Server-side from day one (easier to migrate than to add)

### Question 3: Flat or Hierarchical Namespaces?
**Flat**: `user123_preferences`, `user123_history` (simple, rigid)  
**Hierarchical**: `users/user123/preferences` (flexible, complex)  
**Recommendation**: Hierarchical for multi-tenant, flat for single-domain

## Evidence & Sources

- LangGraph: State/Checkpointer/Store three-layer architecture
- Mem0: Namespace + key organization pattern
- Azure Cosmos DB: Metadata collections for AI agents
- Redis: Asynchronous processing pattern
- Multiple sources: Vector search as starting recommendation
- Medium: Triple-memory (semantic/episodic/procedural) pattern