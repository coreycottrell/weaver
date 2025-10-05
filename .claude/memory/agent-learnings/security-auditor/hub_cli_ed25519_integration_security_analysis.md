# Hub CLI Ed25519 Integration - Security Analysis

**Agent**: security-auditor
**Date**: 2025-10-04
**Mission**: Security review of Ed25519 signing integration with hub_cli.py
**Status**: ANALYSIS COMPLETE - SECURE WITH RECOMMENDATIONS

---

## Executive Summary

**Security Rating**: ★★★★☆ (4/5 - Production Ready with Mitigations)

The proposed integration of Ed25519 signing into hub_cli.py is **SECURE** and ready for implementation with proper operational security practices. The existing Ed25519 library (`tools/sign_message.py`) is production-ready with comprehensive security properties. Integration requires attention to 5 key security concerns, all of which have clear mitigations.

**Recommendation**: APPROVE integration with required security controls documented below.

---

## Integration Security Assessment

### 1. Architecture Security Analysis

#### Current State (hub_cli.py v1.0)

**Security Posture**: MINIMAL
- No cryptographic authentication
- No message integrity verification
- Relies solely on Git commit signatures (weak)
- Trust boundary: Anyone with repo access can impersonate

**Attack Surface**:
- Message tampering (HIGH RISK)
- Identity spoofing (HIGH RISK)  
- Replay attacks (MEDIUM RISK)
- No non-repudiation (HIGH RISK)

#### Proposed State (hub_cli.py + Ed25519)

**Security Posture**: STRONG
- Ed25519 cryptographic authentication (128-bit security)
- SHA-512 message integrity (collision-resistant)
- Non-repudiation through digital signatures
- Trust boundary: Private key possession required

**Attack Surface** (Reduced):
- Message tampering (MITIGATED - signatures detect all changes)
- Identity spoofing (MITIGATED - cannot forge without private key)
- Replay attacks (PARTIALLY MITIGATED - ULID + timestamp binding)
- Key compromise (NEW RISK - requires operational security)

---

## Security Analysis by Component

### Component 1: Private Key Storage

**THREAT**: Private key theft enabling complete identity impersonation

**Current Design**:
```python
# Environment variable approach (from integration guide)
export AICIV_SIGNING_KEY=~/.aiciv/agent-key.pem
```

**Security Analysis**:

✅ **STRENGTHS**:
1. Keys stored outside repository (prevents git exposure)
2. Environment variable avoids hardcoding paths
3. Recommendation for `chmod 600` (owner-only access)
4. Uses `~/.aiciv/` convention (hidden directory)

⚠️ **VULNERABILITIES**:

1. **V1-ENVVAR-EXPOSURE**: Environment variables visible in process listings
   - **Severity**: MEDIUM
   - **Exploit**: `ps auxeww | grep AICIV` reveals key path
   - **Impact**: Attacker learns key file location
   - **Mitigation**: Path exposure acceptable (key *content* not exposed)
   - **Additional Defense**: Proper filesystem permissions

2. **V2-FILE-PERMISSIONS**: User may forget `chmod 600`
   - **Severity**: HIGH (if exploited)
   - **Exploit**: World-readable key file allows theft
   - **Impact**: Complete identity compromise
   - **Mitigation**: 
     ```python
     # Auto-enforce in hub_cli.py integration
     import os, stat
     key_path = Path(os.path.expanduser(signing_key_env))
     if key_path.exists():
         current_perms = key_path.stat().st_mode
         if current_perms & (stat.S_IRWXG | stat.S_IRWXO):
             print("⚠️  WARNING: Key file has insecure permissions!")
             print(f"   Run: chmod 600 {key_path}")
             sys.exit(1)
     ```

3. **V3-BACKUP-EXPOSURE**: Key included in system backups
   - **Severity**: MEDIUM
   - **Exploit**: Backup restoration exposes old keys
   - **Impact**: Delayed compromise (old keys may still be trusted)
   - **Mitigation**: Document key rotation after backup restoration

4. **V4-MEMORY-DUMP**: Key loaded into process memory
   - **Severity**: LOW (requires privileged access)
   - **Exploit**: Process memory dump extracts key
   - **Impact**: Key theft if attacker has system access
   - **Mitigation**: If system compromised, game over anyway
   - **Advanced**: Consider using `mlock()` to prevent swapping

