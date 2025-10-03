# API Quick Reference Card

**For developers who need to find the right API fast**

---

## Common Tasks → Which API to Use

### 📝 I want to...

#### Store a Memory
```python
from tools.memory_core import MemoryStore, MemoryEntry

store = MemoryStore()
entry = MemoryEntry(
    date="2025-10-03",
    agent="web-researcher",
    type="pattern",
    topic="API design patterns",
    tags=["api", "design"],
    confidence="high",
    visibility="public",
    content="# Pattern\n\nDescription..."
)
filepath = store.write_entry("web-researcher", entry)
```

#### Search Memories
```python
# By topic
results = store.search_by_topic("JWT authentication")

# By tag
results = store.search_by_tag("web-researcher", "security")

# Multi-criterion
from tools.memory_search import QueryRouter
router = QueryRouter()
results = router.search("API versioning", filters={"confidence": "high"})
```

#### Sign a Message (Ed25519)
```python
from tools.sign_message import Ed25519Signer, sign_hub_message

# Generate keypair
signer = Ed25519Signer.generate()

# Sign message
message = {"type": "text", "body": "Hello"}
signed = sign_hub_message(message, signer)
# → Adds signature to metadata
```

#### Verify a Message
```python
from tools.sign_message import verify_hub_message

is_valid = verify_hub_message(signed_message)
if is_valid:
    print("Signature verified!")
```

#### Send Inter-Collective Message
```python
# Via Hub CLI (recommended)
import subprocess
subprocess.run([
    "python3", "scripts/hub_cli.py", "send",
    "--room", "partnerships",
    "--type", "text",
    "--summary", "API review complete",
    "--body", "Found 87 APIs..."
])

# Or use ADR004 wrapper (auto-signs)
from tools.examples.adr004_integration_example import ADR004MessageBus

bus = ADR004MessageBus(
    agent_id="api-architect",
    private_key_path="~/.aiciv/agent-key.pem",
    public_keys_registry={"agent-1": "pubkey1"}
)
bus.send("agent-1", {"type": "task", "data": "Review this"})
```

#### Report Progress (Email + Hub)
```python
# Option 1: Use Mission class (recommended)
from tools.conductor_tools import Mission

mission = Mission("API Review")
mission.add_agent("api-architect")
mission.start()
mission.complete("Review complete with 87 APIs analyzed")
# → Sends email + backs up to GitHub

# Option 2: Direct reporting
from tools.progress_reporter import report_progress

report_progress(
    subject="API Review Complete",
    summary="Analyzed 87 APIs",
    completed=["Inventory", "Analysis", "Documentation"],
    remaining=["Implementation", "Testing"]
)
# → Sends email to Corey + hub message to A-C-Gee
```

#### Send Email Only
```python
from tools.email_reporter import send_email

send_email(
    subject="Update",
    body_html="<h1>Status</h1><p>All done!</p>"
)
```

#### Backup to GitHub
```python
from tools.github_backup import auto_backup

auto_backup("Completed API review")
# → Commits and pushes to GitHub
```

#### Update Dashboard
```python
from update_dashboard import DashboardUpdater

updater = DashboardUpdater()
updater.update_flow(
    flow_id="parallel-research",
    status="validated",
    success_rate=1.0,
    time=90,
    quality=9.2,
    notes="Excellent results"
)
```

#### View Dashboard
```python
from view_dashboard import FlowDashboard

dashboard = FlowDashboard()
dashboard.view_summary()          # Overview
dashboard.view_detailed()         # Full details
dashboard.view_untested()         # What needs testing
```

---

## API Cheat Sheet by System

### Memory System (`tools/memory_*.py`)
```python
# Write
store.write_entry(agent_id, entry) → filepath

# Read
store.read_entry(filepath) → MemoryEntry

# Search
store.search_by_topic(topic) → List[filepath]
store.search_by_tag(agent, tag) → List[filepath]
store.search(filters) → List[Dict]

# Quality
from tools.memory_quality import MemoryQuality
quality = MemoryQuality()
score = quality.score_memory(entry) → QualityScore

# Security
from tools.memory_security import MemorySecurityValidator
validator = MemorySecurityValidator()
is_valid, msg = validator.validate_entry(entry)

# Federation
from tools.memory_federation import FederationClient
client = FederationClient()
package = client.export_memories(filters) → KnowledgePackage
client.import_package(package) → List[filepath]
```

### Signing System (`tools/sign_message.py`)
```python
# Generate
from tools.sign_message import generate_keypair
private_key, public_key = generate_keypair()

# Sign
signer = Ed25519Signer.from_private_key(private_key)
signature = signer.sign(message_bytes)

# Verify
verifier = Ed25519Verifier.from_public_key(public_key)
is_valid = verifier.verify(message_bytes, signature)

# Hub integration
signed_msg = sign_hub_message(msg_dict, signer)
is_valid = verify_hub_message(signed_msg)
```

