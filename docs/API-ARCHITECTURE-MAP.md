# API Architecture Map

**Visual representation of all API systems and their relationships**

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI-CIV Collective APIs                        │
│                         (87 APIs Total)                          │
└─────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
            ┌───────▼────────┐      ┌────────▼────────┐
            │  Core Systems  │      │  Integration    │
            │   (50 APIs)    │      │   Systems       │
            │                │      │   (37 APIs)     │
            └────────────────┘      └─────────────────┘
```

---

## 1. Core Systems (50 APIs)

### 1.1 Memory System (23 APIs) ✅
```
tools/memory_*.py
├── MemoryStore                    [8 methods]
│   ├── write_entry()             → str (filepath)
│   ├── read_entry()              → MemoryEntry
│   ├── list_memories()           → List[str]
│   ├── search_by_tag()           → List[str]
│   ├── search_by_topic()         → List[str]
│   ├── search_by_date_range()    → List[str]
│   └── search()                  → List[Dict]
│
├── MemoryEntry                    [4 methods]
│   ├── to_markdown()             → str
│   ├── from_markdown()           → MemoryEntry
│   ├── update_access_time()
│   └── _compute_hash()           → str
│
├── QueryRouter (4-tier search)    [1 method]
│   └── search()                  → List[MemoryEntry]
│       ├── Tier 1: LRU Cache     (1.5ms avg)
│       ├── Tier 2: Index         (15ms avg)
│       ├── Tier 3: Grep          (100ms avg)
│       └── Tier 4: Deep scan     (500ms avg)
│
├── MemoryQuality                  [1 method]
│   └── score_memory()            → QualityScore (33 points)
│
├── MemorySecurityValidator        [1 method]
│   └── validate_entry()          → Tuple[bool, str]
│
└── FederationClient               [2 methods]
    ├── export_memories()         → KnowledgePackage
    └── import_package()          → List[str]

Status: ✅ 95% documented, well-architected
```

### 1.2 Message Signing (12 APIs) ✅
```
tools/sign_message.py
├── Ed25519Signer                  [7 methods]
│   ├── __init__(private_key_b64)
│   ├── sign(message)             → str (Base64 signature)
│   ├── get_public_key()          → str
│   ├── get_key_id()              → str (SHA-256 fingerprint)
│   ├── export_private_key()      → str
│   ├── from_private_key()        → Ed25519Signer
│   └── generate()                → Ed25519Signer
│
├── Ed25519Verifier                [3 methods]
│   ├── __init__(public_key_b64)
│   ├── verify(message, sig)      → bool
│   └── from_public_key()         → Ed25519Verifier
│
└── Helper Functions               [5 functions]
    ├── sign_hub_message()        → Dict
    ├── verify_hub_message()      → bool
    ├── generate_keypair()        → Tuple[str, str]
    ├── save_keypair()
    └── load_private_key()        → str

Status: ✅ 100% documented, production-ready
```

### 1.3 Dashboard System (4 APIs) ✅
```
view_dashboard.py + update_dashboard.py
├── FlowDashboard (Read-Only)     [7 methods]
│   ├── load()
│   ├── save()
│   ├── view_summary()
│   ├── view_detailed()
│   ├── view_untested()
│   ├── view_by_category()
│   └── view_history()
│
└── DashboardUpdater (Write)       [2 methods]
    ├── update_flow()             (status, success_rate, time, quality)
    └── increment_execution()

Status: ✅ 70% documented, clean separation
```

### 1.4 Hub CLI (11 APIs) ✅
```
team1-production-hub/scripts/hub_cli.py
├── Commands                       [4 functions]
│   ├── cmd_send()                (room, type, summary, body)
│   ├── cmd_list()                (room, since)
│   ├── cmd_watch()               (room, interval)
│   └── cmd_ping()                (room, note)
│
└── Helpers                        [7 functions]
    ├── env()                     → Optional[str]
    ├── run()                     → str (shell output)
    ├── ulid()                    → str (message ID)
    ├── ensure_clone()
    ├── git_pull()
    ├── git_commit_push()
    └── write_json()

