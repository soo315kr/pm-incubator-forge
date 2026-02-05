import pandas as pd
import numpy as np
import sqlite3

# 1. DB 연결
conn = sqlite3.connect("sales_data.db")
cur = conn.cursor()

cur.execute('''
            CREATE TABLE IF NOT EXISTS sales
            (
                date
                TEXT
                PRIMARY
                KEY,
                revenue
                INTEGER,
                event
                TEXT,
                weekday
                TEXT
            )
            ''')

# 2. 365일 샘플 데이터 생성
np.random.seed(42)

dates = pd.date_range(start="2026-01-01", periods=365, freq='D')
revenues = []
events = []

for d in dates:
    base = 100  # 기본 매출
    # 주말 효과
    if d.weekday() >= 5:
        base += 20
    # 계절성 효과
    if d.month in [11, 12]:
        base += 15  # 연말 프로모션 시즌
    elif d.month in [6, 7, 8]:
        base += 5  # 여름 약간 상승
    # 랜덤 변동
    base += np.random.randint(-5, 6)

    # 이벤트 배치
    if d.day % 10 == 0:
        event = "프로모션"
        base += 10
    elif d.day % 15 == 0:
        event = "광고 캠페인"
        base += 15
    elif d.weekday() >= 5:
        event = "주말 특수"
    else:
        event = "없음"

    revenues.append(base)
    events.append(event)

# 요일 이름 추가
weekdays = [d.strftime("%A") for d in dates]

# 데이터프레임 생성
df = pd.DataFrame({
    "date": dates,
    "revenue": revenues,
    "event": events,
    "weekday": weekdays
})

# 3. DB 삽입
for row in df.itertuples(index=False):
    cur.execute('''
        INSERT OR REPLACE INTO sales(date, revenue, event, weekday) VALUES (?, ?, ?, ?)
    ''', (row.date.strftime("%Y-%m-%d"), row.revenue, row.event, row.weekday))

conn.commit()

# 4. 확인
print(df.head(20))
