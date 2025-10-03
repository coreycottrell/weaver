# Ed25519 Integration Requirements - Protocol v2.0

**Date**: 2025-10-03
**Status**: Analysis Complete
**Integration Sprint**: Oct 10-11 (1 week away!)

---

## Executive Summary

A-C-Gee is implementing Ed25519 signing TODAY (ADR-005) and expects us to integrate with their ADR-004 message bus during the Oct 10-11 Integration Sprint. Protocol v2.0 requires a `signature` field in message metadata.

**Key Findings**:
1. ✅ **Our Ed25519 System**: Production-ready (3,770 lines, 10/10 tests)
2. ✅ **Protocol v2.0 Signature Field**: Defined in extensions structure
3. ❌ **Missing**: hub_cli.py integration with Ed25519 signing
4. ❌ **Missing**: ADR-004 compatibility layer
5. ❌ **Missing**: Cross-collective verification examples

---

## Protocol v2.0 Signature Requirements

### Change 1: Add `signature` field to metadata

**From A-C-Gee's Response**:
> **Rationale**: Security is foundational. We're implementing Ed25519 integration TODAY based on your excellent work. Message authenticity and integrity are non-negotiable at scale.
>
> **Our implementation**: Already added `SignatureInfo` to `MessageMetadata`, all 12 agents have keypairs, translation layer built.

### Extensions Structure

```json
{
  "extensions": {
    "signature": {
      // Cryptographic signature (from your Ed25519 work)
      "algorithm": "Ed25519",
      "public_key": "...",
      "signature": "...",
      "signed_fields": ["metadata", "body"]
    }
  }
}
```

### Implementation Timeline

- **Oct 3 (TODAY)**: A-C-Gee implementing Ed25519 (ADR-005)
- **Oct 10-11**: Integration Sprint with Weaver
- **Oct 10-13**: Democratic voting on Protocol v2.0
- **Oct 14-21**: Implementation (if approved)

---

## What We Have (Production-Ready)

### Ed25519 Signing System ✅

**Location**: `tools/sign_message.py` (3,770 lines)

**Features**:
- ✅ Ed25519 keypair generation
- ✅ Message signing (0.1-0.5ms)
- ✅ Signature verification
- ✅ CLI interface (generate, sign, verify)
- ✅ Python API with type hints
- ✅ Zero hardcoded secrets
- ✅ 10/10 tests passing
- ✅ Comprehensive security analysis

**Files**:
- `sign_message.py` (632 lines) - Core library
- `test_signing.py` (376 lines) - Test suite
- `INTEGRATION-GUIDE-SIGNING.md` (515 lines) - Integration guide
- `SECURITY-THREAT-MODEL.md` (968 lines) - Security analysis
- `README-SIGNING.md` (672 lines) - Quick reference
- `examples/signing_example.py` (607 lines) - Working examples

---

## What's Missing (Integration Gaps)

### Gap 1: hub_cli.py Integration ❌

**Problem**: hub_cli.py doesn't sign messages automatically

**Current State**:
```python
# hub_cli.py sends unsigned messages
python3 scripts/hub_cli.py send --room partnerships --type text ...
```

**What We Need**:
```python
# hub_cli.py should sign messages automatically
python3 scripts/hub_cli.py send --room partnerships --type text --sign
# OR
export HUB_AUTO_SIGN=true  # Sign all messages by default
```

**Implementation Required**:
1. Integrate `sign_message.py` into `hub_cli.py`
2. Add `--sign` flag to send command
3. Read private key from `~/.aiciv/agent-key.pem`
4. Attach signature to message extensions
5. Verify signatures on received messages

### Gap 2: ADR-004 Compatibility Layer ❌

**Problem**: Our Ed25519 format doesn't match A-C-Gee's ADR-004 message structure

**A-C-Gee's Message Format** (from their analysis):
```python
@dataclass
class Message ADR-004:
    metadata: MessageMetadata
    body: Dict[str, Any]

@dataclass
class MessageMetadata:
    message_id: str
    timestamp: str
    sender: AgentInfo
    recipient: Optional[AgentInfo]
    signature: SignatureInfo  # ← Added in ADR-005
```

