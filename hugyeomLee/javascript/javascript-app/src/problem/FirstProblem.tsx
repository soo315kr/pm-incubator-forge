export const FirstProblem = () => {
    // z가 x보다 크면 Hello를 result에 할당
    // 그렇지 않으면 Hi를 result에 할당

    let x = 10;
    let z = 20;
    let result;
    
    if (x > z) {
        result = "Hello"
    } else {
        result = "Hi"
    }

    let ternaryResult = x > z ? "Hello" : "Hi"

    return (
        <div>
            <h3>Javascript 제어문 (if)</h3>

            <pre>{
                `
x = ${x}                         // 10
z = ${z}                         // 20
result = ${result}               // x는 z보다 작다. if-else 문 결과
ternaryResult = ${ternaryResult} // 삼항 연산자 결과
                `
            }</pre>
        </div>
    )
}