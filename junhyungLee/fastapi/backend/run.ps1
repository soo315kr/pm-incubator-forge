# Backend 서버 실행 (의존성 설치 후 uvicorn)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Starting server at http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Open: http://localhost:8000/kakao-authentication/request-oauth-link" -ForegroundColor Yellow
uvicorn main:app --host 127.0.0.1 --port 8000
