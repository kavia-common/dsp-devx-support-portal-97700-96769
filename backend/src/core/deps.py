"""
Dependency wiring for repositories and application-wide singletons.

This module initializes in-memory repositories and seeds demo data for a
healthy out-of-the-box experience. It also exposes FastAPI dependency
providers to retrieve repository instances.
"""
from __future__ import annotations

from .models import TicketCreate, CommentCreate, KBArticleCreate
from .repository import (
    InMemoryTicketRepository, InMemoryCommentRepository, InMemoryKBRepository,
    TicketRepository, CommentRepository, KBRepository
)

# Singleton in-memory repos for app lifetime
_ticket_repo = InMemoryTicketRepository()
_comment_repo = InMemoryCommentRepository()
_kb_repo = InMemoryKBRepository()


def _seed_demo_data() -> None:
    """Seed initial demo data for tickets, comments, and KB articles."""
    if _ticket_repo.list():
        # Already seeded
        return

    # Tickets
    t1 = _ticket_repo.create(TicketCreate(
        title="Cannot deploy service on staging",
        description="Deployment fails with timeout when pushing to staging.",
        created_by="alice",
        tags=["deployment", "staging"]
    ))
    t2 = _ticket_repo.create(TicketCreate(
        title="API rate limit errors",
        description="Hitting 429 too frequently when running load tests.",
        created_by="bob",
        tags=["api", "limits"]
    ))
    t3 = _ticket_repo.create(TicketCreate(
        title="Build pipeline flaky",
        description="Intermittent failures in CI on ubuntu-latest runner.",
        created_by="carol",
        tags=["ci", "flaky"]
    ))

    # Comments
    _comment_repo.create(CommentCreate(
        ticket_id=t1.id, author="support-bot",
        message="We are investigating the staging cluster. ETA 2 hours."
    ))
    _comment_repo.create(CommentCreate(
        ticket_id=t1.id, author="alice",
        message="Sharing logs from the last failed deployment."
    ))
    _comment_repo.create(CommentCreate(
        ticket_id=t2.id, author="dave",
        message="Consider batching requests, docs suggest a 100 RPS soft limit."
    ))
    _comment_repo.create(CommentCreate(
        ticket_id=t3.id, author="support",
        message="We increased retry budget on CI tasks to mitigate flakiness."
    ))

    # KB articles
    _kb_repo.create(KBArticleCreate(
        title="How to configure staging deployments",
        content="# Staging Deployments\n\nFollow these steps to configure staging...",
        tags=["deployment", "staging"]
    ))
    _kb_repo.create(KBArticleCreate(
        title="Understanding API rate limits",
        content="# API Rate Limits\n\nOur API enforces dynamic throttling...",
        tags=["api", "limits"]
    ))
    _kb_repo.create(KBArticleCreate(
        title="Reducing CI flakiness",
        content="# CI Flakiness\n\nUse retries and cache restoration...",
        tags=["ci", "stability"]
    ))


_seed_demo_data()


# PUBLIC_INTERFACE
def get_ticket_repo() -> TicketRepository:
    """FastAPI dependency provider for TicketRepository."""
    return _ticket_repo


# PUBLIC_INTERFACE
def get_comment_repo() -> CommentRepository:
    """FastAPI dependency provider for CommentRepository."""
    return _comment_repo


# PUBLIC_INTERFACE
def get_kb_repo() -> KBRepository:
    """FastAPI dependency provider for KBRepository."""
    return _kb_repo
