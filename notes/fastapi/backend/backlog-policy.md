# Backlog Progress Governance Policy

## 0. 이 문서의 지위 (변경 불가)

이 문서는 본 프로젝트의 **백로그 진행 관리에 대한 최상위 규칙**이다.  
이 문서의 규칙은 모든 도메인, 모든 기능, 모든 도구에 **우선**한다.

이 문서는 설계 문서도, 구현 문서도 아니다.  
이 문서는 **진행 상태를 어떻게 판단·관리할 것인가**만을 정의한다.

---

## 1. 핵심 개념 정의 (절대 혼동 금지)

### 1.1 Strategy
- 위치: `strategy/**/PM-*.yaml`
- 의미: **무엇을 만족해야 하는가**

특징:
- 요구사항의 **유일한 진실 원천**
- Success Criteria는 설명이 아니라 **판단 기준**
- Strategy는 진행 상태를 알지 못한다

---

### 1.2 Backlog List
- 파일: `backlog-list.md`
- 의미: **무엇이 어디까지 진행되었는가**

특징:
- 상태 데이터만 포함
- 설명, 판단, 해석 **절대 금지**
- 사람이 직접 수정한다

---

### 1.3 Evidence
- 위치: `evidence/PM-EDDI-*.md`
- 의미: **Strategy를 충족했음을 주장하기 위한 증거**

특징:
- Success Criteria 항목별 1:1 대응
- 코드가 아니라 **충족 논리에 대한 서술**
- Evidence 없는 완료는 **존재하지 않는다**

---

## 2. Status 정의 (엄격)

| Status | 의미 | Claude 가능 행위 |
|------|------|----------------|
| NOT_STARTED | Evidence 없음 | 구조 분석 |
| IN_PROGRESS | 작업 진행 중 | 누락 지적 |
| EVIDENCE_SUBMITTED | Evidence 완료 | **논리 검증** |
| VERIFIED | 인간이 승인 | 없음 |

⚠️ Claude는 VERIFIED를 직접 선언하지 않는다.

---

## 3. Evidence 규칙 (위반 불가)

- Evidence 파일은 Feature ID와 **1:1 대응**

evidence/
├── PM-EDDI-1.md
├── PM-EDDI-2.md
└── PM-EDDI-3.md


- Evidence가 없으면:
  - 완료는 불가능
  - VERIFIED는 논리적으로 성립하지 않는다

---

## 4. Claude 사용 규칙 (강제)

### 허용
- Evidence의 Success Criteria 충족 여부 검증
- 논리적 누락, 모호성 지적
- Strategy의 검증 가능성 평가

### 금지
- status 변경
- 완료 선언
- 다음 백로그 선택
- Evidence 대리 작성

> Claude는 **판단 보조자**이지 **결정 주체**가 아니다

---

## 5. 책임 분리 (Role Boundary)

| 항목 | 인간 | Claude |
|----|----|----|
| Strategy 작성 | O | X |
| Evidence 작성 | O | X |
| 논리 검증 | O(최종) | O(보조) |
| 상태 변경 | O | X |
| 완료 선언 | O | X |

---

## 6. 변경 규칙 (운영 안정성)

- `strategy/**` → 요구사항 변경
- `evidence/**` → 주장 보완
- `backlog-list.md` → 진행 상태 변경
- `backlog-policy.md` → **운영 체계 변경 (극히 제한)**

---

## 7. 실제 운용 절차 (Operational Flow)

### 7.1 백로그 착수
1. 인간이 `backlog-list.md`에서 항목을 `IN_PROGRESS`로 변경
2. 해당 Strategy(`PM-*.yaml`)를 기준으로 구현 진행

### 7.2 Evidence 작성
1. 모든 Success Criteria에 대해 Evidence 문서 작성
2. Evidence 완료 후 상태를 `EVIDENCE_SUBMITTED`로 변경

### 7.3 Claude 검증 요청
- 허용 예:
  > “PM-EDDI-2 evidence가 Strategy의 Success Criteria를 충족하는지 검증해라”

Claude의 출력:
- 충족 여부 판단 근거
- 누락 또는 모호성 지적
- 추가 보완 필요 항목

### 7.4 인간 최종 결정
1. Claude 분석을 참고
2. 인간이 직접 판단
3. 조건 충족 시 `VERIFIED`로 상태 변경

---

## 8. 실패 허용 원칙 (중요)

- Evidence 보완 요구는 **실패가 아니다**
- VERIFIED 이전의 모든 상태는 **가역적**
- VERIFIED는 **되돌릴 수 없는 선언**

---

## 9. 최종 선언

- Strategy는 요구사항을 정의한다  
- Evidence는 충족을 주장한다  
- Backlog List는 상태를 선언한다  
- Claude는 판단을 보조한다  
- **결정은 항상 인간의 몫이다**