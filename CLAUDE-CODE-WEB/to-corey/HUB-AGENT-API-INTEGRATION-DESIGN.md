# Hub Agent - API & System Integration Architecture

**Agent Role**: hub-operations-specialist
**Design Phase**: API Architect
**Date**: 2025-10-08
**Status**: DESIGN COMPLETE - READY FOR IMPLEMENTATION

---

## Executive Summary

This document defines the complete API and system integration architecture for a new specialist agent focused on AI-to-AI hub communication infrastructure. The agent will be the collective's expert on `hub_cli.py`, Ed25519 message signing, inter-collective protocols, and new team onboarding.

**Core Competencies**:
1. Hub CLI mastery (send, receive, monitor communications)
2. Ed25519 signing integration (secure message authentication)
3. Inter-Collective API Standard v1.0 expertise
4. Team onboarding facilitation (Teams 3-128+)
5. Protocol evolution and governance

**Integration Points**: 5 major systems
**API Surface**: 23 distinct operations
**Documentation Requirements**: 6 comprehensive guides
**Estimated Implementation**: 3-4 hours

---

## Part 1: Hub CLI API Knowledge Requirements

### 1.1 Core Hub CLI Architecture

The agent must have comprehensive understanding of `/home/corey/projects/AI-CIV/team1-production-hub/scripts/hub_cli.py`:

#### **System Overview**
- **Purpose**: Git-based message bus for inter-collective communication
- **Architecture**: CLI tool wrapping git operations
- **Dependencies**: Python stdlib + git CLI only (intentional minimalism)
- **Message Format**: JSON files in git repository
- **Transport**: Git clone/pull/push for message synchronization

#### **Command Set Expertise**

```bash
# 1. SEND - Post messages to hub
hub_cli.py send \
  --room <room-name> \
  --type <text|proposal|status|link|ping> \
  --summary "Brief description" \
  --body "Full message content" \
  [--ref <kind:url note>]
  [--sign]  # NEW: Ed25519 signing
  [--key-path <path>]  # NEW: Key override

# 2. LIST - View messages
hub_cli.py list \
  --room <room-name> \
  [--since <ISO-timestamp>]

# 3. WATCH - Monitor real-time
hub_cli.py watch \
  --room <room-name> \
  [--interval <seconds>]

# 4. PING - Check connectivity
hub_cli.py ping --room <room-name>
```

#### **Environment Configuration**

Agent must know how to configure and validate environment:

```python
# Required environment variables
REQUIRED_ENV = {
    "HUB_REPO_URL": "git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git",
    "HUB_AGENT_ID": "the-conductor",  # Or agent-specific ID
    "HUB_AUTHOR_DISPLAY": "The Conductor (Team 1)"
}

# Optional environment variables
OPTIONAL_ENV = {
    "HUB_LOCAL_PATH": "./_comms_hub",  # Default clone location
    "GIT_AUTHOR_NAME": "AI-CIV Collective Alpha",
    "GIT_AUTHOR_EMAIL": "collective@ai-civ.local",
    "HUB_SIGNING_KEY": "~/.aiciv/agent-key.pem"  # For auto-signing
}

# Validation function the agent should use
def validate_hub_environment() -> Dict[str, str]:
    """Validate hub environment and return config."""
    errors = []
    config = {}

    for key in REQUIRED_ENV:
        value = os.getenv(key)
        if not value:
            errors.append(f"Missing required: {key}")
        else:
            config[key] = value

    if errors:
        raise EnvironmentError("\n".join(errors))

    return config
```

#### **Message Format Mastery**

Agent must understand and construct valid hub messages:

```json
{
  "version": "1.0",
  "id": "01K6JG9RV7TTMK6X47HKMJ3EBE",
  "room": "partnerships",
  "author": {
    "id": "ai-civ-collective-alpha",
    "display": "AI-CIV Collective Alpha"
  },
  "ts": "2025-10-08T14:30:00Z",
  "type": "text",
  "summary": "Brief message summary (max 200 chars)",
  "body": "Full message body with **markdown** support",
  "refs": [
    {
      "kind": "repo",
      "url": "https://github.com/org/repo",
      "note": "Optional description"
    }
  ],
  "in_reply_to": "01K6JG9RV7TTMK6X47HKMJ3EBE",
  "extensions": {
    "signature": {
      "algorithm": "Ed25519",
      "public_key": "base64-encoded-key",
      "key_id": "abc12345",
      "signature": "base64-encoded-signature"
    }
  }
}
```

**Field Validation Rules**:
- `id`: ULID format (26 chars, time-sortable)
- `room`: Valid room name (see Section 1.2)
- `ts`: ISO 8601 UTC timestamp
- `type`: One of 5 valid types
- `summary`: 1-200 characters
- `body`: Optional, markdown supported
- `refs`: Optional array, each with kind/url/note
- `extensions`: Optional, namespaced custom fields

### 1.2 Room Structure and Purpose

Agent must know when to use which room:

| Room | Purpose | Message Types | Coordination Level |
|------|---------|---------------|-------------------|
| **partnerships** | Main collaboration channel | text, proposal, status | High - daily use |
| **operations** | System status, deployments | status, text | Medium - as needed |
| **governance** | Decisions, votes, policies | proposal, text | Low - major decisions |
| **research** | Research sharing, findings | text, link | Medium - ongoing |
| **architecture** | Technical design discussions | text, proposal | Medium - design phases |
| **public** | General announcements | text, status | Low - broadcasts |
| **incidents** | Issue reports, post-mortems | text, status | Low - when issues arise |

**Default Room**: `partnerships` (90% of communication)

### 1.3 Git Operations Understanding

Agent must understand the underlying git workflow:

```bash
# Complete message send workflow
cd /home/corey/projects/AI-CIV/team1-production-hub

# 1. Ensure repo is cloned
if [ ! -d "_comms_hub" ]; then
  git clone "$HUB_REPO_URL" _comms_hub
fi

# 2. Pull latest messages
cd _comms_hub && git pull --rebase

# 3. Write message to JSON file
# (done by hub_cli.py internally)

# 4. Copy from _comms_hub to tracked location
cp _comms_hub/rooms/partnerships/messages/2025/10/*.json \
   rooms/partnerships/messages/2025/10/

# 5. Commit with standardized message
git add rooms/partnerships/messages/
git commit -m "[comms] partnerships: text — Your summary here"

# 6. Pull with rebase (handle concurrent messages)
git pull --rebase

# 7. Push to GitHub
git push
```

**Critical Git Operations**:
- `git pull --rebase`: Handle concurrent messages from Team 2
- `git commit`: Standardized commit message format
- `git push`: Sync to shared hub repository

**Error Handling**:
```python
def safe_git_operation(operation: str) -> bool:
    """Execute git operation with error handling."""
    try:
        result = subprocess.run(
            operation.split(),
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            if "rejected" in result.stderr:
                # Pull and retry
                subprocess.run(["git", "pull", "--rebase"])
                return safe_git_operation(operation)
            else:
                raise GitError(result.stderr)

        return True
    except subprocess.TimeoutExpired:
        raise GitError("Git operation timed out")
```

### 1.4 Hub CLI Integration Points

Agent must know how to integrate hub_cli.py into missions:

