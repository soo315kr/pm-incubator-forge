export interface BoardItem {
  id: number;
  title: string;
  author: string;
  date: string;
  views: number;
  category?: string;
}

export const boardData: BoardItem[] = [
  { 
    id: 1, 
    title: 'React와 TypeScript를 활용한 프론트엔드 개발 가이드', 
    author: '김개발', 
    date: '2026-01-21', 
    views: 152,
    category: '개발'
  },
  { 
    id: 2, 
    title: 'Vite를 사용한 빠른 개발 환경 구축하기', 
    author: '이코딩', 
    date: '2026-01-20', 
    views: 89,
    category: '개발'
  },
  { 
    id: 3, 
    title: '게시판 UI/UX 디자인 베스트 프랙티스', 
    author: '박디자인', 
    date: '2026-01-19', 
    views: 234,
    category: '디자인'
  },
  { 
    id: 4, 
    title: 'Mock Data를 활용한 프론트엔드 테스트 전략', 
    author: '최테스트', 
    date: '2026-01-18', 
    views: 67,
    category: '테스트'
  },
  { 
    id: 5, 
    title: '컴포넌트 재사용성을 높이는 방법', 
    author: '정리팩', 
    date: '2026-01-17', 
    views: 198,
    category: '개발'
  },
  { 
    id: 6, 
    title: 'CSS Grid와 Flexbox 완벽 가이드', 
    author: '강스타일', 
    date: '2026-01-16', 
    views: 312,
    category: '디자인'
  },
  { 
    id: 7, 
    title: 'TypeScript 타입 안정성 확보하기', 
    author: '김타입', 
    date: '2026-01-15', 
    views: 145,
    category: '개발'
  },
  { 
    id: 8, 
    title: '반응형 웹 디자인 구현 팁', 
    author: '이반응', 
    date: '2026-01-14', 
    views: 276,
    category: '디자인'
  },
];
