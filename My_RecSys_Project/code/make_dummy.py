import pandas as pd
import os
import random

# 1. 저장 경로 설정 (자네의 프로젝트 구조에 맞춤)
# code 폴더 안에서 실행한다고 가정하고, 상위 폴더의 data로 이동
base_path = '../data' 
if not os.path.exists(base_path):
    os.makedirs(base_path, exist_ok=True)
    print(f"[알림] {base_path} 폴더를 생성했습니다.")

print(f"--- [데이터 소환술] 데이터를 {base_path} 에 생성합니다 ---")

# ==========================================
# 2. Books 데이터 생성 (책 정보)
# ==========================================
num_books = 50
books_data = {
    'isbn': [f'978-000{i:05d}' for i in range(num_books)],
    'book_title': [f'무공비급 제{i}권' for i in range(num_books)],
    'book_author': [f'저자_{i%5}' for i in range(num_books)], # 저자 5명 돌려막기
    'year_of_publication': [random.randint(1990, 2023) for _ in range(num_books)],
    'publisher': [f'출판사_{i%3}' for i in range(num_books)],
}
df_books = pd.DataFrame(books_data)
df_books.to_csv(os.path.join(base_path, 'books.csv'), index=False)
print(f"[완료] books.csv 생성 ({num_books}권)")

# ==========================================
# 3. Train Ratings 데이터 생성 (학습용 평점)
# ==========================================
num_users = 20
num_ratings = 100 # 자네가 원한 100개

users = [i for i in range(num_users)] # 유저 ID: 0 ~ 19
items = df_books['isbn'].tolist()

train_data = {
    'user_id': [random.choice(users) for _ in range(num_ratings)],
    'isbn': [random.choice(items) for _ in range(num_ratings)],
    'rating': [random.randint(1, 10) for _ in range(num_ratings)] # 1~10점 (RMSE용)
}
df_train = pd.DataFrame(train_data)
df_train.to_csv(os.path.join(base_path, 'train_ratings.csv'), index=False)
print(f"[완료] train_ratings.csv 생성 ({num_ratings}건)")

# ==========================================
# 4. Sample Submission 데이터 생성 (제출용)
# ==========================================
# 보통 테스트셋(users x items)에 대한 예측을 제출함
# 여기서는 랜덤하게 50개의 빈칸을 채우라고 가정
num_submit = 50
submit_data = {
    'user_id': [random.choice(users) for _ in range(num_submit)],
    'isbn': [random.choice(items) for _ in range(num_submit)],
    'rating': [0] * num_submit # 예측값은 일단 0으로 채움
}
df_submit = pd.DataFrame(submit_data)
df_submit.to_csv(os.path.join(base_path, 'sample_submission.csv'), index=False)
print(f"[완료] sample_submission.csv 생성 ({num_submit}건)")

print("\n>>> 모든 허수아비 소환 완료! 이제 main.py를 실행하라!")