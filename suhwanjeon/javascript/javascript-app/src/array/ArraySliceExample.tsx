export const ArraySliceExample = () => {
    let number_array: number[] = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

    // 제가 이전 sliceExample에서 살짝 놓쳐서 질문드립니다. 3번 인덱스 포함(이상)부터  7번 인덱스 미포함(미만)이 맞을까요? 네, 맞습니다.  
    // 이 문법이 헷갈립니다. 그런데  3=< x < 7이 맞습니다. 
    let sliced_array: number [] = number_array.slice(3, 7)
    
    return (
        <div> 
            <h3>javascript Array Slice</h3>
            
            <pre>{
                `
number_array = ${number_array}
sliced_array = ${sliced_array}
                `   
            }</pre>
        </div>    
    )
}
 