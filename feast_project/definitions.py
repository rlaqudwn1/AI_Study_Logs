from feast import Entity, FeatureView, FileSource, Field
from feast.types import Float64, Int64
from datetime import timedelta

# 1. 데이터 소스 지정
user_stats_source = FileSource(
    path="user_stats.parquet",
    timestamp_field="event_timestamp"
)

# 엔티티 정의 (이 데이터의 주인은 누구인가?)
user = Entity (name="user", join_keys=["user_id"])

# 피처 뷰 정의?
user_stats_view = FeatureView(
    name= "user_daily_stats",
    entities=[user],
    ttl=timedelta(days=30),
    schema=[
        Field(name="daily_transactions", dtype=Int64),
        Field(name="total_spend", dtype=Float64)
    ],
    source= user_stats_source,
    online=True
)