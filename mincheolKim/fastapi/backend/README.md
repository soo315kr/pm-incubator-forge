# FastAPI Backend

FastAPI를 사용한 백엔드 프로젝트입니다.

## 설치 방법

1. 가상 환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

## 실행 방법

```bash
python main.py
```

또는

```bash
uvicorn main:app --reload
```

서버가 실행되면 다음 URL에서 접근할 수 있습니다:
- API: http://localhost:8000
- API 문서 (Swagger UI): http://localhost:8000/docs
- API 문서 (ReDoc): http://localhost:8000/redoc

## 엔드포인트

- `GET /`: 루트 엔드포인트
- `GET /health`: 헬스 체크 엔드포인트
