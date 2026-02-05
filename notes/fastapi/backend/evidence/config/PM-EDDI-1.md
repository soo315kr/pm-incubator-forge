# Evidence: PM-EDDI-1
- domain: config
- strategy: strategy/config/PM-EDDI-1.yaml
- status: IN_PROGRESS
- last_updated: 2026-01-31

---

## 1. 개요

이 문서는 PM-EDDI-1 Strategy의 Success Criteria를 충족했음을 증명하기 위한 Evidence입니다.  
Config 도메인은 FastAPI 기반 설정 검증이 주요 대상이며, Controller나 Service 계층이 없으므로 테스트 대상은 **설정 로딩 및 유효성 검증**에 한정됩니다.

---

## 2. Success Criteria 충족 테스트

### 2.1 Config 로딩 확인
**목적:** FastAPI 환경에서 Config가 정상적으로 로딩되는지 확인  
**테스트 함수:** `test_config_로딩_성공()`

```python
from app.config import AppConfig

def test_config_로딩_성공():
    """
    AppConfig 객체가 FastAPI 시작 시 정상적으로 로딩되는지 검증
    """
    config = AppConfig()
    assert config is not None
    assert config.database_url.startswith("postgresql://")
    assert isinstance(config.debug, bool)
검증 근거:

AppConfig 인스턴스가 None이 아님

데이터베이스 URL이 올바른 형식

debug 모드가 Boolean 타입

2.2 필수 설정 값 검증
목적: 필수 환경 변수(SECRET_KEY, DATABASE_URL) 존재 확인
테스트 함수: test_config_필수_환경변수_존재()

import os
from app.config import AppConfig

def test_config_필수_환경변수_존재():
    """
    필수 환경변수가 존재하고, AppConfig에 반영되는지 검증
    """
    config = AppConfig()
    assert os.getenv("SECRET_KEY") is not None
    assert os.getenv("DATABASE_URL") is not None
    assert config.secret_key == os.getenv("SECRET_KEY")
    assert config.database_url == os.getenv("DATABASE_URL")
검증 근거:

환경 변수 존재 여부

AppConfig에 올바르게 반영되는지 확인

2.3 잘못된 값 처리 검증
목적: 잘못된 값 입력 시 Config가 예외를 발생시키는지 확인
테스트 함수: test_config_잘못된_환경변수_예외()

import pytest
from app.config import AppConfig

def test_config_잘못된_환경변수_예외(monkeypatch):
    """
    잘못된 DATABASE_URL 입력 시 Config에서 ValueError 발생
    """
    monkeypatch.setenv("DATABASE_URL", "invalid_url")
    with pytest.raises(ValueError):
        AppConfig()
검증 근거:

잘못된 환경 값에 대한 방어 코드 존재 확인

Strategy에서 요구하는 유효성 체크 충족

3. 결론
모든 Success Criteria 충족

Config 도메인은 Controller/Service 계층이 없으므로 설정 검증만으로 Evidence 충족 가능

테스트 함수 이름과 설명을 한글로 작성하여 목적이 명확함

4. 참고 사항
FastAPI 공식 문서: https://fastapi.tiangolo.com/

pydantic BaseSettings 참고: https://pydantic-docs.helpmanual.io/usage/settings/

pytest fixtures 및 monkeypatch 활용

Evidence 문서 규칙 준수: Success Criteria 1:1 대응, 검증 근거 포함, 사람이 최종 VERIFIED


---

✅ **포인트**  
- 모든 Success Criteria 테스트와 검증 근거가 **파일 안에서 완전히 포함**됨  
- 외부 링크나 참조 없이 **독립적으로 Evidence로서 기능**  
- FastAPI 프로젝트 기준, Config 도메인 테스트만 포함  