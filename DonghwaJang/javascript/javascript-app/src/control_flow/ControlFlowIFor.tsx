export const ControlFlowFor = () => {
    let loopResultArray = []
    
    for (let i = 1; i< 3; i++){
        loopResultArray.push(i)
    }
    
    
    return (
        <div>
            <h3>javascript 제어문(switch)</h3>

            <pre>{
                `
loopResultArray = ${loopResultArray}

                `
            }</pre>
        </div>
    )
}










