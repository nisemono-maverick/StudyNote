## 一、从有序链表到二叉搜索树的思考

### 1.1 有序链表的局限性
- **时间复杂度**：在有序链表中查找元素需要 O (n) 时间
- **优化思路**：从中间开始，向两边查找（类似于二分查找）

### 1.2 二叉搜索树的核心思想
- 将链表的"中间节点"作为根节点
- 左子树包含所有小于根节点的元素
- 右子树包含所有大于根节点的元素
- 对每个子树递归应用相同规则

## 二、二叉搜索树（BST）基本概念

### 2.1 定义
二叉搜索树是一种特殊的二叉树，满足以下性质：
1. 左子树所有节点的值 < 根节点的值
2. 右子树所有节点的值 > 根节点的值
3. 左右子树也都是二叉搜索树

### 2.2 搜索操作
```java
// 伪代码
search(节点 T, 搜索键 key):
    if T == null: return null
    if key == T.key: return T
    if key < T.key: return search(T.left, key)
    if key > T.key: return search(T.right, key)
```

**时间复杂度**：
- 最好/平均情况：O (log n) - 树是平衡的
- 最坏情况：O (n) - 树退化为链表

### 2.3 插入操作
```java
// 伪代码
插入节点：
1. 搜索键值是否存在
2. 如果找到，不操作或更新值
3. 如果未找到，在适当位置创建新节点
```

### 2.4 删除操作
删除节点有三种情况：

#### 情况 1：无子节点
直接断开与父节点的连接

#### 情况 2：有一个子节点
父节点直接指向该子节点


#### 情况 3：有两个子节点
1. 找到左子树的最大节点（最右节点）或右子树的最小节点（最左节点）
2. 将该节点从原位置删除（情况 1 或 2）
3. 用该节点替换要删除的节点

## 三、BSTMap 实现详解

### 3.1 核心数据结构
```java
private class Entry {
    K key;          // 键（可比较）
    V val;          // 值
    Entry left;     // 左子树
    Entry right;    // 右子树
}
```

### 3.2 主要方法实现

#### 3.2.1 插入（put）
```java
private Entry putHelper(Entry entry, K key, V value) {
    if (entry == null) {
        size++;
        return new Entry(key, value, null, null);
    }
    int cmp = key.compareTo(entry.key);
    if (cmp == 0) entry.val = value;        // 键已存在，更新值
    else if (cmp < 0) entry.left = putHelper(entry.left, key, value);
    else entry.right = putHelper(entry.right, key, value);
    return entry;
}
```

#### 3.2.2 搜索（get）
```java
private Entry getHelper(Entry entry, K key) {
    if (entry == null) return null;
    int cmp = key.compareTo(entry.key);
    if (cmp == 0) return entry;
    if (cmp < 0) return getHelper(entry.left, key);
    return getHelper(entry.right, key);
}
```

#### 3.2.3 删除（remove）
```java
private Entry removeHelper(Entry entry, K key) {
    if (entry == null) return null;
    int cmp = key.compareTo(entry.key);
    if (cmp < 0) entry.left = removeHelper(entry.left, key);
    else if (cmp > 0) entry.right = removeHelper(entry.right, key);
    else {  // 找到要删除的节点
        size--;
        if (entry.left == null) return entry.right;      // 情况1或2
        if (entry.right == null) return entry.left;      // 情况2
        Entry temp = entry;                             // 情况3
        entry = maxEntry(entry.left);                   // 找到左子树最大节点
        entry.left = removeMaxEntry(temp.left);         // 删除原最大节点
        entry.right = temp.right;                       // 连接右子树
    }
    return entry;
}
```

### 3.3 遍历方式

#### 3.3.1 中序遍历（In-order Traversal）
- 左子树 → 根节点 → 右子树
- **重要特性**：对 BST 进行中序遍历会得到有序序列
- 在代码中通过 Iterator 实现

```java
private void inorder(Entry entry, List<K> list) {
    if (entry == null) return;
    inorder(entry.left, list);    // 遍历左子树
    list.add(entry.key);          // 访问根节点
    inorder(entry.right, list);   // 遍历右子树
}
```

#### 3.3.2 其他遍历方式
- **先序遍历**：根节点 → 左子树 → 右子树
- **后序遍历**：左子树 → 右子树 → 根节点
- **层次遍历**：按层次从上到下，从左到右

### 3.4 集合与映射
- **作为有序集合（Ordered Set）**：只需关注键
- **作为映射（Map）**：键值对存储，键唯一且有序

## 四、性能分析

### 4.1 时间复杂度
| 操作 | 最好/平均情况 | 最坏情况 |
|------|--------------|----------|
| 搜索 | O (log n)     | O (n)     |
| 插入 | O (log n)     | O (n)     |
| 删除 | O (log n)     | O (n)     |
| 遍历 | O (n)         | O (n)     |

### 4.2 空间复杂度
- 存储：O (n)
- 递归栈深度：O (h)，其中 h 为树的高度

### 4.3 优缺点
**优点**：
1. 有序存储，便于范围查询
2. 平均情况下操作高效（O (log n)）
3. 实现相对简单

**缺点**：
1. 最坏情况下退化为链表（O (n)）
2. 需要保持平衡以获得最佳性能

## 五、平衡二叉搜索树简介

### 5.1 为什么需要平衡？
- 避免树退化为链表
- 保持 O (log n) 的时间复杂度

### 5.2 常见的平衡 BST
1. **AVL 树**：通过旋转保持平衡，高度差不超过 1
2. **红黑树**：通过颜色标记和旋转保持近似平衡
3. **B 树/B+树**：多路搜索树，常用于数据库和文件系统

## 六、应用场景

### 6.1 适合使用 BST 的场景
1. 需要有序数据存储和检索
2. 频繁的插入和删除操作
3. 需要范围查询（如查找某个区间的所有元素）

### 6.2 不适合使用 BST 的场景
1. 数据基本静态，很少变化（数组二分查找可能更合适）
2. 内存非常受限（树结构有额外指针开销）
3. 需要严格的 O (log n) 性能保证（需使用平衡 BST）

## 七、实践建议

### 7.1 实现注意事项
1. 考虑使用递归或迭代两种方式实现
2. 注意处理空指针异常
3. 在删除节点时正确维护树的连接

### 7.2 优化方向
1. 实现自平衡机制
2. 添加节点高度/深度信息
3. 实现非递归版本以减少栈开销
4. 添加范围查询、前驱/后继节点查找等功能

---

**总结**：二叉搜索树是从有序数据结构优化而来的重要数据结构，它将有序链表的 O (n) 搜索时间优化为平均 O (log n)。虽然普通 BST 在最坏情况下会退化为链表，但理解其基本原理是学习更高级平衡树结构的基础。在实际应用中，根据需求选择合适的 BST 变体至关重要。