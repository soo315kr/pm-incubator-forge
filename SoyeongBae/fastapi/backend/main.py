"""애플리케이션 엔트리포인트. 시작 시 config에서 환경 변수를 1회 로드한다."""

from config.env import load_env
from fastapi import FastAPI

from kakao_authentication.controller import router as kakao_auth_router

# 애플리케이션 시작 전 .env 1회 로드 (config 패키지 책임)
load_env()

app = FastAPI()

app.include_router(kakao_auth_router, prefix="/kakao-authentication")


@app.get("/")
def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=33333, reload=True)
