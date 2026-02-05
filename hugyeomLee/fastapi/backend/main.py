"""
애플리케이션 엔트리포인트.
환경 변수 로딩 후 FastAPI 앱을 생성한다. (PM-EDDI-1)
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.env import load_env
from kakao_authentication.controller import router as kakao_auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_env()
    yield
    # shutdown if needed


app = FastAPI(title="Kakao Authentication API", lifespan=lifespan)
app.include_router(kakao_auth_router, prefix="/kakao-authentication", tags=["kakao-authentication"])


def main() -> None:
    """애플리케이션을 로컬에서 구동한다."""
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
