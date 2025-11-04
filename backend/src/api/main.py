from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.health import router as health_router
from src.api.routers.tickets import router as tickets_router
from src.api.routers.kb import router as kb_router
from src.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings["app_name"],
    description="Backend API for DSP DevX Support Pioneer with in-memory repositories for demo.",
    version="0.1.0",
    openapi_tags=[
        {"name": "health", "description": "Health and diagnostics"},
        {"name": "tickets", "description": "Manage support tickets"},
        {"name": "comments", "description": "Manage ticket comments"},
        {"name": "kb", "description": "Knowledge base articles"},
    ],
)

# CORS based on env ALLOW_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings["allow_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(tickets_router)
app.include_router(kb_router)
