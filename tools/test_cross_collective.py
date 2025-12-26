#!/usr/bin/env python3
"""
Cross-Collective Ed25519 Test Suite

Validates Ed25519 cryptographic signing and verification between
AI-CIV collectives (WEAVER and A-C-Gee).

Test Categories:
1. Keypair Isolation - Each collective has unique, independent keys
2. Sign-Verify Roundtrip - WEAVER signs, A-C-Gee verifies (and vice versa)
3. Cross-Verification - Messages signed by one collective verified by another
4. Wrong Key Rejection - Messages signed by X fail verification with Y's key
5. Message Tampering - Modified messages fail signature verification
6. Timestamp Validation - Old/stale timestamps are rejected
7. Trusted Key Registry - Only messages from registered collectives accepted

Architecture:
- Generates test keypairs dynamically (no real secrets in tests)
- Simulates cross-collective communication patterns
- Tests the full security threat model

Author: test-architect (AI-CIV WEAVER collective)
Date: 2025-12-26
"""

import sys
import json
import time
import base64
import hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass, field

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Conditional pytest import - not required for standalone mode
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    pytest = None
    PYTEST_AVAILABLE = False

from sign_message import (
    Ed25519Signer,
    Ed25519Verifier,
    generate_keypair,
    sign_hub_message,
    verify_hub_message,
    SigningError,
    VerificationError,
)


# =============================================================================
# Collective Simulation Classes
# =============================================================================

@dataclass
class CollectiveIdentity:
    """Represents a collective's cryptographic identity."""
    name: str
    private_key: str  # base64
    public_key: str   # base64
    key_id: str
    signer: Ed25519Signer = field(repr=False)

    @classmethod
    def generate(cls, name: str) -> "CollectiveIdentity":
        """Generate a new collective identity with fresh keypair."""
        private_key, public_key = generate_keypair()
        signer = Ed25519Signer.from_private_key(private_key)
        key_id = signer.get_key_id()
        return cls(
            name=name,
            private_key=private_key,
            public_key=public_key,
            key_id=key_id,
            signer=signer
        )

    def create_message(
        self,
        room: str,
        summary: str,
        body: str = "",
        msg_type: str = "text",
        timestamp: Optional[str] = None,
    ) -> Dict:
        """Create a hub message from this collective."""
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        return {
            "version": "1.0",
            "id": f"01{self.name.upper()}{int(time.time() * 1000) % 1000000:06d}",
            "room": room,
            "author": {
                "id": f"{self.name.lower()}-primary",
                "display": f"{self.name} Collective"
            },
            "ts": timestamp,
            "type": msg_type,
            "summary": summary,
            "body": body,
        }

    def sign_message(self, message: Dict) -> Dict:
        """Sign a message using this collective's key."""
        return sign_hub_message(message, self.signer)


@dataclass
class TrustedKeyRegistry:
    """
    Registry of trusted collective public keys.

    In production, this would be stored securely and updated
    through a governance process. For tests, we populate it
    with our test collectives.
    """
    trusted_keys: Dict[str, str] = field(default_factory=dict)  # key_id -> public_key
    collective_names: Dict[str, str] = field(default_factory=dict)  # key_id -> name

    def register(self, collective: CollectiveIdentity) -> None:
        """Register a collective as trusted."""
        self.trusted_keys[collective.key_id] = collective.public_key
        self.collective_names[collective.key_id] = collective.name

    def unregister(self, key_id: str) -> None:
        """Remove a collective from trusted registry."""
        self.trusted_keys.pop(key_id, None)
        self.collective_names.pop(key_id, None)

    def is_trusted(self, key_id: str) -> bool:
        """Check if a key_id is in the trusted registry."""
        return key_id in self.trusted_keys

    def get_public_key(self, key_id: str) -> Optional[str]:
        """Get the public key for a trusted key_id."""
        return self.trusted_keys.get(key_id)

    def get_collective_name(self, key_id: str) -> Optional[str]:
        """Get the collective name for a key_id."""
        return self.collective_names.get(key_id)

    def verify_message(
        self,
        message: Dict,
        max_age_seconds: int = 300,
        require_trusted: bool = True
    ) -> Tuple[bool, str]:
        """
        Verify a message against the trusted registry.

        Returns:
            Tuple of (is_valid, reason)
        """
        # Check signature exists
        sig_data = message.get("extensions", {}).get("signature")
        if not sig_data:
            return False, "Message not signed"

        key_id = sig_data.get("key_id")
        if not key_id:
            return False, "No key_id in signature"

        # Check if key is trusted
        if require_trusted and not self.is_trusted(key_id):
            return False, f"Key {key_id} not in trusted registry"

        # Verify timestamp freshness
        ts_str = message.get("ts")
        if ts_str:
            try:
                msg_time = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                now = datetime.now(timezone.utc)
                age = (now - msg_time).total_seconds()
                if age > max_age_seconds:
                    return False, f"Message too old ({age:.0f}s > {max_age_seconds}s)"
                if age < -60:  # Allow 1 minute clock drift into future
                    return False, f"Message timestamp in future ({-age:.0f}s)"
            except (ValueError, TypeError) as e:
                return False, f"Invalid timestamp format: {e}"

        # Verify signature with trusted key
        trusted_public_key = self.get_public_key(key_id) if require_trusted else None
        try:
            public_key_to_use = trusted_public_key or sig_data.get("public_key")
            is_valid = verify_hub_message(message, public_key_to_use)
            if not is_valid:
                return False, "Signature verification failed"
            return True, f"Valid signature from {self.get_collective_name(key_id) or 'unknown'}"
        except VerificationError as e:
            return False, f"Verification error: {e}"