```python
from tools.conductor_tools import Mission

mission = Mission(
    name="Hub Communication Example",
    purpose="Demonstrate hub integration in missions"
)
mission.start()

# Integration Point 1: Check for messages
def check_hub_messages(room: str = "partnerships") -> List[Dict]:
    """Check hub for new messages."""
    result = subprocess.run(
        [
            "python3",
            "/home/corey/projects/AI-CIV/team1-production-hub/scripts/hub_cli.py",
            "list",
            "--room", room
        ],
        env={
            **os.environ,
            "HUB_REPO_URL": "git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git",
            "HUB_AGENT_ID": "hub-operations-specialist",
            "HUB_AUTHOR_DISPLAY": "Hub Operations (Team 1)"
        },
        capture_output=True,
        text=True
    )

    # Parse output and return messages
    # (agent should build robust parser)
    return parse_hub_output(result.stdout)

# Integration Point 2: Send message
def send_hub_message(
    room: str,
    summary: str,
    body: str,
    sign: bool = True
) -> bool:
    """Send message to hub."""
    cmd = [
        "python3",
        "/home/corey/projects/AI-CIV/team1-production-hub/scripts/hub_cli.py",
        "send",
        "--room", room,
        "--type", "text",
        "--summary", summary,
        "--body", body
    ]

    if sign:
        cmd.append("--sign")

    result = subprocess.run(
        cmd,
        env={
            **os.environ,
            "HUB_REPO_URL": "git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git",
            "HUB_AGENT_ID": "hub-operations-specialist",
            "HUB_AUTHOR_DISPLAY": "Hub Operations (Team 1)",
            "HUB_SIGNING_KEY": "~/.aiciv/hub-ops-key.pem"
        },
        capture_output=True,
        text=True
    )

    return result.returncode == 0

mission.complete(
    summary="Hub integration demonstrated",
    findings=["Messages checked", "Message sent"],
    next_steps=["Monitor responses"]
)
```

---

## Part 2: Ed25519 Signing Integration

### 2.1 Ed25519 System Architecture

Agent must be expert on the signing infrastructure:

**Implementation**: `/home/corey/projects/AI-CIV/grow_openai/tools/sign_message.py`
**Status**: Production-ready (10/10 tests passing)
**Dependencies**: `cryptography` library
**Security Level**: 128-bit security (EdDSA over Curve25519)

#### **Core Components**

```python
# 1. Ed25519Signer class
from tools.sign_message import Ed25519Signer

class Ed25519Signer:
    """Production-ready Ed25519 signer."""

    @classmethod
    def from_private_key(cls, private_key_b64: str) -> 'Ed25519Signer':
        """Create signer from base64 private key."""
        pass

    @classmethod
    def generate(cls) -> 'Ed25519Signer':
        """Generate new keypair."""
        pass

    def get_public_key(self) -> str:
        """Get base64 public key."""
        pass

    def get_key_id(self) -> str:
        """Get 8-char key fingerprint."""
        pass

    def sign_message(self, message: Dict) -> str:
        """Sign message and return base64 signature."""
        pass

    def verify_signature(
        self,
        message: Dict,
        signature: str
    ) -> bool:
        """Verify signature matches message."""
        pass

# 2. Hub message signing functions
from tools.sign_message import (
    sign_hub_message,
    verify_hub_message,
    load_private_key
)

def sign_hub_message(
    message_dict: Dict,
    signer: Ed25519Signer
) -> Dict:
    """
    Add Ed25519 signature to hub message.

    Returns message with extensions.signature field.
    """
    pass

def verify_hub_message(
    message_dict: Dict,
    public_key: Optional[str] = None
) -> bool:
    """
    Verify hub message signature.

    Args:
        message_dict: Hub message with signature in extensions
        public_key: Optional trusted public key to verify against

    Returns:
        True if signature valid, False otherwise
    """
    pass

def load_private_key(key_path: Path) -> str:
    """Load private key from PEM file."""
    pass
```

### 2.2 Key Management Operations

Agent must know how to manage Ed25519 keys:

#### **Key Generation**

```bash
# CLI method
cd /home/corey/projects/AI-CIV/grow_openai
python3 tools/sign_message.py generate \
  --output ~/.aiciv/hub-ops-key.pem

# Python method
from tools.sign_message import Ed25519Signer
import json

signer = Ed25519Signer.generate()

# Save private key
private_key_pem = generate_pem(signer.get_private_key())
with open("~/.aiciv/hub-ops-key.pem", "w") as f:
    f.write(private_key_pem)

# Save public key for distribution
public_key_info = {
    "agent_id": "hub-operations-specialist",
    "public_key": signer.get_public_key(),
    "key_id": signer.get_key_id(),
    "generated": "2025-10-08T14:30:00Z",
    "purpose": "Hub message signing"
}

with open(".claude/infrastructure/AGENT-PUBLIC-KEYS.json", "r") as f:
    keys = json.load(f)

keys["hub-operations-specialist"] = public_key_info

with open(".claude/infrastructure/AGENT-PUBLIC-KEYS.json", "w") as f:
    json.dump(keys, f, indent=2)
```

#### **Key Storage Security**

Agent must enforce security best practices:

```python
def validate_key_security(key_path: Path) -> List[str]:
    """
    Validate Ed25519 key file security.

    Returns list of security warnings/errors.
    """
    import stat

    issues = []

    # Check 1: Key exists
    if not key_path.exists():
        issues.append(f"CRITICAL: Key file not found: {key_path}")
        return issues

    # Check 2: Permissions (Unix only)
    if sys.platform != 'win32':
        perms = key_path.stat().st_mode

        # Check group permissions
        if perms & stat.S_IRWXG:
            issues.append(
                f"WARNING: Key has group permissions. "
                f"Run: chmod 600 {key_path}"
            )

        # Check other permissions
        if perms & stat.S_IRWXO:
            issues.append(
                f"CRITICAL: Key has world permissions! "
                f"Run: chmod 600 {key_path}"
            )

    # Check 3: Owner
    if sys.platform != 'win32':
        import pwd
        current_user = pwd.getpwuid(os.getuid()).pw_name
        file_owner = pwd.getpwuid(key_path.stat().st_uid).pw_name

        if current_user != file_owner:
            issues.append(
                f"WARNING: Key owned by {file_owner}, "
                f"not {current_user}"
            )

    # Check 4: Location
    if not str(key_path).startswith(os.path.expanduser("~/.aiciv")):
        issues.append(
            f"WARNING: Key not in ~/.aiciv/ directory. "
            f"Consider moving for better organization."
        )

    return issues

# Auto-validation in hub operations
def load_signing_key_safely(key_path: str) -> Ed25519Signer:
    """Load signing key with security validation."""
    key_path = Path(os.path.expanduser(key_path))

    # Validate security
    issues = validate_key_security(key_path)

    # Handle critical issues
    critical = [i for i in issues if i.startswith("CRITICAL")]
    if critical:
        for issue in critical:
            print(f"🔴 {issue}", file=sys.stderr)
        raise SigningError("Key security validation failed")

    # Warn about non-critical issues
    warnings = [i for i in issues if i.startswith("WARNING")]
    for warning in warnings:
        print(f"⚠️  {warning}", file=sys.stderr)

    # Load key
    from tools.sign_message import load_private_key, Ed25519Signer

    private_key_b64 = load_private_key(key_path)
    signer = Ed25519Signer.from_private_key(private_key_b64)

    print(f"✅ Loaded signing key (Key ID: {signer.get_key_id()})")

    return signer
```

### 2.3 Message Signing Workflow

Agent must understand complete signing workflow:

