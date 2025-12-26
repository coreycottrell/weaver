"""
Test Fixtures and Configuration

Pytest fixtures for Trading Arena API integration testing.
- Test client (FastAPI TestClient)
- Ed25519 keypair generation
- Request signing helpers
- Nonce tracking for replay detection
"""

import base64
import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Optional, Generator
import pytest

from nacl.signing import SigningKey
from fastapi.testclient import TestClient

from api.app import app
from api.auth.middleware import PUBLIC_KEY_REGISTRY
from api.routes.collectives import COLLECTIVES
from api.routes.orders import ORDERS


# --- Fixtures: Test Client ---

@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """
    Provide a FastAPI TestClient with clean state.

    Clears all in-memory storage before each test.
    """
    # Clear state before test
    PUBLIC_KEY_REGISTRY.clear()
    COLLECTIVES.clear()
    ORDERS.clear()

    with TestClient(app) as test_client:
        yield test_client

    # Clean up after test
    PUBLIC_KEY_REGISTRY.clear()
    COLLECTIVES.clear()
    ORDERS.clear()


# --- Fixtures: Ed25519 Keypairs ---

@pytest.fixture
def keypair() -> dict:
    """
    Generate a fresh Ed25519 keypair for testing.

    Returns:
        dict with 'signing_key', 'verify_key', 'public_key_b64', 'private_key_b64'
    """
    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key

    return {
        "signing_key": signing_key,
        "verify_key": verify_key,
        "public_key_b64": base64.b64encode(verify_key.encode()).decode(),
        "private_key_b64": base64.b64encode(signing_key.encode()).decode(),
    }


@pytest.fixture
def keypair_2() -> dict:
    """
    Generate a second keypair for multi-collective testing.
    """
    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key

    return {
        "signing_key": signing_key,
        "verify_key": verify_key,
        "public_key_b64": base64.b64encode(verify_key.encode()).decode(),
        "private_key_b64": base64.b64encode(signing_key.encode()).decode(),
    }


# --- Helper: Request Signing ---

class RequestSigner:
    """
    Helper class for signing Trading Arena API requests.

    Implements the Trading Arena authentication protocol:
    - Signature computed over: {method}|{path}|{timestamp}|{body_hash}
    - 5-minute timestamp window for replay protection
    """

    def __init__(self, collective_id: str, signing_key: SigningKey):
        """
        Initialize signer with collective credentials.

        Args:
            collective_id: The collective's unique identifier
            signing_key: Ed25519 SigningKey for request signing
        """
        self.collective_id = collective_id
        self.signing_key = signing_key
        self._used_nonces: set[str] = set()

    def _compute_body_hash(self, body: Optional[dict]) -> str:
        """Compute SHA256 hash of request body."""
        if body is None:
            return ""
        body_json = json.dumps(body, sort_keys=True)
        return hashlib.sha256(body_json.encode()).hexdigest()

    def _compute_canonical_message(
        self,
        method: str,
        path: str,
        timestamp: str,
        body_hash: str
    ) -> str:
        """Build canonical message for signing."""
        return f"{method}|{path}|{timestamp}|{body_hash}"

    def sign_request(
        self,
        method: str,
        path: str,
        body: Optional[dict] = None,
        timestamp: Optional[str] = None
    ) -> dict:
        """
        Sign a request and return auth headers.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: Request path (e.g., /v1/orders)
            body: Request body dict (for POST/PUT/PATCH)
            timestamp: Optional custom timestamp (for testing expired timestamps)

        Returns:
            dict with X-Collective-ID, X-Timestamp, X-Signature headers
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat()

        body_hash = self._compute_body_hash(body)
        canonical = self._compute_canonical_message(method, path, timestamp, body_hash)

        # Sign the canonical message
        signature = self.signing_key.sign(canonical.encode())
        signature_b64 = base64.b64encode(signature.signature).decode()

        return {
            "X-Collective-ID": self.collective_id,
            "X-Timestamp": timestamp,
            "X-Signature": signature_b64,
        }

    def sign_request_with_wrong_key(
        self,
        method: str,
        path: str,
        body: Optional[dict] = None
    ) -> dict:
        """
        Sign a request with a different (wrong) key for testing invalid signatures.
        """
        wrong_key = SigningKey.generate()
        timestamp = datetime.now(timezone.utc).isoformat()

        body_hash = self._compute_body_hash(body)
        canonical = self._compute_canonical_message(method, path, timestamp, body_hash)

        signature = wrong_key.sign(canonical.encode())
        signature_b64 = base64.b64encode(signature.signature).decode()

        return {
            "X-Collective-ID": self.collective_id,
            "X-Timestamp": timestamp,
            "X-Signature": signature_b64,
        }

    def sign_request_with_expired_timestamp(
        self,
        method: str,
        path: str,
        body: Optional[dict] = None,
        minutes_ago: int = 10
    ) -> dict:
        """
        Sign a request with an expired timestamp for testing timestamp validation.
        """
        expired_time = datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)
        timestamp = expired_time.isoformat()

        body_hash = self._compute_body_hash(body)
        canonical = self._compute_canonical_message(method, path, timestamp, body_hash)

        signature = self.signing_key.sign(canonical.encode())
        signature_b64 = base64.b64encode(signature.signature).decode()

        return {
            "X-Collective-ID": self.collective_id,
            "X-Timestamp": timestamp,
            "X-Signature": signature_b64,
        }

    def sign_request_with_tampered_body(
        self,
        method: str,
        path: str,
        original_body: dict,
        tampered_body: dict
    ) -> tuple[dict, dict]:
        """
        Sign request with original body but return tampered body.

        Returns:
            tuple of (headers, tampered_body) - signature will be invalid
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        # Sign with original body hash
        body_hash = self._compute_body_hash(original_body)
        canonical = self._compute_canonical_message(method, path, timestamp, body_hash)

        signature = self.signing_key.sign(canonical.encode())
        signature_b64 = base64.b64encode(signature.signature).decode()

        headers = {
            "X-Collective-ID": self.collective_id,
            "X-Timestamp": timestamp,
            "X-Signature": signature_b64,
        }

        return headers, tampered_body


