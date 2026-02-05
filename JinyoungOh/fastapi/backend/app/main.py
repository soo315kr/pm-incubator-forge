from fastapi import FastAPI

from app.config.env import load_env
from app.kakao_authentication.controller.kakao_oauth_controller import router as kakao_oauth_router

# 애플리케이션 전역에서 .env 1회 로드 보장 (uvicorn이 app.main:app 직접 로드 시에도 동작)
load_env()

app = FastAPI()

app.include_router(kakao_oauth_router)


@app.get("/")
def root():
    return {"message": "Hello"}
