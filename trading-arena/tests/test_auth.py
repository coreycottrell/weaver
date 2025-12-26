"""
Authentication Integration Tests

Tests for Ed25519 signature verification:
- Valid signature acceptance
- Invalid signature rejection
- Expired timestamp rejection
- Replay (nonce reuse) detection
- Tampered body detection
"""

import base64
from datetime import datetime, timedelta, timezone

import pytest
from nacl.signing import SigningKey
from fastapi.testclient import TestClient

from .conftest import RequestSigner, make_order_data


class TestValidSignature:
    """Test that valid Ed25519 signatures are accepted."""

    def test_valid_signature_accepted_for_get(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Valid signature on GET request should be accepted."""
        path = f"/v1/collectives/{registered_collective['collective_id']}"
        headers = auth_signer.sign_request("GET", path)

        response = client.get(path, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["collective_id"] == registered_collective["collective_id"]
        # Authenticated as self - should see private info
        assert "metadata" in data
        assert "initial_balance" in data

    def test_valid_signature_accepted_for_post(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Valid signature on POST request should be accepted."""
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 201
        data = response.json()
        assert data["collective_id"] == registered_collective["collective_id"]
        assert data["symbol"] == "SOL/USDC"
        assert data["side"] == "buy"
        assert data["status"] == "open"

    def test_valid_signature_accepted_for_delete(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Valid signature on DELETE request should be accepted."""
        # First create an order
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request("POST", path, body=body)
        response = client.post(path, json=body, headers=headers)
        assert response.status_code == 201
        order_id = response.json()["order_id"]

        # Now cancel it
        delete_path = f"/v1/orders/{order_id}"
        delete_headers = auth_signer.sign_request("DELETE", delete_path)

        response = client.delete(delete_path, headers=delete_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["order_id"] == order_id
        assert data["status"] == "cancelled"


class TestInvalidSignature:
    """Test that invalid signatures are rejected with 401."""

    def test_wrong_key_signature_rejected(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Signature from wrong key should be rejected."""
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request_with_wrong_key("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 401
        error = response.json()["error"]
        assert error["code"] == "INVALID_SIGNATURE"

    def test_tampered_body_rejected(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Request with tampered body should be rejected."""
        path = "/v1/orders"
        original_body = make_order_data(quantity=10.0)
        tampered_body = make_order_data(quantity=1000.0)  # Attacker tries to change quantity

        headers, _ = auth_signer.sign_request_with_tampered_body(
            "POST", path, original_body, tampered_body
        )

        response = client.post(path, json=tampered_body, headers=headers)

        assert response.status_code == 401
        error = response.json()["error"]
        assert error["code"] == "INVALID_SIGNATURE"

    def test_missing_signature_header_rejected(
        self,
        client: TestClient,
        registered_collective: dict
    ):
        """Request missing X-Signature header should be rejected."""
        path = "/v1/orders"
        body = make_order_data()

        headers = {
            "X-Collective-ID": registered_collective["collective_id"],
            "X-Timestamp": datetime.now(timezone.utc).isoformat(),
            # X-Signature intentionally missing
        }

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 401

    def test_missing_collective_id_rejected(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Request missing X-Collective-ID header should be rejected."""
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request("POST", path, body=body)
        del headers["X-Collective-ID"]

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 401

    def test_missing_timestamp_rejected(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Request missing X-Timestamp header should be rejected."""
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request("POST", path, body=body)
        del headers["X-Timestamp"]

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 401

    def test_unregistered_collective_rejected(
        self,
        client: TestClient,
        keypair
    ):
        """Request from unregistered collective should be rejected."""
        # Create signer for unregistered collective
        signer = RequestSigner("unregistered-collective", keypair["signing_key"])

        path = "/v1/orders"
        body = make_order_data()
        headers = signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 401

    def test_corrupted_signature_rejected(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Request with corrupted signature bytes should be rejected."""
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request("POST", path, body=body)

        # Corrupt the signature
        sig_bytes = base64.b64decode(headers["X-Signature"])
        corrupted = bytes([b ^ 0xFF for b in sig_bytes[:8]]) + sig_bytes[8:]
        headers["X-Signature"] = base64.b64encode(corrupted).decode()

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 401


class TestExpiredTimestamp:
    """Test that expired timestamps are rejected."""

    def test_expired_timestamp_rejected_10_minutes(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Timestamp 10 minutes in past should be rejected."""
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request_with_expired_timestamp(
            "POST", path, body=body, minutes_ago=10
        )

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 401

    def test_expired_timestamp_rejected_6_minutes(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Timestamp 6 minutes in past should be rejected (outside 5-min window)."""
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request_with_expired_timestamp(
            "POST", path, body=body, minutes_ago=6
        )

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 401

    def test_timestamp_within_window_accepted(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Timestamp 4 minutes in past should be accepted (within 5-min window)."""
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request_with_expired_timestamp(
            "POST", path, body=body, minutes_ago=4
        )

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 201

    def test_future_timestamp_within_window_accepted(
        self,
        client: TestClient,
        registered_collective: dict
    ):
        """Timestamp 2 minutes in future should be accepted (within 5-min window)."""
        signer = RequestSigner(
            registered_collective["collective_id"],
            registered_collective["signing_key"]
        )

        future_time = datetime.now(timezone.utc) + timedelta(minutes=2)
        timestamp = future_time.isoformat()

        path = "/v1/orders"
        body = make_order_data()
        headers = signer.sign_request("POST", path, body=body, timestamp=timestamp)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 201

    def test_future_timestamp_outside_window_rejected(
        self,
        client: TestClient,
        registered_collective: dict
    ):
        """Timestamp 10 minutes in future should be rejected."""
        signer = RequestSigner(
            registered_collective["collective_id"],
            registered_collective["signing_key"]
        )

        future_time = datetime.now(timezone.utc) + timedelta(minutes=10)
        timestamp = future_time.isoformat()

        path = "/v1/orders"
        body = make_order_data()
        headers = signer.sign_request("POST", path, body=body, timestamp=timestamp)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 401

    def test_malformed_timestamp_rejected(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Malformed timestamp string should be rejected."""
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request("POST", path, body=body)
        headers["X-Timestamp"] = "not-a-valid-timestamp"

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 401


class TestReplayProtection:
    """Test that replay attacks are detected via client_order_id deduplication."""

    def test_duplicate_client_order_id_rejected(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Replay with same client_order_id should be rejected."""
        path = "/v1/orders"
        client_order_id = "unique-order-12345"
        body = make_order_data(client_order_id=client_order_id)

        # First request - should succeed
        headers1 = auth_signer.sign_request("POST", path, body=body)
        response1 = client.post(path, json=body, headers=headers1)
        assert response1.status_code == 201

        # Replay attempt with same client_order_id
        headers2 = auth_signer.sign_request("POST", path, body=body)
        response2 = client.post(path, json=body, headers=headers2)

        assert response2.status_code == 409
        error = response2.json()["error"]
        assert error["code"] == "DUPLICATE_ORDER"

    def test_different_client_order_ids_accepted(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Different client_order_ids should be accepted."""
        path = "/v1/orders"

        # First order
        body1 = make_order_data(client_order_id="order-001")
        headers1 = auth_signer.sign_request("POST", path, body=body1)
        response1 = client.post(path, json=body1, headers=headers1)
        assert response1.status_code == 201

        # Second order with different ID
        body2 = make_order_data(client_order_id="order-002")
        headers2 = auth_signer.sign_request("POST", path, body=body2)
        response2 = client.post(path, json=body2, headers=headers2)
        assert response2.status_code == 201

        # Verify they created different orders
        assert response1.json()["order_id"] != response2.json()["order_id"]

    def test_orders_without_client_order_id_not_deduplicated(
        self,
        client: TestClient,
        registered_collective: dict,
        auth_signer: RequestSigner
    ):
        """Orders without client_order_id should not be deduplicated."""
        path = "/v1/orders"
        body = make_order_data()  # No client_order_id

        # First order
        headers1 = auth_signer.sign_request("POST", path, body=body)
        response1 = client.post(path, json=body, headers=headers1)
        assert response1.status_code == 201

        # Second identical order - should also succeed
        headers2 = auth_signer.sign_request("POST", path, body=body)
        response2 = client.post(path, json=body, headers=headers2)
        assert response2.status_code == 201

        # They should have different order IDs
        assert response1.json()["order_id"] != response2.json()["order_id"]


class TestCrossCollectiveSecurity:
    """Test that collectives cannot impersonate each other."""

    def test_collective_cannot_access_other_orders(
        self,
        client: TestClient,
        registered_collective: dict,
        registered_collective_2: dict,
        auth_signer: RequestSigner
    ):
        """Collective cannot access orders from another collective."""
        # Create order as collective 1
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request("POST", path, body=body)
        response = client.post(path, json=body, headers=headers)
        assert response.status_code == 201
        order_id = response.json()["order_id"]

        # Try to access as collective 2
        signer_2 = RequestSigner(
            registered_collective_2["collective_id"],
            registered_collective_2["signing_key"]
        )
        get_path = f"/v1/orders/{order_id}"
        headers_2 = signer_2.sign_request("GET", get_path)

        response = client.get(get_path, headers=headers_2)

        # Should return 404 (not 403) to avoid information leakage
        assert response.status_code == 404

    def test_collective_cannot_cancel_other_orders(
        self,
        client: TestClient,
        registered_collective: dict,
        registered_collective_2: dict,
        auth_signer: RequestSigner
    ):
        """Collective cannot cancel orders from another collective."""
        # Create order as collective 1
        path = "/v1/orders"
        body = make_order_data()
        headers = auth_signer.sign_request("POST", path, body=body)
        response = client.post(path, json=body, headers=headers)
        assert response.status_code == 201
        order_id = response.json()["order_id"]

        # Try to cancel as collective 2
        signer_2 = RequestSigner(
            registered_collective_2["collective_id"],
            registered_collective_2["signing_key"]
        )
        delete_path = f"/v1/orders/{order_id}"
        headers_2 = signer_2.sign_request("DELETE", delete_path)

        response = client.delete(delete_path, headers=headers_2)

        # Should return 404 (not 403) to avoid information leakage
        assert response.status_code == 404

    def test_collective_cannot_use_others_public_key(
        self,
        client: TestClient,
        registered_collective: dict,
        keypair_2
    ):
        """Signing with collective 1's ID but collective 2's key should fail."""
        # Create signer with collective 1's ID but collective 2's key
        signer = RequestSigner(
            registered_collective["collective_id"],  # collective 1's ID
            keypair_2["signing_key"]  # collective 2's key (not registered for collective 1)
        )

        path = "/v1/orders"
        body = make_order_data()
        headers = signer.sign_request("POST", path, body=body)

        response = client.post(path, json=body, headers=headers)

        assert response.status_code == 401
