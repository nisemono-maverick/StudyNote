B 树的问题：对于 L 较小的 B 树来说，在插入、删除 item 过程中，会频繁牵涉到结点分裂、合并、重新分配的场景，此时可能会触发大量的连锁反应，需要进行大量的递归完成，且需要处理大量的分支情况，实现较困难

树旋转（Tree Rotation）
假设有一个 BST，插入节点 1,2,3，那么实际实现的 BST 可能用 5 种不同的形态
![[Pasted image 20260107105727.png]]
理论上来说，这 5 颗结构不同的树其实都是同一颗树
如果可能的话，希望可以通过方式都转化为中间那样茂密的形式
`rotateLeft(G): Let x be the right child of G. Make G the new left child of x.`
将 G 向左旋转：将 P 的 left child 作为 G 的 right child，将 G 作为 P 的新 left child
![[Pasted image 20260107111016.png]]
相对的，向右旋转同理
```java
private Node rotateRight (Node h) {
    // assert (h != null) && isRed (h.left);
    Node x = h.left;
    h.left = x.right;
    x.right = h;
    return x;
}

// make a right-leaning link lean to the left
private Node rotateLeft (Node h) {
    // assert (h != null) && isRed (h.right);
    Node x = h.right;
    h.right = x.left;
    x.left = h;
    return x;
}
```
![[Pasted image 20260107143909.png]]
还是以 3 个元素的 BST 为例，如上图，经过 2 步旋转可以转化为一颗茂密的树
`rotateRight(3)` and `rotateLeft(1)`

左倾红黑树
到目前为止，我们拥有了：
二叉搜索树：可以通过不断的树旋转，是他转化到平衡状态，但是没有一种算法支持此操作
2-3 树：本身就是平衡的，不需要旋转
那么：我们是否可以用构建 2-3 树的方法（因为他总是平衡的），构建一颗与他完全对应的二叉搜索树呢
![[Pasted image 20260107150056.png]]
如上图的 B 树，他使用 BST 应该如何表示呢
创建一个虚拟的，被标记为红色的连接，这个连接当然创建在左边和右边都是相似的
当如果把红色的连接当做真实的连接，就可以将他看作一颗 BST 了
我们将这种结构称作左倾红黑树（红色的连接总是在左侧）
左倾红黑树其实就是一颗 BST 只是加上了一些标记表示红色的连接
一颗 LLRB 树的高度是他对应的 2-3 树的 2 倍（当全部节点都有 2 个 item 的时候）

当需要执行搜索操作时，就和普通 BST 一样就行了

构建一颗红黑树
当插入一个 item 时，使用红色连接
如果有一个向右的红色连接，使用左旋转来修正
如果有两个相连的向左红色连接，使用右旋转来修正
如果一个节点有两个红色连接，翻转该节点的所有连接颜色来修正