import './App.css'

//실행 방법 : npm run dev

function App() {

  return (
    <>
      <div> 
        {/* h1 태그는 제목을 표시할 때 사용합니다 */}
        {/* 숫자 크기에 따라 사이즈가 조정됩니다. */}
        <h1>First HTMLS/CSS3</h1>
        <h2>First HTMLS/CSS3</h2>
        <h3>First HTMLS/CSS3</h3>
        <h4>First HTMLS/CSS3</h4>
        <h5>First HTMLS/CSS3</h5>
        <h6>First HTMLS/CSS3</h6>

        {/*주석*/}
        {/*실제 여러 사람들과 개발 할 때 내 머리속의 생각이 공유되지 않기 때문*/}
        {/*시간이 지나도 해당 파트가 무엇인지 기록을 해두기 위해 사용함. */}
        <p>단락 paragraph의 역할입니다.</p>

        {/* 리스트(list) */}
        {/* ul = unordered list) */}
        <ul>
          <li>리스트 1 </li>
          <li>리스트 2 </li>
          <li>리스트 3 </li>
          <li>리스트 4 </li>
        </ul>
      
      {/* ol = ordered list) */}
      <ol>
          <li>리스트 1 </li>
          <li>리스트 2 </li>
          <li>리스트 3 </li>
          <li>리스트 4 </li>
      </ol>
      </div>
    </>
  )
}

export default App
