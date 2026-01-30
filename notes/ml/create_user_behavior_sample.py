import pandas as pd
import random
from datetime import datetime, timedelta

users = []
item_pool = ["A","B","C","D","E"]

for i in range(1, 51):
    last_login = datetime(2026,1,1) + timedelta(days=random.randint(0,26))
    purchase_amount = round(random.choice([0, random.randint(20,300)]),2)
    recommended_items = random.sample(item_pool, random.randint(1,3))
    clicked_items = random.sample(recommended_items, random.randint(0,len(recommended_items)))
    subscription_status = "churned" if random.random() < 0.3 else "active"  # 30% 이탈
    users.append({
        "user_id": i,
        "last_login": last_login.strftime("%Y-%m-%d"),
        "purchase_amount": purchase_amount,
        "recommended_items": recommended_items,
        "clicked_items": clicked_items,
        "subscription_status": subscription_status
    })

df = pd.DataFrame(users)
df.to_csv("user_behavior_sample.csv", index=False)
print("샘플 데이터(user_behavior_sample.csv) 생성 완료!")

