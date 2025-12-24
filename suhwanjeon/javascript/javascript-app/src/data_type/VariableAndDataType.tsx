export const VariableAndDataType = () => {
    let firstNumber = 10;
    const secondNumber = "Hello"
    var thridBoolean = true;
    let fourthNull = null
    let fifthUndefined = undefined;
    // Map 형식  
    // 사물함 열쇠 <- key 
    // 사물함 내용물 <- "value"
    let sixthMap = { key: "value" };
    
    // Array (배열) 형식
    // 1 ~ 1000까지 숫자를 적어야 할 때 
    // first, second, third, fourth, fifth, sixth
    // 일일히 변수 이름을 지정하려고 하면 피곤함.
    // 그러니 그냥 Array라는 배열을 하나 잡아높고 필요한 값들을 설정 
    let seventhArray = [1, 2, 3];
    
    return (
        <div>
            <h3>javascrpit 변수와 데이터 타입</h3>
            {/* Pre 태그 사이에 있는 내용드른 전체가 웹 페이지에 그대로 반영됩니다. */} 
            <pre>{
                `
                let firstNumber = ${firstNumber}            // number 타입 (숫자 타입)
                const secondNumber = "${secondNumber}"      // string 타입 (문자열 타입)
                var thridBoolean = ${thridBoolean}          // boolean 타입 (참/거짓 타입)
                let fourthNull = ${fourthNull}              // null 타입 (값이 없음)
                let fifthUndefined = ${fifthUndefined}      // undefined 타입 (정의되지 않음)
                let sixthMap = ${sixthMap}                  // object 타입 (객체 타입)
                let sixthMapJsonify = ${JSON.stringify(sixthMap)}  // object 타입 해석 (객체 타입) - JSON.stringify() 사용 시 문자열로 변환 (해석)
                let seventhArray = ${seventhArray}          // Array 타입 (배열 타입) 
                `
                
                }</pre>
        </div>
    )
}