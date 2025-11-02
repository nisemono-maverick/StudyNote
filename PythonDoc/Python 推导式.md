# Python 推导式详解

### 概述

推导式（Comprehension）是 Python 中一种简洁、高效的数据结构构建方式，可以大幅简化代码行数，提升开发效率。Python 支持列表、字典、集合和生成器四种推导式。

### 列表推导式（List Comprehension）

#### 基本语法
```python
[expression for item in iterable]
```

#### 基础用法对比

##### 传统方式
```python
nums = [0, 1, 2, 3, 4, 5]

my_list = []
for i in nums:
    my_list.append(i)
print(my_list)  # [0, 1, 2, 3, 4, 5]
```

##### 推导式方式
```python
my_list = [i for i in nums]
print(my_list)  # [0, 1, 2, 3, 4, 5]
```

##### 带运算的列表推导式

```python
# 存储每个元素的平方
my_list = [i**2 for i in nums]
print(my_list)  # [0, 1, 4, 9, 16, 25]
```

#### 带条件的列表推导式

##### 只有 if 条件
```python
nums = [0, 1, 2, 3, 4, 5]

# 只为偶数的元素计算平方
my_list = [i**2 for i in nums if i % 2 == 0]
print(my_list)  # [0, 4, 16]
```

##### 包含 if-else 条件
```python
nums = [0, 1, 2, 3, 4, 5]

# 偶数平方，奇数立方
my_list = [i**2 if i % 2 == 0 else i**3 for i in nums]
print(my_list)  # [0, 1, 4, 27, 16, 125]
```

**注意**：if-else 条件的语法与只有 if 条件时不同，需要将条件表达式放在 for 循环前面。

#### 嵌套循环的列表推导式

##### 传统方式
```python
letters = ['a', 'b', 'c']
nums = [1, 2, 3]

my_list = []
for i in letters:
    for j in nums:
        my_list.append((i, j))
print(my_list)  # [('a', 1), ('a', 2), ('a', 3), ('b', 1), ('b', 2), ('b', 3), ('c', 1), ('c', 2), ('c', 3)]
```

##### 推导式方式
```python
my_list = [(i, j) for i in letters for j in nums]
print(my_list)  # [('a', 1), ('a', 2), ('a', 3), ('b', 1), ('b', 2), ('b', 3), ('c', 1), ('c', 2), ('c', 3)]
```

### 字典推导式（Dictionary Comprehension）

#### 基本语法
```python
{key_expression: value_expression for item in iterable}
```

#### 基础用法对比

##### 传统方式
```python
letters = ['a', 'b', 'c']
nums = [1, 2, 3]

my_dict = {}
for i, j in zip(letters, nums):
    my_dict[i] = j
print(my_dict)  # {'a': 1, 'b': 2, 'c': 3}
```

##### 推导式方式
```python
my_dict = {i: j for i, j in zip(letters, nums)}
print(my_dict)  # {'a': 1, 'b': 2, 'c': 3}
```

### 集合推导式（Set Comprehension）

#### 基本语法
```python
{expression for item in iterable}
```

#### 基础用法对比

##### 传统方式
```python
l = [1, 2, 3, 4, 5, 5, 6, 6, 6, 7, 8, 9]

my_set = set()
for i in l:
    my_set.add(i)
print(my_set)  # {1, 2, 3, 4, 5, 6, 7, 8, 9}
```

##### 推导式方式
```python
my_set = {i for i in l}
print(my_set)  # {1, 2, 3, 4, 5, 6, 7, 8, 9}
```

### 生成器表达式（Generator Expression）

#### 基本语法
```python
(expression for item in iterable)
```

#### 使用示例
```python
nums = [0, 1, 2, 3, 4, 5]

# 生成器表达式
my_generator = (i**2 for i in nums if i % 2 == 0)

# 使用生成器
for value in my_generator:
    print(value)  # 输出: 0, 4, 16

# 或者转换为列表
result_list = list(my_generator)
```

### 推导式性能优势

推导式不仅在代码简洁性上有优势，在性能上也通常优于传统的循环方式(但是似乎并不会快特别多 有视频结论快8%-20%?)：

```python
import timeit

# 传统方式
def traditional_way():
    result = []
    for i in range(1000):
        if i % 2 == 0:
            result.append(i**2)
    return result

# 推导式方式
def comprehension_way():
    return [i**2 for i in range(1000) if i % 2 == 0]

# 性能测试
print("传统方式:", timeit.timeit(traditional_way, number=10000))
print("推导式方式:", timeit.timeit(comprehension_way, number=10000))
```

### 最佳实践与注意事项

#### 1. 可读性优先
```python
# 过于复杂的推导式（不推荐）
complex_list = [x**2 if x % 2 == 0 else x**3 for x in range(20) if x > 5 and x < 15]

# 拆分为多个步骤（推荐）
filtered_numbers = [x for x in range(20) if x > 5 and x < 15]
result_list = [x**2 if x % 2 == 0 else x**3 for x in filtered_numbers]
```

#### 2. 避免重复计算
```python
# 不推荐：重复计算 len(data)
result = [data[i] for i in range(len(data)) if len(data) > 10]

# 推荐：预先计算
data_length = len(data)
result = [data[i] for i in range(data_length) if data_length > 10]
```

#### 3. 嵌套推导式要适度
```python
# 二维列表展平
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [item for row in matrix for item in row]
print(flattened)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### 总结

| 推导式类型  | 语法                                  | 特点         |
| ------ | ----------------------------------- | ---------- |
| 列表推导式  | `[expr for item in iterable]`       | 返回列表，可包含条件 |
| 字典推导式  | `{key: value for item in iterable}` | 返回字典，键值对形式 |
| 集合推导式  | `{expr for item in iterable}`       | 返回集合，自动去重  |
| 生成器表达式 | `(expr for item in iterable)`       | 返回生成器，惰性求值 |
