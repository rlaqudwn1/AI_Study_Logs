import torch
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

# [1] 데이터 로드
def context_data_load(args):
    print(f"[Data] Loading data from {args.data_path}...")
    
    # 데이터 경로가 없으면 에러 방지 (방어코드)
    file_path = os.path.join(args.data_path, 'train_ratings.csv')
    if not os.path.exists(file_path):
        print(f"[Warning] 파일이 없습니다: {file_path}. 더미 데이터를 생성합니다.")
        # 테스트용 더미 데이터 생성 (실행을 위해)
        dummy = pd.DataFrame({
            'user_id': [0, 1, 0, 1]*25,
            'item_id': [1, 2, 3, 4]*25,
            'rating': [5, 4, 3, 2]*25
        })
        train_df = dummy
    else:
        train_df = pd.read_csv(file_path)
    
    if not args.predict:
        train_df = train_df.dropna()
        
    # 라벨 인코딩 (문자열/ID -> 0, 1, 2... 정수 인덱스)
    # DeepFM 임베딩을 위해 필수
    for col in train_df.columns:
        if col != 'rating': # 타겟 제외
            le = LabelEncoder()
            train_df[col] = le.fit_transform(train_df[col].astype(str))
            
    print(f"[Data] Loaded Shape: {train_df.shape}")
    return {'train': train_df}

# [2] 데이터 분할
def context_data_split(args, data):
    print("[Data] Splitting data...")
    df = data['train']
    
    # Q1. 슬라이싱 (자네의 정답)
    X = df.iloc[:, :-1].values  # 마지막 컬럼 제외 (Features)
    y = df.iloc[:, -1].values   # 마지막 컬럼만 (Target)

    # Q2. 비율 설정 (getattr 방어술 적용)
    test_size = getattr(args, 'test_size', 0.2) 
    
    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=args.seed, 
        shuffle=True
    )
    
    data['X_train'], data['X_valid'] = X_train, X_valid
    data['y_train'], data['y_valid'] = y_train, y_valid
    return data

# [3] 데이터 로더 생성
def context_data_loader(args, data):
    print("[Data] Creating DataLoaders...")
    
    # Q3. 텐서 변환 (교정: X는 Long, y는 Float)
    train_dataset = TensorDataset(
        torch.LongTensor(data['X_train']), 
        torch.FloatTensor(data['y_train'])
    )
    valid_dataset = TensorDataset(
        torch.LongTensor(data['X_valid']), 
        torch.FloatTensor(data['y_valid'])
    )

    # Q4. 로더 설정
    # args.train이 없을 수도 있으니 안전하게 가져오기
    train_args = getattr(args, 'train', {})
    batch_size = getattr(train_args, 'batch_size', 256)
    
    # num_workers 설정 (윈도우면 0, 아니면 설정값)
    # os.name: 'nt'는 윈도우
    num_workers = 0 if os.name == 'nt' else getattr(train_args, 'num_workers', 2)

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,       
        num_workers=num_workers, 
        pin_memory=True,
        drop_last=False
    )
    
    valid_loader = DataLoader(
        valid_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )

    return {
        'train_dataloader': train_loader,
        'valid_dataloader': valid_loader
    }