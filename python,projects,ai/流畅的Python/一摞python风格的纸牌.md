
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

#### 概述

虽然实现了 `__getitem__` 就自动获得了 `in` 操作符的支持，但 `__contains__` 方法提供了更高效、更可控的成员关系测试方式。

#### `__getitem__` 实现 in 的机制
- Python 会从索引 0 开始迭代
- 逐个调用 `__getitem__(i)` 直到找到匹配项或抛出 `IndexError`
- **时间复杂度**：O(n) 线性搜索

#### 专门优化：`__contains__` 方法

##### 基本实现
```python
class FrenchDeck:
    def __contains__(self, card):
        # 自定义的高效查找逻辑
        return any(c.rank == card.rank and c.suit == card.suit 
                  for c in self._cards)
```

##### 更高效的实现
```python
class OptimizedFrenchDeck:
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        self._card_set = set(self._cards)  # 预计算集合
    
    def __contains__(self, card):
        return card in self._card_set  # O(1) 时间复杂度
```

#### 性能对比

```python
import time

# 测试 __getitem__ 的 in 操作
start = time.time()
result1 = Card('K', 'spades') in deck_via_getitem  # 线性搜索
time1 = time.time() - start

# 测试 __contains__ 的 in 操作  
start = time.time()
result2 = Card('K', 'spades') in deck_via_contains  # 哈希查找
time2 = time.time() - start

print(f"__getitem__: {time1:.6f}s")   # __getitem__: 0.000062s
print(f"__contains__: {time2:.6f}s")  # __contains__: 0.000012s
```

#### 使用场景对比

##### 适合使用 `__getitem__` + 默认 in：
- 数据量小（< 1000 元素）
- 不需要频繁的成员检查
- 追求代码简洁性
- 数据结构本身不支持高效查找

##### 适合实现 `__contains__`：
- 数据量大
- 频繁进行成员关系测试
- 数据结构支持高效查找（集合、字典等）
- 需要自定义匹配逻辑

#### 实际应用示例

##### 案例1：范围检查
```python
class TemperatureRange:
    def __init__(self, min_temp, max_temp):
        self.min = min_temp
        self.max = max_temp
    
    def __contains__(self, temperature):
        return self.min <= temperature <= self.max

temp_range = TemperatureRange(0, 100)
print(50 in temp_range)  # True
print(150 in temp_range)  # False
```

##### 案例2：模式匹配
```python
class TextPattern:
    def __init__(self, patterns):
        self.patterns = patterns
    
    def __contains__(self, text):
        return any(pattern in text for pattern in self.patterns)

pattern_checker = TextPattern(['error', 'warning', 'critical'])
log_message = "System encountered an error"
print(log_message in pattern_checker)  # True
```

##### 案例3：复杂对象查找
```python
class StudentRoster:
    def __init__(self, students):
        self.students = students
        self._id_index = {s.id: s for s in students}  # 建立索引
    
    def __contains__(self, item):
        if isinstance(item, Student):
            return item.id in self._id_index
        elif isinstance(item, str):  # 按姓名查找
            return any(s.name == item for s in self.students)
        elif isinstance(item, int):  # 按ID查找
            return item in self._id_index
        return False
```

#### 优先级规则

**执行顺序**：
1. 先检查是否实现了 `__contains__`
2. 如果未实现，回退到 `__getitem__` + 迭代


### sorted() 方法与自定义排序

#### 基本概念

`sorted()` 函数可以对任何可迭代对象进行排序，通过 `key` 参数指定自定义排序规则。

#### 扑克牌排序示例

```python
# 定义花色权重字典
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

def spades_high(card):
    """自定义排序函数：计算每张牌的权重值"""
    # 获取牌面值的索引（2=0, 3=1, ..., A=12）
    rank_value = FrenchDeck.ranks.index(card.rank)
    # 计算总权重：牌面值 × 4 + 花色权重
    return rank_value * len(suit_values) + suit_values[card.suit]

# 按自定义规则排序并遍历
for card in sorted(deck, key=spades_high):
    print(card)
```

#### 排序逻辑解析

##### 权重计算公式
```
总权重 = 牌面值索引 × 4 + 花色权重
```

##### 排序效果
- **先按牌面值排序**：2 < 3 < ... < K < A
- **同牌面值按花色排序**：clubs(0) < diamonds(1) < hearts(2) < spades(3)

##### 示例计算
- 梅花2：`0 × 4 + 0 = 0`（最小）
- 黑桃A：`12 × 4 + 3 = 51`（最大）

#### 核心要点

- `key` 参数接受一个函数，该函数为每个元素返回用于比较的值
- 自定义排序函数使得复杂对象的排序变得简单
- 这种方法适用于任何需要特定排序规则的场景

