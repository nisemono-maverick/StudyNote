# CS61B Project 3: Build Your Own World

一个基于瓷砖（Tile-based）的 2D 世界生成器项目框架。

## 项目结构

```
proj3/
├── src/
│   ├── core/           # 核心逻辑
│   │   ├── Main.java              # 程序入口
│   │   ├── World.java             # 世界生成逻辑（待实现）
│   │   └── AutograderBuddy.java   # 自动评分辅助类
│   ├── tileengine/     # 瓷砖渲染引擎
│   │   ├── TETile.java            # 瓷砖类定义
│   │   ├── Tileset.java           # 预定义瓷砖集合
│   │   └── TERenderer.java        # 渲染器
│   └── utils/          # 工具类
│       ├── FileUtils.java         # 文件操作工具
│       └── RandomUtils.java       # 随机数生成工具
├── tests/
│   └── WorldGenTests.java         # 世界生成测试
└── README.md           # 本文件
```

## 模块说明

### 1. Core 模块 (`src/core/`)

#### `Main.java`
- **作用**: 程序入口点
- **状态**: 待实现
- **说明**: 包含 `main` 方法，用于启动整个应用程序

#### `World.java`
- **作用**: 世界生成核心逻辑
- **状态**: 待实现
- **说明**: 负责生成 2D 世界地图，包括房间、走廊、地形等

#### `AutograderBuddy.java`
- **作用**: 自动评分系统交互接口
- **核心方法**:
  - `getWorldFromInput(String input)`: 根据输入字符串模拟游戏，返回世界状态
  - `isGroundTile(TETile t)`: 判断是否为地面瓷砖
  - `isBoundaryTile(TETile t)`: 判断是否为边界/墙壁瓷砖
- **说明**: 处理以 `:q` 结尾的保存退出指令

### 2. Tile Engine 模块 (`src/tileengine/`)

#### `TETile.java`
- **作用**: 定义世界中的单个瓷砖
- **属性**:
  - `character`: 显示的字符
  - `textColor`: 文字颜色
  - `backgroundColor`: 背景颜色
  - `description`: 描述信息（鼠标悬停显示）
  - `filepath`: 可选的图片路径（size 16x16）
  - `id`: 唯一标识符
- **核心方法**:
  - `draw(x, y)`: 在指定位置绘制瓷砖
  - `colorVariant()`: 生成颜色变体
  - `toString()`: 将世界转换为字符串表示
  - `copyOf()`: 复制瓷砖数组

#### `Tileset.java`
- **作用**: 预定义的瓷砖常量集合
- **可用瓷砖**:

| 常量              | 字符  | 描述   |
| --------------- | --- | ---- |
| `AVATAR`        | `@` | 玩家角色 |
| `WALL`          | `#` | 墙壁   |
| `FLOOR`         | `·` | 地板   |
| `NOTHING`       | ` ` | 空白   |
| `GRASS`         | `"` | 草地   |
| `WATER`         | `≈` | 水    |
| `FLOWER`        | `❀` | 花    |
| `LOCKED_DOOR`   | `█` | 锁着的门 |
| `UNLOCKED_DOOR` | `▢` | 未锁的门 |
| `SAND`          | `▒` | 沙子   |
| `MOUNTAIN`      | `▲` | 山    |
| `TREE`          | `♠` | 树    |
| `CELL`          | `█` | 细胞   |


#### `TERenderer.java`
- **作用**: 瓷砖世界渲染器
- **核心方法**:
  - `initialize(w, h)`: 初始化画布
  - `initialize(w, h, xOff, yOff)`: 带偏移量的初始化
  - `renderFrame(world)`: 渲染整个帧
  - `drawTiles(world)`: 仅绘制瓷砖（不清除画布）
- **说明**: 基于 `StdDraw` 实现，支持双缓冲

### 3. Utils 模块 (`src/utils/`)

#### `FileUtils.java`
- **作用**: 简单的文件操作封装
- **方法**:
  - `writeFile(filename, contents)`: 写入文件
  - `readFile(filename)`: 读取文件
  - `fileExists(filename)`: 检查文件是否存在

#### `RandomUtils.java`
- **作用**: 伪随机数生成工具库
- **分布类型**:
  - Uniform: 均匀分布
  - Bernoulli: 伯努利分布
  - Gaussian: 高斯/正态分布
  - Geometric: 几何分布
  - Poisson: 泊松分布
  - Pareto: 帕累托分布
  - Cauchy: 柯西分布
  - Exponential: 指数分布
- **其他功能**:
  - `shuffle()`: 数组随机打乱
  - `permutation()`: 生成随机排列
  - `discrete()`: 离散分布采样

### 4. Tests 模块 (`tests/`)

#### `WorldGenTests.java`
- **作用**: 世界生成测试用例
- **测试方法**:
  - `basicTest()`: 基础测试，使用种子生成世界并显示 5 秒
  - `basicInteractivityTest()`: 交互测试（待实现）
  - `basicSaveTest()`: 存档/读档测试（待实现）
- **输入格式**: `n<seed>s`（如 `n1234567890123456789s`）

## 使用方式

### 生成世界

```java
// 通过种子生成世界
TETile[][] world = AutograderBuddy.getWorldFromInput("n1234567890123456789s");

// 渲染世界
TERenderer ter = new TERenderer();
ter.initialize(width, height);
ter.renderFrame(world);
```

### 使用瓷砖

```java
// 设置世界某位置为地板
world[x][y] = Tileset.FLOOR;

// 设置墙壁
world[x][y] = Tileset.WALL;

// 设置玩家位置
world[x][y] = Tileset.AVATAR;
```

## 输入指令格式

| 指令 | 说明 |
|------|------|
| `n<seed>s` | 开始新游戏，使用指定种子 |
| `w/a/s/d` | 上下左右移动 |
| `:q` | 保存并退出 |
| `l` | 加载上次保存的游戏 |

## 待完成任务

1. **实现 `World.java`**: 完成世界生成算法（房间、走廊等）
2. **实现 `Main.java`**: 完成游戏主循环
3. **完成 `AutograderBuddy.getWorldFromInput()`**: 处理输入指令
4. **添加交互功能**: 角色移动、碰撞检测等
5. **实现存档功能**: 保存/加载游戏状态

## 依赖

- `edu.princeton.cs.algs4.StdDraw`: 用于图形绘制
- JUnit 5: 用于测试
