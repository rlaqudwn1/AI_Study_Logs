import torch
from datasets_v2 import SASRecDataset
# 1. Mock Arguments
class MockArgs:
    max_seq_length = 5
    item_size = 100 # 임의의 아이템 개수
args = MockArgs()
# 2. Mock Data: User 0 has watched items [10, 20, 30, 40, 50]
# 시간순으로 정렬되어 있다고 가정
user_seq = [
    [10, 20, 30, 40, 50]
]
print(f"Original Sequence: {user_seq[0]}")
print(f"Max Len: {args.max_seq_length}")
print("-" * 50)
# 3. Verify Each Mode
# --- Train ---
ds_train = SASRecDataset(args, user_seq, data_type="train")
data = ds_train[0]
# data: (user_id, input_ids, target_pos, target_neg, answer)
print(f"[Train Phase]")
print(f"Input:  {data[1].tolist()}") # Expect: [..., 10, 20] (padded)
print(f"Target: {data[2].tolist()}") # Expect: [..., 20, 30] (padded)
print("Logic: 50(Test), 40(Valid) 제외 -> [10, 20, 30] 남음 -> Input[10, 20], Target[20, 30]")
print("-" * 50)
# --- Valid ---
ds_valid = SASRecDataset(args, user_seq, data_type="valid")
data = ds_valid[0]
print(f"[Valid Phase]")
print(f"Input:  {data[1].tolist()}") # Expect: [..., 10, 20, 30]
print(f"Answer: {data[4].tolist()}") # Expect: [40]
print("Logic: 50(Test) 제외 -> [10, 20, 30, 40] -> Input[10, 20, 30], Answer[40]")
print("-" * 50)
# --- Test ---
ds_test = SASRecDataset(args, user_seq, data_type="test")
data = ds_test[0]
print(f"[Test Phase]")
print(f"Input:  {data[1].tolist()}") # Expect: [..., 10, 20, 30, 40]
print(f"Answer: {data[4].tolist()}") # Expect: [50]
print("Logic: 전체 사용 -> Input[10, 20, 30, 40], Answer[50]")
print("-" * 50)