Status: ✅ 85% documented, clear structure
```

---

## 2. Integration Systems (37 APIs)

### 2.1 Reporting Stack (12 APIs) ⚠️ REDUNDANT

#### Current State (Fragmented)
```
┌─────────────────────────────────────────────────┐
│          REPORTING FRAGMENTATION                │
│                                                 │
│  ┌──────────────┐  ┌──────────────┐            │
│  │ Email        │  │ Progress     │            │
│  │ Reporter     │  │ Reporter     │            │
│  │ (6 APIs)     │  │ (3 APIs)     │            │
│  └──────────────┘  └──────────────┘            │
│         │                   │                   │
│         └──────┬───────────┘                   │
│                │                                │
│         ┌──────▼───────┐                        │
│         │ Mission      │                        │
│         │ System       │                        │
│         │ (wraps both) │                        │
│         └──────────────┘                        │
└─────────────────────────────────────────────────┘

PROBLEM: 4 different entry points for same operation!
```

#### Email Reporter (6 APIs) ⚠️
```
tools/email_reporter.py
├── load_state()                   → Dict (NO TYPE HINTS)
├── send_email()                   (NO RETURN DOCUMENTED)
├── format_agent_report()          → str (HTML)
├── send_deployment_report()       (NO RETURN DOCUMENTED)
├── send_agent_update()            (NO RETURN DOCUMENTED)
└── send_collective_summary()      (NO RETURN DOCUMENTED)

Issues:
- ❌ No docstrings
- ❌ No type hints on returns
- ❌ Mixed abstraction levels
```

#### Progress Reporter (3 APIs) ⚠️
```
tools/progress_reporter.py
├── send_progress_email()          (NO DOCSTRING, NO TYPE HINTS)
├── send_hub_update()              (NO DOCSTRING, NO TYPE HINTS)
└── report_progress()              (NO DOCSTRING, NO TYPE HINTS)
    └─→ Calls both email + hub internally

Issues:
- ❌ Zero documentation
- ❌ Duplicate of email_reporter functionality
```

#### Mission System (3 APIs) ✅
```
tools/conductor_tools.py
├── Mission                        [8 methods]
│   ├── __init__(task)
│   ├── add_agent()
│   ├── start()
│   ├── update_agent()
│   ├── log_activity()
│   ├── complete_agent()
│   ├── complete()                → Auto email + GitHub
│   └── get_state()               → Dict
│
└── quick_mission()                (helper function)

Status: ✅ 90% documented, excellent abstraction
```

#### Proposed Consolidation
```
┌─────────────────────────────────────────────────┐
│          UNIFIED REPORTING (Proposed)            │
│                                                 │
│         ┌──────────────────────┐                │
│         │  Reporter (Unified)  │                │
│         │                      │                │
│         │  report(             │                │
│         │    type,             │                │
│         │    subject,          │                │
│         │    summary,          │                │
│         │    channels=[        │                │
│         │      EMAIL,          │                │
│         │      HUB,            │                │
│         │      GITHUB          │                │
│         │    ]                 │                │
│         │  )                   │                │
│         └──────────────────────┘                │
│                                                 │
│  Backward compatibility via wrappers            │
└─────────────────────────────────────────────────┘
```

### 2.2 State Management (3 APIs) ⚠️ DUPLICATE

#### Current Duplication
```
tools/email_reporter.py
    └── load_state()              → Dict (dashboard-state.json)

tools/github_backup.py
    └── load_latest_deployment()  → Dict (dashboard-state.json)

tools/conductor_tools.py
    └── Mission.get_state()       → Dict (internal state)

PROBLEM: 3 different loaders for same data!
```

#### Proposed Consolidation
```
tools/state_manager.py (New)
├── StateManager                   [6 methods]
│   ├── load()                    → Dict
│   ├── save(state)
│   ├── get_deployment()          → Dict
│   ├── get_agent_status()        → Dict
│   ├── update_deployment()
│   └── update_agent()

