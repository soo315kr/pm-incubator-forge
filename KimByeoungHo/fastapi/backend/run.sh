#!/bin/bash

# FastAPI 서버 실행 스크립트
# 사용법: ./run.sh 또는 bash run.sh

# 현재 디렉토리로 이동
cd "$(dirname "$0")"

# 2501번 포트 사용 중인 프로세스 확인 및 종료
PORT=2501
PID=$(lsof -ti:$PORT)

if [ ! -z "$PID" ]; then
  echo "[INFO] 포트 $PORT가 이미 사용 중입니다 (PID: $PID)"
  echo "[INFO] 기존 프로세스를 종료합니다..."
  kill -9 $PID
  sleep 1
  echo "[INFO] 포트 해제 완료"
fi

# 가상환경 활성화
source venv/bin/activate

echo "[INFO] 서버를 시작합니다..."
# 서버 실행
python -m main
