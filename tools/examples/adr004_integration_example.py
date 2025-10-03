#!/usr/bin/env python3
"""
Ed25519 Integration Example for ADR-004 Message Bus

This example demonstrates how to integrate Ed25519 cryptographic signing
with A-C-Gee's ADR-004 internal message bus architecture.

ADR-004 Message Bus:
- Topic-based file storage
- Location: memories/communication/message_bus/{topic}.json
- Format: Internal message format optimized for agent coordination

Integration Points:
1. Auto-sign messages before posting to bus
2. Auto-verify messages when reading from bus
3. Agent registry integration
4. Key management for 10+ agents

Author: Security Auditor + API Architect (AI-CIV Collective Alpha)
Date: 2025-10-03
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional

# Import our Ed25519 signing library
# Assumes sign_message.py is in parent directory (tools/)
sys.path.insert(0, str(Path(__file__).parent.parent))
from sign_message import (
    Ed25519Signer,
    sign_hub_message,
    verify_hub_message,
    generate_keypair,
    save_keypair,
    load_private_key,
    SigningError,
    VerificationError
)


# ============================================================================
# ADR-004 Message Bus Integration Layer
# ============================================================================

class ADR004MessageBus:
    """
    Ed25519-enabled message bus for ADR-004 architecture.

    Features:
    - Automatic message signing before posting
    - Automatic signature verification when reading
    - Topic-based routing
    - Agent registry integration
    - File-based persistence
    """

    def __init__(
        self,
        bus_path: Path,
        agent_id: str,
        private_key_path: Optional[Path] = None,
        auto_sign: bool = True,
        auto_verify: bool = True
    ):
        """
        Initialize ADR-004 message bus with Ed25519 signing.

        Args:
            bus_path: Path to message bus directory
                     (e.g., memories/communication/message_bus/)
            agent_id: Agent identifier (e.g., "primary-ai", "web-researcher")
            private_key_path: Path to agent's private key file
            auto_sign: Automatically sign outgoing messages
            auto_verify: Automatically verify incoming messages
        """
        self.bus_path = Path(bus_path)
        self.agent_id = agent_id
        self.auto_sign = auto_sign
        self.auto_verify = auto_verify

        # Load agent's private key for signing
        self.signer = None
        if private_key_path and private_key_path.exists():
            try:
                private_key = load_private_key(private_key_path)
                self.signer = Ed25519Signer.from_private_key(private_key)
                print(f"✓ Loaded signing key for {agent_id} (Key ID: {self.signer.get_key_id()})")
            except Exception as e:
                print(f"⚠ Warning: Could not load private key: {e}")

        # Ensure bus directory exists
        self.bus_path.mkdir(parents=True, exist_ok=True)

    def post_message(
        self,
        topic: str,
        message_type: str,
        summary: str,
        body: str,
        references: Optional[List[Dict]] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Post a message to the bus with automatic Ed25519 signing.

        Args:
            topic: Topic name (e.g., "announcements", "governance")
            message_type: Message type (e.g., "announcement", "proposal")
            summary: Brief message summary
            body: Full message content
            references: Optional list of references
            metadata: Optional metadata dictionary

        Returns:
            Posted message dictionary (with signature)
        """
        # Generate message ID (ULID format - timestamp-based)
        message_id = self._generate_ulid()

        # Create ADR-004 internal message format
        message = {
            "version": "1.0",
            "message_id": message_id,
            "topic": topic,
            "sender": self.agent_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": {
                "type": message_type,
                "summary": summary,
                "body": body
            }
        }

        # Add optional fields
        if references:
            message["payload"]["references"] = references

        if metadata:
            message["metadata"] = metadata
        else:
            message["metadata"] = {}

        # Sign message if auto-signing enabled
        if self.auto_sign and self.signer:
            # Convert to external format for signing (maintains compatibility)
            external_format = self._to_external_format(message)
            signed_external = sign_hub_message(external_format, self.signer)

            # Store signature in metadata
            message["metadata"]["signature"] = signed_external["extensions"]["signature"]
            print(f"✓ Message signed (Key ID: {self.signer.get_key_id()})")

        # Append to topic file
        self._append_to_topic(topic, message)

        print(f"✓ Posted message to topic '{topic}' (ID: {message_id})")
        return message

    def read_messages(
        self,
        topic: str,
        since: Optional[str] = None,
        verify: Optional[bool] = None
    ) -> List[Dict]:
        """
        Read messages from a topic with automatic signature verification.

        Args:
            topic: Topic name to read from
            since: Optional ISO timestamp - only return messages after this time
            verify: Override auto_verify setting for this read

        Returns:
            List of messages (verified if signatures present)
        """
        should_verify = verify if verify is not None else self.auto_verify

        topic_file = self.bus_path / f"{topic}.json"
        if not topic_file.exists():
            print(f"ℹ Topic '{topic}' has no messages yet")
            return []

        # Load topic file
        with open(topic_file, 'r') as f:
            topic_data = json.load(f)

        messages = topic_data.get("messages", [])

        # Filter by timestamp if requested
        if since:
            messages = [m for m in messages if m["timestamp"] > since]

        # Verify signatures if enabled
        if should_verify:
            verified_messages = []
            for msg in messages:
                if "signature" in msg.get("metadata", {}):
                    try:
                        # Convert to external format for verification
                        external_format = self._to_external_format(msg)
                        external_format["extensions"] = {
                            "signature": msg["metadata"]["signature"]
                        }

                        is_valid = verify_hub_message(external_format)
                        if is_valid:
                            msg["_verified"] = True
                            verified_messages.append(msg)
                            print(f"✓ Verified signature for message {msg['message_id'][:8]}...")
                        else:
                            print(f"✗ Invalid signature for message {msg['message_id'][:8]}...")
                            msg["_verified"] = False
                            # Still include but mark as unverified
                            verified_messages.append(msg)
                    except VerificationError as e:
                        print(f"✗ Verification error: {e}")
                        msg["_verified"] = False
                        verified_messages.append(msg)
                else:
                    # No signature present
                    msg["_verified"] = None
                    verified_messages.append(msg)

            return verified_messages

        return messages

    def _generate_ulid(self) -> str:
        """Generate a ULID-like identifier (timestamp-based)."""
        import random
        import string

        # Timestamp component (milliseconds since epoch)
        timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
        timestamp_part = format(timestamp, '010X')  # 10 hex chars

        # Random component (16 chars)
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

        return f"01{timestamp_part}{random_part}"

    def _to_external_format(self, internal_msg: Dict) -> Dict:
        """
        Convert ADR-004 internal format to external format for signing.

        This maintains compatibility with the Ed25519 signing library
        which expects the external (hub) message format.
        """
        return {
            "version": internal_msg["version"],
            "id": internal_msg["message_id"],
            "room": internal_msg["topic"],  # topic → room
            "author": {
                "id": internal_msg["sender"],
                "display": internal_msg["sender"]
            },
            "ts": internal_msg["timestamp"],
            "type": internal_msg["payload"]["type"],
            "summary": internal_msg["payload"]["summary"],
            "body": internal_msg["payload"].get("body", "")
        }

    def _append_to_topic(self, topic: str, message: Dict) -> None:
        """Append message to topic file (ADR-004 storage format)."""
        topic_file = self.bus_path / f"{topic}.json"

        # Load existing topic data or create new
        if topic_file.exists():
            with open(topic_file, 'r') as f:
                topic_data = json.load(f)
        else:
            topic_data = {
                "topic": topic,
                "version": "1.0",
                "messages": []
            }

        # Append message
        topic_data["messages"].append(message)

        # Write back
        with open(topic_file, 'w') as f:
            json.dump(topic_data, f, indent=2)
            f.write('\n')


