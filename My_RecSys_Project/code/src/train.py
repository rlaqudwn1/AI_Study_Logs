import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import roc_auc_score, accuracy_score, mean_squared_error
import numpy as np

# [1] 학습 함수
def train(args, model, data, logger, setting):
    print("\n>>> [Train] 학습을 시작합니다! (치익- 치익-)")
    
    # 1. 장비 설정 (Q1 정답)
    device = args.device
    model.to(device)

    # 2. 손실함수 & 옵티마이저
    # (RMSE 과제라면 MSELoss, 확률 예측이라면 BCELoss)
    # 여기서는 RMSE(평점 예측)를 위해 MSELoss로 변경해서 보여주겠다.
    criterion = nn.MSELoss() 
    
    # (옵티마이저에 weight_decay 추가)
    weight_decay = getattr(args.train, 'weight_decay', 0.0)
    optimizer = optim.Adam(model.parameters(), lr=args.train.lr, weight_decay=weight_decay)

    train_loader = data['train_dataloader']
    valid_loader = data['valid_dataloader']

    for epoch in range(args.train.epochs):
        model.train() # 학습 모드
        total_loss = 0

        for i, (X, y) in enumerate(train_loader):
            X, y = X.to(device), y.to(device)

            # (Q2 정답: 기울기 초기화)
            optimizer.zero_grad()

            output = model(X)
            
            # (차원 맞추기 & 실수형 변환)
            # MSELoss는 Float형을 원함. y가 Long일 수 있으므로 변환.
            loss = criterion(output, y.unsqueeze(1).float())
            
            # (Q3, Q4 정답: 역전파 및 갱신)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            if (i + 1) % 50 == 0:
                print(f"    Epoch {epoch+1} | Batch {i+1} | Loss: {loss.item():.4f}")

        # 검증 (RMSE 점수 확인)
        valid_rmse = valid(args, model, valid_loader, criterion)
        print(f"[Epoch {epoch+1}] Train Loss: {total_loss/len(train_loader):.4f} | Valid RMSE: {valid_rmse:.4f}")
        
        # 로그 저장
        logger.log(epoch+1, total_loss/len(train_loader), valid_metrics={'rmse': valid_rmse})

    print(">>> [Train] 학습 완료.\n")
    return model

# [2] 검증 함수
def valid(args, model, dataloader, criterion):
    model.eval()
    targets = []
    predicts = []
    
    # (Q5 정답: 미분 끄기)
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(args.device), y.to(args.device)
            output = model(X)
            
            # CPU로 옮겨서 리스트에 저장
            targets.extend(y.cpu().numpy())
            predicts.extend(output.detach().cpu().numpy())

    # RMSE 계산 (DeepFM이 평점을 예측했으니, 실제 평점과 비교)
    return np.sqrt(mean_squared_error(targets, predicts))

# [3] 추론 함수
def test(args, model, data, setting):
    print(">>> [Test] 추론을 시작합니다!")
    model.eval()
    device = args.device
    model.to(device)
    
    # data.py에 test_dataloader가 없으면 valid로 임시 대체 (에러 방지용)
    loader = data.get('test_dataloader', data['valid_dataloader'])
    predicts = []
    
    with torch.no_grad():
        for batch in loader:
            # Test Loader가 (X, y)를 주는지 (X,)만 주는지에 따라 처리
            X = batch[0] if isinstance(batch, list) else batch
            X = X.to(device)
            
            output = model(X)
            predicts.extend(output.detach().cpu().numpy())
            
    return predicts