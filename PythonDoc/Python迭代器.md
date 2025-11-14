### 基本概念

#### 可迭代对象 (Iterables)
- 在 Python 中，能够使用 `for` 循环遍历的对象称为**可迭代对象**
- 可迭代对象通过实现 `__iter__` 方法来实现迭代功能
- 常见的可迭代对象：列表、元组、字符串、字典、集合、文件对象等

#### 迭代器 (Iterator)
- 迭代器是实际执行迭代过程的对象
- 迭代器必须实现 `__iter__` 和 `__next__` 两个方法
- `__iter__` 方法返回迭代器自身
- `__next__` 方法返回下一个值，如果没有更多元素则抛出 `StopIteration` 异常

### 迭代工作原理

#### 迭代过程
1. 调用可迭代对象的 `__iter__` 方法获取迭代器
2. 重复调用迭代器的 `__next__` 方法获取下一个值
3. 当无法获取更多值时（抛出 `StopIteration`），退出循环

#### 用 while 循环模拟 for 循环
```python
# for 循环的底层实现原理
it = iter(my_str)  # 获取迭代器

while True:
    try:
        print(next(it))  # 获取下一个元素
    except StopIteration:  # 没有更多元素时退出
        break
```

### 自定义可迭代对象

#### 基本实现
要使一个对象成为可迭代对象，需要实现 `__iter__` 和 `__next__` 方法：

```python
class MyIterable:
    def __init__(self, data):
        self.data = data
        self.index = 0
    
    def __iter__(self):
        return self  # 返回迭代器自身
    
    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration  # 迭代结束

# 使用示例
my_iter = MyIterable([1, 2, 3, 4, 5])
for item in my_iter:
    print(item)
```

#### 更优雅的实现方式
可以将迭代器与可迭代对象分离，这样同一个可迭代对象可以创建多个独立的迭代器：

```python
class MyIterable:
    def __init__(self, data):
        self.data = data
    
    def __iter__(self):
        return MyIterator(self.data)

class MyIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        raise StopIteration
```

### 实用案例：文件行迭代器

#### 问题背景
读取大文件时，一次性加载全部内容会占用大量内存。使用迭代器可以逐行读取，节省内存。

#### 实现代码
```python
class LineIterator:
    def __init__(self, filepath):
        self.file = open(filepath, 'r', encoding='utf-8') 
    
    def __iter__(self):
        return self
    
    def __next__(self):
        line = self.file.readline()
        if line:  # 如果读取到内容
            return line.rstrip('\n')  # 去掉换行符
        else:  # 文件结束
            self.file.close()
            raise StopIteration

# 使用示例
for line in LineIterator('large_log_file.log'):
    print(line)
```

#### 更简洁的实现（使用生成器）
```python
def read_lines(filepath):
    """生成器版本的文件行迭代器"""
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.rstrip('\n')

# 使用示例
for line in read_lines('large_log_file.log'):
    print(line)
```

## 内置迭代工具

Python 提供了许多内置函数来处理可迭代对象：

```python
# 创建迭代器
numbers = [1, 2, 3, 4, 5]
iter_numbers = iter(numbers)

# 常用内置函数
result = list(iter_numbers)  # 转换为列表
result = sum([1, 2, 3, 4, 5])  # 求和
result = max([1, 2, 3, 4, 5])  # 最大值
result = min([1, 2, 3, 4, 5])  # 最小值
result = any([True, False, True])  # 任意为真
result = all([True, True, True])  # 全部为真
```

### 注意事项

1. **迭代器是一次性的**：迭代器遍历完成后就不能再次使用，需要重新创建
2. **内存效率**：迭代器按需生成数据，适合处理大型数据集
3. **生成器是特殊的迭代器**：使用 `yield` 关键字的函数会自动创建迭代器
4. **检查可迭代性**：可以使用 `isinstance(obj, collections.abc.Iterable)` 检查对象是否可迭代

```python
from collections.abc import Iterable

my_list = [1, 2, 3]
print(isinstance(my_list, Iterable))  # True
```

通过理解可迭代对象和迭代器的工作原理，可以更有效地处理数据流和创建内存友好的应用程序。