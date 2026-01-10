import pandas as pd


def __getitem__(self):
    if self.data_type == "train":
        input_ids = items[:-3]
        target_pos = items[1:-2]
        answer = []
    elif self.data_type =="valid":
        input_ids = items[:-2]
        answer = [items[-2]]
    elif self.data_type =="test":
        input_ids = item[:-1]
        answer = [items[-1]]