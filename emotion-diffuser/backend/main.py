"""
Emotion Diffuser — FastAPI Application Entry Point.
Start with: uvicorn backend.main:app --reload
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import router
from backend.config import API_TITLE, API_DESCRIPTION, API_VERSION, CORS_ORIGINS, DEBUG


# ────────────────────────────────────────
# LIFESPAN (startup / shutdown)
# ────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Called on startup and shutdown. Load models here later."""
    if DEBUG:
        print(f"[START] {API_TITLE} {API_VERSION} starting up...")
        print(f"[DOCS]  http://127.0.0.1:8000/docs")
        print(f"[INFO]  Built for Hack for Humanity 6.0")
    yield
    if DEBUG:
        print("[STOP] Shutting down Emotion Diffuser...")


# ────────────────────────────────────────
# APP INSTANCE
# ────────────────────────────────────────

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ────────────────────────────────────────
# MIDDLEWARE
# ────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ────────────────────────────────────────
# ROUTES
# ────────────────────────────────────────

app.include_router(router, prefix=f"/api/{API_VERSION}")


# ────────────────────────────────────────
# ROOT
# ────────────────────────────────────────

@app.get("/", tags=["System"])
async def root():
    """Root endpoint — redirect to docs."""
    return {
        "message": "Emotion Diffuser API is running",
        "docs": f"/docs",
        "health": f"/api/{API_VERSION}/health",
        "version": API_VERSION,
    }

