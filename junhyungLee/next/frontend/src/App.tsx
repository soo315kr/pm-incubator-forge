import './App.css'

type Post = {
  id: number
  title: string
  author: string
  date: string
  views: number
}

const mockPosts: Post[] = [
  {
    id: 12,
    title: '신입 개발자 포트폴리오 피드백 부탁드립니다',
    author: 'june_dev',
    date: '2024-03-02',
    views: 482,
  },
  {
    id: 11,
    title: 'React 쿼리 캐싱 전략 공유합니다',
    author: 'frontend_park',
    date: '2024-02-28',
    views: 523,
  },
  {
    id: 10,
    title: 'Next.js 14 App Router 전환 후기',
    author: 'hkim',
    date: '2024-02-25',
    views: 731,
  },
  {
    id: 9,
    title: 'AWS 비용 최적화 팁 5가지',
    author: 'opslee',
    date: '2024-02-20',
    views: 398,
  },
  {
    id: 8,
    title: 'Side project 팀원 모집합니다 (디자이너/프론트)',
    author: 'collab_seo',
    date: '2024-02-18',
    views: 612,
  },
]

function App() {
  return (
    <div className="app">
      <header className="app__header">
        <h1>커뮤니티 게시판</h1>
        <p>Mock 데이터로 구성된 리스트 예시입니다.</p>
      </header>

      <section className="board">
        <div className="board__toolbar">
          <span className="board__count">총 {mockPosts.length}건</span>
          <button className="board__button" type="button">
            글쓰기
          </button>
        </div>

        <div className="board__table-wrapper">
          <table className="board__table">
            <thead>
              <tr>
                <th>No</th>
                <th>제목</th>
                <th>작성자</th>
                <th>작성일</th>
                <th>조회수</th>
              </tr>
            </thead>
            <tbody>
              {mockPosts.length === 0 ? (
                <tr>
                  <td colSpan={5} className="board__empty">
                    등록된 글이 없습니다.
                  </td>
                </tr>
              ) : (
                mockPosts.map((post) => (
                  <tr key={post.id}>
                    <td>{post.id}</td>
                    <td className="board__title">
                      <a href="#">{post.title}</a>
                    </td>
                    <td>{post.author}</td>
                    <td>{post.date}</td>
                    <td>{post.views.toLocaleString()}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}

export default App
