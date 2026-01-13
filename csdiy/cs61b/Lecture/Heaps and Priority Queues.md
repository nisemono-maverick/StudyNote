## 优先队列概述

### 基本概念
**优先队列**是一种特殊的数据结构，支持以下操作：
- `add (x)`: 添加元素到队列中
- `getSmallest ()`: 获取最小元素（不移除）
- `removeSmallest ()`: 移除并返回最小元素

与普通队列（FIFO）不同，优先队列根据元素的优先级（通常是最小值）来决定出队顺序。

### 应用场景
1. **任务调度系统**：处理紧急医疗任务
2. **操作系统**：进程调度
3. **网络路由**：数据包优先级处理
4. **图算法**：Dijkstra 最短路径算法、Prim 最小生成树算法
5. **事件驱动模拟**：按时间顺序处理事件

## 不同数据结构实现对比

| 数据结构 | add | getSmallest | removeSmallest | 适用性分析 |
|---------|-----|------------|---------------|-----------|
| **有序数组** | Θ(N) | Θ(1) | Θ(N) | 查询快但插入删除慢 |
| **平衡 BST** | Θ(logN) | Θ(logN) | Θ(logN) | 各方面均衡但无法处理重复元素 |
| **哈希表** | Θ(1) | Θ(N) | Θ(N) | 插入快但查询最小元素慢 |
| **二叉堆** | Θ(logN) | Θ(1) | Θ(logN) | **最优选择**，专为优先队列设计 |

## 二叉堆（Binary Heap）

### 定义与性质

**二叉最小堆**是一个满足以下两个性质的完全二叉树：

1. **完全二叉树性质**：
   - 所有层都完全填满，除了最后一层
   - 最后一层的节点从左到右连续填充

2. **最小堆性质**：
   - 每个节点的值都小于或等于其子节点的值
   - 根节点总是树中的最小值

### 堆的表示方法

#### 方案对比

| 方案 | 描述 | 优缺点 |
|------|------|--------|
| **节点指针** | 每个节点存储值和指向子节点的指针 | 直观但内存开销大 |
| **兄弟节点指针** | 每个节点指向第一个子节点和下一个兄弟节点 | 节省空间但访问复杂 |
| **双数组** | 一个数组存值，一个数组存父节点索引 | 灵活但需要额外存储 |
| **单数组（最优）** | 利用完全二叉树性质在数组中存储 | **内存效率最高，实现简单** |

#### 最优方案：单数组表示
对于完全二叉树，可以用数组高效表示：
- 索引从 1 开始：`keys[1]`为根节点
- 节点`k`的父节点：`k/2`（整数除法）
- 节点`k`的左子节点：`2 k`
- 节点 `k` 的右子节点：`2 k+1`
 ![[Pasted image 20260110113402.png]]

```
索引:    1    2    3    4    5    6    7
        A
       / \
      B   C
     / \ / \
    D  E F  G
```

### 堆的核心操作

#### 1. `getSmallest ()` - O (1)
```java
public Key getSmallest () {
    if (isEmpty ()) throw new IllegalStateException ("Heap is empty");
    return keys[1];  // 直接返回根节点
}
```

#### 2. `add (x)` - O (logN)
**步骤**：
1. 将新元素放在数组末尾（保持完全二叉树性质）
2. 执行"上浮"操作：与父节点比较，如果更小则交换
3. 重复步骤 2 直到满足堆性质

```java
public void add (Key key) {
    // 1. 放在末尾
    keys[++size] = key;
    // 2. 上浮恢复堆性质
    swim (size);
}

private void swim (int k) {
    while (k > 1 && greater (parent (k), k)) {
        swap (k, parent (k));
        k = parent (k);
    }
}
```

#### 3. `removeSmallest ()` - O (logN)
**步骤**：
1. 保存根节点值（最小值）
2. 将最后一个元素移到根节点
3. 执行"下沉"操作：与子节点中较小的比较，如果更大则交换
4. 重复步骤 3 直到满足堆性质

```java
public Key removeSmallest () {
    // 1. 保存最小值
    Key min = keys[1];
    // 2. 将最后一个元素移到根节点
    swap (1, size);
    keys[size--] = null;
    // 3. 下沉恢复堆性质
    sink (1);
    return min;
}

private void sink (int k) {
    while (2 * k <= size) {
        int j = 2 * k;  // 左子节点
        // 选择较小的子节点
        if (j < size && greater (j, j + 1)) j++;
        // 如果当前节点不大于子节点，停止
        if (! greater (k, j)) break;
        swap (k, j);
        k = j;
    }
}
```

