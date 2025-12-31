export const MapReduceExample = () => {
    let number_array: number[] = [2, 4, 6, 8, 10]

    // reduce의 경우엔 아래와 같이 연산됩니다
    // (누산 대상, 배열의 요소) => 누산 대상 + 배열 요소, 초기값)
    // accumulator의 시작값은 지정한 초기값으로 설정됨


    // 실행 효율 Te 관점
    // 앞서 만들었던 다소 복잡한 연산의 for loop 구성을 단순화 시킨 작업임
    let result_array: number =
        number_array.reduce((accumulator, element) => accumulator + element, 0)
    // 따라서, 위 예제는 2+4+6+8+10에 초기값이 더해지는 것 (초기값은 0,1,2,3....n 달라질 수 있다)

    
    return (
        <div>
            <h3>Javascript Reduce Function</h3>

            <pre>{
                `
number_array = ${number_array}
result_array = ${result_array}
                `
            }</pre>
        </div>
    )
}