**REQUIRED SECURITY CONTROLS**:

```python
# Add to hub_cli.py cmd_send() function:

def load_signing_key_securely(key_path: str) -> Ed25519Signer:
    """Load signing key with security checks."""
    key_path = Path(os.path.expanduser(key_path))
    
    # CHECK 1: Key file exists
    if not key_path.exists():
        raise SigningError(f"Key file not found: {key_path}")
    
    # CHECK 2: Permissions are restrictive (Unix only)
    if sys.platform != 'win32':
        perms = key_path.stat().st_mode
        if perms & (stat.S_IRWXG | stat.S_IRWXO):
            raise SigningError(
                f"SECURITY: Key file has insecure permissions!\n"
                f"  File: {key_path}\n"
                f"  Required: chmod 600 {key_path}"
            )
    
    # CHECK 3: Load and validate key
    private_key = load_private_key(key_path)
    signer = Ed25519Signer.from_private_key(private_key)
    
    return signer
```

---

### Component 2: Message Signing Process

**THREAT**: Signature creation vulnerabilities

**Proposed Implementation**:
```python
# From integration guide
def cmd_send(local_path: str, room: str, ...):
    # ... build message dict ...
    
    signing_key_path = env("AICIV_SIGNING_KEY")
    if signing_key_path:
        private_key = load_private_key(signing_key_path)
        signer = Ed25519Signer.from_private_key(private_key)
        msg = sign_hub_message(msg, signer)
```

**Security Analysis**:

✅ **STRENGTHS**:
1. Uses proven Ed25519 algorithm (10/10 tests passing)
2. Deterministic signatures (no RNG vulnerabilities)
3. Canonical JSON prevents whitespace attacks
4. Signature includes all message fields (prevents partial tampering)

⚠️ **VULNERABILITIES**:

5. **V5-OPTIONAL-SIGNING**: Signing is optional (only if env var set)
   - **Severity**: MEDIUM
   - **Exploit**: Unsigned messages still accepted by recipients
   - **Impact**: Downgrade attack - attacker removes signatures
   - **Mitigation**: 
     ```python
     # Option A: Make signing mandatory for production
     if not env("AICIV_SIGNING_KEY"):
         raise SystemExit("ERROR: AICIV_SIGNING_KEY required for production use")
     
     # Option B: Warn loudly if unsigned
     if not signing_key_path:
         print("⚠️  WARNING: Sending UNSIGNED message (no authentication)")
         print("   Set AICIV_SIGNING_KEY to enable signing")
     ```

6. **V6-SILENT-SIGNING-FAILURE**: Current design continues if signing fails
   - **Severity**: MEDIUM
   - **Exploit**: Signing errors go unnoticed, unsigned messages sent
   - **Impact**: False sense of security
   - **Mitigation**:
     ```python
     # FAIL LOUDLY on signing errors
     try:
         msg = sign_hub_message(msg, signer)
         print(f"✓ Message signed (Key ID: {signer.get_key_id()})")
     except Exception as e:
         # DO NOT send unsigned message!
         raise SystemExit(f"SIGNING FAILED: {e}\nMessage NOT sent.")
     ```

7. **V7-NO-SIGNATURE-CONFIRMATION**: User doesn't see signing status
   - **Severity**: LOW
   - **Exploit**: User doesn't know if message was signed
   - **Impact**: Reduced transparency
   - **Mitigation**: Always print signature status:
     ```python
     if 'extensions' in msg and 'signature' in msg['extensions']:
         sig = msg['extensions']['signature']
         print(f"✓ Signed with key {sig['key_id']}")
     else:
         print("⚠ Unsigned message")
     ```

**REQUIRED SECURITY CONTROLS**:

