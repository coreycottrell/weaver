# Ed25519 + hub_cli.py Integration Testing Strategy

**Agent**: test-architect
**Date**: 2025-10-04
**Type**: Testing Strategy
**Confidence**: HIGH
**Tags**: ed25519, testing, integration, hub_cli, cryptography, security

---

## Executive Summary

Comprehensive testing strategy for integrating Ed25519 signing into hub_cli.py. This integration is CRITICAL for the Oct 10-11 Integration Sprint with A-C-Gee. Testing must ensure bulletproof security, backward compatibility, and cross-collective verification.

**Key Insight**: The existing `test_signing.py` provides excellent unit test coverage (10/10 passing). Our strategy adds integration, compatibility, security, and cross-collective testing layers.

---

## 1. Testing Architecture

### 1.1 Test Pyramid

```
                    ┌─────────────────┐
                    │  E2E Tests (5)  │  Cross-collective verification
                    │  Oct 10-11      │  with A-C-Gee
                    └─────────────────┘
                 ┌────────────────────────┐
                 │  Integration Tests (8) │  hub_cli.py + Ed25519
                 │  Oct 4-9               │  End-to-end workflows
                 └────────────────────────┘
              ┌───────────────────────────────┐
              │  Compatibility Tests (6)      │  Unsigned messages
              │  Oct 4-9                      │  ADR-004 format
              └───────────────────────────────┘
           ┌──────────────────────────────────────┐
           │  Security Tests (7)                  │  Tampering, key mgmt
           │  Oct 4-9                             │  Error scenarios
           └──────────────────────────────────────┘
        ┌─────────────────────────────────────────────┐
        │  Unit Tests (10) - ALREADY PASSING ✓        │  sign_message.py
        │  tools/test_signing.py                      │  Core functions
        └─────────────────────────────────────────────┘

Total: 36 test scenarios
```

### 1.2 Test Coverage Targets

| Layer | Coverage | Status |
|-------|----------|--------|
| Unit Tests (Ed25519) | 100% | ✅ DONE (10/10 passing) |
| Integration Tests | 90%+ | ⏳ TODO (8 scenarios) |
| Compatibility Tests | 100% | ⏳ TODO (6 scenarios) |
| Security Tests | 100% | ⏳ TODO (7 scenarios) |
| E2E Tests | 100% | ⏳ TODO (5 scenarios, Oct 10-11) |

**Overall Target**: 95%+ coverage across all layers

---

## 2. Unit Tests (EXISTING - Already Passing ✓)

**File**: `/home/corey/projects/AI-CIV/grow_openai/tools/test_signing.py`
**Status**: ✅ 10/10 PASSING
**Coverage**: Ed25519 core functions

### 2.1 Existing Test Cases

1. ✅ **Key Generation** - `test_key_generation()`
   - Validates keypair generation
   - Checks key length and format

2. ✅ **Signer Creation** - `test_signer_creation()`
   - Tests Ed25519Signer instantiation
   - Validates public key export and key ID

3. ✅ **Message Signing** - `test_message_signing()`
   - Signs sample hub message
   - Checks signature structure

4. ✅ **Signature Verification** - `test_signature_verification()`
   - Verifies valid signatures
   - Tests verification logic

5. ✅ **Tamper Detection** - `test_tamper_detection()`
   - Modifies signed message
   - Ensures verification fails

6. ✅ **Invalid Signature Rejection** - `test_invalid_signature()`
   - Tests with corrupted signatures
   - Validates error handling

7. ✅ **Key Loading** - `test_key_loading()`
   - Load keys from files
   - Tests PEM format parsing

8. ✅ **Public Key Export** - `test_public_key_export()`
   - Export public keys
   - Validate base64 encoding

9. ✅ **Key ID Generation** - `test_key_id()`
   - Consistent key IDs
   - First 8 chars of public key hash

10. ✅ **Canonical Signing** - `test_canonical_json()`
    - Tests deterministic JSON serialization
    - Ensures signature consistency

### 2.2 Unit Test Maintenance

**Action**: Keep existing tests running as regression suite
**Frequency**: Run on every commit
**Command**: `python3 tools/test_signing.py`
**Expected**: All 10 tests PASS

---

## 3. Integration Tests (NEW - hub_cli.py + Ed25519)

**Goal**: Test hub_cli.py with Ed25519 signing enabled
**File**: `tools/test_hub_cli_integration.py` (to create)
**Coverage**: End-to-end message workflows

### 3.1 Test Scenarios

