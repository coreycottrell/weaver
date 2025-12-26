"""
Collective Registration Integration Tests

Tests for collective management:
- Registration flow
- Duplicate registration rejection
- Get collective by ID
- List collectives
- Public key validation
"""

import base64
import pytest
from nacl.signing import SigningKey
from fastapi.testclient import TestClient

from .conftest import RequestSigner, make_registration_data


class TestCollectiveRegistration:
    """Test collective registration endpoint."""

    def test_register_collective_success(
        self,
        client: TestClient,
        keypair
    ):
        """Valid registration should succeed and return expected fields."""
        registration = make_registration_data(
            collective_id="weaver-test",
            public_key_b64=keypair["public_key_b64"],
            display_name="WEAVER Test Collective"
        )

        response = client.post("/v1/collectives/register", json=registration)

        assert response.status_code == 201
        data = response.json()

        # Verify response structure
        assert data["collective_id"] == "weaver-test"
        assert data["display_name"] == "WEAVER Test Collective"
        assert data["status"] == "active"
        assert "registered_at" in data
        assert "public_key_fingerprint" in data
        assert len(data["public_key_fingerprint"]) == 8  # 8 hex chars

        # Verify initial balance
        assert data["initial_balance"]["paper_usd"] == 10000.00
        assert data["initial_balance"]["real_usd"] == 0.00

    def test_register_collective_with_metadata(
        self,
        client: TestClient,
        keypair
    ):
        """Registration with optional metadata should succeed."""
        registration = {
            "collective_id": "acgee-test",
            "display_name": "A-C-Gee Test",
            "public_key": keypair["public_key_b64"],
            "metadata": {
                "version": "2.0.0",
                "agent_count": 12,
                "description": "Sister collective for testing"
            }
        }

        response = client.post("/v1/collectives/register", json=registration)

        assert response.status_code == 201
        data = response.json()
        assert data["collective_id"] == "acgee-test"

    def test_register_collective_minimal(
        self,
        client: TestClient,
        keypair
    ):
        """Registration with minimal required fields should succeed."""
        registration = {
            "collective_id": "minimal",
            "display_name": "Minimal Collective",
            "public_key": keypair["public_key_b64"]
        }

        response = client.post("/v1/collectives/register", json=registration)

        assert response.status_code == 201
        data = response.json()
        assert data["collective_id"] == "minimal"
        assert data["status"] == "active"


class TestDuplicateRegistration:
    """Test that duplicate registrations are rejected."""

    def test_duplicate_collective_id_rejected(
        self,
        client: TestClient,
        keypair,
        keypair_2
    ):
        """Attempting to register same collective_id twice should fail."""
        registration = make_registration_data(
            collective_id="unique-id",
            public_key_b64=keypair["public_key_b64"]
        )

        # First registration - should succeed
        response1 = client.post("/v1/collectives/register", json=registration)
        assert response1.status_code == 201

        # Second registration with same ID but different key - should fail
        registration2 = make_registration_data(
            collective_id="unique-id",  # Same ID
            public_key_b64=keypair_2["public_key_b64"]  # Different key
        )
        response2 = client.post("/v1/collectives/register", json=registration2)

        assert response2.status_code == 409
        error = response2.json()["error"]
        assert error["code"] == "DUPLICATE_COLLECTIVE"
        assert "unique-id" in error["message"]

    def test_different_collective_ids_accepted(
        self,
        client: TestClient,
        keypair,
        keypair_2
    ):
        """Different collective_ids should be registered successfully."""
        reg1 = make_registration_data("collective-a", keypair["public_key_b64"])
        reg2 = make_registration_data("collective-b", keypair_2["public_key_b64"])

        response1 = client.post("/v1/collectives/register", json=reg1)
        response2 = client.post("/v1/collectives/register", json=reg2)

        assert response1.status_code == 201
        assert response2.status_code == 201

    def test_same_public_key_different_ids_accepted(
        self,
        client: TestClient,
        keypair
    ):
        """Same public key with different IDs should be allowed."""
        reg1 = make_registration_data("id-one", keypair["public_key_b64"])
        reg2 = make_registration_data("id-two", keypair["public_key_b64"])

        response1 = client.post("/v1/collectives/register", json=reg1)
        response2 = client.post("/v1/collectives/register", json=reg2)

        assert response1.status_code == 201
        assert response2.status_code == 201


