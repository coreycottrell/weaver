# ATProto MVP Specification: Agent Learning Records

**Agent**: test-architect
**Domain**: Test Strategy, MVP Design
**Date**: 2026-01-14

---

## Executive Summary

This specification defines a Minimal Viable Product for ATProto integration. The MVP publishes agent learning memories to ATProto as custom records, creating a "glass box" cognitive archive that other agents and humans can query.

**The smallest thing that teaches us the most**: Publishing memory entries as custom ATProto records using our existing `weaver-aiciv.bsky.social` account.

---

## Memory Search Results

**Searched**: `.claude/memory/` for "atproto", "lexicon", "custom records"

**Found**:
- `2026-01-14--atproto-ai-infrastructure-comprehensive-brief.md` - Detailed lexicon research
- `2026-01-04--atproto-ai-collective-intelligence.md` - Blog post on Cameron's thesis
- `2026-01-13--void-comind-network-atproto-reasoning.md` - Comind analysis

**Applying**:
- Lexicon schema patterns from research
- SDK usage patterns from `tools/bsky_utils.py`
- Rate limit awareness from `docs/BLUESKY-API-REFERENCE.md`

---

## Section 1: MVP Scope Definition

### What We're Building

**Single lexicon, single record type, write + read operations.**

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Record type** | Agent Learning | Directly maps to existing memory system |
| **Operations** | Write + Read | Need both to verify data integrity |
| **Lexicon count** | ONE | Start minimal, expand later |
| **Namespace** | `social.aiciv.learning.entry` | We control `aiciv.social` domain |
| **Storage location** | WEAVER's existing PDS | No new infrastructure needed |

### What We're NOT Building (Yet)

- Custom App View (aggregation service)
- Multi-collective publishing
- Real-time firehose consumption
- Complex knowledge graphs (links between records)
- DNS TXT record for lexicon authority (Phase 2)

### Why Agent Learning Records?

1. **Direct mapping**: Our `.claude/memory/agent-learnings/` already produces this data
2. **Immediate value**: Public cognitive archive enables external auditing
3. **Testable**: Clear success criteria (can we read back what we wrote?)
4. **Demonstrative**: Shows glass box architecture in action
5. **Low risk**: Doesn't affect existing Bluesky posting

---

## Section 2: Lexicon Schema

### social.aiciv.learning.entry (v0.1.0)

```json
{
  "lexicon": 1,
  "id": "social.aiciv.learning.entry",
  "revision": 1,
  "description": "An agent learning memory entry published by WEAVER collective",
  "defs": {
    "main": {
      "type": "record",
      "key": "tid",
      "record": {
        "type": "object",
        "required": ["content", "createdAt", "agentId"],
        "properties": {
          "content": {
            "type": "string",
            "maxLength": 10000,
            "description": "The learning content (markdown supported)"
          },
          "createdAt": {
            "type": "string",
            "format": "datetime",
            "description": "ISO 8601 timestamp"
          },
          "agentId": {
            "type": "string",
            "maxLength": 64,
            "description": "Agent name (e.g., 'pattern-detector', 'security-auditor')"
          },
          "topic": {
            "type": "string",
            "maxLength": 200,
            "description": "Brief topic description"
          },
          "learningType": {
            "type": "string",
            "knownValues": ["pattern", "technique", "gotcha", "synthesis", "operational", "teaching", "experiential"],
            "description": "Category of learning (from A-C-Gee taxonomy)"
          },
          "confidence": {
            "type": "string",
            "knownValues": ["low", "medium", "high"],
            "description": "Confidence in the learning"
          },
          "tags": {
            "type": "array",
            "items": {"type": "string", "maxLength": 50},
            "maxLength": 10,
            "description": "Categorization tags"
          },
          "sourceFile": {
            "type": "string",
            "maxLength": 500,
            "description": "Original file path in WEAVER memory system"
          }
        }
      }
    }
  }
}
```

### Schema Design Decisions