#### INT-1: Send Signed Message
**Description**: Send message with --sign flag
**Setup**:
- Generate test keypair
- Set HUB_REPO_URL to test repo
- Set AICIV_SIGNING_KEY to test key

**Test Steps**:
```bash
# 1. Generate test key
python3 tools/sign_message.py generate --output /tmp/test-key.pem

# 2. Send signed message
export HUB_REPO_URL="git@github.com:test/test-hub.git"
export AICIV_SIGNING_KEY="/tmp/test-key.pem"
export HUB_AGENT_ID="test-agent"
export HUB_AGENT_DISPLAY="Test Agent"

cd /home/corey/projects/AI-CIV/team1-production-hub
python3 scripts/hub_cli.py send \
  --room test \
  --type text \
  --summary "Test signed message" \
  --body "Testing Ed25519 integration" \
  --sign
```

**Expected**:
- Message file created with signature in extensions
- Git commit created
- Console output: "✓ Message signed (key: <key_id>)"

**Validation**:
```python
import json
with open("_comms_hub/rooms/test/messages/2025/10/message.json") as f:
    msg = json.load(f)

assert "extensions" in msg
assert "signature" in msg["extensions"]
assert msg["extensions"]["signature"]["algorithm"] == "Ed25519"
assert "public_key" in msg["extensions"]["signature"]
assert "signature" in msg["extensions"]["signature"]
```

---

#### INT-2: Send Unsigned Message (No --sign Flag)
**Description**: Ensure unsigned messages still work
**Test Steps**:
```bash
python3 scripts/hub_cli.py send \
  --room test \
  --type text \
  --summary "Unsigned message" \
  --body "No signature"
# Note: No --sign flag
```

**Expected**:
- Message file created WITHOUT signature
- Git commit successful
- No errors

**Validation**:
```python
with open("_comms_hub/rooms/test/messages/2025/10/message.json") as f:
    msg = json.load(f)

# Should NOT have signature
assert "extensions" not in msg or "signature" not in msg.get("extensions", {})
```

---

#### INT-3: Verify Signed Message on List
**Description**: hub_cli.py list shows signature status
**Test Steps**:
```bash
# After INT-1 sends signed message
python3 scripts/hub_cli.py list --room test
```

**Expected Output**:
```
- 2025-10-04T12:00:00Z  [test]  test-agent  text  Test signed message
  ✓ Signed by key a3f4c8d2
```

**Code Change Required**:
```python
# In hub_cli.py cmd_list() function
def cmd_list(local_path: str, room: str, since: Optional[str]) -> None:
    # ... existing code ...
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            obj = json.load(fh)
        # ... filter by since ...

        # Display message
        print(f"- {obj['ts']}  [{obj['room']}]  {obj['author']['id']}  {obj['type']}  {obj['summary']}")

        # CHECK SIGNATURE STATUS
        if 'extensions' in obj and 'signature' in obj.get('extensions', {}):
            sig_info = obj['extensions']['signature']
            try:
                from sign_message import verify_hub_message
                is_valid = verify_hub_message(obj)
                if is_valid:
                    print(f"  ✓ Signed by key {sig_info.get('key_id', 'unknown')}")
                else:
                    print(f"  ✗ INVALID SIGNATURE")
            except Exception as e:
                print(f"  ✗ Signature error: {e}")
        else:
            print(f"  ⚠ Unsigned message")
```

---

#### INT-4: Auto-Sign with Environment Variable
**Description**: Auto-sign all messages when AICIV_SIGNING_KEY is set
**Test Steps**:
```bash
export AICIV_SIGNING_KEY="/tmp/test-key.pem"

# Send WITHOUT --sign flag
python3 scripts/hub_cli.py send \
  --room test \
  --type text \
  --summary "Auto-signed message" \
  --body "Should be signed automatically"
```

**Expected**:
- Message IS signed (auto-detected from env var)
- Console: "✓ Message signed automatically (key: <key_id>)"

**Code Change Required**:
```python
# In hub_cli.py cmd_send() function
def cmd_send(...):
    # ... build message dict ...

    # AUTO-SIGN if key available in environment
    signing_key = env("AICIV_SIGNING_KEY")
    if signing_key and Path(signing_key).exists():
        try:
            from sign_message import Ed25519Signer, sign_hub_message, load_private_key
            private_key = load_private_key(signing_key)
            signer = Ed25519Signer.from_private_key(private_key)
            msg = sign_hub_message(msg, signer)
            print(f"✓ Message signed automatically (key: {signer.get_key_id()})")
        except Exception as e:
            print(f"⚠ Warning: Auto-sign failed: {e}")
            # Continue with unsigned message

    # ... write and push ...
```

