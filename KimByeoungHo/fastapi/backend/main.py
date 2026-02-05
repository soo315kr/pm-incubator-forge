"""
FastAPI 애플리케이션 엔트리포인트

PM-BH-1: 애플리케이션 시작 시 환경 변수를 로드합니다.
PM-BH-2, 3, 4: Kakao Authentication API 라우터를 등록합니다.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# PM-BH-1: 환경 변수 로딩 (애플리케이션 시작 시 1회 호출)
from config.env import load_env
load_env()

# Kakao Authentication 의존성
from kakao_authentication.service_implementation import KakaoAuthenticationService
from kakao_authentication.controller import KakaoAuthenticationController, setup_routes


# FastAPI 앱 생성
app = FastAPI(
    title="Kakao OAuth Authentication API",
    description="Kakao OAuth 인증 시스템 (PM-BH-1, 2, 3, 4 구현)",
    version="1.0.0"
)

# CORS 설정 (개발 환경)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency Injection: Service 구현체 생성 및 Controller에 주입
# Controller는 Service Interface에만 의존하며, 구체적인 구현은 알지 못함
kakao_service = KakaoAuthenticationService()
kakao_controller = KakaoAuthenticationController(service=kakao_service)

# PM-BH-2, 3, 4: Kakao Authentication 라우터 등록
app.include_router(setup_routes(kakao_controller))


@app.get("/")
async def root():
    """
    API 루트 엔드포인트
    """
    return {
        "message": "Kakao OAuth Authentication API",
        "version": "1.0.0",
        "endpoints": {
            "PM-BH-2": "GET /kakao-authentication/request-oauth-link",
            "PM-BH-3": "GET /kakao-authentication/callback?code={code}",
            "PM-BH-4": "GET /kakao-authentication/user-info?access_token={token}"
        }
    }


@app.get("/health")
async def health_check():
    """
    헬스 체크 엔드포인트
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    # 개발 서버 실행
    uvicorn.run(
        app,  # 직접 app 객체 전달 (python -m main 실행 지원)
        host="0.0.0.0",
        port=2501,
        reload=False,  # 모듈 실행 시 reload 비활성화
        log_level="info"  # INFO 로그 출력
    )