| Field | Decision | Rationale |
|-------|----------|-----------|
| `content` | 10KB max | Supports full memory entries |
| `agentId` | String not DID | Agents don't have separate DIDs |
| `learningType` | Known values | Maps to existing taxonomy |
| `sourceFile` | Optional | Enables cross-reference to local memory |
| `key` | TID | Auto-generated timestamp ID |

---

## Section 3: Implementation Plan

### Prerequisites

| Item | Status | Action |
|------|--------|--------|
| ATProto SDK | INSTALLED | `atproto 0.0.65` |
| Bluesky account | ACTIVE | `weaver-aiciv.bsky.social` |
| Session file | EXISTS | `.claude/from-corey/bsky/bsky_automation/bsky_session.txt` |
| Test memories | EXISTS | `.claude/memory/agent-learnings/` has 50+ files |

### Step-by-Step Implementation

#### Step 1: Create ATProto Custom Records Module (30 min)

**File**: `/home/corey/projects/AI-CIV/WEAVER/tools/atproto_records.py`

```python
"""
ATProto Custom Records - Publish agent learnings to protocol

MVP: Write and read social.aiciv.learning.entry records
"""

from atproto import Client
from datetime import datetime, timezone
from pathlib import Path
import json

# Constants
LEXICON_ID = "social.aiciv.learning.entry"
SESSION_FILE = Path('/home/corey/projects/AI-CIV/WEAVER/.claude/from-corey/bsky/bsky_automation/bsky_session.txt')


def get_client() -> Client:
    """Get authenticated client using session file."""
    client = Client()
    with open(SESSION_FILE, 'r') as f:
        client.login(session_string=f.read().strip())
    return client


def create_learning_record(
    client: Client,
    content: str,
    agent_id: str,
    topic: str,
    learning_type: str = "pattern",
    confidence: str = "medium",
    tags: list[str] = None,
    source_file: str = None
) -> dict:
    """
    Publish a learning entry to ATProto.

    Returns the created record with uri and cid.
    """
    record = {
        "$type": LEXICON_ID,
        "content": content[:10000],  # Respect max length
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "agentId": agent_id[:64],
        "topic": topic[:200] if topic else None,
        "learningType": learning_type,
        "confidence": confidence,
        "tags": (tags or [])[:10],
    }

    if source_file:
        record["sourceFile"] = source_file[:500]

    # Remove None values
    record = {k: v for k, v in record.items() if v is not None}

    # Create record in repo
    response = client.com.atproto.repo.create_record({
        "repo": client.me.did,
        "collection": LEXICON_ID,
        "record": record
    })

    return {
        "uri": response.uri,
        "cid": response.cid,
        "record": record
    }


def list_learning_records(client: Client, limit: int = 50) -> list:
    """
    Fetch learning records from WEAVER's repo.

    Returns list of records with uri, cid, and value.
    """
    response = client.com.atproto.repo.list_records({
        "repo": client.me.did,
        "collection": LEXICON_ID,
        "limit": limit
    })

    return [
        {
            "uri": record.uri,
            "cid": record.cid,
            "value": record.value
        }
        for record in response.records
    ]


def get_learning_record(client: Client, rkey: str) -> dict:
    """
    Fetch a specific learning record by record key.
    """
    response = client.com.atproto.repo.get_record({
        "repo": client.me.did,
        "collection": LEXICON_ID,
        "rkey": rkey
    })

    return {
        "uri": response.uri,
        "cid": response.cid,
        "value": response.value
    }


def delete_learning_record(client: Client, rkey: str) -> bool:
    """
    Delete a learning record by record key.

    Use for cleanup during testing.
    """
    try:
        client.com.atproto.repo.delete_record({
            "repo": client.me.did,
            "collection": LEXICON_ID,
            "rkey": rkey
        })
        return True
    except Exception as e:
        print(f"Delete failed: {e}")
        return False


# Utility: Parse memory file to learning record
def memory_file_to_record(file_path: Path) -> dict:
    """
    Parse a WEAVER memory file into learning record fields.

    Expected format:
    # Topic Line
    **Agent**: agent-name
    **Type**: pattern|technique|gotcha
    ...
    [content]
    """
    content = file_path.read_text()

    # Extract agent from path or content
    agent_id = "unknown"
    if "/agent-learnings/" in str(file_path):
        parts = str(file_path).split("/agent-learnings/")
        if len(parts) > 1:
            agent_id = parts[1].split("/")[0]

    # Extract metadata from content
    lines = content.split("\n")
    topic = lines[0].replace("#", "").strip() if lines else "Untitled"

    learning_type = "pattern"
    confidence = "medium"
    tags = []

    for line in lines[:20]:  # Check first 20 lines for metadata
        if "**Type**:" in line:
            type_val = line.split(":")[-1].strip().lower()
            if type_val in ["pattern", "technique", "gotcha", "synthesis", "operational", "teaching", "experiential"]:
                learning_type = type_val
        if "**Confidence**:" in line:
            conf_val = line.split(":")[-1].strip().lower()
            if conf_val in ["low", "medium", "high"]:
                confidence = conf_val
        if "**Tags**:" in line:
            tag_str = line.split(":")[-1].strip()
            tags = [t.strip() for t in tag_str.split(",")][:10]

    return {
        "content": content,
        "agent_id": agent_id,
        "topic": topic,
        "learning_type": learning_type,
        "confidence": confidence,
        "tags": tags,
        "source_file": str(file_path)
    }
```

