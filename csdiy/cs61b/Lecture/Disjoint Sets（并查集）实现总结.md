## 概述
Disjoint Sets（并查集）是一种用于处理不相交集合的数据结构，主要支持两种操作：
- `connect(x, y)`：连接两个元素
- `isConnected(x, y)`：检查两个元素是否连接

## 1. QuickFind 实现

### 原理
- 使用数组实现，数组索引代表元素，数组值代表该元素所属的集合 ID
- 所有相连的元素具有相同的集合 ID

### 代码实现
```java
public class QuickFindDS implements DisjointSets {
    private int[] id;
    
    public QuickFindDS(int N) {
        id = new int[N];
        for (int i = 0; i < N; i++) {
            id[i] = i;  // 初始时每个元素自成一组
        }
    }
    
    public boolean isConnected(int p, int q) {
        return id[p] == id[q];
    }
    
    public void connect(int p, int q) {
        int pid = id[p];
        int qid = id[q];
        if (pid == qid) return;  // 已经连接
        
        for (int i = 0; i < id.length; i++) {
            if (id[i] == pid) {
                id[i] = qid;
            }
        }
    }
}
```

### 时间复杂度
- `isConnected`: O (1)
- `connect`: O (N)

## 2. QuickUnion 实现

### 原理
- 使用数组表示森林，每个元素指向其父节点
- 根节点的父节点为负数或自身（不同实现方式）
- 通过向上查找找到根节点来判断连接关系

### 代码实现
```java
public class QuickUnionDS implements DisjointSets {
    private int[] parent;
    
    public QuickUnionDS(int N) {
        parent = new int[N];
        for (int i = 0; i < N; i++) {
            parent[i] = -1;  // 初始时每个元素都是根节点
        }
    }
    
    private int find(int p) {
        int r = p;
        while (parent[r] >= 0) {
            r = parent[r];
        }
        return r;
    }
    
    public boolean isConnected(int p, int q) {
        return find(p) == find(q);
    }
    
    public void connect(int p, int q) {
        int i = find(p);  
        int j = find(q);  
        if (i == j) return;  // 已经连接
        
        parent[i] = j;  // 将i的根节点连接到j的根节点
    }
}
```

### 时间复杂度
- `find`: O (h)，h 为树高
- `isConnected`: O (h)
- `connect`: O (h)

## 3. WeightedQuickUnion 实现

### 原理
- 改进 QuickUnion，避免生成高树
- 跟踪每棵树的大小（元素数量）
- 总是将小树连接到大树的根节点上
- 根节点的值存储负的树大小

### 代码实现
```java
public class WeightedQuickUnionDS implements DisjointSets {
    private int[] parent;
    
    public WeightedQuickUnionDS(int N) {
        parent = new int[N];
        for (int i = 0; i < N; i++) {
            parent[i] = -1;
        }
    }
    
    private int find(int p) {
        int r = p;
        while (parent[r] >= 0) {
            r = parent[r];
        }
        return r;
    }
    
    public boolean isConnected(int p, int q) {
        return find(p) == find(q);
    }
    
    public void connect(int p, int q) {
        int i = find(p);
        int j = find(q) ;
        if (i == j) return;
        
        // 比较树的大小（注意：存储的是负值，所以值越小表示树越大）
        if (parent[i] > parent[j]) {  // i的树更小（因为负数的比较：-2 > -5）
            parent[j] += parent[i];
            parent[i] = j;
        } else {
            parent[i] += parent[j];
            parent[j] = i;
        }
    }
}
```

### 时间复杂度
- 树的最大高度为 O (log N)
- 所有操作：O (log N)

## 4. HeightedQuickUnion 实现

### 原理
- 跟踪每棵树的深度（高度）
- 连接时，将较浅的树连接到较深的树上
- 根节点的值存储负的树深度

