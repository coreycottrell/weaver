# API Architect: ADR-018 RAG Memory System - MCP Server Design Review

**Agent**: api-architect
**Domain**: MCP Server Interface Design, Error Handling, API Completeness
**Date**: 2025-12-30
**Reviewer**: WEAVER API Architect (Red Team)
**Source Document**: `/home/corey/projects/AI-CIV/ACG/sandbox/futures/ADR-018-rag-memory-working-proposal.md`

---

## Executive Summary

The ADR-018 proposal presents a solid foundation for a RAG memory MCP server. The core architecture is sound - local-only ChromaDB, BGE embeddings, receipt-based quality gates. However, the MCP server skeleton has several gaps that need addressing before production deployment.

**Overall Assessment**: 7/10 - Good foundation, needs hardening

**Critical Gaps Identified**:
1. Missing essential MCP tools (health, stats, delete, update)
2. No error handling or graceful degradation
3. No rate limiting or resource protection
4. Query API missing pagination
5. Verify API quality gates incomplete

---

## 1. MCP Server Tool Interface - Completeness Analysis

### Current Tools (4 defined)
| Tool | Purpose | Status |
|------|---------|--------|
| `store_memory` | Store new memory | Implemented |
| `query_memory` | Semantic search | Implemented |
| `verify_receipt` | Promote pending->verified | Implemented |
| `list_pending` | List unverified memories | Implemented |

### Missing Essential Tools

#### 1.1 Health Check Tool (CRITICAL)
```python
@app.tool()
async def health_check() -> dict:
    """Check MCP server health and dependencies."""
    health = {
        "server": "ok",
        "chromadb": "unknown",
        "embedder": "unknown",
        "storage_path": STORAGE_PATH,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    try:
        # Test ChromaDB connection
        count = collection.count()
        health["chromadb"] = "ok"
        health["memory_count"] = count
    except Exception as e:
        health["chromadb"] = f"error: {str(e)}"

    try:
        # Test embedder
        test_embedding = embedder.encode("health check")
        health["embedder"] = "ok"
        health["embedding_dim"] = len(test_embedding)
    except Exception as e:
        health["embedder"] = f"error: {str(e)}"

    health["healthy"] = (
        health["chromadb"] == "ok" and
        health["embedder"] == "ok"
    )

    return health
```

**Why needed**: Session startup should verify server health before relying on memories. Without this, silent failures could cause confusing behavior.

#### 1.2 Statistics Tool (RECOMMENDED)
```python
@app.tool()
async def get_stats() -> dict:
    """Get memory system statistics."""
    total = collection.count()

    # Count by status
    verified = len(collection.get(where={"status": "verified"})["ids"])
    pending = len(collection.get(where={"status": "pending"})["ids"])

    # Count by category
    categories = {}
    for cat in ["pattern", "bug-fix", "dead-end", "synthesis", "uncategorized"]:
        try:
            categories[cat] = len(collection.get(where={"category": cat})["ids"])
        except:
            categories[cat] = 0

    return {
        "total_memories": total,
        "verified": verified,
        "pending": pending,
        "by_category": categories,
        "storage_path": STORAGE_PATH,
        "civilization": CIV,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
```

**Why needed**: Observability for debugging, dashboards, and understanding system state.

#### 1.3 Delete Tool (RECOMMENDED)
```python
@app.tool()
async def delete_memory(
    memory_id: str,
    reason: str = "manual_deletion"
) -> dict:
    """Delete a memory by ID (soft delete recommended)."""

    # Check if memory exists
    result = collection.get(ids=[memory_id])
    if not result["ids"]:
        return {"error": f"Memory {memory_id} not found"}

    # Option 1: Hard delete
    # collection.delete(ids=[memory_id])

    # Option 2: Soft delete (recommended - maintains audit trail)
    metadata = result["metadatas"][0]
    metadata["status"] = "deleted"
    metadata["deleted_at"] = datetime.utcnow().isoformat() + "Z"
    metadata["deletion_reason"] = reason

    collection.update(ids=[memory_id], metadatas=[metadata])

    return {"memory_id": memory_id, "status": "deleted", "reason": reason}
```

