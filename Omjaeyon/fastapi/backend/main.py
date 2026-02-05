"""FastAPI application entry point."""
from fastapi import FastAPI
from strategy.config.env import load_env

# Load environment variables FIRST - before any module that needs them
load_env()

from strategy.kakao_authentification.controller.kakao_oauth_controller import router as kakao_oauth_router

app = FastAPI(
    title="Kakao Authentication API",
    description="Kakao OAuth authentication API",
    version="1.0.0"
)

# Register routers
app.include_router(kakao_oauth_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Kakao Authentication API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