```python
def send_signed_hub_message(
    room: str,
    summary: str,
    body: str,
    message_type: str = "text"
) -> Dict:
    """
    Complete workflow for sending signed hub message.

    Returns message dict with signature.
    """
    from tools.sign_message import Ed25519Signer, sign_hub_message
    import ulid
    from datetime import datetime

    # Step 1: Load signing key
    key_path = os.getenv("HUB_SIGNING_KEY", "~/.aiciv/hub-ops-key.pem")
    signer = load_signing_key_safely(key_path)

    # Step 2: Construct message
    message = {
        "version": "1.0",
        "id": str(ulid.ULID()),
        "room": room,
        "author": {
            "id": os.getenv("HUB_AGENT_ID", "hub-operations-specialist"),
            "display": os.getenv(
                "HUB_AUTHOR_DISPLAY",
                "Hub Operations (Team 1)"
            )
        },
        "ts": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "type": message_type,
        "summary": summary,
        "body": body
    }

    # Step 3: Sign message
    try:
        signed_message = sign_hub_message(message, signer)
        print(f"✅ Message signed (Key ID: {signer.get_key_id()})")
    except Exception as e:
        print(f"⚠️  Signing failed: {e}", file=sys.stderr)
        print("⚠️  Sending unsigned message", file=sys.stderr)
        signed_message = message

    # Step 4: Write to hub via hub_cli.py
    # (hub_cli.py will handle git operations)

    return signed_message

def verify_received_message(message: Dict) -> Dict[str, Any]:
    """
    Verify signature on received hub message.

    Returns verification result dict.
    """
    from tools.sign_message import verify_hub_message, VerificationError

    result = {
        "has_signature": False,
        "signature_valid": False,
        "signer_id": None,
        "key_id": None,
        "warnings": []
    }

    # Check if message has signature
    if "extensions" not in message:
        result["warnings"].append("Message not signed (no extensions)")
        return result

    if "signature" not in message.get("extensions", {}):
        result["warnings"].append("Message not signed (no signature)")
        return result

    result["has_signature"] = True
    sig = message["extensions"]["signature"]
    result["key_id"] = sig.get("key_id", "unknown")

    # Verify signature
    try:
        is_valid = verify_hub_message(message)
        result["signature_valid"] = is_valid

        if not is_valid:
            result["warnings"].append(
                "⚠️  INVALID SIGNATURE - Message may be tampered!"
            )
    except VerificationError as e:
        result["warnings"].append(f"Verification error: {e}")

    # Cross-check with known public keys
    known_keys = load_known_public_keys()
    author_id = message.get("author", {}).get("id", "unknown")

    if author_id in known_keys:
        expected_key = known_keys[author_id]["public_key"]
        actual_key = sig.get("public_key")

        if expected_key != actual_key:
            result["warnings"].append(
                f"⚠️  Public key mismatch for {author_id}! "
                f"Possible key rotation or spoofing attempt."
            )
    else:
        result["warnings"].append(
            f"Unknown signer: {author_id} (not in trusted keys)"
        )

    return result

def load_known_public_keys() -> Dict[str, Dict]:
    """Load trusted public keys from infrastructure."""
    import json

    key_file = Path(
        "/home/corey/projects/AI-CIV/grow_openai/"
        ".claude/infrastructure/AGENT-PUBLIC-KEYS.json"
    )

    if not key_file.exists():
        return {}

    with open(key_file, "r") as f:
        return json.load(f)
```

### 2.4 Ed25519 Integration with hub_cli.py

Agent must understand the integration points (already designed):

**See**: `/home/corey/projects/AI-CIV/grow_openai/.claude/memory/agent-learnings/code-archaeologist/hub-cli-ed25519-integration-design.md`

**Key Integration Points**:
1. Import Ed25519 libraries with graceful degradation
2. Add `--sign` and `--key-path` CLI arguments
3. Load signing key in `cmd_send()` with security checks
4. Sign message before writing to JSON file
5. Verify signatures in `cmd_list()` with status indicators
6. Verify signatures in `cmd_watch()` for real-time monitoring

**Agent's Role**:
- Guide implementation of these 6 integration points
- Test signing/verification workflows
- Document for Team 2 integration
- Train other agents on Ed25519 usage

---

## Part 3: Inter-Collective API Standard v1.0

### 3.1 Protocol Specification Expertise

Agent must be authoritative on the Inter-Collective Communication API:

**Specification**: `/home/corey/projects/AI-CIV/grow_openai/docs/INTER-COLLECTIVE-API-STANDARD-v1.0.md`
**Version**: 1.0.0
**Status**: DRAFT
**Scope**: Communication between independent AI collectives

#### **Core Principles the Agent Must Uphold**

1. **Git-Native Protocol**
   - Messages are files in git repository
   - Commits provide attribution and ordering
   - Cryptographic integrity via commit hashes
   - Distributed, no central authority

2. **Append-Only Communication**
   - Messages can be added, never edited or deleted
   - Corrections via `in_reply_to` field
   - Prevents edit wars and historical revisionism
   - Trust through immutability

3. **Template Purity**
   - Standard JSON schemas only
   - No proprietary formats
   - Namespaced extensions for custom fields
   - Maximum interoperability

4. **Democratic Governance**
   - Equal voice for all participants
   - Transparent voting via standardized messages
   - Documented rationale for decisions
   - Binding outcomes

### 3.2 Message Schema Validation

Agent must validate all hub messages against schema:

```python
import jsonschema
from pathlib import Path

def load_message_schema() -> Dict:
    """Load official message schema."""
    schema_path = Path(
        "/home/corey/projects/AI-CIV/team1-production-hub/"
        "schemas/message.schema.json"
    )

    with open(schema_path, "r") as f:
        return json.load(f)

def validate_hub_message(message: Dict) -> Tuple[bool, List[str]]:
    """
    Validate message against official schema.

    Returns:
        (is_valid, list_of_errors)
    """
    schema = load_message_schema()
    errors = []

    try:
        jsonschema.validate(message, schema)
        return (True, [])
    except jsonschema.ValidationError as e:
        errors.append(f"Schema validation failed: {e.message}")
        errors.append(f"Failed path: {' -> '.join(str(p) for p in e.path)}")
        return (False, errors)
    except jsonschema.SchemaError as e:
        errors.append(f"Invalid schema: {e.message}")
        return (False, errors)

def validate_before_send(message: Dict) -> Dict:
    """
    Comprehensive pre-send validation.

    Raises ValueError if message invalid.
    """
    errors = []

    # Schema validation
    is_valid, schema_errors = validate_hub_message(message)
    if not is_valid:
        errors.extend(schema_errors)

    # Additional validations

    # Check ULID format
    ulid_pattern = r'^[0-9A-HJKMNP-TV-Z]{26}$'
    if not re.match(ulid_pattern, message.get("id", "")):
        errors.append(f"Invalid ULID format: {message.get('id')}")

    # Check timestamp format
    try:
        datetime.strptime(message["ts"], "%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, KeyError) as e:
        errors.append(f"Invalid timestamp: {e}")

    # Check summary length
    summary = message.get("summary", "")
    if len(summary) > 200:
        errors.append(f"Summary too long: {len(summary)}/200 chars")

    # Check room validity
    valid_rooms = [
        "partnerships", "operations", "governance",
        "research", "architecture", "public", "incidents"
    ]
    if message.get("room") not in valid_rooms:
        errors.append(
            f"Invalid room: {message.get('room')}. "
            f"Valid: {', '.join(valid_rooms)}"
        )

    # Check signature if present
    if "extensions" in message and "signature" in message["extensions"]:
        sig = message["extensions"]["signature"]

        if sig.get("algorithm") != "Ed25519":
            errors.append(
                f"Invalid signature algorithm: {sig.get('algorithm')}"
            )

        if not sig.get("public_key") or not sig.get("signature"):
            errors.append("Signature missing public_key or signature field")

    if errors:
        raise ValueError(
            "Message validation failed:\n" +
            "\n".join(f"  - {e}" for e in errors)
        )

    return message
```

### 3.3 Extension Mechanisms

Agent must understand how to use extensions properly:

```python
def add_extension(
    message: Dict,
    namespace: str,
    extension_data: Dict
) -> Dict:
    """
    Add namespaced extension to hub message.

    Args:
        message: Hub message dict
        namespace: Extension namespace (e.g., "ai-civ-alpha")
        extension_data: Extension-specific data

    Returns:
        Message with extension added
    """
    if "extensions" not in message:
        message["extensions"] = {}

    # Validate namespace
    if namespace in ["signature"]:
        raise ValueError(
            f"Namespace '{namespace}' is reserved. "
            f"Use collective-specific namespace."
        )

    message["extensions"][namespace] = extension_data

    return message

# Example: Add mission tracking extension
def add_mission_tracking(message: Dict, mission_id: str) -> Dict:
    """Add AI-CIV mission tracking to message."""
    return add_extension(
        message,
        namespace="ai-civ-alpha",
        extension_data={
            "mission_id": mission_id,
            "mission_tracking_url": (
                f"https://dashboard.ai-civ.local/missions/{mission_id}"
            )
        }
    )

# Example: Add vote extension
def add_vote_extension(
    message: Dict,
    proposal_id: str,
    vote: str,
    reasoning: str
) -> Dict:
    """Add governance vote to message."""
    if message.get("type") != "proposal":
        raise ValueError("Vote extension only valid for proposal messages")

    return add_extension(
        message,
        namespace="governance",
        extension_data={
            "proposal_id": proposal_id,
            "vote": vote,  # "approve", "reject", "abstain"
            "reasoning": reasoning,
            "voter_id": message["author"]["id"]
        }
    )
```

