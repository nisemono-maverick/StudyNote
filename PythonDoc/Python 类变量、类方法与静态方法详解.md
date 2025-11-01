
### 概述

在面向对象编程中，除了实例变量和实例方法外，Python 还提供了**类变量**、**类方法**和**静态方法**，用于处理与类本身相关而非特定实例相关的数据和操作。

### 类变量（Class Variables）

#### 定义与用途
类变量属于类本身，在所有实例间共享，用于存储与整个类相关的信息。

#### 基本语法
```python
class ClassName:
    class_variable = value  # 类变量定义
    
    def __init__(self, ...):
        # 在构造方法中更新类变量
        ClassName.class_variable += 1
```
#### 实际示例
```python
class Student:
    student_num = 0  # 类变量：记录学生总数
    
    def __init__(self, name, sex):
        self.name = name      # 实例变量
        self.sex = sex        # 实例变量
        Student.student_num += 1  # 更新类变量

# 创建实例
s1 = Student('Maverick', 'Male')
s2 = Student('Alice', 'Female')
```

#### 访问方式
- **推荐方式**：通过类名访问 `ClassName.class_variable`
- **可行但不推荐**：通过实例访问 `instance.class_variable`
```python
print(f'学生总数: {Student.student_num}')  # 输出: 学生总数: 2
print(f's1.student_num: {s1.student_num}') # 输出: s1.student_num: 2
```
### 类方法（Class Methods）

#### 定义与用途
类方法用于操作类变量或执行与类相关的操作，类方法前需要加上装饰器`@classmethod`,第一个参数为类本身（通常命名为`cls`）。

#### 基本语法
```python
class ClassName:
    @classmethod
    def class_method(cls, parameters):
        # 方法体
        pass
```

#### 实际应用

##### 1. 操作类变量
```python
class Student:
    student_num = 0
    
    def __init__(self, name, sex):
        self.name = name
        self.sex = sex
        Student.student_num += 1
    
    @classmethod
    def add_students(cls, add_num):
        """批量添加学生"""
        cls.student_num += add_num
        print(f"批量添加了 {add_num} 名学生")

# 使用类方法
Student.add_students(5)  # 批量添加了 5 名学生
print(f"当前学生总数: {Student.student_num}")
```

##### 2. 替代构造方法
```python
class Student:
    student_num = 0
    
    def __init__(self, name, sex):
        self.name = name
        self.sex = sex
        Student.student_num += 1
    
    @classmethod
    def from_string(cls, info):
        """从字符串创建学生实例"""
        name, sex = info.split(' ')
        return cls(name, sex)  # 调用原始构造方法
    
    @classmethod
    def from_list(cls, info_list):
        """从列表创建学生实例"""
        return cls(info_list[0], info_list[1])

# 使用替代构造方法
s2 = Student.from_string('Maverick Male')
s3 = Student.from_list(['Bob', 'Male'])
```

### 静态方法（Static Methods）

#### 定义与用途
静态方法与类相关但不操作类或实例，相当于定义在类命名空间中的普通函数，静态方法前需要加上装饰器`@staticmethod`。

#### 基本语法
```python
class ClassName:
    @staticmethod
    def static_method(parameters):
        # 方法体
        pass
```

#### 实际应用
```python
class Student:
    student_num = 0
    
    def __init__(self, name, sex):
        self.name = name
        self.sex = sex
        Student.student_num += 1
    
    @staticmethod
    def name_len(name):
        """计算姓名长度"""
        return len(name)
    
    @staticmethod
    def is_valid_name(name):
        """验证姓名是否有效"""
        return len(name) >= 2 and name.isalpha()

# 使用静态方法
print(f"姓名长度: {Student.name_len('Maverick')}")
print(f"姓名是否有效: {Student.is_valid_name('Tom')}")

s2 = Student.from_string('Maverick Male')
print(f's2.name: {s2.name}, 姓名长度: {Student.name_len(s2.name)}')
```

### 三者的区别总结

| 特性         | 实例方法                | 类方法                                    | 静态方法                                   |
| ---------- | ------------------- | -------------------------------------- | -------------------------------------- |
| **装饰器**    | 无                   | `@classmethod`                         | `@staticmethod`                        |
| **第一个参数**  | `self`（实例）          | `cls`（类）                               | 无特殊参数                                  |
| **访问实例变量** | ✅                   | ❌                                      | ❌                                      |
| **访问类变量**  | ✅                   | ✅                                      | ❌                                      |
| **调用方式**   | `instance.method()` | `Class.method()` 或 `instance.method()` | `Class.method()` 或 `instance.method()` |

### 最佳实践建议

1. **类变量**：用于存储类级别的共享数据
2. **类方法**：
   - 操作类变量时使用
   - 提供替代构造方法时使用
   - 需要访问类状态时使用
3. **静态方法**：
   - 与类功能相关但不需要访问类或实例状态时使用
   - 作为工具函数时使用

## 完整示例代码

```python
class Student:
    student_num = 0  # 类变量
    
    def __init__(self, name, sex):
        self.name = name
        self.sex = sex
        Student.student_num += 1
    
    @classmethod
    def get_student_count(cls):
        """获取学生总数"""
        return cls.student_num
    
    @classmethod
    def from_string(cls, info):
        """从字符串创建实例"""
        name, sex = info.split(' ')
        return cls(name, sex)
    
    @classmethod
    def reset_counter(cls):
        """重置计数器（用于测试等场景）"""
        cls.student_num = 0
    
    @staticmethod
    def validate_student_info(name, sex):
        """验证学生信息"""
        if not name or len(name) < 2:
            return False
        if sex not in ['Male', 'Female']:
            return False
        return True
    
    @staticmethod
    def calculate_name_score(name):
        """计算姓名分数（示例用途）"""
        return len(name) * 10

# 使用示例
Student.reset_counter()

s1 = Student('Maverick', 'Male')
s2 = Student.from_string('Alice Female')

print(f"学生总数: {Student.get_student_count()}")
print(f"信息验证: {Student.validate_student_info('Bob', 'Male')}")
print(f"姓名分数: {Student.calculate_name_score('Maverick')}")
```
