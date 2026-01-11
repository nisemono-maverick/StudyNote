## 1. 问题的引出：为什么需要哈希表

### 1.1 Search Tree 的限制
- Search Tree (如 BST、红黑树) 要求元素必须可比（实现 Comparable 接口）
- 时间复杂度为 O (logN) 量级
- 对于不可比较的元素，Search Tree 无法直接使用

### 1.2 哈希表的基本思想
**核心思路**：分而治之，通过哈希函数将元素分配到不同的区域（桶）

**工作流程**：
1. 每个元素通过哈希函数计算得到一个哈希值
2. 将哈希值映射到特定的桶（区域）
3. 每个桶内部使用链表等结构存储元素

**优势**：
- 不要求元素可比
- 理想情况下可达 O (1) 时间复杂度

## 2. 哈希表原理详解

### 2.1 时间复杂度分析

假设：
- N：元素总数
- M：桶的数量（区域数）

**理想情况**：
- 每个桶平均有 N/M 个元素
- 查找时间复杂度：O (N/M)

**挑战**：
- 若 M 固定，时间复杂度为 O (N/M)，但 M 是常数
- 若 M 太小，退化为 O (N)
- 若 M 太大，浪费空间

### 2.2 动态扩容策略

**目标**：保持 N/M ≤ k（k 为常数）

**扩容机制**：
1. 当负载因子（N/M）超过阈值时触发扩容
2. 通常以 2 倍（或其他因子）增加桶的数量
3. 重新哈希所有元素到新的桶中

**优势**：
- 保持平均时间复杂度为 O (1)
- 动态适应数据规模

## 3. 哈希函数的设计

### 3.1 哈希函数的要求
1. **一致性**：相同对象必须产生相同哈希值
2. **高效性**：计算速度快
3. **均匀性**：元素应均匀分布到各个桶中

### 3.2 不同数据类型的哈希计算
- **整数**：`hash = value % M`
- **字符串**：使用多项式哈希等算法
- **对象**：组合各字段的哈希值

### 3.3 Java 中的 hashCode 方法
```java
// 默认实现：基于内存地址
public native int hashCode();

// 正确实现示例
@Override
public int hashCode() {
    // 使用对象的属性计算哈希值
    return Objects.hash(field1, field2, ...);
}
```

**注意事项**：
- 重写 `hashCode()` 时通常需要同时重写 `equals()`
- 哈希值应保持稳定（键对象不可变）
- 不同对象可能产生相同哈希值（哈希冲突）

## 4. HashMap 实现详解

### 4.1 核心数据结构

```java
public class MyHashMap<K, V> implements Map61B<K, V> {
    // 桶数组：每个桶是一个 Collection<Node>
    private Collection<Node>[] buckets;
    
    // 关键参数
    int size = 0;           // 元素数量
    int capacity;           // 桶的数量
    double loadFactor;      // 负载因子阈值
    
    // 默认值
    static final int DEFAULT_CAPACITY = 16;
    static final double DEFAULT_LOAD_FACTOR = 0.75;
}
```

### 4.2 内部节点类
```java
protected class Node {
    K key;
    V value;
    
    Node(K k, V v) {
        key = k;
        value = v;
    }
    
    @Override
    public int hashCode() {
        return key.hashCode();  // 使用键的哈希值
    }
}
```

### 4.3 关键操作实现

#### 4.3.1 put 操作
```java
@Override
public void put(K key, V value) {
    // 1. 计算桶索引
    int index = Math.floorMod(key.hashCode(), capacity);
    Collection<Node> bucket = buckets[index];
    
    // 2. 检查是否已存在该键
    for (Node node: bucket) {
        if (node.key.equals(key)) {
            node.value = value;  // 更新值
            return;
        }
    }
    
    // 3. 插入新节点
    bucket.add(new Node(key, value));
    size++;
    
    // 4. 检查是否需要扩容
    if ((double) size / capacity >= loadFactor) {
        resize();
    }
}
```