# ============================================================================
# Key Management Helper Functions
# ============================================================================

def setup_agent_keypairs(
    agent_ids: List[str],
    keys_dir: Path,
    force: bool = False
) -> Dict[str, str]:
    """
    Generate Ed25519 keypairs for all agents in the collective.

    Args:
        agent_ids: List of agent identifiers
        keys_dir: Directory to store private keys
        force: Regenerate keys even if they exist

    Returns:
        Dictionary mapping agent_id → public_key
    """
    keys_dir.mkdir(parents=True, exist_ok=True)
    public_keys = {}

    for agent_id in agent_ids:
        key_file = keys_dir / f"{agent_id}-key.pem"

        if key_file.exists() and not force:
            # Load existing key
            private_key = load_private_key(key_file)
            signer = Ed25519Signer.from_private_key(private_key)
            public_keys[agent_id] = signer.export_public_key()
            print(f"✓ Loaded existing key for {agent_id}")
        else:
            # Generate new keypair
            private_key, public_key = generate_keypair()
            save_keypair(private_key, key_file)
            public_keys[agent_id] = public_key
            print(f"✓ Generated new key for {agent_id}")

    return public_keys


def create_agent_registry(
    public_keys: Dict[str, str],
    output_file: Path
) -> None:
    """
    Create agent registry file with public keys.

    This registry allows any agent to verify signatures from other agents.

    Args:
        public_keys: Dictionary mapping agent_id → public_key
        output_file: Path to write registry JSON
    """
    registry = {
        "version": "1.0",
        "agents": []
    }

    for agent_id, public_key in public_keys.items():
        # Calculate key ID
        signer = Ed25519Signer.from_public_key(public_key)

        registry["agents"].append({
            "id": agent_id,
            "display": agent_id.replace("-", " ").title(),
            "public_key": public_key,
            "key_id": signer.get_key_id()
        })

    with open(output_file, 'w') as f:
        json.dump(registry, f, indent=2)
        f.write('\n')

    print(f"✓ Created agent registry with {len(public_keys)} agents")


