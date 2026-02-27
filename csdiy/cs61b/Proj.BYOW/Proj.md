> [!DANGER]
> Do NOT change TETile.java’s `character` field or `character()` method as it may lead to bad autograder results. Additionally, if you add new floor or wall tiles, make sure to modify `isBoundaryTile` and `isGroundTile` so that the autograder recognizes your tiles.

## 3A: World Generation
## 1. 房间 + 走廊算法（推荐，最常用）

核心思想：生成多个不重叠的房间，然后用走廊连接它们。
```
步骤：
1. 随机生成 N 个房间（随机位置、大小）
2. 确保房间不重叠，删除或重新放置重叠的房间
3. 用走廊连接相邻的房间（L形或直线）
4. 用墙壁包围地板
```
## 2. 随机游走算法（Drunkard's Walk）

核心思想：从起点开始，随机方向行走，走过的地方变成地板。

## 3. 细胞自动机（洞穴生成）

核心思想：随机初始化，然后应用规则迭代平滑。