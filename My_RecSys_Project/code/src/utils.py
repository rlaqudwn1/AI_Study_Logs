import os
import time
import random
import numpy as np
import torch
import logging
from omegaconf import OmegaConf


def rmse(real: list, predict: list) -> float:
    pred = np.array(predict)
    return np.sqrt(np.mean((real-pred) ** 2))
class Setting:
    @staticmethod
    def seef_deverthing(seed):
        print(f"[Utils] 시드 고정: {seed}")
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual.seed(seed)
        torch.backends.cudnn.deterministic = True
    def __init__(self):
        now = time.localtime()

    def get_log_path(self, args):
            # config에 log_dir이 없으면 기본값 'saved' 사용
            log_root = getattr(args, 'log_dir', './saved')
            
            # 모델 이름이 없으면 'Unknown'
            model_name = getattr(args, 'model', 'Unknown')
            
            path = os.path.join(log_root, f'{self.save_time}_{model_name}')
            os.makedirs(path, exist_ok=True)
            return path

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
        
        # getLogger로 logger를 얻고 
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        
        # 기존 로거 핸들러 제거 
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
            
        # 포맷
        self.formatter = logging.Formatter('[%(asctime)s] - %(message)s')
        
        # 파일 로깅
        # 로그 핸들러는 인스턴스화 초기화는 path와 로그 이름을 설정해 초기화한다
        self.file_handlear = logging.FileHandler(os.path.join(self.path, 'train.log'))
        # 설정 포멧을 넣고 
        self.file_handlear.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handlear)
        
    
    def log(self, epoch, train_loss, valid_loss=None, valid_metrics=None):
        message = f'epoch : {epoch}/{self.args.train.epochs} | train loss : {train_loss:.4f}'
        if valid_loss:
            message += f' | valid loss : {valid_loss:.4f}'
        if valid_metrics:
            for metric, value in valid_metrics.items():
                message += f' | {metric} : {value:.4f}'
        self.logger.info(message)
    # 로그 닫기
    def close(self):
        self.logger.removeHandler(self.file_handler)
        self.file_handler.close()
        self.logger.removeHandler(self.stream_handler) # 스트림도 닫기
    
    #args를 저장
    def save_args(self):
        # args 저장
        with open(os.path.join(self.path, 'config.yaml'), 'w') as f:
            OmegaConf.save(self.args, f)
            
    def __del__(self):
        # 소멸자에서 close 호출은 주의가 필요하지만, 여기선 유지
        pass