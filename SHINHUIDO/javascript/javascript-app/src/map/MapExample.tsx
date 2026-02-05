export const MapExample = () => {

  // 'nember[]' <- 이거는 typescript 특성을 가짐
  // 숫자 배열임을 명시하는 행위
   let number_array: number[] = [2, 4, 6, 8, 10]

  //  square(제곱) 결과 배열
  // number_array_map() 을 사용하면 아래와 같이 동작함
  // 1. number_array 내부에 요소들을 1개씩 꺼내옴.
  //  2. num이라는 것이 2,4,6,8,10 이 됨을 의미함
  // 3. => 를 통해 이 내용을 화살표 내용의 연산으로 적용함
  // num * num = 각 요소의 제곱
   let square_result_array: number[] = number_array. map(num => num * num)
    
  return (
        <div>
          <h3>javascript Map Function </h3>

            <pre>{
              `
number_array = ${number_array}
square_result_array = ${square_result_array}
              `                        
            }</pre>     
        </div>
    )
}