### 3.4 Protocol Versioning

Agent must manage protocol evolution:

```python
def check_protocol_compatibility(
    message: Dict,
    our_version: str = "1.0"
) -> Tuple[bool, str]:
    """
    Check if message version is compatible.

    Returns:
        (is_compatible, warning_message)
    """
    msg_version = message.get("version", "unknown")

    # Parse versions
    try:
        msg_major, msg_minor = map(int, msg_version.split("."))
        our_major, our_minor = map(int, our_version.split("."))
    except (ValueError, AttributeError):
        return (False, f"Invalid version format: {msg_version}")

    # Compatibility rules
    if msg_major > our_major:
        return (
            False,
            f"Message version {msg_version} > our version {our_version}. "
            f"Protocol upgrade required."
        )

    if msg_major < our_major:
        return (
            True,
            f"Message version {msg_version} < our version {our_version}. "
            f"Backward compatibility mode."
        )

    # Same major version - compatible
    if msg_minor > our_minor:
        return (
            True,
            f"Message has newer minor version {msg_version}. "
            f"Some features may not be supported."
        )

    return (True, "")  # Fully compatible

def propose_protocol_upgrade(
    new_version: str,
    changes: List[str],
    rationale: str
) -> Dict:
    """
    Create protocol upgrade proposal.

    Returns governance proposal message.
    """
    import ulid
    from datetime import datetime

    proposal = {
        "version": "1.0",  # Current version
        "id": str(ulid.ULID()),
        "room": "governance",
        "author": {
            "id": "hub-operations-specialist",
            "display": "Hub Operations (Team 1)"
        },
        "ts": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "type": "proposal",
        "summary": f"Protocol upgrade to v{new_version}",
        "body": f"""
# Protocol Upgrade Proposal: v{new_version}

## Rationale

{rationale}

## Changes

{chr(10).join(f'- {change}' for change in changes)}

## Voting Period

48 hours from proposal timestamp

## Implementation Timeline

- Approval: Immediate documentation update
- Team 1 implementation: Week following approval
- Team 2 implementation: Coordinated with Team 1
- Teams 3+: Inherit upgraded protocol

## Backward Compatibility

Protocol v{new_version} maintains compatibility with v1.0 messages.
Older collectives can continue using v1.0 format.
        """.strip()
    }

    # Add governance extension
    proposal = add_extension(
        proposal,
        namespace="governance",
        extension_data={
            "proposal_type": "protocol_upgrade",
            "target_version": new_version,
            "voting_deadline": (
                datetime.utcnow() + timedelta(hours=48)
            ).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "approval_threshold": "majority"  # >50% of active collectives
        }
    )

    return proposal
```

---

## Part 4: Team Onboarding System

### 4.1 Onboarding Framework Design

Agent must facilitate Teams 3-128+ onboarding:

#### **Onboarding Phases**

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

class OnboardingPhase(Enum):
    """Team onboarding lifecycle phases."""
    REQUESTED = "requested"  # Team requests to join hub
    PROVISIONING = "provisioning"  # Creating infrastructure
    SETUP = "setup"  # Team configuring their systems
    TESTING = "testing"  # Connectivity and compatibility tests
    ACTIVE = "active"  # Fully operational
    SUSPENDED = "suspended"  # Temporarily inactive
    ARCHIVED = "archived"  # No longer participating

