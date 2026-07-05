---
tags:
  - pandas
  - JSON
  - 数据处理
source: pandas 官方文档
---

# pandas 读取和写入 JSON

## 1. 概述

pandas 通过 `to_json()` 和 `read_json()` 实现 DataFrame / Series 与 JSON 格式之间的互相转换。

| 函数 | 作用 |
|------|------|
| `df.to_json()` | 将 DataFrame / Series 转为 JSON 字符串或文件 |
| `pd.read_json()` | 将 JSON 字符串或文件读入为 DataFrame / Series |

---

## 2. 写入 JSON：`to_json()`

### 2.1 基本用法

```python
import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(5, 2), columns=list("AB"))

# 返回 JSON 字符串
json_str = df.to_json()

# 写入文件
df.to_json("output.json")
```

### 2.2 常用参数

| 参数 | 说明 |
|------|------|
| `path_or_buf` | 输出路径；为 `None` 时返回 JSON 字符串 |
| `orient` | JSON 格式，见下表 |
| `date_format` | 日期格式：`"epoch"`（时间戳）或 `"iso"`（ISO 8601） |
| `date_unit` | 时间精度：`"s"`, `"ms"`, `"us"`, `"ns"`，默认 `"ms"` |
| `double_precision` | 浮点数小数位，默认 10 |
| `force_ascii` | 是否强制 ASCII 编码，默认 `True` |
| `lines` | `orient="records"` 时每行一条记录 |
| `mode` | 文件写入模式：`"w"`（覆盖）或 `"a"`（追加），默认 `"w"` |
| `default_handler` | 遇到不可序列化对象时的处理函数 |

### 2.3 `orient` 格式详解

#### Series 可用

| orient | 格式 | 示例 |
|--------|------|------|
| `index`（默认） | `{index: value}` | `{"x":15,"y":16,"z":17}` |
| `records` | `[value1, value2, ...]` | `[15,16,17]` |
| `split` | `{name, index, data}` | `{"name":"D","index":["x","y","z"],"data":[15,16,17]}` |

#### DataFrame 可用

| orient | 格式 | 示例 |
|--------|------|------|
| `columns`（默认） | `{col: {index: value}}` | `{"A":{"x":1,"y":2},"B":{"x":4,"y":5}}` |
| `index` | `{index: {col: value}}` | `{"x":{"A":1,"B":4},"y":{"A":2,"B":5}}` |
| `records` | `[{col: value}, ...]` | `[{"A":1,"B":4},{"A":2,"B":5}]` |
| `values` | 仅数值数组 | `[[1,4],[2,5]]` |
| `split` | `{columns, index, data}` | `{"columns":["A","B"],"index":["x","y"],"data":[[1,4],[2,5]]}` |
| `table` | JSON Table Schema | 包含 schema + data，保留元数据 |

> **注意**：除 `split` 外，其他 orient 在序列化后可能不保留 index/column 的顺序。

### 2.4 日期处理

```python
# ISO 格式，默认毫秒
df.to_json(date_format="iso")

# ISO 格式，微秒
df.to_json(date_format="iso", date_unit="us")

# 写入文件
df.to_json("test.json", date_format="iso")
```

### 2.5 逐行 JSON（JSONL）

```python
# 每行一个 JSON 对象
df.to_json(orient="records", lines=True)
# 输出: {"a":1,"b":2}\n{"a":3,"b":4}\n
```

### 2.6 特殊类型处理

`NaN`、`NaT`、`None` 会被转为 `null`。如果遇到 pandas 无法直接序列化的类型（如 `np.complex_`），可提供 `default_handler`：

```python
# 会报错
df = pd.DataFrame([1.0, 2.0, complex(1.0, 2.0)])
df.to_json()

# 转为字符串处理
df.to_json(default_handler=str)
```

---

## 3. 读取 JSON：`read_json()`

### 3.1 基本用法

```python
import pandas as pd
from io import StringIO

# 从字符串读取
pd.read_json(StringIO(json_str))

# 从文件读取
pd.read_json("test.json")

# 指定解析为 Series
pd.read_json(StringIO(json_str), typ="series")
```

### 3.2 常用参数

| 参数 | 说明 |
|------|------|
| `filepath_or_buffer` | JSON 字符串、文件路径或 URL |
| `orient` | JSON 格式，需与写入时一致 |
| `typ` | 解析为 `"frame"`（默认）或 `"series"` |
| `dtype` | 类型推断：`True`（默认）、`False`、或指定列类型的 dict |
| `convert_axes` | 是否转换 axes 类型，默认 `True` |
| `convert_dates` | 是否解析日期，默认 `True` |
| `keep_default_dates` | 是否使用默认日期列名规则，默认 `True` |
| `date_unit` | 强制指定时间戳精度 |
| `lines` | 按行读取 JSONL |
| `chunksize` | 与 `lines=True` 配合，分批读取 |
| `encoding` | 编码格式 |
| `engine` | `"ujson"`（默认）或 `"pyarrow"`（仅 `lines=True`） |

