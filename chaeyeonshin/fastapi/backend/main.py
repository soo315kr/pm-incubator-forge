"""FastAPI 애플리케이션 엔트리포인트. 시작 시 config.load_env를 1회 호출한다."""
from config.env import load_env

load_env()

from fastapi import FastAPI

from kakao_authentication.controller import get_router
from kakao_authentication.service_impl import KakaoAuthServiceImpl

app = FastAPI(title="Kakao Authentication API")
app.include_router(
    get_router(KakaoAuthServiceImpl()),
    prefix="/kakao-authentication",
    tags=["kakao-authentication"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=33333, reload=True)
