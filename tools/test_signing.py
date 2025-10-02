#!/usr/bin/env python3
"""
Quick test script to verify Ed25519 signing implementation.

This script runs basic tests to ensure the signing library works correctly.
Run this before integrating into production.

Usage:
    python3 test_signing.py
"""

import sys
import json
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sign_message import (
    Ed25519Signer,
    generate_keypair,
    sign_hub_message,
    verify_hub_message,
    SigningError,
    VerificationError
)


def test_key_generation():
    """Test keypair generation."""
    print("Test 1: Key Generation...", end=" ")
    try:
        private_key, public_key = generate_keypair()
        assert len(private_key) > 0, "Private key is empty"
        assert len(public_key) > 0, "Public key is empty"
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_signer_creation():
    """Test creating signer from keys."""
    print("Test 2: Signer Creation...", end=" ")
    try:
        private_key, public_key = generate_keypair()
        signer = Ed25519Signer.from_private_key(private_key)
        assert signer.export_public_key() == public_key, "Public key mismatch"
        assert signer.get_key_id() is not None, "Key ID not generated"
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_message_signing():
    """Test signing a message."""
    print("Test 3: Message Signing...", end=" ")
    try:
        private_key, _ = generate_keypair()
        signer = Ed25519Signer.from_private_key(private_key)

        message = {
            "version": "1.0",
            "id": "01TEST",
            "room": "test",
            "author": {"id": "test", "display": "Test"},
            "ts": "2025-10-02T10:00:00Z",
            "type": "text",
            "summary": "Test message"
        }

        signed = sign_hub_message(message, signer)
        assert "extensions" in signed, "No extensions field"
        assert "signature" in signed["extensions"], "No signature in extensions"
        assert signed["extensions"]["signature"]["algorithm"] == "Ed25519", "Wrong algorithm"
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_signature_verification():
    """Test verifying a valid signature."""
    print("Test 4: Signature Verification...", end=" ")
    try:
        private_key, _ = generate_keypair()
        signer = Ed25519Signer.from_private_key(private_key)

        message = {
            "version": "1.0",
            "id": "01TEST",
            "room": "test",
            "author": {"id": "test", "display": "Test"},
            "ts": "2025-10-02T10:00:00Z",
            "type": "text",
            "summary": "Test message"
        }

        signed = sign_hub_message(message, signer)
        is_valid = verify_hub_message(signed)
        assert is_valid == True, "Valid signature not verified"
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_tampering_detection():
    """Test detecting tampered messages."""
    print("Test 5: Tampering Detection...", end=" ")
    try:
        private_key, _ = generate_keypair()
        signer = Ed25519Signer.from_private_key(private_key)

        message = {
            "version": "1.0",
            "id": "01TEST",
            "room": "test",
            "author": {"id": "test", "display": "Test"},
            "ts": "2025-10-02T10:00:00Z",
            "type": "text",
            "summary": "Test message",
            "body": "Original content"
        }

        signed = sign_hub_message(message, signer)

        # Tamper with the message
        tampered = signed.copy()
        tampered["body"] = "TAMPERED"

        is_valid = verify_hub_message(tampered)
        assert is_valid == False, "Tampered message verified as valid!"
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_unsigned_message():
    """Test handling unsigned messages."""
    print("Test 6: Unsigned Message Handling...", end=" ")
    try:
        message = {
            "version": "1.0",
            "id": "01TEST",
            "room": "test",
            "author": {"id": "test", "display": "Test"},
            "ts": "2025-10-02T10:00:00Z",
            "type": "text",
            "summary": "Unsigned message"
        }

        try:
            verify_hub_message(message)
            print("✗ FAIL: Should raise VerificationError")
            return False
        except VerificationError:
            print("✓ PASS")
            return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_wrong_key_verification():
    """Test verification with wrong public key."""
    print("Test 7: Wrong Key Detection...", end=" ")
    try:
        private_key1, _ = generate_keypair()
        private_key2, public_key2 = generate_keypair()

        signer1 = Ed25519Signer.from_private_key(private_key1)

        message = {
            "version": "1.0",
            "id": "01TEST",
            "room": "test",
            "author": {"id": "test", "display": "Test"},
            "ts": "2025-10-02T10:00:00Z",
            "type": "text",
            "summary": "Test message"
        }

        signed = sign_hub_message(message, signer1)

        # Try to verify with different key
        is_valid = verify_hub_message(signed, public_key2)
        assert is_valid == False, "Wrong key verified as valid!"
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_key_export_import():
    """Test exporting and reimporting keys."""
    print("Test 8: Key Export/Import...", end=" ")
    try:
        # Generate and export
        private_key1, public_key1 = generate_keypair()
        signer1 = Ed25519Signer.from_private_key(private_key1)
        key_id1 = signer1.get_key_id()

        # Reimport
        signer2 = Ed25519Signer.from_private_key(private_key1)
        public_key2 = signer2.export_public_key()
        key_id2 = signer2.get_key_id()

        # Verify consistency
        assert public_key1 == public_key2, "Public key changed after reimport"
        assert key_id1 == key_id2, "Key ID changed after reimport"

        # Sign with both and verify
        message = {"test": "data"}
        sig1 = signer1.sign(json.dumps(message).encode())
        sig2 = signer2.sign(json.dumps(message).encode())
        assert sig1 == sig2, "Different signatures from same key"

        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_deterministic_signatures():
    """Test that signatures are deterministic."""
    print("Test 9: Deterministic Signatures...", end=" ")
    try:
        private_key, _ = generate_keypair()
        signer = Ed25519Signer.from_private_key(private_key)

        message = {
            "version": "1.0",
            "id": "01TEST",
            "room": "test",
            "author": {"id": "test", "display": "Test"},
            "ts": "2025-10-02T10:00:00Z",
            "type": "text",
            "summary": "Test message"
        }

        # Sign twice
        signed1 = sign_hub_message(message, signer)
        signed2 = sign_hub_message(message, signer)

        # Signatures should be identical
        sig1 = signed1["extensions"]["signature"]["signature"]
        sig2 = signed2["extensions"]["signature"]["signature"]
        assert sig1 == sig2, "Signatures are not deterministic"

        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_all_message_fields():
    """Test signing message with all optional fields."""
    print("Test 10: All Message Fields...", end=" ")
    try:
        private_key, _ = generate_keypair()
        signer = Ed25519Signer.from_private_key(private_key)

        message = {
            "version": "1.0",
            "id": "01TEST",
            "room": "test",
            "author": {"id": "test", "display": "Test Agent"},
            "ts": "2025-10-02T10:00:00Z",
            "type": "text",
            "summary": "Complete message",
            "body": "Full message body with content",
            "refs": [
                {
                    "kind": "repo",
                    "url": "https://github.com/example/repo",
                    "note": "Related repository"
                }
            ],
            "in_reply_to": "01PREVIOUS",
            "extensions": {
                "custom_field": "custom_value"
            }
        }

        signed = sign_hub_message(message, signer)
        is_valid = verify_hub_message(signed)
        assert is_valid == True, "Complex message failed verification"

        # Verify all original fields preserved
        assert signed["body"] == message["body"], "Body field lost"
        assert signed["refs"] == message["refs"], "Refs field lost"
        assert signed["in_reply_to"] == message["in_reply_to"], "in_reply_to field lost"
        assert "custom_field" in signed["extensions"], "Custom extension lost"

        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("Ed25519 Message Signing - Test Suite")
    print("=" * 70 + "\n")

    tests = [
        test_key_generation,
        test_signer_creation,
        test_message_signing,
        test_signature_verification,
        test_tampering_detection,
        test_unsigned_message,
        test_wrong_key_verification,
        test_key_export_import,
        test_deterministic_signatures,
        test_all_message_fields,
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"   Unexpected error: {e}")
            results.append(False)

    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("✓ All tests PASSED! Implementation is working correctly.")
        print("=" * 70 + "\n")
        return 0
    else:
        print(f"✗ {total - passed} test(s) FAILED. Please review errors above.")
        print("=" * 70 + "\n")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ImportError as e:
        print("\n" + "=" * 70)
        print("✗ Import Error")
        print("=" * 70)
        print(f"\nError: {e}")
        print("\nThis likely means the 'cryptography' library is not installed.")
        print("\nTo fix this, run:")
        print("  pip install cryptography")
        print("\nThen run this test again.")
        print("=" * 70 + "\n")
        sys.exit(1)
    except Exception as e:
        print("\n" + "=" * 70)
        print("✗ Unexpected Error")
        print("=" * 70)
        print(f"\nError: {e}")
        print("\nPlease check the error message above and fix any issues.")
        print("=" * 70 + "\n")
        sys.exit(1)
