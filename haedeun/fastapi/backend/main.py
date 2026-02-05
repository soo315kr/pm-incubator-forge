"""
FastAPI 애플리케이션 엔트리포인트

애플리케이션 시작 시 환경 변수를 로드하고 FastAPI 앱을 초기화합니다.
"""
from fastapi import FastAPI
from config.env import load_env

# 환경 변수 로드 (애플리케이션 시작 시 1회)
load_env()

# FastAPI 앱 생성
app = FastAPI(
    title="Kakao Authentication API",
    description="Kakao OAuth 인증을 위한 API",
    version="1.0.0"
)


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {"message": "Kakao Authentication API"}


# 라우터 등록
from kakao_authentication.controller import router as kakao_auth_router
app.include_router(kakao_auth_router, prefix="/kakao-authentication", tags=["kakao-authentication"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=33333)
