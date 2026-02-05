import './App.css'

const stats = [
  {
    label: '이번 주 신청',
    sub: 'Weekly signups',
    value: '48',
  },
  {
    label: '참석률',
    sub: 'Attendance rate',
    value: '92%',
  },
  {
    label: '만족도',
    sub: 'Satisfaction score',
    value: '4.7/5',
  },
  {
    label: '신고 건수',
    sub: 'Reports',
    value: '2',
    tone: 'danger',
  },
]

const meetups = [
  {
    title: '정원 산책과 차 한잔',
    subtitle: 'Garden walk & tea',
    time: '2월 6일(목) 14:00',
    capacity: '8/12',
    approvals: '승인 대기 2',
  },
  {
    title: '클래식 음악 감상',
    subtitle: 'Classical listening',
    time: '2월 8일(토) 10:30',
    capacity: '12/12',
    approvals: '대기 없음',
  },
  {
    title: '사진으로 나누는 추억',
    subtitle: 'Memory sharing',
    time: '2월 10일(월) 15:00',
    capacity: '6/12',
    approvals: '승인 대기 1',
  },
]

const participants = [
  {
    name: '박은정',
    ageBand: '70대 초반',
    gender: '여성',
    interests: '산책, 클래식',
    mobility: '보조기구 사용',
  },
  {
    name: '이성호',
    ageBand: '60대 후반',
    gender: '남성',
    interests: '사진, 지역 역사',
    mobility: '보행 가능',
  },
  {
    name: '김정수',
    ageBand: '80대 초반',
    gender: '남성',
    interests: '바둑, 책',
    mobility: '휠체어',
  },
]

const reports = [
  {
    id: 'R-204',
    title: '금전 요청으로 불편함',
    detail: '참여 중 개인 연락처 교환 후 금전 부탁 언급',
    status: '검토중',
  },
  {
    id: 'R-205',
    title: '예의 부족한 발언',
    detail: '대화 중 반복적 무례함',
    status: '주의 필요',
  },
]

const meetupsParticipant = [
  {
    title: '가벼운 스트레칭과 대화',
    subtitle: 'Movement & talk',
    time: '2월 7일(금) 10:00',
    status: '모집중',
  },
  {
    title: '센터 작은 전시 투어',
    subtitle: 'Center mini tour',
    time: '2월 9일(일) 13:30',
    status: '마감 임박',
  },
]

