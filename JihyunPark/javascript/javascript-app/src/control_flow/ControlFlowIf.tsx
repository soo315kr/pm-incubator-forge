export const ControlFlowIf = () => {
    let x = 10;
    let result;

    // x > 5 부등식은 X가 5보다 큰지 비교하는 조건식
    if (x > 5) {
        result = "x는 5보다 크다.";
    } else {
        result = "x는 5보다 작거나 같다.";
    }

    // if문 작성 요령
    // 1. 일단 if() {} 작성
    // 2. () 안에 조건식 작성
    // 3. {} 안에 조건식이 true일 때 실행할 코드 작성
    // 4. 필요시 else {} 작성
    // 5. else {} 안에 조건식이 false일 때 실행할 코드 작성

    // 삼항 연산자라고 부름
    // x > 5 ? A : B
    // 조건 ? 참인 경우 : 거짓인 경우
    // x가 5보다 크다면? 참인 경우 : 거짓인 경우
    let ternaryResult = x > 5 ? "x는 5보다 크다." : "x는 5보다 작거나 같다.";

    return (
        <div>
            <h3>javascript 제어문 (if)</h3>

            <pre>{
                `
x = ${x}                            // 10
result = ${result}                  // x는 5보다 크다.
ternaryResult = ${ternaryResult}
                `
            }</pre>
        </div>
    )
}