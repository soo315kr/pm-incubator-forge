import './App.css'
import { ArraySliceExample } from './array/ArraySliceExample'
import { ArraySpliceExample } from './array/ArraySpliceExample'
import { ControlFlowFor } from './control_flow/ControlFlowFor'
import { ControlFlowForSumExample } from './control_flow/ControlFlowForSumExample'
import { ControlFlowForSummation } from './control_flow/ControlFlowForSummation'
import { ControlFlowIf } from './control_flow/ControlFlowIf'
import { ControlFlowIfSwitch } from './control_flow/ControlFlowSwitch'
import { VariableAndDataTypes } from './data_type/VariableAndDataTypes'
import { LogicalOperationExample } from './logical_operation/LogicalOperationExample'
import { MapExample } from './map/MapExample'
import { MapFilterExample } from './map/MapFilterExample'
import { MapReduceExample } from './map/MapReduceExample'
import { CalculationExample } from './math_operation/CalculationExample'
import { FirstProblem } from './problem/FirstProblem'
import { SecondProblem } from './problem/SecondProblem'

function App() {

  return (
    <>
      <div>
        <CalculationExample/>
        <VariableAndDataTypes/>        
        <LogicalOperationExample/>
        <ControlFlowIf/>
        <FirstProblem/>
        <ControlFlowIfSwitch/>
        <ControlFlowFor/>
        <ControlFlowForSummation/>
        <ControlFlowForSumExample/>
        <SecondProblem/>
        <MapExample/>
        <MapReduceExample/>
        <MapFilterExample/>
        <ArraySliceExample/>
        <ArraySpliceExample/>
      </div>
    </>
  )
}

export default App