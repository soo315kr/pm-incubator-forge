"""FastAPI 애플리케이션 엔트리포인트. 환경 변수 로딩 후 앱을 생성한다."""

from contextlib import asynccontextmanager

from config import load_env
from fastapi import FastAPI

from kakao_authentication.router import register_kakao_exception_handler, router as kakao_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_env()
    yield


app = FastAPI(title="Kakao Authentication API", lifespan=lifespan)
app.include_router(kakao_router, prefix="/kakao-authentication", tags=["kakao-authentication"])
register_kakao_exception_handler(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )
