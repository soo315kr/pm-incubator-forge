// z가 x 보다 크면 Hello, (x < z)
// z가 x 보다 작거나 같으면 Hi를 출력해주세요. (x >= z)

export const FirstProblem = () => {
    let x = 10;
    let z = 15;
    let result;

    if (x < z) {
        result = "Hello";
    } else {
        result = "Hi";
    }

    // if문 작성 요령
    // 1. 일단 if() {} 작성
    // 2. () 안에 조건식 작성
    // 3. {} 안에 조건식이 true일 때 실행할 코드 작성
    // 4. 필요시 else {} 작성
    // 5. else {} 안에 조건식이 false일 때 실행할 코드 작성

    // 삼항 연산자라고 부름
    // x < z ? A : B
    // 조건 ? 참인 경우 : 거짓인 경우
    // x가 z보다 작다면? 참인 경우 : 거짓인 경우
    let ternaryResult = x < z ? "Hello" : "Hi";

    return (
        <div>
            <h3>javascript 제어문 (if) - FirstProblem</h3>

            <pre>{
                `
x = ${x}                            // 10
z = ${z}                            // 15

result = ${result}                  // x는 z보다 작다. Hello
ternaryResult = ${ternaryResult}
                `
            }</pre>
        </div>
    )
}