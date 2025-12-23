import './App.css'

// 실행 방법: npm run dev
// 실행 이후 나타나는 Local: http://localhost:숫자/ 가 있음
// http://localhost:숫자/ 를 웹 브라우저에 입력해야 페이지가 보입니다.

// 그리고 현재 구성 특성 상 웹 브라우저를 그냥 켜놓고
// 코드만 바꾸면 알아서 페이지가 코드에 따라 변경됩니다.

// Ctrl + / 를 누르면 자동으로 특정 위치에서 사용할 수 있는 주석이 만들어짐
function App() {

  return (
    <>
      <div>
        {/* h1 태그는 제목을 표시할 때 사용합니다 */}
        {/* 숫자 크기에 따라 사이즈가 조정됩니다. */}
        <h1>First HTML5/CSS3</h1>
        <h2>First HTML5/CSS3</h2>
        <h3>First HTML5/CSS3</h3>
        <h4>First HTML5/CSS3</h4>
        <h5>First HTML5/CSS3</h5>
        <h6>First HTML5/CSS3</h6>

        {/* 주석 */}
        {/* 실제 여러 사람들과 개발 할 때 내 머리속의 생각이 공유되지 않기 때문 */}
        {/* 시간이 지나더라도 해당 파트가 무엇인지 기록을 해두기 위해 사용함. */}
        <p>단락 paragraph의 역할입니다.</p>

        {/* 리스트(list) */}
        {/* ul = unordered list */}
        <ul>
          <li>리스트 1</li>
          <li>리스트 2</li>
          <li>리스트 3</li>
          <li>리스트 4</li>
        </ul>

        {/* ol = ordered list */}
        <ol>
          <li>리스트 1</li>
          <li>리스트 2</li>
          <li>리스트 3</li>
          <li>리스트 4</li>
        </ol>

        {/* tailwindcss 같은 편리한 녀석들이 존재함 */}
        {/* html / css를 알고 쓰는 것과 차이가 있긴함 */}
        <div className="box">
          <h2>CSS 속성 적용</h2>
          <p>CSS는 HTML요소를 스타일링 하기 위한 목적으로 사용</p>

          {/* a href의 경우엔 하이퍼링크를 거는 부분 */}
          {/* 그렇기 때문에 'HTML/CSS 학습 사이트' 를 누르면 특정 사이트로 이동함 */}
          {/* target="_blank" 의 경우 새로운 탭에서 화면을 띄우는 것을 의미함 */}
          <a href='https://www.w3schools.com/'>
            HTML / CSS 학습 사이트
          </a>
        </div>
      </div>
    </>
  )
}

export default App
