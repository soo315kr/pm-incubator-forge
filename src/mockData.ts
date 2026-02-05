export interface BoardItem {
  id: number;
  title: string;
  author: string;
  date: string;
}

export const mockBoardData: BoardItem[] = [
  {
    id: 1,
    title: '첫 번째 게시글입니다.',
    author: '김철수',
    date: '2026-01-20',
  },
  {
    id: 2,
    title: '두 번째 게시글입니다.',
    author: '이영희',
    date: '2026-01-19',
  },
  {
    id: 3,
    title: '세 번째 게시글입니다.',
    author: '박찬호',
    date: '2026-01-18',
  },
  {
    id: 4,
    title: '네 번째 게시글입니다.',
    author: '최수영',
    date: '2026-01-17',
  },
  {
    id: 5,
    title: '다섯 번째 게시글입니다.',
    author: '정민아',
    date: '2026-01-16',
  },
];