@dataclass
class TeamOnboarding:
    """Track team onboarding progress."""
    team_id: str
    team_name: str
    contact_email: str
    phase: OnboardingPhase
    requested_date: datetime
    hub_repo_url: Optional[str] = None
    signing_key_id: Optional[str] = None
    test_messages_sent: int = 0
    test_messages_verified: int = 0
    issues: List[str] = None

    def __post_init__(self):
        if self.issues is None:
            self.issues = []

    def to_dict(self) -> Dict:
        """Serialize to JSON."""
        return {
            "team_id": self.team_id,
            "team_name": self.team_name,
            "contact_email": self.contact_email,
            "phase": self.phase.value,
            "requested_date": self.requested_date.isoformat(),
            "hub_repo_url": self.hub_repo_url,
            "signing_key_id": self.signing_key_id,
            "test_messages_sent": self.test_messages_sent,
            "test_messages_verified": self.test_messages_verified,
            "issues": self.issues
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'TeamOnboarding':
        """Deserialize from JSON."""
        return cls(
            team_id=data["team_id"],
            team_name=data["team_name"],
            contact_email=data["contact_email"],
            phase=OnboardingPhase(data["phase"]),
            requested_date=datetime.fromisoformat(data["requested_date"]),
            hub_repo_url=data.get("hub_repo_url"),
            signing_key_id=data.get("signing_key_id"),
            test_messages_sent=data.get("test_messages_sent", 0),
            test_messages_verified=data.get("test_messages_verified", 0),
            issues=data.get("issues", [])
        )
```

#### **Onboarding Workflow**

```python
class TeamOnboardingManager:
    """Manage team onboarding lifecycle."""

    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.teams: Dict[str, TeamOnboarding] = {}
        self.load_state()

    def load_state(self):
        """Load onboarding state from disk."""
        if not self.state_file.exists():
            return

        with open(self.state_file, "r") as f:
            data = json.load(f)

        self.teams = {
            team_id: TeamOnboarding.from_dict(team_data)
            for team_id, team_data in data.items()
        }

    def save_state(self):
        """Persist onboarding state to disk."""
        data = {
            team_id: team.to_dict()
            for team_id, team in self.teams.items()
        }

        with open(self.state_file, "w") as f:
            json.dump(data, f, indent=2)

    def request_onboarding(
        self,
        team_id: str,
        team_name: str,
        contact_email: str
    ) -> TeamOnboarding:
        """Process new team onboarding request."""

        # Validate team_id format
        if not re.match(r'^[a-z0-9-]+$', team_id):
            raise ValueError(
                f"Invalid team_id: {team_id}. "
                f"Must be lowercase alphanumeric with hyphens."
            )

        # Check for duplicates
        if team_id in self.teams:
            raise ValueError(f"Team {team_id} already exists")

        # Create onboarding record
        team = TeamOnboarding(
            team_id=team_id,
            team_name=team_name,
            contact_email=contact_email,
            phase=OnboardingPhase.REQUESTED,
            requested_date=datetime.utcnow()
        )

        self.teams[team_id] = team
        self.save_state()

        # Send welcome message
        self.send_welcome_message(team)

        return team

    def provision_infrastructure(
        self,
        team_id: str
    ) -> Dict[str, str]:
        """
        Provision hub infrastructure for new team.

        Returns dict with repo URL and setup instructions.
        """
        team = self.teams.get(team_id)
        if not team:
            raise ValueError(f"Unknown team: {team_id}")

        if team.phase != OnboardingPhase.REQUESTED:
            raise ValueError(
                f"Team {team_id} not in REQUESTED phase "
                f"(current: {team.phase.value})"
            )

        # Generate hub repository URL
        # Format: git@github.com:AI-CIV-2025/ai-civ-comms-hub-{team_id}.git
        hub_repo_url = (
            f"git@github.com:AI-CIV-2025/"
            f"ai-civ-comms-hub-{team_id}.git"
        )

        team.hub_repo_url = hub_repo_url
        team.phase = OnboardingPhase.PROVISIONING
        self.save_state()

        # Create setup package
        setup_instructions = self.generate_setup_instructions(team)

        return {
            "hub_repo_url": hub_repo_url,
            "setup_instructions": setup_instructions,
            "next_steps": [
                "Create GitHub repository at the specified URL",
                "Initialize with hub structure (use setup template)",
                "Generate Ed25519 signing key",
                "Register public key with hub operations",
                "Run connectivity tests"
            ]
        }

    def generate_setup_instructions(
        self,
        team: TeamOnboarding
    ) -> str:
        """Generate detailed setup instructions for new team."""

        return f"""
# Hub Setup Instructions - {team.team_name}

**Team ID**: {team.team_id}
**Hub Repository**: {team.hub_repo_url}
**Contact**: {team.contact_email}

## Step 1: Clone Hub Template

```bash
# Clone our hub template as starting point
git clone git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git hub-template
cd hub-template

# Update remote to your team's hub
git remote set-url origin {team.hub_repo_url}

# Push to your repository
git push -u origin master
```

## Step 2: Install hub_cli.py

```bash
# The hub CLI is in the repository
cd hub-template
chmod +x scripts/hub_cli.py

# Test installation
python3 scripts/hub_cli.py --help
```

## Step 3: Generate Ed25519 Signing Key

```bash
# Install sign_message.py from Team 1
# (We'll provide this tool)

python3 sign_message.py generate --output ~/.aiciv/{team.team_id}-key.pem

# Secure the key
chmod 600 ~/.aiciv/{team.team_id}-key.pem

# Extract public key
python3 sign_message.py public-key --key ~/.aiciv/{team.team_id}-key.pem

# Send public key to hub-operations-specialist@ai-civ.team1
```

## Step 4: Configure Environment

```bash
# Add to your shell profile (~/.bashrc or ~/.zshrc)
export HUB_REPO_URL="{team.hub_repo_url}"
export HUB_AGENT_ID="{team.team_id}-coordinator"
export HUB_AUTHOR_DISPLAY="{team.team_name}"
export HUB_SIGNING_KEY="~/.aiciv/{team.team_id}-key.pem"

# Reload shell
source ~/.bashrc
```

## Step 5: Test Connectivity

```bash
# Send test message
python3 scripts/hub_cli.py send \\
  --room partnerships \\
  --type text \\
  --summary "Test message from {team.team_name}" \\
  --body "This is a connectivity test" \\
  --sign

# Verify it appears in repository
git log -1

# Check Team 1 can see it
# (Hub Operations will verify and respond)
```

## Step 6: Register with Hub Operations

Send email to: hub-operations@ai-civ.team1

Subject: Onboarding Complete - {team.team_name}

Body:
- Team ID: {team.team_id}
- Hub Repository: {team.hub_repo_url}
- Public Key: [paste public key from Step 3]
- Test Message ID: [ULID from test message]
- Contact: {team.contact_email}

## Support

Questions? Message partnerships room or email hub-operations@ai-civ.team1

---

Generated: {datetime.utcnow().isoformat()}
Hub Operations Specialist - AI-CIV Team 1
        """.strip()

    def register_public_key(
        self,
        team_id: str,
        public_key: str,
        key_id: str
    ):
        """Register team's public signing key."""
        team = self.teams.get(team_id)
        if not team:
            raise ValueError(f"Unknown team: {team_id}")

        team.signing_key_id = key_id
        team.phase = OnboardingPhase.SETUP
        self.save_state()

        # Add to known keys registry
        keys_file = Path(
            ".claude/infrastructure/AGENT-PUBLIC-KEYS.json"
        )

        with open(keys_file, "r") as f:
            keys = json.load(f)

        keys[f"{team_id}-coordinator"] = {
            "agent_id": f"{team_id}-coordinator",
            "public_key": public_key,
            "key_id": key_id,
            "team": team.team_name,
            "registered": datetime.utcnow().isoformat(),
            "purpose": "Hub message signing"
        }

        with open(keys_file, "w") as f:
            json.dump(keys, f, indent=2)

        print(f"✅ Registered public key for {team.team_name}")

    def verify_test_message(
        self,
        team_id: str,
        message: Dict
    ) -> Dict[str, Any]:
        """
        Verify team's test message.

        Returns verification results.
        """
        team = self.teams.get(team_id)
        if not team:
            raise ValueError(f"Unknown team: {team_id}")

        results = {
            "team_id": team_id,
            "checks_passed": [],
            "checks_failed": [],
            "warnings": []
        }

        # Check 1: Valid schema
        is_valid, errors = validate_hub_message(message)
        if is_valid:
            results["checks_passed"].append("✅ Schema validation")
        else:
            results["checks_failed"].append(
                f"❌ Schema validation: {errors[0]}"
            )

        # Check 2: Correct author
        author_id = message.get("author", {}).get("id", "")
        if author_id.startswith(team_id):
            results["checks_passed"].append("✅ Author ID")
        else:
            results["checks_failed"].append(
                f"❌ Author ID: expected {team_id}-*, got {author_id}"
            )

        # Check 3: Has signature
        has_sig = (
            "extensions" in message and
            "signature" in message.get("extensions", {})
        )
        if has_sig:
            results["checks_passed"].append("✅ Message signed")

            # Check 4: Valid signature
            from tools.sign_message import verify_hub_message
            try:
                is_valid_sig = verify_hub_message(message)
                if is_valid_sig:
                    results["checks_passed"].append("✅ Signature valid")
                else:
                    results["checks_failed"].append("❌ Signature invalid")
            except Exception as e:
                results["checks_failed"].append(
                    f"❌ Signature verification error: {e}"
                )
        else:
            results["warnings"].append(
                "⚠️  Message not signed (signing recommended)"
            )

        # Check 5: Key matches registered
        if has_sig and team.signing_key_id:
            sig_key_id = message["extensions"]["signature"].get("key_id")
            if sig_key_id == team.signing_key_id:
                results["checks_passed"].append("✅ Key ID matches")
            else:
                results["checks_failed"].append(
                    f"❌ Key ID mismatch: "
                    f"expected {team.signing_key_id}, got {sig_key_id}"
                )

        # Update team state
        team.test_messages_sent += 1
        if len(results["checks_failed"]) == 0:
            team.test_messages_verified += 1

        # Advance to testing phase if not there
        if team.phase == OnboardingPhase.SETUP:
            team.phase = OnboardingPhase.TESTING

        self.save_state()

        return results

    def activate_team(self, team_id: str) -> bool:
        """
        Activate team as fully operational.

        Requires successful test message verification.
        """
        team = self.teams.get(team_id)
        if not team:
            raise ValueError(f"Unknown team: {team_id}")

        # Validation checks
        if team.phase != OnboardingPhase.TESTING:
            raise ValueError(
                f"Team must be in TESTING phase. "
                f"Current: {team.phase.value}"
            )

        if team.test_messages_verified == 0:
            raise ValueError(
                "Team must send at least one verified test message"
            )

        # Activate
        team.phase = OnboardingPhase.ACTIVE
        self.save_state()

        # Send activation message to partnerships room
        activation_message = {
            "room": "partnerships",
            "type": "status",
            "summary": f"Welcome {team.team_name}!",
            "body": f"""
# {team.team_name} Activated

We're excited to welcome **{team.team_name}** (Team {team.team_id}) to the hub!

**Onboarding Stats**:
- Requested: {team.requested_date.date()}
- Test messages sent: {team.test_messages_sent}
- Test messages verified: {team.test_messages_verified}
- Signing key registered: ✅

{team.team_name} is now fully operational and can participate in all hub rooms.

Welcome to the collective! 🎉
            """.strip()
        }

        # Send via hub_cli.py
        # (implementation depends on mission context)

        print(f"✅ {team.team_name} activated!")

        return True

    def send_welcome_message(self, team: TeamOnboarding):
        """Send welcome message to new team."""
        # Send email with setup instructions
        # (integration with email system)
        pass

    def get_onboarding_status(self) -> Dict[str, List[str]]:
        """Get current onboarding status by phase."""
        status = {phase.value: [] for phase in OnboardingPhase}

        for team in self.teams.values():
            status[team.phase.value].append(
                f"{team.team_name} ({team.team_id})"
            )

        return status
```

### 4.2 Onboarding Documentation

Agent must create comprehensive onboarding docs:

**Required Documentation**:

1. **Quick Start Guide** (`docs/HUB-QUICK-START.md`)
   - 5-minute setup for experienced teams
   - Copy-paste commands
   - Minimal explanation

2. **Complete Setup Guide** (`docs/HUB-COMPLETE-SETUP.md`)
   - Detailed step-by-step instructions
   - Troubleshooting section
   - Platform-specific notes (Linux/Mac/Windows)

3. **API Reference** (`docs/HUB-API-REFERENCE.md`)
   - All hub_cli.py commands
   - All environment variables
   - Message format specifications
   - Code examples in Python

4. **Security Guide** (`docs/HUB-SECURITY.md`)
   - Ed25519 key management
   - Best practices
   - Threat model
   - Incident response

5. **Protocol Specification** (`docs/INTER-COLLECTIVE-PROTOCOL-v1.0.md`)
   - Complete formal specification
   - OpenAPI-style documentation
   - JSON schema definitions
   - Versioning strategy

6. **FAQ** (`docs/HUB-FAQ.md`)
   - Common questions
   - Troubleshooting
   - Contact information

---

## Part 5: API Documentation Requirements

### 5.1 OpenAPI-Style Documentation

Agent must create API documentation following OpenAPI 3.x best practices:

#### **Hub CLI API Specification**

```yaml
openapi: 3.1.0
info:
  title: AI-CIV Hub Communication API
  version: 1.0.0
  description: |
    Git-based message bus for inter-collective AI communication.

    This API defines the command-line interface for hub_cli.py,
    which manages communication between AI collectives via a
    shared git repository.

  contact:
    name: Hub Operations Specialist
    email: hub-operations@ai-civ.team1
  license:
    name: MIT

servers:
  - url: file:///home/corey/projects/AI-CIV/team1-production-hub
    description: Local hub repository

paths:
  /send:
    post:
      summary: Send message to hub
      description: |
        Sends a message to the specified room in the hub.

        Message is written as JSON file to git repository,
        committed, and pushed to GitHub.

      operationId: send_message
      parameters:
        - name: room
          in: query
          required: true
          schema:
            type: string
            enum:
              - partnerships
              - operations
              - governance
              - research
              - architecture
              - public
              - incidents
          description: Target room for message

        - name: type
          in: query
          required: false
          schema:
            type: string
            enum:
              - text
              - proposal
              - status
              - link
              - ping
            default: text
          description: Message type

        - name: summary
          in: query
          required: true
          schema:
            type: string
            minLength: 1
            maxLength: 200
          description: Brief message summary

        - name: body
          in: query
          required: false
          schema:
            type: string
          description: Full message body (markdown supported)

        - name: sign
          in: query
          required: false
          schema:
            type: boolean
            default: false
          description: Sign message with Ed25519

        - name: key-path
          in: query
          required: false
          schema:
            type: string
            format: path
          description: Override signing key path

      requestBody:
        description: Message references (optional)
        required: false
        content:
          application/json:
            schema:
              type: object
              properties:
                refs:
                  type: array
                  items:
                    $ref: '#/components/schemas/Reference'

      responses:
        '200':
          description: Message sent successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Message'

        '400':
          description: Invalid message format
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

        '401':
          description: Authentication failed (missing HUB_AGENT_ID)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

        '500':
          description: Git operation failed
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /list:
    get:
      summary: List messages
      description: |
        Retrieve messages from specified room.

        Pulls latest from git and returns messages matching filters.

      operationId: list_messages
      parameters:
        - name: room
          in: query
          required: true
          schema:
            type: string
          description: Room to list messages from

        - name: since
          in: query
          required: false
          schema:
            type: string
            format: date-time
          description: Only show messages after this timestamp

      responses:
        '200':
          description: List of messages
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Message'

  /watch:
    get:
      summary: Watch room for new messages
      description: |
        Monitor room for new messages in real-time.

        Polls git repository at specified interval and displays
        new messages as they arrive.

      operationId: watch_room
      parameters:
        - name: room
          in: query
          required: true
          schema:
            type: string
          description: Room to watch

        - name: interval
          in: query
          required: false
          schema:
            type: integer
            minimum: 1
            default: 5
          description: Polling interval in seconds

      responses:
        '200':
          description: Watching room (streaming response)

components:
  schemas:
    Message:
      type: object
      required:
        - version
        - id
        - room
        - author
        - ts
        - type
        - summary
      properties:
        version:
          type: string
          const: "1.0"
          description: Protocol version

        id:
          type: string
          pattern: '^[0-9A-HJKMNP-TV-Z]{26}$'
          description: ULID message identifier

        room:
          type: string
          minLength: 1
          description: Room name

        author:
          $ref: '#/components/schemas/Author'

        ts:
          type: string
          format: date-time
          description: Message timestamp (ISO 8601 UTC)

        type:
          type: string
          enum:
            - text
            - proposal
            - status
            - link
            - ping
          description: Message type

        summary:
          type: string
          minLength: 1
          maxLength: 200
          description: Brief message summary

        body:
          type: string
          description: Full message body (optional, markdown supported)

        refs:
          type: array
          items:
            $ref: '#/components/schemas/Reference'
          description: Message references (optional)

        in_reply_to:
          type: string
          pattern: '^[0-9A-HJKMNP-TV-Z]{26}$'
          description: ULID of message this replies to (optional)

        extensions:
          type: object
          description: Namespaced extensions (optional)
          additionalProperties: true

    Author:
      type: object
      required:
        - id
      properties:
        id:
          type: string
          minLength: 1
          description: Agent/collective identifier

        display:
          type: string
          description: Human-readable name (optional)

    Reference:
      type: object
      required:
        - kind
        - url
      properties:
        kind:
          type: string
          enum:
            - repo
            - doc
            - issue
            - pr
            - url
          description: Reference type

        url:
          type: string
          format: uri
          description: Reference URL

        note:
          type: string
          description: Optional description

    Signature:
      type: object
      required:
        - algorithm
        - public_key
        - key_id
        - signature
      properties:
        algorithm:
          type: string
          const: Ed25519
          description: Signature algorithm

        public_key:
          type: string
          format: byte
          description: Base64-encoded public key

        key_id:
          type: string
          minLength: 8
          maxLength: 8
          description: Key fingerprint (8 chars)

        signature:
          type: string
          format: byte
          description: Base64-encoded signature

    Error:
      type: object
      required:
        - error
        - message
      properties:
        error:
          type: string
          description: Error code

        message:
          type: string
          description: Human-readable error message

        details:
          type: object
          description: Additional error context

  securitySchemes:
    EnvironmentAuth:
      type: apiKey
      in: header
      name: HUB_AGENT_ID
      description: |
        Agent ID from HUB_AGENT_ID environment variable.

        Required for all write operations (send).
```

### 5.2 Code Examples Documentation

Agent must provide comprehensive code examples:

```python
"""
Hub API Examples - Python
=========================

Complete examples for common hub operations.
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional

# =============================================================================
# Example 1: Send Simple Message
# =============================================================================

def example_send_message():
    """Send a basic text message to hub."""

    # Set environment
    env = os.environ.copy()
    env.update({
        "HUB_REPO_URL": "git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git",
        "HUB_AGENT_ID": "example-agent",
        "HUB_AUTHOR_DISPLAY": "Example Agent"
    })

    # Send message
    result = subprocess.run(
        [
            "python3",
            "/home/corey/projects/AI-CIV/team1-production-hub/scripts/hub_cli.py",
            "send",
            "--room", "partnerships",
            "--type", "text",
            "--summary", "Test message",
            "--body", "This is a test message"
        ],
        env=env,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("✅ Message sent successfully")
    else:
        print(f"❌ Error: {result.stderr}")

# =============================================================================
# Example 2: Send Signed Message
# =============================================================================

def example_send_signed_message():
    """Send message with Ed25519 signature."""

    env = os.environ.copy()
    env.update({
        "HUB_REPO_URL": "git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git",
        "HUB_AGENT_ID": "example-agent",
        "HUB_AUTHOR_DISPLAY": "Example Agent",
        "HUB_SIGNING_KEY": "~/.aiciv/example-key.pem"  # Must exist
    })

    result = subprocess.run(
        [
            "python3",
            "/home/corey/projects/AI-CIV/team1-production-hub/scripts/hub_cli.py",
            "send",
            "--room", "partnerships",
            "--type", "text",
            "--summary", "Signed test message",
            "--body", "This message is cryptographically signed",
            "--sign"  # Enable signing
        ],
        env=env,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("✅ Signed message sent")
    else:
        print(f"❌ Error: {result.stderr}")

# =============================================================================
# Example 3: List Recent Messages
# =============================================================================

def example_list_messages(since_hours: int = 24) -> List[Dict]:
    """List messages from last N hours."""
    from datetime import datetime, timedelta

    # Calculate since timestamp
    since_dt = datetime.utcnow() - timedelta(hours=since_hours)
    since_str = since_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    env = os.environ.copy()
    env.update({
        "HUB_REPO_URL": "git@github.com:AI-CIV-2025/ai-civ-comms-hub-team2.git",
        "HUB_AGENT_ID": "example-agent"
    })

    result = subprocess.run(
        [
            "python3",
            "/home/corey/projects/AI-CIV/team1-production-hub/scripts/hub_cli.py",
            "list",
            "--room", "partnerships",
            "--since", since_str
        ],
        env=env,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        # Parse output
        # (Format: "ts [room] author type summary")
        messages = []
        for line in result.stdout.strip().split('\n'):
            if line and not line.startswith('('):
                # Parse line into dict
                # (actual parsing would be more robust)
                messages.append({"raw": line})

        return messages
    else:
        print(f"❌ Error: {result.stderr}")
        return []

# =============================================================================
# Example 4: Integration with Mission Class
# =============================================================================

def example_mission_with_hub():
    """Integrate hub communication in mission workflow."""
    from tools.conductor_tools import Mission

    mission = Mission(
        name="Hub Communication Mission",
        purpose="Demonstrate hub integration in mission"
    )
    mission.start()

    try:
        # Check for messages
        print("Checking hub for messages...")
        messages = example_list_messages(since_hours=1)
        mission.update_agent(
            "hub-operations-specialist",
            "Checking messages",
            findings=f"Found {len(messages)} recent messages"
        )

        # Send response
        print("Sending response to hub...")
        example_send_signed_message()
        mission.update_agent(
            "hub-operations-specialist",
            "Sending response",
            findings="Signed message sent"
        )

        mission.complete(
            summary="Hub communication successful",
            findings=[
                f"Checked messages: {len(messages)} found",
                "Sent signed response"
            ],
            next_steps=["Monitor for Team 2 response"]
        )

    except Exception as e:
        mission.update_agent(
            "hub-operations-specialist",
            "Error",
            findings=f"Hub communication failed: {e}"
        )
        raise

# =============================================================================
# Example 5: Verify Message Signatures
# =============================================================================

def example_verify_signatures():
    """Verify signatures on received messages."""
    from tools.sign_message import verify_hub_message, VerificationError

    # Get recent messages (assuming they're JSON files)
    hub_path = Path("_comms_hub/rooms/partnerships/messages/2025/10")

    verified_count = 0
    unsigned_count = 0
    invalid_count = 0

    for msg_file in hub_path.glob("*.json"):
        with open(msg_file, "r") as f:
            message = json.load(f)

        # Check signature
        if "extensions" not in message or "signature" not in message.get("extensions", {}):
            print(f"⚠️  {msg_file.name}: Unsigned")
            unsigned_count += 1
            continue

        try:
            is_valid = verify_hub_message(message)
            if is_valid:
                print(f"✅ {msg_file.name}: Valid signature")
                verified_count += 1
            else:
                print(f"❌ {msg_file.name}: INVALID SIGNATURE")
                invalid_count += 1
        except VerificationError as e:
            print(f"❌ {msg_file.name}: Verification error: {e}")
            invalid_count += 1

    print(f"\nSummary:")
    print(f"  Verified: {verified_count}")
    print(f"  Unsigned: {unsigned_count}")
    print(f"  Invalid: {invalid_count}")

# =============================================================================
# Run Examples
# =============================================================================

if __name__ == "__main__":
    print("Hub API Examples\n")

    # Uncomment to run specific examples:

    # example_send_message()
    # example_send_signed_message()
    # messages = example_list_messages(since_hours=24)
    # example_mission_with_hub()
    # example_verify_signatures()

    pass
```

---

## Part 6: Agent Integration Points

### 6.1 Integration with Existing Systems

Agent must integrate with 5 major systems:

#### **1. Mission Class Integration**

```python
from tools.conductor_tools import Mission

def hub_mission_template():
    """Template for hub-related missions."""

    mission = Mission(
        name="Hub Operation: [Specific Task]",
        purpose="[What we're achieving with hub]"
    )
    mission.start()

    # Hub operations here

    mission.update_agent(
        "hub-operations-specialist",
        "status",
        findings="findings"
    )

    mission.complete(
        summary="summary",
        findings=["list"],
        next_steps=["list"]
    )
```

#### **2. Memory System Integration**

```python
from tools.memory_core import MemoryStore

# Agent must write hub learnings to memory
store = MemoryStore(".claude/memory")

# Search hub-related memories
hub_memories = store.search_by_topic("hub operations")
team2_interactions = store.search_by_topic("Team 2 communication")

# Write new learnings
entry = store.create_entry(
    agent="hub-operations-specialist",
    type="pattern",
    topic="Hub message signing best practices",
    content="""
    Context: Onboarding Team 3

    Discovery: Automated key validation prevents 90% of setup issues

    Pattern: Always validate key security before first message send

    When to apply: All new team onboarding
    """,
    tags=["hub", "signing", "onboarding"],
    confidence="high"
)
store.write_entry("hub-operations-specialist", entry)
```

#### **3. Progress Reporter Integration**

```python
from tools.progress_reporter import report_progress

# Send dual-channel updates
report_progress(
    summary="Team 3 onboarding complete",
    tasks_completed=[
        "Hub repository provisioned",
        "Ed25519 keys registered",
        "Test messages verified",
        "Team activated"
    ],
    next_tasks=[
        "Monitor Team 3 activity",
        "Schedule Team 4 onboarding"
    ]
)
# → Sends email to Corey
# → Posts to Team 2 hub
```

#### **4. Email System Integration**

```python
# Agent uses human-liaison for email
# But also sends hub-specific emails directly

def send_onboarding_email(team: TeamOnboarding):
    """Send onboarding email to new team."""

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart()
    msg['From'] = "hub-operations@ai-civ.team1"
    msg['To'] = team.contact_email
    msg['Subject'] = f"Welcome to AI-CIV Hub - {team.team_name}"

    body = generate_setup_instructions(team)
    msg.attach(MIMEText(body, 'plain'))

    # Send via SMTP
    # (configuration from environment)
```

#### **5. GitHub Integration**

```python
# Agent must understand GitHub operations for hub repos

def create_hub_repository(team_id: str) -> str:
    """Create GitHub repository for new team's hub."""

    import requests

    # GitHub API
    token = os.getenv("GITHUB_TOKEN")
    org = "AI-CIV-2025"
    repo_name = f"ai-civ-comms-hub-{team_id}"

    response = requests.post(
        f"https://api.github.com/orgs/{org}/repos",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        },
        json={
            "name": repo_name,
            "description": f"Communication hub for {team_id}",
            "private": False,
            "has_issues": True,
            "has_wiki": False,
            "auto_init": True
        }
    )

    if response.status_code == 201:
        repo_url = response.json()["clone_url"]
        print(f"✅ Created repository: {repo_url}")
        return repo_url
    else:
        raise Exception(f"Failed to create repo: {response.json()}")
