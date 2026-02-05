import React from 'react';
import { boardData } from '../data/boardData';

const BoardList: React.FC = () => {
  return (
    <div className="board-list">
      <div className="board-header">
        <h1>게시판 목록</h1>
        <div className="board-stats">
          총 <strong>{boardData.length}</strong>개의 게시글
        </div>
      </div>
      
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th className="col-id">번호</th>
              <th className="col-category">분류</th>
              <th className="col-title">제목</th>
              <th className="col-author">작성자</th>
              <th className="col-date">작성일</th>
              <th className="col-views">조회수</th>
            </tr>
          </thead>
          <tbody>
            {boardData.map((item) => (
              <tr key={item.id}>
                <td className="col-id">{item.id}</td>
                <td className="col-category">
                  <span className="category-badge">{item.category || '일반'}</span>
                </td>
                <td className="col-title">
                  <span className="title-link">{item.title}</span>
                </td>
                <td className="col-author">{item.author}</td>
                <td className="col-date">{item.date}</td>
                <td className="col-views">{item.views.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default BoardList;