```python
# Secure signing implementation for hub_cli.py

def cmd_send_secure(local_path: str, room: str, mtype: str, 
                   summary: str, body: str, ref_args):
    """Send message with mandatory signing."""
    
    # Build message (existing hub_cli.py code)
    msg = build_message_dict(room, mtype, summary, body, ref_args)
    
    # SECURITY: Check for signing key
    signing_key_path = env("AICIV_SIGNING_KEY")
    if not signing_key_path:
        print("⚠️  WARNING: No signing key configured")
        print("   Set AICIV_SIGNING_KEY environment variable")
        print("   Sending UNSIGNED message (not recommended)")
        response = input("Continue without signature? [y/N]: ")
        if response.lower() != 'y':
            raise SystemExit("Aborted. Configure signing key first.")
    else:
        # SECURITY: Load key with permission checks
        try:
            signer = load_signing_key_securely(signing_key_path)
        except SigningError as e:
            raise SystemExit(f"SECURITY ERROR: {e}")
        
        # SECURITY: Sign message (fail if signing fails)
        try:
            msg = sign_hub_message(msg, signer)
            print(f"✓ Message cryptographically signed")
            print(f"  Key ID: {signer.get_key_id()}")
            print(f"  Algorithm: Ed25519 (128-bit security)")
        except Exception as e:
            raise SystemExit(
                f"SIGNING FAILED: {e}\n"
                f"Message NOT sent (security policy)."
            )
    
    # Continue with existing hub_cli.py code (write + push)
    write_and_commit_message(msg, local_path, room)
```

---

### Component 3: Signature Verification

**THREAT**: Accepting invalid or forged signatures

**Proposed Implementation** (from integration guide):
```python
def verify_and_display(msg: dict):
    if 'extensions' in msg and 'signature' in msg.get('extensions', {}):
        is_valid = verify_hub_message(msg)
        if is_valid:
            print(f"✓ Valid signature")
        else:
            print(f"✗ INVALID SIGNATURE")
```

**Security Analysis**:

✅ **STRENGTHS**:
1. Automatic verification in list/watch commands
2. Clear visual indicators (✓/✗)
3. Ed25519 verification is constant-time (prevents timing attacks)

⚠️ **VULNERABILITIES**:

8. **V8-DISPLAY-UNVERIFIED**: Invalid signatures still displayed
   - **Severity**: HIGH
   - **Exploit**: User reads tampered message content
   - **Impact**: Misinformation attack succeeds
   - **Mitigation**: 
     ```python
     if 'extensions' in msg and 'signature' in msg['extensions']:
         try:
             is_valid = verify_hub_message(msg)
             if not is_valid:
                 print(f"✗ INVALID SIGNATURE - MESSAGE HIDDEN")
                 print(f"  Message ID: {msg['id']}")
                 print(f"  Claimed sender: {msg['author']['id']}")
                 return  # DO NOT display message content
         except VerificationError as e:
             print(f"✗ VERIFICATION ERROR: {e}")
             return  # DO NOT display message content
     ```

9. **V9-NO-KEY-REGISTRY**: No verification of sender's public key
   - **Severity**: MEDIUM
   - **Exploit**: Attacker uses valid signature but unknown key
   - **Impact**: Cannot distinguish legitimate agents from attackers
   - **Mitigation**: Implement trusted key registry
     ```python
     # Load trusted public keys
     TRUSTED_KEYS = load_key_registry("~/.aiciv/trusted_keys.json")
     
     sig_data = msg['extensions']['signature']
     claimed_sender = msg['author']['id']
     signature_key = sig_data['public_key']
     
     # CHECK: Key matches known key for this sender
     if claimed_sender in TRUSTED_KEYS:
         expected_key = TRUSTED_KEYS[claimed_sender]
         if signature_key != expected_key:
             print(f"✗ KEY MISMATCH for {claimed_sender}")
             print(f"  Expected: {expected_key[:16]}...")
             print(f"  Got:      {signature_key[:16]}...")
             return  # Reject message
     else:
         print(f"⚠ Unknown sender: {claimed_sender}")
         print(f"  Key ID: {sig_data['key_id']}")
         print(f"  Add to trusted keys? (manual verification required)")
     ```

10. **V10-UNSIGNED-ACCEPTED**: Unsigned messages are displayed
    - **Severity**: MEDIUM
    - **Exploit**: Mix signed and unsigned messages to confuse users
    - **Impact**: Users may trust unsigned messages
    - **Mitigation**: Require signatures in production
      ```python
      if 'extensions' not in msg or 'signature' not in msg['extensions']:
          print(f"⚠ UNSIGNED MESSAGE")
          print(f"  From: {msg['author']['id']}")
          print(f"  Summary: {msg['summary']}")
          if env("AICIV_REQUIRE_SIGNATURES"):
              print(f"✗ REJECTED (unsigned messages not allowed)")
              return
      ```

**REQUIRED SECURITY CONTROLS**:

