"""
Repository interfaces and in-memory implementations.

These repositories are intentionally simple and keep a clean interface to
facilitate swapping the implementation with a real database in the future.
"""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from .models import (
    Ticket, TicketCreate, TicketUpdate,
    Comment, CommentCreate,
    KBArticle, KBArticleCreate, KBArticleUpdate
)


# PUBLIC_INTERFACE
class TicketRepository:
    """This is the abstraction for a Ticket repository."""
    def list(self) -> List[Ticket]:
        """List all tickets."""
        raise NotImplementedError

    def get(self, ticket_id: int) -> Optional[Ticket]:
        """Get a ticket by id."""
        raise NotImplementedError

    def create(self, payload: TicketCreate) -> Ticket:
        """Create a new ticket."""
        raise NotImplementedError

    def update(self, ticket_id: int, payload: TicketUpdate) -> Optional[Ticket]:
        """Update an existing ticket."""
        raise NotImplementedError

    def delete(self, ticket_id: int) -> bool:
        """Delete a ticket by id."""
        raise NotImplementedError


# PUBLIC_INTERFACE
class CommentRepository:
    """This is the abstraction for a Comment repository."""
    def list_for_ticket(self, ticket_id: int) -> List[Comment]:
        """List all comments for a given ticket."""
        raise NotImplementedError

    def create(self, payload: CommentCreate) -> Comment:
        """Create a new comment for a ticket."""
        raise NotImplementedError


# PUBLIC_INTERFACE
class KBRepository:
    """This is the abstraction for a Knowledge Base repository."""
    def list(self) -> List[KBArticle]:
        """List all KB articles."""
        raise NotImplementedError

    def get(self, article_id: int) -> Optional[KBArticle]:
        """Get a KB article by id."""
        raise NotImplementedError

    def create(self, payload: KBArticleCreate) -> KBArticle:
        """Create a new KB article."""
        raise NotImplementedError

    def update(self, article_id: int, payload: KBArticleUpdate) -> Optional[KBArticle]:
        """Update an existing KB article."""
        raise NotImplementedError

    def delete(self, article_id: int) -> bool:
        """Delete a KB article by id."""
        raise NotImplementedError


class InMemoryTicketRepository(TicketRepository):
    """In-memory implementation of TicketRepository."""

    def __init__(self) -> None:
        self._items: Dict[int, Ticket] = {}
        self._next_id: int = 1

    def list(self) -> List[Ticket]:
        return list(self._items.values())

    def get(self, ticket_id: int) -> Optional[Ticket]:
        return self._items.get(ticket_id)

    def create(self, payload: TicketCreate) -> Ticket:
        new = Ticket(
            id=self._next_id,
            title=payload.title,
            description=payload.description,
            status="open",
            created_by=payload.created_by,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            tags=payload.tags or [],
        )
        self._items[self._next_id] = new
        self._next_id += 1
        return new

    def update(self, ticket_id: int, payload: TicketUpdate) -> Optional[Ticket]:
        existing = self._items.get(ticket_id)
        if not existing:
            return None
        data = existing.model_dump()
        if payload.title is not None:
            data["title"] = payload.title
        if payload.description is not None:
            data["description"] = payload.description
        if payload.status is not None:
            data["status"] = payload.status
        if payload.tags is not None:
            data["tags"] = payload.tags
        data["updated_at"] = datetime.utcnow()
        updated = Ticket(**data)
        self._items[ticket_id] = updated
        return updated

    def delete(self, ticket_id: int) -> bool:
        return self._items.pop(ticket_id, None) is not None


class InMemoryCommentRepository(CommentRepository):
    """In-memory implementation of CommentRepository."""

    def __init__(self) -> None:
        self._items: Dict[int, Comment] = {}
        self._by_ticket: Dict[int, List[int]] = {}
        self._next_id: int = 1

    def list_for_ticket(self, ticket_id: int) -> List[Comment]:
        ids = self._by_ticket.get(ticket_id, [])
        return [self._items[i] for i in ids]

    def create(self, payload: CommentCreate) -> Comment:
        new = Comment(
            id=self._next_id,
            ticket_id=payload.ticket_id,
            author=payload.author,
            message=payload.message,
        )
        self._items[self._next_id] = new
        self._by_ticket.setdefault(payload.ticket_id, []).append(self._next_id)
        self._next_id += 1
        return new


class InMemoryKBRepository(KBRepository):
    """In-memory implementation of KBRepository."""

    def __init__(self) -> None:
        self._items: Dict[int, KBArticle] = {}
        self._next_id: int = 1

    def list(self) -> List[KBArticle]:
        return list(self._items.values())

    def get(self, article_id: int) -> Optional[KBArticle]:
        return self._items.get(article_id)

    def create(self, payload: KBArticleCreate) -> KBArticle:
        new = KBArticle(
            id=self._next_id,
            title=payload.title,
            content=payload.content,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            tags=payload.tags or [],
        )
        self._items[self._next_id] = new
        self._next_id += 1
        return new

    def update(self, article_id: int, payload: KBArticleUpdate) -> Optional[KBArticle]:
        existing = self._items.get(article_id)
        if not existing:
            return None
        data = existing.model_dump()
        if payload.title is not None:
            data["title"] = payload.title
        if payload.content is not None:
            data["content"] = payload.content
        if payload.tags is not None:
            data["tags"] = payload.tags
        data["updated_at"] = datetime.utcnow()
        updated = KBArticle(**data)
        self._items[article_id] = updated
        return updated

    def delete(self, article_id: int) -> bool:
        return self._items.pop(article_id, None) is not None
