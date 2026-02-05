"""FastAPI 앱 진입점 (sprint_1: config, kakao_authentication)."""
from fastapi import FastAPI

from config import get_settings
from kakao_authentication import kakao_router

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(kakao_router)


@app.get("/")
def root():
    return {"message": "FastAPI Backend", "sprint": "sprint_1", "batch": ["config", "kakao_authentication"]}


if __name__ == "__main__":
    import uvicorn
    # py -m main 또는 python -m main → 포트 33333
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=33333,
        reload=False,
    )
