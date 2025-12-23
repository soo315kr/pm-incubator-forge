import './App.css'

// 실행 방법: npm run dev
// 실행 이후 나타나는 Local : http://localhost:숫자/ 가 있음
// http://localhost:숫자/ 를 웹 부라우저에 입력해야 페이지가 보임

// 현재 구성 특성상 웹 부라우저를 그냥 켜놓고
// 코드만 바꾸면 알아서 페이지가 코드에 따라 변경됨.

// Ctrl + / 를 누르면 자동으로 특정 위치에서 사용할 수 있는 주석이 만들어짐
function App() {
  
  return (
    <>
      <div>
        {/* h1 태그는 제목을 표시할때 사용. */}
        {/* 숫자 크기에 따라 사이즈가 조정됨. */}
        <h1>Frist HTML5/CSS3</h1>
        <h2>Frist HTML5/CSS3</h2>
        <h3>Frist HTML5/CSS3</h3>
        <h4>Frist HTML5/CSS3</h4>
        <h5>Frist HTML5/CSS3</h5>
        <h6>Frist HTML5/CSS3</h6>

        {/* 주석 */}
        {/* 실제 여러 사람들과 개발할 때 내 머리속의 생각이 공유되지 않기 때문 */}
        {/* 시간이 지나더라도 해당 파트가 무엇인지 기록해두기 위해 사용 */}
        <p>단락 paragraph의 역할입니다.</p>

        {/* 리스트(list) */}
        {/* ul = unordered list */}
        <ul>
          <li>리스트1</li>
          <li>리스트2</li>
          <li>리스트3</li>
          <li>리스트4</li>
        </ul>

        {/* ol = ordered list */}
        <ol>
        <ol>리스트1</ol>
        <ol>리스트2</ol>
        <ol>리스트3</ol>
        <ol>리스트4</ol>
      </div>
    </>
  ) 
}

export default App
