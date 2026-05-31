"""
从零实现 Skip-gram + Negative Sampling 的 Word2Vec
用于理解词向量的训练原理
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import Counter
import random
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# ==================== 1. 准备语料 ====================
# 用简单的中文语料，方便观察结果
corpus = [
    "我 今天 吃 了 一个 苹果",
    "我 昨天 吃 了 一个 香蕉",
    "他 明天 想 吃 一个 橙子",
    "苹果 和 香蕉 都是 水果",
    "橙子 也是 水果",
    "我 喜欢 吃 水果",
    "他 喜欢 吃 苹果",
    "香蕉 很 甜",
    "橙子 也 很 甜",
    "苹果 不 太 甜",
    "我 今天 去 超市 买 水果",
    "超市 有 很多 水果",
    "我 买 了 苹果 和 香蕉",
]

# 分词（已用空格分隔）
sentences = [s.split() for s in corpus]
print(f"句子数: {len(sentences)}")

# ==================== 2. 构建词表 ====================
word_freq = Counter()
for sent in sentences:
    word_freq.update(sent)

# 过滤低频词（这里所有词都保留）
vocab = [w for w, c in word_freq.items() if c >= 1]
vocab_size = len(vocab)
word2idx = {w: i for i, w in enumerate(vocab)}
idx2word = {i: w for w, i in word2idx.items()}

print(f"词汇表大小: {vocab_size}")
print(f"词汇表: {vocab}")

# ==================== 3. 构建负采样概率表 ====================
# 按词频的 3/4 次幂采样（Mikolov 论文中的做法）
word_counts = np.array([word_freq[w] for w in vocab], dtype=np.float32)
word_freqs = word_counts / word_counts.sum()
noise_dist = torch.from_numpy(word_freqs ** 0.75)
noise_dist = noise_dist / noise_dist.sum()

print(f"噪声分布: {noise_dist}")

# ==================== 4. 生成 Skip-gram 训练样本 ====================
def generate_skipgram_data(sentences, word2idx, window_size=2):
    """
    生成 Skip-gram 训练样本
    返回: [(center_idx, context_idx), ...]
    """
    data = []
    for sent in sentences:
        indices = [word2idx[w] for w in sent if w in word2idx]
        for i, center in enumerate(indices):
            # 左右窗口
            left = max(0, i - window_size)
            right = min(len(indices), i + window_size + 1)
            for j in range(left, right):
                if i != j:
                    context = indices[j]
                    data.append((center, context))
    return data

train_data = generate_skipgram_data(sentences, word2idx, window_size=2)
print(f"训练样本数: {len(train_data)}")
print(f"前5个样本: {[(idx2word[c], idx2word[t]) for c, t in train_data[:5]]}")

# ==================== 5. 定义模型 ====================
class Word2Vec(nn.Module):
    """
    Skip-gram with Negative Sampling
    
    两个嵌入矩阵:
    - center_embed: 中心词嵌入 (V x D)
    - context_embed: 上下文词嵌入 (V x D)
    
    为什么是两个矩阵?
    因为每个词既可能作为中心词出现，也可能作为上下文词出现。
    最终使用时，通常只用 center_embed 作为词向量。
    """
    def __init__(self, vocab_size, embedding_dim):
        super(Word2Vec, self).__init__()
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        
        # 中心词嵌入
        self.center_embed = nn.Embedding(vocab_size, embedding_dim)
        # 上下文词嵌入
        self.context_embed = nn.Embedding(vocab_size, embedding_dim)
        
        # 初始化
        self._init_weights()
    
    def _init_weights(self):
        init_range = 0.5 / self.embedding_dim
        self.center_embed.weight.data.uniform_(-init_range, init_range)
        self.context_embed.weight.data.uniform_(-init_range, init_range)
    
    def forward(self, center_words, pos_context, neg_context):
        """
        前向传播（负采样版本）
        
        Args:
            center_words: (batch_size,) 中心词索引
            pos_context: (batch_size,) 正样本上下文词索引
            neg_context: (batch_size, neg_samples) 负样本上下文词索引
        
        Returns:
            loss: 标量损失
        """
        # 中心词向量: (batch_size, embed_dim)
        center_vec = self.center_embed(center_words)
        
        # 正样本上下文向量: (batch_size, embed_dim)
        pos_vec = self.context_embed(pos_context)
        
        # 负样本上下文向量: (batch_size, neg_samples, embed_dim)
        neg_vec = self.context_embed(neg_context)
        
        # 正样本分数（内积）: (batch_size,)
        pos_score = torch.sum(center_vec * pos_vec, dim=1)
        pos_loss = -torch.log(torch.sigmoid(pos_score) + 1e-10)
        
        # 负样本分数: (batch_size, neg_samples)
        neg_score = torch.bmm(neg_vec, center_vec.unsqueeze(2)).squeeze(2)
        neg_loss = -torch.sum(torch.log(torch.sigmoid(-neg_score) + 1e-10), dim=1)
        
        # 总损失
        return torch.mean(pos_loss + neg_loss)
    
    def get_embeddings(self):
        """获取训练好的词向量（取中心词嵌入）"""
        return self.center_embed.weight.data.cpu().numpy()

# ==================== 6. 训练 ====================
EMBEDDING_DIM = 10  # 小维度方便观察
NEG_SAMPLES = 5
BATCH_SIZE = 4
EPOCHS = 1000
LR = 0.01

model = Word2Vec(vocab_size, EMBEDDING_DIM)
optimizer = optim.Adam(model.parameters(), lr=LR)

# 转换为 Tensor
train_data = np.array(train_data)
centers = torch.LongTensor(train_data[:, 0])
contexts = torch.LongTensor(train_data[:, 1])

dataset_size = len(train_data)

print("\n开始训练...")
for epoch in range(EPOCHS):
    total_loss = 0
    
    # 随机打乱
    perm = torch.randperm(dataset_size)
    
    for i in range(0, dataset_size, BATCH_SIZE):
        batch_idx = perm[i:i+BATCH_SIZE]
        
        batch_centers = centers[batch_idx]
        batch_pos = contexts[batch_idx]
        
        # 负采样：从噪声分布中采样
        batch_neg = torch.multinomial(
            noise_dist, 
            len(batch_idx) * NEG_SAMPLES, 
            replacement=True
        ).view(len(batch_idx), NEG_SAMPLES)
        
        # 前向 + 反向
        optimizer.zero_grad()
        loss = model(batch_centers, batch_pos, batch_neg)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    if (epoch + 1) % 200 == 0:
        print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {total_loss:.4f}")

print("训练完成!")

# ==================== 7. 验证结果 ====================
def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

embeddings = model.get_embeddings()

print("\n=== 词向量相似度 ===")
test_words = ["苹果", "香蕉", "橙子", "水果", "超市", "吃"]
for w in test_words:
    if w in word2idx:
        idx = word2idx[w]
        vec = embeddings[idx]
        
        # 找最相似的词
        similarities = []
        for j in range(vocab_size):
            if j != idx:
                sim = cosine_similarity(vec, embeddings[j])
                similarities.append((idx2word[j], sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        print(f"\n'{w}' 最相似的词:")
        for word, sim in similarities[:3]:
            print(f"  {word}: {sim:.4f}")

# ==================== 8. 可视化 ====================
print("\n=== 绘制 t-SNE 可视化 ===")

# 用 t-SNE 降到 2 维
tsne = TSNE(n_components=2, random_state=42, perplexity=5)
embeddings_2d = tsne.fit_transform(embeddings)

plt.figure(figsize=(10, 8))
for i, word in enumerate(vocab):
    x, y = embeddings_2d[i]
    plt.scatter(x, y, s=100, alpha=0.6)
    plt.annotate(word, (x, y), fontsize=12, ha='center')

plt.title("Word2Vec t-SNE Visualization")
plt.xlabel("t-SNE dim 1")
plt.ylabel("t-SNE dim 2")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("word2vec_tsne.png", dpi=150)
plt.show()

print("\n可视化已保存为 word2vec_tsne.png")

# ==================== 9. 打印最终词向量 ====================
print("\n=== 最终词向量 (center_embed) ===")
for i, word in enumerate(vocab):
    vec = embeddings[i]
    print(f"{word:6s}: [{', '.join([f'{v:7.3f}' for v in vec])}]")
