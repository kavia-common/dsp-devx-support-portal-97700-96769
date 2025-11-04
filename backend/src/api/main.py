from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.core.models import (
    Ticket, TicketCreate, TicketUpdate,
    Comment, CommentCreate,
    KBArticle, KBArticleCreate, KBArticleUpdate
)
from src.core.deps import get_ticket_repo, get_comment_repo, get_kb_repo
from src.core.repository import TicketRepository, CommentRepository, KBRepository

app = FastAPI(
    title="DSP DevX Support Backend",
    description="Backend API for DSP DevX Support Pioneer with in-memory repositories for demo.",
    version="0.1.0",
    openapi_tags=[
        {"name": "health", "description": "Health and diagnostics"},
        {"name": "tickets", "description": "Manage support tickets"},
        {"name": "comments", "description": "Manage ticket comments"},
        {"name": "kb", "description": "Knowledge base articles"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PUBLIC_INTERFACE
@app.get("/", tags=["health"], summary="Health Check")
def health_check():
    """Health check endpoint.
    Returns a simple payload to indicate the service is running.
    """
    return {"message": "Healthy"}


# Tickets Endpoints

# PUBLIC_INTERFACE
@app.get(
    "/tickets",
    response_model=List[Ticket],
    tags=["tickets"],
    summary="List tickets",
    description="Retrieve all tickets. Optional filter by status or tag.",
)
def list_tickets(
    status: Optional[str] = Query(None, description="Optional status filter"),
    tag: Optional[str] = Query(None, description="Optional tag filter"),
    repo: TicketRepository = Depends(get_ticket_repo),
):
    """List all tickets with optional filtering."""
    items = repo.list()
    if status:
        items = [t for t in items if t.status == status]
    if tag:
        items = [t for t in items if tag in (t.tags or [])]
    return items


# PUBLIC_INTERFACE
@app.get(
    "/tickets/{ticket_id}",
    response_model=Ticket,
    tags=["tickets"],
    summary="Get ticket by id",
)
def get_ticket(ticket_id: int, repo: TicketRepository = Depends(get_ticket_repo)):
    """Get a ticket by its identifier."""
    t = repo.get(ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t


# PUBLIC_INTERFACE
@app.post(
    "/tickets",
    response_model=Ticket,
    tags=["tickets"],
    summary="Create ticket",
)
def create_ticket(payload: TicketCreate, repo: TicketRepository = Depends(get_ticket_repo)):
    """Create a new ticket."""
    return repo.create(payload)


# PUBLIC_INTERFACE
@app.patch(
    "/tickets/{ticket_id}",
    response_model=Ticket,
    tags=["tickets"],
    summary="Update ticket",
)
def update_ticket(ticket_id: int, payload: TicketUpdate, repo: TicketRepository = Depends(get_ticket_repo)):
    """Update an existing ticket by id."""
    t = repo.update(ticket_id, payload)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t


# PUBLIC_INTERFACE
@app.delete(
    "/tickets/{ticket_id}",
    tags=["tickets"],
    summary="Delete ticket",
    responses={204: {"description": "Deleted"}},
)
def delete_ticket(ticket_id: int, repo: TicketRepository = Depends(get_ticket_repo)):
    """Delete a ticket by id."""
    ok = repo.delete(ticket_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"status": "deleted"}


# Comments Endpoints

# PUBLIC_INTERFACE
@app.get(
    "/tickets/{ticket_id}/comments",
    response_model=List[Comment],
    tags=["comments"],
    summary="List comments for ticket",
)
def list_comments(ticket_id: int, repo: CommentRepository = Depends(get_comment_repo)):
    """List all comments associated with a ticket."""
    return repo.list_for_ticket(ticket_id)


# PUBLIC_INTERFACE
@app.post(
    "/tickets/{ticket_id}/comments",
    response_model=Comment,
    tags=["comments"],
    summary="Create comment for ticket",
)
def create_comment(ticket_id: int, payload: CommentCreate, repo: CommentRepository = Depends(get_comment_repo)):
    """Create a new comment for a ticket."""
    if payload.ticket_id != ticket_id:
        # Ensure path param and payload match for integrity
        raise HTTPException(status_code=400, detail="ticket_id mismatch between path and payload")
    return repo.create(payload)


# Knowledge Base Endpoints

# PUBLIC_INTERFACE
@app.get(
    "/kb",
    response_model=List[KBArticle],
    tags=["kb"],
    summary="List KB articles",
)
def list_kb(repo: KBRepository = Depends(get_kb_repo)):
    """List all knowledge base articles."""
    return repo.list()


# PUBLIC_INTERFACE
@app.get(
    "/kb/{article_id}",
    response_model=KBArticle,
    tags=["kb"],
    summary="Get KB article by id",
)
def get_kb(article_id: int, repo: KBRepository = Depends(get_kb_repo)):
    """Get a knowledge base article by its identifier."""
    a = repo.get(article_id)
    if not a:
        raise HTTPException(status_code=404, detail="KB article not found")
    return a


# PUBLIC_INTERFACE
@app.post(
    "/kb",
    response_model=KBArticle,
    tags=["kb"],
    summary="Create KB article",
)
def create_kb(payload: KBArticleCreate, repo: KBRepository = Depends(get_kb_repo)):
    """Create a new knowledge base article."""
    return repo.create(payload)


# PUBLIC_INTERFACE
@app.patch(
    "/kb/{article_id}",
    response_model=KBArticle,
    tags=["kb"],
    summary="Update KB article",
)
def update_kb(article_id: int, payload: KBArticleUpdate, repo: KBRepository = Depends(get_kb_repo)):
    """Update an existing knowledge base article."""
    a = repo.update(article_id, payload)
    if not a:
        raise HTTPException(status_code=404, detail="KB article not found")
    return a


# PUBLIC_INTERFACE
@app.delete(
    "/kb/{article_id}",
    tags=["kb"],
    summary="Delete KB article",
    responses={204: {"description": "Deleted"}},
)
def delete_kb(article_id: int, repo: KBRepository = Depends(get_kb_repo)):
    """Delete a knowledge base article by id."""
    ok = repo.delete(article_id)
    if not ok:
        raise HTTPException(status_code=404, detail="KB article not found")
    return {"status": "deleted"}
