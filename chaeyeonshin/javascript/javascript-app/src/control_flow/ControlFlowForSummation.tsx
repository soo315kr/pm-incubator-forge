export const ControlFlowForSummation = () => {
    let loopResultArray = []

    // 누적치를 저장할 변수 선언 및 초기화
    // 초기화를 통해 NaN(Not a Number) 방지
    let summation = 0

    for (let i = 1; i <=3; i++) {
        loopResultArray.push(i)
    }

    // 누적치 계산
    for (let i =1; i <=3; i++) {
        // A += B  <=>  A = A + B (왼쪽 값과 오른쪽 값을 더한 값이 왼쪽 값이 된다.)
        // i-1 : 배열의 인덱스는 0부터 시작하기 때문에 i값에서 1을 뺌
        // loopResultArray[0] : 1
        // loopResultArray[1] : 2
        // loopResultArray[2] : 3
        summation += loopResultArray[i-1]
    }

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