function App() {
  return (
    <div className="app">
      <header className="hero">
        <div className="hero__top">
          <span className="eyebrow">Senior Community Program</span>
          <h1>
            센터 운영 안전 커뮤니티 모임
            <small>Center-run social meetups</small>
          </h1>
          <p className="subtitle">
            따뜻하고 안전한 만남을 위해, 모든 첫 만남은 센터에서 진행하며
            직원이 1:1 요청을 승인합니다.
          </p>
        </div>
        <div className="policy-banner">
          <strong>금전 교류 금지</strong>
          <span>No money exchange policy</span>
          <button className="link">불편함 신고하기</button>
        </div>
      </header>

      <section className="system">
        <div className="section-title">
          <h2>
            디자인 시스템
            <small>Design system</small>
          </h2>
          <p>큰 글자, 높은 대비, 편안한 여백을 기준으로 구성했습니다.</p>
        </div>
        <div className="system__grid">
          <div className="card">
            <h3>타이포그래피</h3>
            <ul className="type-scale">
              <li>
                <span className="type-label">Heading XL</span>
                <span className="type-sample type-xl">모임 일정</span>
              </li>
              <li>
                <span className="type-label">Heading L</span>
                <span className="type-sample type-lg">참가 신청</span>
              </li>
              <li>
                <span className="type-label">Body</span>
                <span className="type-sample type-body">
                  센터에서 진행하는 안전한 교류 모임입니다
                </span>
              </li>
              <li>
                <span className="type-label">Caption</span>
                <span className="type-sample type-caption">
                  No money exchange
                </span>
              </li>
            </ul>
          </div>
          <div className="card">
            <h3>컬러 팔레트</h3>
            <div className="swatches">
              <div className="swatch swatch--primary">
                Primary
                <small>#1E4DB7</small>
              </div>
              <div className="swatch swatch--accent">
                Accent
                <small>#F97316</small>
              </div>
              <div className="swatch swatch--warm">
                Warm
                <small>#FFEFD6</small>
              </div>
              <div className="swatch swatch--danger">
                Safety
                <small>#E11D48</small>
              </div>
              <div className="swatch swatch--neutral">
                Neutral
                <small>#F8FAFC</small>
              </div>
            </div>
          </div>
          <div className="card">
            <h3>버튼 & 폼</h3>
            <div className="button-row">
              <button className="button button--primary">모임 참가 신청</button>
              <button className="button button--ghost">센터 문의</button>
            </div>
            <div className="field">
              <label>관심사</label>
              <input placeholder="예: 산책, 음악 감상" />
            </div>
            <div className="chips">
              <span className="chip">대화</span>
              <span className="chip">정원</span>
              <span className="chip chip--outline">모임 알림</span>
            </div>
          </div>
        </div>
      </section>

      <section className="views">
        <div className="section-title">
          <h2>
            관리자 + 참여자 화면
            <small>Admin & participant views</small>
          </h2>
          <p>모바일 중심으로 설계하고, 관리자 화면은 데스크톱에서 확장됩니다.</p>
        </div>
        <div className="views__grid">
          <section className="panel">
            <header className="panel__header">
              <h3>
                직원 콘솔
                <small>Staff console</small>
              </h3>
              <div className="panel__actions">
                <button className="button button--primary">모임 만들기</button>
                <button className="button button--ghost">신고 보기</button>
              </div>
            </header>
            <div className="panel__body">
              <div className="login card card--muted">
                <div>
                  <strong>직원 로그인</strong>
                  <p>센터 계정으로 안전하게 로그인하세요.</p>
                </div>
                <button className="button button--primary">로그인</button>
              </div>
              <div className="stats">
                {stats.map((stat) => (
                  <div
                    key={stat.label}
                    className={`stat ${stat.tone === 'danger' ? 'stat--danger' : ''}`}
                  >
                    <span>{stat.label}</span>
                    <strong>{stat.value}</strong>
                    <small>{stat.sub}</small>
                  </div>
                ))}
              </div>
              <div className="card">
                <div className="card__title">
                  <h4>다가오는 모임</h4>
                  <button className="link">전체보기</button>
                </div>
                <ul className="list">
                  {meetups.map((meetup) => (
                    <li key={meetup.title}>
                      <div>
                        <strong>{meetup.title}</strong>
                        <small>{meetup.subtitle}</small>
                        <span>{meetup.time}</span>
                      </div>
                      <div className="meta">
                        <span className="pill">{meetup.capacity}</span>
                        <span className="pill pill--muted">
                          {meetup.approvals}
                        </span>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="card">
                <div className="card__title">
                  <h4>모임 만들기</h4>
                  <small>안전 정책을 자동으로 안내합니다</small>
                </div>
                <div className="form-grid">
                  <div className="field">
                    <label>날짜/시간</label>
                    <input placeholder="2월 12일(수) 14:00" />
                  </div>
                  <div className="field">
                    <label>테마</label>
                    <input placeholder="예: 전통 차 이야기" />
                  </div>
                  <div className="field">
                    <label>장소</label>
                    <input placeholder="센터 2층 모임실" />
                  </div>
                  <div className="field">
                    <label>정원</label>
                    <input placeholder="최대 12명" />
                  </div>
                  <div className="field field--full">
                    <label>안전 메모</label>
                    <textarea placeholder="금전 교류 금지 안내 및 센터 규칙" />
                  </div>
                </div>
                <div className="policy-card">
                  <strong>안전 정책 안내</strong>
                  <span>첫 만남은 센터에서 그룹으로 진행됩니다.</span>
                </div>
              </div>

              <div className="card">
                <div className="card__title">
                  <h4>참여자 데이터베이스</h4>
                  <small>최소 정보만 표시됩니다</small>
                </div>
                <div className="filters">
                  <button className="chip">60대</button>
                  <button className="chip">70대</button>
                  <button className="chip">80대</button>
                  <button className="chip chip--outline">이동 지원</button>
                </div>
                <div className="table">
                  {participants.map((person) => (
                    <div className="table__row" key={person.name}>
                      <div>
                        <strong>{person.name}</strong>
                        <small>센터 연락 담당</small>
                      </div>
                      <span>{person.ageBand}</span>
                      <span>{person.gender}</span>
                      <span>{person.interests}</span>
                      <span>{person.mobility}</span>
                      <button className="link">프로필</button>
                    </div>
                  ))}
                </div>
              </div>

              <div className="card">
                <div className="card__title">
                  <h4>그룹 구성 / 좌석 배치</h4>
                  <small>균형 힌트를 제공합니다</small>
                </div>
                <div className="seating">
                  {Array.from({ length: 8 }).map((_, index) => (
                    <button className="seat" key={`seat-${index}`}>
                      {index + 1}
                    </button>
                  ))}
                </div>
                <div className="hint">
                  <strong>균형 제안</strong>
                  <span>연령대가 고르게 섞이도록 배치해 주세요.</span>
                </div>
              </div>

              <div className="card">
                <div className="card__title">
                  <h4>출석 체크</h4>
                  <small>현장 확인용 리스트</small>
                </div>
                <div className="checklist">
                  {['박은정', '이성호', '김정수', '최미영'].map((name) => (
                    <label key={name} className="checklist__item">
                      <input type="checkbox" defaultChecked={name === '박은정'} />
                      <span>{name}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="card">
                <div className="card__title">
                  <h4>피드백 요약</h4>
                  <small>모임 이후 바로 확인</small>
                </div>
                <div className="metrics">
                  <div>
                    <strong>만족</strong>
                    <span className="metric">88%</span>
                  </div>
                  <div>
                    <strong>다시 참여</strong>
                    <span className="metric">76%</span>
                  </div>
                  <div>
                    <strong>1:1 요청</strong>
                    <span className="metric">4명</span>
                  </div>
                </div>
                <button className="button button--ghost">
                  1:1 요청 검토 (센터 승인 필요)
                </button>
              </div>

              <div className="card">
                <div className="card__title">
                  <h4>신고 & 안전</h4>
                  <small>금전 교류 금지 정책</small>
                </div>
                <div className="policy-banner policy-banner--compact">
                  <strong>금전 교류는 금지됩니다</strong>
                  <span>Report concerns any time</span>
                </div>
                <ul className="reports">
                  {reports.map((report) => (
                    <li key={report.id}>
                      <div>
                        <strong>{report.title}</strong>
                        <small>{report.detail}</small>
                      </div>
                      <div className="actions">
                        <span className="pill">{report.status}</span>
                        <button className="button button--ghost">조치</button>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </section>

          <section className="panel panel--participant">
            <header className="panel__header">
              <h3>
                참여자 화면
                <small>Participant view</small>
              </h3>
              <button className="button button--primary">모임 참가 신청</button>
            </header>
            <div className="panel__body">
              <div className="card card--highlight">
                <h4>다음 모임</h4>
                <p>센터에서 진행하는 안전한 교류 모임입니다.</p>
                <div className="card__cta">
                  <span>2월 6일(목) 14:00 · 센터 2층</span>
                  <button className="button button--primary">참가</button>
                </div>
              </div>
              <div className="card">
                <div className="card__title">
                  <h4>모임 둘러보기</h4>
                  <small>Browse meetups</small>
                </div>
                <div className="meetup-cards">
                  {meetupsParticipant.map((item) => (
                    <article key={item.title} className="meetup-card">
                      <div>
                        <strong>{item.title}</strong>
                        <small>{item.subtitle}</small>
                        <span>{item.time}</span>
                      </div>
                      <span className="pill pill--accent">{item.status}</span>
                    </article>
                  ))}
                </div>
              </div>
              <div className="card">
                <div className="card__title">
                  <h4>참가 신청</h4>
                  <small>짧고 간단한 신청서</small>
                </div>
                <div className="form-grid">
                  <div className="field">
                    <label>이름 또는 별명</label>
                    <input placeholder="홍길동" />
                  </div>
                  <div className="field">
                    <label>연령대</label>
                    <input placeholder="70대" />
                  </div>
                  <div className="field field--full">
                    <label>관심사</label>
                    <div className="chips">
                      <button className="chip">산책</button>
                      <button className="chip">음악</button>
                      <button className="chip">책</button>
                      <button className="chip chip--outline">직접 입력</button>
                    </div>
                  </div>
                  <div className="field">
                    <label>이동 지원</label>
                    <input placeholder="보행 가능" />
                  </div>
                  <div className="field field--full">
                    <label className="checkbox">
                      <input type="checkbox" />
                      <span>
                        금전 교류 금지 정책에 동의합니다
                        <small>No money exchange</small>
                      </span>
                    </label>
                  </div>
                </div>
                <button className="button button--primary">모임 참가 신청</button>
              </div>
              <div className="card">
                <div className="card__title">
                  <h4>내 모임</h4>
                  <small>My meetup</small>
                </div>
                <div className="my-meetup">
                  <div>
                    <strong>2월 6일(목) 14:00</strong>
                    <span>센터 2층 모임실</span>
                  </div>
                  <div className="button-row">
                    <button className="button button--ghost">참가 취소</button>
                    <button className="button button--primary">센터 문의</button>
                  </div>
                </div>
              </div>
              <div className="card">
                <div className="card__title">
                  <h4>모임 후 설문</h4>
                  <small>3문항으로 간단히</small>
                </div>
                <div className="survey">
                  <label>
                    만족하셨나요?
                    <div className="survey__options">
                      <button className="chip">매우 만족</button>
                      <button className="chip">보통</button>
                      <button className="chip">아쉬움</button>
                    </div>
                  </label>
                  <label>
                    다시 참여하고 싶나요?
                    <div className="survey__options">
                      <button className="chip">예</button>
                      <button className="chip">아니오</button>
                    </div>
                  </label>
                  <label>
                    더 대화하고 싶은 분이 있나요? (좌석 번호 선택)
                    <input placeholder="예: 3번 좌석" />
                  </label>
                </div>
                <button className="button button--primary">제출</button>
              </div>
              <div className="card card--danger">
                <div className="card__title">
                  <h4>안전 & 정책</h4>
                  <small>Safety & policy</small>
                </div>
                <p>금전 교류는 금지됩니다. 불편함이 있으면 바로 알려주세요.</p>
                <button className="button button--ghost">불편함 신고하기</button>
              </div>
            </div>
          </section>
        </div>
      </section>

      <section className="prototype">
        <div className="section-title">
          <h2>
            클릭 가능한 프로토타입 흐름
            <small>Prototype flows</small>
          </h2>
        </div>
        <div className="prototype__grid">
          <div className="card">
            <h3>직원 흐름</h3>
            <ol className="flow">
              <li>대시보드</li>
              <li>모임 만들기</li>
              <li>그룹 구성</li>
              <li>출석 체크</li>
              <li>피드백 요약</li>
              <li>신고 처리</li>
            </ol>
          </div>
          <div className="card">
            <h3>참여자 흐름</h3>
            <ol className="flow">
              <li>홈</li>
              <li>모임 신청</li>
              <li>내 모임</li>
              <li>모임 후 설문</li>
              <li>불편함 신고</li>
            </ol>
          </div>
        </div>
      </section>
    </div>
  )
}

export default App
