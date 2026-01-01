## 概述

Python 3.10 引入了 `match` 语句，这是一种结构化的模式匹配机制，类似于其他语言中的 `switch case`，但功能更加强大。它不仅支持简单的值匹配，还支持结构匹配、析构、守卫条件等高级特性。

## 基本语法对比

### 传统 if-elif-else 方式
```python
def if_traffic_light(color):
    if color == 'red':
        return 'Stop'
    elif color == 'yellow':
        return 'Caution'
    elif color == 'green':
        return 'Go'
    else:
        return 'Invalid color'
```

### match case 方式
```python
def match_traffic_light(color):
    match color:
        case 'red':
            return 'Stop'
        case 'yellow':
            return 'Caution'
        case 'green':
            return 'Go'
        case _:
            return 'Invalid color'
```

## 核心特性

### 1. 结构匹配与析构

`match case` 的强大之处在于能够匹配复杂的数据结构，并自动解构（destructure）它们。

#### 匹配序列（元组、列表等）

```python
def match_point(point: tuple):
    match point:
        case (0, 0):
            print('原点!')
        case (0, x) | (x, 0):  # 使用 | 表示或模式
            print(f'在坐标轴上，非零坐标为 {x}')
        case (x, y):
            print(f'x={x}, y={y}')
        case _:
            print(f'{point} 不是有效的点!')
```

#### 指定类型匹配
```python
def match_sequence(seq):
    match seq:
        case list([1, 2, 3]):
            print("列表 [1, 2, 3]")
        case tuple((x, y)):
            print(f"元组包含两个元素: {x}, {y}")
        case str(s):
            print(f"字符串: {s}")
        case _:
            print("未知类型")
```

### 2. 守卫条件（Guard Clauses）

可以在 `case` 语句中添加 `if` 条件进行更精细的控制：

```python
def match_quadrant(point):
    match point:
        case (x, y) if x > 0 and y > 0:
            print('第一象限')
        case (x, y) if x < 0 and y > 0:
            print('第二象限')
        case (x, y) if x < 0 and y < 0:
            print('第三象限')
        case (x, y) if x > 0 and y < 0:
            print('第四象限')
        case (x, y) if x == 0 or y == 0:
            print('在坐标轴上')
        case _:
            print('无效坐标')
```

### 3. 匹配字典

```python
def match_dict(data):
    match data:
        case {'type': 'user', 'name': name, 'age': age} if age >= 18:
            print(f'成年用户: {name}')
        case {'type': 'user', 'name': name, 'age': age}:
            print(f'未成年用户: {name}')
        case {'type': 'admin', 'username': username}:
            print(f'管理员: {username}')
        case _:
            print('未知数据类型')
```

### 4. 匹配自定义类

要使自定义类支持模式匹配，需要定义 `__match_args__` 属性：

```python
class Point:
    # 定义匹配时使用的属性顺序
    __match_args__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f'Point({self.x}, {self.y})'

class Circle:
    __match_args__ = ('center', 'radius')
    
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

def match_shapes(shape):
    match shape:
        case Point(0, 0):
            print('原点')
        case Point(x, 0) | Point(0, x):
            print(f'在坐标轴上: ({x})')
        case Point(x, y):
            print(f'点坐标: ({x}, {y})')
        case Circle(Point(0, 0), r):
            print(f'以原点为圆心，半径为 {r} 的圆')
        case Circle(center, radius):
            print(f'圆心在 {center}，半径为 {radius} 的圆')
        case _:
            print('未知形状')
```

### 5. 通配符和占位符

- `_`: 通配符，匹配任意值但不绑定变量
- `*rest`: 匹配剩余的所有元素

```python
def match_list(lst):
    match lst:
        case []:
            print('空列表')
        case [x]:
            print(f'单元素列表: {x}')
        case [first, second, *rest]:
            print(f'第一个: {first}, 第二个: {second}, 剩余: {rest}')
        case [1, 2, *tail]:
            print(f'以1,2开头，后面是: {tail}')
```

## 高级模式匹配技巧

### 1. 嵌套模式匹配

```python
def match_nested(data):
    match data:
        case {'user': {'name': name, 'age': age}, 'status': 'active'}:
            print(f'活跃用户: {name}, 年龄: {age}')
        case {'user': {'name': name}, 'status': 'inactive'}:
            print(f'非活跃用户: {name}')
        case _:
            print('无效数据')
```

### 2. 类型匹配

```python
from typing import Union

def process_value(value: Union[int, str, list]):
    match value:
        case int(n):
            print(f'整数: {n}')
        case str(s):
            print(f'字符串: {s}')
        case list(items):
            print(f'列表，包含 {len(items)} 个元素')
```

### 3. 常量与变量区分

以小写字母开头的名称视为变量，将绑定匹配的值；以大写字母开头的名称视为常量，将进行相等性比较。

```python
MAX_VALUE = 100

def match_with_constants(value):
    match value:
        case MAX_VALUE:  # 常量，比较是否等于100
            print('达到最大值')
        case x if x < MAX_VALUE:  # x是变量
            print(f'小于最大值: {x}')
        case _:
            print('其他情况')
```

## 性能与注意事项

1. **性能**: `match` 语句通常比等价的 `if-elif` 链更快，因为Python可以优化模式匹配。

2. **顺序**: case语句按顺序匹配，第一个匹配的模式会被执行。

3. **完备性检查**: 虽然Python不强制要求匹配所有情况，但良好的实践是使用 `case _:` 作为默认情况。

4. **版本要求**: `match` 语句需要Python 3.10或更高版本。

## 实际应用示例

```python
def handle_http_response(response):
    match response:
        case {'status': 200, 'data': data}:
            return process_data(data)
        case {'status': 404}:
            raise NotFoundError("资源不存在")
        case {'status': 500, 'error': error_msg}:
            raise ServerError(error_msg)
        case {'status': status} if 400 <= status < 500:
            raise ClientError(f"客户端错误: {status}")
        case _:
            raise UnknownResponseError("未知响应格式")
```

## 总结

Python的 `match case` 语句提供了强大而灵活的模式匹配能力，它比传统的 `if-elif-else` 语句更加清晰和强大，特别适合处理复杂的数据结构。通过结构匹配、守卫条件和模式析构，可以写出更简洁、更易读的代码。