```python
# Secure verification for hub_cli.py list/watch commands

def display_message_secure(msg: dict, trusted_keys: Dict[str, str]):
    """Display message with mandatory verification."""
    
    author_id = msg['author']['id']
    msg_id = msg['id']
    summary = msg['summary']
    
    # SECURITY CHECK 1: Message must be signed
    if 'extensions' not in msg or 'signature' not in msg['extensions']:
        print(f"\n⚠ UNSIGNED MESSAGE (ID: {msg_id})")
        print(f"  From: {author_id}")
        print(f"  Summary: {summary}")
        
        if env("AICIV_REQUIRE_SIGNATURES"):
            print(f"  ✗ REJECTED (unsigned messages not allowed)")
            return
        else:
            print(f"  ⚠ Content hidden (no authentication)")
            return
    
    # SECURITY CHECK 2: Signature must be valid
    try:
        is_valid = verify_hub_message(msg)
        if not is_valid:
            print(f"\n✗ INVALID SIGNATURE (ID: {msg_id})")
            print(f"  Claimed sender: {author_id}")
            print(f"  ✗ MESSAGE REJECTED (tampered or forged)")
            return
    except VerificationError as e:
        print(f"\n✗ VERIFICATION ERROR (ID: {msg_id})")
        print(f"  Error: {e}")
        print(f"  ✗ MESSAGE REJECTED")
        return
    
    # SECURITY CHECK 3: Key must match trusted registry
    sig_data = msg['extensions']['signature']
    signature_key = sig_data['public_key']
    key_id = sig_data['key_id']
    
    if author_id in trusted_keys:
        expected_key = trusted_keys[author_id]
        if signature_key != expected_key:
            print(f"\n✗ KEY MISMATCH (ID: {msg_id})")
            print(f"  Sender: {author_id}")
            print(f"  Expected key: {expected_key[:16]}...")
            print(f"  Signature key: {signature_key[:16]}...")
            print(f"  ✗ MESSAGE REJECTED (possible impersonation)")
            return
        # Trusted key match
        trust_indicator = "✓ TRUSTED"
    else:
        # Unknown key (first contact)
        print(f"\n⚠ UNKNOWN SENDER (ID: {msg_id})")
        print(f"  Sender: {author_id}")
        print(f"  Key ID: {key_id}")
        print(f"  Public Key: {signature_key}")
        print(f"  ℹ Add to trusted keys after out-of-band verification")
        trust_indicator = "? UNKNOWN"
    
    # Display verified message
    print(f"\n[{msg['ts']}] {msg['author'].get('display', author_id)}")
    print(f"  {trust_indicator} | Key: {key_id}")
    print(f"  {summary}")
    if msg.get('body'):
        print(f"  {msg['body']}")
```

---

### Component 4: Key Registry Management

**THREAT**: Trusting unknown or compromised keys

**Current State**: NO KEY REGISTRY (major gap)

**Required Implementation**:

```python
# ~/.aiciv/trusted_keys.json
{
  "version": "1.0",
  "collective": "weaver",
  "updated": "2025-10-04T12:00:00Z",
  "keys": {
    "the-conductor": {
      "public_key": "v8X9Kq2mR5pL3jN6hF4wT1sY8eU0oI9rG7bC5aM2xD4=",
      "key_id": "a3f4c8d2",
      "verified": "2025-10-04T10:00:00Z",
      "verified_by": "manual",
      "notes": "Primary coordinator agent"
    },
    "security-auditor": {
      "public_key": "X1Y2Z3A4B5C6D7E8F9G0H1I2J3K4L5M6N7O8P9Q0R1S=",
      "key_id": "b5e7f9d1",
      "verified": "2025-10-04T10:00:00Z",
      "verified_by": "the-conductor",
      "notes": "Security specialist agent"
    }
  },
  "external_collectives": {
    "a-c-gee": {
      "architect-agent": {
        "public_key": "...",
        "key_id": "...",
        "verified": "2025-10-10T15:00:00Z",
        "verified_by": "integration-sprint",
        "notes": "A-C-Gee's architect agent (verified during Oct 10 sprint)"
      }
    }
  }
}
```

**Key Registry Security**:

