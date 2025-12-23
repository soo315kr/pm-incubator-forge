import './App.css'

// 실행 방법 : npm run dev
// 실행 이후 나타나는 local 주소에 접속

// 현재 구성 특성 상 웹 브라우저에 바로 코드가 반영됨

function App() {

  return (
    <>
      <div>
        {/* h1태그는 제목을 표시할 때 사용합니다. */}
        {/* 숫자 크기에 따라 사이즈가 변경됩니다. */}
        <h1>First HTML5/CSS3</h1>
        <h2>First HTML5/CSS3</h2>
        <h3>First HTML5/CSS3</h3>
        <h4>First HTML5/CSS3</h4>
        <h5>First HTML5/CSS3</h5>
        <h6>First HTML5/CSS3</h6>

        {/* 주석을 다는 이유 */}
        {/* 여러 사람들과 개발할 때 사람들과 생각 공유를 하기 위함 */}
        <p>단락 paragragh 설정입니다.</p>

        {/* 리스트(list) */}
        {/* ul = unordered list */}
          <ul>
          <li>리스트 아이템 1</li>
          <li>리스트 아이템 2</li>
          <li>리스트 아이템 3</li>
          <li>리스트 아이템 4</li>
        </ul>

        {/* ol = ordered list */}
        <ol>
          <li>리스트 아이템 1</li>
          <li>리스트 아이템 2</li>
          <li>리스트 아이템 3</li>
          <li>리스트 아이템 4</li>
        </ol>
      </div>
    </>
  )
}

export default App

