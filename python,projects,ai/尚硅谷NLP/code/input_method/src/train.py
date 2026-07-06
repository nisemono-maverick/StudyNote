import torch
from dataset import get_dataloader
from model import InputMethodModel
import config
from tqdm import tqdm

def train():
    # 1. 确定设备
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # 2. 数据集
    dataloader = get_dataloader()

    # 3. 加载词表
    with open(config.MODELS_DIR / "vocab.txt", 'r', encoding='utf-8') as f:
        vocab_list =  [line.strip() for line in f]

    # 4. 模型
    model = InputMethodModel(vocab_size=len(vocab_list)).to(device)
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.LEARNING_RATE)
    # writer = torch.utils.tensorboard.SummaryWriter()

    # 5. 训练
    for epoch in range(1, 1 + config.EPOCHS):
        print("="*10, f"Epoch: {epoch}", "="*10)
        loss = train_one_epoch(model, dataloader, loss_fn, optimizer, device)
        print(f"loss: {loss}")


def train_one_epoch(model:InputMethodModel, dataloader, loss_fn, optimizer, device):
    model.train()
    total_loss = 0
    for inputs, targets in tqdm(dataloader, desc="训练"):
        inputs = inputs.to(device)
        targets = targets.to(device)
        # inputs.shape [batch_size, seq_len]
        # targets.shape [batch_size]

        # 前向传播
        outputs = model(inputs)
        # outputs.shape [batch_size, vocab_size]
        loss = loss_fn(outputs, targets)

        # 反向传播
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        total_loss += loss.item()
    return total_loss / len(dataloader)


if __name__ == '__main__':
    train()