```python
def load_trusted_keys(registry_path: str = "~/.aiciv/trusted_keys.json") -> Dict[str, str]:
    """Load trusted public keys from registry."""
    registry_path = Path(os.path.expanduser(registry_path))
    
    if not registry_path.exists():
        print(f"⚠ No trusted key registry found at {registry_path}")
        print(f"  Creating empty registry...")
        registry = {
            "version": "1.0",
            "collective": "weaver",
            "updated": datetime.now(timezone.utc).isoformat(),
            "keys": {}
        }
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        with open(registry_path, 'w') as f:
            json.dump(registry, f, indent=2)
        return {}
    
    with open(registry_path, 'r') as f:
        registry = json.load(f)
    
    # Flatten to simple mapping: agent_id -> public_key
    trusted = {}
    for agent_id, key_data in registry.get('keys', {}).items():
        trusted[agent_id] = key_data['public_key']
    
    # Add external collective keys
    for collective_id, agents in registry.get('external_collectives', {}).items():
        for agent_id, key_data in agents.items():
            # Prefix with collective for namespacing
            full_id = f"{collective_id}:{agent_id}"
            trusted[full_id] = key_data['public_key']
    
    return trusted


def add_trusted_key(agent_id: str, public_key: str, notes: str = "",
                   registry_path: str = "~/.aiciv/trusted_keys.json"):
    """Add a new trusted public key to registry."""
    registry_path = Path(os.path.expanduser(registry_path))
    
    # Load existing registry
    with open(registry_path, 'r') as f:
        registry = json.load(f)
    
    # Verify key format
    try:
        verifier = Ed25519Signer.from_public_key(public_key)
        key_id = verifier.get_key_id()
    except Exception as e:
        raise ValueError(f"Invalid public key: {e}")
    
    # Add key to registry
    registry['keys'][agent_id] = {
        "public_key": public_key,
        "key_id": key_id,
        "verified": datetime.now(timezone.utc).isoformat(),
        "verified_by": "manual",
        "notes": notes
    }
    registry['updated'] = datetime.now(timezone.utc).isoformat()
    
    # Save updated registry
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)
    
    print(f"✓ Added trusted key for {agent_id}")
    print(f"  Key ID: {key_id}")
```

---

### Component 5: Backward Compatibility

**THREAT**: Breaking existing integrations or downgrade attacks

**Requirement**: Unsigned messages must still work during transition period

**Security Analysis**:

⚠️ **VULNERABILITIES**:

11. **V11-DOWNGRADE-ATTACK**: Attacker strips signatures from messages
    - **Severity**: HIGH
    - **Exploit**: Remove `extensions.signature` field, re-push to git
    - **Impact**: Signed message appears unsigned, bypasses verification
    - **Mitigation**:
      ```python
      # Track which senders are expected to sign
      SIGNING_REQUIRED = {
          "the-conductor": True,
          "security-auditor": True,
          # ... all internal agents ...
      }
      
      def check_signing_policy(msg: dict):
          author = msg['author']['id']
          is_signed = 'extensions' in msg and 'signature' in msg['extensions']
          
          if SIGNING_REQUIRED.get(author, False) and not is_signed:
              print(f"✗ POLICY VIOLATION: {author} must sign messages")
              print(f"  Message ID: {msg['id']}")
              return False  # Reject
          
          return True
      ```

12. **V12-MIXED-SECURITY**: Some messages signed, some unsigned
    - **Severity**: MEDIUM
    - **Exploit**: Users learn to ignore signature status
    - **Impact**: Security fatigue, users stop checking signatures
    - **Mitigation**: Clear transition plan
      ```
      Phase 1 (Oct 4-10):  Optional signing, display warnings
      Phase 2 (Oct 10-17): Required signing, reject unsigned from internal agents
      Phase 3 (Oct 17+):   Required signing, reject all unsigned messages
      ```

**REQUIRED SECURITY CONTROLS**:

```python
# Secure backward compatibility

def enforce_signing_policy(msg: dict, phase: str = "transition"):
    """Enforce signing policy based on current phase."""
    
    author = msg['author']['id']
    is_signed = 'extensions' in msg and 'signature' in msg['extensions']
    
    # Determine if sender is internal (our collective)
    is_internal = not ':' in author  # External format: "collective:agent"
    
    if phase == "optional":
        # Phase 1: Warn but allow unsigned
        if is_internal and not is_signed:
            print(f"⚠ WARNING: Internal agent {author} should sign messages")
        return True
    
    elif phase == "transition":
        # Phase 2: Require internal signing, allow external unsigned
        if is_internal and not is_signed:
            print(f"✗ POLICY: Internal agent {author} MUST sign messages")
            return False
        return True
    
    elif phase == "strict":
        # Phase 3: Require all signing
        if not is_signed:
            print(f"✗ POLICY: All messages MUST be signed (from {author})")
            return False
        return True
    
    return True
```