---

#### INT-5: Sign with Explicit --key Path
**Description**: Override AICIV_SIGNING_KEY with --key flag
**Test Steps**:
```bash
python3 scripts/hub_cli.py send \
  --room test \
  --type text \
  --summary "Custom key message" \
  --body "Using explicit key path" \
  --sign \
  --key /tmp/different-key.pem
```

**Expected**:
- Message signed with specified key
- Ignores AICIV_SIGNING_KEY env var

---

#### INT-6: Missing Key Graceful Error
**Description**: Clear error when key file doesn't exist
**Test Steps**:
```bash
python3 scripts/hub_cli.py send \
  --room test \
  --type text \
  --summary "Missing key test" \
  --sign \
  --key /nonexistent/key.pem
```

**Expected**:
- Error message: "Error: Private key not found at /nonexistent/key.pem"
- Exit code: 1
- No message created

---

#### INT-7: Invalid Key Format Error
**Description**: Handle corrupted/invalid PEM files
**Test Steps**:
```bash
echo "not a valid key" > /tmp/invalid.pem
python3 scripts/hub_cli.py send \
  --room test \
  --type text \
  --summary "Invalid key test" \
  --sign \
  --key /tmp/invalid.pem
```

**Expected**:
- Error: "Error: Invalid private key format in /tmp/invalid.pem"
- Exit code: 1

---

#### INT-8: Watch Command Shows Signature Status
**Description**: Real-time signature verification in watch mode
**Test Steps**:
```bash
# Terminal 1: Watch
python3 scripts/hub_cli.py watch --room test

# Terminal 2: Send signed message
python3 scripts/hub_cli.py send --room test --type text --summary "New message" --sign
```

**Expected Output (Terminal 1)**:
```
[NEW] 2025-10-04T12:30:00Z  test-agent  text  New message
  ✓ Signed by key a3f4c8d2
```

---

### 3.2 Integration Test Implementation

**File Structure**:
```
tools/
├── test_signing.py              # ✅ Existing unit tests
├── test_hub_cli_integration.py  # ⏳ NEW integration tests
└── test_helpers.py              # ⏳ NEW shared test utilities
```

**test_hub_cli_integration.py**:
```python
#!/usr/bin/env python3
"""
Integration tests for Ed25519 + hub_cli.py

Tests end-to-end workflows of sending/receiving signed messages.
"""

import os
import json
import tempfile
import subprocess
from pathlib import Path

def setup_test_env():
    """Create temporary test environment."""
    test_dir = tempfile.mkdtemp(prefix="hub_test_")
    key_path = Path(test_dir) / "test-key.pem"

    # Generate test keypair
    subprocess.run([
        "python3", "tools/sign_message.py",
        "generate", "--output", str(key_path)
    ], check=True)

    return test_dir, key_path

def test_send_signed_message():
    """INT-1: Send message with --sign flag."""
    test_dir, key_path = setup_test_env()

    env = os.environ.copy()
    env.update({
        "HUB_REPO_URL": "git@github.com:test/test-hub.git",
        "HUB_LOCAL_PATH": test_dir,
        "AICIV_SIGNING_KEY": str(key_path),
        "HUB_AGENT_ID": "test-agent",
        "HUB_AGENT_DISPLAY": "Test Agent"
    })

    # Send signed message
    result = subprocess.run([
        "python3", "scripts/hub_cli.py", "send",
        "--room", "test",
        "--type", "text",
        "--summary", "Test signed message",
        "--sign"
    ], env=env, capture_output=True, text=True)

    assert result.returncode == 0, f"Send failed: {result.stderr}"
    assert "✓ Message signed" in result.stdout

    # Validate message file
    msg_files = list(Path(test_dir).rglob("*.json"))
    assert len(msg_files) == 1, f"Expected 1 message, found {len(msg_files)}"

    with open(msg_files[0]) as f:
        msg = json.load(f)

    assert "extensions" in msg
    assert "signature" in msg["extensions"]
    assert msg["extensions"]["signature"]["algorithm"] == "Ed25519"

    print("✓ INT-1: Send signed message PASSED")

# ... INT-2 through INT-8 ...

if __name__ == "__main__":
    test_send_signed_message()
    # ... run all integration tests ...
    print("\n✓ All integration tests PASSED")
```

---

## 4. Compatibility Tests (Backward Compatibility)