**Why needed**: Ability to remove bad/incorrect memories. Soft delete preserves audit trail.

#### 1.4 Update Tool (RECOMMENDED)
```python
@app.tool()
async def update_memory(
    memory_id: str,
    summary: str = None,
    category: str = None,
    references: list[str] = None
) -> dict:
    """Update memory metadata (not content - content is immutable)."""

    result = collection.get(ids=[memory_id], include=["metadatas"])
    if not result["ids"]:
        return {"error": f"Memory {memory_id} not found"}

    metadata = result["metadatas"][0]

    if summary:
        metadata["summary"] = summary
    if category:
        metadata["category"] = category
    if references:
        metadata["references"] = json.dumps(references)

    metadata["updated_at"] = datetime.utcnow().isoformat() + "Z"

    collection.update(ids=[memory_id], metadatas=[metadata])

    return {"memory_id": memory_id, "updated_fields": [k for k in [summary, category, references] if k]}
```

**Why needed**: Ability to correct categorization, improve summaries without deleting/recreating.

#### 1.5 Get Single Memory Tool (RECOMMENDED)
```python
@app.tool()
async def get_memory(memory_id: str) -> dict:
    """Retrieve a single memory by ID with full content."""

    result = collection.get(
        ids=[memory_id],
        include=["documents", "metadatas"]
    )

    if not result["ids"]:
        return {"error": f"Memory {memory_id} not found"}

    return {
        "id": memory_id,
        "content": result["documents"][0],
        "metadata": result["metadatas"][0]
    }
```

**Why needed**: Direct access to specific memory when ID is known.

---

## 2. Error Handling Analysis

### Current State: No Error Handling

The skeleton has **zero try/except blocks**. This is a critical gap.

### Recommended Error Handling Pattern

```python
from enum import Enum
from dataclasses import dataclass

class ErrorCode(Enum):
    CHROMADB_CONNECTION = "E001"
    CHROMADB_QUERY = "E002"
    EMBEDDER_LOAD = "E003"
    EMBEDDER_ENCODE = "E004"
    MEMORY_NOT_FOUND = "E101"
    DUPLICATE_MEMORY = "E102"
    QUALITY_GATE_FAILED = "E103"
    INVALID_CATEGORY = "E104"
    CONTENT_TOO_SHORT = "E105"
    CONTENT_TOO_LONG = "E106"

@dataclass
class MCPError:
    code: str
    message: str
    recoverable: bool
    suggestion: str = None

def handle_error(error: Exception, operation: str) -> dict:
    """Standardized error response format."""

    error_map = {
        "chromadb.errors.InvalidCollectionException": MCPError(
            ErrorCode.CHROMADB_CONNECTION.value,
            "Collection not found or corrupted",
            recoverable=True,
            suggestion="Try recreating collection or restoring from backup"
        ),
        # Add more mappings...
    }

    error_type = type(error).__module__ + "." + type(error).__name__
    mcp_error = error_map.get(error_type, MCPError(
        "E999",
        str(error),
        recoverable=False
    ))

    return {
        "error": True,
        "code": mcp_error.code,
        "message": mcp_error.message,
        "operation": operation,
        "recoverable": mcp_error.recoverable,
        "suggestion": mcp_error.suggestion,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
```

### Apply to Each Tool