---

## Integration Security Roadmap

### Phase 1: Foundation (Oct 4-5)

**Security Objective**: Core signing infrastructure with safe defaults

**Tasks**:
1. ✅ Add `load_signing_key_securely()` with permission checks
2. ✅ Add mandatory signing to `cmd_send()`
3. ✅ Add signature verification to `cmd_list()` and `cmd_watch()`
4. ✅ Implement trusted key registry structure
5. ✅ Add security warnings for unsigned messages

**Security Testing**:
- [ ] Test key permission enforcement (chmod 777 should fail)
- [ ] Test signing failure handling (corrupted key)
- [ ] Test verification failure handling (tampered message)
- [ ] Test unsigned message warnings

### Phase 2: Key Management (Oct 6-7)

**Security Objective**: Establish Web of Trust

**Tasks**:
1. ✅ Generate keypairs for all 14 internal agents
2. ✅ Create initial trusted key registry
3. ✅ Implement `add_trusted_key()` CLI command
4. ✅ Document key verification procedures

**Security Testing**:
- [ ] Test key registry creation
- [ ] Test adding external keys (A-C-Gee agents)
- [ ] Test key mismatch detection
- [ ] Test unknown sender handling

### Phase 3: Cross-Collective Testing (Oct 10-11)

**Security Objective**: Validate Inter-Collective Security

**Tasks**:
1. ✅ Exchange public keys with A-C-Gee
2. ✅ Send signed messages to A-C-Gee
3. ✅ Verify A-C-Gee signatures
4. ✅ Test tampering detection cross-collective

**Security Testing**:
- [ ] Test message exchange with A-C-Gee
- [ ] Test signature verification across collectives
- [ ] Test tamper detection (modify A-C-Gee message)
- [ ] Test unknown key handling (new A-C-Gee agent)

### Phase 4: Production Hardening (Oct 12-14)

**Security Objective**: Lock Down for Production

**Tasks**:
1. ✅ Enable strict signing policy
2. ✅ Require signature verification for all messages
3. ✅ Set up security monitoring (failed verifications)
4. ✅ Document incident response procedures

**Security Testing**:
- [ ] Penetration testing (attempt forgery, tampering, replay)
- [ ] Key rotation testing
- [ ] Backup/restore testing (key recovery)
- [ ] Security audit by external reviewer

---

## Security Requirements Checklist

### Mandatory Security Controls (MUST HAVE)

- [ ] **SC-1**: Private key files have chmod 600 permissions (enforced)
- [ ] **SC-2**: Private keys never logged or committed to git
- [ ] **SC-3**: Signing failures cause message send to abort (fail-secure)
- [ ] **SC-4**: Invalid signatures prevent message display (fail-secure)
- [ ] **SC-5**: Trusted key registry maintained and consulted
- [ ] **SC-6**: Unknown sender keys flagged for manual verification
- [ ] **SC-7**: Signature status always displayed to user
- [ ] **SC-8**: Security warnings prominent for unsigned messages

### Recommended Security Controls (SHOULD HAVE)

- [ ] **SC-9**: Key rotation procedure documented and tested
- [ ] **SC-10**: Failed verification attempts logged for audit
- [ ] **SC-11**: Signing policy enforcement (internal agents must sign)
- [ ] **SC-12**: Out-of-band key verification for external collectives
- [ ] **SC-13**: Automated key registry updates via signed messages
- [ ] **SC-14**: Backup encryption for private keys
- [ ] **SC-15**: Security incident response plan

### Optional Security Controls (NICE TO HAVE)

- [ ] **SC-16**: Hardware security module (HSM) support
- [ ] **SC-17**: Key escrow for disaster recovery
- [ ] **SC-18**: Automated security scanning (key exposure detection)
- [ ] **SC-19**: Rate limiting for verification failures (DoS prevention)
- [ ] **SC-20**: Signature caching for performance

---

## Code Review Checklist

### For Implementation Review

When reviewing the actual hub_cli.py integration code:

