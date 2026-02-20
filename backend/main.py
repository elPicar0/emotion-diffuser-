from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import router
from backend.config import settings

app = FastAPI(
    title="Emotion Diffuser API",
    description="AI-powered emotion analysis and conflict mediation system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "status": "Emotion Diffuser API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
