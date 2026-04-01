# World 类开发指南  
  
## 一、世界配置常量  
  
```java  
public class World {  
    // ========== 世界尺寸 ==========    
    private static final int WIDTH = 80;    
    private static final int HEIGHT = 50;    
    // ========== 房间配置 ==========    
    private static final int MAX_ATTEMPTS = 100;      // 最大尝试次数  
    private static final int TARGET_ROOM_COUNT = 25;  // 目标房间数  
    // 大房间（1个，Boss房/起始房）  
    private static final int BIG_ROOM_MIN_W = 20;    
    private static final int BIG_ROOM_MAX_W = 25;    
    private static final int BIG_ROOM_MIN_H = 10;    
    private static final int BIG_ROOM_MAX_H = 15;    
    // 正常房间（约80%，主体探索区域）  
    private static final int NORMAL_ROOM_MIN_W = 5;    
    private static final int NORMAL_ROOM_MAX_W = 10;    
    private static final int NORMAL_ROOM_MIN_H = 3;    
    private static final int NORMAL_ROOM_MAX_H = 8;    
    // 小房间（约20%，隐藏奖励房）  
    private static final int SMALL_ROOM_MIN_W = 3;    
    private static final int SMALL_ROOM_MAX_W = 5;    
    private static final int SMALL_ROOM_MIN_H = 3;    
    private static final int SMALL_ROOM_MAX_H = 5;    
    // ========== 实例变量 ==========    
    private TETile[][] world;    
    private List<Room> rooms;    
    private Random random;    
    private Position avatarPos;}  
```  
  
## 二、内部类 

### 2.1 Room 类
用于记录房间的坐标，大小

| 属性            | 说明       |
| ------------- | -------- |
| `x: int`      | 记录左下角横坐标 |
| `y: int`      | 记录左下角纵坐标 |
| `width: int`  | 记录宽度     |
| `height: int` | 记录高度     |

| 构造方法                                        | 说明         | 复杂度   |
| ------------------------------------------- | ---------- | ----- |
| `Room(int x, int y, int width, int height)` | 根据属性生成房间   | O (?) |

| 方法               | 说明       | 复杂度   |
| ---------------- | -------- | ----- |
| `centerX(): int` | 返回中心的横坐标 | O (?) |
| `centerY(): int` | 返回中心的纵坐标 | O (?) |
| `top(): int`     | 返回上边界    |       |
| `bottom(): int`  | 返回下边界    |       |
| `left(): int`    | 返回左边界    |       |
| `right(): int`   | 返回右边界    |       |

### 2.2 RoomType 类
`private enum RoomType { BIG, NORMAL, SMALL }`

### 2.3 Position 类
- [ ] 待完成

## 三、核心方法清单  
  
### 3.1 构造与初始化  
  
| 方法                  | 功能                         | 复杂度    |
| ------------------- | -------------------------- | ------ |
| `World(long seed)`  | 初始化随机种子，分配数组，开始生成          | O(W×H) |
| `initialize()`      | 主流程：填充空白→生成房间→连接走廊→加墙壁→放玩家 | O(N²)  |
| `fillWithNothing()` | 将全部格子设为 Tileset.NOTHING    | O(W×H) |
  
### 3.2 房间生成  
  
| 方法                                        | 功能            | 关键逻辑        |     |
| ----------------------------------------- | ------------- | ----------- | --- |
| `generateRooms()`                         | 按优先级生成三类房间    | 大→正常→小      |     |
| `tryPlaceBigRoom()`                       | 尝试放置1个大房间     | 单独处理，失败也继续  |     |
| `tryPlaceRooms(int count, RoomType type)` | 批量尝试放置房间      | 重叠则重试，计尝试次数 |     |
| `createRandomRoom(RoomType type)`         | 根据类型生成随机尺寸房间  | 随机位置+尺寸，留边距 |     |
| `isValidPosition(Room r)`                 | 检查房间是否合法      | 不靠边 + 不重叠   |     |
| `overlaps(Room r)`                        | 检查与现有房间是否重叠   | 扩展1格间隙（给墙壁） |     |
| `carveRoom(Room r)`                       | 将房间区域设为 FLOOR | 双重循环填充      |     |
  
### 3.3 走廊生成  
  
| 方法                                       | 功能          | 策略           |     |
| ---------------------------------------- | ----------- | ------------ | --- |
| `connectRooms()`                         | 连接所有房间      | 顺序连接，i 连 i+1 |     |
| `carveCorridor(Room a, Room b)`          | 在两个房间中心间挖走廊 | L形，随机方向      |     |
| `carveHorizontal(int x1, int x2, int y)` | 水平挖走廊       | 包含两端点        |     |
| `carveVertical(int y1, int y2, int x)`   | 垂直挖走廊       | 包含两端点        |     |
  
**走廊方向策略**：  
如果随机选择"先水平后垂直":  
    从 (x1,y1) 水平挖到 (x2,y1)    然后从 (x2,y1) 垂直挖到 (x2,y2)  
