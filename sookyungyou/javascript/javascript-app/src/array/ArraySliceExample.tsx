export const ArraySliceExample = () => {
    let number_array :number[] = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    
    let sliced_array: number[] =  number_array.slice(3, 7)
    // 위 코드는 number_array에서 
    // 3번 인덱스 ~ 6번 (7번 비포함) 인덱스까지 정보를 잘라서 가져옴
    // 8~14까지 
       
   

   
    return (
        <div>
            <h3>javascript Array Slice </h3>
            
            <pre>{
                `
number_array = ${number_array}
result_array = ${sliced_array}
                `        
    
             }</pre>
        </div>
    )
}