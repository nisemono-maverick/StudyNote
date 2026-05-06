# BYOW 进度与路线图

> 本页只记录**当前真实进度**和**下一步行动项**，不堆积历史草稿。
> 最后更新：2026-04-14（3A 完成）

---

## 3A World Generation — ✅ 已完成

| 检查项 | 状态 | 备注 |
|--------|------|------|
| `TETile[][]` 非空填充 | ✅ | `fillWithNothing()` + 房间/走廊/WALL |
| 矩形房间生成 | ✅ | 大/正常/小 三类房间 |
| 房间不重叠、不越界 | ✅ | `isValidPosition()` + AABB `overlaps()` |
| L 型转弯走廊 | ✅ | `carveCorridor()` 随机先水平/先垂直 |
| 所有房间连通 | ✅ | Kruskal MST 连接 |
| 墙壁与地板/空白区分 | ✅ | `addWalls()` 8邻域 |
| 无边缘地板 | ✅ | 生成时 `right() >= WIDTH-1` 拒绝 |
| 空间利用率 50%+ | ✅ | 25 房间 + MST 走廊，目测满足 |
| `getWorldFromInput("N####S")` | ✅ | `AutograderBuddy` 已解析大小写 |
| 固定种子确定性输出 | ✅ | `new Random(seed)` |
| `Main` 能渲染世界 | ✅ | 直接 `ter.renderFrame(world)` |

**3A 剩余动作：**
- 无（代码层面已 closed）。由于不是 UCB 学生，无法 Gradescope 验证。

---

## 3B Interactivity — 🚧 未开始

### P0：必须实现（9 分）

- [ ] **主菜单**（N / L / Q），键盘导航
- [ ] **种子输入界面**，实时显示已输入数字，按 S 确认
- [ ] **Avatar WASD 移动**，撞墙不报错
- [ ] **HUD**：鼠标指向 tile 显示 description，**不能闪烁**
- [ ] **`:Q` 保存退出**，`.txt` 文件
- [ ] **L 加载**，恢复地图 + Avatar 位置 + Random 状态
- [ ] **`getWorldFromInput` 扩展**：支持 `"n123swasd:q"` / `"lwasd"`

### 3B 设计思路（预研）

**FSM 状态机方案：**
```
MENU ──N──> SEED_INPUT ──S──> PLAYING
  │                              │
  │<──────────────:Q(保存)───────┤
  │                              │
  └──L──> LOAD ────────────────> PLAYING
  │
  └──Q──> EXIT
```

**保存什么（确保确定性）：**
1. `seed`（long）
2. `randomCallCount`（int）—— Random 已经被 nextXXX 调用了多少次
3. `avatarX`, `avatarY`（int）
4. 或直接保存完整的 `TETile[][]` + 位置（更简单，但丢失 random 状态，3B 够用）

> Spec 要求"相同 seed + 相同按键序列 = 相同结果"。如果保存完整 tile 数组，加载后不再重新生成世界，也满足确定性。但 `getWorldFromInput("lwasd")` 必须能从 save 文件恢复状态。

---

## 3C Ambition — ⏸️ 未规划

### 主要功能候选（21 分必选 1+）

| 功能 | 可行性 | 个人倾向 |
|------|--------|----------|
| 视野系统（Fog of War） | 高 | ⭐ 推荐，代码量小，视觉冲击强 |
| 光源系统 | 中 | 渲染复杂 |
| 追逐实体（A*） | 中 | 算法学过但调试耗时 |
| 遭遇/战斗系统 | 低 | UI 工作量大 |
| 第一人称/3D 视角 | 低 | 改动渲染引擎，风险高 |

### 次要功能候选（7 分）

| 功能 | 可行性 |
|------|--------|
| 不重启新建 | 高 |
| 多存档槽 | 高 |
| 主题切换 | 中 |
| 小地图 | 中 |
| 撤销移动 | 中 |

**当前倾向组合：**
- **主要**：视野系统（只渲染 Avatar 周围圆形区域，其余黑屏，按键开关）
- **次要**：不重启新建 + 多存档槽

---

## 待解决问题 / 风险点

1. **`:q` 保存的 Random 状态** — 需要决定是保存 seed+counter 还是直接保存 tile 数组。
2. **HUD 闪烁** — `TERenderer.renderFrame()` 清屏重绘，HUD 如果也在 StdDraw 里画，需要在每次 renderFrame 后重画。
3. **3B 时间窗口** — DDL 4/22，3A 刚结束，3B+3C 要在 8 天内完成并 demo。

---

## 参考资料链接

- 完整 Spec 摘要：[[Proj3_SPEC]]
- 实现细节参考：[[Project3 Document]]
- 骨架代码说明：[[Skeleton]]
- 官方 FAQ：https://sp24.datastructur.es/projects/proj3/faq