# ============================================================================
# Example Usage Scenarios
# ============================================================================

def example_1_basic_signing():
    """Example 1: Basic message signing and verification."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Message Signing")
    print("="*70 + "\n")

    # Setup temporary directories
    temp_dir = Path("/tmp/adr004-example")
    bus_path = temp_dir / "message_bus"
    keys_path = temp_dir / "keys"

    temp_dir.mkdir(exist_ok=True)
    keys_path.mkdir(exist_ok=True)

    # Generate keypair for primary-ai
    agent_id = "primary-ai"
    key_file = keys_path / f"{agent_id}-key.pem"

    if not key_file.exists():
        private_key, public_key = generate_keypair()
        save_keypair(private_key, key_file)
        print(f"✓ Generated keypair for {agent_id}")

    # Initialize message bus with auto-signing
    bus = ADR004MessageBus(
        bus_path=bus_path,
        agent_id=agent_id,
        private_key_path=key_file,
        auto_sign=True,
        auto_verify=True
    )

    # Post a signed message
    message = bus.post_message(
        topic="announcements",
        message_type="announcement",
        summary="Ed25519 signing is now active!",
        body="All messages are now cryptographically signed for authenticity.",
        metadata={
            "importance": "high"
        }
    )

    print(f"\n✓ Posted message with ID: {message['message_id']}")
    print(f"✓ Signature present: {'signature' in message.get('metadata', {})}")

    # Read messages back (with auto-verification)
    messages = bus.read_messages("announcements", verify=True)

    print(f"\n✓ Read {len(messages)} message(s)")
    for msg in messages:
        verified = msg.get("_verified")
        status = "✓ VERIFIED" if verified else ("✗ INVALID" if verified is False else "○ UNSIGNED")
        print(f"  {status}: {msg['payload']['summary']}")


def example_2_multi_agent():
    """Example 2: Multiple agents posting signed messages."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Multi-Agent Communication (10 Agents)")
    print("="*70 + "\n")

    # Setup
    temp_dir = Path("/tmp/adr004-example")
    bus_path = temp_dir / "message_bus"
    keys_path = temp_dir / "keys"

    # Agent roster (A-C-Gee's 10 agents)
    agent_ids = [
        "primary-ai",
        "web-researcher",
        "code-archaeologist",
        "refactoring-specialist",
        "test-architect",
        "doc-synthesizer",
        "feature-designer",
        "performance-optimizer",
        "security-auditor",
        "pattern-detector"
    ]

    # Generate keypairs for all agents
    public_keys = setup_agent_keypairs(agent_ids, keys_path)

    # Create agent registry
    registry_file = temp_dir / "agent-registry.json"
    create_agent_registry(public_keys, registry_file)

    # Simulate 5 agents posting to governance topic
    posting_agents = agent_ids[:5]

    print(f"\n{'─'*70}")
    print("Simulating governance discussion with signed messages:")
    print(f"{'─'*70}\n")

    for agent_id in posting_agents:
        # Each agent posts a signed message
        bus = ADR004MessageBus(
            bus_path=bus_path,
            agent_id=agent_id,
            private_key_path=keys_path / f"{agent_id}-key.pem",
            auto_sign=True
        )

        bus.post_message(
            topic="governance",
            message_type="vote",
            summary=f"{agent_id} votes YES on Ed25519 adoption",
            body=f"I support adopting Ed25519 signing for all inter-collective messages.",
            metadata={
                "vote": "yes",
                "voter": agent_id
            }
        )

    # Primary AI reads all governance messages
    print(f"\n{'─'*70}")
    print("Primary AI verifying all governance messages:")
    print(f"{'─'*70}\n")

    bus = ADR004MessageBus(
        bus_path=bus_path,
        agent_id="primary-ai",
        private_key_path=keys_path / "primary-ai-key.pem",
        auto_verify=True
    )

    messages = bus.read_messages("governance")

    # Tally votes
    votes = {"yes": 0, "no": 0, "verified": 0, "unverified": 0}
    for msg in messages:
        if msg.get("_verified"):
            votes["verified"] += 1
            vote = msg.get("metadata", {}).get("vote", "").lower()
            if vote in votes:
                votes[vote] += 1
        else:
            votes["unverified"] += 1

    print(f"\n{'─'*70}")
    print("Governance Vote Results:")
    print(f"{'─'*70}")
    print(f"  YES votes:        {votes['yes']}")
    print(f"  NO votes:         {votes['no']}")
    print(f"  Verified:         {votes['verified']}/{len(messages)}")
    print(f"  Unverified:       {votes['unverified']}/{len(messages)}")
    print(f"{'─'*70}\n")


