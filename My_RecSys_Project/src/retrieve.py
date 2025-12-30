# %%
import pandas as pd
import numpy as np
import os

DATA_PATH ="../train/"
# 1. 데이터 로드
# train_ratings는 csv, genres는 tsv 파일입니다.

train_ratings = pd.read_csv(os.path.join(DATA_PATH,'train_ratings.csv'))
df_genres = pd.read_csv(os.path.join(DATA_PATH,'genres.tsv'),sep='\t')
train_ratings.head(5)
df_genres.head(5)
# 2. 데이터 병합 (Merge)
# train_ratings를 기준으로 df_genres를 붙입니다.
# TODO: on에는 공통 컬럼명, how에는 병합 방식을 적어주세요.
df_merged = pd.merge(train_ratings, df_genres, on='item', how='left')

# 3. 결측치 처리 (Fillna)
# 장르가 없는 경우(NaN) 튕겨내지 말고 'Unknown'으로 채워줍니다.
df_merged['genre'] = df_merged['genre'].fillna('Unknown')

# 검증
print(f"Total Log Count: {len(df_merged)}")
print(df_merged.head())

# %%
## 실험 설계 무엇을 input label 로 할지 나누는 작업

## 검증 전략 각 유저가 마지막으로 본 아이템 딱 1개를 정답으로 숨겨두고  나머지 과거 데이터만 가지고 맞출 수 있는지
## validate로 구성하는 방법
df_sorted=df_merged.sort_values(['user','time'])

df_sorted.head()
## duplicated로 각 중복 user id중 가장 마지막을 추출함
df_test = df_sorted.drop_duplicates(subset=['user'], keep='last')
# 가장 마지막 인덱스를 통해서 드롭함
df_temp = df_sorted.drop(df_test.index)

df_val = df_temp.drop_duplicates(subset="user",keep='last')


df_train = df_temp.drop(df_val.index)
# 검증
print(f"Train: {len(df_train)}, Valid: {len(df_val)}, Test: {len(df_test)}")

# %%
from collections import Counter
import itertools as it  # (A) 라이브러리 이름
# 윈도우를 5개로 정하나요?
def train_cooc_dict(df, window_size=5):
    # counter 이름을 왜 cooc라고 지은거지
    cooc_counts = Counter()
    
    # user로 묶는데 item을 []로 감싸면 무슨효과로 item이 시간순 리스트가 되는거죠
    user_item_list = df.groupby('user')['item'].apply(list)
    
    for items in user_item_list:
    
        # 아이템 리스트가 [A,B,C,D]
        for i in range(len(items)):
            # 현재 타깃 i에 대해서 윈도우 만큼의 애들을 자름 파이썬이라 index 오류는 안남..
            context_items = items[i+i : i+1+window_size]
            
            # 윈도우에 있는 context_items에서 이웃을 짝짔는다
            for neigbor in context_items:
                # (A) -> (B) 방향
                cooc_counts[(items[i], neigbor)] += 1
                # (B) -> (A) 방향
                cooc_counts[(neigbor,items[i])]+= 1
    return cooc_counts
cooc_dict = train_cooc_dict(df_train, window_size=5)
print(f"Top 5 Pairs: {cooc_dict.most_common(5)}")

# %%
from collections import defaultdict

def cooc_to_map(cooc_counts):
    # item_id를 키로 하고 값은 Counter인 딕셔너리?
    item_cooc_map = defaultdict(Counter)
    
    for (item_i, item_j), count in cooc_counts.items():
        # 두가지 아이템조합의 dict -> 2차원 배열로 만들어서 관리한다
        #그래서 두가지 아이템이 있으면 그 카운트를 뱉는 맵을 생성하는거군요
        item_cooc_map[item_i][item_j] = count
        
    return item_cooc_map
item_map = cooc_to_map(cooc_dict)

test_item = list(item_map.keys())[0]

print(f"item{test_item}의 연관 아이템 Top3:")
#mostcommon이 어떻게 쓰이는지도 까먹은 것 같네요
print(item_map[test_item].most_common(3))

# %%
# 1. 유저별 과거 기록 가져오기 (Retrieval의 힌트로 사용)
# train_df는 이미 시간순 정렬이 되어 있습니다.
user_history_dict = df_train.groupby('user')['item'].apply(list).to_dict()

# 2. Candidate Generation 함수
def generate_candidates(user_id, history_dict, cooc_map, n_candidates=100):
    # 유저의 기록이 없으면 빈 리스트 반환 (Cold Start)
    if user_id not in history_dict:
        return []
    
    # 2-1. 유저가 가장 최근에 본 아이템 (힌트)
    last_item = history_dict[user_id][-1]
    
    # 2-2. 해당 아이템과 함께 많이 본 아이템 리스트 가져오기
    # cooc_map[last_item]은 Counter 객체입니다.
    # Counter.most_common(n)은 (item_id, count) 튜플 리스트를 반환합니다.
    
    # (A) cooc_map을 사용하여 Top-N개 추천 리스트를 뽑아보세요.
    # 힌트: candidates = [item for item, score in cooc_map[_______]._________(n_candidates)]
    top_items = cooc_map[last_item].most_common(n_candidates)
    candidates = [item for item, score in top_items]
    
    # (선택 사항) 이미 본 아이템을 제외하는 로직을 추가할 수도 있습니다.
    # 여기서는 단순화를 위해 생략합니다.
    
    return candidates

# 검증: Valid Set의 첫 번째 유저에 대해 테스트
test_user = df_val['user'].iloc[0]
candidates = generate_candidates(test_user, user_history_dict, item_map)

print(f"User {test_user}의 Last Item: {user_history_dict[test_user][-1]}")
print(f"추천된 후보군 개수: {len(candidates)}")
print(f"후보군 Top 10: {candidates[:10]}")

# %%
## candidate Generation 실행
user_history_dict = df_train.groupby('user')['item'].apply(list).to_dict()

# df_train을 이용해 각 유저의 **과거 기록(History)**을 가져옵니다.
# 각 유저의 **가장 마지막에 본 아이템(Last Item)**을 찾습니다.
# 이유: 아이언맨 1을 어제 봤다면, 오늘 아이언맨 2를 볼 확률이 높겠죠? 가장 최근 기록이 추천의 가장 큰 힌트입니다.
# item_map에 그 마지막 아이템을 넣고, 가장 친한 친구 100명을 데려옵니다.

def generate_candidates(user_id, history_dict, cooc_map, n_candidates=100):
    if user_id not in history_dict:
        return []
# 유저가 본 가장 최근 아이템 
    last_item = history_dict[user_id][-1]
    
    top_items = cooc_map[last_item].most_common(n_candidates)
    candidates = [item for item, score in top_items]
    
    return candidates
test_user = df_val['user']