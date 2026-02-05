"""
FastAPI 애플리케이션 엔트리포인트
PM-EDDI-1: 애플리케이션 시작 시 load_env 호출
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from config.env import load_env
from kakao_authentication.controller import router as kakao_authentication_router

# PM-EDDI-1: 최초 한 번 load_env()에서 .env 로드 후, get_kakao_config()로만 제공.
load_env()

app = FastAPI(
    title="Kakao Authentication API",
    description="Kakao OAuth 인증 API",
    version="1.0.0",
)

# 라우터 등록
app.include_router(kakao_authentication_router)


@app.exception_handler(ValueError)
def handle_value_error(request, exc: ValueError):
    """PM-EDDI-2/3: 파라미터 누락, 잘못된 인가 코드 등에 대한 400 응답."""
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/")
def root():
    """루트 엔드포인트"""
    return {"message": "Kakao Authentication API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=33333, reload=True)