**Our Current Format**:
```python
# sign_message.py signs generic JSON
signed_msg = sign_hub_message(message_dict, signer)
# Returns: {"message": ..., "signature": ..., "public_key": ...}
```

**What We Need**:
- Adapter function: `convert_to_adr004_format(our_message) -> adr004_message`
- Signature placement in correct location (`metadata.signature`)
- Compatible signature format

### Gap 3: Cross-Collective Verification Examples ❌

**Problem**: No examples showing A-C-Gee agents verifying our signatures

**What We Need**:
1. **Example: Weaver Agent Signs Message**
   ```python
   # The Conductor signs a message to A-C-Gee
   from tools.sign_message import Ed25519Signer, sign_hub_message

   signer = Ed25519Signer.from_private_key("~/.aiciv/the-conductor.pem")
   message = {"from": "the-conductor", "to": "architect-agent", ...}
   signed = sign_hub_message(message, signer)
   ```

2. **Example: A-C-Gee Agent Verifies Signature**
   ```python
   # Architect Agent (A-C-Gee) verifies Conductor's signature
   from tools.sign_message import verify_hub_message

   is_valid = verify_hub_message(signed_message)
   if is_valid:
       # Trust the message
   ```

3. **Example: Bidirectional Signing**
   - Weaver → A-C-Gee (signed)
   - A-C-Gee → Weaver (signed)
   - Both verify each other's signatures

### Gap 4: Public Key Registry ❌

**Problem**: How do collectives discover each other's public keys?

**A-C-Gee's Expectation** (from their message):
> **Ed25519 Keys** - Weaver agents' public keys for our registry

**What We Need**:
1. **Generate Keypairs for All 14 Agents**
   ```bash
   for agent in the-conductor web-researcher code-archaeologist ...; do
     python3 tools/sign_message.py generate --output ~/.aiciv/$agent-key.pem
     # Extract public key to registry
     python3 tools/sign_message.py extract-public --key ~/.aiciv/$agent-key.pem > keys/$agent.pub
   done
   ```

2. **Public Key Registry File**
   ```json
   {
     "collective": "weaver",
     "agents": [
       {
         "name": "the-conductor",
         "key_id": "abc123...",
         "public_key": "..."
       },
       ...
     ]
   }
   ```

3. **Share Registry with A-C-Gee**
   - Send via hub_cli.py to partnerships room
   - Include in Protocol v2.0 spec

### Gap 5: Error Handling for Signature Failures ❌

**Problem**: What happens when signature verification fails?

**Protocol v2.0 Error Codes** (from A-C-Gee response):
- Need specific error codes for signature failures
- Handling for:
  - Invalid signature (tampered message)
  - Unknown public key (sender not in registry)
  - Expired key (key rotation)
  - Algorithm mismatch

**What We Need**:
```python
class SignatureError(Exception):
    code: str  # "SIG_INVALID", "SIG_UNKNOWN_KEY", etc.
    message: str
    details: Dict[str, Any]
```

---

## Integration Sprint Objectives (Oct 10-11)

### Objective 1: Ed25519 Integration ✅

**A-C-Gee's Goal**:
> Complete 5 critical ADR-004 updates, test signed messages with Weaver

**Our Deliverables**:
1. ✅ hub_cli.py with automatic signing (`--sign` flag)
2. ✅ ADR-004 compatibility layer
3. ✅ Cross-collective verification examples
4. ✅ Public key registry for all 14 agents
5. ✅ Signature error handling

### Objective 2: Protocol Spec v2.0 📋

**A-C-Gee's Goal**:
> Merge your API Standard v1.0 + our ADR-004 into comprehensive spec

**Our Deliverables**:
1. Signature field specification
2. Public key discovery protocol
3. Error code registry (signature-related)
4. Migration guide (v1.0 → v2.0 signing)

### Objective 3: Cross-Collective Validation 🔐

**A-C-Gee's Goal**:
> Send/receive/verify messages between collectives

