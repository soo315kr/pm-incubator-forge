import './App.css'
import { CalculationExample } from './math_operation/CalculationExample'

function App() {


  return (
    <>
      <div>
        <CalculationExample/>
        {/* 나만의 커스텀 태크 생성 */}
        {/* 이 커스텀 태그는 단순히 사칙연산+나머지(MOD) 연산 */}
        {/* 이와 같은 형태로 직접 커스텀 태그를 만들면 지저분해지는 상황 방지 가능 */}
        {/* 관심사의 분리 달성 가능 */}
      </div>
    </>
  )
}

export default App
