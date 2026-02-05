export const MapReduceExample = () => {
   let number_array: number[] = [2, 4, 6, 8, 10]

   let result_array: number = 
       number_array. reduce((accumulator, element) => accumulator + element, 0)
    
  return (
        <div>
          <h3>javascript Reduce Function </h3>

            <pre>{
              `
number_array = ${number_array}
result_array= ${result_array}
              `                        
            }</pre>     
        </div>
    )
}
