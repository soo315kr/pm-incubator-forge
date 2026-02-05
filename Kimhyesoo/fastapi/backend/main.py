"""
FastAPI 애플리케이션 엔트리포인트
"""
from fastapi import FastAPI
from config.env import load_env
from api.kakao_authentication import router as kakao_auth_router

# 환경 변수 로드 (애플리케이션 시작 시 1회)
load_env()

app = FastAPI(title="Kakao Authentication API")

# 라우터 등록
app.include_router(kakao_auth_router)


@app.get("/")
async def root():
    return {"message": "Kakao Authentication API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=33333)
