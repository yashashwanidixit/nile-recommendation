from fastapi import FastAPI
from api.routes.itinerary import router as itinerary_router
from api.routes.recommendations import router as recommendation_router

app = FastAPI(
    title="NILE Recommendation Engine",
    description="AI-powered travel recommendation and itinerary service",
    version="0.1.0",
)

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

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
