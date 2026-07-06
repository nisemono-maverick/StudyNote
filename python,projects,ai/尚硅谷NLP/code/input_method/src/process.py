import time
import pandas as pd
import config
from sklearn.model_selection import train_test_split
import jieba
from tqdm import tqdm

def build_dataset(sentences, word2index):
    indexed_sentences = [[word2index.get(token,0) for token in jieba.lcut(sentence)] for sentence in sentences]
    dataset = []
    for sentence in tqdm(indexed_sentences, desc='构建数据集'):
        for i in range(len(sentence) - config.SEQ_LEN):
            input = sentence[i:i+config.SEQ_LEN]
            target = sentence[i+config.SEQ_LEN]
            dataset.append({'input': input, 'target': target})
    return dataset

def process():
    print("开始处理数据")
    # 1.读取文件
    df = pd.read_json(config.RAW_DATA_DIR / "synthesized_.jsonl",lines=True,orient="records")
    
    # 2.提取句子
    sentences = []
    for dialog in df['dialog']:
        for sentence in dialog:
            sentences.append(sentence.split("：")[1])

    # 3.划分数据集
    train_sentences, test_sentences = train_test_split(sentences, test_size=0.2, random_state=42)

    # 3.99.如果词表文件已存在，跳过创建词表这一步
    vocab_path = config.MODELS_DIR / "vocab.txt"
    if not vocab_path.exists():
        # 4.基于训练集构建词表
        vocab_set = set()
        for sentence in tqdm(train_sentences, desc="构建词表"):
            vocab_set.update(jieba.lcut(sentence))
        vocab_list = ['<unk>'] + sorted(vocab_set)

        # 5.保存词表
        with open(config.MODELS_DIR / "vocab.txt", 'w', encoding='utf-8') as f:
            f.write('\n'.join(vocab_list))
    else:
        # 从文件中读取词表
        with open(config.MODELS_DIR / "vocab.txt", 'r', encoding='utf-8') as f:
            vocab_list =  [line.strip() for line in f]

    # 6.构建训练集
    word2index = {word: index for index, word in enumerate(vocab_list)}
    train_dataset = build_dataset(train_sentences, word2index)

    # 7.保存训练集
    pd.DataFrame(train_dataset).to_json(config.PROCESSED_DATA_DIR / 'train.jsonl', orient='records', lines=True)

    # 8.测试集处理
    test_dataset = build_dataset(test_sentences, word2index)
    pd.DataFrame(test_dataset).to_json(config.PROCESSED_DATA_DIR / 'test.jsonl', orient='records', lines=True)
            
    print("数据处理完成")

if __name__ == '__main__':
    process() 