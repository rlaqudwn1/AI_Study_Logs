import torch.nn as nn
import torch

class DeepFM(nn.Module):
    def __init__(self, args, data):
        super(DeepFM, self).__init__()
        
        # [수정 1] args['model_name']을 삭제하고 하드코딩하거나 클래스명을 쓴다.
        # config에 있는 input_dim을 확인하기 위해 출력에 포함시켰다.
        print(f"[Model] DeepFM 모델 소환! (설정된 차원: {args.input_dim})")
        
        # [수정 2] 하드코딩(10) 대신 config에서 받아온 input_dim 사용
        # 이렇게 해야 config.yaml에서 숫자를 바꿔도 에러가 안 난다.
        self.layer = nn.Linear(args.input_dim, 1)

    def forward(self, x):
        # [수정 3] x는 LongTensor(정수)로 들어오지만, 
        # nn.Linear는 FloatTensor(실수)를 원한다.
        # 진짜 DeepFM은 임베딩을 쓰지만, 지금은 껍데기 선형 모델이므로 형변환을 해준다.
        return torch.sigmoid(self.layer(x.float()))