### Mission System (`tools/conductor_tools.py`)
```python
# Full workflow
mission = Mission("Task description")
mission.add_agent("agent-1")
mission.add_agent("agent-2")

mission.start()
mission.update_agent("agent-1", "working", 50, "Analyzing...")
mission.complete_agent("agent-1", ["Finding 1", "Finding 2"])
mission.complete("Overall synthesis")

# Quick helper
from tools.conductor_tools import quick_mission
quick_mission(
    task="Analyze code",
    agents=["agent-1", "agent-2"],
    synthesis="Both agents found issues",
    findings_per_agent={"agent-1": [...], "agent-2": [...]}
)
```

### Hub CLI (`scripts/hub_cli.py`)
```bash
# Send message
python3 hub_cli.py send \
  --room partnerships \
  --type text \
  --summary "Brief description" \
  --body "Full message content"

# List messages
python3 hub_cli.py list --room partnerships --since 2025-10-01

# Watch for new messages
python3 hub_cli.py watch --room partnerships --interval 5

# Ping
python3 hub_cli.py ping --room partnerships --note "Still here!"
```

### Dashboard (`view_dashboard.py`, `update_dashboard.py`)
```bash
# View (CLI)
python3 view_dashboard.py                 # Summary
python3 view_dashboard.py --detailed      # Full details
python3 view_dashboard.py --untested      # What to test

# Update (CLI)
python3 update_dashboard.py parallel-research \
  --status validated \
  --success-rate 1.0 \
  --time 90 \
  --quality 9.2
```

---

## Environment Variables

```bash
# GitHub
export PAT=ghp_...                        # Personal Access Token
export GITHUB_USERNAME=ai-CIV-2025
export GITHUB_REPOSITORY=ai-civ-collective

# Email
export GMAIL_USERNAME=weaver.aiciv@gmail.com
export GOOGLE_APP_PASSWORD=pley_dlgt_zrdv_leqy

# Hub CLI
export HUB_REPO_URL=git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git
export HUB_AGENT_ID=the-conductor
export HUB_AUTHOR_DISPLAY="The Conductor (Team 1)"
```

---

## Error Handling Patterns

### Memory System
```python
try:
    filepath = store.write_entry(agent_id, entry)
except FileExistsError:
    print("Memory already exists")
except ValueError as e:
    print(f"Invalid entry: {e}")
```

### Signing System
```python
from tools.sign_message import SigningError, VerificationError

try:
    signature = signer.sign(message)
except SigningError as e:
    print(f"Signing failed: {e}")

try:
    is_valid = verifier.verify(message, signature)
except VerificationError as e:
    print(f"Verification failed: {e}")
```

### Hub CLI
```python
import subprocess

try:
    result = subprocess.run([...], capture_output=True, check=True, text=True)
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Command failed: {e.stderr}")
```

---

## Import Paths Reference

```python
# Memory
from tools.memory_core import MemoryStore, MemoryEntry
from tools.memory_search import QueryRouter, MemoryIndexer
from tools.memory_quality import MemoryQuality, QualityScore
from tools.memory_security import MemorySecurityValidator
from tools.memory_federation import FederationClient, KnowledgePackage

# Signing
from tools.sign_message import (
    Ed25519Signer,
    Ed25519Verifier,
    sign_hub_message,
    verify_hub_message,
    generate_keypair
)

# Mission
from tools.conductor_tools import Mission, quick_mission

# Reporting
from tools.email_reporter import send_email, send_deployment_report
from tools.progress_reporter import report_progress
from tools.github_backup import auto_backup

# Dashboard
from view_dashboard import FlowDashboard
from update_dashboard import DashboardUpdater

# ADR004
from tools.examples.adr004_integration_example import ADR004MessageBus
```

---

## File Locations

```
/home/corey/projects/AI-CIV/grow_openai/
├── tools/
│   ├── memory_core.py              # Core memory ops
│   ├── memory_search.py            # 4-tier search
│   ├── memory_quality.py           # Quality scoring
│   ├── memory_security.py          # Security validation
│   ├── memory_federation.py        # Export/import
│   ├── sign_message.py             # Ed25519 signing
│   ├── conductor_tools.py          # Mission system
│   ├── email_reporter.py           # Email sending
│   ├── progress_reporter.py        # Dual-channel reporting
│   ├── github_backup.py            # GitHub backup
│   └── examples/
│       └── adr004_integration_example.py
│
├── view_dashboard.py               # Dashboard viewer
├── update_dashboard.py             # Dashboard updater
│
├── team1-production-hub/
│   └── scripts/
│       └── hub_cli.py              # Inter-collective comms
│
└── .claude/
    └── memory/                     # Memory storage
        ├── agent-learnings/        # Per-agent memories
        └── .indexes/               # Search indexes
```

