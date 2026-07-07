---
description:
tags:
date:
---
#### 安装 Tensorboard
`conda install tensorboard`

#### 基础使用
##### 基本流程
- 使用 `torch.utils.tensorboard.SummaryWriter` 将数据写入日志文件
- 启动 TensorBoard 服务，监听指定日志目录`tensorboard --logdir logs`
- 访问服务页面，查看可视化结果 `http://localhost:6006/`
```python
from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter(log_dir="./logs/scalar_demo")

for step in range(100):
    writer.add_scalar("scaler/y=x", step, step)
    writer.add_scalar("scaler/y=x^2", step ** 2, step)

writer.close()
```

- 为了便于查看，可定义不同日志存放位置
`writer = SummaryWriter(log_dir=config.LOGS_DIR / time.strftime("%Y-%m-%d_%H:%M:%S"))`