#### 4.3.2 动态扩容
```java
private void resize() {
    // 1. 扩容为原来的2倍
    this.capacity *= 2;
    Collection<Node>[] newBuckets = new Collection[this.capacity];
    
    // 2. 初始化新桶
    for (int i = 0; i < newBuckets.length; i++) {
        newBuckets[i] = createBucket();
    }
    
    // 3. 重新哈希所有元素
    for (int i = 0; i < buckets.length; i++) {
        for (Node node: buckets[i]) {
            // 关键：使用新的容量重新计算索引
            int index = Math.floorMod(node.key.hashCode(), capacity);
            newBuckets[index].add(node);
        }
    }
    
    // 4. 替换桶数组
    this.buckets = newBuckets;
}
```

**扩容规律**：
- 当容量变为原来的 2 倍时
- 元素的桶位置要么不变，要么变为 `原位置 + 原容量`
- 这是因为 `hash % (2*capacity) = hash % capacity` 或 `hash % capacity + capacity`

#### 4.3.3 get 操作
```java
@Override
public V get(K key) {
    Node node = getNode(key);
    return node != null ? node.value : null;
}

private Node getNode(K key) {
    if (key == null) return null;
    int index = Math.floorMod(key.hashCode(), capacity);
    Collection<Node> bucket = buckets[index];
    
    for (Node node: bucket) {
        if (node.key.equals(key)) {
            return node;
        }
    }
    return null;
}
```

#### 4.3.4 remove 操作
```java
@Override
public V remove(K key) {
    if (key == null) return null;
    
    int index = Math.floorMod(key.hashCode(), capacity);
    Collection<Node> bucket = buckets[index];
    Node node = getNode(key);
    
    if (node != null) {
        bucket.remove(node);
        size--;
        return node.value;
    }
    return null;
}
```

## 5. 时间复杂度分析

| 操作 | 最好情况 | 平均情况 | 最坏情况 |
|------|---------|---------|---------|
| 插入 (put) | O (1) | O (1) | O (n) |
| 查找 (get/contains) | O (1) | O (1) | O (n) |
| 删除 (remove) | O (1) | O (1) | O (n) |

**说明**：
- 平均情况基于良好哈希函数和适当负载因子
- 最坏情况发生在所有元素哈希到同一桶时
- 通过动态扩容和良好哈希函数可避免最坏情况

## 6. 重要注意事项

### 6.1 键的不可变性
- 哈希表要求键对象不可变
- 如果键的哈希值在插入后改变，将无法正确查找
- 解决方案：使用不可变对象作为键，或确保键对象不变

### 6.2 equals 和 hashCode 的契约
```java
// 必须同时重写这两个方法
@Override
public boolean equals(Object obj) {
    // 实现相等性判断
}

@Override
public int hashCode() {
    // 计算哈希值，相等的对象必须返回相同哈希值
}
```

**契约规则**：
1. 如果 `a.equals(b)` 返回 true，则 `a.hashCode() == b.hashCode()`
2. 反之不成立：哈希值相同的对象不一定相等（哈希冲突）

### 6.3 负载因子选择
- **默认值 0.75**：时间与空间的良好平衡
- **较小值**（如 0.5）：更快的操作，更多空间
- **较大值**（如 0.9）：更少空间，可能更慢

### 6.4 冲突解决策略
1. **链地址法**（本实现使用）：每个桶使用链表存储冲突元素
2. **开放地址法**：在数组中寻找下一个空桶
3. **再哈希法**：使用第二个哈希函数

## 7. 桶数据结构的选择

```java
protected Collection<Node> createBucket() {
    // 可选择不同的数据结构作为桶
    return new LinkedList<>();        // 简单链表
    // return new ArrayList<>();      // 动态数组
    // return new TreeSet<>();        // 有序集合（如果键可比）
}
```

**链表 vs 红黑树**（Java 8+ HashMap）：
- 桶元素少时：使用链表（O (n)）
- 桶元素多时：转为红黑树（O (log n)）
- 阈值：通常为 8 个元素

## 8. 总结

哈希表通过以下机制实现高效操作：

1. **哈希函数**：将任意对象映射到有限范围的整数
2. **桶数组**：分散存储元素，减少比较次数
3. **动态扩容**：保持负载因子在合理范围内
4. **冲突解决**：处理哈希碰撞，保证正确性

相比 Search Tree，哈希表：
- ✓ 不要求元素可比
- ✓ 平均 O (1) 时间复杂度
- ✗ 没有顺序性
- ✗ 对哈希函数质量敏感

在实际应用中，Java 的 HashMap 实现还包含更多优化，如树化、缓存哈希值等，以应对各种使用场景。