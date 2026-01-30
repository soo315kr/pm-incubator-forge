from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import load_env

load_env()

from kakao_authentication.controller.kakao_oauth_controller import router as kakao_oauth_router

app = FastAPI(
    title="FastAPI Backend",
    description="FastAPI 백엔드 프로젝트",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용하도록 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(kakao_oauth_router)


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {"message": "FastAPI 백엔드에 오신 것을 환영합니다!"}


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=33333)
