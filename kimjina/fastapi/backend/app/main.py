# PM-EDDI-1: 애플리케이션 시작 시 .env 1회 로드 (config 패키지 책임)
from app.config.env import load_env
load_env()

from fastapi import FastAPI
from app.config import settings
from app.auth import kakao_router
from app.kakao_authentication import kakao_authentication_router

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(kakao_router)
app.include_router(kakao_authentication_router)


@app.get("/")
async def root():
    return {"message": "ok", "app": settings.app_name}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
