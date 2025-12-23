import './App.css'

//실행 방법: Terminal창에서 npm run dev
//실행 이후 나타나는 Local: http://localhost:숫자가 있음
//http://localhost:숫자 를 복사해서 웹 브라우저에 띄운채로 코드 작업하고
// 실시간으로 페이지 변경 확인
// ctrl+/ 입력하면 해당 위치에서 사용가능한 주석 자동처리
function App() {

  return (
    <>
      <div>
        {/*h1~h5는 제목의 크기 */}
        <h1>First HTML5/CSS3</h1>
        <h2>First HTML5/CSS3</h2>
        <h3>First HTML5/CSS3</h3>
        <h4>First HTML5/CSS3</h4>
        <h5>First HTML5/CSS3</h5>
        
        {/*p는 단락표시 */}
        <p>단락 paragraph의 역할입니다.</p>
        {/*리스트(list) unordered list(순서가 X)*/}
        <ul>
          <li>리스트 1</li>
          <li>리스트 2</li>
          <li>리스트 3</li>
          <li>리스트 4</li>
        </ul>
        {/*리스트(list) ordered list(순서가 O)*/}
        <ol>
          <li>리스트 1</li>
          <li>리스트 2</li>
          <li>리스트 3</li>
          <li>리스트 4</li>
        </ol>
      </div>
      
    </>
  )
}

export default App
