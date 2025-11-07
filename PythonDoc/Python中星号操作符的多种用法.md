
### 1. 基础数学运算
作为乘法运算符用于数字计算：
```python
print(2*3)  # 6
```

### 2. 序列重复
对字符串和列表进行重复操作：
```python
print('ha'*3)      # hahaha
print([1,2]*3)     # [1,2,1,2,1,2]
```

### 3. 打包操作

#### 单个星号`*`打包序列
```python
numbers = [1,2,3,4,5]
first, *rest = numbers
print(first)  # 1
print(rest)   # [2,3,4,5]
```

#### 函数定义中的可变参数
```python
def print_values(*args):
    for arg in args:
        print(arg)

print_values(1,2,3,4)
# 输出：
# 1
# 2
# 3
# 4
```

#### 双星号`**`打包字典参数
```python
def example(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')

example(a=1, b=2, c=3)
# 输出：
# a = 1
# b = 2
# c = 3
```

### 4. 解包操作

#### 序列解包
```python
def greet(name, age):
    print(f'hello {name}, you are {age} years old.')

person = ('Alice', 30)
greet(*person)  # hello Alice, you are 30 years old.
```

#### 字典解包
```python
def create_profile(name, age, email):
    print(f'name: {name}')
    print(f'age: {age}')
    print(f'email: {email}')

option = {
    'name': 'tony',
    'age': '18',
    'email': 'tony@qq.com'
}

create_profile(**option)
# 输出：
# name: tony
# age: 18
# email: tony@qq.com
```

## 5. 合并操作

#### 合并序列
```python
list1 = [1,2,3]
tuple1 = (4,5,6)
merged = [*list1, *tuple1]
print(merged)  # [1, 2, 3, 4, 5, 6]
```

#### 合并字典
```python
dict1 = {'a':1, 'b':2}
dict2 = {'c':3, 'd':4}
merged = {**dict1, **dict2}
print(merged)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}
```
