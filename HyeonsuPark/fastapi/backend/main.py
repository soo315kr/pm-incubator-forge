"""FastAPI 애플리케이션 엔트리포인트. 시작 시 config에서 환경 변수를 1회 로드한다."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import load_env
from kakao_authentication.controller import router as kakao_auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_env()
    yield


app = FastAPI(title="Kakao Auth Backend", lifespan=lifespan)
app.include_router(kakao_auth_router, prefix="/kakao-authentication", tags=["kakao-authentication"])


@app.get("/")
def root():
    return {"message": "Kakao Auth Backend", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=33333, reload=True)
