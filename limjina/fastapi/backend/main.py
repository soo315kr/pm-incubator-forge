"""
FastAPI 애플리케이션 엔트리포인트.
환경 변수는 config.load_env에서 1회 로드되며, Service/Controller는 .env를 직접 로드하지 않는다.
"""
import uvicorn
from fastapi import FastAPI

from config.env import load_env
from kakao_authentication.controller import register_exception_handlers, router as kakao_router

# 애플리케이션 시작 전 환경 변수 1회 로드 (PM-EDDI-1)
load_env()

application = FastAPI(title="Kakao OAuth Backend")
application.include_router(kakao_router, prefix="/kakao-authentication", tags=["kakao-authentication"])


if __name__ == "__main__":
    uvicorn.run("main:application", host="0.0.0.0", port=8000, reload=True)
