import React from 'react';
import { BoardItem, mockBoardData } from '../mockData';
import './BoardList.css'; // Assuming you'll want some basic styling

const BoardList: React.FC = () => {
  return (
    <div className="board-list-container">
      <h1>게시판</h1>
      <div className="board-header">
        <span className="board-header-id">번호</span>
        <span className="board-header-title">제목</span>
        <span className="board-header-author">작성자</span>
        <span className="board-header-date">작성일</span>
      </div>
      {mockBoardData.map((item: BoardItem) => (
        <div key={item.id} className="board-item">
          <span className="board-item-id">{item.id}</span>
          <span className="board-item-title">{item.title}</span>
          <span className="board-item-author">{item.author}</span>
          <span className="board-item-date">{item.date}</span>
        </div>
      ))}
    </div>
  );
};

export default BoardList;