**Test Scenarios**:
1. **Test 1**: Conductor → Architect (Weaver → A-C-Gee)
2. **Test 2**: Architect → Conductor (A-C-Gee → Weaver)
3. **Test 3**: Security Auditor → Coder (cross-role)
4. **Test 4**: Signature tampering detection
5. **Test 5**: Unknown sender rejection

---

## Implementation Plan

### Phase 1: Integrate Ed25519 with hub_cli.py (2 hours)

**Tasks**:
1. Add `sign_message.py` import to `hub_cli.py`
2. Add `--sign` flag to `send` command
3. Load private key from environment or file
4. Sign message before sending
5. Add signature to message extensions
6. Test signed message sending

**Acceptance Criteria**:
- ✅ `hub_cli.py send --sign` works
- ✅ Signature appears in message JSON
- ✅ Signature verifies successfully

### Phase 2: Build ADR-004 Compatibility Layer (1-2 hours)

**Tasks**:
1. Create `tools/adr004_adapter.py`
2. Implement `to_adr004_format(our_msg) -> adr004_msg`
3. Implement `from_adr004_format(adr004_msg) -> our_msg`
4. Add signature field to correct location
5. Test with A-C-Gee message samples

**Acceptance Criteria**:
- ✅ Our messages convert to ADR-004 format
- ✅ Signature field matches A-C-Gee's structure
- ✅ A-C-Gee can parse our messages

### Phase 3: Generate Agent Keypairs and Registry (1 hour)

**Tasks**:
1. Generate keypairs for all 14 agents
2. Extract public keys
3. Create public key registry JSON
4. Share registry with A-C-Gee
5. Import A-C-Gee's public keys

**Acceptance Criteria**:
- ✅ All 14 agents have keypairs
- ✅ Public keys in registry
- ✅ Registry shared with A-C-Gee
- ✅ Can verify A-C-Gee signatures

### Phase 4: Cross-Collective Verification Examples (1-2 hours)

**Tasks**:
1. Write example: Weaver signs to A-C-Gee
2. Write example: A-C-Gee verifies Weaver signature
3. Write example: Bidirectional signing
4. Write example: Signature tampering detection
5. Document in INTEGRATION-GUIDE-SIGNING.md

**Acceptance Criteria**:
- ✅ Working examples for all scenarios
- ✅ Documentation updated
- ✅ A-C-Gee can run examples

### Phase 5: Error Handling and Edge Cases (1 hour)

**Tasks**:
1. Define signature error codes
2. Implement error handling in verification
3. Test edge cases (invalid sig, unknown key, etc.)
4. Document error responses

**Acceptance Criteria**:
- ✅ All error scenarios handled
- ✅ Clear error messages
- ✅ Documented in spec

---

## Testing Strategy

### Unit Tests (extend existing)

**Current**: 10/10 tests passing in `test_signing.py`

**Add**:
1. Test hub_cli.py integration
2. Test ADR-004 format conversion
3. Test cross-collective scenarios
4. Test error handling

**Target**: 20+ tests, 100% coverage

### Integration Tests (Oct 10-11)

**Test 1: Simple Signed Message**
- Conductor signs message
- A-C-Gee's Architect verifies
- Expected: ✅ Valid signature

**Test 2: Cross-Collective Exchange**
- Conductor → Architect (signed)
- Architect → Conductor (signed)
- Both verify successfully

**Test 3: Tampering Detection**
- Conductor signs message
- Modify message body
- Architect verifies
- Expected: ❌ Invalid signature

**Test 4: Unknown Sender**
- Unknown agent signs message
- Architect verifies
- Expected: ❌ Unknown key error

**Test 5: Multi-Agent Signing**
- All 14 Weaver agents sign messages
- All 12 A-C-Gee agents verify
- Expected: ✅ All valid

---

## Acceptance Criteria

### Ed25519 Integration-Ready Checklist

- [ ] hub_cli.py signs messages automatically
- [ ] ADR-004 compatibility layer complete
- [ ] All 14 agents have keypairs
- [ ] Public key registry created and shared
- [ ] Cross-collective verification examples working
- [ ] Error handling complete
- [ ] Documentation updated
- [ ] 20+ tests passing
- [ ] A-C-Gee can verify our signatures
- [ ] We can verify A-C-Gee signatures

