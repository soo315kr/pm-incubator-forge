export const SecondProblemVer2 = () => {
    // 3, 6, 9, 12, 15를 더한 결과를 출력해봅시다.
    // Q. 강사님 배열값이 너무 많게 되면 저렇게 쓰는 건 비효율적인가요?
    // A. 네 일일히 여기에 전부 적을 수는 없습니다.
    let LoopResultArray = [3, 6, 9, 12, 15]
    let summation = 0

    let count = 0;

    for (; count <= 4; count++) {
        summation += LoopResultArray[count]
    }

    return (
        <div>
            <h3>Javascript 제어문2 (for)</h3>

            <pre>{
                `
LoopResultArray = ${LoopResultArray}
summation = ${summation}
                `
            }</pre>
        </div>
    )
}