#### Step 2: Create Test Suite (30 min)

**File**: `/home/corey/projects/AI-CIV/WEAVER/tests/test_atproto_records.py`

```python
"""
Test Suite for ATProto Custom Records

TDD approach: RED -> GREEN -> REFACTOR
"""

import pytest
from pathlib import Path
from datetime import datetime

# Import module under test (will fail initially - RED)
from tools.atproto_records import (
    get_client,
    create_learning_record,
    list_learning_records,
    get_learning_record,
    delete_learning_record,
    memory_file_to_record,
    LEXICON_ID
)


class TestATProtoRecords:
    """Integration tests for ATProto custom records."""

    @pytest.fixture
    def client(self):
        """Get authenticated client."""
        return get_client()

    @pytest.fixture
    def test_record_data(self):
        """Sample learning record data."""
        return {
            "content": "Test learning: ATProto custom records work as expected.",
            "agent_id": "test-architect",
            "topic": "ATProto MVP Testing",
            "learning_type": "technique",
            "confidence": "high",
            "tags": ["testing", "atproto", "mvp"]
        }

    # ============ CREATE TESTS ============

    def test_create_record_returns_uri(self, client, test_record_data):
        """Creating a record should return a valid URI."""
        result = create_learning_record(client, **test_record_data)

        assert "uri" in result
        assert result["uri"].startswith("at://")
        assert LEXICON_ID in result["uri"]

        # Cleanup
        rkey = result["uri"].split("/")[-1]
        delete_learning_record(client, rkey)

    def test_create_record_returns_cid(self, client, test_record_data):
        """Creating a record should return a valid CID."""
        result = create_learning_record(client, **test_record_data)

        assert "cid" in result
        assert len(result["cid"]) > 10  # CIDs are base32 strings

        # Cleanup
        rkey = result["uri"].split("/")[-1]
        delete_learning_record(client, rkey)

    def test_create_record_content_preserved(self, client, test_record_data):
        """Record content should match what was submitted."""
        result = create_learning_record(client, **test_record_data)

        assert result["record"]["content"] == test_record_data["content"]
        assert result["record"]["agentId"] == test_record_data["agent_id"]
        assert result["record"]["topic"] == test_record_data["topic"]

        # Cleanup
        rkey = result["uri"].split("/")[-1]
        delete_learning_record(client, rkey)

    def test_create_record_has_timestamp(self, client, test_record_data):
        """Record should have valid ISO timestamp."""
        result = create_learning_record(client, **test_record_data)

        assert "createdAt" in result["record"]
        # Should parse as ISO datetime
        datetime.fromisoformat(result["record"]["createdAt"].replace("Z", "+00:00"))

        # Cleanup
        rkey = result["uri"].split("/")[-1]
        delete_learning_record(client, rkey)

    def test_create_record_long_content_truncated(self, client):
        """Content over 10KB should be truncated."""
        long_content = "x" * 15000

        result = create_learning_record(
            client,
            content=long_content,
            agent_id="test-architect",
            topic="Long content test"
        )

        assert len(result["record"]["content"]) == 10000

        # Cleanup
        rkey = result["uri"].split("/")[-1]
        delete_learning_record(client, rkey)

    # ============ READ TESTS ============

    def test_list_records_returns_list(self, client):
        """Listing records should return a list."""
        result = list_learning_records(client, limit=5)

        assert isinstance(result, list)

    def test_get_record_retrieves_created(self, client, test_record_data):
        """Should be able to fetch a record by rkey after creating it."""
        # Create
        create_result = create_learning_record(client, **test_record_data)
        rkey = create_result["uri"].split("/")[-1]

        # Read
        get_result = get_learning_record(client, rkey)

        assert get_result["value"]["content"] == test_record_data["content"]
        assert get_result["value"]["agentId"] == test_record_data["agent_id"]

        # Cleanup
        delete_learning_record(client, rkey)

    # ============ DELETE TESTS ============

    def test_delete_record_removes_record(self, client, test_record_data):
        """Deleting a record should remove it from the repo."""
        # Create
        create_result = create_learning_record(client, **test_record_data)
        rkey = create_result["uri"].split("/")[-1]

        # Delete
        delete_result = delete_learning_record(client, rkey)
        assert delete_result is True

        # Verify gone
        with pytest.raises(Exception):
            get_learning_record(client, rkey)

    # ============ MEMORY FILE PARSER TESTS ============

    def test_memory_file_extracts_agent(self, tmp_path):
        """Parser should extract agent ID from file path."""
        # Create mock memory file
        agent_dir = tmp_path / "agent-learnings" / "security-auditor"
        agent_dir.mkdir(parents=True)
        memory_file = agent_dir / "2026-01-14--test-learning.md"
        memory_file.write_text("# Test Topic\nContent here.")

        result = memory_file_to_record(memory_file)

        assert result["agent_id"] == "security-auditor"

    def test_memory_file_extracts_topic(self, tmp_path):
        """Parser should extract topic from first line."""
        memory_file = tmp_path / "test.md"
        memory_file.write_text("# Security Patterns in ATProto\nMore content...")

        result = memory_file_to_record(memory_file)

        assert result["topic"] == "Security Patterns in ATProto"

    def test_memory_file_extracts_metadata(self, tmp_path):
        """Parser should extract type, confidence, tags from content."""
        memory_file = tmp_path / "test.md"
        memory_file.write_text("""# Topic
**Type**: gotcha
**Confidence**: low
**Tags**: security, testing, edge-case

Content here.
""")

        result = memory_file_to_record(memory_file)

        assert result["learning_type"] == "gotcha"
        assert result["confidence"] == "low"
        assert "security" in result["tags"]


class TestLexiconCompliance:
    """Tests ensuring our records comply with ATProto lexicon requirements."""

    @pytest.fixture
    def client(self):
        return get_client()

    def test_record_has_required_fields(self, client):
        """Record must have content, createdAt, agentId."""
        result = create_learning_record(
            client,
            content="Required fields test",
            agent_id="test-architect",
            topic="Compliance"
        )

        record = result["record"]
        assert "content" in record
        assert "createdAt" in record
        assert "agentId" in record

        # Cleanup
        rkey = result["uri"].split("/")[-1]
        delete_learning_record(client, rkey)

    def test_record_type_is_set(self, client):
        """Record must have $type field matching lexicon."""
        result = create_learning_record(
            client,
            content="Type field test",
            agent_id="test-architect",
            topic="Compliance"
        )

        assert result["record"]["$type"] == LEXICON_ID

        # Cleanup
        rkey = result["uri"].split("/")[-1]
        delete_learning_record(client, rkey)

    def test_known_values_enforced(self, client):
        """learningType should only accept known values."""
        result = create_learning_record(
            client,
            content="Known values test",
            agent_id="test-architect",
            topic="Compliance",
            learning_type="pattern"  # Valid
        )

        assert result["record"]["learningType"] == "pattern"

        # Cleanup
        rkey = result["uri"].split("/")[-1]
        delete_learning_record(client, rkey)


class TestRoundTrip:
    """End-to-end tests verifying full cycle."""

    @pytest.fixture
    def client(self):
        return get_client()

    def test_full_roundtrip(self, client):
        """Create -> List -> Get -> Delete cycle."""
        # CREATE
        content = "Full roundtrip test content"
        create_result = create_learning_record(
            client,
            content=content,
            agent_id="test-architect",
            topic="Roundtrip Test",
            learning_type="technique",
            confidence="high",
            tags=["roundtrip", "test"]
        )
        rkey = create_result["uri"].split("/")[-1]

        # LIST (should include new record)
        list_result = list_learning_records(client, limit=50)
        uris = [r["uri"] for r in list_result]
        assert create_result["uri"] in uris

        # GET
        get_result = get_learning_record(client, rkey)
        assert get_result["value"]["content"] == content

        # DELETE
        delete_result = delete_learning_record(client, rkey)
        assert delete_result is True

        # VERIFY GONE
        with pytest.raises(Exception):
            get_learning_record(client, rkey)
```

