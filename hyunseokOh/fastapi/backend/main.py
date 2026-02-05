"""Application entrypoint. Load env once, then create FastAPI app."""

from config.env import load_env

load_env()

from fastapi import FastAPI

from kakao_authentication.router import router as kakao_router

app = FastAPI(title="Kakao Auth Backend")
app.include_router(kakao_router, prefix="/kakao-authentication", tags=["kakao-authentication"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)