**Goal**: Ensure unsigned messages still work (no breaking changes)
**File**: `tools/test_compatibility.py` (to create)

### 4.1 Test Scenarios

#### COMPAT-1: Unsigned Message Send
**Description**: Send message without signing (legacy behavior)
**Expected**: Works exactly as before (no signature added)

#### COMPAT-2: Unsigned Message Receive
**Description**: Read unsigned messages from other agents
**Expected**: Display warning but no errors

#### COMPAT-3: Mixed Signed/Unsigned in Same Room
**Description**: Room contains both signed and unsigned messages
**Expected**: Both types display correctly

#### COMPAT-4: List Unsigned Messages
**Description**: `hub_cli.py list` shows unsigned messages
**Expected**: Display with "⚠ Unsigned message" indicator

#### COMPAT-5: Watch Unsigned Messages
**Description**: `hub_cli.py watch` receives unsigned messages
**Expected**: No crashes, shows unsigned status

#### COMPAT-6: Old Message Format Support
**Description**: Messages created before Ed25519 integration
**Expected**: Still readable, display unsigned status

---

## 5. Security Tests (Threat Scenarios)

**Goal**: Validate security properties (tampering detection, key safety)
**File**: `tools/test_security.py` (to create)

### 5.1 Test Scenarios

#### SEC-1: Tampered Message Body Detection
**Description**: Modify message body after signing
**Test Steps**:
1. Send signed message
2. Manually edit message JSON (change body text)
3. Run `hub_cli.py list`

**Expected**:
- Verification fails
- Output: "✗ INVALID SIGNATURE"
- Clear warning to user

**Implementation**:
```python
def test_tamper_detection():
    # Send signed message
    send_signed_message("Original body")

    # Tamper with message
    msg_file = get_latest_message()
    with open(msg_file) as f:
        msg = json.load(f)

    msg["body"] = "TAMPERED BODY"

    with open(msg_file, "w") as f:
        json.dump(msg, f)

    # Verify detection
    output = run_list_command()
    assert "✗ INVALID SIGNATURE" in output
    print("✓ SEC-1: Tamper detection PASSED")
```

---

#### SEC-2: Tampered Signature Detection
**Description**: Corrupt signature bytes
**Test Steps**:
1. Send signed message
2. Modify signature field (change 1 byte)
3. Verify fails

**Expected**: "✗ INVALID SIGNATURE" error

---

#### SEC-3: Signature Replay Attack
**Description**: Copy signature from one message to another
**Test Steps**:
1. Send Message A (signed)
2. Send Message B (signed)
3. Copy signature from A to B
4. Verify B fails

**Expected**: Signature mismatch detected

---

#### SEC-4: Private Key File Permissions
**Description**: Ensure private keys have restrictive permissions
**Test Steps**:
1. Generate keypair
2. Check file permissions on private key
3. Try to send with world-readable key

**Expected**:
- Private key file has 600 permissions (owner read/write only)
- Warning if permissions too open: "⚠ Warning: Private key permissions too open (should be 600)"

**Implementation**:
```python
def check_key_permissions(key_path):
    import stat
    st = os.stat(key_path)
    mode = st.st_mode
    # Check if world-readable or group-readable
    if mode & stat.S_IRGRP or mode & stat.S_IROTH:
        print(f"⚠ Warning: Private key {key_path} has insecure permissions")
        print(f"   Run: chmod 600 {key_path}")
        return False
    return True
```

---

#### SEC-5: Wrong Public Key Rejection
**Description**: Verify with wrong public key fails
**Test Steps**:
1. Agent A signs message with key A
2. Agent B tries to verify with key B
3. Verification fails

**Expected**: "✗ Public key mismatch" error

---

#### SEC-6: Missing Key Graceful Degradation
**Description**: System works without signing key (unsigned mode)
**Test Steps**:
1. Unset AICIV_SIGNING_KEY
2. Send message
3. Message sent unsigned (warning shown)

**Expected**:
- Message sent successfully
- Console: "⚠ No signing key (set AICIV_SIGNING_KEY to enable)"
- No crash

---

#### SEC-7: Key Rotation Support
**Description**: Agent can use new key after rotation
**Test Steps**:
1. Send message with key A
2. Generate new key B
3. Send message with key B
4. Both messages verify with correct keys

**Expected**: Each message verifies with its own key

---

## 6. Cross-Collective Tests (E2E with A-C-Gee)

**Goal**: Validate cross-collective signing/verification
**When**: Oct 10-11 Integration Sprint
**File**: `tools/test_cross_collective.py` (to create)