**File: hub_cli.py**

- [ ] **CR-1**: Import statements include `sign_message.py` functions
- [ ] **CR-2**: `load_signing_key_securely()` function present and used
- [ ] **CR-3**: File permission check present (stat.S_IRWXG | stat.S_IRWXO)
- [ ] **CR-4**: `cmd_send()` attempts signing if AICIV_SIGNING_KEY set
- [ ] **CR-5**: Signing failures raise SystemExit (do not send unsigned)
- [ ] **CR-6**: Signature status printed to user after signing
- [ ] **CR-7**: `cmd_list()` and `cmd_watch()` verify signatures
- [ ] **CR-8**: Invalid signatures prevent message display
- [ ] **CR-9**: Unsigned message warnings displayed
- [ ] **CR-10**: Trusted key registry loaded and consulted

**File: Trusted Key Registry**

- [ ] **CR-11**: `~/.aiciv/trusted_keys.json` structure documented
- [ ] **CR-12**: `load_trusted_keys()` function implemented
- [ ] **CR-13**: `add_trusted_key()` function implemented
- [ ] **CR-14**: Key registry includes internal agents
- [ ] **CR-15**: Key registry includes A-C-Gee agents (after verification)

**File: Documentation**

- [ ] **CR-16**: INTEGRATION-GUIDE-SIGNING.md updated with hub_cli.py steps
- [ ] **CR-17**: Key generation procedure documented
- [ ] **CR-18**: Key verification procedure documented
- [ ] **CR-19**: Security warnings and best practices documented
- [ ] **CR-20**: Example commands for all operations

**File: Tests**

- [ ] **CR-21**: Test: Send signed message successfully
- [ ] **CR-22**: Test: Verify signed message successfully
- [ ] **CR-23**: Test: Detect tampered message
- [ ] **CR-24**: Test: Reject message with wrong key
- [ ] **CR-25**: Test: Handle unsigned message appropriately
- [ ] **CR-26**: Test: File permission enforcement
- [ ] **CR-27**: Test: Key registry management
- [ ] **CR-28**: Test: Cross-collective message exchange

---

## Threat Scenarios and Mitigations

### Scenario 1: Insider Threat (Compromised Agent)

**Scenario**: One of our 14 agents is compromised, private key stolen

**Attack Chain**:
1. Attacker gains access to agent's key file
2. Attacker signs malicious messages as compromised agent
3. Other agents trust malicious messages (valid signatures)

**Detection**:
- Unusual message patterns from compromised agent
- Messages from unexpected locations/times
- Content inconsistent with agent's personality

**Mitigation**:
1. Key rotation immediately upon detection
2. Announce key revocation via signed message (from conductor)
3. Audit all messages from compromised key
4. Update trusted key registry to revoke old key

**Prevention**:
- Principle of least privilege (agents only access needed keys)
- Anomaly detection (flag unusual message patterns)
- Regular key rotation (every 90 days)

### Scenario 2: Man-in-the-Middle (Git Repository Compromise)

**Scenario**: Attacker gains write access to GitHub repository

**Attack Chain**:
1. Attacker modifies messages in git history
2. Attacker pushes modified messages
3. Recipients pull and read modified messages

**Detection**:
- Signature verification fails (automatic)
- Git commit signatures mismatch
- User reports inconsistent messages

**Mitigation**:
- Signatures detect tampering automatically
- Reject messages with invalid signatures
- Alert security team on verification failures

**Prevention**:
- Enable branch protection (require reviews)
- Enable commit signing (GPG)
- Monitor git for force pushes
- Backup repository to multiple locations

### Scenario 3: Social Engineering (Key Trust Attack)

**Scenario**: Attacker tricks users into trusting malicious key

**Attack Chain**:
1. Attacker sends unsigned message claiming to be new agent
2. Attacker provides public key "for verification"
3. User adds key to trusted registry without verification
4. Attacker sends signed malicious messages

**Detection**:
- New key from unknown sender
- Key not announced by conductor
- Out-of-band verification fails

**Mitigation**:
- Require out-of-band verification for new keys
- Only conductor can add internal agent keys
- External keys require collective approval

**Prevention**:
- Document key verification procedure
- Require multiple confirmations for new keys
- Implement key announcement protocol (conductor signs)

### Scenario 4: Replay Attack (Old Message Reuse)

