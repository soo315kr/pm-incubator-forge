import os

import uvicorn
from fastapi import FastAPI

from config.env import load_fastapi_env
from dice.infrastructure.api.dice_controller import dice_router

def create_app() -> FastAPI:
    load_fastapi_env(".env")

    app = FastAPI(title="Dice DDD API")

    app.include_router(dice_router, prefix="/dice")
    return app

app = create_app()

# uvicorn으로 직접 실행 가능
if __name__ == "__main__":
    host = os.getenv("APP_HOST")
    port = int(os.getenv("APP_PORT"))

    uvicorn.run(app, host=host, port=port)
