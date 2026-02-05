"""
FastAPI 애플리케이션 엔트리포인트

애플리케이션 시작 시 환경 변수를 로드하고 FastAPI 앱을 초기화합니다.
"""
from fastapi import FastAPI
from config.env import load_env

# 환경 변수 로드 (애플리케이션 시작 시 1회 실행)
load_env()

# FastAPI 앱 생성
app = FastAPI(
    title="Kakao Authentication API",
    description="Kakao OAuth 인증을 위한 API",
    version="1.0.0"
)

# 라우터 등록
from kakao_authentication.controller.kakao_authentication_controller import router as kakao_auth_router

app.include_router(kakao_auth_router, prefix="/kakao-authentication", tags=["kakao-authentication"])


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {"message": "Kakao Authentication API"}


@app.get("/health")
async def health():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # 강사님 코드 방식: 파일 경로와 앱 객체를 문자열로 지정
    uvicorn.run("main:app", host="0.0.0.0", port=33333, reload=True)