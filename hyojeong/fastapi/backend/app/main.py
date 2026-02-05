from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from app.config.env import load_env
from app.kakao_authentication.controller import router as kakao_router


def create_app() -> FastAPI:
    load_env()

    app = FastAPI(title="Kakao Authentication API")
    app.include_router(kakao_router)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