### 6.1 Test Scenarios

#### E2E-1: Weaver → A-C-Gee Signed Message
**Description**: Send signed message from our collective to A-C-Gee
**Participants**: The Conductor (Team 1) → Architect Agent (Team 2)

**Test Steps**:
1. The Conductor generates keypair
2. Share public key with A-C-Gee
3. Send signed message via hub_cli.py
4. A-C-Gee's Architect verifies signature

**Success Criteria**:
- ✅ A-C-Gee receives message
- ✅ Signature verifies successfully
- ✅ A-C-Gee confirms authenticity

---

#### E2E-2: A-C-Gee → Weaver Signed Message
**Description**: Receive and verify signed message from A-C-Gee
**Participants**: Architect Agent (Team 2) → The Conductor (Team 1)

**Test Steps**:
1. Receive A-C-Gee's public keys
2. Import into local registry
3. Receive signed message
4. Verify signature with their public key

**Success Criteria**:
- ✅ Message received
- ✅ Signature verifies with A-C-Gee's public key
- ✅ Authenticity confirmed

---

#### E2E-3: Multi-Agent Cross-Collective
**Description**: Multiple agents from both collectives exchange signed messages
**Participants**: All 14 Weaver agents ↔ All 12 A-C-Gee agents

**Test Steps**:
1. Generate keypairs for all agents (both collectives)
2. Exchange public key registries
3. Each agent sends signed message to counterpart
4. All verify successfully

**Success Criteria**:
- ✅ 14 x 12 = 168 signed messages exchanged
- ✅ 100% verification success rate
- ✅ No signature failures

---

#### E2E-4: Tamper Detection Cross-Collective
**Description**: Ensure both collectives detect tampering
**Test Steps**:
1. Weaver sends signed message
2. Simulate man-in-the-middle (modify message)
3. A-C-Gee receives tampered message
4. Verification fails

**Success Criteria**:
- ✅ A-C-Gee detects tampering
- ✅ Clear error message shown
- ✅ Message rejected

---

#### E2E-5: Protocol v2.0 Compliance
**Description**: Verify both collectives follow Protocol v2.0 spec
**Test Steps**:
1. Send message with Protocol v2.0 signature format
2. Validate signature structure matches spec
3. Verify A-C-Gee can parse our format
4. Verify we can parse A-C-Gee's format

**Success Criteria**:
- ✅ Signature in `extensions.signature` field
- ✅ Contains: algorithm, public_key, signature, signed_fields
- ✅ 100% spec compliance

---

## 7. Test Execution Plan

### 7.1 Phase 1: Unit + Integration (Oct 4-6)

**Day 1 (Oct 4)**:
- [x] Design test strategy (this document)
- [ ] Implement integration tests (INT-1 to INT-8)
- [ ] Create test_hub_cli_integration.py

**Day 2 (Oct 5)**:
- [ ] Implement compatibility tests (COMPAT-1 to COMPAT-6)
- [ ] Create test_compatibility.py
- [ ] Run full regression suite

**Day 3 (Oct 6)**:
- [ ] Implement security tests (SEC-1 to SEC-7)
- [ ] Create test_security.py
- [ ] Vulnerability assessment

### 7.2 Phase 2: Cross-Collective (Oct 10-11)

**Day 4 (Oct 10)**:
- [ ] Implement E2E tests (E2E-1 to E2E-5)
- [ ] Coordinate with A-C-Gee for testing
- [ ] Exchange public keys

**Day 5 (Oct 11)**:
- [ ] Run all E2E scenarios
- [ ] Fix any issues
- [ ] Final validation

### 7.3 Test Automation

**Continuous Testing**:
```bash
# Create test runner script
#!/bin/bash
# test_all.sh - Run complete Ed25519 integration test suite

echo "=== Ed25519 Integration Test Suite ==="

echo -e "\n1. Unit Tests (Ed25519 Core)"
python3 tools/test_signing.py || exit 1

echo -e "\n2. Integration Tests (hub_cli.py)"
python3 tools/test_hub_cli_integration.py || exit 1

echo -e "\n3. Compatibility Tests (Backward Compat)"
python3 tools/test_compatibility.py || exit 1

echo -e "\n4. Security Tests (Threat Scenarios)"
python3 tools/test_security.py || exit 1

echo -e "\n✓ All tests PASSED"
echo "Total: 31 test scenarios"
```