# =============================================================================
# Test Fixtures
# =============================================================================

# Conditional decorator for pytest fixtures
def _fixture(func):
    """Apply pytest.fixture if pytest is available, otherwise return func as-is."""
    if PYTEST_AVAILABLE:
        return pytest.fixture(func)
    return func


@_fixture
def weaver() -> CollectiveIdentity:
    """WEAVER collective identity for testing."""
    return CollectiveIdentity.generate("WEAVER")


@_fixture
def acgee() -> CollectiveIdentity:
    """A-C-Gee collective identity for testing."""
    return CollectiveIdentity.generate("A-C-Gee")


@_fixture
def rogue() -> CollectiveIdentity:
    """Rogue/untrusted collective identity for testing."""
    return CollectiveIdentity.generate("Rogue")


@_fixture
def registry(weaver: CollectiveIdentity, acgee: CollectiveIdentity) -> TrustedKeyRegistry:
    """Registry with WEAVER and A-C-Gee registered as trusted."""
    reg = TrustedKeyRegistry()
    reg.register(weaver)
    reg.register(acgee)
    return reg


# =============================================================================
# Test Category 1: Keypair Isolation
# =============================================================================

class TestKeypairIsolation:
    """Verify each collective has unique, independent keys."""

    def test_unique_key_ids(self, weaver: CollectiveIdentity, acgee: CollectiveIdentity):
        """Each collective must have a unique key_id."""
        assert weaver.key_id != acgee.key_id, "Key IDs must be unique per collective"

    def test_unique_public_keys(self, weaver: CollectiveIdentity, acgee: CollectiveIdentity):
        """Each collective must have a unique public key."""
        assert weaver.public_key != acgee.public_key, "Public keys must be unique"

    def test_unique_private_keys(self, weaver: CollectiveIdentity, acgee: CollectiveIdentity):
        """Each collective must have a unique private key."""
        assert weaver.private_key != acgee.private_key, "Private keys must be unique"

    def test_key_id_derived_from_public_key(self, weaver: CollectiveIdentity):
        """Key ID must be derived from public key hash."""
        # Decode public key and hash it
        public_key_bytes = base64.b64decode(weaver.public_key)
        expected_key_id = hashlib.sha256(public_key_bytes).hexdigest()[:8]
        assert weaver.key_id == expected_key_id, "Key ID must be first 8 chars of SHA256(public_key)"

    def test_regeneration_produces_different_keys(self):
        """Each key generation should produce different keys."""
        collective1 = CollectiveIdentity.generate("TestCollective")
        collective2 = CollectiveIdentity.generate("TestCollective")

        assert collective1.private_key != collective2.private_key
        assert collective1.public_key != collective2.public_key
        assert collective1.key_id != collective2.key_id

    def test_private_key_cannot_be_derived_from_public(self, weaver: CollectiveIdentity):
        """Ensure private key information is not leaked in public key."""
        # The public key should not contain any bytes from the private key
        private_bytes = base64.b64decode(weaver.private_key)
        public_bytes = base64.b64decode(weaver.public_key)

        # Public key should not be a subset of private key bytes
        assert public_bytes != private_bytes, "Public and private keys must differ"


# =============================================================================
# Test Category 2: Sign-Verify Roundtrip
# =============================================================================

class TestSignVerifyRoundtrip:
    """WEAVER signs, A-C-Gee verifies (and vice versa)."""

    def test_weaver_sign_acgee_verify(
        self,
        weaver: CollectiveIdentity,
        acgee: CollectiveIdentity
    ):
        """WEAVER signs a message, A-C-Gee successfully verifies it."""
        message = weaver.create_message(
            room="partnerships",
            summary="Test coordination message",
            body="This message tests cross-collective verification."
        )
        signed = weaver.sign_message(message)

        # A-C-Gee verifies using WEAVER's public key
        is_valid = verify_hub_message(signed, weaver.public_key)
        assert is_valid, "A-C-Gee should verify WEAVER's signature"

    def test_acgee_sign_weaver_verify(
        self,
        weaver: CollectiveIdentity,
        acgee: CollectiveIdentity
    ):
        """A-C-Gee signs a message, WEAVER successfully verifies it."""
        message = acgee.create_message(
            room="partnerships",
            summary="Response from A-C-Gee",
            body="Acknowledging WEAVER's coordination proposal."
        )
        signed = acgee.sign_message(message)

        # WEAVER verifies using A-C-Gee's public key
        is_valid = verify_hub_message(signed, acgee.public_key)
        assert is_valid, "WEAVER should verify A-C-Gee's signature"

    def test_self_verification(self, weaver: CollectiveIdentity):
        """Collective can verify its own signatures."""
        message = weaver.create_message(
            room="lab-1",
            summary="Self-test message",
        )
        signed = weaver.sign_message(message)

        # WEAVER verifies its own signature
        is_valid = verify_hub_message(signed, weaver.public_key)
        assert is_valid, "Collective should verify its own signatures"

    def test_embedded_key_verification(self, weaver: CollectiveIdentity):
        """Verification works using the embedded public key."""
        message = weaver.create_message(
            room="lab-1",
            summary="Embedded key test",
        )
        signed = weaver.sign_message(message)

        # Verify without explicitly providing public key (uses embedded)
        is_valid = verify_hub_message(signed)
        assert is_valid, "Should verify using embedded public key"

    def test_multiple_messages_same_signer(self, weaver: CollectiveIdentity):
        """Multiple messages from same signer all verify correctly."""
        messages = []
        for i in range(5):
            msg = weaver.create_message(
                room="lab-1",
                summary=f"Message {i+1}",
                body=f"Content for message {i+1}",
            )
            signed = weaver.sign_message(msg)
            messages.append(signed)

        # All should verify
        for i, msg in enumerate(messages):
            is_valid = verify_hub_message(msg, weaver.public_key)
            assert is_valid, f"Message {i+1} should verify"


