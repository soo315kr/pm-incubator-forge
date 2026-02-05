"""FastAPI 애플리케이션 엔트리포인트."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse # 이 줄을 추가했습니다

from config.env import load_env
from kakao_authentication.router import router as kakao_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 시작 시 환경 변수 1회 로드."""
    load_env()
    yield


app = FastAPI(title="Kakao Authentication API", lifespan=lifespan)
app.include_router(kakao_router, prefix="/kakao-authentication", tags=["kakao-authentication"])


@app.get("/health")
def health():
    return RedirectResponse(url=kakao_url)

from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse
router = APIRouter()

@router.get("/request-oauth-link")
async def request_oauth_link():
    return RedirectResponse(url=kakao_url)
    # 1. 카카오 인증에 필요한 정보들 (본인의 설정값 확인)
    client_id = bd7c363cc38a2500094b9460b4cedd5a 
    redirect_uri = "http://127.0.0.1:8000/kakao-authentication/callback" # 등록한 리다이렉트 URI
    
    # 2. 카카오 로그인 페이지 주소 생성
    kakao_url = (
        f"https://kauth.kakao.com/oauth/authorize?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code"
    )
    
    # 3. 핵심: 생성된 주소로 브라우저를 보냄
    return RedirectResponse(url=kakao_url)