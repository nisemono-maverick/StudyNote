# BYOW Implementation Reference

> 本文档与实际代码同步，记录当前已实现的核心逻辑和接口。
> 最后更新：2026-04-14（3A 完成）

---

## 一、项目结构

```
proj3/src/
├── core/
│   ├── Main.java              # 程序入口（3A：直接渲染；3B：需加菜单）
│   ├── World.java             # 世界生成 + 角色位置
│   ├── AutograderBuddy.java   # 输入解析 + autograder 接口
│	└── game/ ← 新包
│		├── GameEngine.java ← 可选，主循环容器
│		├── GameState.java ← 状态接口
│		├── MenuState.java
│		├── SeedInputState.java
│		└── PlayingState.java
├── tileengine/
│   ├── TETile.java            # （禁止修改 character 相关方法）
│   ├── Tileset.java           # 瓦片常量
│   └── TERenderer.java        # 渲染器
└── utils/
    ├── RandomUtils.java
    └── FileUtils.java
```

---

## 二、World 类（当前实现）

### 2.1 配置常量

```java
private static final int WIDTH = 80;
private static final int HEIGHT = 50;
private static final int MAX_ATTEMPTS = 100;
private static final int TARGET_ROOM_COUNT = 25;

// 大房间 1 个
private static final int BIG_ROOM_MIN_W = 20, BIG_ROOM_MAX_W = 25;
private static final int BIG_ROOM_MIN_H = 10, BIG_ROOM_MAX_H = 15;

// 正常房间 ~80%
private static final int NORMAL_ROOM_MIN_W = 5, NORMAL_ROOM_MAX_W = 10;
private static final int NORMAL_ROOM_MIN_H = 3, NORMAL_ROOM_MAX_H = 8;

// 小房间 ~20%
private static final int SMALL_ROOM_MIN_W = 3, SMALL_ROOM_MAX_W = 5;
private static final int SMALL_ROOM_MIN_H = 3, SMALL_ROOM_MAX_H = 5;
```

### 2.2 实例变量

```java
private TETile[][] world;
private List<Room> rooms;
private Random random;
private Position avatarPos;
```

### 2.3 内部类

#### Room
```java
class Room {
    final int x, y, width, height;
    RoomType roomType;

    int centerX() { return x + width / 2; }
    int centerY() { return y + height / 2; }
    int left()   { return x; }
    int right()  { return x + width - 1; }
    int bottom() { return y; }
    int top()    { return y + height - 1; }
}
```

#### RoomType
```java
private enum RoomType { BIG, NORMAL, SMALL }
```

#### Position
```java
private class Position {
    int x, y;
    Position(int x, int y) { this.x = x; this.y = y; }
}
```

---

## 三、世界生成流程

```
World(seed)
    ↓ fillWithNothing()          → 全填 NOTHING
    ↓ initialize()
        ↓ generateRooms()
            ├── tryPlaceBigRoom()        → 必须成功（while true）
            ├── tryPlaceRoom(NORMAL, ~20)
            └── tryPlaceRoom(SMALL, ~5)
        ↓ connectRooms()             → Kruskal MST + L 型走廊
        ↓ addWalls()                 → 8 邻域填 WALL
    ↓ placeAvatar()              → rooms.get(0) 中心放 AVATAR
```

### 3.1 房间生成

```java
private void generateRooms() {
    tryPlaceBigRoom();
    tryPlaceRoom(RoomType.NORMAL, (int) (TARGET_ROOM_COUNT * 0.8));
    tryPlaceRoom(RoomType.SMALL, (int) (TARGET_ROOM_COUNT * 0.2));
}
```

**合法性检查：** 越界检测 + 重叠检测（含 1 格 buffer）

```java
private boolean isValidPosition(Room room) {
    if (room.right() >= WIDTH - 1 || room.top() >= HEIGHT - 1) return false;
    if (overlaps(room)) return false;
    return true;
}

private boolean overlaps(Room room) {
    for (Room other : rooms) {
        if (room.left() <= other.right() + 1 &&
            room.right() >= other.left() - 1 &&
            room.bottom() <= other.top() + 1 &&
            room.top() >= other.bottom() - 1) {
            return true;
        }
    }
    return false;
}
```

### 3.2 走廊生成（Kruskal MST）

```java
private void connectRooms() {
    EdgeWeightedGraph graph = new EdgeWeightedGraph(rooms.size());
    for (int i = 0; i < rooms.size(); i++) {
        for (int j = i + 1; j < rooms.size(); j++) {
            Room v = rooms.get(i);
            Room w = rooms.get(j);
            double dist = Math.abs(v.centerX() - w.centerX())
                        + Math.abs(v.centerY() - w.centerY());
            graph.addEdge(new Edge(i, j, dist));
        }
    }
    KruskalMST mst = new KruskalMST(graph);
    for (Edge edge : mst.edges()) {
        Room v = rooms.get(edge.either());
        Room w = rooms.get(edge.other(edge.either()));
        carveCorridor(v, w);
    }
}
```

