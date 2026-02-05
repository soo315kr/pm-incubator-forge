export const SecondProblem = () => {
    let loopResultArray = []
    let summation = 0
    

    for (let number = 3, count = 1; number <= 15; number +=3, count++) {
        loopResultArray.push(number)
        summation += number
    }

  return (
        <div>
          <h3>javascript 제어문 (for)</h3>

            <pre>{
              `
loopResultArray = ${loopResultArray}   
summation = ${summation}                        
              `                        
            }</pre>     
        </div>
    )
}
