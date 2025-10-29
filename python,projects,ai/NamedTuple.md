#python
## 概述

在Python中，当需要同时拥有字典的可读性和元组不变性的数据结构时，可以使用 `namedtuple` 或 `NamedTuple`。这两种方法都提供了给元组元素命名的能力，使得代码更易读，同时保持元组的不可变性。

## 方法一：使用 `collections.namedtuple`

### 基本语法
```python
from collections import namedtuple

# 创建 namedtuple 类型
类型名 = namedtuple('类型名', ['字段1', '字段2', ...])
```

### 示例代码
```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p1 = Point(1, 2)

# 访问方式
print(p1.x)    # 通过字段名访问 → 输出: 1
print(p1[0])   # 通过索引访问 → 输出: 1
```

### 特点
- **轻量级**：不需要定义完整的类
- **可读性强**：可以通过有意义的字段名访问数据
- **保持元组特性**：支持索引访问和不可变性
- **缺点**：会丢失类型信息

## 方法二：使用 `typing.NamedTuple`（推荐）

### 基本语法
```python
from typing import NamedTuple

class 类名(NamedTuple):
    字段1: 类型
    字段2: 类型
    ...
```

### 示例代码
```python
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

p1 = Point(1, 2)

# 访问方式
print(p1.x)    # 通过字段名访问 → 输出: 1
print(p1[0])   # 通过索引访问 → 输出: 1
```

### 优势
- **类型注解**：支持完整的类型提示
- **更好的IDE支持**：代码补全和类型检查更完善
- **类语法**：使用熟悉的类定义语法
- **保持所有优点**：继承了 `namedtuple` 的所有优点

## 两种方法对比

| 特性       | `collections.namedtuple` | `typing.NamedTuple` |
| -------- | ------------------------ | ------------------- |
| 类型提示     | ❌ 不支持                    | ✅ 支持                |
| IDE支持    | 有限                       | 良好                  |
| 语法       | 函数式                      | 类定义式                |
| Python版本 | 所有版本                     | Python 3.6+         |
| 推荐程度     | ⭐⭐                       | ⭐⭐⭐⭐                |

## 使用场景

1. **数据记录**：当需要表示简单的数据记录时
2. **替代简单类**：不需要复杂方法的简单数据结构
3. **API返回**：函数返回多个有含义的值时
4. **配置对象**：存储配置信息，保证不可变性

## 注意事项

- 两种方法创建的对象都是**不可变的**
- 支持所有元组操作（解包、迭代等）
- 可以通过 `_asdict()` 方法转换为字典
- 可以通过 `_replace()` 方法创建修改后的新实例

## 总结

对于现代Python开发，推荐使用 `typing.NamedTuple`，因为它提供了更好的类型支持和开发体验。如果需要兼容旧版本Python或不需要类型提示，可以使用 `collections.namedtuple`。