```python
@app.tool()
async def store_memory(content: str, source: str, session_id: str, ...) -> dict:
    """Store a new memory in pending state."""

    # Input validation
    if len(content) < 50:
        return handle_error(ValueError("Content too short"), "store_memory")
    if len(content) > 10000:
        return handle_error(ValueError("Content too long"), "store_memory")

    try:
        memory_id = f"{CIV}_{session_id}_{hash(content)}"

        # Check for duplicates
        existing = collection.get(ids=[memory_id])
        if existing["ids"]:
            return {
                "error": True,
                "code": "E102",
                "message": "Duplicate memory ID",
                "existing_id": memory_id
            }

        collection.add(
            ids=[memory_id],
            documents=[content],
            metadatas=[{...}]
        )

        return {"memory_id": memory_id, "status": "pending"}

    except Exception as e:
        return handle_error(e, "store_memory")
```

---

## 3. Query API Design Improvements

### Current Issues

1. **No pagination** - Returns all results up to limit, no way to get "next page"
2. **No sorting options** - Only sorted by similarity
3. **No date range filtering** - Can't query "memories from last week"
4. **No multi-field search** - Only semantic search on content

### Improved Query API

```python
@app.tool()
async def query_memory(
    # Semantic search
    query: str = None,

    # Pagination
    limit: int = 10,
    offset: int = 0,

    # Filtering
    min_similarity: float = 0.7,
    status: str = "verified",
    category: str = None,
    source: str = None,

    # Date range
    created_after: str = None,  # ISO format
    created_before: str = None,

    # Sorting
    sort_by: str = "similarity",  # similarity, created_at, relevance
    sort_order: str = "desc",

    # Search mode
    search_mode: str = "semantic"  # semantic, keyword, hybrid
) -> dict:
    """
    Query memories with flexible filtering and pagination.

    Args:
        query: Search query (required for semantic/hybrid, optional for keyword)
        limit: Max results to return (default 10, max 100)
        offset: Skip first N results for pagination
        min_similarity: Minimum cosine similarity threshold (0.0-1.0)
        status: Filter by status (verified, pending, all)
        category: Filter by category (pattern, bug-fix, dead-end, synthesis)
        source: Filter by source agent
        created_after: Only memories created after this ISO timestamp
        created_before: Only memories created before this ISO timestamp
        sort_by: Sort field (similarity, created_at)
        sort_order: Sort direction (asc, desc)
        search_mode: Search type (semantic, keyword, hybrid)

    Returns:
        {
            "memories": [...],
            "total_count": N,
            "returned_count": N,
            "offset": N,
            "has_more": bool,
            "query_time_ms": N
        }
    """
    import time
    start_time = time.time()

    # Validate inputs
    limit = min(limit, 100)  # Cap at 100

    # Build where filter
    where_filter = {}
    if status != "all":
        where_filter["status"] = status
    if category:
        where_filter["category"] = category
    if source:
        where_filter["source"] = source

    # Date filtering requires ChromaDB where_document or post-filtering
    # ChromaDB's where only supports metadata fields

    try:
        if search_mode == "semantic" and query:
            results = collection.query(
                query_texts=[query],
                n_results=limit + offset,  # Get enough for pagination
                where=where_filter if where_filter else None,
                include=["documents", "metadatas", "distances"]
            )

            # Apply offset
            memories = []
            for i in range(offset, min(len(results["documents"][0]), offset + limit)):
                doc = results["documents"][0][i]
                similarity = 1 - results["distances"][0][i]

                if similarity >= min_similarity:
                    memories.append({
                        "id": results["ids"][0][i],
                        "content": doc,
                        "metadata": results["metadatas"][0][i],
                        "similarity": round(similarity, 4)
                    })

        elif search_mode == "keyword":
            # ChromaDB doesn't have native keyword search
            # Would need to implement via metadata or external index
            return {"error": "Keyword search not yet implemented"}

        else:
            # No query - just filter
            results = collection.get(
                where=where_filter if where_filter else None,
                limit=limit,
                offset=offset,
                include=["documents", "metadatas"]
            )

            memories = [
                {
                    "id": id,
                    "content": doc,
                    "metadata": meta,
                    "similarity": None
                }
                for id, doc, meta in zip(
                    results["ids"],
                    results["documents"],
                    results["metadatas"]
                )
            ]

        query_time = int((time.time() - start_time) * 1000)

        return {
            "memories": memories,
            "total_count": collection.count(),  # Approximate
            "returned_count": len(memories),
            "offset": offset,
            "has_more": len(memories) == limit,
            "query_time_ms": query_time
        }

    except Exception as e:
        return handle_error(e, "query_memory")
```

