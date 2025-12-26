"""
Authentication Middleware

FastAPI dependency for Ed25519 signature verification.
"""

from typing import Optional
from fastapi import Request, HTTPException, Depends
from fastapi.security import APIKeyHeader

from .ed25519 import verify_signature


# Custom header scheme for collective authentication
collective_id_header = APIKeyHeader(name="X-Collective-ID", auto_error=False)
timestamp_header = APIKeyHeader(name="X-Timestamp", auto_error=False)
signature_header = APIKeyHeader(name="X-Signature", auto_error=False)


# In-memory public key registry (TODO: Replace with database)
PUBLIC_KEY_REGISTRY: dict[str, str] = {}


def register_public_key(collective_id: str, public_key_b64: str) -> None:
    """Register a collective's public key."""
    PUBLIC_KEY_REGISTRY[collective_id] = public_key_b64


def get_public_key(collective_id: str) -> Optional[str]:
    """Get a collective's registered public key."""
    return PUBLIC_KEY_REGISTRY.get(collective_id)


async def get_current_collective(
    request: Request,
    collective_id: Optional[str] = Depends(collective_id_header),
    timestamp: Optional[str] = Depends(timestamp_header),
    signature: Optional[str] = Depends(signature_header),
) -> Optional[str]:
    """
    Extract and validate collective identity from request.
    Returns None if not authenticated (for optional auth endpoints).
    """
    if not all([collective_id, timestamp, signature]):
        return None
    
    # Get registered public key
    public_key = get_public_key(collective_id)
    if not public_key:
        return None
    
    # Get request body for signature verification
    body = None
    if request.method in ("POST", "PUT", "PATCH"):
        try:
            body = await request.json()
        except Exception:
            body = None
    
    # Verify signature
    try:
        if verify_signature(
            public_key_b64=public_key,
            signature_b64=signature,
            method=request.method,
            path=request.url.path,
            timestamp=timestamp,
            body=body
        ):
            return collective_id
    except ValueError:
        # Timestamp validation failed
        pass
    
    return None


async def require_auth(
    collective_id: Optional[str] = Depends(get_current_collective),
) -> str:
    """
    Require valid authentication.
    Use as dependency for protected endpoints.
    """
    if not collective_id:
        raise HTTPException(
            status_code=401,
            detail={
                "error": {
                    "code": "INVALID_SIGNATURE",
                    "message": "Authentication required. Provide valid X-Collective-ID, X-Timestamp, and X-Signature headers."
                }
            }
        )
    return collective_id
