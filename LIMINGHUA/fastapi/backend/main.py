"""
Application entry. Environment is loaded once here; do not load .env in services or controllers.
"""
from config.env import load_env

load_env()

from fastapi import FastAPI
from kakao_authentication.controller import router as kakao_router

app = FastAPI(title="Kakao Auth API")
app.include_router(kakao_router, prefix="/kakao-authentication", tags=["kakao-authentication"])


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=33333, reload=True)