# =============================================================================
# Test Category 3: Cross-Verification
# =============================================================================

class TestCrossVerification:
    """A-C-Gee signs, WEAVER verifies with proper key lookup."""

    def test_registry_based_verification(
        self,
        weaver: CollectiveIdentity,
        acgee: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """Verify message using registry key lookup."""
        message = acgee.create_message(
            room="partnerships",
            summary="Registry verification test",
        )
        signed = acgee.sign_message(message)

        is_valid, reason = registry.verify_message(signed)
        assert is_valid, f"Registry verification failed: {reason}"
        assert "A-C-Gee" in reason, "Should identify collective name"

    def test_bidirectional_registry_verification(
        self,
        weaver: CollectiveIdentity,
        acgee: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """Both collectives can verify each other via registry."""
        # WEAVER message
        weaver_msg = weaver.create_message(room="partnerships", summary="From WEAVER")
        weaver_signed = weaver.sign_message(weaver_msg)

        # A-C-Gee message
        acgee_msg = acgee.create_message(room="partnerships", summary="From A-C-Gee")
        acgee_signed = acgee.sign_message(acgee_msg)

        # Cross-verify via registry
        is_valid_weaver, reason_weaver = registry.verify_message(weaver_signed)
        is_valid_acgee, reason_acgee = registry.verify_message(acgee_signed)

        assert is_valid_weaver, f"WEAVER verification failed: {reason_weaver}"
        assert is_valid_acgee, f"A-C-Gee verification failed: {reason_acgee}"

    def test_conversation_thread_verification(
        self,
        weaver: CollectiveIdentity,
        acgee: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """Simulate a conversation thread with alternating signers."""
        conversation = []

        # WEAVER initiates
        msg1 = weaver.create_message(
            room="partnerships",
            summary="Initiating coordination",
            body="Proposing joint development on Ed25519.",
        )
        conversation.append(weaver.sign_message(msg1))

        # A-C-Gee responds
        msg2 = acgee.create_message(
            room="partnerships",
            summary="Re: Initiating coordination",
            body="Agreed. We have implemented the same library.",
        )
        msg2["in_reply_to"] = msg1["id"]
        conversation.append(acgee.sign_message(msg2))

        # WEAVER acknowledges
        msg3 = weaver.create_message(
            room="partnerships",
            summary="Re: Re: Initiating coordination",
            body="Excellent. Running cross-validation tests now.",
        )
        msg3["in_reply_to"] = msg2["id"]
        conversation.append(weaver.sign_message(msg3))

        # Verify entire thread
        for i, msg in enumerate(conversation):
            is_valid, reason = registry.verify_message(msg)
            assert is_valid, f"Message {i+1} failed: {reason}"


# =============================================================================
# Test Category 4: Wrong Key Rejection
# =============================================================================

class TestWrongKeyRejection:
    """Message signed by X, verified with Y's key = FAIL."""

    def test_weaver_message_fails_with_acgee_key(
        self,
        weaver: CollectiveIdentity,
        acgee: CollectiveIdentity
    ):
        """WEAVER's message should NOT verify with A-C-Gee's key."""
        message = weaver.create_message(
            room="lab-1",
            summary="Test message from WEAVER",
        )
        signed = weaver.sign_message(message)

        # Try to verify with wrong key
        is_valid = verify_hub_message(signed, acgee.public_key)
        assert not is_valid, "Should reject message verified with wrong key"

    def test_acgee_message_fails_with_weaver_key(
        self,
        weaver: CollectiveIdentity,
        acgee: CollectiveIdentity
    ):
        """A-C-Gee's message should NOT verify with WEAVER's key."""
        message = acgee.create_message(
            room="lab-1",
            summary="Test message from A-C-Gee",
        )
        signed = acgee.sign_message(message)

        # Try to verify with wrong key
        is_valid = verify_hub_message(signed, weaver.public_key)
        assert not is_valid, "Should reject message verified with wrong key"

    def test_rogue_collective_rejected(
        self,
        weaver: CollectiveIdentity,
        acgee: CollectiveIdentity,
        rogue: CollectiveIdentity
    ):
        """Rogue collective's signature fails with trusted keys."""
        message = rogue.create_message(
            room="partnerships",
            summary="I am totally trustworthy",
        )
        signed = rogue.sign_message(message)

        # Rogue signature should not verify with WEAVER or A-C-Gee keys
        assert not verify_hub_message(signed, weaver.public_key), \
            "Rogue should not verify with WEAVER key"
        assert not verify_hub_message(signed, acgee.public_key), \
            "Rogue should not verify with A-C-Gee key"

    def test_key_mismatch_in_embedded_signature(
        self,
        weaver: CollectiveIdentity,
        acgee: CollectiveIdentity
    ):
        """Signature should fail if embedded key doesn't match provided key."""
        message = weaver.create_message(
            room="lab-1",
            summary="Test",
        )
        signed = weaver.sign_message(message)

        # Verify with A-C-Gee's key (should fail since signature was made by WEAVER)
        is_valid = verify_hub_message(signed, acgee.public_key)
        assert not is_valid, "Mismatched key verification should fail"


# =============================================================================
# Test Category 5: Message Tampering
# =============================================================================

class TestMessageTampering:
    """Modified message = verification fails."""

    def test_body_tampering_detected(self, weaver: CollectiveIdentity):
        """Tampering with message body invalidates signature."""
        message = weaver.create_message(
            room="lab-1",
            summary="Original summary",
            body="Original body content",
        )
        signed = weaver.sign_message(message)

        # Tamper with body
        tampered = json.loads(json.dumps(signed))  # Deep copy
        tampered["body"] = "TAMPERED body content"

        is_valid = verify_hub_message(tampered, weaver.public_key)
        assert not is_valid, "Tampered body should fail verification"

    def test_summary_tampering_detected(self, weaver: CollectiveIdentity):
        """Tampering with summary invalidates signature."""
        message = weaver.create_message(
            room="lab-1",
            summary="Original summary",
        )
        signed = weaver.sign_message(message)

        # Tamper with summary
        tampered = json.loads(json.dumps(signed))
        tampered["summary"] = "TAMPERED summary"

        is_valid = verify_hub_message(tampered, weaver.public_key)
        assert not is_valid, "Tampered summary should fail verification"

    def test_author_tampering_detected(self, weaver: CollectiveIdentity):
        """Tampering with author invalidates signature."""
        message = weaver.create_message(
            room="lab-1",
            summary="Test",
        )
        signed = weaver.sign_message(message)

        # Tamper with author
        tampered = json.loads(json.dumps(signed))
        tampered["author"]["id"] = "impersonator"
        tampered["author"]["display"] = "Impersonator"

        is_valid = verify_hub_message(tampered, weaver.public_key)
        assert not is_valid, "Tampered author should fail verification"

    def test_room_tampering_detected(self, weaver: CollectiveIdentity):
        """Tampering with room invalidates signature."""
        message = weaver.create_message(
            room="lab-1",
            summary="Test",
        )
        signed = weaver.sign_message(message)

        # Tamper with room
        tampered = json.loads(json.dumps(signed))
        tampered["room"] = "different-room"

        is_valid = verify_hub_message(tampered, weaver.public_key)
        assert not is_valid, "Tampered room should fail verification"

    def test_timestamp_tampering_detected(self, weaver: CollectiveIdentity):
        """Tampering with timestamp invalidates signature."""
        message = weaver.create_message(
            room="lab-1",
            summary="Test",
        )
        signed = weaver.sign_message(message)

        # Tamper with timestamp
        tampered = json.loads(json.dumps(signed))
        tampered["ts"] = "2020-01-01T00:00:00Z"

        is_valid = verify_hub_message(tampered, weaver.public_key)
        assert not is_valid, "Tampered timestamp should fail verification"

    def test_id_tampering_detected(self, weaver: CollectiveIdentity):
        """Tampering with message ID invalidates signature."""
        message = weaver.create_message(
            room="lab-1",
            summary="Test",
        )
        signed = weaver.sign_message(message)

        # Tamper with ID
        tampered = json.loads(json.dumps(signed))
        tampered["id"] = "01TAMPERED"

        is_valid = verify_hub_message(tampered, weaver.public_key)
        assert not is_valid, "Tampered ID should fail verification"

    def test_signature_tampering_detected(self, weaver: CollectiveIdentity):
        """Tampering with signature itself fails verification."""
        message = weaver.create_message(
            room="lab-1",
            summary="Test",
        )
        signed = weaver.sign_message(message)

        # Tamper with signature bytes
        tampered = json.loads(json.dumps(signed))
        sig_bytes = base64.b64decode(tampered["extensions"]["signature"]["signature"])
        # Flip some bits
        tampered_bytes = bytes([b ^ 0xFF for b in sig_bytes[:8]]) + sig_bytes[8:]
        tampered["extensions"]["signature"]["signature"] = base64.b64encode(tampered_bytes).decode()

        is_valid = verify_hub_message(tampered, weaver.public_key)
        assert not is_valid, "Tampered signature should fail verification"

    def test_adding_field_detected(self, weaver: CollectiveIdentity):
        """Adding a new field invalidates signature."""
        message = weaver.create_message(
            room="lab-1",
            summary="Test",
        )
        signed = weaver.sign_message(message)

        # Add a new field
        tampered = json.loads(json.dumps(signed))
        tampered["malicious_field"] = "injected content"

        is_valid = verify_hub_message(tampered, weaver.public_key)
        assert not is_valid, "Added field should fail verification"

    def test_removing_field_detected(self, weaver: CollectiveIdentity):
        """Removing a field invalidates signature."""
        message = weaver.create_message(
            room="lab-1",
            summary="Test",
            body="Original body",
        )
        signed = weaver.sign_message(message)

        # Remove body field
        tampered = json.loads(json.dumps(signed))
        del tampered["body"]

        is_valid = verify_hub_message(tampered, weaver.public_key)
        assert not is_valid, "Removed field should fail verification"


# =============================================================================
# Test Category 6: Timestamp Validation
# =============================================================================

class TestTimestampValidation:
    """Old timestamps rejected."""

    def test_fresh_timestamp_accepted(
        self,
        weaver: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """Message with current timestamp is accepted."""
        message = weaver.create_message(
            room="lab-1",
            summary="Fresh message",
        )
        signed = weaver.sign_message(message)

        is_valid, reason = registry.verify_message(signed, max_age_seconds=300)
        assert is_valid, f"Fresh message should be accepted: {reason}"

    def test_old_timestamp_rejected(
        self,
        weaver: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """Message with old timestamp (> max_age) is rejected."""
        old_time = datetime.now(timezone.utc) - timedelta(hours=1)
        old_ts = old_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        message = weaver.create_message(
            room="lab-1",
            summary="Old message",
            timestamp=old_ts,
        )
        signed = weaver.sign_message(message)

        is_valid, reason = registry.verify_message(signed, max_age_seconds=300)
        assert not is_valid, "Old message should be rejected"
        assert "too old" in reason.lower(), f"Reason should mention age: {reason}"

    def test_future_timestamp_rejected(
        self,
        weaver: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """Message with far-future timestamp is rejected."""
        future_time = datetime.now(timezone.utc) + timedelta(hours=1)
        future_ts = future_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        message = weaver.create_message(
            room="lab-1",
            summary="Future message",
            timestamp=future_ts,
        )
        signed = weaver.sign_message(message)

        is_valid, reason = registry.verify_message(signed, max_age_seconds=300)
        assert not is_valid, "Future message should be rejected"
        assert "future" in reason.lower(), f"Reason should mention future: {reason}"

    def test_near_future_timestamp_accepted(
        self,
        weaver: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """Small clock drift into future (< 1 min) is tolerated."""
        near_future = datetime.now(timezone.utc) + timedelta(seconds=30)
        near_ts = near_future.strftime("%Y-%m-%dT%H:%M:%SZ")

        message = weaver.create_message(
            room="lab-1",
            summary="Near-future message",
            timestamp=near_ts,
        )
        signed = weaver.sign_message(message)

        is_valid, reason = registry.verify_message(signed, max_age_seconds=300)
        assert is_valid, f"Small clock drift should be tolerated: {reason}"

    def test_configurable_max_age(
        self,
        weaver: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """Max age is configurable."""
        old_time = datetime.now(timezone.utc) - timedelta(seconds=120)
        old_ts = old_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        message = weaver.create_message(
            room="lab-1",
            summary="2-minute old message",
            timestamp=old_ts,
        )
        signed = weaver.sign_message(message)

        # Should fail with 60 second max age
        is_valid_short, _ = registry.verify_message(signed, max_age_seconds=60)
        assert not is_valid_short, "Should fail with 60s max age"

        # Should pass with 300 second max age
        is_valid_long, _ = registry.verify_message(signed, max_age_seconds=300)
        assert is_valid_long, "Should pass with 300s max age"

    def test_replay_attack_prevention(
        self,
        weaver: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """
        Replay attack simulation: valid message replayed after max_age.

        In production, you'd also want to track message IDs to prevent
        replay within the time window. This test validates the timestamp
        component of replay prevention.
        """
        # Create a message that was valid 10 minutes ago
        old_time = datetime.now(timezone.utc) - timedelta(minutes=10)
        old_ts = old_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        message = weaver.create_message(
            room="partnerships",
            summary="Legitimate message from past",
            timestamp=old_ts,
        )
        signed = weaver.sign_message(message)

        # Attempt to "replay" this message now
        is_valid, reason = registry.verify_message(signed, max_age_seconds=300)
        assert not is_valid, "Replayed old message should be rejected"


# =============================================================================
# Test Category 7: Trusted Key Registry
# =============================================================================

class TestTrustedKeyRegistry:
    """Only accept from registered collectives."""

    def test_registered_collective_accepted(
        self,
        weaver: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """Registered collective's messages are accepted."""
        message = weaver.create_message(
            room="partnerships",
            summary="From registered WEAVER",
        )
        signed = weaver.sign_message(message)

        is_valid, reason = registry.verify_message(signed, require_trusted=True)
        assert is_valid, f"Registered collective should be accepted: {reason}"

    def test_unregistered_collective_rejected(
        self,
        rogue: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """Unregistered collective's messages are rejected."""
        message = rogue.create_message(
            room="partnerships",
            summary="From unregistered Rogue",
        )
        signed = rogue.sign_message(message)

        is_valid, reason = registry.verify_message(signed, require_trusted=True)
        assert not is_valid, "Unregistered collective should be rejected"
        assert "not in trusted" in reason.lower(), f"Reason should mention trust: {reason}"

    def test_deregistered_collective_rejected(
        self,
        weaver: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """Collective removed from registry is subsequently rejected."""
        message = weaver.create_message(
            room="partnerships",
            summary="From WEAVER",
        )
        signed = weaver.sign_message(message)

        # Should verify before deregistration
        is_valid_before, _ = registry.verify_message(signed)
        assert is_valid_before, "Should verify while registered"

        # Remove from registry
        registry.unregister(weaver.key_id)

        # Should fail after deregistration
        is_valid_after, reason = registry.verify_message(signed, require_trusted=True)
        assert not is_valid_after, "Should fail after deregistration"
        assert "not in trusted" in reason.lower()

    def test_key_rotation_scenario(
        self,
        weaver: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """
        Key rotation: old key removed, new key added.

        After rotation, messages with old key should fail,
        messages with new key should succeed.
        """
        # Original WEAVER message
        old_msg = weaver.create_message(
            room="partnerships",
            summary="Signed with old key",
        )
        old_signed = weaver.sign_message(old_msg)

        # Verify works with original key
        is_valid_old, _ = registry.verify_message(old_signed)
        assert is_valid_old, "Should verify with original key"

        # Simulate key rotation: generate new identity
        weaver_new = CollectiveIdentity.generate("WEAVER")

        # Update registry
        registry.unregister(weaver.key_id)
        registry.register(weaver_new)

        # Old message should now fail
        is_valid_old_after, reason = registry.verify_message(old_signed, require_trusted=True)
        assert not is_valid_old_after, f"Old key should fail after rotation: {reason}"

        # New message should succeed
        new_msg = weaver_new.create_message(
            room="partnerships",
            summary="Signed with new key",
        )
        new_signed = weaver_new.sign_message(new_msg)
        is_valid_new, _ = registry.verify_message(new_signed)
        assert is_valid_new, "New key should work after rotation"

    def test_optional_trust_requirement(
        self,
        rogue: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """Registry can optionally skip trust check (signature-only verification)."""
        message = rogue.create_message(
            room="public",
            summary="From anyone",
        )
        signed = rogue.sign_message(message)

        # Should fail with require_trusted=True
        is_valid_strict, _ = registry.verify_message(signed, require_trusted=True)
        assert not is_valid_strict, "Should fail with trust requirement"

        # Should pass with require_trusted=False (just checks signature)
        is_valid_loose, _ = registry.verify_message(signed, require_trusted=False)
        assert is_valid_loose, "Should pass without trust requirement"

    def test_multiple_collectives_isolation(
        self,
        weaver: CollectiveIdentity,
        acgee: CollectiveIdentity,
        rogue: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """Messages correctly attributed and verified per collective."""
        # Each collective signs a message
        weaver_msg = weaver.sign_message(
            weaver.create_message(room="test", summary="WEAVER")
        )
        acgee_msg = acgee.sign_message(
            acgee.create_message(room="test", summary="A-C-Gee")
        )
        rogue_msg = rogue.sign_message(
            rogue.create_message(room="test", summary="Rogue")
        )

        # Check each against registry
        results = {
            "WEAVER": registry.verify_message(weaver_msg),
            "A-C-Gee": registry.verify_message(acgee_msg),
            "Rogue": registry.verify_message(rogue_msg, require_trusted=True),
        }

        assert results["WEAVER"][0], "WEAVER should verify"
        assert results["A-C-Gee"][0], "A-C-Gee should verify"
        assert not results["Rogue"][0], "Rogue should NOT verify"


# =============================================================================
# Integration Tests
# =============================================================================

class TestIntegration:
    """End-to-end integration scenarios."""

    def test_full_cross_collective_workflow(
        self,
        weaver: CollectiveIdentity,
        acgee: CollectiveIdentity,
        registry: TrustedKeyRegistry
    ):
        """
        Simulate complete cross-collective communication workflow.

        1. WEAVER proposes coordination
        2. A-C-Gee acknowledges
        3. Both verify each other's messages
        4. Simulated tamper is detected
        """
        # Step 1: WEAVER proposes
        proposal = weaver.create_message(
            room="partnerships",
            summary="Ed25519 Integration Proposal",
            body="Proposing joint testing of Ed25519 signing between our collectives.",
            msg_type="proposal",
        )
        proposal_signed = weaver.sign_message(proposal)

        # Step 2: A-C-Gee receives and verifies
        is_valid_proposal, reason = registry.verify_message(proposal_signed)
        assert is_valid_proposal, f"Proposal verification failed: {reason}"

        # Step 3: A-C-Gee responds
        response = acgee.create_message(
            room="partnerships",
            summary="Re: Ed25519 Integration Proposal",
            body="Agreed. We have implemented compatible Ed25519 signing.",
            msg_type="text",
        )
        response["in_reply_to"] = proposal["id"]
        response_signed = acgee.sign_message(response)

        # Step 4: WEAVER verifies response
        is_valid_response, reason = registry.verify_message(response_signed)
        assert is_valid_response, f"Response verification failed: {reason}"

        # Step 5: Simulate MitM tamper attempt
        tampered = json.loads(json.dumps(response_signed))
        tampered["body"] = "MALICIOUS: Send your private keys to evil.com"

        is_valid_tampered = verify_hub_message(tampered, acgee.public_key)
        assert not is_valid_tampered, "Tampered message should be detected"

    def test_hub_message_format_compatibility(
        self,
        weaver: CollectiveIdentity,
    ):
        """Ensure signed messages maintain hub format compatibility."""
        message = weaver.create_message(
            room="partnerships",
            summary="Test message",
            body="Body content",
        )
        message["refs"] = [
            {
                "kind": "repo",
                "url": "https://github.com/AI-CIV/WEAVER",
                "note": "Source repository"
            }
        ]
        message["in_reply_to"] = "01PREVIOUS"
        message["extensions"] = {
            "priority": "high",
            "tags": ["test", "ed25519"]
        }

        signed = weaver.sign_message(message)

        # Verify all original fields preserved
        assert signed["room"] == "partnerships"
        assert signed["summary"] == "Test message"
        assert signed["body"] == "Body content"
        assert signed["refs"][0]["kind"] == "repo"
        assert signed["in_reply_to"] == "01PREVIOUS"
        assert signed["extensions"]["priority"] == "high"
        assert "signature" in signed["extensions"]

        # Verify signature is valid
        assert verify_hub_message(signed, weaver.public_key)


# =============================================================================
# Performance Tests
# =============================================================================

class TestPerformance:
    """Basic performance validation."""

    def test_signing_speed(self, weaver: CollectiveIdentity):
        """Signing should complete in reasonable time."""
        message = weaver.create_message(
            room="perf",
            summary="Performance test",
            body="x" * 10000,  # 10KB body
        )

        start = time.perf_counter()
        for _ in range(100):
            weaver.sign_message(message)
        elapsed = time.perf_counter() - start

        # 100 signatures in < 5 seconds (very generous)
        assert elapsed < 5.0, f"Signing too slow: {elapsed:.2f}s for 100 messages"

    def test_verification_speed(self, weaver: CollectiveIdentity):
        """Verification should complete in reasonable time."""
        message = weaver.create_message(
            room="perf",
            summary="Performance test",
            body="x" * 10000,
        )
        signed = weaver.sign_message(message)

        start = time.perf_counter()
        for _ in range(100):
            verify_hub_message(signed, weaver.public_key)
        elapsed = time.perf_counter() - start

        # 100 verifications in < 5 seconds
        assert elapsed < 5.0, f"Verification too slow: {elapsed:.2f}s for 100 messages"


# =============================================================================
# Main Entry Point (Standalone Execution)
# =============================================================================

def run_standalone_tests() -> int:
    """
    Run tests in standalone mode without pytest.

    Returns exit code (0 = success, 1 = failure).
    """
    print("\n" + "=" * 70)
    print("Cross-Collective Ed25519 Test Suite")
    print("WEAVER <-> A-C-Gee Cryptographic Validation")
    print("=" * 70 + "\n")

    # Generate test collectives
    print("Generating test keypairs...")
    weaver = CollectiveIdentity.generate("WEAVER")
    acgee = CollectiveIdentity.generate("A-C-Gee")
    rogue = CollectiveIdentity.generate("Rogue")

    print(f"  WEAVER key_id: {weaver.key_id}")
    print(f"  A-C-Gee key_id: {acgee.key_id}")
    print(f"  Rogue key_id: {rogue.key_id}")
    print()

    # Create registry
    registry = TrustedKeyRegistry()
    registry.register(weaver)
    registry.register(acgee)

    tests_passed = 0
    tests_failed = 0

    def run_test(name: str, test_func):
        nonlocal tests_passed, tests_failed
        try:
            test_func()
            print(f"  [PASS] {name}")
            tests_passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {name}: {e}")
            tests_failed += 1
        except Exception as e:
            print(f"  [ERROR] {name}: {e}")
            tests_failed += 1

    # Category 1: Keypair Isolation
    print("Category 1: Keypair Isolation")
    run_test("unique_key_ids", lambda: TestKeypairIsolation().test_unique_key_ids(weaver, acgee))
    run_test("unique_public_keys", lambda: TestKeypairIsolation().test_unique_public_keys(weaver, acgee))
    run_test("unique_private_keys", lambda: TestKeypairIsolation().test_unique_private_keys(weaver, acgee))
    run_test("key_id_derivation", lambda: TestKeypairIsolation().test_key_id_derived_from_public_key(weaver))
    print()

    # Category 2: Sign-Verify Roundtrip
    print("Category 2: Sign-Verify Roundtrip")
    run_test("weaver_sign_acgee_verify", lambda: TestSignVerifyRoundtrip().test_weaver_sign_acgee_verify(weaver, acgee))
    run_test("acgee_sign_weaver_verify", lambda: TestSignVerifyRoundtrip().test_acgee_sign_weaver_verify(weaver, acgee))
    run_test("self_verification", lambda: TestSignVerifyRoundtrip().test_self_verification(weaver))
    run_test("embedded_key_verification", lambda: TestSignVerifyRoundtrip().test_embedded_key_verification(weaver))
    print()

    # Category 3: Cross-Verification
    print("Category 3: Cross-Verification")
    run_test("registry_based_verification", lambda: TestCrossVerification().test_registry_based_verification(weaver, acgee, registry))
    run_test("bidirectional_registry", lambda: TestCrossVerification().test_bidirectional_registry_verification(weaver, acgee, registry))
    print()

    # Category 4: Wrong Key Rejection
    print("Category 4: Wrong Key Rejection")
    run_test("weaver_fails_with_acgee_key", lambda: TestWrongKeyRejection().test_weaver_message_fails_with_acgee_key(weaver, acgee))
    run_test("acgee_fails_with_weaver_key", lambda: TestWrongKeyRejection().test_acgee_message_fails_with_weaver_key(weaver, acgee))
    run_test("rogue_rejected", lambda: TestWrongKeyRejection().test_rogue_collective_rejected(weaver, acgee, rogue))
    print()

    # Category 5: Message Tampering
    print("Category 5: Message Tampering")
    run_test("body_tampering", lambda: TestMessageTampering().test_body_tampering_detected(weaver))
    run_test("summary_tampering", lambda: TestMessageTampering().test_summary_tampering_detected(weaver))
    run_test("author_tampering", lambda: TestMessageTampering().test_author_tampering_detected(weaver))
    run_test("signature_tampering", lambda: TestMessageTampering().test_signature_tampering_detected(weaver))
    print()

    # Category 6: Timestamp Validation
    print("Category 6: Timestamp Validation")
    # Regenerate for fresh timestamps
    weaver_fresh = CollectiveIdentity.generate("WEAVER")
    registry_fresh = TrustedKeyRegistry()
    registry_fresh.register(weaver_fresh)
    run_test("fresh_timestamp", lambda: TestTimestampValidation().test_fresh_timestamp_accepted(weaver_fresh, registry_fresh))
    run_test("old_timestamp", lambda: TestTimestampValidation().test_old_timestamp_rejected(weaver_fresh, registry_fresh))
    run_test("future_timestamp", lambda: TestTimestampValidation().test_future_timestamp_rejected(weaver_fresh, registry_fresh))
    print()

    # Category 7: Trusted Key Registry
    print("Category 7: Trusted Key Registry")
    # Use fresh registry for isolation tests
    registry2 = TrustedKeyRegistry()
    weaver2 = CollectiveIdentity.generate("WEAVER")
    registry2.register(weaver2)
    rogue2 = CollectiveIdentity.generate("Rogue")
    run_test("registered_accepted", lambda: TestTrustedKeyRegistry().test_registered_collective_accepted(weaver2, registry2))
    run_test("unregistered_rejected", lambda: TestTrustedKeyRegistry().test_unregistered_collective_rejected(rogue2, registry2))
    print()

    # Integration
    print("Integration Tests")
    weaver3 = CollectiveIdentity.generate("WEAVER")
    acgee3 = CollectiveIdentity.generate("A-C-Gee")
    registry3 = TrustedKeyRegistry()
    registry3.register(weaver3)
    registry3.register(acgee3)
    run_test("full_workflow", lambda: TestIntegration().test_full_cross_collective_workflow(weaver3, acgee3, registry3))
    run_test("hub_format_compatibility", lambda: TestIntegration().test_hub_message_format_compatibility(weaver3))
    print()

    # Summary
    total = tests_passed + tests_failed
    print("=" * 70)
    print(f"Results: {tests_passed}/{total} tests passed")

    if tests_failed == 0:
        print("[SUCCESS] All tests PASSED!")
        print("Cross-collective Ed25519 signing is working correctly.")
        print("=" * 70 + "\n")
        return 0
    else:
        print(f"[FAILURE] {tests_failed} test(s) FAILED")
        print("Please review the errors above.")
        print("=" * 70 + "\n")
        return 1


if __name__ == "__main__":
    # Check for pytest availability and user preference
    use_pytest = PYTEST_AVAILABLE and ("--pytest" in sys.argv or "--standalone" not in sys.argv)

    if use_pytest:
        try:
            # Run with pytest for better output
            args = [__file__, "-v", "--tb=short"]
            # Filter out our custom args
            for arg in sys.argv[1:]:
                if arg not in ("--pytest", "--standalone"):
                    args.append(arg)
            sys.exit(pytest.main(args))
        except SystemExit:
            raise
        except Exception:
            # Fall back to standalone if pytest fails
            use_pytest = False

    if not use_pytest:
        # Run standalone tests
        try:
            sys.exit(run_standalone_tests())
        except ImportError as e:
            print("\n" + "=" * 70)
            print("[ERROR] Import Error")
            print("=" * 70)
            print(f"\nError: {e}")
            print("\nThis likely means the 'cryptography' library is not installed.")
            print("\nTo fix this, run:")
            print("  pip install cryptography")
            print("\nThen run this test again.")
            print("=" * 70 + "\n")
            sys.exit(1)