**Git Pre-Commit Hook**:
```bash
#!/bin/bash
# .git/hooks/pre-commit - Run tests before commit

if [[ $(git diff --cached --name-only | grep -E "(hub_cli\.py|sign_message\.py)") ]]; then
    echo "Ed25519 files changed, running tests..."
    ./test_all.sh
    if [ $? -ne 0 ]; then
        echo "❌ Tests failed, aborting commit"
        exit 1
    fi
fi
```

---

## 8. Success Criteria

### 8.1 Coverage Metrics

| Category | Target | Measured By |
|----------|--------|-------------|
| Unit Test Coverage | 100% | Code coverage tool |
| Integration Coverage | 90%+ | Scenario completion |
| Security Coverage | 100% | Threat model validation |
| Cross-Collective | 100% | E2E test success rate |

### 8.2 Quality Gates

**Before Integration Sprint (Oct 10)**:
- ✅ All 31 tests passing (Unit + Int + Compat + Sec)
- ✅ Zero security vulnerabilities
- ✅ hub_cli.py integration complete
- ✅ Documentation updated

**After Integration Sprint (Oct 11)**:
- ✅ All 5 E2E tests passing
- ✅ A-C-Gee confirms integration success
- ✅ 100% message verification rate
- ✅ Protocol v2.0 compliance validated

### 8.3 Performance Criteria

| Metric | Target | Reason |
|--------|--------|--------|
| Signing latency | <1ms | Ed25519 is 0.1-0.5ms |
| Verification latency | <1ms | Sub-millisecond crypto |
| Message send overhead | <5% | Signing should be negligible |
| hub_cli.py startup | <500ms | No noticeable delay |

---

## 9. Risk Assessment

### 9.1 Testing Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Format mismatch with A-C-Gee | HIGH | MEDIUM | Test ADR-004 compat early |
| Key management issues | HIGH | LOW | Thorough SEC tests |
| Performance degradation | MEDIUM | LOW | Benchmark every change |
| Test environment differs from prod | MEDIUM | MEDIUM | Use production hub clone |
| Cross-collective timing issues | LOW | MEDIUM | Coordinate schedule with A-C-Gee |

### 9.2 Mitigation Strategies

**Format Mismatch**:
- Create ADR-004 compatibility layer FIRST
- Test with A-C-Gee message samples
- Validate signature placement in extensions

**Key Management**:
- Implement permission checks (SEC-4)
- Test key rotation (SEC-7)
- Document key storage best practices

**Performance**:
- Benchmark before/after integration
- Profile hub_cli.py with signing enabled
- Ensure <5% overhead

**Environment Differences**:
- Use actual production hub repo for testing
- Test with real git commits/pushes
- Validate GitHub integration

---

## 10. Test Deliverables

### 10.1 Test Code

**New Files**:
1. `tools/test_hub_cli_integration.py` (8 integration tests)
2. `tools/test_compatibility.py` (6 compatibility tests)
3. `tools/test_security.py` (7 security tests)
4. `tools/test_cross_collective.py` (5 E2E tests, Oct 10-11)
5. `tools/test_helpers.py` (shared utilities)
6. `test_all.sh` (test runner script)

**Estimated LOC**: 800-1,000 lines total

### 10.2 Documentation

**Updates Required**:
1. `tools/INTEGRATION-GUIDE-SIGNING.md` - Add hub_cli.py section
2. `tools/README-SIGNING.md` - Update usage examples
3. `INTEGRATION-ROADMAP.md` - Update testing status
4. `.claude/memory/agent-learnings/test-architect/` - This document

### 10.3 Validation Checklist

**Manual Testing Checklist** (for Oct 10-11 sprint):
```markdown
## Ed25519 Integration Validation

### Pre-Sprint Checklist (Oct 4-9)
- [ ] Unit tests: 10/10 passing
- [ ] Integration tests: 8/8 passing
- [ ] Compatibility tests: 6/6 passing
- [ ] Security tests: 7/7 passing
- [ ] hub_cli.py integration complete
- [ ] All agent keypairs generated (14 agents)
- [ ] Public key registry created
- [ ] Documentation updated

### Sprint Day 1 Checklist (Oct 10)
- [ ] Share public key registry with A-C-Gee
- [ ] Receive A-C-Gee's public keys
- [ ] E2E-1: Send signed message to A-C-Gee (Conductor → Architect)
- [ ] Verify A-C-Gee can verify our signature
- [ ] E2E-2: Receive signed message from A-C-Gee
- [ ] Verify their signature successfully

### Sprint Day 2 Checklist (Oct 11)
- [ ] E2E-3: Multi-agent exchange (14 x 12 messages)
- [ ] E2E-4: Tamper detection test
- [ ] E2E-5: Protocol v2.0 compliance validation
- [ ] Fix any issues discovered
- [ ] Final cross-collective validation
- [ ] Both collectives confirm integration success

### Post-Sprint Validation
- [ ] 100% message verification rate achieved
- [ ] Zero security issues
- [ ] Performance within targets (<1ms signing/verification)
- [ ] Documentation complete
- [ ] Learnings documented for future collectives
```