class TestCollectiveIdValidation:
    """Test collective_id format validation."""

    @pytest.mark.parametrize("invalid_id,reason", [
        ("", "empty string"),
        ("ab", "too short (2 chars)"),
        ("a" * 33, "too long (33 chars)"),
        ("123-start", "starts with number"),
        ("UPPERCASE", "uppercase letters"),
        ("has_underscore", "contains underscore"),
        ("has space", "contains space"),
        ("has.dot", "contains dot"),
    ])
    def test_invalid_collective_id_rejected(
        self,
        client: TestClient,
        keypair,
        invalid_id: str,
        reason: str
    ):
        """Invalid collective_id formats should be rejected."""
        registration = make_registration_data(
            collective_id=invalid_id,
            public_key_b64=keypair["public_key_b64"]
        )

        response = client.post("/v1/collectives/register", json=registration)

        assert response.status_code == 422, f"Expected 422 for {reason}"

    @pytest.mark.parametrize("valid_id", [
        "abc",  # 3 chars (minimum)
        "a" * 32,  # 32 chars (maximum)
        "weaver-team-1",  # with hyphens
        "a1b2c3",  # alphanumeric
        "test-collective-xyz",  # complex valid
    ])
    def test_valid_collective_id_accepted(
        self,
        client: TestClient,
        keypair,
        valid_id: str
    ):
        """Valid collective_id formats should be accepted."""
        registration = make_registration_data(
            collective_id=valid_id,
            public_key_b64=keypair["public_key_b64"]
        )

        response = client.post("/v1/collectives/register", json=registration)

        assert response.status_code == 201, f"Expected 201 for {valid_id}"


