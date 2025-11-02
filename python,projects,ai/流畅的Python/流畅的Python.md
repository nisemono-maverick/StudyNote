# [[一摞python风格的纸牌]]


## 特殊方法是如何调用的
- 特殊方法供python解释器调用，而非开发者调用
- 如写`len(object)`时，解释器会调用实现的`__len__`方法
- 对于List、str、bytearray或Numpy数组等内置类型时，python解释器直接读取底层C语言实现的名为PyVarObject的结构体中的ob_size字段

- 当输入`for i in x:`语句时，背后是调用了`iter(x)`，解释器又调用`x.__iter__()`或`x.__getitem__()`

- 特殊方法最主要的用途有几种
	- 模拟数值类型
	- 对象的字符串表示类型
	- 对象的布尔值
	- 实现容器

### 模拟数值类型
实现一个二维向量类
使用`__repr__、__abs__、__add__、__mul__`等特殊方法实现Vector类的这几种运算
```python
import math

class Vector:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	
	def __repr__(self):
		return f'Vector({self.x!r}, {self.y!r})' # 这是什么意思
		
	def __abs__(self):
		return math.hypot(self.x, self.y)
	
	def __bool__(self):
		return bool(abs(self))
		
	def __add__(self, other):
		x = self.x + other.x
		y = self.y + other.y
		return Vector(x, y)
		
	def __mul__(self, scaler):
		return Vector(self.x * scaler, self.y * scaler)
```