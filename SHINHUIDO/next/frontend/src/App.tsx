import './App.css'

type Post = {
  id: number
  title: string
  author: string
  category: string
  createdAt: string
  views: number
  comments: number
}

const mockPosts: Post[] = [
  {
    id: 132,
    title: 'Next.js 15 업그레이드 가이드 정리',
    author: '김프론트',
    category: '공지',
    createdAt: '2026-01-18',
    views: 1823,
    comments: 12,
  },
  {
    id: 131,
    title: '프로덕트 디자인 시스템 구축 경험 공유',
    author: '박디자',
    category: '노하우',
    createdAt: '2026-01-16',
    views: 984,
    comments: 4,
  },
  {
    id: 130,
    title: 'React 서버 컴포넌트 적용 후기',
    author: '최개발',
    category: '후기',
    createdAt: '2026-01-15',
    views: 1120,
    comments: 9,
  },
  {
    id: 129,
    title: 'CI/CD 파이프라인 속도 개선 팁',
    author: '이DevOps',
    category: '노하우',
    createdAt: '2026-01-14',
    views: 723,
    comments: 3,
  },
  {
    id: 128,
    title: '모의 면접 스터디 모집합니다',
    author: '문스터디',
    category: '모집',
    createdAt: '2026-01-12',
    views: 645,
    comments: 7,
  },
  {
    id: 127,
    title: '데이터 시각화 라이브러리 추천 리스트',
    author: '양데이터',
    category: '자료',
    createdAt: '2026-01-10',
    views: 531,
    comments: 5,
  },
  {
    id: 126,
    title: 'PM을 위한 SQL 쿼리 작성법',
    author: '안PM',
    category: '가이드',
    createdAt: '2026-01-09',
    views: 817,
    comments: 6,
  },
  {
    id: 125,
    title: '신규 멤버 온보딩 체크리스트 공유',
    author: '정리더',
    category: '자료',
    createdAt: '2026-01-07',
    views: 402,
    comments: 2,
  },
]

function App() {
  return (
    <div className="page">
      <header className="page__header">
        <div>
          <p className="eyebrow">Mock 데이터 기반</p>
          <h1 className="title">게시판 리스트</h1>
          <p className="subtitle">
            더미 데이터를 이용해 게시글 목록을 테이블로 출력한 예제입니다.
          </p>
        </div>
        <div className="actions">
          <input
            aria-label="검색"
            type="search"
            placeholder="제목 또는 작성자 검색"
            className="search"
          />
          <button className="primary">새 글 작성</button>
        </div>
      </header>

      <section className="board">
        <div className="board__meta">
          <span className="badge">총 {mockPosts.length}건</span>
          <span className="divider" />
          <span className="caption">최신순 정렬</span>
        </div>
        <div className="table">
          <div className="table__head">
            <span>No.</span>
            <span>제목</span>
            <span>작성자</span>
            <span>카테고리</span>
            <span>등록일</span>
            <span>조회</span>
            <span>댓글</span>
          </div>
          <div className="table__body">
            {mockPosts.map((post) => (
              <div className="table__row" key={post.id}>
                <span className="muted">#{post.id}</span>
                <div className="title-cell">
                  <p className="post-title">{post.title}</p>
                </div>
                <span>{post.author}</span>
                <span>
                  <span className="chip">{post.category}</span>
                </span>
                <span className="muted">{post.createdAt}</span>
                <span>{post.views.toLocaleString()}</span>
                <span>{post.comments}</span>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

export default App
