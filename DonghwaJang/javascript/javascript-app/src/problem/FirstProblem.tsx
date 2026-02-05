export const FirstProblem = () => {
    let x = 7;
    let result;

    if(x > 6) {
        result = "hello"
    } else {
        result = "hi"
    }
    let ternaryResult = x > 6 ? "Hello" : "Hi"
    return (
        <div>
            <h3>javascript 제어문(if)</h3>

            <pre>{
                `
x = ${x}                                // 7
result = ${result}                      // Hello
ternary Result = ${ternaryResult}
                `
            }</pre>
        </div>
    )
}










