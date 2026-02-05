import { useState } from 'react'
import './App.css'

type ScheduleItem = {
  id: string
  date: string
  time: string
  place: string
  activity: string
  memo: string
}

type TravelScheduleForm = {
  title: string
  destination: string
  startDate: string
  endDate: string
  budget: string
  participants: string
  description: string
  schedules: ScheduleItem[]
}

function App() {
  const [formData, setFormData] = useState<TravelScheduleForm>({
    title: '',
    destination: '',
    startDate: '',
    endDate: '',
    budget: '',
    participants: '',
    description: '',
    schedules: [],
  })

  const [newSchedule, setNewSchedule] = useState<ScheduleItem>({
    id: '',
    date: '',
    time: '',
    place: '',
    activity: '',
    memo: '',
  })

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleScheduleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target
    setNewSchedule((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const addSchedule = () => {
    if (!newSchedule.date || !newSchedule.place || !newSchedule.activity) {
      alert('날짜, 장소, 활동은 필수 입력 항목입니다.')
      return
    }

    const schedule: ScheduleItem = {
      ...newSchedule,
      id: Date.now().toString(),
    }

    setFormData((prev) => ({
      ...prev,
      schedules: [...prev.schedules, schedule],
    }))

    setNewSchedule({
      id: '',
      date: '',
      time: '',
      place: '',
      activity: '',
      memo: '',
    })
  }

  const removeSchedule = (id: string) => {
    setFormData((prev) => ({
      ...prev,
      schedules: prev.schedules.filter((schedule) => schedule.id !== id),
    }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('여행 스케줄 제출:', formData)
    alert('여행 스케줄이 생성되었습니다!')
  }

  return (
    <div className="page">
      <header className="page-header">
        <p className="eyebrow">여행 관리</p>
        <h1>여행 스케줄 생성</h1>
        <p className="sub">
          새로운 여행 일정을 만들고 상세 스케줄을 관리해보세요.
        </p>
      </header>

      <form className="travel-form" onSubmit={handleSubmit}>
        <section className="form-section">
          <h2 className="section-title">기본 정보</h2>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="title">
                여행 제목 <span className="required">*</span>
              </label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                placeholder="예: 제주도 3박 4일 여행"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="destination">
                여행지 <span className="required">*</span>
              </label>
              <input
                type="text"
                id="destination"
                name="destination"
                value={formData.destination}
                onChange={handleInputChange}
                placeholder="예: 제주도"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="startDate">
                출발일 <span className="required">*</span>
              </label>
              <input
                type="date"
                id="startDate"
                name="startDate"
                value={formData.startDate}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="endDate">
                귀국일 <span className="required">*</span>
              </label>
              <input
                type="date"
                id="endDate"
                name="endDate"
                value={formData.endDate}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="budget">예산 (원)</label>
              <input
                type="number"
                id="budget"
                name="budget"
                value={formData.budget}
                onChange={handleInputChange}
                placeholder="예: 500000"
                min="0"
              />
            </div>

            <div className="form-group">
              <label htmlFor="participants">참가자</label>
              <input
                type="text"
                id="participants"
                name="participants"
                value={formData.participants}
                onChange={handleInputChange}
                placeholder="예: 홍길동, 김철수"
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="description">여행 설명</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              placeholder="여행에 대한 간단한 설명을 입력하세요..."
              rows={4}
            />
          </div>
        </section>

        <section className="form-section">
          <h2 className="section-title">상세 일정</h2>

          <div className="schedule-form">
            <div className="schedule-form-grid">
              <div className="form-group">
                <label htmlFor="schedule-date">
                  날짜 <span className="required">*</span>
                </label>
                <input
                  type="date"
                  id="schedule-date"
                  name="date"
                  value={newSchedule.date}
                  onChange={handleScheduleChange}
                />
              </div>

              <div className="form-group">
                <label htmlFor="schedule-time">시간</label>
                <input
                  type="time"
                  id="schedule-time"
                  name="time"
                  value={newSchedule.time}
                  onChange={handleScheduleChange}
                />
              </div>

              <div className="form-group">
                <label htmlFor="schedule-place">
                  장소 <span className="required">*</span>
                </label>
                <input
                  type="text"
                  id="schedule-place"
                  name="place"
                  value={newSchedule.place}
                  onChange={handleScheduleChange}
                  placeholder="예: 제주공항"
                />
              </div>

              <div className="form-group">
                <label htmlFor="schedule-activity">
                  활동 <span className="required">*</span>
                </label>
                <input
                  type="text"
                  id="schedule-activity"
                  name="activity"
                  value={newSchedule.activity}
                  onChange={handleScheduleChange}
                  placeholder="예: 공항 도착"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="schedule-memo">메모</label>
              <textarea
                id="schedule-memo"
                name="memo"
                value={newSchedule.memo}
                onChange={handleScheduleChange}
                placeholder="추가 메모를 입력하세요..."
                rows={2}
              />
            </div>

            <button
              type="button"
              className="add-schedule-btn"
              onClick={addSchedule}
            >
              일정 추가
            </button>
          </div>

          {formData.schedules.length > 0 && (
            <div className="schedule-list">
              <h3 className="schedule-list-title">추가된 일정 ({formData.schedules.length})</h3>
              <div className="schedule-items">
                {formData.schedules.map((schedule) => (
                  <div key={schedule.id} className="schedule-item">
                    <div className="schedule-item-header">
                      <div className="schedule-date-badge">
                        {schedule.date} {schedule.time && `• ${schedule.time}`}
                      </div>
                      <button
                        type="button"
                        className="remove-schedule-btn"
                        onClick={() => removeSchedule(schedule.id)}
                      >
                        삭제
                      </button>
                    </div>
                    <div className="schedule-item-content">
                      <div className="schedule-place">
                        <strong>📍 {schedule.place}</strong>
                      </div>
                      <div className="schedule-activity">{schedule.activity}</div>
                      {schedule.memo && (
                        <div className="schedule-memo">{schedule.memo}</div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>

        <div className="form-actions">
          <button type="button" className="ghost-btn">
            취소
          </button>
          <button type="submit" className="primary-btn">
            여행 스케줄 생성
          </button>
        </div>
      </form>
    </div>
  )
}

export default App
