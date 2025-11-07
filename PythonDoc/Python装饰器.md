### 概述
装饰器（Decorator）是Python中一种强大的语法特性，允许开发者在不修改原函数代码的情况下，动态地增强或修改函数的行为。这种机制基于高阶函数和闭包实现，遵循开放-封闭原则，即对扩展开放，对修改封闭。

### 前置知识：函数作为一等对象

在Python中，函数是一等对象（First-class Object），这意味着函数可以像其他对象一样被传递、赋值和返回。这是理解装饰器的基础。

#### 示例：函数作为参数

```python
def square(x):
    """计算平方"""
    return x * x

def print_running(func, x):
    """在执行函数前打印运行信息"""
    print(f'{func.__name__} is running.')
    return func(x)

# 函数作为参数传递
result = print_running(square, 2)
print(f'执行结果: {result}')
```

输出：
```
square is running.
执行结果: 4
```

### 装饰器基础

#### 装饰器定义

装饰器本质上是一个接收函数作为参数并返回新函数的可调用对象。

```python
import time

def execution_timer(func):
    """记录函数执行时间的装饰器"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)  # 执行原函数
        end_time = time.time()
        execution_time = end_time - start_time
        print(f'{func.__name__} 执行时间: {execution_time:.6f} 秒')
        return result
    return wrapper
```

#### 装饰器应用方式

##### 方式一：显式调用
```python
def square(x):
    return x * x

# 应用装饰器
square = execution_timer(square)
result = square(10)
print(f'计算结果: {result}')
```

##### 方式二：使用@语法糖（推荐）
```python
@execution_timer
def square(x):
    return x * x

result = square(10)
print(f'计算结果: {result}')
```

两种方式输出相同：
```
square 执行时间: 0.000001 秒
计算结果: 100
```

### 参数化装饰器

参数化装饰器（或称装饰器工厂）允许通过参数配置装饰器的行为，返回特定的装饰器实例。

#### 定义参数化装饰器

```python
import time
import functools

def timer(threshold=0.0):
    """
    带阈值检测的执行时间装饰器
    
    Args:
        threshold: 时间阈值（秒），超过此阈值将输出警告
    """
    def decorator(func):
        @functools.wraps(func)  # 保留原函数元信息
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            
            if execution_time > threshold:
                print(f'警告: {func.__name__} 执行时间 {execution_time:.3f} 秒超过阈值 {threshold} 秒')
            
            return result
        return wrapper
    return decorator
```

#### 参数化装饰器的应用

```python
@timer(threshold=0.2)
def delayed_operation():
    """模拟耗时操作"""
    time.sleep(0.4)
    return "操作完成"

# 等价于: delayed_operation = timer(threshold=0.2)(delayed_operation)
result = delayed_operation()
print(f'执行结果: {result}')
```

输出：
```
警告: delayed_operation 执行时间 0.400 秒超过阈值 0.2 秒
执行结果: 操作完成
```

#### 保留函数元信息

使用`functools.wraps`装饰器可以保留原函数的名称、文档字符串等元信息：

```python
# 不使用 functools.wraps
print(delayed_operation.__name__)  # 输出: wrapper

# 使用 functools.wraps
print(delayed_operation.__name__)  # 输出: delayed_operation
```


### 装饰器的优势
- 代码复用性
装饰器将横切关注点（如日志记录、性能监测、权限验证）封装为可重用的组件。
- 关注点分离
通过装饰器可以将核心业务逻辑与辅助功能分离，提高代码的可读性和可维护性。
- 非侵入式扩展
装饰器允许在不修改源代码的情况下扩展第三方库或框架中函数的功能。

### 组合性
多个装饰器可以组合使用，按声明顺序依次应用：

```python
@decorator1
@decorator2
def my_function():
    pass

# 等价于: my_function = decorator1(decorator2(my_function))
```
