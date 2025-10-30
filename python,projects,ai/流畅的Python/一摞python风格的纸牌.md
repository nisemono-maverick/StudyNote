
### 概述

在 Python 中，`__len__` 和 `__getitem__` 是两个重要的魔法方法，它们使得自定义对象能够像内置序列类型（如列表、元组）一样工作。

### 代码示例分析
```python
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, index):
        return self._cards[index]
```

### [[NamedTuple]] 方法 
在Python中，当需要同时拥有字典的可读性和元组不变性的数据结构时，可以使用 `namedtuple` 或 `NamedTuple`。

### `__len__` 方法

#### 功能
- 定义对象的长度
- 当调用 `len(obj)` 时自动调用
```python
deck = FrenchDeck()
print(len(deck))  # 输出: 52
```

#### 特点
- 必须返回一个非负整数
- 使得对象支持 `len()` 函数
您提出了一个非常重要的观察！让我修正和补充这个要点：

#### `__len__` 方法的重要说明

##### 运行时检查而非编译时检查

```python
class ProblematicDeck:
    def __len__(self):
        return -5  # 这不会在定义时报错
        
deck = ProblematicDeck()
print(len(deck))  # 这里才会报错：ValueError: __len__() should return >= 0
```

##### 实际开发中的最佳实践

```python
class FrenchDeck:
    def __len__(self):
        # 添加类型检查和验证
        length = len(self._cards)
        if length < 0:
            raise ValueError("Length cannot be negative")
        return length
    
    # 或者使用断言
    def __len__(self):
        length = len(self._cards)
        assert length >= 0, "Length must be non-negative"
        return length
```

### `__getitem__` 方法

#### 功能
- 定义索引访问行为
- 当使用 `obj[index]` 或切片时自动调用

#### 特点
- 支持索引访问：`deck[0]`
- 支持切片操作：`deck[:3]`
- 支持迭代：`for card in deck`
- 支持 `in` 操作符：`Card('Q', 'hearts') in deck`

#### 使用示例
```python
# 索引访问
print(deck[0])  # 输出: Card(rank='2', suit='spades')

# 切片操作
print(deck[:3])  # 输出前3张牌

# 迭代
for card in deck:
    print(card)

# 成员检查
print(Card('Q', 'hearts') in deck)  # 输出: True
```

### `__contains__` 方法