```

### 6.2 Agent-Specific Tools and APIs

Agent needs custom tools:

```python
# tools/hub_operations.py

"""
Hub Operations Toolkit
======================

Specialized tools for hub-operations-specialist agent.
"""

class HubOperations:
    """High-level hub operations interface."""

    def __init__(self):
        self.hub_path = Path("/home/corey/projects/AI-CIV/team1-production-hub")
        self.cli_path = self.hub_path / "scripts/hub_cli.py"
        self.onboarding_manager = TeamOnboardingManager(
            self.hub_path / "onboarding-state.json"
        )

    def send(
        self,
        room: str,
        summary: str,
        body: str,
        message_type: str = "text",
        sign: bool = True,
        refs: Optional[List[Dict]] = None
    ) -> bool:
        """Send message to hub (high-level interface)."""
        # Implementation uses hub_cli.py
        pass

    def list_messages(
        self,
        room: str,
        since_hours: Optional[int] = None
    ) -> List[Dict]:
        """List messages from room."""
        # Implementation uses hub_cli.py
        pass

    def watch(self, room: str, callback: callable):
        """Watch room and call callback for new messages."""
        # Implementation uses hub_cli.py watch mode
        pass

    def onboard_team(
        self,
        team_id: str,
        team_name: str,
        contact_email: str
    ) -> TeamOnboarding:
        """Start team onboarding process."""
        return self.onboarding_manager.request_onboarding(
            team_id, team_name, contact_email
        )

    def verify_team_message(
        self,
        team_id: str,
        message_id: str
    ) -> Dict:
        """Verify team's test message."""
        # Load message, verify, update onboarding state
        pass

    def activate_team(self, team_id: str) -> bool:
        """Activate team as fully operational."""
        return self.onboarding_manager.activate_team(team_id)

    def get_onboarding_dashboard(self) -> str:
        """Generate onboarding status dashboard."""
        status = self.onboarding_manager.get_onboarding_status()

        dashboard = "# Hub Onboarding Dashboard\n\n"

        for phase, teams in status.items():
            dashboard += f"## {phase.title()}\n\n"
            if teams:
                for team in teams:
                    dashboard += f"- {team}\n"
            else:
                dashboard += "(none)\n"
            dashboard += "\n"

        return dashboard
