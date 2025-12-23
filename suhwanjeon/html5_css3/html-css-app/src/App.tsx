import './App.css'

// 실행 방법: npm run dev 
// 실행 이후 나타나는 Local:http://localhost:숫자/ 가 있음
// http://localhost:숫자/ 를 웹 브라우저에 입력해야 페이지가 보입니다.

// 그리고 현재 구성 특성 상 웹 브라우저를 그냥 켜놓고
//코드만 바꾸면 알아서 페이지가 코드에 따라 변경됩니다. 

// Cmd + / 를 누르면 자동으로 특정 위치에서 사용할 수 있는 주석이 만들어짐 
function App() {

  return (
    <>
      <div>
        {/* h1 태그는 제목을 표시할 때 사용합니다 */}
        {/* 숫자 크기에 따라 사이즈가 조정됩니다. */}
      <h1>First HTML5/CSS3</h1>
      <h2>Second HTML5/CSS3</h2>
      <h3>Third HTML5/CSS3</h3>
      <h4>Fourth HTML5/CSS3</h4>
      <h5>Fifth HTML5/CSS3</h5>
      <h6>Sixth HTML5/CSS3</h6>

      {/* 주석 */}
      {/* 주석을 다는 이유: 여러 사람들과 개발 할 때 내 머리속의 생각이 공유되지 않기 때문 */}
      {/* 시간이 지나더라도 해당 파트가 무엇인지 기록을 해두기 위해 사용함. */}
      <p>단락 paragraph의 역할입니다.</p>
      
      {/* 리스트(List) */}
      {/* ul = unorded list = 순서 없는 리스트 */}
      <ul>
        <li>리스트 아이템 1</li>
        <li>리스트 아이템 2</li>
        <li>리스트 아이템 3</li>
      </ul>

      {/* ol = ordered list = 순서 있는 리스트 */}
      <ol>
        <li>순서 있는 리스트 아이템 1</li>
        <li>순서 있는 리스트 아이템 2</li>
        <li>순서 있는 리스트 아이템 3</li>
      </ol>

      </div>
    </>
  )
}

export default App
