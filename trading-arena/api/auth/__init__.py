"""
Authentication Module

Ed25519 signature verification for Trading Arena API.
Integrates with existing WEAVER sign_message.py infrastructure.
"""

# Core crypto functions (no external deps beyond nacl)
from .ed25519 import (
    verify_signature,
    compute_body_hash,
    compute_canonical_message,
    get_public_key_fingerprint
)

# FastAPI middleware (requires fastapi - import when needed)
# from .middleware import require_auth, get_current_collective

__all__ = [
    "verify_signature",
    "compute_body_hash", 
    "compute_canonical_message",
    "get_public_key_fingerprint",
]
