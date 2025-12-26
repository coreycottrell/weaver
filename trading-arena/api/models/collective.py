"""
Collective Models

Pydantic models for collective registration and management.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CollectiveMetadata(BaseModel):
    """Optional metadata for collective registration."""
    version: Optional[str] = None
    agent_count: Optional[int] = Field(None, ge=1)
    description: Optional[str] = Field(None, max_length=500)


class CollectiveRegistration(BaseModel):
    """Request model for collective registration."""
    collective_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9-]{2,31}$",
        description="Unique collective identifier (lowercase, 3-32 chars)"
    )
    display_name: str = Field(..., min_length=1, max_length=100)
    public_key: str = Field(..., description="Base64-encoded Ed25519 public key")
    metadata: Optional[CollectiveMetadata] = None


class CollectiveResponse(BaseModel):
    """Response model for collective registration."""
    collective_id: str
    display_name: str
    registered_at: datetime
    public_key_fingerprint: str
    status: str
    initial_balance: Optional[dict] = None


class CollectiveListItem(BaseModel):
    """Abbreviated collective info for list responses."""
    collective_id: str
    display_name: str
    status: str
    public_key_fingerprint: str


class CollectiveListResponse(BaseModel):
    """Response model for listing collectives."""
    collectives: list[dict]  # Using dict for flexibility
    total: int
    limit: int
    offset: int
