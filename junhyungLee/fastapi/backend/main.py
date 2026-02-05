"""FastAPI 애플리케이션 엔트리포인트 (PM-EDDI-1: load_env 1회 호출)."""

from config.env import load_env

load_env()

from fastapi import FastAPI

from kakao_authentication.controller.routes import router as kakao_router

app = FastAPI(title="Backend", version="0.1.0")
app.include_router(kakao_router)


@app.get("/")
def root() -> dict:
    return {"message": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
