"""FastAPI application entry point."""
import uvicorn
from fastapi import FastAPI

from config.env import load_env
from kakao_authentication.presentation.controller import router as kakao_auth_router

# Load environment variables once at application startup
load_env()

app = FastAPI(
    title="Kakao Authentication API",
    description="API for Kakao OAuth authentication",
    version="1.0.0",
)

# Register routers
app.include_router(kakao_auth_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Kakao Authentication API"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=33333)