**L 型走廊：**
```java
private void carveCorridor(Room v, Room w) {
    int direction = RandomUtils.uniform(random, 2);
    if (direction == 0) {
        carveHorizontal(v.centerX(), w.centerX(), v.centerY());
        carveVertical(v.centerY(), w.centerY(), w.centerX());
    } else {
        carveVertical(v.centerY(), w.centerY(), v.centerX());
        carveHorizontal(v.centerX(), w.centerX(), w.centerY());
    }
}

private void carveHorizontal(int x1, int x2, int y) {
    int start = Math.min(x1, x2);
    int end = Math.max(x1, x2);
    for (int i = start; i <= end; i++) world[i][y] = Tileset.FLOOR;
}

private void carveVertical(int y1, int y2, int x) {
    int start = Math.min(y1, y2);
    int end = Math.max(y1, y2);
    for (int i = start; i <= end; i++) world[x][i] = Tileset.FLOOR;
}
```

### 3.3 墙壁生成

遍历每个 `FLOOR`，8 邻域的 `NOTHING` 变成 `WALL`：

```java
private void addWalls() {
    for (int i = 1; i < WIDTH; i++) {
        for (int j = 1; j < HEIGHT; j++) {
            if (world[i][j] == Tileset.FLOOR) {
                // 8 方向检查
                for (int dx = -1; dx <= 1; dx++) {
                    for (int dy = -1; dy <= 1; dy++) {
                        int nx = i + dx, ny = j + dy;
                        if (nx >= 0 && nx < WIDTH && ny >= 0 && ny < HEIGHT
                            && world[nx][ny] == Tileset.NOTHING) {
                            world[nx][ny] = Tileset.WALL;
                        }
                    }
                }
            }
        }
    }
}
```

### 3.4 Avatar 放置

```java
private void placeAvatar() {
    Room room = rooms.get(0);  // 大房间
    avatarPos = new Position(room.centerX(), room.centerY());
    world[room.centerX()][room.centerY()] = Tileset.AVATAR;
}
```

---

## 四、AutograderBuddy

### 4.1 输入解析

```java
public static TETile[][] getWorldFromInput(String input) {
    int index = 0;
    while (true) {
        if (index == input.length()) return null;
        char c = Character.toLowerCase(input.charAt(index));
        index++;
        if (c == 'n') break;
    }
    StringBuilder sb = new StringBuilder();
    while (true) {
        if (index == input.length()) return null;
        char c = Character.toLowerCase(input.charAt(index));
        index++;
        if (c != 's') sb.append(c);
        else break;
    }
    String s = sb.toString();
    if (s.length() == 0) return null;
    World world = new World(Long.parseLong(s));
    return world.getWorld();
}
```

**约束：**
- 大小写不敏感
- **不调用任何渲染方法**
- `:q` 保存逻辑留到 3B 实现

### 4.2 瓦片判断

```java
public static boolean isGroundTile(TETile t) {
    return t.character() == Tileset.FLOOR.character()
        || t.character() == Tileset.AVATAR.character()
        || t.character() == Tileset.FLOWER.character();
}

public static boolean isBoundaryTile(TETile t) {
    return t.character() == Tileset.WALL.character()
        || t.character() == Tileset.LOCKED_DOOR.character()
        || t.character() == Tileset.UNLOCKED_DOOR.character();
}
```

---


## 五、有限状态机
### 5.1 StateEnum 枚举类
```java
private enum StateEnum { MENU, SEED_INPUT, PLAYING}
```

### 5.2 GameState 接口


## 五、3B 待实现接口

### 5.1 World 中需添加

```java
public void moveAvatar(char direction)   // WASD 移动，撞墙不动
public Position getAvatarPos()           // 获取位置
public void setAvatarPos(Position p)     // 设置位置（加载用）
```

### 5.2 Main 中需添加

- 主菜单（N / L / Q）
- 种子输入界面（实时显示数字）
- 游戏主循环（监听键盘输入）
- HUD（鼠标悬停显示 tile description，不能闪烁）

### 5.3 保存/加载

- `:Q`（冒号+Q）保存并退出
- 只能创建 `.txt` 后缀文件
- `L` 从主菜单加载上次状态
- **关键：** 保存的不仅是地图和位置，还有 `Random` 的状态（seed + 已调用次数），否则无法保证确定性

---

## 六、关键设计决策

| 决策 | 说明 |
|------|------|
| **MST 连走廊** | 保证所有房间连通且无冗余长走廊；用 Kruskal 是因为课程刚教过 |
| **房间 index 映射为图节点** | `rooms.get(i)` 的 `i` 直接作为 `EdgeWeightedGraph` 的顶点，不改现有 Kruskal 代码 |
| **AABB 边界框检测** | `overlaps` 用扩展 1 格的边界矩形，而非逐像素遍历 |
| **8 邻域墙生成** | 走廊和房间统一后处理，不需要单独给走廊/房间分别围墙 |
| **Avatar 放大房间** | `rooms.get(0)` 是 `tryPlaceBigRoom()` 生成的大房间，逻辑上作为起点最合理 |