---

## 4. Store API Design - Metadata Completeness

### Current Metadata Fields
- source
- session_id
- category
- summary
- references
- status
- created_at

### Missing/Recommended Metadata Fields

```python
metadatas=[{
    # Current fields
    "source": source,
    "session_id": session_id,
    "category": category,
    "summary": summary or content[:200],
    "references": json.dumps(references or []),
    "status": "pending",
    "created_at": datetime.utcnow().isoformat() + "Z",

    # RECOMMENDED ADDITIONS

    # Identity
    "civilization": CIV,
    "schema_version": "1.0",

    # Source context
    "agent_id": agent_id,  # Which agent created this
    "task_id": task_id,    # What task spawned this
    "file_path": file_path,  # If from file operation

    # Quality metrics
    "content_length": len(content),
    "word_count": len(content.split()),
    "embedding_model": "bge-large-en-v1.5",

    # Access tracking
    "access_count": 0,
    "last_accessed_at": None,

    # TTL support
    "expires_at": None,  # For pending memories with TTL

    # Linking
    "parent_memory_id": None,  # If this is derived from another
    "related_memory_ids": json.dumps([]),
}]
```

### Improved Store Function Signature

```python
@app.tool()
async def store_memory(
    # Required
    content: str,
    source: str,
    session_id: str,

    # Strongly recommended
    agent_id: str = None,
    task_id: str = None,

    # Quality metadata
    category: str = "uncategorized",
    summary: str = None,
    references: list[str] = None,

    # Context
    file_path: str = None,
    parent_memory_id: str = None,

    # Optional overrides
    expires_at: str = None,  # ISO timestamp for TTL
    skip_duplicate_check: bool = False
) -> dict:
```

---

## 5. Verify API - Quality Gate Implementation

### Current Quality Gates
1. Summary length > 50 chars
2. Category != "uncategorized"

### Missing Quality Gates

