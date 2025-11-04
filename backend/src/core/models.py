"""
Core domain models for the DSP DevX Support backend.

These Pydantic models define the API-facing schemas and internal entities
for tickets, comments, and knowledge base (KB) articles. They are designed
to keep interfaces clean for a future database swap (e.g., swapping the
in-memory repo with a real DB repository).
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class Comment(BaseModel):
    """A comment associated with a ticket."""
    id: int = Field(..., description="Unique identifier of the comment")
    ticket_id: int = Field(..., description="Identifier of the ticket this comment belongs to")
    author: str = Field(..., description="Author of the comment")
    message: str = Field(..., description="Comment message body")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="UTC creation timestamp")


# PUBLIC_INTERFACE
class CommentCreate(BaseModel):
    """Payload for creating a new comment."""
    ticket_id: int = Field(..., description="Identifier of the ticket this comment belongs to")
    author: str = Field(..., description="Author of the comment")
    message: str = Field(..., description="Comment message body")


# PUBLIC_INTERFACE
class Ticket(BaseModel):
    """A support ticket raised by a user."""
    id: int = Field(..., description="Unique identifier of the ticket")
    title: str = Field(..., description="Title of the ticket")
    description: str = Field(..., description="Detailed description of the issue")
    status: str = Field("open", description="Status of the ticket (e.g., open, in_progress, closed)")
    created_by: str = Field(..., description="Username or ID of the ticket creator")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="UTC creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="UTC last update timestamp")
    tags: List[str] = Field(default_factory=list, description="Tags associated with the ticket")


# PUBLIC_INTERFACE
class TicketCreate(BaseModel):
    """Payload for creating a new support ticket."""
    title: str = Field(..., description="Title of the ticket")
    description: str = Field(..., description="Detailed description of the issue")
    created_by: str = Field(..., description="Username or ID of the ticket creator")
    tags: List[str] = Field(default_factory=list, description="Tags associated with the ticket")


# PUBLIC_INTERFACE
class TicketUpdate(BaseModel):
    """Payload for updating an existing support ticket."""
    title: Optional[str] = Field(None, description="Updated title")
    description: Optional[str] = Field(None, description="Updated description")
    status: Optional[str] = Field(None, description="Updated status")
    tags: Optional[List[str]] = Field(None, description="Updated tags")


# PUBLIC_INTERFACE
class KBArticle(BaseModel):
    """A knowledge base article."""
    id: int = Field(..., description="Unique identifier of the KB article")
    title: str = Field(..., description="Title of the KB article")
    content: str = Field(..., description="Markdown content of the article")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="UTC creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="UTC last update timestamp")
    tags: List[str] = Field(default_factory=list, description="Tags for discoverability")


# PUBLIC_INTERFACE
class KBArticleCreate(BaseModel):
    """Payload for creating a new knowledge base article."""
    title: str = Field(..., description="Title of the KB article")
    content: str = Field(..., description="Markdown content of the article")
    tags: List[str] = Field(default_factory=list, description="Tags for discoverability")


# PUBLIC_INTERFACE
class KBArticleUpdate(BaseModel):
    """Payload for updating an existing knowledge base article."""
    title: Optional[str] = Field(None, description="Updated title")
    content: Optional[str] = Field(None, description="Updated markdown content")
    tags: Optional[List[str]] = Field(None, description="Updated tags")