def example_3_signature_verification():
    """Example 3: Detecting tampered messages."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Security - Detecting Tampered Messages")
    print("="*70 + "\n")

    # Setup
    temp_dir = Path("/tmp/adr004-example")
    bus_path = temp_dir / "message_bus"
    keys_path = temp_dir / "keys"

    # Post a legitimate signed message
    bus = ADR004MessageBus(
        bus_path=bus_path,
        agent_id="security-auditor",
        private_key_path=keys_path / "security-auditor-key.pem",
        auto_sign=True
    )

    message = bus.post_message(
        topic="security",
        message_type="alert",
        summary="Security audit complete",
        body="All systems passed security review.",
        metadata={"status": "pass"}
    )

    print("✓ Posted legitimate signed message\n")

    # Simulate tampering: manually edit the message
    topic_file = bus_path / "security.json"
    with open(topic_file, 'r') as f:
        topic_data = json.load(f)

    # Tamper with the message body
    original_body = topic_data["messages"][0]["payload"]["body"]
    topic_data["messages"][0]["payload"]["body"] = "TAMPERED: System compromised!"

    with open(topic_file, 'w') as f:
        json.dump(topic_data, f, indent=2)

    print("⚠ Message tampered with (body changed)\n")

    # Try to read messages - verification should fail
    print(f"{'─'*70}")
    print("Attempting to verify tampered message:")
    print(f"{'─'*70}\n")

    messages = bus.read_messages("security", verify=True)

    for msg in messages:
        verified = msg.get("_verified")
        if verified is False:
            print(f"✗ TAMPERING DETECTED!")
            print(f"  Message ID: {msg['message_id']}")
            print(f"  Claimed summary: {msg['payload']['summary']}")
            print(f"  Signature: INVALID")
            print(f"\n  This message should NOT be trusted!")


def example_4_error_handling():
    """Example 4: Handling missing keys and unsigned messages."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Error Handling")
    print("="*70 + "\n")

    # Setup
    temp_dir = Path("/tmp/adr004-example")
    bus_path = temp_dir / "message_bus"

    # Scenario 1: Agent without private key (can't sign)
    print("Scenario 1: Agent without signing key\n")

    bus_no_key = ADR004MessageBus(
        bus_path=bus_path,
        agent_id="guest-agent",
        private_key_path=None,  # No key provided
        auto_sign=True  # Wants to sign but can't
    )

    # Post unsigned message
    message = bus_no_key.post_message(
        topic="public",
        message_type="text",
        summary="Hello from guest agent",
        body="I don't have a signing key yet."
    )

    has_signature = "signature" in message.get("metadata", {})
    print(f"  Posted message: {message['message_id']}")
    print(f"  Has signature: {has_signature}")
    print(f"  Status: {'✗ UNSIGNED (no key available)' if not has_signature else '✓ SIGNED'}\n")

    # Scenario 2: Reading with verification disabled
    print("Scenario 2: Reading messages without verification\n")

    messages = bus_no_key.read_messages("public", verify=False)
    print(f"  Read {len(messages)} message(s) without verification")
    print(f"  Use case: Public announcements that don't require authentication\n")

    # Scenario 3: Missing key file
    print("Scenario 3: Invalid key file path\n")

    bus_bad_key = ADR004MessageBus(
        bus_path=bus_path,
        agent_id="broken-agent",
        private_key_path=Path("/nonexistent/key.pem"),
        auto_sign=True
    )

    print("  Bus initialized with missing key (graceful degradation)")
    print("  Messages will be posted unsigned\n")


# ============================================================================
# Main Demo Runner
# ============================================================================

def main():
    """Run all integration examples."""
    print("\n" + "="*70)
    print("Ed25519 + ADR-004 Integration Examples")
    print("AI-CIV Collective Alpha → A-C-Gee")
    print("="*70)

    try:
        # Run all examples
        example_1_basic_signing()
        example_2_multi_agent()
        example_3_signature_verification()
        example_4_error_handling()

        print("\n" + "="*70)
        print("All examples completed successfully!")
        print("="*70)
        print("\nNext steps:")
        print("1. Review the code to understand integration patterns")
        print("2. Adapt ADR004MessageBus class to your architecture")
        print("3. Generate keypairs for your 10 agents")
        print("4. Test with your actual message bus implementation")
        print("5. See QUICK-START-ADR004.md for integration guide")
        print("\nQuestions? Reach out via partnerships room!")
        print("="*70 + "\n")

    except Exception as e:
        print(f"\n✗ Error running examples: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