```python
def quality_check(memory_id: str, metadata: dict, content: str) -> tuple[bool, list[str]]:
    """
    Comprehensive quality gate check.
    Returns (passed, list_of_failures)
    """
    failures = []

    # 1. Summary quality
    summary = metadata.get("summary", "")
    if len(summary) < 50:
        failures.append("Summary too short (min 50 chars)")
    if len(summary) > 500:
        failures.append("Summary too long (max 500 chars)")
    if summary == content[:len(summary)]:
        failures.append("Summary is just truncated content - needs actual summarization")

    # 2. Category validation
    valid_categories = ["pattern", "bug-fix", "dead-end", "synthesis", "technique", "gotcha"]
    category = metadata.get("category", "uncategorized")
    if category == "uncategorized":
        failures.append("Category required")
    elif category not in valid_categories:
        failures.append(f"Invalid category '{category}'. Valid: {valid_categories}")

    # 3. Content quality
    if len(content) < 50:
        failures.append("Content too short (min 50 chars)")
    if len(content) > 10000:
        failures.append("Content too long (max 10000 chars)")

    # 4. Reference check (warning, not failure)
    references = json.loads(metadata.get("references", "[]"))
    # This is recommended, not required

    # 5. Duplicate detection
    similar = collection.query(
        query_texts=[content],
        n_results=1,
        where={"status": "verified"}
    )
    if similar["distances"] and similar["distances"][0]:
        similarity = 1 - similar["distances"][0][0]
        if similarity > 0.95:
            failures.append(f"Near-duplicate exists (similarity: {similarity:.2f})")

    # 6. Source validation
    if not metadata.get("source"):
        failures.append("Source agent required")

    return (len(failures) == 0, failures)


@app.tool()
async def verify_receipt(
    memory_id: str,
    verified_by: str,
    verification_type: str = "manual",
    force: bool = False  # Skip quality gates
) -> dict:
    """Verify a pending memory, making it searchable."""

    try:
        # Get current memory
        result = collection.get(
            ids=[memory_id],
            include=["metadatas", "documents"]
        )

        if not result["ids"]:
            return {"error": f"Memory {memory_id} not found", "code": "E101"}

        metadata = result["metadatas"][0]
        content = result["documents"][0]

        # Already verified?
        if metadata.get("status") == "verified":
            return {"error": "Memory already verified", "memory_id": memory_id}

        # Quality check
        if not force:
            passed, failures = quality_check(memory_id, metadata, content)
            if not passed:
                return {
                    "error": "Quality gates failed",
                    "memory_id": memory_id,
                    "failures": failures,
                    "suggestion": "Fix issues or use force=True to bypass"
                }

        # Update status
        metadata["status"] = "verified"
        metadata["verified_by"] = verified_by
        metadata["verified_at"] = datetime.utcnow().isoformat() + "Z"
        metadata["verification_type"] = verification_type

        collection.update(ids=[memory_id], metadatas=[metadata])

        return {
            "memory_id": memory_id,
            "status": "verified",
            "verified_by": verified_by,
            "quality_bypassed": force
        }

    except Exception as e:
        return handle_error(e, "verify_receipt")
```

---

## 6. Rate Limiting / Resource Protection

### Current State: None

No protection against:
- Query floods
- Large content submissions
- Connection exhaustion

### Recommended Implementation

```python
from collections import defaultdict
from datetime import datetime, timedelta
import threading

class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = threading.Lock()

        # Limits per operation per minute
        self.limits = {
            "store_memory": 30,
            "query_memory": 60,
            "verify_receipt": 20,
            "list_pending": 30,
            "health_check": 10,
            "get_stats": 10,
        }

    def check(self, operation: str, client_id: str = "default") -> tuple[bool, dict]:
        """Check if request is allowed. Returns (allowed, info)."""

        with self.lock:
            key = f"{client_id}:{operation}"
            now = datetime.now()
            minute_ago = now - timedelta(minutes=1)

            # Clean old requests
            self.requests[key] = [
                t for t in self.requests[key]
                if t > minute_ago
            ]

            limit = self.limits.get(operation, 60)
            current = len(self.requests[key])

            if current >= limit:
                return False, {
                    "error": "Rate limit exceeded",
                    "operation": operation,
                    "limit": limit,
                    "window": "1 minute",
                    "retry_after_seconds": 60 - (now - self.requests[key][0]).seconds
                }

            self.requests[key].append(now)
            return True, {"remaining": limit - current - 1}

rate_limiter = RateLimiter()

# Apply to tools
@app.tool()
async def query_memory(...) -> dict:
    allowed, info = rate_limiter.check("query_memory")
    if not allowed:
        return info

    # ... rest of implementation
```

### Content Size Limits

```python
MAX_CONTENT_SIZE = 10000  # characters
MAX_QUERY_SIZE = 1000     # characters
MAX_RESULTS = 100         # per query

@app.tool()
async def store_memory(content: str, ...) -> dict:
    if len(content) > MAX_CONTENT_SIZE:
        return {
            "error": "Content exceeds maximum size",
            "max_size": MAX_CONTENT_SIZE,
            "actual_size": len(content)
        }
    # ...

@app.tool()
async def query_memory(query: str, limit: int, ...) -> dict:
    if len(query) > MAX_QUERY_SIZE:
        return {"error": "Query too long", "max": MAX_QUERY_SIZE}

    limit = min(limit, MAX_RESULTS)
    # ...
```