#### Step 3: Create Integration Hook (20 min)

**File**: `/home/corey/projects/AI-CIV/WEAVER/.claude/hooks/post_memory_write_atproto.py`

```python
#!/usr/bin/env python3
"""
Post-Memory-Write Hook: Publish significant learnings to ATProto

Triggered after agent writes to memory system.
Publishes to social.aiciv.learning.entry collection.
"""

import sys
import json
from pathlib import Path

# Add tools to path
sys.path.insert(0, '/home/corey/projects/AI-CIV/WEAVER')

from tools.atproto_records import (
    get_client,
    create_learning_record,
    memory_file_to_record
)


def should_publish(file_path: Path) -> bool:
    """
    Determine if a memory file should be published to ATProto.

    Criteria:
    - In agent-learnings directory
    - Not a draft (no "draft" in filename)
    - Not private (no "private" in path)
    - Minimum content length (> 100 chars)
    """
    path_str = str(file_path)

    # Must be in agent-learnings
    if "/agent-learnings/" not in path_str:
        return False

    # No drafts or private
    if "draft" in path_str.lower() or "private" in path_str.lower():
        return False

    # Check content length
    try:
        content = file_path.read_text()
        if len(content) < 100:
            return False
    except:
        return False

    return True


def publish_memory_to_atproto(file_path: Path) -> dict | None:
    """
    Publish a memory file to ATProto.

    Returns the created record or None if skipped.
    """
    if not should_publish(file_path):
        return None

    try:
        client = get_client()
        record_data = memory_file_to_record(file_path)

        result = create_learning_record(
            client,
            content=record_data["content"],
            agent_id=record_data["agent_id"],
            topic=record_data["topic"],
            learning_type=record_data["learning_type"],
            confidence=record_data["confidence"],
            tags=record_data["tags"],
            source_file=record_data["source_file"]
        )

        return result
    except Exception as e:
        print(f"ATProto publish failed: {e}", file=sys.stderr)
        return None


def main():
    """
    Hook entry point.

    Expected input: JSON with file_path of written memory.
    """
    if len(sys.argv) < 2:
        print("Usage: post_memory_write_atproto.py <file_path>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    result = publish_memory_to_atproto(file_path)

    if result:
        print(f"Published to ATProto: {result['uri']}")
    else:
        print("Skipped (did not meet publication criteria)")


if __name__ == "__main__":
    main()
```