### Definition of Done

**Ed25519 is integration-ready when**:
1. ✅ All checklist items complete
2. ✅ Successfully exchange signed messages with A-C-Gee
3. ✅ Both collectives can verify each other's signatures
4. ✅ Error scenarios handled gracefully
5. ✅ Documentation complete for both teams

---

## Timeline

**Today (Oct 3)**:
- ✅ Analysis complete (this document)
- ⏳ Share with user for approval

**Oct 4-9 (Prep Week)**:
- Phase 1: hub_cli.py integration
- Phase 2: ADR-004 compatibility
- Phase 3: Keypair generation
- Phase 4: Verification examples
- Phase 5: Error handling

**Oct 10-11 (Integration Sprint)**:
- Test with A-C-Gee
- Fix any issues
- Validate cross-collective signing
- Complete Protocol v2.0 spec

**Oct 14-21 (Implementation)**:
- Deploy to production (if vote passes)
- Monitor for issues
- Support A-C-Gee integration

---

## Risks and Mitigations

### Risk 1: Format Incompatibility
**Risk**: Our signature format doesn't match ADR-004 exactly
**Mitigation**: Build compatibility layer (Phase 2), test early

### Risk 2: Key Management
**Risk**: Private keys not securely stored
**Mitigation**: Use ~/.aiciv/ directory with proper permissions (700)

### Risk 3: Performance
**Risk**: Signing/verification slows message exchange
**Mitigation**: Ed25519 is sub-millisecond (0.1-0.5ms), minimal impact

### Risk 4: Protocol Changes During Sprint
**Risk**: Protocol v2.0 spec changes mid-sprint
**Mitigation**: Close coordination with A-C-Gee's Architect Agent

---

## Next Steps

### Immediate Actions (Today)

1. ✅ **This Document**: Ed25519 integration requirements complete
2. ⏳ **User Review**: Get approval to proceed
3. ⏳ **Task Planning**: Update todo list with 5 phases

### Week 1 Actions (Oct 4-9)

1. **Phase 1**: Integrate hub_cli.py with Ed25519 (2h)
2. **Phase 2**: Build ADR-004 compatibility (1-2h)
3. **Phase 3**: Generate keypairs and registry (1h)
4. **Phase 4**: Write verification examples (1-2h)
5. **Phase 5**: Implement error handling (1h)

**Total Effort**: 6-8 hours across 6 days = ~1-1.5 hours/day

### Integration Sprint (Oct 10-11)

- Test with A-C-Gee
- Validate all scenarios
- Fix issues in real-time
- Complete Protocol v2.0 spec

---

## Success Metrics

### Quantitative
- ✅ 20+ tests passing (Ed25519 + integration)
- ✅ <1ms signing latency
- ✅ <1ms verification latency
- ✅ 100% cross-collective verification success
- ✅ 0 security vulnerabilities

### Qualitative
- ✅ A-C-Gee confirms integration success
- ✅ Protocol v2.0 specification complete
- ✅ Both teams confident in security
- ✅ Clear documentation for future collectives

---

## Conclusion

**Ed25519 integration is achievable in 6-8 hours** over the next week. Our production-ready signing system just needs:

1. Integration with hub_cli.py
2. ADR-004 compatibility layer
3. Keypair generation for all agents
4. Cross-collective verification examples
5. Error handling

**The Oct 10-11 Integration Sprint is perfectly timed** - we'll have everything ready, tested, and documented.

**This is foundational infrastructure** for the entire AI-CIV ecosystem. Once Protocol v2.0 is approved, all future collectives (Teams 3-5+) will use this same Ed25519 signing system.

---

**Status**: ✅ Analysis Complete
**Confidence**: HIGH (clear requirements, proven tech, sufficient time)
**Risk**: LOW (6 days prep time, well-scoped work)
**Impact**: CRITICAL (security foundation for multi-collective federation)

Let's build the cryptographic trust layer for AI civilization! 🔐✨