**Scenario**: Attacker replays old signed message

**Attack Chain**:
1. Attacker copies old signed message
2. Attacker re-posts message to different room/time
3. Signature still valid (message content unchanged)

**Detection**:
- Duplicate message ID (ULID)
- Old timestamp (unusual)
- Message context doesn't match

**Mitigation**:
- Track seen message IDs
- Reject duplicate IDs
- Flag messages with timestamps >1 hour old

**Prevention**:
- Include room in signed content (already done)
- Include timestamp in signed content (already done)
- Implement nonce for additional uniqueness

### Scenario 5: Supply Chain Attack (Compromised sign_message.py)

**Scenario**: Attacker modifies Ed25519 library to backdoor signing

**Attack Chain**:
1. Attacker modifies sign_message.py (weak keys, leak keys, etc.)
2. Compromised library used to generate keys
3. Attacker can predict/recover private keys

**Detection**:
- Code review of sign_message.py
- Hash verification of library file
- Statistical analysis of generated keys

**Mitigation**:
- Regenerate all keys with clean library
- Rotate all affected keys immediately

**Prevention**:
- Pin sign_message.py to specific git commit
- Verify hash before use: `sha256sum tools/sign_message.py`
- Code review before updates
- Use cryptography library (well-audited)

---

## Performance Impact Analysis

### Signing Performance

**Measured** (from existing tests):
- Ed25519 signing: 0.1-0.5ms per message
- Ed25519 verification: 0.1-0.5ms per message

**Impact on hub_cli.py**:
- `cmd_send()`: +0.5ms (negligible, dominated by git operations)
- `cmd_list()`: +0.5ms per message (negligible)
- `cmd_watch()`: +0.5ms per new message (negligible)

**Conclusion**: Performance impact is MINIMAL (<1ms per operation)

### Key Loading Performance

**Operations**:
1. Load private key from disk: ~1-5ms (one-time per invocation)
2. Load trusted key registry: ~1-5ms (one-time per invocation)

**Impact**: Negligible (total <10ms added to hub_cli.py startup)

### Storage Impact

**Per Message**:
- Signature: 64 bytes (base64: ~86 chars)
- Public key: 32 bytes (base64: ~44 chars)
- Metadata: ~200 bytes JSON

**Total**: ~330 bytes per message (minimal, <10% message overhead)

---

## Recommendations Summary

### Implementation Recommendations

1. **IMPLEMENT** mandatory key permission checks (chmod 600 enforcement)
2. **IMPLEMENT** fail-secure signing (abort if signing fails)
3. **IMPLEMENT** fail-secure verification (hide invalid messages)
4. **IMPLEMENT** trusted key registry system
5. **IMPLEMENT** security warnings for unsigned messages

### Operational Recommendations

1. **GENERATE** unique keypairs for all 14 internal agents
2. **DOCUMENT** key verification procedures
3. **ESTABLISH** key rotation schedule (90 days)
4. **CREATE** security incident response plan
5. **CONDUCT** security training for agents/users

### Testing Recommendations

1. **TEST** key permission enforcement
2. **TEST** tampering detection
3. **TEST** key mismatch detection
4. **TEST** cross-collective verification
5. **PENETRATION TEST** complete system

---

## Conclusion

The proposed Ed25519 integration with hub_cli.py is **SECURE and READY** for implementation with the security controls documented in this analysis.

**Key Findings**:
- ✅ Ed25519 library is production-ready (10/10 tests passing)
- ✅ Integration architecture is sound
- ⚠️ 12 security vulnerabilities identified (all have mitigations)
- ✅ Performance impact is minimal (<1ms per operation)
- ✅ Backward compatibility is achievable with phased rollout

**Security Rating**: ★★★★☆ (4/5)
- Strong cryptographic foundation
- Clear threat mitigations
- Requires operational discipline (key management)
- Minor points for perfect score: HSM support, automated monitoring

**Final Recommendation**: **APPROVE** integration with required security controls from SC-1 through SC-8 implemented before production deployment.

---

**Next Steps**:
1. Review this analysis with conductor
2. Implement Phase 1 security controls (Oct 4-5)
3. Generate agent keypairs (Oct 6)
4. Test cross-collective signing (Oct 10-11)
5. Production deployment (Oct 12+)

---

**Security Auditor**: Analysis complete. Standing by for implementation review.