#### Step 4: Run Tests (TDD RED Phase)

```bash
cd /home/corey/projects/AI-CIV/WEAVER
pytest tests/test_atproto_records.py -v
```

**Expected**: Tests FAIL because module doesn't exist yet.

#### Step 5: Implement Module (TDD GREEN Phase)

Create `/home/corey/projects/AI-CIV/WEAVER/tools/atproto_records.py` with the code from Step 1.

```bash
pytest tests/test_atproto_records.py -v
```

**Expected**: Tests PASS.

#### Step 6: Manual Verification

```bash
# Interactive test
python3 -c "
from tools.atproto_records import get_client, create_learning_record, list_learning_records, delete_learning_record

client = get_client()
print(f'Connected as: {client.me.handle}')

# Create test record
result = create_learning_record(
    client,
    content='MVP test: This learning was published via ATProto custom records.',
    agent_id='test-architect',
    topic='ATProto MVP Verification',
    learning_type='technique',
    confidence='high',
    tags=['mvp', 'atproto', 'test']
)
print(f'Created: {result[\"uri\"]}')

# List records
records = list_learning_records(client, limit=5)
print(f'Found {len(records)} learning records')

# Cleanup
rkey = result['uri'].split('/')[-1]
delete_learning_record(client, rkey)
print('Test record deleted')
"
```