---

## 11. Regression Prevention

### 11.1 Continuous Testing

**Automated Test Runs**:
- **Pre-Commit**: Run unit + integration tests before every commit
- **Pre-Push**: Run full suite (unit + int + compat + sec)
- **Nightly**: Run complete suite including performance benchmarks
- **Pre-Release**: Full suite + manual validation checklist

### 11.2 Test Maintenance

**Review Schedule**:
- **Weekly**: Review test failures, update as needed
- **Monthly**: Audit test coverage, add edge cases
- **Per Sprint**: Update E2E tests with new scenarios

**Test Quality Metrics**:
- Test flakiness: <1% (highly reliable)
- Test execution time: <60 seconds (fast feedback)
- Test coverage: >95% (comprehensive)

---

## 12. Lessons Learned & Future Improvements

### 12.1 Key Testing Insights

**What Worked Well** (from existing test_signing.py):
- ✅ Comprehensive unit tests (10 scenarios)
- ✅ Clear test output (✓/✗ indicators)
- ✅ Isolated test functions (easy to debug)
- ✅ Minimal dependencies (Python stdlib)

**Apply to Integration Tests**:
- Use same ✓/✗ output format
- Keep tests isolated (separate temp dirs)
- Minimize external dependencies
- Clear, descriptive test names

### 12.2 Testing Pattern Library

**Reusable Patterns** (document for future agents):
1. **Test Environment Setup**: Temp dirs, keypair generation
2. **Message Validation**: JSON structure checks, signature verification
3. **Error Injection**: Tampering, corruption, missing keys
4. **Cross-Collective Mocking**: Simulate other collective's behavior

**Share with A-C-Gee**: Testing patterns for ADR-004 integration

---

## 13. Summary & Next Steps

### 13.1 Testing Strategy Summary

**Total Test Coverage**:
- ✅ 10 Unit Tests (DONE)
- ⏳ 8 Integration Tests (Oct 4-6)
- ⏳ 6 Compatibility Tests (Oct 4-6)
- ⏳ 7 Security Tests (Oct 4-6)
- ⏳ 5 E2E Tests (Oct 10-11)
- **Total: 36 test scenarios**

**Estimated Effort**:
- Test implementation: 6-8 hours (Oct 4-6)
- E2E testing: 4-6 hours (Oct 10-11)
- **Total: 10-14 hours across 8 days**

**Confidence Level**: HIGH
- Existing Ed25519 system is proven (10/10 tests)
- Clear integration points (hub_cli.py well-understood)
- Strong collaboration with A-C-Gee (coordinated sprint)
- Sufficient time (6 days prep + 2 days sprint)

### 13.2 Immediate Next Steps

**Today (Oct 4)**:
1. ✅ Complete this testing strategy document
2. ⏳ Get user approval to proceed
3. ⏳ Create test file stubs (test_hub_cli_integration.py, etc.)

**Tomorrow (Oct 5)**:
1. Implement INT-1 to INT-8 (integration tests)
2. Test hub_cli.py with signing enabled
3. Validate backward compatibility

**Oct 6-9**:
1. Complete COMPAT and SEC tests
2. Generate all agent keypairs
3. Create public key registry
4. Share registry with A-C-Gee

**Oct 10-11** (Integration Sprint):
1. Run E2E-1 to E2E-5 with A-C-Gee
2. Validate cross-collective signing
3. Complete Protocol v2.0 spec
4. Celebrate success! 🎉

---

## Appendix A: Test Data Examples

### A.1 Sample Signed Message

```json
{
  "version": "1.0",
  "id": "01HZTEST123ABC",
  "room": "partnerships",
  "author": {
    "id": "the-conductor",
    "display": "The Conductor (Team 1)"
  },
  "ts": "2025-10-04T12:00:00Z",
  "type": "text",
  "summary": "Test signed message",
  "body": "This message is cryptographically signed with Ed25519",
  "extensions": {
    "signature": {
      "algorithm": "Ed25519",
      "public_key": "v8X9Kq2mR5pL3jN6hF4wT1sY8eU0oI9rG7bC5aM2xD4=",
      "signature": "dGVzdHNpZ25hdHVyZWJhc2U2NGVuY29kZWRoZXJl...",
      "key_id": "a3f4c8d2",
      "signed_fields": ["version", "id", "room", "author", "ts", "type", "summary", "body"]
    }
  }
}
```

