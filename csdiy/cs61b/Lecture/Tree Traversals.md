![[Pasted image 20260112201913.png]]
层次遍历（Level Order）：从上到下，从左到右依次遍历
如图，顺序为：DBFACEG
这种遍历方式被称为广度优先搜索 Breadth First Search (BFS)

深度优先搜索 Depth First Search（DFS）
有三种形式：前序遍历、中序遍历、后序遍历
前序、中序、后序遍历是二叉树的三种深度优先遍历方式，它们的核心区别在于 **访问根节点的时机不同**：
- **前序遍历**：先访问 **根节点**，再遍历左子树，最后遍历右子树（根→左→右）。
- **中序遍历**：先遍历左子树，再访问 **根节点**，最后遍历右子树（左→根→右）。对二叉搜索树使用中序遍历，会得到一个升序序列。
- **后序遍历**：先遍历左子树，再遍历右子树，最后访问 **根节点**（左→右→根）。

三种遍历对左右子树的访问顺序始终是左在前、右在后，唯一的变量就是根节点的访问位置（前、中、后）。例如对于同一棵树：
- 前序输出为：`D B A C F E G`
```java
preOrder(BSTNode x) {
    if (x == null) return;
    print(x.key)
    preOrder(x.left)
    preOrder(x.right)
}
```
- 中序输出为：`A B C D E F G`
```java
inOrder(BSTNode x) {
    if (x == null) return;
    inOrder(x.left)
	print(x.key)
    inOrder(x.right)
}
```
- 后序输出为：`A C B E G F D`
```java
postOrder(BSTNode x) {
    if (x == null) return;
    postOrder(x.left)
    postOrder(x.right)
	print(x.key)
}
```
一个理解三种遍历方式的可视化 trick
![[Pasted image 20260112203432.png]]
画一条路径逆时针经过每个节点
前序遍历：当经过每个节点的左侧时记录
中序遍历：当经过每个节点的底部时记录
后序遍历：当经过每个节点的右侧时记录

使用案例：
前序：打印文件夹目录
后序：计算文件大小