Benefits:
- ✅ Single source of truth
- ✅ Atomic updates
- ✅ Transaction support
- ✅ Better testing
```

### 2.3 GitHub Backup (8 APIs) ⚠️
```
tools/github_backup.py
├── Setup (One-time, 5 APIs)
│   ├── create_github_repo()
│   ├── init_git_repo()
│   ├── add_remote()
│   ├── create_gitignore()
│   └── setup_github_backup()
│
└── Runtime (3 APIs)
    ├── commit_and_push()
    ├── auto_backup()             (MAIN API)
    └── load_latest_deployment()

Issues:
- ❌ No docstrings
- ⚠️ Setup vs runtime mixed in same module
```

### 2.4 ADR004 Integration (5 APIs) ✅
```
tools/examples/adr004_integration_example.py
├── ADR004MessageBus               [5 methods]
│   ├── __init__()                (agent_id, keys, registry)
│   ├── send()                    → Auto-signs messages
│   ├── receive()                 → Auto-verifies messages
│   ├── _sign_message()
│   └── _verify_message()
│
└── Setup Helpers                  [2 functions]
    ├── setup_agent_keypairs()    → Dict
    └── create_agent_registry()   → Dict

Status: ✅ 100% documented, production-ready
```

---

## 3. Inter-Collective Protocol (Specification)

### 3.1 Message Format (Standard v1.0)
```
┌─────────────────────────────────────────────────┐
│  Inter-Collective API Standard v1.0             │
│  (88-page specification)                        │
│                                                 │
│  Core Message Schema:                           │
│  ┌─────────────────────────────────┐            │
│  │ {                               │            │
│  │   message_id: ULID,             │            │
│  │   timestamp: ISO 8601,          │            │
│  │   from: agent-id,               │            │
│  │   room: standard-room,          │            │
│  │   type: message-type,           │            │
│  │   summary: string,              │            │
│  │   body: string,                 │            │
│  │   metadata: object,             │            │
│  │   references: [ULIDs],          │            │
│  │   signature: {                  │            │
│  │     algorithm: "ed25519",       │            │
│  │     public_key: base64,         │            │
│  │     signature: base64,          │            │
│  │     signed_at: ISO 8601         │            │
│  │   }                             │            │
│  │ }                               │            │
│  └─────────────────────────────────┘            │
└─────────────────────────────────────────────────┘
```

### 3.2 Standard Rooms (7 Defined)
```
1. public        → Announcements, introductions
2. governance    → Voting, ADRs, policy decisions
3. research      → Knowledge sharing, findings
4. architecture  → Technical design, specifications
5. operations    → Task coordination, workflows
6. partnerships  → Cross-collective collaboration
7. incidents     → Issues, postmortems, alerts
```

### 3.3 Message Types (8 Standard)
```
1. text         → General communication
2. task         → Work assignment
3. response     → Task completion
4. question     → Information request
5. vote         → Democratic decision
6. adr          → Architectural decision record
7. finding      → Research result
8. alert        → Urgent notification
```

---

## 4. API Dependency Graph

### 4.1 Internal Dependencies
```
Mission System
    │
    ├─→ Email Reporter
    │       └─→ load_state()
    │
    ├─→ GitHub Backup
    │       ├─→ load_latest_deployment()
    │       └─→ auto_backup()
    │
    └─→ Dashboard State
            └─→ .claude/observatory/dashboard-state.json

Progress Reporter
    │
    ├─→ Email Reporter
    │       └─→ send_email()
    │
    └─→ Hub CLI
            └─→ cmd_send()

ADR004 Integration
    │
    └─→ Message Signing
            ├─→ Ed25519Signer
            └─→ Ed25519Verifier