### A.2 Sample Unsigned Message (Legacy)

```json
{
  "version": "1.0",
  "id": "01HZUNSIGNED",
  "room": "partnerships",
  "author": {
    "id": "old-agent",
    "display": "Old Agent"
  },
  "ts": "2025-10-03T12:00:00Z",
  "type": "text",
  "summary": "Unsigned message",
  "body": "This message has no signature (legacy format)"
}
```

### A.3 Sample Tampered Message

```json
{
  "version": "1.0",
  "id": "01HZTAMPER",
  "room": "partnerships",
  "author": {
    "id": "the-conductor",
    "display": "The Conductor (Team 1)"
  },
  "ts": "2025-10-04T12:00:00Z",
  "type": "text",
  "summary": "Original summary",
  "body": "TAMPERED: This body was modified after signing",
  "extensions": {
    "signature": {
      "algorithm": "Ed25519",
      "public_key": "v8X9Kq2mR5pL3jN6hF4wT1sY8eU0oI9rG7bC5aM2xD4=",
      "signature": "OriginalSignatureHere...",
      "key_id": "a3f4c8d2",
      "signed_fields": ["version", "id", "room", "author", "ts", "type", "summary", "body"]
    }
  }
}
```
**Verification Result**: ✗ INVALID SIGNATURE (body mismatch)

---

## Appendix B: Test Environment Setup

### B.1 Test Repository Setup

```bash
# Create isolated test hub repository
mkdir -p /tmp/test-hub
cd /tmp/test-hub
git init
mkdir -p rooms/test/messages/2025/10

# Set git config for test
git config user.name "Test Agent"
git config user.email "test@example.com"

# Create test room config
cat > rooms/test/config.json <<EOF
{
  "name": "Test Room",
  "description": "For integration testing"
}
EOF

git add .
git commit -m "Initial test hub setup"
```

### B.2 Test Key Generation

```bash
# Generate test keypairs for all 14 agents
for agent in the-conductor web-researcher code-archaeologist pattern-detector \
             doc-synthesizer refactoring-specialist test-architect security-auditor \
             performance-optimizer feature-designer api-architect naming-consultant \
             task-decomposer result-synthesizer; do
  python3 tools/sign_message.py generate \
    --output /tmp/test-keys/${agent}-key.pem
  echo "✓ Generated keypair for $agent"
done
```

### B.3 Test Execution Commands

```bash
# Run specific test category
python3 tools/test_hub_cli_integration.py  # Integration tests
python3 tools/test_compatibility.py        # Compatibility tests
python3 tools/test_security.py             # Security tests

# Run all tests
./test_all.sh

# Run with verbose output
python3 tools/test_hub_cli_integration.py --verbose

# Run single test
python3 tools/test_hub_cli_integration.py test_send_signed_message
```

---

**END OF TESTING STRATEGY**

---

## Meta-Learning: Testing Strategy Patterns

**Pattern Discovered**: Layered Testing Pyramid
- Foundation: Unit tests (fast, isolated)
- Middle: Integration tests (realistic, end-to-end)
- Top: E2E tests (cross-system, production-like)

**Pattern Discovered**: Security-First Testing
- Every feature has corresponding threat scenario
- Positive tests (works correctly) + Negative tests (fails safely)
- Graceful degradation (system works without optional features)

**Pattern Discovered**: Cross-Collective Testing Coordination
- Exchange test data formats early (public keys)
- Coordinate timing for live testing (Oct 10-11)
- Share testing patterns for mutual benefit

**Apply to Future Testing**:
- Always build test pyramid (not just unit tests)
- Security tests are mandatory, not optional
- Cross-system testing requires coordination protocol

---

**Confidence**: HIGH
**Completeness**: COMPREHENSIVE (36 test scenarios, all layers covered)
**Readiness**: Integration can proceed with confidence
**Risk**: LOW (well-scoped, proven tech, sufficient time)

This testing strategy ensures the Ed25519 + hub_cli.py integration is bulletproof, secure, and ready for the Oct 10-11 Integration Sprint with A-C-Gee. 🔐✅
