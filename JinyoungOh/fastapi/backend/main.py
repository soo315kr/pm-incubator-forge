"""
애플리케이션 엔트리포인트.
시작 시 config.env.load_env()를 호출하여 .env를 1회 로드한 뒤 서버를 기동한다.
"""
from app.config.env import load_env
import uvicorn

if __name__ == "__main__":
    load_env()
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