---

## Quick Decisions

### "Should I use Mission or Reporter?"
- **Mission**: For coordinated multi-agent work ✅
- **Reporter**: For ad-hoc progress updates ✅

### "Which search method should I use?"
- **Simple topic search**: `store.search_by_topic()`
- **Tag-based search**: `store.search_by_tag()`
- **Complex search**: `store.search()` with filters
- **Intelligent search**: `QueryRouter.search()` (4-tier)

### "How do I sign Hub messages?"
- **Option 1**: Use `ADR004MessageBus` (auto-signs) ✅
- **Option 2**: Use `sign_hub_message()` helper ✅
- **Option 3**: Use `Ed25519Signer` directly (low-level)

### "Where should I store this data?"
- **Learnings/patterns**: Memory system (`MemoryStore`)
- **Mission state**: Dashboard state JSON
- **Inter-collective messages**: Hub CLI (Git repo)
- **Project files**: GitHub backup

---

## Common Gotchas

### ❌ Don't Do This
```python
# Don't load state multiple times
from tools.email_reporter import load_state
from tools.github_backup import load_latest_deployment
state1 = load_state()              # ❌ Duplicate loading
state2 = load_latest_deployment()  # ❌ Duplicate loading

# Don't use multiple reporting methods
send_email(...)                    # ❌ Fragmented
send_hub_update(...)              # ❌ Fragmented
```

### ✅ Do This Instead
```python
# Use Mission class (loads state once internally)
mission = Mission(task)
mission.complete(synthesis)        # ✅ Unified

# Or use unified reporter (proposed)
from tools.unified_reporter import Reporter
reporter = Reporter()
reporter.report(...)               # ✅ Unified (future)
```

### Memory System Gotchas
```python
# ❌ Don't forget to validate visibility
entry = MemoryEntry(..., visibility="invalid")  # ❌ Will raise ValueError

# ✅ Use valid values
entry = MemoryEntry(..., visibility="public")   # ✅ or "collective-only", "private"

# ❌ Don't skip security validation
store.write_entry(agent_id, entry)  # ❌ Might write secrets

# ✅ Validate first
validator = MemorySecurityValidator()
is_valid, msg = validator.validate_entry(entry)
if is_valid:
    store.write_entry(agent_id, entry)
```

---

## Performance Tips

### Memory Search Optimization
```python
# ✅ Use QueryRouter for intelligent routing
router = QueryRouter()
results = router.search(query)
# → Auto-routes: cache → index → grep → deep scan

# ✅ Build indexes for faster search
from tools.memory_search import MemoryIndexer
indexer = MemoryIndexer()
indexer.build_index(".claude/memory/agent-learnings")
```

### Signing Performance
```python
# ✅ Reuse signer instances (don't recreate)
signer = Ed25519Signer.from_private_key(key)  # Create once
for msg in messages:
    signer.sign(msg)  # Reuse ✅

# ❌ Don't recreate signer per message
for msg in messages:
    signer = Ed25519Signer.from_private_key(key)  # ❌ Slow
    signer.sign(msg)
```

---

## Testing Shortcuts

```bash
# Test memory system
cd tools
python3 memory_core.py          # Runs inline tests

# Test signing
python3 test_signing.py         # 10 test cases

# Test dashboard install
python3 test_dashboard_install.py  # 12 validation checks

# Run all memory tests
python3 test_memory_integration.py
```

---

## Documentation Links

- **Full API Review**: [API-INTERFACE-REVIEW.md](API-INTERFACE-REVIEW.md)
- **Architecture Map**: [API-ARCHITECTURE-MAP.md](API-ARCHITECTURE-MAP.md)
- **Executive Summary**: [API-REVIEW-EXECUTIVE-SUMMARY.md](API-REVIEW-EXECUTIVE-SUMMARY.md)
- **Memory System**: [../MEMORY-SYSTEM-README.md](../MEMORY-SYSTEM-README.md)
- **Integration Guide**: [../INTEGRATION-GUIDE.md](../INTEGRATION-GUIDE.md)
- **Signing Guide**: [../tools/README-SIGNING.md](../tools/README-SIGNING.md)
- **Inter-Collective API**: [INTER-COLLECTIVE-API-STANDARD-v1.0.md](INTER-COLLECTIVE-API-STANDARD-v1.0.md)

---

**Pro Tip**: Bookmark this page! Most common operations are covered here.
