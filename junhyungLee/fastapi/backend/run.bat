@echo off
cd /d "%~dp0"

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 exit /b 1

echo.
echo Starting server at http://127.0.0.1:8000
echo Open: http://localhost:8000/kakao-authentication/request-oauth-link
echo.
uvicorn main:app --host 127.0.0.1 --port 8000
