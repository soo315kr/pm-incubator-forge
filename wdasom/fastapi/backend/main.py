from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from config.env import load_env
from kakao_authentication import router as kakao_auth_router

# PM-EDDI-1: 애플리케이션 시작 시 단 한 번 .env 로드
load_env()

app = FastAPI(
    title="Lectur Kakao Authentication API",
    version="0.1.0",
)

# Kakao 인증 도메인 라우터 등록
app.include_router(
    kakao_auth_router,
    prefix="/kakao-authentication",
    tags=["kakao-authentication"],
)


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    """간단한 헬스 체크 엔드포인트."""
    return {"status": "ok"}


if __name__ == "__main__":
    """
    uvicorn으로 직접 실행할 수 있도록 메인 엔트리포인트를 제공한다.

    - `python main.py` 로 실행 가능
    - 또는 `uvicorn main:app --reload` 로도 동일하게 실행 가능
    """
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=33333,
        reload=True,
    )