@pytest.fixture
def signer(keypair) -> RequestSigner:
    """Create a RequestSigner with the test keypair."""
    return RequestSigner("test-collective", keypair["signing_key"])


# --- Helper: Registered Collective ---

@pytest.fixture
def registered_collective(client: TestClient, keypair) -> dict:
    """
    Register a test collective and return its details.

    Returns:
        dict with collective_id, public_key_b64, signing_key, and registration response
    """
    collective_id = "test-collective"
    registration_data = {
        "collective_id": collective_id,
        "display_name": "Test Collective",
        "public_key": keypair["public_key_b64"],
        "metadata": {
            "version": "1.0.0",
            "agent_count": 5,
            "description": "Test collective for integration tests"
        }
    }

    response = client.post("/v1/collectives/register", json=registration_data)
    assert response.status_code == 201, f"Registration failed: {response.json()}"

    return {
        "collective_id": collective_id,
        "display_name": "Test Collective",
        "public_key_b64": keypair["public_key_b64"],
        "signing_key": keypair["signing_key"],
        "registration_response": response.json()
    }


@pytest.fixture
def registered_collective_2(client: TestClient, keypair_2) -> dict:
    """
    Register a second test collective for multi-collective testing.
    """
    collective_id = "test-collective-2"
    registration_data = {
        "collective_id": collective_id,
        "display_name": "Test Collective 2",
        "public_key": keypair_2["public_key_b64"],
    }

    response = client.post("/v1/collectives/register", json=registration_data)
    assert response.status_code == 201, f"Registration failed: {response.json()}"

    return {
        "collective_id": collective_id,
        "display_name": "Test Collective 2",
        "public_key_b64": keypair_2["public_key_b64"],
        "signing_key": keypair_2["signing_key"],
        "registration_response": response.json()
    }


@pytest.fixture
def auth_signer(registered_collective) -> RequestSigner:
    """
    Create a RequestSigner for a registered collective.
    """
    return RequestSigner(
        registered_collective["collective_id"],
        registered_collective["signing_key"]
    )


# --- Test Data Factories ---

def make_order_data(
    symbol: str = "SOL/USDC",
    side: str = "buy",
    order_type: str = "limit",
    quantity: float = 10.0,
    price: Optional[float] = 100.0,
    client_order_id: Optional[str] = None,
    rationale: Optional[str] = None
) -> dict:
    """
    Factory function to create order request data.
    """
    data = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "time_in_force": "GTC",
    }

    if price is not None:
        data["price"] = price

    if client_order_id is not None:
        data["client_order_id"] = client_order_id

    if rationale is not None:
        data["rationale"] = rationale

    return data


def make_registration_data(
    collective_id: str,
    public_key_b64: str,
    display_name: Optional[str] = None
) -> dict:
    """
    Factory function to create collective registration data.
    """
    return {
        "collective_id": collective_id,
        "display_name": display_name or f"Collective {collective_id}",
        "public_key": public_key_b64,
    }