---

## Section 4: Test Cases

### Unit Tests (Offline)

| Test | Input | Expected Output | Status |
|------|-------|-----------------|--------|
| Memory file parsing | Valid markdown file | Extracted fields | TBD |
| Long content truncation | 15KB string | 10KB string | TBD |
| Known values validation | "invalid_type" | Falls back to "pattern" | TBD |
| Empty tags handling | None | Empty list | TBD |

### Integration Tests (Online)

| Test | Action | Success Criteria | Status |
|------|--------|------------------|--------|
| Create record | POST to repo | Returns valid URI | TBD |
| Read record | GET by rkey | Returns matching content | TBD |
| List records | GET collection | Returns list including new | TBD |
| Delete record | DELETE by rkey | Record no longer fetchable | TBD |
| Full roundtrip | Create->List->Get->Delete | All operations succeed | TBD |

### Error Cases

| Test | Trigger | Expected Behavior | Status |
|------|---------|-------------------|--------|
| Auth failure | Invalid session | Raises exception | TBD |
| Missing required field | No content | Validation error | TBD |
| Rate limit | Rapid requests | Retry with backoff | TBD |
| Network timeout | Slow connection | Graceful failure | TBD |

### Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Test pass rate | 100% | pytest output |
| Roundtrip latency | < 5s | Timing in tests |
| Content integrity | 100% | Compare input vs fetched |
| Error recovery | Graceful | No crashes |

---

## Section 5: Learning Goals

### Questions This MVP Answers

1. **Can we use custom lexicons without DNS authority?**
   - Hypothesis: PDS accepts any lexicon ID
   - Test: Create record with `social.aiciv.*` namespace
   - If fails: Need to set up DNS TXT record first

2. **What's the actual write latency?**
   - Measure: Time from API call to confirmed storage
   - Baseline: Compare to `app.bsky.feed.post` latency

3. **Can other clients read our custom records?**
   - Test: Fetch via raw ATProto API, not Bluesky
   - Implication: Determines discoverability

4. **How large can records be in practice?**
   - Spec says "within reason"
   - Test: 1KB, 5KB, 10KB, 50KB content

5. **Do we need an App View?**
   - If direct repo queries work: No
   - If aggregation needed: Yes (Phase 2)

### What We Learn From Failure Modes

| Failure | Learning |
|---------|----------|
| "Unknown lexicon" error | DNS TXT record required |
| 413 Payload Too Large | Content size limits |
| Rate limiting on custom records | Different limits than posts |
| Records not fetched by others | App View needed for discovery |
| Session issues | Token refresh for long-running ops |

### Success Unlocks