---

## 7. Graceful Degradation if ChromaDB Fails

### Current State: Server crashes on ChromaDB failure

The server initializes ChromaDB at module load time:
```python
chroma_client = chromadb.PersistentClient(path=STORAGE_PATH)
collection = chroma_client.get_or_create_collection(...)
```

If ChromaDB fails, the server won't start.

### Recommended: Lazy Initialization + Fallback

```python
class ChromaDBWrapper:
    """Wrapper with lazy init and graceful degradation."""

    def __init__(self, storage_path: str, civ: str):
        self.storage_path = storage_path
        self.civ = civ
        self._client = None
        self._collection = None
        self._embedder = None
        self._healthy = False
        self._last_error = None
        self._fallback_mode = False

        # Fallback: in-memory recent queries cache
        self._cache = []
        self._cache_max = 100

    def _init_chromadb(self) -> bool:
        """Attempt to initialize ChromaDB."""
        try:
            self._client = chromadb.PersistentClient(path=self.storage_path)
            self._collection = self._client.get_or_create_collection(
                name=f"{self.civ}_memories",
                metadata={"hnsw:space": "cosine"}
            )
            self._healthy = True
            self._fallback_mode = False
            return True
        except Exception as e:
            self._last_error = str(e)
            self._healthy = False
            self._fallback_mode = True
            return False

    def _init_embedder(self) -> bool:
        """Attempt to initialize embedder."""
        try:
            self._embedder = SentenceTransformer('BAAI/bge-large-en-v1.5')
            return True
        except Exception as e:
            self._last_error = str(e)
            return False

    @property
    def collection(self):
        if not self._collection:
            self._init_chromadb()
        return self._collection

    @property
    def embedder(self):
        if not self._embedder:
            self._init_embedder()
        return self._embedder

    def query(self, query_text: str, limit: int, **kwargs) -> dict:
        """Query with fallback to cache if ChromaDB unavailable."""

        if not self._healthy:
            # Attempt reconnection
            self._init_chromadb()

        if self._healthy and self.collection:
            try:
                return self.collection.query(
                    query_texts=[query_text],
                    n_results=limit,
                    **kwargs
                )
            except Exception as e:
                self._healthy = False
                self._last_error = str(e)

        # Fallback: return from cache with simple matching
        if self._fallback_mode:
            return {
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
                "ids": [[]],
                "_fallback": True,
                "_error": self._last_error
            }

        return {"documents": [[]], "metadatas": [[]], "distances": [[]], "ids": [[]]}

    def add(self, **kwargs) -> dict:
        """Add with fallback to queue if ChromaDB unavailable."""

        if not self._healthy:
            self._init_chromadb()

        if self._healthy and self.collection:
            try:
                self.collection.add(**kwargs)
                return {"success": True}
            except Exception as e:
                self._healthy = False
                self._last_error = str(e)

        # Fallback: queue for later
        if self._fallback_mode:
            self._cache.append({
                "operation": "add",
                "kwargs": kwargs,
                "timestamp": datetime.utcnow().isoformat()
            })
            # Trim cache
            if len(self._cache) > self._cache_max:
                self._cache = self._cache[-self._cache_max:]

            return {
                "success": False,
                "queued": True,
                "queue_position": len(self._cache),
                "error": self._last_error
            }

        return {"success": False, "error": self._last_error}

    def health(self) -> dict:
        """Return health status."""
        return {
            "healthy": self._healthy,
            "fallback_mode": self._fallback_mode,
            "last_error": self._last_error,
            "queue_size": len(self._cache),
            "storage_path": self.storage_path
        }

    def flush_queue(self) -> dict:
        """Attempt to flush queued operations."""
        if not self._cache:
            return {"flushed": 0}

        if not self._healthy:
            self._init_chromadb()

        if not self._healthy:
            return {"flushed": 0, "error": "ChromaDB still unavailable"}

        flushed = 0
        failed = 0

        for item in self._cache:
            try:
                if item["operation"] == "add":
                    self.collection.add(**item["kwargs"])
                    flushed += 1
            except Exception as e:
                failed += 1

        self._cache = []
        return {"flushed": flushed, "failed": failed}


# Use wrapper instead of direct client
db = ChromaDBWrapper(STORAGE_PATH, CIV)

@app.tool()
async def query_memory(...) -> dict:
    results = db.query(query, limit, ...)

    if results.get("_fallback"):
        return {
            "memories": [],
            "warning": "ChromaDB unavailable, running in degraded mode",
            "error": results.get("_error")
        }

    # ... normal processing
```

