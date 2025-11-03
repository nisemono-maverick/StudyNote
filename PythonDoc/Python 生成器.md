### 概述

生成器（Generator）是 Python 中一种特殊的迭代器，它不会一次性将所有值存储在内存中，而是按需生成值，这在处理大量数据时能显著提高内存效率和程序性能。

### 生成器 vs 列表

#### 列表方式（内存效率低）
```python
def square_numbers(nums):
    """传统列表方式：一次性返回所有结果"""
    result = []
    for i in nums:
        result.append(i * i)
    return result

my_nums = square_numbers([1, 2, 3, 4, 5])
print(my_nums)  # [1, 4, 9, 16, 25]
```

**缺点**：对于大量数据，会占用大量内存。

#### 生成器方式（内存效率高）
```python
def square_numbers(nums):
    """生成器方式：按需生成结果"""
    for i in nums:
        yield i * i  # 使用 yield 关键字

my_gen = square_numbers([1, 2, 3, 4, 5])
print(my_gen)  # <generator object square_numbers at 0x...>
```

**优点**：只在需要时生成值，节省内存。

### 生成器函数

#### 基本概念
- 使用 `yield` 关键字而非 `return`
- 调用时返回生成器对象，不会立即执行
- 每次调用 `next()` 时执行到下一个 `yield` 语句
- 保持函数状态，下次从上次暂停处继续

### 执行流程示例
```python
def simple_generator():
    print("开始执行")
    yield 1
    print("继续执行")
    yield 2
    print("结束执行")
    yield 3

gen = simple_generator()

print("第一次调用next:")
print(next(gen))  # 输出: 开始执行 \n 1

print("第二次调用next:")
print(next(gen))  # 输出: 继续执行 \n 2

print("第三次调用next:")
print(next(gen))  # 输出: 结束执行 \n 3

# 再次调用会抛出 StopIteration 异常
```

### 生成器的遍历方式

#### 1. 使用 `next()` 函数
```python
def square_numbers(nums):
    for i in nums:
        yield i * i

my_gen = square_numbers([1, 2, 3, 4, 5])

print(next(my_gen))  # 1
print(next(my_gen))  # 4
print(next(my_gen))  # 9
```

#### 2. 使用 `for` 循环（推荐）
```python
def square_numbers(nums):
    for i in nums:
        yield i * i

my_gen = square_numbers([1, 2, 3, 4, 5])

for num in my_gen:
    print(num)  # 依次输出: 1, 4, 9, 16, 25
```

#### 重要特性：生成器只能遍历一次
```python
def square_numbers(nums):
    for i in nums:
        yield i * i

my_gen = square_numbers([1, 2, 3, 4, 5])

print('使用 next 函数:')
print(next(my_gen))  # 1

print('然后使用 for 循环:')
for num in my_gen:
    print(num)  # 输出: 4, 9, 16, 25（从 4 开始，不是 1）
```

**注意**：生成器是状态保持的，一旦值被生成，就无法重新获取。

### 生成器表达式

#### 基本语法
```python
(expression for item in iterable)
```

#### 使用示例
```python
nums = [0, 1, 2, 3, 4, 5]

# 生成器表达式
my_generator = (i**2 for i in nums if i % 2 == 0)

print(my_generator)  # <generator object <genexpr> at 0x...>

# 使用 for 循环遍历
for value in my_generator:
    print(value)  # 输出: 0, 4, 16

# 或转换为列表（会耗尽生成器）
my_generator = (i**2 for i in nums if i % 2 == 0)
result_list = list(my_generator)
print(result_list)  # [0, 4, 16]
```

### 生成器的优势

#### 1. 内存效率对比
```python
import sys

# 列表推导式（占用更多内存）
list_size = sys.getsizeof([i**2 for i in range(1000)])

# 生成器表达式（占用极少内存）
gen_size = sys.getsizeof((i**2 for i in range(1000)))

print(f"列表大小: {list_size} 字节")  # 约 9000+ 字节
print(f"生成器大小: {gen_size} 字节")  # 约 100+ 字节
```

#### 2. 处理大数据集
```python
def read_large_file(file_path):
    """逐行读取大文件，避免内存溢出"""
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

# 使用生成器处理大文件
for line in read_large_file('huge_file.txt'):
    process_line(line)  # 每次只处理一行，不加载整个文件到内存
```

### 高级生成器用法

#### 1. 生成器与 `send()` 方法
```python
def counter(max_value):
    count = 0
    while count < max_value:
        received = yield count
        if received is not None:
            count = received
        else:
            count += 1

gen = counter(10)

print(next(gen))  # 0
print(next(gen))  # 1
print(gen.send(5))  # 5（设置当前值）
print(next(gen))  # 6
```

#### 2. 生成器与 `yield from`
```python
def chain_generators():
    yield from (x for x in range(3))
    yield from (x**2 for x in range(3))

for value in chain_generators():
    print(value)  # 输出: 0, 1, 2, 0, 1, 4
```

#### 3. 无限序列生成器
```python
def fibonacci():
    """生成斐波那契数列"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
for i in range(10):
    print(next(fib))  # 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
```

### 实际应用场景

#### 1. 数据处理管道
```python
def read_data():
    for i in range(1000000):
        yield i

def filter_even(numbers):
    for num in numbers:
        if num % 2 == 0:
            yield num

def square(numbers):
    for num in numbers:
        yield num ** 2

# 构建数据处理管道
data_pipeline = square(filter_even(read_data()))

for result in data_pipeline:
    if result > 100:
        break
    print(result)  # 0, 4, 16, 36, 64, 100
```

#### 2. 实时数据流处理
```python
def sensor_data():
    """模拟传感器数据流"""
    import random
    while True:
        yield random.randint(0, 100)

def process_sensor_data():
    for data in sensor_data():
        if data > 90:
            print(f"警告: 传感器读数过高: {data}")
        elif data < 10:
            print(f"警告: 传感器读数过低: {data}")
        else:
            print(f"正常读数: {data}")

# 开始处理（Ctrl+C 停止）
# process_sensor_data()
```