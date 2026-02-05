# Kakao Auth API (FastAPI)

## 실행 방법

1. **의존성 설치**
   ```powershell
   pip install -r requirements.txt
   ```

2. **환경 변수 설정**  
   `.env.example`을 복사해 `.env`를 만들고 Kakao 앱 키를 넣습니다.
   ```
   KAKAO_CLIENT_ID=your_rest_api_key
   KAKAO_REDIRECT_URI=http://localhost:8000/callback
   ```

3. **서버 실행**
   ```powershell
   uvicorn main:app --reload
   ```

   - API 문서: http://127.0.0.1:8000/docs  
   - `ModuleNotFoundError: No module named 'dotenv'` 가 나오면 `pip install python-dotenv` 또는 `pip install -r requirements.txt` 를 먼저 실행하세요.
