import './App.css'

type Post = {
  id: number
  title: string
  author: string
  createdAt: string
  views: number
  comments: number
}

const mockPosts: Post[] = [
  {
    id: 101,
    title: 'React로 게시판 만들 때 알아두면 좋은 팁 7가지',
    author: '홍길동',
    createdAt: '2025-12-28',
    views: 1240,
    comments: 12,
  },
  {
    id: 100,
    title: 'Next.js 15 미리 써본 후기',
    author: '이서연',
    createdAt: '2025-12-24',
    views: 980,
    comments: 8,
  },
  {
    id: 99,
    title: 'Vite + TypeScript 환경에서 ESLint 빠르게 잡기',
    author: '박민수',
    createdAt: '2025-12-20',
    views: 765,
    comments: 5,
  },
  {
    id: 98,
    title: 'UI/UX 관점에서 본 게시판 목록 정렬 기준',
    author: '정유진',
    createdAt: '2025-12-18',
    views: 512,
    comments: 3,
  },
  {
    id: 97,
    title: 'Mock 데이터로 프론트엔드 빠르게 프로토타이핑하기',
    author: '김도윤',
    createdAt: '2025-12-15',
    views: 468,
    comments: 6,
  },
]

function App() {
  return (
    <div className="page">
      <header className="page__header">
        <div>
          <p className="page__eyebrow">Mock Data · 게시판</p>
          <h1 className="page__title">프론트엔드 게시글 목록</h1>
          <p className="page__description">
            API 없이도 빠르게 리스트 UI를 확인할 수 있도록 더미 데이터를 사용했어요.
          </p>
        </div>
        <button className="primary-button" type="button">
          글쓰기
        </button>
      </header>

      <section className="card">
        <div className="card__header">
          <div>
            <p className="card__eyebrow">전체 {mockPosts.length}건</p>
            <h2 className="card__title">최신 순</h2>
          </div>
          <div className="legend">
            <span className="legend__dot" />
            Mock 데이터로만 렌더링된 리스트입니다
          </div>
        </div>

        <div className="table">
          <div className="table__head">
            <div className="table__row">
              <div className="col col--id">번호</div>
              <div className="col col--title">제목</div>
              <div className="col col--author">작성자</div>
              <div className="col col--date">작성일</div>
              <div className="col col--stats">조회/댓글</div>
            </div>
          </div>
          <div className="table__body">
            {mockPosts.map((post) => (
              <div className="table__row" key={post.id}>
                <div className="col col--id">#{post.id}</div>
                <div className="col col--title">
                  <a className="title-link" href="#">
                    {post.title}
                  </a>
                </div>
                <div className="col col--author">{post.author}</div>
                <div className="col col--date">
                  {new Date(post.createdAt).toLocaleDateString('ko-KR', {
                    month: '2-digit',
                    day: '2-digit',
                  })}
                </div>
                <div className="col col--stats">
                  <span className="badge badge--views">{post.views} 조회</span>
                  <span className="badge badge--comments">
                    {post.comments} 댓글
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

export default App