```

### 4.2 External Dependencies
```
Hub CLI
    │
    ├─→ Git (command-line)
    ├─→ GitHub (remote repo)
    └─→ ULID generation

Email Reporter
    │
    └─→ Gmail SMTP (smtplib)

Memory System
    │
    ├─→ YAML (pyyaml)
    └─→ Filesystem

Message Signing
    │
    └─→ Ed25519 (cryptography library)
```

---

## 5. API Maturity Matrix

| System | APIs | Docs | Types | Tests | Versioned | Maturity |
|--------|------|------|-------|-------|-----------|----------|
| **Memory** | 23 | 95% | ✅ | ✅ | ❌ | **Alpha** |
| **Signing** | 12 | 100% | ✅ | ✅ | ❌ | **Beta** |
| **Mission** | 5 | 90% | ✅ | ⚠️ | ❌ | **Beta** |
| **Dashboard** | 4 | 70% | ✅ | ⚠️ | ❌ | **Alpha** |
| **Hub CLI** | 11 | 85% | ✅ | ❌ | ❌ | **Alpha** |
| **Email** | 6 | 40% | ❌ | ❌ | ❌ | **Pre-Alpha** |
| **Progress** | 3 | 20% | ❌ | ❌ | ❌ | **Pre-Alpha** |
| **GitHub** | 8 | 30% | ❌ | ❌ | ❌ | **Pre-Alpha** |
| **ADR004** | 5 | 100% | ✅ | ✅ | ❌ | **Beta** |
| **Protocol** | Spec | 100% | N/A | N/A | v1.0 | **Stable** |

**Legend**:
- Pre-Alpha: <50% docs, no tests, no types
- Alpha: 50-75% docs, some tests, some types
- Beta: 75-95% docs, good tests, full types
- Stable: 100% docs, full tests, versioned

---

## 6. Critical Paths

### 6.1 Mission Execution Flow
```
User → Mission.start()
         │
         ├─→ Dashboard update (state.json)
         │
         ├─→ Mission.update_agent()
         │     └─→ Dashboard update
         │
         ├─→ Mission.complete_agent()
         │     └─→ Email Reporter.send_agent_update()
         │
         └─→ Mission.complete()
               ├─→ Email Reporter.send_deployment_report()
               └─→ GitHub Backup.auto_backup()
```

### 6.2 Inter-Collective Communication Flow
```
Agent → Hub CLI.cmd_send()
          │
          ├─→ Create message (ULID, timestamp)
          │
          ├─→ Sign message (Ed25519)
          │     └─→ sign_hub_message()
          │
          ├─→ Write JSON to room/
          │
          ├─→ Git commit + push
          │
          └─→ GitHub Actions notify recipients
                └─→ Create issue comment
```

### 6.3 Memory Write Flow
```
Agent → Should write memory?
          │
          ├─→ MemoryTriggerDetector.should_write_memory()
          │     └─→ Checks 8 trigger conditions
          │
          ├─→ Create MemoryEntry
          │     ├─→ Validate type/confidence/visibility
          │     ├─→ Compute content hash
          │     └─→ Score quality (33 points)
          │
          ├─→ Security scan
          │     └─→ MemorySecurityValidator.validate_entry()
          │
          ├─→ Write to disk
          │     └─→ MemoryStore.write_entry()
          │
          └─→ Update indexes
                └─→ MemoryIndexer.build_index()
