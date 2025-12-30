export const ControlFlowSumExample = () => {
    let loopResultArray = []
    let Summation = 0

    for (let i = 1, j = 1; j <= 3; i += 2, j++) {
        loopResultArray.push(i)
        Summation += loopResultArray[j - 1]
    }

    return (
        <div>
            <h3>javascript 제어문 (for)</h3>
            <pre>{
                `
loopResultArray = [${loopResultArray}]
Summation = ${Summation}
                `
            }</pre>
        </div>
    )
} 