### 完整实现示例

```java
/**
 * 二叉最小堆实现
 * @param <Key> 可比较的元素类型
 */
public class BinaryMinHeap<Key extends Comparable<Key>> {
    private Key[] keys;      // 存储堆元素的数组
    private int size;        // 堆中的元素数量
    
    public BinaryMinHeap (int capacity) {
        keys = (Key[]) new Comparable[capacity + 1];  // 索引从 1 开始
        size = 0;
    }
    
    public boolean isEmpty () { return size == 0; }
    public int size () { return size; }
    
    // 辅助方法
    private void swap (int i, int j) {
        Key temp = keys[i];
        keys[i] = keys[j];
        keys[j] = temp;
    }
    
    private boolean greater (int i, int j) {
        return keys[i]. compareTo (keys[j]) > 0;
    }
    
    private int parent (int k) { return k / 2; }
    private int left (int k) { return 2 * k; }
    private int right (int k) { return 2 * k + 1; }
    
    // 堆操作
    public void add (Key key) { /* 如前所述 */ }
    public Key getSmallest () { /* 如前所述 */ }
    public Key removeSmallest () { /* 如前所述 */ }
    
    // 动态调整数组大小
    private void resize (int capacity) {
        Key[] temp = (Key[]) new Comparable[capacity];
        for (int i = 1; i <= size; i++) temp[i] = keys[i];
        keys = temp;
    }
}
```

### 堆的性质验证

#### 完全二叉树验证
数组表示天然保证完全二叉树性质，只需确保在插入时添加到末尾，删除时用末尾元素替换。

#### 最小堆性质验证
可以通过递归方法验证：
```java
public boolean isMinHeap () {
    return isMinHeap (1);
}

private boolean isMinHeap (int k) {
    if (k > size) return true;
    
    int left = left (k);
    int right = right (k);
    
    // 检查当前节点是否小于等于子节点
    if (left <= size && greater (k, left)) return false;
    if (right <= size && greater (k, right)) return false;
    
    // 递归检查子树
    return isMinHeap (left) && isMinHeap (right);
}
```

## 时间复杂度分析

| 操作 | 时间复杂度 | 解释 |
|------|------------|------|
| `getSmallest ()` | O (1) | 直接访问根节点 |
| `add (x)` | O (logN) | 可能需要进行 logN 次上浮操作 |
| `removeSmallest ()` | O (logN) | 可能需要进行 logN 次下沉操作 |
| 构建堆 | O (N) | 通过从最后一个非叶节点开始下沉 |

**构建堆的优化**：
从最后一个非叶节点（索引为 N/2）开始向前遍历，对每个节点执行下沉操作：
```java
public BinaryMinHeap (Key[] array) {
    size = array. length;
    keys = (Key[]) new Comparable[size + 1];
    for (int i = 0; i < size; i++) keys[i + 1] = array[i];
    
    // 构建堆
    for (int k = size / 2; k >= 1; k--) {
        sink (k);
    }
}
```

## 变体与扩展

### 1. 最大堆
将最小堆的比较逻辑反转即可实现最大堆：
```java
private boolean less (int i, int j) {
    return keys[i]. compareTo (keys[j]) < 0;
}
```

### 2. 可调整优先队列
支持改变元素优先级：
```java
public void changePriority (int index, Key newKey) {
    keys[index] = newKey;
    swim (index);  // 可能需要上浮
    sink (index);  // 也可能需要下沉
}
```

### 3. 索引优先队列
为每个元素分配一个外部索引，方便查找和更新。

## 实际应用示例

### 任务调度系统
```java
class Task implements Comparable<Task> {
    int priority;  // 优先级，值越小越紧急
    String name;
    
    public int compareTo (Task other) {
        return Integer.compare (this. priority, other. priority);
    }
}

public class TaskScheduler {
    private MinPQ<Task> taskQueue = new BinaryMinHeap<>();
    
    public void addTask (Task task) {
        taskQueue.add (task);
    }
    
    public Task processNext () {
        return taskQueue.removeSmallest ();
    }
}
```

## 总结

1. **二叉堆是优先队列的高效实现**，在最小/最大元素访问和动态更新间取得平衡
2. **数组表示**充分利用了完全二叉树性质，内存效率高
3. **上浮和下沉操作**保证了堆性质，使所有操作在 O (logN) 时间内完成
4. **实际应用中**，优先队列是许多高效算法（如 Dijkstra、Prim、堆排序）的基础组件

二叉堆的简洁性和高效性使其成为实现优先队列的标准选择，特别适合需要频繁访问和删除最小（或最大）元素的场景。