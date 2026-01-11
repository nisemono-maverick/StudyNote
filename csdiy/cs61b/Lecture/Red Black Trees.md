## 引言
平衡二叉搜索树在数据结构中至关重要，能够提供高效的查找、插入和删除操作。然而，不同平衡树实现有不同的优缺点。本笔记介绍如何通过树旋转和左倾红黑树（LLRB）来解决传统平衡树的问题。

## B 树的局限
B 树是一种自平衡树，通过节点分裂与合并维持平衡。但当节点容量 L 较小时，插入删除操作可能引发大量节点分裂合并的连锁反应，需要复杂的递归处理，实现难度大。

## 树旋转（Tree Rotation）
### 为什么需要旋转？
同一个数据集可能形成不同结构的 BST，影响操作效率。理想情况是保持树的"茂密"（平衡）形态。
![[Pasted image 20260107105727.png]]

### 旋转操作
**左旋（rotateLeft）**：
- 设 G 的右子节点为 P
- 将 P 的左子树作为 G 的右子树
- 将 G 作为 P 的左子节点
- 更新节点颜色（在红黑树中）
![[Pasted image 20260107111016.png]]

**右旋（rotateRight）**：
- 设 G 的左子节点为 P
- 将 P 的右子树作为 G 的左子树
- 将 G 作为 P 的右子节点
- 更新节点颜色（在红黑树中）

```java
private Node rotateRight(Node h) {
    Node x = h.left;
    h.left = x.right;
    x.right = h;
    return x;
}

private Node rotateLeft(Node h) {
    Node x = h.right;
    h.right = x.left;
    x.left = h;
    return x;
}
```


## 左倾红黑树（Left-Leaning Red-Black Tree）
### 核心理念
将 2-3 树的平衡性映射到 BST 中，使用"红链接"表示 2-3 树中的 3-节点连接。

### 2-3 树与红黑树对应关系
- 2-3 树的 2-节点 ↔ 普通黑色节点
- 2-3 树的 3-节点 ↔ 由红连接的两个节点
- 左倾规则：红连接只能在左侧（确保一致性）

### 优势
1. 保持 2-3 树的平衡特性
2. BST 的简单搜索操作
3. 相对简单的插入删除实现

## 左倾红黑树实现

### 节点结构
```java
static class RBTreeNode<T> {
    final T item;
    boolean isBlack;  // true=黑色, false=红色
    RBTreeNode<T> left;
    RBTreeNode<T> right;
    
    RBTreeNode(boolean isBlack, T item, RBTreeNode<T> left, RBTreeNode<T> right) {
        this.isBlack = isBlack;
        this.item = item;
        this.left = left;
        this.right = right;
    }
}
```

### 核心操作
#### 1. 颜色翻转（flipColors）
```java
void flipColors(RBTreeNode<T> node) {
    // 翻转节点及其两个子节点的颜色
    node.isBlack = !node.isBlack;
    node.left.isBlack = !node.left.isBlack;
    node.right.isBlack = !node.right.isBlack;
}
```
**作用**：将 4-节点（临时情况）分裂为三个 2-节点

#### 2. 旋转操作（带颜色交换）
```java
RBTreeNode<T> rotateRight(RBTreeNode<T> node) {
    RBTreeNode<T> x = node.left;
    node.left = x.right;
    x.right = node;
    // 交换新旧根节点颜色
    boolean color = node.isBlack;
    node.isBlack = x.isBlack;
    x.isBlack = color;
    return x;
}
```

#### 3. 插入算法
```java
private RBTreeNode<T> insert(RBTreeNode<T> node, T item) {
    // 1. 标准BST插入（新节点为红色）
    if (node == null) return new RBTreeNode<>(false, item);
    
    int cmp = item.compareTo(node.item);
    if (cmp < 0) node.left = insert(node.left, item);
    else if (cmp > 0) node.right = insert(node.right, item);
    
    // 2. 平衡修复（自底向上）
    // 情况1：修复右红链接
    if (isRed(node.right) && !isRed(node.left)) 
        node = rotateLeft(node);
    
    // 情况2：修复两个连续左红链接
    if (isRed(node.left) && isRed(node.left.left))
        node = rotateRight(node);
    
    // 情况3：修复两个红子节点
    if (isRed(node.left) && isRed(node.right))
        flipColors(node);
    
    return node;
}
```

### 插入修复的三种情况
1. **右红链接**：左旋转换为左红链接
2. **连续两个左红链接**：右旋形成平衡结构
3. **节点有两个红子节点**：颜色翻转，红链接向上传递

## 性能特点
- **时间复杂度**：所有操作 O (log n)
- **空间复杂度**：O (n)
- **高度保证**：最坏情况高度≤2 log₂(n+1)
- **近似平衡**：任意路径黑色节点数相同

## 与 AVL 树比较

| 特性    | 左倾红黑树 | AVL 树 |
| ----- | ----- | ----- |
| 平衡严格度 | 较宽松   | 严格    |
| 旋转频率  | 较低    | 较高    |
| 插入/删除 | 更快    | 稍慢    |
| 查找    | 稍慢    | 更快    |
| 实现难度  | 中等    | 较复杂   |

## 总结
左倾红黑树巧妙地将 2-3 树的平衡性通过颜色标记和旋转操作映射到 BST 中，实现了：
1. 相对简单的平衡维护逻辑
2. 良好的最坏情况性能保证
3. 比 AVL 树更高效的动态操作

这种方法展示了如何通过抽象和映射解决复杂问题：将难以直接实现的 2-3 树转化为相对容易实现的 BST 变体，同时保留了前者的平衡特性。

---
*注：左倾红黑树由 Robert Sedgewick 提出，是红黑树的一种简化实现，特别适合教学和实际应用。*