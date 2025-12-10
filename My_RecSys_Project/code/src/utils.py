import os
import torch
import random
import numpy as np


class Setting:
    @staticmethod
    def seef_deverthing(seed):
        print(f"[Utils] 시드 고정: {seed}")
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual.seed(seed)
        torch.backends.cudnn.deterministic = True

def get_log_path(self, args):
    return "./saved"

def get_submit_filename(self, args):
    return 