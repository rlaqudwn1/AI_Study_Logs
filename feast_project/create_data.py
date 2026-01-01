# create_data.py
import pandas as pd
from datetime import datetime, timedelta

# 1. 가상의 유저 데이터 생성 (내공이 담긴 DataFrame)
# 상황: 유저(1001~1005)의 과거 행동 데이터
data = pd.DataFrame({
    "user_id": [1001, 1002, 1003, 1004, 1005],
    "daily_transactions": [5, 2, 0, 12, 8],      # 피처 1: 일일 거래 횟수
    "total_spend": [50.5, 20.0, 0.0, 150.2, 80.0], # 피처 2: 총 사용 금액
    # [중요] 피처 스토어의 핵심은 '시간'이다. 타임스탬프 필수!
    "event_timestamp": [
        datetime.now() - timedelta(days=2), # 이틀 전 데이터
        datetime.now() - timedelta(days=2),
        datetime.now() - timedelta(days=1), # 어제 데이터
        datetime.now() - timedelta(days=1),
        datetime.now()                  # 오늘 데이터
    ]
})

# 2. Parquet으로 굽기 (압축된 고속 파일 생성)
# index=False는 필수다. 불필요한 인덱스 저장 방지.
data.to_parquet("user_stats.parquet", index=False)

print("✨ [완료] user_stats.parquet 파일이 생성되었다!")
print(data)