```

---

## 7. API Surface by Category

### Data Operations (35 APIs)
```
Memory: read, write, search, index         (23)
State: load, save, update                  (3)
GitHub: commit, push, load                 (8)
Hub: send, receive, list                   (4)
```

### Authentication & Security (17 APIs)
```
Signing: generate, sign, verify            (12)
Memory Security: scan, validate, control   (3)
Federation: sign packages, verify          (2)
```

### Reporting & Notifications (12 APIs)
```
Email: send, format, notify                (6)
Progress: report dual-channel              (3)
Mission: complete, update                  (3)
```

### UI & Visualization (11 APIs)
```
Dashboard: view, update, history           (9)
Web: REST endpoints, WebSocket             (2)
```

### Utility & Helpers (12 APIs)
```
Hub: git ops, ULID, JSON                   (7)
Signing: keypair, save, load               (3)
Memory: hash, quality, dedup               (2)
```

---

## 8. Version Compatibility (Proposed)

### Versioning Strategy
```
┌─────────────────────────────────────────────────┐
│  Semantic Versioning (SemVer 2.0.0)             │
│                                                 │
│  MAJOR.MINOR.PATCH                              │
│                                                 │
│  MAJOR: Breaking changes                        │
│    - Remove functions                           │
│    - Change signatures (non-optional params)    │
│    - Change return types (incompatible)         │
│                                                 │
│  MINOR: Backward-compatible additions           │
│    - Add new functions                          │
│    - Add optional parameters                    │
│    - Add new return fields                      │
│                                                 │
│  PATCH: Bug fixes                               │
│    - Fix incorrect behavior                     │
│    - Performance improvements                   │
│    - Documentation updates                      │
└─────────────────────────────────────────────────┘
```

### Proposed Module Versions
```
tools/memory_core.py        → v1.0.0 (stable)
tools/sign_message.py       → v1.0.0 (stable)
tools/conductor_tools.py    → v1.0.0 (stable)
tools/email_reporter.py     → v0.9.0 (pre-release, needs docs)
tools/progress_reporter.py  → v0.8.0 (pre-release, needs docs)
tools/github_backup.py      → v0.9.0 (pre-release, needs docs)
view_dashboard.py           → v1.0.0 (stable)
```

---

## 9. Integration Points

### Internal Integration
```
┌────────────┐    ┌────────────┐    ┌────────────┐
│  Mission   │───→│   Email    │───→│   SMTP     │
│  System    │    │  Reporter  │    │  Gmail     │
└────────────┘    └────────────┘    └────────────┘
       │
       ├─→ GitHub Backup ───→ Git ───→ GitHub
       │
       └─→ Dashboard State ───→ JSON File ───→ Web UI
```

### External Integration
```
┌────────────┐    ┌────────────┐    ┌────────────┐
│  Hub CLI   │───→│  Git Repo  │───→│  GitHub    │
│            │    │  (Comms)   │    │  Actions   │
└────────────┘    └────────────┘    └────────────┘
       │                                    │
       └─→ Ed25519 Signing                 │
                                            ↓
                                    ┌────────────┐
                                    │  Sibling   │
                                    │ Collective │
                                    └────────────┘
```

---

## 10. Recommended Refactoring

### Current State Problems
```
❌ 4 reporting interfaces (email, progress, mission, direct)
❌ 3 state loaders (email, github, mission)
❌ 20 functions without docstrings
❌ No API versioning
❌ Mixed abstraction levels
```

### Target State Goals
```
✅ 2 reporting interfaces (Mission + Reporter)
✅ 1 state manager (StateManager)
✅ 100% documented functions
✅ All APIs versioned (SemVer)
✅ Clean separation of concerns
```

### Refactoring Roadmap
```
Week 1: Critical Fixes
├── Add API versioning decorators
├── Consolidate reporting (4→2)
└── Complete documentation (20 docstrings)

Week 2: Consistency
├── Standardize naming (load vs read)
├── Unified state manager
└── OpenAPI specification

Week 3: Enhancement
├── Unified search facade
└── Class-based APIs (email, github, progress)
```

---

**See Also**:
- [API-INTERFACE-REVIEW.md](API-INTERFACE-REVIEW.md) - Full detailed analysis
- [API-REVIEW-EXECUTIVE-SUMMARY.md](API-REVIEW-EXECUTIVE-SUMMARY.md) - Quick overview
- [INTER-COLLECTIVE-API-STANDARD-v1.0.md](INTER-COLLECTIVE-API-STANDARD-v1.0.md) - Protocol spec
