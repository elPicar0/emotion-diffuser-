"""
Emotion Diffuser — FastAPI Application Entry Point.
Start with: uvicorn backend.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import router
from backend.config import API_TITLE, API_DESCRIPTION, API_VERSION, CORS_ORIGINS, DEBUG


# ────────────────────────────────────────
# APP INSTANCE
# ────────────────────────────────────────

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
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


# ────────────────────────────────────────
# STARTUP / SHUTDOWN EVENTS
# ────────────────────────────────────────

@app.on_event("startup")
async def startup():
    """Called when server starts. Load models here later."""
    if DEBUG:
        print(f"[START] {API_TITLE} {API_VERSION} starting up...")
        print(f"[DOCS]  http://127.0.0.1:8000/docs")
        print(f"[INFO]  Built for Hack for Humanity 6.0")


@app.on_event("shutdown")
async def shutdown():
    """Called when server shuts down. Cleanup here later."""
    if DEBUG:
        print("[STOP] Shutting down Emotion Diffuser...")
