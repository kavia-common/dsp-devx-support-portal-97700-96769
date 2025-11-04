from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from src.core.deps import get_ticket_repo, get_comment_repo
from src.core.models import (
    Ticket, TicketCreate, TicketUpdate,
    Comment, CommentCreate,
)
from src.core.repository import TicketRepository, CommentRepository

router = APIRouter()


# PUBLIC_INTERFACE
@router.get(
    "/tickets",
    response_model=List[Ticket],
    tags=["tickets"],
    summary="List tickets",
    description="Retrieve all tickets. Optional filter by status or tag. Supports basic pagination via page and size.",
)
def list_tickets(
    status: Optional[str] = Query(None, description="Optional status filter"),
    q: Optional[str] = Query(None, description="Optional search query to match in title or description"),
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    size: int = Query(50, ge=1, le=200, description="Page size"),
    repo: TicketRepository = Depends(get_ticket_repo),
):
    """List all tickets with optional filtering by status and search query, with pagination."""
    items = repo.list()
    if status:
        items = [t for t in items if t.status == status]
    if q:
        q_lower = q.lower()
        items = [t for t in items if q_lower in t.title.lower() or q_lower in t.description.lower()]
    # pagination
    start = (page - 1) * size
    end = start + size
    return items[start:end]


# PUBLIC_INTERFACE
@router.get(
    "/tickets/{ticket_id}",
    response_model=Ticket,
    tags=["tickets"],
    summary="Get ticket by id",
    description="Get a ticket by its identifier.",
)
def get_ticket(ticket_id: int, repo: TicketRepository = Depends(get_ticket_repo)):
    """Get a ticket by its identifier."""
    t = repo.get(ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t


# PUBLIC_INTERFACE
@router.post(
    "/tickets",
    response_model=Ticket,
    tags=["tickets"],
    summary="Create ticket",
    description="Create a new ticket.",
)
def create_ticket(payload: TicketCreate, repo: TicketRepository = Depends(get_ticket_repo)):
    """Create a new ticket."""
    return repo.create(payload)


# PUBLIC_INTERFACE
@router.patch(
    "/tickets/{ticket_id}",
    response_model=Ticket,
    tags=["tickets"],
    summary="Update ticket",
    description="Update an existing ticket by id.",
)
def update_ticket(ticket_id: int, payload: TicketUpdate, repo: TicketRepository = Depends(get_ticket_repo)):
    """Update an existing ticket by id."""
    t = repo.update(ticket_id, payload)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t


# PUBLIC_INTERFACE
@router.delete(
    "/tickets/{ticket_id}",
    tags=["tickets"],
    summary="Delete ticket",
    description="Delete a ticket by id.",
    responses={204: {"description": "Deleted"}},
)
def delete_ticket(ticket_id: int, repo: TicketRepository = Depends(get_ticket_repo)):
    """Delete a ticket by id."""
    ok = repo.delete(ticket_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"status": "deleted"}


# PUBLIC_INTERFACE
@router.get(
    "/tickets/{ticket_id}/comments",
    response_model=List[Comment],
    tags=["comments"],
    summary="List comments for ticket",
    description="List all comments associated with a ticket.",
)
def list_comments(ticket_id: int, repo: CommentRepository = Depends(get_comment_repo)):
    """List all comments associated with a ticket."""
    return repo.list_for_ticket(ticket_id)


# PUBLIC_INTERFACE
@router.post(
    "/tickets/{ticket_id}/comments",
    response_model=Comment,
    tags=["comments"],
    summary="Create comment for ticket",
    description="Create a new comment for a ticket.",
)
def create_comment(ticket_id: int, payload: CommentCreate, repo: CommentRepository = Depends(get_comment_repo)):
    """Create a new comment for a ticket. Ensures path and payload ticket_id match."""
    if payload.ticket_id != ticket_id:
        # Ensure path param and payload match for integrity
        raise HTTPException(status_code=400, detail="ticket_id mismatch between path and payload")
    return repo.create(payload)
