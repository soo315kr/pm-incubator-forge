from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import load_env
from app.kakao_authentication.controller import router as kakao_router
from app.kakao_authentication.exceptions import KakaoAuthenticationError


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_env()
    yield


app = FastAPI(title="Kakao OAuth Backend", lifespan=lifespan)
app.include_router(kakao_router, prefix="/kakao-authentication", tags=["kakao-authentication"])


@app.exception_handler(KakaoAuthenticationError)
def kakao_authentication_exception_handler(
    request: Request, exc: KakaoAuthenticationError
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """필수 파라미터 누락 등 검증 실패 시 400과 한 줄 메시지로 응답. 데이터 추측/생성 없음."""
    errors = exc.errors()
    if not errors:
        message = "요청 데이터가 올바르지 않습니다."
    else:
        first = errors[0]
        loc = first.get("loc", ())
        field = loc[-1] if loc else "필드"
        msg = first.get("msg", "값이 올바르지 않습니다.")
        message = f"{field}: {msg}"
    return JSONResponse(
        status_code=400,
        content={"detail": message},
    )


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
