# Claude Code 如何管理记忆：深度技术分析

> **来源**：[和Hucci一起写代码](https://wx.zsxq.com/group/48888551284228)
> **作者**：Hucci 写代码
> **日期**：2026 年 04 月 01 日

---

> 对 Claude Code 泄漏出来的 harness 中每一套记忆与上下文管理机制的系统性逆向分析。内容覆盖从轻量级 token 剪枝，到会在你"睡觉时"悄悄整合记忆的 dreaming 系统。

---

## 1. 问题：无限任务世界里的有限上下文

LLM 有一个根本约束：**上下文窗口是固定的**。Claude Code 通常工作在 20 万 token 的窗口内；如果模型名带上 `[1m]` 后缀，则可以扩展到 100 万。一个真实的编码会话很容易就把这个额度吃完：读几个文件、跑几次 grep、来回修改几轮，很快就逼近上限。

Claude Code 解决这个问题的方式，是一个 **7 层记忆架构**。它从亚毫秒级的 token 剪枝，一路延伸到耗时数小时的后台"做梦式"整合。每一层都比前一层更贵，但能力也更强；而整个系统的设计目标，是尽量让更便宜的层先把问题消化掉，避免更昂贵的层被触发。

### Token 计数：一切的基础

所有机制的前提，都是先知道当前已经用了多少 token。核心函数是 `src/utils/tokens.ts` 里的 `tokenCountWithEstimation()`：

> 标准 token 数 = 上一次 API 响应里的 `usage.input_tokens` + 从那之后新增消息的粗略估算

这个"粗略估算"用的是启发式规则：

| 类型 | 估算规则 |
|------|----------|
| 普通文本 | 4 字节 ≈ 1 token |
| JSON | 2 字节 ≈ 1 token（通常分词更密） |
| 图片/文档 | 统一估算为 2000 token |

### 上下文窗口如何确定

系统会按一条优先级链来确定当前到底能用多大的上下文窗口：

```
模型后缀 [1m] → 模型能力查询 → 1M beta header → 环境变量覆盖 → 默认值 200K
```

但"有效窗口"不是全部窗口。Claude Code 会先预留 **20K token** 给压缩输出，因为当你真的快爆窗时，系统还得有空间生成总结来救场。

---

## 2. 架构总览：7 层记忆系统

每一层都有不同的触发条件和不同的成本。系统希望做到：

1. **第 1 层**先挡掉一部分上下文膨胀
2. 不够再由**第 2 层**处理
3. 再不够才逐步升级到更重的机制

原文这里有一张总览图。它想表达的核心不是"7 个模块并列存在"，而是"**7 个由轻到重、逐级兜底的防线**"。

---

## 3. 第 1 层：工具结果存储

| 属性 | 内容 |
|------|------|
| **文件** | `src/utils/toolResultStorage.ts` |
| **成本** | 只有磁盘 I/O，没有 API 调用 |
| **触发时机** | 每次工具返回结果，立即执行 |

### 问题

一次全仓库 grep，可能直接返回 100 KB 以上文本。读取一个大文件，也可能就是几十 KB。它们会立刻吞掉大量上下文，而且通常几分钟后就过时了。

### 解决方案

每一个工具结果，在正式塞进上下文之前，都要先经过预算系统。

如果结果超过阈值，系统会这样处理：

1. 把完整结果写到磁盘：`tool-results/<sessionId>/<toolUseId>.txt`
2. 只把前约 2 KB 的预览内容放进上下文，并包在 `<persisted-output>` 标签里
3. 如果模型之后真的还需要完整内容，再用 `Read` 工具去磁盘读取

### `ContentReplacementState`：让缓存稳定的关键

一个很关键的细节是：某个工具结果一旦被替换成预览，这个决定就会被冻结到 `ContentReplacementState` 中。之后无论再次发多少轮 API 请求，这个结果都必须继续对应同一个预览文本。

这样做的目的，是保证 prompt 前缀在字节级别保持一致，便于命中 prompt cache。

```typescript
ContentReplacementState = {
  seenIds: Set<string>,              // 已处理过、决策被冻结的结果
  replacements: Map<string, string>  // 工具结果 ID -> 预览文本
}
```

而且这个状态会被持久化到 transcript 中，所以即使恢复会话，也能延续同样的替换决策。

### GrowthBook 动态调参

不同工具的阈值还可以通过 `tengu_satin_quoll` 这个 feature flag 远程调整。也就是说，Anthropic 不需要重新发版，就可以在线调节某些工具结果何时持久化。

---

## 4. 第 2 层：微压缩（Microcompaction）

| 属性 | 内容 |
|------|------|
| **文件** | `src/services/compact/microCompact.ts` |
| **成本** | 零或极低 API 成本 |
| **触发时机** | 每一轮对话，在真正调用 API 之前 |

微压缩是最轻的一层缓压机制。它不做摘要，不尝试总结，只做一件事：**清理那些大概率已经没用了的旧工具结果**。

### 三种不同机制

#### a) 基于时间的微压缩

**触发条件**：距离上一次 assistant 消息已经空闲超过某个阈值，默认是 **60 分钟**。

**设计理由**：Anthropic 的服务端 prompt cache 大约只有 1 小时 TTL。你如果超过 1 小时没发请求，缓存本来就过期了，下一次整个 prompt 前缀都得重新 tokenize。既然反正要重写，那就顺手先清掉一些旧工具结果，减少需要重写的内容。

**执行方式**：把旧工具结果的内容替换成 `[Old tool result content cleared]`，但至少保留最近 N 个结果，且保底至少留 1 个。

配置来自 GrowthBook 的 `tengu_slate_heron`：

```typescript
TimeBasedMCConfig = {
  enabled: false,
  gapThresholdMinutes: 60,
  keepRecent: 5
}
```

#### b) 基于缓存编辑 API 的微压缩

这是技术上最巧的一种。

问题在于：如果你直接改本地消息，就会破坏 prompt cache；而 Claude Code 想做的是"删掉旧工具结果，但不打破缓存命中"。

它的做法是利用 API 的 `cache_edits` 机制，**在服务端缓存里删内容，而不是改本地消息**。

**流程如下**：

1. 每个工具结果出现时，都登记进全局 `CachedMCState`
2. 数量超过阈值后，选出最老的一批结果，但会留出一个"保留最近"的缓冲区
3. 生成 `cache_edits` 块，跟下一次 API 请求一起发出去
4. 服务端从缓存前缀里删除指定工具结果
5. 本地消息完全不变，因此本地前缀不被破坏

> ⚠️ **重要安全限制**：它只能在主线程运行。因为如果 fork 出来的子代理也去动同一份全局状态，就会把主线程的缓存编辑逻辑搞乱。

#### c) API 级上下文管理

另一条更"官方"的路径，是用 `context_management` 这个 API 参数，直接让服务端负责上下文清理。

```typescript
ContextEditStrategy =
  | { type: 'clear_tool_uses_20250919',
      trigger: { type: 'input_tokens', value: 180_000 },
      clear_at_least: { type: 'input_tokens', value: 140_000 } }
  | { type: 'clear_thinking_20251015',
      keep: { type: 'thinking_turns', value: 1 } | 'all' }
```

这说明 Anthropic 后来已经在 API 层原生支持部分上下文管理，客户端就不必自己维护那么多清理状态了。

### 哪些工具结果能被清？

✅ **允许清理**：
`FileRead`、`Bash/Shell`、`Grep`、`Glob`、`WebSearch`、`WebFetch`、`FileEdit`、`FileWrite`

❌ **不会被这层动到**：
- thinking block
- assistant 正文
- 用户消息
- MCP 工具结果

---

## 5. 第 3 层：Session Memory

| 属性 | 内容 |
|------|------|
| **文件** | `src/services/SessionMemory/` |
| **成本** | 每次提取需要一次 fork 子代理的 API 调用 |
| **触发时机** | 对话过程中周期性运行，挂在 post-sampling hook 上 |

### 核心思想

与其等到上下文满了，再临时抱佛脚总结全部内容，不如平时就持续记笔记。这样一旦真要压缩，上下文摘要其实早就写好了，根本不需要再额外做一次昂贵总结。

### Session Memory 模板

每个会话都会在 `~/.claude/projects/<slug>/.claude/session-memory/<sessionId>.md` 拥有一个结构化 Markdown：

```markdown
# Session Title
_简短且有辨识度的 5-10 个词标题_

# Current State
_当前正在推进什么工作？_

# Task specification
_用户要求构建什么？_

# Files and Functions
_重要文件，以及它们为什么相关_

# Workflow
_常用 Bash 命令及其含义_

# Errors & Corrections
_遇到过哪些错误，是怎么修好的_

# Codebase and System Documentation
_关键系统组件，以及它们之间如何配合_

# Learnings
_哪些方法有效，哪些无效_

# Key results
_如果用户要求特定产出，这里重复记录_

# Worklog
_逐步记录都尝试过什么、做成了什么_
```

### 触发逻辑

只有同时满足下面两类条件时，session memory 才会更新：

```
自上次提取以来 token 增长 >= minimumTokensBetweenUpdate
并且
(
  自上次提取以来的工具调用数 >= toolCallsBetweenUpdates
  或者
  上一轮 assistant 回复里没有工具调用
)
```

注意，**token 增长阈值是硬条件**，即使工具调用次数到了也不够。

"上一轮没有工具调用"这个分支很有意思，它其实是在捕捉一种自然停顿：模型刚完成一波工作，进入解释或收尾阶段，这时候往往正适合把状态整理进 session memory。

### 提取如何执行

提取动作是通过 `runForkedAgent()` 启动一个 fork 子代理来做的：

- `querySource` 为 `'session_memory'`
- 只允许它对 session memory 文件做 `FileEdit`
- 其他工具全部禁用
- 共享父代理的 prompt cache，以降低成本
- 用 `sequential()` 串行执行，防止多个提取过程互相覆盖

### Session Memory Compaction：真正的收益点

自动压缩触发时，系统会优先尝试 `trySessionMemoryCompaction()`：

1. 先检查 session memory 里是不是已经有实质内容，而不是空模板
2. 如果有，就直接把这份 Markdown 当压缩摘要来用
3. 然后计算应该保留哪些最近消息
4. 返回一个 `CompactionResult`，其中包含"session memory 摘要 + 最近保留的消息"

配置如下：

```typescript
SessionMemoryCompactConfig = {
  minTokens: 10_000,
  minTextBlockMessages: 5,
  maxTokens: 40_000
}
```

这一层最关键的洞察是：**它比完整压缩便宜得多**，因为摘要早就存在，不需要重新调 summarizer，也不需要为"生成摘要"额外支付输入输出 token 成本。

---

## 6. 第 4 层：完整压缩（Full Compaction）

| 属性 | 内容 |
|------|------|
| **文件** | `src/services/compact/compact.ts` |
| **成本** | 一次完整 API 调用，输入是整个对话，输出是摘要 |
| **触发时机** | 超过自动压缩阈值，且 session memory compaction 不可用 |

### 触发条件

逻辑可以概括为：

```
有效上下文窗口 = 上下文窗口 - 20K（预留给输出）
自动压缩阈值 = 有效窗口 - 13K（再留一个缓冲区）

如果 tokenCountWithEstimation(messages) > 自动压缩阈值
就触发压缩
```

### 断路器

如果自动压缩连续失败 **3 次**，这个会话剩余时间里就不再尝试自动压缩。

这个机制不是锦上添花，而是被线上事故逼出来的：原文提到，曾经发现有 1279 个会话各自发生了 50 次以上连续失败，最夸张的一个会话连续失败了 3272 次，估算下来每天白白浪费 25 万次 API 调用。

### 压缩算法

#### 第 1 步：预处理

- 执行用户自定义的 PreCompact hooks
- 去掉消息里的图片，替换成 `[image]`
- 去掉 skill discovery/listing 附件，后面再重新注入

#### 第 2 步：生成摘要

系统会 fork 出一个 summarizer 代理，并要求它按 **9 个部分**生成摘要：

1. Primary Request and Intent
2. Key Technical Concepts
3. Files and Code Sections (with code snippets)
4. Errors and Fixes
5. Problem Solving
6. All User Messages (verbatim — critical for intent tracking)
7. Pending Tasks
8. Current Work
9. Optional Next Step

这个 prompt 还用了一个很聪明的两阶段输出结构：

- 先输出 `<analysis>`：仅供草拟和组织思路
- 再输出 `<summary>`：真正会进入上下文的结构化摘要

最后 `<analysis>` 会被剥掉，不进入后续上下文。这样能提高摘要质量，但不会占用压缩后的 token 配额。

#### 第 3 步：压缩后恢复关键上下文

压缩并不是"一刀切只留摘要"，系统还会把一些关键上下文重新补回来：

| 内容 | 预算 |
|------|------|
| 最近读过的前 5 个文件，每个最多 5K token | 总预算 50K |
| 已调用 skill 的内容，每个最多 5K token | 总预算 25K |
| plan 模式下的计划附件 | - |
| 延迟加载的工具 schema、agent 列表、MCP 指令 | - |
| 重新执行 `SessionStart` hooks，用于恢复 `CLAUDE.md` 等内容 | - |
| 重新追加 session metadata，便于 `--resume` 显示 | - |

#### 第 4 步：插入边界消息

系统会插入一条 `SystemCompactBoundaryMessage`，标记压缩发生的位置：

```typescript
compactMetadata = {
  type: 'auto' | 'manual',
  preCompactTokenCount: number,
  compactedMessageUuid: UUID,
  preCompactDiscoveredTools: string[],
  preservedSegment?: {
    headUuid, anchorUuid, tailUuid
  }
}
```

### 部分压缩

Claude Code 还支持更"外科手术式"的压缩方向：

- **`from`**：只总结某个 pivot 之后的消息，保留更早的前缀不变
- **`up_to`**：只总结某个 pivot 之前的消息，保留后面的最新消息

其中 `from` 比较利于缓存，因为被保留的 prompt 前缀没变；`up_to` 会改变前缀，因此更容易打断缓存。

### 如果连"压缩请求本身"都太长怎么办

如果对话长到连 summarizer 都吃不下，会进入 prompt-too-long 恢复流程：

1. 用 `groupMessagesByApiRound()` 按 API 回合对消息分组
2. 从最老的一组开始删，直到补足 token 缺口
3. 如果缺口无法准确解析，就默认先删掉 **20%** 的最老分组
4. 最多重试 **3 次**
5. 再失败就抛出 `ERROR_MESSAGE_PROMPT_TOO_LONG`

---

## 7. 第 5 层：自动记忆提取（Auto Memory Extraction）

| 属性 | 内容 |
|------|------|
| **文件** | `src/services/extractMemories/extractMemories.ts` |
| **成本** | 一次 fork 子代理 API 调用 |
| **触发时机** | 每个完整 query loop 结束时，也就是模型给出最终回复且本轮没有再发工具调用时 |

### 用途

Session Memory 记录的是"当前这次会话"的状态，而 Auto Memory Extraction 要做的是把真正**跨会话、可长期复用**的知识沉淀下来，保存到：

```
~/.claude/projects/<path>/memory/
```

### 记忆类型

原文这里有一张图，说明系统会把长期记忆分成 4 类，每类有各自的保存标准。复制版没保留下图，但从后文语境可以明确看出：它不是"所有重要内容都存"，而是严格筛选"**跨会话且难以从代码重新推导出来**"的信息。

### 记忆文件格式

```yaml
---
name: testing-approach
description: User prefers integration tests over mocks after a prod incident
type: feedback
---

Integration tests must hit a real database, not mocks.

**Why:** Prior incident where mock/prod divergence masked a broken migration.

**How to apply:** When writing tests for database code, always use the test database helper.
```

### 明确不要保存什么

提取 prompt 里明确排除了这些内容：

- ❌ 代码模式、编码规范、架构设计（能从代码本身推导）
- ❌ Git 历史（应该通过 `git log` / `git blame` 获取）
- ❌ 调试过程中的修复细节（fix 已经写进代码里了）
- ❌ `CLAUDE.md` 里的内容
- ❌ 临时性的任务细节

### 与主代理互斥

如果主代理在当前轮里已经写过 memory 文件，那么后台提取会直接跳过，避免重复工作。

```typescript
function hasMemoryWritesSince(messages, sinceUuid): boolean {
  // 扫描 Edit/Write tool_use 是否写到了 auto-memory 路径
  // 如果主代理已经写过，就不再后台重复提取
}
```

### 执行策略

提取代理的 prompt 会特别强调 turn 预算，要它高效工作：

- **第 1 回合**：把可能需要更新的文件全部并行 `FileRead`
- **第 2 回合**：把需要的 `FileWrite` / `FileEdit` 全部并行发出
- 不要跨很多轮来回读写

### `MEMORY.md`：索引，而不是记忆内容本身

`MEMORY.md` 本质上是**索引文件**，而不是总记忆仓库。每一项应该是一行，长度最好控制在 **150 个字符**以内，比如：

- `[Testing Approach](feedback_testing.md) — 只接受真实数据库集成测试，避免 mock`
- `[User Profile](user_role.md) — 资深 Go 工程师，刚接触 React，关注可观测性`

**硬限制**：
- 最多 **200 行**
- 或最多 **25 KB**

哪个先到就以哪个为准。超过 200 行时，系统加载进 prompt 时会截断后面的条目。

---

## 8. 第 6 层：Dreaming

| 属性 | 内容 |
|------|------|
| **文件** | `src/services/autoDream/autoDream.ts` |
| **成本** | 一次 fork 子代理 API 调用，且可能是多轮的 |
| **触发时机** | 后台运行，在积累了足够时间和足够多会话之后才会触发 |

### 核心概念

Dreaming 可以理解成"**跨会话记忆整合**"。它会在后台回顾过去的 session transcript，整理并改进 memory 目录。

这个命名其实非常贴切：就像生物在睡眠中会整理白天经验一样，Claude Code 也会在后台把零散经验重新组织进长期记忆。

### Gate 设计：先做最便宜的检查

Dream 系统采用**级联 gate**。每个检查都比下一个更便宜，所以绝大多数轮次都会在很前面就退出，不会真的走到昂贵整合。

原文这里那张图强调的是"**分层 gate 而不是一上来就扫 transcript**"。这说明 Dreaming 不是高频重活，而是一个经过严格节流的后台维护任务。

### 锁文件机制

锁文件位于 `<memoryDir>/.consolidate-lock`，它一物两用：

| 属性 | 用途 |
|------|------|
| **路径** | `<autoMemPath>/.consolidate-lock` |
| **内容** | 进程 PID |
| **mtime** | 上次 consolidation 的时间戳 |

也就是说，这个文件**既是互斥锁，又是"上次成功整合时间"的存储介质**。

**行为如下**：

- **获取锁**：写入 PID，并把 `mtime` 设为当前时间；随后回读核验 PID，避免竞争条件
- **成功结束**：保留现在的 `mtime`，它就代表最新 consolidation 时间
- **失败回滚**：`rollbackConsolidationLock(priorMtime)` 用 `utimes()` 把时间戳拨回去
- **锁过期**：如果 `mtime` 超过 **60 分钟**，且 PID 对应进程已不存在，就可以回收
- **崩溃恢复**：如果检测到死掉的 PID，下一次进程可以接管

### 四阶段整合流程

Dream 代理拿到的是一个很结构化的四阶段任务：

#### Phase 1：Orient

- `ls` memory 目录
- 读取 `MEMORY.md` 了解当前索引
- 快速浏览已有主题文件，避免创建重复记忆

#### Phase 2：Gather Recent Signal

- 查看日常日志，如 `logs/YYYY/MM/YYYY-MM-DD.md`
- 检查哪些记忆已经与当前代码库漂移或矛盾
- 只对特定关键词做窄范围 transcript 检索，例如：

```bash
grep -rn "<narrow term>" transcripts/ --include="*.jsonl" | tail -50
```

> ⚠️ 系统特别强调：**不要穷举式读 transcript**。只查那些你已经怀疑重要的线索。

#### Phase 3：Consolidate

- 新建或更新 memory 文件
- 尽量把新信息合并进已有主题，而不是制造近似重复文件
- 把相对日期转成绝对日期，比如把 "yesterday" 改成 "2026-03-30"
- 直接删除那些已经被证伪的旧信息

#### Phase 4：Prune and Index

- 更新 `MEMORY.md`，确保不超过 200 行 / 25 KB
- 删除指向过时、错误、已被替代记忆的索引
- 缩短啰嗦索引项，把细节放回主题文件
- 解决文件之间的互相矛盾

### 工具限制

Dream 代理权限很严：

- Bash 只能用只读命令：`ls`、`find`、`grep`、`cat`、`stat`、`wc`、`head`、`tail`
- `Edit/Write` 只能写 memory 目录
- 禁用 MCP 工具、禁用 Agent 工具、禁用破坏性操作

### UI 呈现

Dream 作为后台任务会出现在 footer 的状态胶囊里，并有一个两阶段状态机：

- `DreamPhase`: `starting` → `updating`
- `Status`: `running` → `completed | failed | killed`

如果用户主动杀掉 dream，系统会把锁文件的 `mtime` 回滚，这样后续 session 还能重试。

### 进度追踪

Dream 代理的每一轮 assistant 输出都会被监控：

- 文本块会被抓出来用于 UI 展示
- `tool_use` 数量会被统计
- `Edit/Write` 的文件路径会收集起来，用于结束时摘要
- 实时显示最多只保留最近 **30 轮**

---

## 9. 第 7 层：跨代理通信

| 属性 | 内容 |
|------|------|
| **文件** | `src/utils/forkedAgent.ts`、`src/tools/AgentTool/`、`src/tools/SendMessageTool/` |
| **成本** | 依具体通信模式而定 |
| **触发时机** | 派生代理、后台任务、队友协作时 |

### Forked Agent 模式

Claude Code 几乎所有后台操作都依赖 forked agent 模式，包括：

- session memory
- auto memory extraction
- dreaming
- compaction
- agent summary

这是它的基础参数结构：

```typescript
CacheSafeParams = {
  systemPrompt: SystemPrompt,
  userContext: { [k: string]: string },
  systemContext: { [k: string]: string },
  toolUseContext: ToolUseContext,
  forkContextMessages: Message[],
}
```

fork 出来的子代理会拿到一个"隔离上下文"，其中可变状态是克隆出来的：

| 状态 | 处理方式 |
|------|----------|
| `readFileState` | 克隆的 LRU cache，避免彼此污染 |
| `abortController` | 子控制器，但会挂在父控制器之下 |
| `denialTracking` | 全新状态 |
| `ContentReplacementState` | 克隆，确保工具预览替换决策延续 |

但与此同时，它们又**共享 prompt cache**，因为所有缓存敏感参数都保持一致。也就是说，从 API 视角看，它们共用相同前缀，因此能吃到缓存命中。

### Agent Tool：如何派生子代理

原文这里的图是在展示 Agent tool 支持多种派生模式。虽然图丢了，但从后文可以明确看出核心点有两个：

- 子代理之间需要尽量共享相同 prompt 前缀，降低成本
- 同时又必须阻止递归生成无限子代理

所以系统设计了 **fork 反递归机制**：子代理虽然工具池里仍保留 `Agent` 工具定义，但会检测历史消息中的 `<fork_boilerplate_tag>`，一旦发现自己已经是 fork 出来的，就拒绝继续递归 fork。

为了最大化缓存共享，所有 fork 子代理的 API 请求前缀都会尽可能做成字节一致：

1. 先放完整的父 assistant 消息，包括 tool_use、thinking、text
2. 再放一条 user 消息，其中包含：
   - 每个 tool_use 对应的相同占位结果
   - 只在最后一小段放"这个子代理专属的指令文本"

这样并发 fork 多个子代理时，绝大多数前缀都是相同的，缓存复用率就极高。

### `SendMessage`：代理之间如何通信

运行中的代理可以通过 `SendMessage` 工具互相发消息：

```typescript
SendMessage({
  to: 'research-agent',
  message: 'Check Section 5',
  summary: 'Requesting section review'
})
```

它支持的目标不止单个代理，也可以是广播、UDS 或 bridge。

**路由逻辑大致是**：

1. 如果目标是当前进程内的子代理，就走 `queuePendingMessage()`，在下一个工具回合边界统一投递
2. 如果目标是 ambient team 中的进程级代理，就写入文件邮箱
3. 如果是跨 session，就通过 bridge / UDS 发送

系统还定义了结构化生命周期消息，比如：

- `shutdown_request` / `shutdown_response`
- `plan_approval_response`

### Agent Memory：跨调用持久状态

原文这里有一张图，说明 agent memory 支持 3 个作用域。图丢失后，能可靠恢复的核心意思是：代理不只是"当前一轮活着"，它们还可以在不同范围内保留状态，以支撑多次调用间的连续性。

### Agent Summary：定期生成进度快照

如果子代理处于 coordinator 模式，系统会每 **30 秒** fork 一次对话，生成一个 **3 到 5 个词**的进度摘要：

| ✅ 好例子 | ❌ 坏例子 |
|----------|----------|
| `Reading runAgent.ts` | `Investigating the issue` |
| `Fixing null check in validate.ts` | `Analyzed the branch diff` |

注意它要求"**具体、正在进行中、足够短**"。

这项任务使用 **Haiku** 这种便宜模型，并且完全禁用工具，因为它只是纯文本摘要任务。

---

## 10. QueryLoop：这些机制如何串起来

```
1. 新一轮请求开始前，先估算 token
       ↓
2. 先尝试最便宜的上下文管理，如工具结果持久化、微压缩
       ↓
3. 对话过程中周期性写 session memory
       ↓
4. 如果快爆窗，优先尝试 session memory compaction
       ↓
5. 不行再做 full compaction
       ↓
6. 一轮完整工作结束后，抽取跨会话 memory
       ↓
7. 后台空闲时，再由 dreaming 做更慢、更全局的整合
```

这说明 Claude Code 不是靠某一个"神奇压缩器"工作，而是把上下文治理拆进 queryloop 的多个时间点。

---

## 11. Prompt Cache 优化

Claude Code 架构里最精致的一部分之一，就是它对 prompt cache 的执念。几乎每一个设计决策都会考虑缓存命中率。

> **缓存不是附带优化，而是核心设计约束。**

### 问题

Anthropic 的 API 会在服务端缓存 prompt 前缀，大约 **1 小时 TTL**。命中缓存时，你只需为新增 token 付费；不命中时，就要把整段 prompt 全部重新 tokenize。

在 200 K token 量级下，这个差距是巨大的：原文给出的数量级是，从每次请求约 `$0.003` 到 `$0.60` 的差别。

### 保缓存的设计模式

| 模式 | 说明 |
|------|------|
| `CacheSafeParams` | 每个 fork 子代理都继承父代理完全一致的 system prompt、tools 和消息前缀，因此能直接命中缓存 |
| `renderedSystemPrompt` | 直接沿用父代理已经渲染好的 system prompt 字节串，避免因为重新渲染时 flag 变化而造成字节差异 |
| `ContentReplacementState` 克隆 | 工具结果一旦决定用哪个 preview，就固定下来，保证每次 API 调用看到的是同一份前缀 |
| Cached microcompact | 在服务端 cache 做编辑，不改本地前缀，因此能清理内容但不打破缓存 |
| Fork message construction | 所有 fork 子代理共享尽可能长的相同前缀，只有最后的指令块不同 |
| 压缩后的缓存断裂通知 | 压缩完成后，`notifyCompaction()` 会重置缓存基线，这样压缩后的预期 cache miss 不会被误报成异常 |

### Cache Break 检测

系统还会主动监控意外缓存失效，相关逻辑在 `promptCacheBreakDetection.ts`。像 compaction、microcompact 这种"已知必然会打断缓存"的操作，会提前登记，避免误报。

---

## 12. 关键数字

原文这一节基本都是图表，复制后只剩链接，表格内容已经丢失。结合全文，至少可以可靠恢复出这些"数字层面的设计倾向"：

### Context 阈值

| 参数 | 数值 |
|------|------|
| 默认上下文窗口 | 200 K |
| 扩展窗口 | 1 M（特定模型后缀 / 条件下） |
| 压缩输出预留 | 20 K |
| 自动压缩缓冲 | 13 K |

### Tool Result Budget

| 参数 | 数值 |
|------|------|
| 过大的工具结果 | 会被落盘 |
| prompt 内通常只保留 | 约 2 KB 预览 |
| 不同工具阈值 | 可被 feature flag 远程调整 |

### Session Memory

| 参数 | 数值 |
|------|------|
| 更新条件 | token 增长与回合条件同时满足 |
| 压缩时至少保留 | 10,000 token |
| 至少保留 | 5 条含文本消息 |
| 保留区硬上限 | 40,000 token |

### Full Compaction

| 参数 | 数值 |
|------|------|
| 连续失败后熔断 | 3 次 |
| prompt-too-long 恢复最多重试 | 3 次 |

### Dreaming

| 参数 | 数值 |
|------|------|
| 锁过期判断 | 约 60 分钟 |
| UI 实时显示最多保留 | 最近 30 轮 |

### Microcompact

| 参数 | 数值 |
|------|------|
| 空闲阈值默认 | 60 分钟 |
| 默认保留最近 | 5 个工具结果 |

> 也就是说，原文这组图表想传达的不是"记住每个数值本身"，而是 Claude Code 对上下文治理做了非常明确的**预算化与阈值化设计**。

---

## 13. 设计原则

### 1. 分层防御，便宜优先

每一层的目的，都是尽量阻止下一层触发：

```
工具结果存储 → 减少微压缩要清掉的内容
       ↓
微压缩 → 减少 session memory compaction 的需要
       ↓
session memory compaction → 减少 full compaction 的需要
       ↓
full compaction → 避免真正的上下文溢出
```

### 2. 极端重视 Prompt Cache

几乎所有设计都在为缓存让路：冻结的 `ContentReplacementState`、预渲染 system prompt、`cache_edits`、字节级一致的 fork 消息结构，本质上都服务于"**让缓存前缀尽可能不变**"。

### 3. 隔离中共享

fork 子代理拿到的是克隆出来的可变状态，避免互相污染；但又共享缓存前缀，避免成本爆炸。这是一个非常精细的平衡：

- 隔离太少，会引发状态污染和 bug
- 隔离太多，会浪费缓存，成本暴涨

### 4. 到处都是断路器

| 机制 | 断路器 |
|------|--------|
| 自动压缩 | 3 次失败熔断 |
| dream 扫描 | 10 分钟节流 |
| dream 锁 | 基于 PID 的互斥锁 + 过期检测 |
| session memory | 顺序执行包装 |
| memory extraction | 与主代理写入互斥 |

### 5. 优雅降级

每个系统失败时，通常不会把整条链路打崩，而是安静退出，让下一层接手：

- session memory compaction 失败，返回 `null`，由 full compaction 接管
- dream 锁获取失败，下个 session 再试
- extract memories 失败，只记日志，不抛硬错误

### 6. 用 Feature Flag 当保险丝

几乎所有子系统都挂在 GrowthBook feature flag 后面：

| Feature Flag | 功能 |
|--------------|------|
| `tengu_session_memory` | session memory |
| `tengu_sm_compact` | session memory compaction |
| `tengu_onyx_plover` | dreaming |
| `tengu_passport_quail` | auto memory extraction |
| `tengu_slate_heron` | time-based microcompact |
| `CACHED_MICROCOMPACT` | 基于缓存编辑的微压缩 |
| `CONTEXT_COLLAPSE` | context collapse |
| `HISTORY_SNIP` | 消息裁剪 |

这样一旦某个机制线上出问题，可以不发版直接回滚。

### 7. 必要处显式互斥

系统里有几组明确互斥关系：

- `Context Collapse` 与 `Autocompact` 互斥
- 主代理 memory 写入与后台 extraction 互斥
- session memory compaction 与 full compaction 互斥
- autocompact 与某些 subagent query source 互斥，用于避免死锁

---

## 总结

如果把这篇分析压成一句话，那就是：

> **Claude Code 不是"有一个压缩上下文的功能"，而是把上下文管理做成了一整套分层、预算化、缓存友好、具备后台维护能力的操作系统式设计。**

它真正厉害的地方，不只是"会做摘要"，而是：

- 知道哪些信息该尽快移出 prompt
- 知道哪些信息要先变成 session 级笔记
- 知道哪些信息值得升级为跨会话长期记忆
- 知道什么时候该后台整合，而不是前台打断当前工作
- 更知道如何在这一切之上，尽量不打爆 prompt cache

从工程角度看，这篇文章揭示出的不是一个单点技巧，而是一种很成熟的系统设计观：

- **昂贵能力必须后置**
- **每一层都要有预算**
- **每一层都要考虑失败时怎么降级**
- **每一层都要考虑和缓存、并发、恢复机制的关系**

这也是为什么 Claude Code 的"上下文管理"看起来不像一个 feature，而更像一个小型 runtime。
