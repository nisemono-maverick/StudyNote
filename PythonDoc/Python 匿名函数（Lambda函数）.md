
### 概述

匿名函数（Lambda函数）是 Python 中一种简洁的函数定义方式，它允许我们在一行代码中创建小型、匿名的函数对象。Lambda 函数特别适合需要函数对象作为参数的场景，能够使代码更加简洁和函数式。

### 基本语法

```python
lambda arguments: expression
```

- `lambda`：关键字，表示定义匿名函数
- `arguments`：函数参数，可以是多个，用逗号分隔
- `expression`：单个表达式，作为函数的返回值

### 基础用法对比

#### 传统函数定义
```python
def add(a, b):
    return a + b

print(add(3, 4))  # 输出: 7
```

#### Lambda 函数定义
```python
add = lambda a, b: a + b
print(add(3, 4))  # 输出: 7
```

### 常用场景：作为其他函数的参数

#### 1. 与 `map()` 函数结合
```python
my_lst = [1, 2, 3, 4, 5]
new_lst = list(map(lambda x: x ** 2, my_lst))
print(new_lst)  # 输出: [1, 4, 9, 16, 25]
```

#### 2. 与 `filter()` 函数结合
```python
my_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = list(filter(lambda x: x % 2 == 0, my_lst))
print(even_numbers)  # 输出: [2, 4, 6, 8, 10]
```

#### 3. 与 `sorted()` 函数结合
```python
# 按字符串长度排序
words = ['apple', 'banana', 'cherry', 'date']
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)  # 输出: ['date', 'apple', 'banana', 'cherry']

# 按第二个元素排序
pairs = [(1, 2), (3, 1), (5, 0)]
sorted_pairs = sorted(pairs, key=lambda x: x[1])
print(sorted_pairs)  # 输出: [(5, 0), (3, 1), (1, 2)]
```

### 实际应用：简化条件逻辑

#### 原始代码（冗长）
```python
def user_logging(user):
    if user.level == 1:
        user.credits += 2
    if user.level == 2:
        user.credits += 5
    if user.level == 3:
        user.credits += 10
    if user.level == 4:
        user.credits += 20
```

#### 使用 Lambda 改进
```python
def user_logging(user):
    level_credit_map = {
        1: 2,
        2: 5,
        3: 10,
        4: 20,
    }
    user.credits += level_credit_map.get(user.level, 0)
```

### 更多 Lambda 函数示例

#### 条件表达式
```python
# 返回两个数中较大的数
max_num = lambda x, y: x if x > y else y
print(max_num(5, 8))  # 输出: 8

# 判断奇偶
is_even = lambda x: True if x % 2 == 0 else False
print(is_even(4))  # 输出: True
print(is_even(7))  # 输出: False
```

#### 嵌套 Lambda 函数
```python
# 外层 Lambda 接受参数 x，返回一个内层 Lambda（接受 y）
outer = lambda x: (lambda y: x + y)

# 调用方式
inner_func = outer(10)  # 返回一个函数：lambda y: 10 + y
result = inner_func(5)  # 调用内层函数：10 + 5 = 15
print(result)  # 输出 15

# 简写调用
result = outer(10)(5)
print(result)  # 输出 15
```

### Lambda 函数的限制和注意事项

#### 1. 只能包含单个表达式
```python
# 错误示例：Lambda 中不能包含语句
# invalid_lambda = lambda x: print(x); return x * 2

# 正确做法：使用普通函数
def process_number(x):
    print(x)
    return x * 2
```

#### 2. 变量作用域
```python
# Lambda 函数可以访问外部变量
x = 10
multiplier = lambda y: x * y
print(multiplier(5))  # 输出: 50

# 但要注意变量绑定的时机
functions = []
for i in range(3):
    functions.append(lambda x: x + i)

# 所有函数都会使用 i 的最终值 2
print([f(10) for f in functions])  # 输出: [12, 12, 12]

# 解决方法：使用默认参数
functions = []
for i in range(3):
    functions.append(lambda x, i=i: x + i)

print([f(10) for f in functions])  # 输出: [10, 11, 12]
```

## 何时使用 Lambda 函数

### 适合使用 Lambda 的场景
1. **简单的操作**：一行代码可以完成的简单转换或计算
2. **函数式编程**：作为 `map()`, `filter()`, `sorted()` 等函数的参数
3. **回调函数**：需要简单函数作为参数的情况
4. **临时函数**：只在当前上下文使用的简单函数

### 不适合使用 Lambda 的场景
1. **复杂逻辑**：需要多行代码或复杂控制流
2. **需要文档**：函数需要详细的文档说明
3. **可重用代码**：需要在多个地方使用的函数
4. **调试需求**：需要清晰函数名进行调试的情况
