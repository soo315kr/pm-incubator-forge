#!/bin/zsh

# 1️⃣ 병합 파일 및 프롬프트 파일 위치
mkdir -p tmp
MERGED_FILE="tmp/merged_plan.txt"
PROMPT_FILE="tmp/claude_prompt.txt"

# 2️⃣ 기존 파일 삭제
rm -f $MERGED_FILE $PROMPT_FILE

# 3️⃣ YAML 병합 순서: Domain Layer -> Application Layer
for file in strategy/config/*.yaml strategy/kakao_authentication/*.yaml; do
    echo "\n--- $file ---\n" >> $MERGED_FILE
    cat $file >> $MERGED_FILE
done

echo "✅ YAML 병합 완료: $MERGED_FILE 생성"

# 4️⃣ Claude CLI용 프롬프트 생성
cat <<EOF > $PROMPT_FILE
너는 시니어 소프트웨어 아키텍트이자 DDD 전문가야.
아래는 프로젝트 전체 Feature YAML 병합 내용이야:

$(cat $MERGED_FILE)

너의 목표:
1. Feature별 Success Criteria를 기반으로 우선순위를 평가해라.
2. Layered Architecture와 Domain-Driven Design 준수를 검증해라.
3. Feature 간 의존성을 고려하여 Sprint 단위 Backlog를 배치해라.
4. To-do 목록은 순서대로 정리하고 중복을 제거해라.
5. Sprint 1, Sprint 2 등으로 나누어 보여라.
6. Layered Architecture 또는 DDD 관련 문제점이 있으면 표시해라.

출력 형식:
- Sprint 단위 Backlog
- Feature 우선순위 + Dependencies
- To-do 순서 정리
- DDD/Layered Architecture 문제점

주의:
- 판단과 구조 정리에 집중
EOF

echo "✅ Claude CLI 프롬프트 생성 완료: $PROMPT_FILE"
echo "다음 단계: Claude Max Plan CLI를 열고 $PROMPT_FILE 내용 전체 복사 후 붙여넣기"