### 代码实现
```java
public class HeightedQuickUnionDS implements DisjointSets {
    private int[] parent;
    
    public HeightedQuickUnionDS(int N) {
        parent = new int[N];
        for (int i = 0; i < N; i++) {
            parent[i] = -1;  // 初始深度为1（用-1表示）
        }
    }
    
    private int find(int p) {
        int r = p;
        while (parent[r] >= 0) {
            r = parent[r];
        }
        return r;
    }
    
    public boolean isConnected(int p, int q) {
        return find(p) == find(q);
    }
    
    public void connect(int p, int q) {
        int i = find(p);
        int j = find(q);
        if (i == j) return;
        
        // 注意：parent[i]和parent[j]是负的深度值
        // 深度值越大（绝对值越大）表示树越深
        
        if (parent[i] > parent[j]) {  // i的深度更浅（因为-1 > -2）
            parent[i] = j;
        } else if (parent[i] < parent[j]) {  // j的深度更浅
            parent[j] = i;
        } else {  // 深度相等
            parent[j] -= 1;  // 深度增加1
            parent[i] = j;
        }
    }
}
```

## 5. 路径压缩优化

### 原理
- 在查找根节点时，将路径上的所有节点直接连接到根节点
- 可以大幅降低树的高度

### 代码实现（基于 WeightedQuickUnion）
```java
public class WeightedQuickUnionWithPathCompressionDS implements DisjointSets {
    private int[] parent;
    
    public WeightedQuickUnionWithPathCompressionDS(int N) {
        parent = new int[N];
        for (int i = 0; i < N; i++) {
            parent[i] = -1;
        }
    }
    
    private int find(int p) {
        if (parent[p] < 0) {
            return p;
        }
        // 路径压缩：将当前节点直接连接到根节点
        parent[p] = find(parent[p]);
        return parent[p];
    }
    
    public boolean isConnected(int p, int q) {
        return find(p) == find(q);
    }
    
    public void connect(int p, int q) {
        int i = find(p);
        int j = find(q);
        if (i == j) return;
        
        if (parent[i] > parent[j]) {
            parent[j] += parent[i];
            parent[i] = j;
        } else {
            parent[i] += parent[j];
            parent[j] = i;
        }
    }
}
```

### 时间复杂度
- 接近 O (α(N))，其中α(N) 是反阿克曼函数，非常小

## 测试文件

