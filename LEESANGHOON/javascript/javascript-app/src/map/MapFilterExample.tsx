// 3 6 9 12 15 더한 결과 출력

export const MapFilterExample = () =>{

    // number[] : typescript 특성(type을 명시하는 작업, 숫자 배열임을 의미)
    // number_array.map(): 배열 안의 요소들을 1개씩 꺼내옴 2,4,6,8,10 -> 각 요소의 제곱을 함
    let number_array: number[] = [2,4,6,8,10]

    let result_array: number[] =
        number_array.filter(element => element % 4 === 0)


return(
    <div>
    <h3>javascript Filter Function</h3>
        <pre>{
    `
number_array = ${number_array}
result_array = ${result_array}


    `
        }</pre>
    </div>
)
}