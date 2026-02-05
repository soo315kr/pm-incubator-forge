export const MapExample = () => {
    let number_array: number[] = [2,4,6,8,10]
    let square_result_array: number[] = number_array.map (num => num * num)

    return (
        <div>
            <h3>javascript Map(Hash 방식)</h3>

            <pre>{`
number_array = ${number_array}
square_result_array = ${square_result_array}
            `}</pre>
        </div>
    )
}