```java
import org.junit.Test;
import static org.junit.Assert.*;

public class DisjointSetsTest {
    
    // 测试QuickFindDS
    @Test
    public void testQuickFindDS() {
        DisjointSets ds = new QuickFindDS(10);
        
        // 初始状态：没有连接
        assertFalse(ds.isConnected(0, 1));
        assertFalse(ds.isConnected(2, 3));
        
        // 连接测试
        ds.connect(0, 1);
        assertTrue(ds.isConnected(0, 1));
        assertTrue(ds.isConnected(1, 0));
        
        // 传递性测试
        ds.connect(1, 2);
        assertTrue(ds.isConnected(0, 2));
        assertTrue(ds.isConnected(2, 0));
        
        // 不相交集合测试
        ds.connect(3, 4);
        assertTrue(ds.isConnected(3, 4));
        assertFalse(ds.isConnected(0, 3));
        assertFalse(ds.isConnected(2, 4));
    }
    
    // 测试QuickUnionDS
    @Test
    public void testQuickUnionDS() {
        DisjointSets ds = new QuickUnionDS(10);
        
        // 初始状态：没有连接
        assertFalse(ds.isConnected(0, 1));
        
        // 连接测试
        ds.connect(0, 1);
        assertTrue(ds.isConnected(0, 1));
        
        // 传递性测试
        ds.connect(1, 2);
        assertTrue(ds.isConnected(0, 2));
        
        // 自反性测试
        assertTrue(ds.isConnected(0, 0));
        assertTrue(ds.isConnected(2, 2));
    }
    
    // 测试WeightedQuickUnionDS
    @Test
    public void testWeightedQuickUnionDS() {
        DisjointSets ds = new WeightedQuickUnionDS(10);
        
        // 测试基本连接
        ds.connect(0, 1);
        ds.connect(2, 3);
        assertTrue(ds.isConnected(0, 1));
        assertTrue(ds.isConnected(2, 3));
        assertFalse(ds.isConnected(0, 2));
        
        // 测试权重大小树的连接
        ds.connect(0, 2);  // 连接两棵树
        assertTrue(ds.isConnected(1, 3));
        assertTrue(ds.isConnected(0, 3));
        
        // 测试多次连接
        ds.connect(4, 5);
        ds.connect(5, 6);
        ds.connect(3, 4);
        assertTrue(ds.isConnected(0, 6));
    }
    
    // 测试HeightedQuickUnionDS
    @Test
    public void testHeightedQuickUnionDS() {
        DisjointSets ds = new HeightedQuickUnionDS(10);
        
        // 测试基本连接
        ds.connect(0, 1);
        ds.connect(2, 3);
        assertTrue(ds.isConnected(0, 1));
        assertTrue(ds.isConnected(2, 3));
        
        // 测试深度不同的树连接
        ds.connect(0, 2);
        assertTrue(ds.isConnected(1, 3));
        
        // 测试深度相同的树连接
        ds.connect(4, 5);
        ds.connect(6, 7);
        ds.connect(4, 6);  // 深度相同，连接后深度增加
        assertTrue(ds.isConnected(5, 7));
    }
    
    // 测试WeightedQuickUnionWithPathCompressionDS
    @Test
    public void testWeightedQuickUnionWithPathCompressionDS() {
        DisjointSets ds = new WeightedQuickUnionWithPathCompressionDS(10);
        
        // 创建一条长链
        ds.connect(0, 1);
        ds.connect(1, 2);
        ds.connect(2, 3);
        ds.connect(3, 4);
        
        // 测试连接
        assertTrue(ds.isConnected(0, 4));
        assertTrue(ds.isConnected(1, 3));
        
        // 路径压缩后，查找应该更快
        ds.isConnected(0, 4);  // 这次查找会压缩路径
        
        // 继续测试
        ds.connect(5, 6);
        ds.connect(6, 7);
        ds.connect(7, 8);
        ds.connect(0, 5);
        
        assertTrue(ds.isConnected(4, 8));
        assertTrue(ds.isConnected(1, 7));
    }
    
    // 比较不同实现的性能（可选）
    @Test
    public void testLargeDataSet() {
        int N = 1000;
        
        // 测试WeightedQuickUnion的性能
        DisjointSets ds1 = new WeightedQuickUnionDS(N);
        long start = System.currentTimeMillis();
        for (int i = 0; i < N - 1; i++) {
            ds1.connect(i, i + 1);
        }
        long end = System.currentTimeMillis();
        System.out.println("WeightedQuickUnion time: " + (end - start) + "ms");
        assertTrue(ds1.isConnected(0, N - 1));
        
        // 测试带路径压缩的性能
        DisjointSets ds2 = new WeightedQuickUnionWithPathCompressionDS(N);
        start = System.currentTimeMillis();
        for (int i = 0; i < N - 1; i++) {
            ds2.connect(i, i + 1);
        }
        end = System.currentTimeMillis();
        System.out.println("WeightedQuickUnion with Path Compression time: " + (end - start) + "ms");
        assertTrue(ds2.isConnected(0, N - 1));
    }
}

// 定义DisjointSets接口
interface DisjointSets {
    boolean isConnected(int p, int q);
    void connect(int p, int q);
}
```

## 总结比较

| 实现方式 | connect 时间复杂度 | isConnected 时间复杂度 | 特点 |
|---------|-----------------|---------------------|------|
| QuickFind | O (N) | O (1) | 查找快，连接慢 |
| QuickUnion | O (h) | O (h) | 可能产生高树 |
| WeightedQuickUnion | O (log N) | O (log N) | 平衡树大小 |
| HeightedQuickUnion | O (log N) | O (log N) | 平衡树高度 |
| 带路径压缩的 WeightedQuickUnion | 接近 O (α(N)) | 接近 O (α(N)) | 最优实现 |

在实际应用中，**带路径压缩的 WeightedQuickUnion**是最常用的实现方式，因为它提供了接近常数时间的操作性能。