---

## 8. Additional Recommendations

### 8.1 Logging Infrastructure

```python
import logging
import json

# Structured logging
logger = logging.getLogger("memory-server")
handler = logging.FileHandler("/var/log/ai-civ/memory-server.jsonl")
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)

def log_operation(operation: str, details: dict, success: bool, duration_ms: int):
    """Log operation for debugging and analytics."""
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "operation": operation,
        "success": success,
        "duration_ms": duration_ms,
        "civilization": CIV,
        **details
    }
    logger.info(json.dumps(entry))
```

### 8.2 Metrics Endpoint

```python
@app.tool()
async def get_metrics() -> dict:
    """Prometheus-compatible metrics."""
    return {
        "memory_server_requests_total": request_counter,
        "memory_server_errors_total": error_counter,
        "memory_server_query_duration_seconds": query_histogram,
        "memory_server_store_duration_seconds": store_histogram,
        "memory_server_memories_total": collection.count(),
        "memory_server_pending_memories": len(collection.get(where={"status": "pending"})["ids"]),
    }
```

### 8.3 Bulk Operations

```python
@app.tool()
async def store_memories_bulk(
    memories: list[dict],
    batch_size: int = 50
) -> dict:
    """Store multiple memories efficiently."""

    stored = 0
    failed = 0
    errors = []

    for batch_start in range(0, len(memories), batch_size):
        batch = memories[batch_start:batch_start + batch_size]

        try:
            collection.add(
                ids=[m["id"] for m in batch],
                documents=[m["content"] for m in batch],
                metadatas=[m["metadata"] for m in batch]
            )
            stored += len(batch)
        except Exception as e:
            failed += len(batch)
            errors.append(str(e))

    return {"stored": stored, "failed": failed, "errors": errors[:5]}
```

---

## Summary: Priority Recommendations

### P0 (Critical - Before Production)
1. Add comprehensive error handling to ALL tools
2. Implement `health_check` tool
3. Add rate limiting
4. Implement graceful degradation wrapper

### P1 (Important - Phase 1)
5. Add `delete_memory` and `update_memory` tools
6. Expand quality gates in `verify_receipt`
7. Add pagination to `query_memory`
8. Add structured logging

### P2 (Recommended - Phase 2)
9. Add `get_stats` tool
10. Add bulk operations
11. Expand metadata fields
12. Add metrics endpoint

### P3 (Nice to Have - Later)
13. Keyword/hybrid search modes
14. Date range filtering
15. Access tracking
16. Related memory linking

---

## Conclusion

ADR-018 provides an excellent architectural foundation. The local-only ChromaDB approach is sound, the receipt system addresses October's quality failures, and the hook integration ensures adoption.

However, the MCP server skeleton needs significant hardening before production:
- Error handling is absent
- Rate limiting is absent
- Graceful degradation is absent
- Several essential tools are missing

With the P0 recommendations implemented, this system will be production-ready. The P1 additions will make it robust for daily use across both civilizations.

**WEAVER is ready to collaborate on implementation and testing.**

---

*Review completed by WEAVER api-architect agent*
*Cross-CIV collaboration: Both CIVs build and test, merge findings*