### 3.3 dtype 控制

```python
# 不推断类型，全部按 object 读取
pd.read_json("test.json", dtype=object)

# 为指定列指定类型
pd.read_json("test.json", dtype={"A": "float32", "bools": "int8"})
```

### 3.4 保留字符串索引

```python
si = pd.DataFrame(np.zeros((4, 4)), columns=list(range(4)), index=[str(i) for i in range(4)])
json_str = si.to_json()

# 保留字符串类型的 axes
pd.read_json(StringIO(json_str), convert_axes=False)
```

### 3.5 日期精度匹配

写入和读取时的 `date_unit` 要一致：

```python
json = df.to_json(date_format="iso", date_unit="ns")

# 自动检测精度
pd.read_json(StringIO(json))

# 或显式指定
pd.read_json(StringIO(json), date_unit="ns")
```

### 3.6 使用 pyarrow 后端

```python
from io import BytesIO

jsonl = b'{"a": 1, "b": 2}\n{"a": 3, "b": 4}'
pd.read_json(BytesIO(jsonl), lines=True, engine="pyarrow")
```

### 3.7 读取 JSONL 大文件

```python
# 分块读取
with pd.read_json("large.jsonl", lines=True, chunksize=1000) as reader:
    for chunk in reader:
        process(chunk)
```

---

## 4. JSON 规范化：`json_normalize()`

将嵌套 dict / list of dict 展平为 DataFrame。

### 4.1 基本用法

```python
data = [
    {"id": 1, "name": {"first": "Coleen", "last": "Volk"}},
    {"name": {"given": "Mark", "family": "Regner"}},
    {"id": 2, "name": "Faye Raker"},
]

pd.json_normalize(data)
```

输出：

| id | name.first | name.last | name.given | name.family | name |
|---:|-----------:|----------:|-----------:|------------:|-----:|
| 1 | Coleen | Volk | NaN | NaN | NaN |
| NaN | NaN | NaN | Mark | Regner | NaN |
| 2 | NaN | NaN | NaN | NaN | Faye Raker |

### 4.2 指定展开字段

```python
data = [
    {
        "state": "Florida",
        "shortname": "FL",
        "info": {"governor": "Rick Scott"},
        "county": [
            {"name": "Dade", "population": 12345},
            {"name": "Broward", "population": 40000},
        ],
    }
]

pd.json_normalize(data, "county", ["state", "shortname", ["info", "governor"]])
```

输出：

| name | population | state | shortname | info.governor |
|------|-----------:|-------|-----------|---------------|
| Dade | 12345 | Florida | FL | Rick Scott |
| Broward | 40000 | Florida | FL | Rick Scott |

### 4.3 控制嵌套层级

```python
data = [
    {
        "CreatedBy": {"Name": "User 001"},
        "Lookup": {
            "TextField": "Some text",
            "UserField": {"Id": "ID 001", "Name": "Name 001"},
        },
    }
]

pd.json_normalize(data, max_level=1)
```

`max_level=1` 表示只展平到第 1 层嵌套。

---

## 5. Table Schema

`orient="table"` 会生成符合 [JSON Table Schema](https://specs.frictionlessdata.io/table-schema/) 的格式，包含 `schema`（字段元数据）和 `data`（记录）。

```python
df = pd.DataFrame({
    "A": [1, 2, 3],
    "B": ["a", "b", "c"],
    "C": pd.date_range("2016-01-01", periods=3),
}, index=pd.Index(range(3), name="idx"))

# 写入
df.to_json(orient="table", date_format="iso")

# 读取（可保留 dtype 和 index name）
new_df = pd.read_json("test.json", orient="table")
```

### pandas 类型与 Table Schema 映射

| pandas 类型 | Table Schema 类型 |
|-------------|-------------------|
| int64 | integer |
| float64 | number |
| bool | boolean |
| datetime64[ns] | datetime |
| timedelta64[ns] | duration |
| categorical | any |
| object | str |

---

## 6. 常见问题

| 问题 | 说明 |
|------|------|
| 索引顺序不一致 | 除 `split` 外，其他 orient 不保证 round-trip 后索引顺序一致 |
| float 被转 int | 读取时，若 float 列可安全转为 int，pandas 会自动转换 |
| bool 被转 int | 读取重建时 bool 列可能被转为 int，可用 `dtype` 指定 |
| 大整数被当日期 | `convert_dates=True` 时，列名像日期的整数可能被误判，可用 `convert_dates=False` |
| `index` 作为索引名 | 使用 `orient="table"` 时，索引名不能是 `"index"` 或以 `"level_"` 开头，否则 round-trip 会丢失 |

---

## 7. 快速选择建议

| 场景 | 推荐方式 |
|------|---------|
| 需要保留索引和列名 | `orient="split"` 或 `"table"` |
| 传给前端 / JS 库 | `orient="records"` |
| 需要保留 dtype 元数据 | `orient="table"` |
| 大数据逐行处理 | `lines=True` + `chunksize` |
| 嵌套 JSON 数据 | `pd.json_normalize()` |
