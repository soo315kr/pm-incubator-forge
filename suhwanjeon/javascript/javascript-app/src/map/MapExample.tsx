export const MapExample = () => {
    // 순수 javascript인 경우에 아래와 같이 표현해도 됩니다. 
    // let nubmer_array = [2, 4, 6, 8, 10] 
    // 저기 옆에 있는 ':number[]' -> 이건 뭐지?

    // 코드도 역시 모호하면 리스크가 있다. 
    // typescript라는 녀석은 type을 명시하는 작업입니다. 
    // 결론적으로 ':number[]'는 숫자 배열임을 명시하는 행위입니다. * [element, element, element]
    let numbber_array: number[] = [2, 4, 6, 8, 10]
    
    // square(제곰) 결과 배열
    // number_array.map()을 사용하면 아래와 같이 작동함. 

    // 1. number_array 내부에 요소들을 1개씩 꺼내옴. 
    // 2. element이라는 것이 2 혹은 4, 6, 8, 10이 됨을 의마함. 
    // 3. => 를 통해 이 내용을 화살표 내용의 연산으로 적용함을 의미함. 
    // element * element = 각 요소의 제곱 
    let square_result_array: number [] = numbber_array.map(element => element * element)
    
    return (
        <div> 
            <h3>javascript Map (Hash 방식)</h3>
            <pre>{
            `
number_array = ${numbber_array}
square_result_array = ${square_result_array}
            `   
            }</pre>
        </div>    
    )
}
 