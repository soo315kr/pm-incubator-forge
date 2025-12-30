import './App.css'
import { VariableAndDataTypes } from './data_type/VariableAndDataTypes'
import { CalculationExample } from './math_operation/CalculationExample'
import { LogicalOperationExample } from './logical_operation/LogicalOperationExample'
import { ControlFlowIf } from './control_flow/ControlFlowIf'
import { FristProblem } from './assets/problem/FristProblem'
import { ControlFlowSwitch } from './control_flow/ControlFlowSwitch'
import { ControlFlowFor } from './control_flow/ControlFlowFor'
import { ControlFlowSummation } from './control_flow/ControlFlowSummation'
import { ControlFlowSumExample } from './control_flow/ControlFlowSumExample'

function App() {

  return (
    <>
      <div>
        <CalculationExample/>
        <VariableAndDataTypes/>
        <LogicalOperationExample/>
        <ControlFlowIf/>
        <FristProblem/>
        <ControlFlowSwitch/>
        <ControlFlowFor/>
        <ControlFlowSummation/>
        <ControlFlowSumExample/>
      </div>
    </>
  )
}

export default App 