BSTs 使得可以在 log(N) 时间内快速搜寻 items
如果我们只关心快速的找到最小活最大的元素而非快速搜寻呢

新的数据结构：优先队列（Priority Queues）
可以向队列中 add 元素；
可以 get 和 remove 元素，但都只能与最小的那个元素交互
```java
/** (Min) Priority Queue: Allowing tracking and removal of 
  * the smallest item in a priority queue. */
public interface MinPQ<Item> {
    /** Adds the item to the priority queue. */
    public void add (Item x);
    /** Returns the smallest item in the priority queue. */
    public Item getSmallest ();
    /** Removes the smallest item from the priority queue. */
    public Item removeSmallest ();
    /** Returns the size of the priority queue. */
    public int size ();
}
```

优先队列能解决哪些实际问题呢？
在大量信息中处理最重要的。如医疗监控系统中处理紧急任务。
优先队列的目的是在特化查询时间
这也就解释了为什么我们不能使用之前学习过的数据结构来实现他

|                | Ordered Array | Bushy BST      | Hash Table  | Heap           |
| -------------- | ------------- | -------------- | ----------- | -------------- |
| add            | $\Theta(N)$   | $\Theta(logN)$ | $\Theta(1)$ | $\Theta(logN)$ |
| getSmallest    | $\Theta(1)$   | $\Theta(logN)$ | $\Theta(N)$ | $\Theta(1)$    |
| removeSmallest | $\Theta(N)$   | $\Theta(logN)$ | $\Theta(N)$ | $\Theta(logN)$ |
看起来 Bushy BST 都在 logN 时间内，但是 BST 里不能存在重复的元素，所以不能直接使用


堆（heaps）

二叉最小堆（Binary min-heap）
二叉最小堆是一颗二叉树，并且满足 complete 和 min-heap 两个性质
Min-heap：每个节点都小于或等于他的两个子节点
complete：只可能在底端可能缺少节点，换句话说，这棵树只能从上到下，从左往右依次填充
一些示例：
![[Pasted image 20260110105017.png]]
getSmallest 方法只需要取 root 节点的值就行
add 方法：
第一步，把新元素放在一个合适的位置，满足 complete 性质（**那么什么位置是合适位置呢**）
第二步，如果他违反了 min-heap 性质，就迭代的进行与父节点的元素交换的过程
removeSmallest 方法：
第一步，将根节点元素取出来，拿最后加入的元素移动到根节点
第二步，如果他违反了 min-heap 性质，就迭代的进行与子节点的元素交换的过程（对比的时候对比 2 个子节点）

代码实现
如何表示一棵树
1a: 父节点指向他的每个子节点
![[Pasted image 20260110111440.png]]
1b：父节点存储数组，数组中存每个子节点的指针
![[Pasted image 20260110111635.png]]
1c: 父节点一个指针指向他的子节点的第一个，另一个节点指向他的下一个兄弟节点
![[Pasted image 20260110111814.png]]
2：用一个数组 `keys` 存储值，另一个数组 `parents` 存储 parentID（连接状态）
![[Pasted image 20260110111933.png]]
3a：结合二叉最小堆，如果要求我的树是 complete 的，那么 parents 数组的值一定是确定的，也就是说实现时根本就没必要建 parents 数组了
问题：那么我们怎么实现 parents 这个方法？ `return (value-1)/2`
3b：或者，存储 keys 数组时可以在 0 位置不存数，这样 parents 方法就直接变成了 `return value/2`
![[Pasted image 20260110113402.png]]
