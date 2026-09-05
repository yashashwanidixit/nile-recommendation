from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.itinerary import router as itinerary_router
from api.routes.recommendations import router as recommendation_router
from core.config import get_settings
from core.exceptions import register_exception_handlers
from services.data_loader import get_cached_activities, get_cached_hotels

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup and shutdown tasks."""
    # Pre-warm in-memory data caches at application startup
    get_cached_hotels()
    get_cached_activities()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handlers
register_exception_handlers(app)

# Include API Routers
app.include_router(recommendation_router)
app.include_router(itinerary_router)


@app.get("/health", tags=["health"])
def health_check() -> dict:
    """Health check endpoint returning service status."""
    return {
        "status": "ok",
        "service": "nile-recommendation",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
