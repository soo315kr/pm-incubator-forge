# 오늘 운동

- 오늘 운동
    - Strategy / Direction (최상위)
        - 목적: 스터디 참여자들이 매일 운동 습관을 기록하고, 계획-실행-회고 루프를 체험
        - 핵심 가치: 자기 관리, 건강 습관 형성, 일일 피드백 경험
        - 의도적 배제: 운동 외 활동은 체크하지 않음 (예: 다른 일상 활동, 운동 강도 세부 측정)
        - 실패 감수 기준: 하루 운동 기록 누락 → 학습 데이터로 활용, 루프 분석 경험 제공
        
    - Product (판단 프레임)
        - Objective / Key Results (OKR)
            - Objective: 매일 운동 습관 만들기
            - Key Results:
                1. 일주일간 운동 기록 완료율 100%
                2. 2주간 운동 미기록 1회 이하
            
        - 판단 구조
            1. 오늘 운동 수행 여부 → OKR 기준 검증
            2. 실패 → 원인 분석 (왜 운동하지 못했는가)
            3. 성공 → 다음 주 목표와 Backlog 결정
        
        - 핵심 질문
            - 오늘 운동을 했는가?
            - 기록하지 못했다면 무엇을 배울 수 있는가?
            - 성공적으로 기록했다면 다음 주 계획은 무엇인가?
        
    - 실행 시스템 (Backlog / Sprint Term / Status)
        - Backlog
            - 운동 기록 작성 (종류, 시간, 강도 등 간략 기록)
            - 기록 확인 / 간단 코멘트 작성 (선택)
            - 주간 회고 / 패턴 분석
        
        - Sprint Term (주간 계획)
            - 월 ~ 금: 하루 1회 운동 기록 체크
            - 매주 금요일: 주간 회고 & OKR 체크
        
        - Status Board
            - Todo → In Progress → Done → Review → Block
        
    - 검증 & 회고
        - Success Criteria
            - 하루 운동 기록 완료 → Done
            - 주간 기록 완료율 → OKR Check-in
        
        - Decision Log
            - 매일/매주 기록 완료 여부 기록
            - 성공/실패 판단 근거 기록
            - 다음 주 Backlog 조정
        
    - 흐름 시각화 (루프)
        
        ```
        Strategy / Direction
                 ↓
        Product(판단 기준 & OKR)
                 ↓
        Backlog 등록 & Sprint Term 계획
                 ↓
        Daily Execution(운동 기록 작성)
                 ↓
        검증(Success Criteria)
                 ↓
        회고 & Decision Log 기록
                 ↓
        다음 주 Sprint Term 결정
        ```
        
    - 핵심 체험 포인트
        1. Domain 이해: Daily Exercise라는 단일 책임, 작은 세계 정의
        2. Product 체험: OKR + 판단 기준으로 Backlog 실행 여부 결정
        3. Sprint Term 체험: 주간 단위 계획 → 실행 → 피드백 루프
        4. 실행 & 기록: Status Board, Decision Log로 재현 가능성과 검증 경험
        5. 학습 루프 완성: 반복적 회고와 판단으로 Product 프레임 이해


# Kakao Auth Backend

FastAPI backend for Kakao OAuth (PM-OHS-1 ~ PM-OHS-4).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: set KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI (and optionally KAKAO_CLIENT_SECRET)
```

## Run

```bash
uvicorn main:app --reload
```

- Health: `GET /health`
- OAuth link: `GET /kakao-authentication/request-oauth-link`
- Token after redirect: `GET /kakao-authentication/request-access-token-after-redirection?code=...`
- User info: `GET /kakao-authentication/user-info?access_token=...` or `Authorization: Bearer <token>`
