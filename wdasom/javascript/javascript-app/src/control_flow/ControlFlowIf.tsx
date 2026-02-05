export const ControlFlowIF = () => {
    let x = 10;
    let resurlt;

    if (x >5) {
        result = "x는 5보다 크다."
    } elss {
        result = "x는 5 보다 작다."
    }

    let ternaryResult = x > 5 ? "X는 5보다 크다" : "X는 5보다 작거나 같다."

    return (
        <div>
            <h3>javascript 제어문 (if)</h3> 

            <Pre>{
                '

X = ${X}                            //10 
result = ${result}                  // X는 5보다 크다. 
ternayReslt = ${ternaryResult} 
               '
            }</Pre>        
        </div>
    )
}