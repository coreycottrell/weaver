"""
Audit Log Endpoints

GET /v1/audit - Retrieve audit log entries
"""

from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, Query

from ..auth.middleware import require_auth

router = APIRouter()

# In-memory storage (TODO: Replace with database)
AUDIT_LOGS: list[dict] = []


def create_audit_entry(
    collective_id: str,
    event_type: str,
    resource_type: str,
    resource_id: str,
    action: str,
    details: dict,
    result: str = "success"
) -> dict:
    """Create and store an audit log entry."""
    import uuid
    entry = {
        "audit_id": f"audit-{uuid.uuid4().hex[:12]}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "collective_id": collective_id,
        "event_type": event_type,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "action": action,
        "details": details,
        "result": result
    }
    AUDIT_LOGS.append(entry)
    return entry


@router.get("")
async def get_audit_logs(
    collective_id: str = Depends(require_auth),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    resource_type: Optional[str] = Query(None, description="Filter by resource type"),
    resource_id: Optional[str] = Query(None, description="Filter by resource ID"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
) -> dict:
    """
    Retrieve audit log entries.
    
    Returns entries for the authenticated collective only.
    """
    # Filter for this collective
    entries = [e for e in AUDIT_LOGS if e["collective_id"] == collective_id]
    
    # Apply filters
    if event_type:
        entries = [e for e in entries if e["event_type"] == event_type]
    if resource_type:
        entries = [e for e in entries if e["resource_type"] == resource_type]
    if resource_id:
        entries = [e for e in entries if e["resource_id"] == resource_id]
    
    # Sort by timestamp descending
    entries.sort(key=lambda x: x["timestamp"], reverse=True)
    
    total = len(entries)
    entries = entries[offset:offset + limit]
    
    return {
        "audit_entries": entries,
        "total": total,
        "limit": limit,
        "offset": offset
    }