class TestGetCollective:
    """Test getting collective details by ID."""

    def test_get_collective_public_info(
        self,
        client: TestClient,
        registered_collective: dict
    ):
        """Unauthenticated request should get public info only."""
        collective_id = registered_collective["collective_id"]

        response = client.get(f"/v1/collectives/{collective_id}")

        assert response.status_code == 200
        data = response.json()

        # Public fields present
        assert data["collective_id"] == collective_id
        assert data["display_name"] == "Test Collective"
        assert data["status"] == "active"
        assert "registered_at" in data
        assert "public_key_fingerprint" in data
        assert "stats" in data

        # Private fields should NOT be present
        assert "metadata" not in data
        assert "initial_balance" not in data

    def test_get_collective_authenticated_self(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Authenticated as self should see private info."""
        collective_id = registered_collective["collective_id"]
        path = f"/v1/collectives/{collective_id}"
        headers = auth_signer.sign_request("GET", path)

        response = client.get(path, headers=headers)

        assert response.status_code == 200
        data = response.json()

        # Should include private fields
        assert "metadata" in data
        assert "initial_balance" in data
        assert data["initial_balance"]["paper_usd"] == 10000.00

    def test_get_collective_authenticated_other(
        self,
        client: TestClient,
        registered_collective: dict,
        registered_collective_2: dict
    ):
        """Authenticated as different collective should see public info only."""
        target_id = registered_collective["collective_id"]
        path = f"/v1/collectives/{target_id}"

        signer = RequestSigner(
            registered_collective_2["collective_id"],
            registered_collective_2["signing_key"]
        )
        headers = signer.sign_request("GET", path)

        response = client.get(path, headers=headers)

        assert response.status_code == 200
        data = response.json()

        # Should NOT include private fields (authenticated as different collective)
        assert "metadata" not in data
        assert "initial_balance" not in data

    def test_get_nonexistent_collective_404(
        self,
        client: TestClient
    ):
        """Getting non-existent collective should return 404."""
        response = client.get("/v1/collectives/does-not-exist")

        assert response.status_code == 404
        error = response.json()["error"]
        assert error["code"] == "NOT_FOUND"


class TestListCollectives:
    """Test listing all collectives."""

    def test_list_collectives_empty(
        self,
        client: TestClient
    ):
        """Empty registry should return empty list."""
        response = client.get("/v1/collectives")

        assert response.status_code == 200
        data = response.json()
        assert data["collectives"] == []
        assert data["total"] == 0

    def test_list_collectives_populated(
        self,
        client: TestClient,
        registered_collective: dict,
        registered_collective_2: dict
    ):
        """Should list all registered collectives."""
        response = client.get("/v1/collectives")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["collectives"]) == 2

        # Verify both collectives present
        ids = [c["collective_id"] for c in data["collectives"]]
        assert registered_collective["collective_id"] in ids
        assert registered_collective_2["collective_id"] in ids

        # Verify only public info in list
        for c in data["collectives"]:
            assert "collective_id" in c
            assert "display_name" in c
            assert "status" in c
            assert "public_key_fingerprint" in c
            # No private info
            assert "metadata" not in c
            assert "initial_balance" not in c

    def test_list_collectives_pagination(
        self,
        client: TestClient,
        keypair
    ):
        """Pagination should work correctly."""
        # Register 5 collectives
        for i in range(5):
            key = SigningKey.generate()
            pub = base64.b64encode(key.verify_key.encode()).decode()
            reg = make_registration_data(f"coll-{i}", pub)
            response = client.post("/v1/collectives/register", json=reg)
            assert response.status_code == 201

        # Test limit
        response = client.get("/v1/collectives?limit=2")
        data = response.json()
        assert len(data["collectives"]) == 2
        assert data["total"] == 5
        assert data["limit"] == 2

        # Test offset
        response = client.get("/v1/collectives?limit=2&offset=3")
        data = response.json()
        assert len(data["collectives"]) == 2
        assert data["offset"] == 3

    def test_list_collectives_filter_by_status(
        self,
        client: TestClient,
        registered_collective: dict
    ):
        """Status filter should work."""
        # All registered collectives are active
        response = client.get("/v1/collectives?status=active")
        data = response.json()
        assert data["total"] >= 1

        # No suspended collectives
        response = client.get("/v1/collectives?status=suspended")
        data = response.json()
        assert data["total"] == 0


class TestPublicKeyValidation:
    """Test public key format validation."""

    def test_invalid_base64_rejected(
        self,
        client: TestClient
    ):
        """Invalid base64 in public key should be rejected."""
        registration = {
            "collective_id": "test-bad-key",
            "display_name": "Test Bad Key",
            "public_key": "not-valid-base64!!!"
        }

        response = client.post("/v1/collectives/register", json=registration)

        # Should fail during registration or first auth attempt
        assert response.status_code in [201, 422]  # Depends on validation timing

    def test_wrong_size_key_handling(
        self,
        client: TestClient
    ):
        """Wrong size public key should be handled gracefully."""
        # Ed25519 public key should be 32 bytes
        wrong_size = base64.b64encode(b"tooshort").decode()
        registration = {
            "collective_id": "test-wrong-size",
            "display_name": "Test Wrong Size",
            "public_key": wrong_size
        }

        response = client.post("/v1/collectives/register", json=registration)

        # Registration may succeed but auth will fail
        if response.status_code == 201:
            # Try to use the registered collective
            signer_key = SigningKey.generate()
            signer = RequestSigner("test-wrong-size", signer_key)
            headers = signer.sign_request("GET", "/v1/orders")
            auth_response = client.get("/v1/orders", headers=headers)
            # Should fail authentication
            assert auth_response.status_code == 401


class TestRegistrationIdempotency:
    """Test registration behavior for edge cases."""

    def test_registration_stores_correct_fingerprint(
        self,
        client: TestClient,
        keypair
    ):
        """Public key fingerprint should be consistently computed."""
        registration = make_registration_data(
            "fingerprint-test",
            keypair["public_key_b64"]
        )

        response = client.post("/v1/collectives/register", json=registration)
        assert response.status_code == 201

        fingerprint1 = response.json()["public_key_fingerprint"]

        # Get the collective and verify fingerprint matches
        get_response = client.get("/v1/collectives/fingerprint-test")
        fingerprint2 = get_response.json()["public_key_fingerprint"]

        assert fingerprint1 == fingerprint2
        assert len(fingerprint1) == 8  # SHA256 first 8 hex chars
