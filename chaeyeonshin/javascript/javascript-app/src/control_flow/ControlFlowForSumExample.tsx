export const ControlFlowForSummExample = () => {
    let loopResultArray = []
    let summation = 0

    for (let i = 1, j = 1; i <= 5; i += 2, j++) {
        loopResultArray.push(i)
        summation += loopResultArray[j-1]
    }

    // i=1 j=1 -> loopResultArray[0] = 1 -> summation = 0 + 1 = 1
    // i=3 j=2 -> loopResultArray[1] = 3 -> summation = 1 + 3 = 4
    // i=5 j=3 -> loopResultArray[2] = 5 -> summation = 4 + 5 = 9

    // for (let i = 1, j = 1; j <= 3; i += 2, j++) {
    //     loopResultArray.push(i)
    //     summation += loopResultArray[j-1]
    // }    

    // for (let i = 1, j = 0; i <= 5; i += 2, j++) {
    //     loopResultArray.push(i)
    //     summation += loopResultArray[j]
    // }




    return (
        <div>
            <h3>javascript 제어문 (summation)</h3>

            <pre>{
                ` 
loopResultArray = ${loopResultArray}
summation = ${summation}
                `
            }</pre>
        </div>
    )
}

