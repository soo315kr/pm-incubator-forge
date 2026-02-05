from fastapi import FastAPI
from config.env import get_env_config
from kakao_authentication.controller.kakao_oauth_controller import kakao_oauth_router

# 환경 변수 로드 확인
get_env_config()

app = FastAPI()

app.include_router(kakao_oauth_router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=33333)
