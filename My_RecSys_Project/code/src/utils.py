import os
import time
import random
import numpy as np
import torch
import logging
from omegaconf import OmegaConf

# [1] 지표 계산 함수
def rmse(real: list, predict: list) -> float:
    pred = np.array(predict)
    return np.sqrt(np.mean((real-pred) ** 2))

class Setting:
    # [2] 초기화 함수 (여기가 자네에게 없었던 심장이다!)
    def __init__(self):
        now = time.localtime()
        # 현재 시간을 '년월일_시분초' 형식으로 기록해둔다.
        self.save_time = time.strftime('%Y%m%d_%H%M%S', now)

    # [3] 시드 고정 (오타 수정됨)
    @staticmethod
    def seed_everything(seed):
        random.seed(seed)
        os.environ['PYTHONHASHSEED'] = str(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed) # 멀티 GPU라면 manual_seed_all 권장
        torch.backends.cudnn.deterministic = True
        print(f"[Setting] Seed fixed to {seed}")

    # [4] 로그 경로 생성
    def get_log_path(self, args):
        # config에 log_dir이 없으면 기본값 'saved' 사용
        log_root = getattr(args, 'log_dir', './saved')
        
        # 모델 이름이 없으면 'Unknown'
        model_name = getattr(args, 'model', 'Unknown')
        
        # 여기서 self.save_time을 사용한다! (__init__이 없으면 여기서 에러 남)
        path = os.path.join(log_root, f'{self.save_time}_{model_name}')
        os.makedirs(path, exist_ok=True)
        return path

    # [5] 제출 파일명 생성
    def get_submit_filename(self, args):
        submit_dir = getattr(args, 'submit_dir', './submit')
        os.makedirs(submit_dir, exist_ok=True)
        
        if not args.predict:
            filename = os.path.join(submit_dir, f'{self.save_time}_{args.model}.csv')
        else:
            filename = f"submit_{self.save_time}.csv"
            
        return filename

class Logger:
    def __init__(self, args, path):
        self.args = args
        self.path = path

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        
        # 중복 출력 방지
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.formatter = logging.Formatter('[%(asctime)s] - %(message)s')

        # 파일 로깅
        self.file_handler = logging.FileHandler(os.path.join(self.path, 'train.log'))
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        
        # 콘솔 출력
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.stream_handler)

    def log(self, epoch, train_loss, valid_loss=None, valid_metrics=None):
        message = f'epoch : {epoch}/{self.args.train.epochs} | train loss : {train_loss:.4f}'
        if valid_loss:
            message += f' | valid loss : {valid_loss:.4f}'
        if valid_metrics:
            for metric, value in valid_metrics.items():
                message += f' | {metric} : {value:.4f}'
        self.logger.info(message)
    
    def close(self):
        self.logger.removeHandler(self.file_handler)
        self.file_handler.close()
        self.logger.removeHandler(self.stream_handler)

    def save_args(self):
        with open(os.path.join(self.path, 'config.yaml'), 'w') as f:
            OmegaConf.save(self.args, f)
            
    def __del__(self):
        pass