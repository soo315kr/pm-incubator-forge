export const ControlFlowIf = () => {
    let x = 10;
    let result;
    
    // x > 5 부등식은 x가 5보다 큰지 여부를 판단합니다.
    // 해당 질문의 답은 참 혹은 거짓
    if (x > 5) {
        // 조건이 참이라면 if 내부로 진입
        result = "x는 5 보다 크다."
    } else {
        // 조건이 거짓이라면 else 로 빠짐
        result = "x는 5 보다 작거나 같다."
    }


    // if 문 작성 요령
    // 1. 일단 if () {} 작성
    // 2. () 내부에 조건식 작성
    // 3. 조건이 만족 되었을 경우 어떤 작업을 할 것인지 {} 내부에 조건이 참일 때 실행할 코드 작성
    // 4. 아닌 경우를 표현하고자 한다면 else {} 구문 작성
    // 5. 실제 조건이 거짓이 되었을 경우 else {} 내부에 조건이 거짓일 때 실행할 코드 작성

    // 삼항 연산자
    // x > 5 ? A : B
    // 조건식 ? 참일 때 실행할 코드 : 거짓일 때 실행할 코드
    // x가 5보다 크다면? 참인 경우 : 거짓인 경우
    // 이후 최종 계산된 결과가 ternaryResult 변수에 할당됩니다.
    let ternaryResult = x > 5 ? "x는 5 보다 크다." : "x는 5 보다 작거나 같다."

    return (
        <div>
            <h3>Javascript 제어문 (if)</h3>

            <pre>{
                `
x = ${x}                         // 10
result = ${result}               // x는 5보다 크다. if-else 문 결과
ternaryResult = ${ternaryResult} // 삼항 연산자 결과
                `
            }</pre>
        </div>
    )
}