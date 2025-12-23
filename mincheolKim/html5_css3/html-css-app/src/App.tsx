import './App.css'

// 실행 방법: npm run dev
// 실행 이후 나타나는 Local: http://localhost:숫자/ 가 있음
// http://localhost:숫자/ 접속
// 맨 처음 숫자는 5173으로 나오는데 만약 5173이 이미 사용 중이라면 5174, 5175... 순으로 올라감

// 그리고 현재 구성 특성 상 웹 브라우저를 그냥 켜놓고
// 코드만 바꾸면 페이지가 자동으로 새로고침 된다.

// HTML (HyperText Markup Language)
// 하이퍼텍스트 마크업 언어
// 웹 페이지를 만들기 위한 언어
// 문서의 구조를 정의하고 내용을 표시하는 데 사용

function App() {

  return (
    <>
      <div>
        {/* h1 태그는 제목을 표시할 때 사용합니다. */}
        {/* 숫자 크기에 따라 사이즈가 조정됩니다. */}
        <h1>First HTML/CSS3</h1>
        <h2>First HTML/CSS3</h2>
        <h3>First HTML/CSS3</h3>
        <h4>First HTML/CSS3</h4>
        <h5>First HTML/CSS3</h5>
        <h6>First HTML/CSS3</h6>

        {/* 주석 */}
        {/* 실제 여러 사람들과 개발 할 때 내 머릿속의 생각이 공유되지 않기 때문 */}
        <p>단락 paragraph의 역할이다.</p>

        {/* 리스트(list) */}
        {/* ul = unordered list: 순서가 없는 리스트 */}
        <ul>
          <li>리스트 1</li>
          <li>리스트 2</li>
          <li>리스트 3</li>
        </ul>

        {/* ol = ordered list: 순서가 있는 리스트 */}
        <ol>
          <li>리스트 1</li>
          <li>리스트 2</li>
          <li>리스트 3</li>
        </ol>
      </div>
    </>
  )
}

export default App
