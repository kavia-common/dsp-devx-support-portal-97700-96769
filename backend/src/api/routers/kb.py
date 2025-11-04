from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from src.core.deps import get_kb_repo
from src.core.models import KBArticle, KBArticleCreate, KBArticleUpdate
from src.core.repository import KBRepository

router = APIRouter()


# PUBLIC_INTERFACE
@router.get(
    "/kb",
    response_model=List[KBArticle],
    tags=["kb"],
    summary="List KB articles",
    description="List all knowledge base articles.",
)
def list_kb(repo: KBRepository = Depends(get_kb_repo)):
    """List all knowledge base articles."""
    return repo.list()


# PUBLIC_INTERFACE
@router.get(
    "/kb/{article_id}",
    response_model=KBArticle,
    tags=["kb"],
    summary="Get KB article by id",
    description="Get a knowledge base article by its identifier.",
)
def get_kb(article_id: int, repo: KBRepository = Depends(get_kb_repo)):
    """Get a knowledge base article by its identifier."""
    a = repo.get(article_id)
    if not a:
        raise HTTPException(status_code=404, detail="KB article not found")
    return a


# PUBLIC_INTERFACE
@router.post(
    "/kb",
    response_model=KBArticle,
    tags=["kb"],
    summary="Create KB article",
    description="Create a new knowledge base article.",
)
def create_kb(payload: KBArticleCreate, repo: KBRepository = Depends(get_kb_repo)):
    """Create a new knowledge base article."""
    return repo.create(payload)


# PUBLIC_INTERFACE
@router.patch(
    "/kb/{article_id}",
    response_model=KBArticle,
    tags=["kb"],
    summary="Update KB article",
    description="Update an existing knowledge base article.",
)
def update_kb(article_id: int, payload: KBArticleUpdate, repo: KBRepository = Depends(get_kb_repo)):
    """Update an existing knowledge base article."""
    a = repo.update(article_id, payload)
    if not a:
        raise HTTPException(status_code=404, detail="KB article not found")
    return a


# PUBLIC_INTERFACE
@router.delete(
    "/kb/{article_id}",
    tags=["kb"],
    summary="Delete KB article",
    description="Delete a knowledge base article by id.",
    responses={204: {"description": "Deleted"}},
)
def delete_kb(article_id: int, repo: KBRepository = Depends(get_kb_repo)):
    """Delete a knowledge base article by id."""
    ok = repo.delete(article_id)
    if not ok:
        raise HTTPException(status_code=404, detail="KB article not found")
    return {"status": "deleted"}


# PUBLIC_INTERFACE
@router.get(
    "/kb/search",
    response_model=List[KBArticle],
    tags=["kb"],
    summary="Search KB articles",
    description="Search KB articles by query across title, content and tags. Supports pagination.",
)
def search_kb(
    q: str = Query(..., description="Search query string"),
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    size: int = Query(50, ge=1, le=200, description="Page size"),
    repo: KBRepository = Depends(get_kb_repo),
):
    """Search KB by term in title, content or tags; returns a paginated list."""
    items = repo.list()
    q_lower = q.lower()
    filtered = [
        a for a in items
        if (q_lower in a.title.lower())
        or (q_lower in a.content.lower())
        or any(q_lower in (tag or "").lower() for tag in (a.tags or []))
    ]
    start = (page - 1) * size
    end = start + size
    return filtered[start:end]