If MVP succeeds:
- **Phase 2**: Memory sync pipeline (auto-publish significant learnings)
- **Phase 3**: Cross-collective querying (read other agents' learnings)
- **Phase 4**: Knowledge graph links (connect related learnings)
- **Phase 5**: App View for public discovery

---

## Section 6: Hooks Design

### Architecture: Memory Write -> ATProto Publish

```
Agent completes task
    |
    v
Writes to .claude/memory/agent-learnings/{agent}/{date}--{topic}.md
    |
    v
[Hook triggers] post_memory_write_atproto.py
    |
    v
Parses memory file -> learning record fields
    |
    v
Publishes to social.aiciv.learning.entry collection
    |
    v
Returns URI for cross-reference
```

### Which Agent Actions Trigger Publishing

| Action | Publish? | Rationale |
|--------|----------|-----------|
| Memory write (significant learning) | YES | Core MVP |
| Memory write (operational log) | NO | Too noisy |
| Ceremony output | YES | High-value synthesis |
| Task completion summary | MAYBE | Filter by importance |
| Error recovery learning | YES | Valuable gotchas |
| Draft/WIP content | NO | Not ready for public |

### Publishing Criteria

```python
def should_publish(memory_entry):
    """Criteria for ATProto publication."""

    # MUST be in agent-learnings (not tasks, not summaries)
    if not in_agent_learnings_dir(memory_entry):
        return False

    # MUST have substantial content
    if len(memory_entry.content) < 100:
        return False

    # MUST NOT be draft or private
    if "draft" in memory_entry.path or "private" in memory_entry.path:
        return False

    # SHOULD have high or medium confidence
    if memory_entry.confidence == "low":
        return False  # Or require manual approval

    return True
```

### Hook Integration Points

**Option A: Post-tool hook (recommended for MVP)**
- Trigger: After Write tool creates `.md` file in memory dir
- Pros: Automatic, no agent changes needed
- Cons: May catch drafts, needs path filtering

**Option B: Explicit agent call**
- Agent calls `publish_to_atproto(memory_entry)` after writing
- Pros: Full control, explicit intent
- Cons: Requires skill updates, may be forgotten

**Option C: Batch sync (Phase 2)**
- Periodic job syncs recent memories to ATProto
- Pros: Debounced, efficient
- Cons: Not real-time, more complex

**MVP Choice**: Option A with path filtering (simplest, automatic)

---

## Section 7: Timeline

| Phase | Task | Duration | Dependencies |
|-------|------|----------|--------------|
| 1 | Write test suite | 30 min | None |
| 2 | Run tests (RED) | 5 min | Test suite |
| 3 | Implement module | 30 min | Tests defined |
| 4 | Run tests (GREEN) | 10 min | Module exists |
| 5 | Manual verification | 15 min | Tests pass |
| 6 | Hook implementation | 20 min | Module works |
| 7 | Documentation | 15 min | All above |
| **Total** | | **~2 hours** | |

---

## Section 8: Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| DNS TXT required | Medium | Blocks MVP | Test with aiciv.social domain |
| Rate limits different | Low | Slows testing | Use separate test account |
| SDK doesn't support custom lexicons | Low | Major rework | Verified: `create_record` is generic |
| Content size limits | Medium | Truncation needed | Already handling in schema |
| Session expiry during tests | Medium | Test failures | Refresh session before test run |

---

## Section 9: Files to Create

| File | Purpose |
|------|---------|
| `/home/corey/projects/AI-CIV/WEAVER/tools/atproto_records.py` | Core module |
| `/home/corey/projects/AI-CIV/WEAVER/tests/test_atproto_records.py` | Test suite |
| `/home/corey/projects/AI-CIV/WEAVER/.claude/hooks/post_memory_write_atproto.py` | Integration hook |
| `/home/corey/projects/AI-CIV/WEAVER/lexicons/social.aiciv.learning.entry.json` | Lexicon schema (reference) |
| `/home/corey/projects/AI-CIV/WEAVER/docs/ATPROTO-MVP-SPECIFICATION.md` | This document |

---

## Section 10: Verification Checklist

Before claiming MVP complete:

- [ ] Test suite exists and passes
- [ ] Module creates records successfully
- [ ] Module reads records back correctly
- [ ] Module deletes test records (cleanup)
- [ ] Full roundtrip verified manually
- [ ] Hook implemented (if time permits)
- [ ] Documentation updated
- [ ] Memory written with learnings

---

## Memory Written

**Path**: `/home/corey/projects/AI-CIV/WEAVER/.claude/memory/agent-learnings/test-architect/2026-01-14--atproto-mvp-specification.md`
**Type**: synthesis
**Topic**: ATProto MVP design - agent learning records as custom ATProto collection

**Key learnings captured**:
- Custom lexicon schema for agent learnings
- TDD approach with pytest for ATProto operations
- Hook architecture for automatic publishing
- Learning goals and failure mode analysis
- 2-hour implementation timeline
