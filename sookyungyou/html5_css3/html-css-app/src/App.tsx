import './App.css'

//실행방법: npm run dev
//실행 이후 나타나는 local: http://localhost:숫자/ 가 있음
//http://localhost:숫자/를 웹브라우저에 입력해야 페이지 보임

//그리고 현재 구성 특성 상 웹브라우저 그냥 켜놓고
//코드만 바꾸면 알아서 페이지가 코드에 따라서 변경됨 
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

        {/*ctr+/: 주석 */}
        {/* 실제로 사람들과 개발 진행 시 내 생각 공유x */}
        {/* 시간이 지나도 해당 파트가 무엇인지 기록하기 위해 사용 */}
        <p>단락 paragraph의 역할입니다.</p>
        {/* 리스트 (list) */}
        <li>리스트1</li>
        <li>리스트2</li>
        {/* ul: unordered list */}
        <ul>
          <li>리스트1</li>
          <li>리스트2</li>
          <li>리스트3</li>
         </ul>
         {/* ol: ordered list */}
         <ol>
          <li>리스트1</li>
          <li>리스트2</li>
          <li>리스트3</li>
         </ol>
         
        
      </div>
    </>
  )
}

export default App
