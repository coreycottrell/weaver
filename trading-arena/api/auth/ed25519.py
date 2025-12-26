"""
Ed25519 Signature Verification

Implements the Trading Arena authentication protocol:
- Signature computed over: {method}|{path}|{timestamp}|{body_hash}
- 5-minute timestamp window for replay protection
- Integration with WEAVER's existing Ed25519 infrastructure
"""

import base64
import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Optional

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


# Timestamp validation window (seconds)
TIMESTAMP_WINDOW = 300  # 5 minutes


def compute_body_hash(body: Optional[dict]) -> str:
    """
    Compute SHA256 hash of request body.
    
    Args:
        body: Request body as dict, or None for bodyless requests
        
    Returns:
        Hex-encoded SHA256 hash, or empty string for None body
    """
    if body is None:
        return ""
    body_json = json.dumps(body, sort_keys=True)
    return hashlib.sha256(body_json.encode()).hexdigest()


def compute_canonical_message(
    method: str,
    path: str,
    timestamp: str,
    body_hash: str
) -> str:
    """
    Compute canonical message string for signing/verification.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        path: Request path (e.g., /v1/orders)
        timestamp: ISO format timestamp
        body_hash: SHA256 hash of body (or empty string)
        
    Returns:
        Canonical message string: {method}|{path}|{timestamp}|{body_hash}
    """
    return f"{method}|{path}|{timestamp}|{body_hash}"


def verify_timestamp(timestamp: str) -> bool:
    """
    Verify timestamp is within acceptable window.
    
    Args:
        timestamp: ISO format timestamp string
        
    Returns:
        True if timestamp is valid (within 5-minute window)
    """
    try:
        # Parse timestamp (handle both Z and +00:00 formats)
        ts_str = timestamp.replace('Z', '+00:00')
        ts = datetime.fromisoformat(ts_str)
        
        now = datetime.now(timezone.utc)
        delta = abs((now - ts).total_seconds())
        
        return delta <= TIMESTAMP_WINDOW
    except (ValueError, TypeError):
        return False


def verify_signature(
    public_key_b64: str,
    signature_b64: str,
    method: str,
    path: str,
    timestamp: str,
    body: Optional[dict] = None
) -> bool:
    """
    Verify an Ed25519 request signature.
    
    Args:
        public_key_b64: Base64-encoded public key
        signature_b64: Base64-encoded signature
        method: HTTP method
        path: Request path
        timestamp: ISO format timestamp
        body: Request body dict (or None)
        
    Returns:
        True if signature is valid
        
    Raises:
        ValueError: If timestamp is outside valid window
    """
    # Validate timestamp first
    if not verify_timestamp(timestamp):
        raise ValueError("Timestamp outside valid window")
    
    try:
        # Decode public key and signature
        public_key_bytes = base64.b64decode(public_key_b64)
        signature_bytes = base64.b64decode(signature_b64)
        
        # Compute canonical message
        body_hash = compute_body_hash(body)
        canonical = compute_canonical_message(method, path, timestamp, body_hash)
        
        # Verify signature
        verify_key = VerifyKey(public_key_bytes)
        verify_key.verify(canonical.encode(), signature_bytes)
        
        return True
        
    except (BadSignatureError, ValueError, TypeError):
        return False


def get_public_key_fingerprint(public_key_b64: str) -> str:
    """
    Compute fingerprint of public key (first 8 hex chars of SHA256).
    
    Args:
        public_key_b64: Base64-encoded public key
        
    Returns:
        8-character hex fingerprint
    """
    try:
        public_key_bytes = base64.b64decode(public_key_b64)
        hash_bytes = hashlib.sha256(public_key_bytes).hexdigest()
        return hash_bytes[:8]
    except (ValueError, TypeError):
        return "00000000"
