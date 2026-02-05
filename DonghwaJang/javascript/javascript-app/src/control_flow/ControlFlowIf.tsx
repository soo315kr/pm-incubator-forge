export const ControlFlowIf = () => {
    let x = 10;
    let result;

    if(x > 5) {
        result = "x는 5보다 크다."
    } else {
        result = "x는 5보다 작다"
    }
    let ternaryResult = x > 5 ? "x는 5 보다 크다" : "x는 5 보다 작거나 같다."
    return (
        <div>
            <h3>javascript 제어문(if)</h3>

            <pre>{
                `
x = ${x}                                // 10
result = ${result}                      // x는 5 보다 크다.
ternary Result = ${ternaryResult}
                `
            }</pre>
        </div>
    )
}










