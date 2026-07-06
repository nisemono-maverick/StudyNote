from torch.utils.data import Dataset, DataLoader
import torch
import pandas as pd
import config

# 1. 定义Dataset
class InputMethodDataset(Dataset):
    def __init__(self, filepath):
        self.data = pd.read_json(filepath, lines=True).to_dict(orient='records')

    def __getitem__(self, index):
        # row = self.data.iloc[index]
        input_tensor = torch.tensor(self.data[index]['input'], dtype=torch.long)
        target_tensor = torch.tensor(self.data[index]['target'], dtype=torch.long)
        return input_tensor, target_tensor

    def __len__(self):
        return len(self.data)
    
# 2. 提供一个获取dataloader的方法
def get_dataloader(train=True):
    file_name = 'train.jsonl' if train else 'test.jsonl'
    return DataLoader(dataset=InputMethodDataset(config.PROCESSED_DATA_DIR / file_name),
                    batch_size=config.BATCH_SIZE,
                    shuffle=True)
        
if __name__ == "__main__":
    train_dataloader = get_dataloader()
    for step, (input, target) in enumerate(train_dataloader):
        print('step is :', step)
        data, label = input, target
        print('data is {}, label is {}'.format(data, label))
        break