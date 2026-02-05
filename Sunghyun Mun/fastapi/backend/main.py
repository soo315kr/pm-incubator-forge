"""
FastAPI 애플리케이션 엔트리포인트.
환경 변수 로딩은 config 패키지에서 1회 수행한다.
"""
from contextlib import asynccontextmanager

import uvicorn
from config.env import load_env
from fastapi import FastAPI

from kakao_authentication.controller import router as kakao_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_env()
    yield


app = FastAPI(
    title="Kakao Auth API",
    description="Kakao OAuth 인증 URL 발급, 액세스 토큰 발급, 사용자 정보 조회 API",
    lifespan=lifespan,
)
app.include_router(kakao_router, prefix="/kakao-authentication", tags=["kakao-authentication"])


@app.get("/")
def root():
    """API 문서 링크를 반환한다."""
    return {
        "message": "Kakao Auth API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    """헬스 체크."""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
