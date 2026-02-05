export const ArraySpliceExample = () => {
   let number_array: number[] = [ 4, 6, 8, 10, 12, 14, 16, 18, 20]
   let spliced_array: number[] = [...number_array]

   spliced_array.splice(3, 1, 777)
    
   let second_spliced_array: number[] = [...number_array]
   second_spliced_array.splice(4, 3, 0)

  return (
        <div>
          <h3>javascript Array Slice </h3>

            <pre>{
              `
number_array = ${number_array}
spliced_array = ${spliced_array}
second_spliced_array = ${second_spliced_array}
              `                        
            }</pre>     
        </div>
    )
}