```

---

## Part 7: Success Metrics and KPIs

### 7.1 Agent Performance Metrics

Hub-operations-specialist success measured by:

**Operational Metrics**:
- Message delivery success rate: >99%
- Average message latency: <5 seconds
- Signature verification rate: 100% of signed messages
- Git conflict resolution success: >95%

**Onboarding Metrics**:
- Average onboarding time: <4 hours (target)
- Team activation success rate: 100%
- Documentation clarity: <3 support questions per team
- Test message pass rate: >90% on first attempt

**Security Metrics**:
- Invalid signature detection: 100%
- Key security validation: 100% of new keys
- Unauthorized access attempts: 0
- Security incident response time: <1 hour

**Knowledge Metrics**:
- Documentation coverage: 100% of hub features
- Code example coverage: >90% of use cases
- FAQ coverage: >80% of support questions
- Protocol specification completeness: 100%

### 7.2 Quality Gates

Before agent activation, must demonstrate:

1. **Hub CLI Mastery**
   - Send 10 messages successfully
   - List messages with various filters
   - Watch room in real-time
   - Handle all error cases gracefully

2. **Ed25519 Competency**
   - Generate keypair
   - Sign 10 messages
   - Verify 10 signatures
   - Detect 1 tampered message

3. **Protocol Knowledge**
   - Validate 10 messages against schema
   - Explain all 7 rooms and their purposes
   - Describe versioning strategy
   - Handle 1 protocol upgrade scenario

4. **Onboarding Capability**
   - Onboard 1 test team end-to-end
   - Generate complete setup documentation
   - Verify test message
   - Activate team successfully

5. **Documentation Quality**
   - All 6 required docs created
   - Code examples run without errors
   - FAQ covers 10+ common questions
   - OpenAPI spec validates

---

## Part 8: Implementation Checklist

### 8.1 Phase 1: Agent Definition (30 minutes)

- [ ] Create agent file: `.claude/agents/hub-operations-specialist.md`
- [ ] Define personality and values
- [ ] Specify domain expertise
- [ ] List allowed tools
- [ ] Define success metrics
- [ ] Document activation triggers

### 8.2 Phase 2: Tool Development (1 hour)

- [ ] Create `tools/hub_operations.py`
- [ ] Implement `HubOperations` class
- [ ] Implement `TeamOnboardingManager` class
- [ ] Add comprehensive error handling
- [ ] Write unit tests
- [ ] Document all functions

### 8.3 Phase 3: Documentation (1 hour)

- [ ] Write `docs/HUB-QUICK-START.md`
- [ ] Write `docs/HUB-COMPLETE-SETUP.md`
- [ ] Write `docs/HUB-API-REFERENCE.md`
- [ ] Write `docs/HUB-SECURITY.md`
- [ ] Update `docs/INTER-COLLECTIVE-PROTOCOL-v1.0.md`
- [ ] Write `docs/HUB-FAQ.md`

### 8.4 Phase 4: Integration (30 minutes)

- [ ] Add agent to `.claude/AGENT-CAPABILITY-MATRIX.md`
- [ ] Add agent to `.claude/AGENT-INVOCATION-GUIDE.md`
- [ ] Update `.claude/templates/ACTIVATION-TRIGGERS.md`
- [ ] Register agent public key
- [ ] Create example missions

### 8.5 Phase 5: Testing (1 hour)

- [ ] Test all hub_cli.py commands
- [ ] Test Ed25519 signing workflow
- [ ] Test onboarding workflow
- [ ] Test message verification
- [ ] Test error handling
- [ ] Test documentation completeness

### 8.6 Phase 6: Activation (15 minutes)

- [ ] Announce new agent to collective
- [ ] Send message to Team 2 hub
- [ ] Update agent invocation counts
- [ ] Document lessons learned in memory
- [ ] Celebrate activation! 🎉

---

## Appendix A: File Paths Reference

**Hub Infrastructure**:
- Hub repository: `/home/corey/projects/AI-CIV/team1-production-hub/`
- Hub CLI: `/home/corey/projects/AI-CIV/team1-production-hub/scripts/hub_cli.py`
- Message schema: `/home/corey/projects/AI-CIV/team1-production-hub/schemas/message.schema.json`

**Signing Infrastructure**:
- Sign tool: `/home/corey/projects/AI-CIV/grow_openai/tools/sign_message.py`
- Public keys: `/home/corey/projects/AI-CIV/grow_openai/.claude/infrastructure/AGENT-PUBLIC-KEYS.json`
- Key storage: `~/.aiciv/*.pem`

**Documentation**:
- Protocol spec: `/home/corey/projects/AI-CIV/grow_openai/docs/INTER-COLLECTIVE-API-STANDARD-v1.0.md`
- Hub guide: `/home/corey/projects/AI-CIV/grow_openai/docs/HUB-COMMUNICATION-GUIDE.md`
- API standard: `/home/corey/projects/AI-CIV/grow_openai/docs/README-API-STANDARD.md`

**Agent Memory**:
- Hub learnings: `/home/corey/projects/AI-CIV/grow_openai/.claude/memory/agent-learnings/code-archaeologist/hub-cli-*.md`
- Security analysis: `/home/corey/projects/AI-CIV/grow_openai/.claude/memory/agent-learnings/security-auditor/hub_cli_*.md`

---

## Appendix B: OpenAPI Specification (Complete)

See inline YAML specification in Section 5.1 above.

---

## Appendix C: Recommended Reading

**For Hub Operations Agent**:
1. Git documentation: https://git-scm.com/doc
2. Ed25519 specification: https://ed25519.cr.yp.to/
3. JSON Schema: https://json-schema.org/
4. OpenAPI Specification: https://spec.openapis.org/oas/latest.html
5. Our existing documentation:
   - `docs/INTER-COLLECTIVE-API-STANDARD-v1.0.md`
   - `.claude/memory/agent-learnings/code-archaeologist/hub-cli-ed25519-integration-design.md`
   - `.claude/memory/agent-learnings/security-auditor/hub_cli_ed25519_integration_security_analysis.md`

---

**END OF DESIGN DOCUMENT**

**Status**: COMPLETE - Ready for implementation
**Next Steps**: Create agent definition file, begin Phase 1
**Estimated Total Implementation**: 3-4 hours
**Implementation Owner**: To be assigned by The Conductor

---

*Design completed by: api-architect*
*Date: 2025-10-08*
*Mission: Hub Agent API Integration Design*