如果随机选择"先垂直后水平":  
    从 (x1,y1) 垂直挖到 (x1,y2)    然后从 (x1,y2) 水平挖到 (x2,y2)

### 3.4 墙壁与玩家  
  
| 方法 | 功能 | 策略 |  
|------|------|------|  
| `addWalls()` | 在地板周围添加墙壁 | 检查8邻域 |  
| `placeAvatar()` | 放置玩家角色 | 放在第一个房间中心 |  
| `isFloor(int x, int y)` | 判断是否为地板 | 边界检查 + tile判断 |  
  
### 3.5 公开接口  
  
| 方法 | 功能 |  
|------|------|  
| `TETile[][] getTiles()` | 获取世界状态（用于渲染） |  
| `void moveAvatar(char direction)` | 移动玩家（wasd） |  
| `Position getAvatarPos()` | 获取玩家位置（用于存档） |  
| `void setAvatarPos(Position p)` | 设置玩家位置（用于读档） |  
  
## 四、生成流程图  
  
```  
World(seed)  
    ↓initialize()  
    ↓fillWithNothing() ─────────→ 全部是 NOTHING    ↓generateRooms()  
    ├── tryPlaceBigRoom() ──→ 1个大房间（非必须成功）  
    ├── tryPlaceRooms(80%, NORMAL)    │       └── 最多尝试100次，每次：  
    │           创建随机正常房间  
    │           检查合法性（不靠边、不重叠）  
    │           合法则雕刻，不合法则重试  
    └── tryPlaceRooms(20%, SMALL)    ↓connectRooms()  
    └── 对每对相邻房间 (i, i+1)：  
        计算中心点        随机选择L形方向  
        carveHorizontal + carveVertical    ↓addWalls()  
    └── 遍历每个FLOOR的8邻域：  
        如果是NOTHING则变成WALL  
    ↓placeAvatar()  
    └── 在rooms.get(0)的中心放置AVATAR  
```  
  
## 五、关键算法细节  
  
### 5.1 重叠检测（含1格间隙）  
  
```java  
// 两个房间之间至少留1格间隙（给墙壁）  
private boolean overlaps(Room r) {  
    for (Room other : rooms) {        // 扩展1格后的边界检查  
        if (r.left() - 1 <= other.right() + 1 &&            r.right() + 1 >= other.left() - 1 &&            r.bottom() - 1 <= other.top() + 1 &&            r.top() + 1 >= other.bottom() - 1) {            return true;        }    }    return false;}  
```  
  
### 5.2 墙壁生成（8邻域）  
  
```java  
private void addWalls() {  
    for (int x = 1; x < WIDTH - 1; x++) {        for (int y = 1; y < HEIGHT - 1; y++) {            if (tiles[x][y] == Tileset.FLOOR) {                // 检查8个方向  
                for (int dx = -1; dx <= 1; dx++) {                    for (int dy = -1; dy <= 1; dy++) {                        int nx = x + dx, ny = y + dy;                        if (tiles[nx][ny] == Tileset.NOTHING) {                            tiles[nx][ny] = Tileset.WALL;                        }                    }                }            }        }    }}  
```  
  
### 5.3 玩家移动  
  
```java  
public void moveAvatar(char direction) {  
    int nx = avatarPos.x;    int ny = avatarPos.y;        switch (direction) {  
        case 'w': ny++; break;        case 's': ny--; break;        case 'a': nx--; break;        case 'd': nx++; break;        default: return;    }    // 只能移动到FLOOR上  
    if (tiles[nx][ny] == Tileset.FLOOR) {        tiles[avatarPos.x][avatarPos.y] = Tileset.FLOOR;        avatarPos.x = nx;        avatarPos.y = ny;        tiles[nx][ny] = Tileset.AVATAR;    }}  
```  
  
## 六、测试检查点  
  
### 阶段1：基础测试  
- [ ] 固定种子生成相同世界  
- [ ] 不同种子生成不同世界  
- [ ] 世界四周被墙壁包围  
  
### 阶段2：房间测试  
- [ ] 至少生成1个房间  
- [ ] 房间之间有走廊连接  
- [ ] 可以走到每个房间  
  
### 阶段3：移动测试  
- [ ] wasd可以移动玩家  
- [ ] 不能穿墙  
- [ ] 移动后原位置恢复为地板  
  
### 阶段4：保存测试  
- [ ] 可以保存世界状态  
- [ ] 可以加载世界状态  
- [ ] 加载后玩家位置正确  
  
## 七、常见问题  
  
**Q: 房间生成数量不够 TARGET_ROOM_COUNT 怎么办？**  
A: 没关系，地图空间可能不够。只要有房间且能连通即可。  
  
**Q: 走廊穿墙怎么办？**  
A: 走廊只覆盖 NOTHING，不覆盖已有的 WALL 或 FLOOR。  
  
**Q: 玩家被墙包围出不去？**  
A: 确保玩家生成在房间中心（FLOOR），且房间有出口连接到走廊。  
  
**Q: 世界生成太慢？**  
A: 检查重叠检测算法，确保没有 O(N²) 以上的复杂度。