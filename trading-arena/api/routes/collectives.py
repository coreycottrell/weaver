"""
Collective Registration Endpoints

POST /v1/collectives/register - Register new collective
GET  /v1/collectives/{collective_id} - Get collective details
GET  /v1/collectives - List all collectives
"""

from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query

from ..models.collective import (
    CollectiveRegistration,
    CollectiveResponse,
    CollectiveListResponse
)
from ..auth.middleware import get_current_collective, register_public_key
from ..auth.ed25519 import get_public_key_fingerprint

router = APIRouter()

# In-memory storage (TODO: Replace with database)
COLLECTIVES: dict[str, dict] = {}


@router.post("/register", status_code=201)
async def register_collective(registration: CollectiveRegistration) -> CollectiveResponse:
    """
    Register a new collective to participate in Trading Arena.
    
    No authentication required - public key provided in request.
    """
    # Check for duplicate
    if registration.collective_id in COLLECTIVES:
        raise HTTPException(
            status_code=409,
            detail={
                "error": {
                    "code": "DUPLICATE_COLLECTIVE",
                    "message": f"Collective '{registration.collective_id}' already registered"
                }
            }
        )
    
    # Compute public key fingerprint
    fingerprint = get_public_key_fingerprint(registration.public_key)
    
    now = datetime.now(timezone.utc)
    
    # Store collective
    collective_data = {
        "collective_id": registration.collective_id,
        "display_name": registration.display_name,
        "public_key": registration.public_key,
        "public_key_fingerprint": fingerprint,
        "status": "active",
        "metadata": registration.metadata.model_dump() if registration.metadata else {},
        "registered_at": now.isoformat(),
        "initial_balance": {
            "paper_usd": 10000.00,
            "real_usd": 0.00
        }
    }
    COLLECTIVES[registration.collective_id] = collective_data
    
    # Register public key for authentication
    register_public_key(registration.collective_id, registration.public_key)
    
    return CollectiveResponse(
        collective_id=registration.collective_id,
        display_name=registration.display_name,
        registered_at=now,
        public_key_fingerprint=fingerprint,
        status="active",
        initial_balance=collective_data["initial_balance"]
    )


@router.get("/{collective_id}")
async def get_collective(
    collective_id: str,
    current_collective: Optional[str] = Depends(get_current_collective)
) -> dict:
    """
    Get collective registration details.
    
    Optional authentication - more details if authenticated as self.
    """
    if collective_id not in COLLECTIVES:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Collective '{collective_id}' not found"
                }
            }
        )
    
    collective = COLLECTIVES[collective_id]
    
    # Base response (public info)
    response = {
        "collective_id": collective["collective_id"],
        "display_name": collective["display_name"],
        "registered_at": collective["registered_at"],
        "public_key_fingerprint": collective["public_key_fingerprint"],
        "status": collective["status"],
        "stats": {
            "total_trades": 0,  # TODO: Calculate from orders
            "member_since_days": 0  # TODO: Calculate
        }
    }
    
    # Add private info if authenticated as self
    if current_collective == collective_id:
        response["metadata"] = collective.get("metadata", {})
        response["initial_balance"] = collective.get("initial_balance", {})
    
    return response


@router.get("")
async def list_collectives(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
) -> CollectiveListResponse:
    """
    List all registered collectives (public endpoint).
    """
    # Filter by status if provided
    collectives = list(COLLECTIVES.values())
    if status and status != "all":
        collectives = [c for c in collectives if c["status"] == status]
    
    total = len(collectives)
    
    # Apply pagination
    collectives = collectives[offset:offset + limit]
    
    return CollectiveListResponse(
        collectives=[
            {
                "collective_id": c["collective_id"],
                "display_name": c["display_name"],
                "status": c["status"],
                "public_key_fingerprint": c["public_key_fingerprint"]
            }
            for c in collectives
        ],
        total=total,
        limit=limit,
        offset=offset
    )
