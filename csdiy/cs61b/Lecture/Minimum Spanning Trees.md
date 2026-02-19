## 1. Core Concepts

### Spanning Tree
Given a connected, undirected graph `G(V, E)`, a **Spanning Tree** `T` is a subgraph that satisfies:
- **Connected**: All vertices are reachable from any other vertex.
- **Acyclic**: Contains no cycles.
- **Spanning**: Includes all vertices of `G`.

A graph with `V` vertices has a spanning tree with exactly `V - 1` edges.

### Minimum Spanning Tree (MST)
A **Minimum Spanning Tree** is a spanning tree where the sum of the edge weights is minimized.

---

## 2. The Cut Property: Foundation of MST Algorithms

A **Cut** is a partition of the graph's vertices into two non-empty sets `(S, V-S)`.

A **Crossing Edge** is an edge that connects a vertex in `S` to a vertex in `V-S`.

**Cut Property**: For any cut of the graph, the minimum-weight crossing edge must be in the MST.
> This property is fundamental to proving the correctness of both Prim's and Kruskal's algorithms.
> It provides a *greedy* rule for building the MST safely.

![[Pasted image 20260127151621.png]]

### Algorithmic Idea from the Cut Property
1. Find a cut such that **no crossing edge** is currently in the MST.
2. Add the **minimum-weight crossing edge** of this cut to the MST.
3. Repeat until the MST has `V-1` edges.

The challenge: *How do we find such a cut efficiently?* This leads to different algorithms.

![[Pasted image 20260127152711.png]]

---

## 3. Prim's Algorithm

### Principle
- **Start** from an arbitrary vertex. This defines the initial cut: one set contains this single vertex, the other contains all the rest.
- **Grow** the MST by iteratively adding the minimum-weight edge connecting the current tree to a vertex not yet in the tree.
- This is equivalent to **moving** the newly connected vertex from the "unvisited" set to the "tree" set, creating a new cut, and repeating.

### Optimized Implementation (Using a Priority Queue)
Similar to Dijkstra's algorithm for shortest paths, but the priority is based on the **distance to the MST** (the weight of the lightest edge connecting a vertex to the current tree), not the distance from a source.

**Data Structures**:
- `edgeTo[v]`: The lightest edge connecting vertex `v` to the MST.
- `distTo[v]`: The weight of that edge (`Double.POSITIVE_INFINITY` if not yet connected).
- A **Min-Priority Queue (Fringe PQ)**: Stores vertices not yet in the MST, keyed by `distTo[]`.

**Steps**:
1. Initialize `distTo[]` to infinity and `edgeTo[]` to null. Add all vertices to the PQ.
2. Set `distTo[start] = 0` and update its priority in the PQ.
3. While the PQ is not empty:
    a. **Remove the vertex `v` with the minimum `distTo`** from the PQ (add it to the MST).
    b. **Relax** all edges incident to `v`. For each edge `e = (v, w)`:
        - If `w` is still in the PQ and `e.weight() < distTo[w]`, update `distTo[w]` and `edgeTo[w]`, and decrease `w` 's key in the PQ.

### Runtime Analysis of Prim's Algorithm
| Operation              | Number of Times | Cost per Op | Total Cost  |
| ---------------------- | --------------- | ----------- | ----------- |
| **PQ Insert (init)**   | V               | O (log V)    | O (V log V)  |
| **PQ Delete Min**      | V               | O (log V)    | O (V log V)  |
| **PQ Decrease Key**    | O (E)            | O (log V)    | O (E log V)  |
| **Total**              |                 |             | **O (E log V)** |

---

## 4. Kruskal's Algorithm

### Principle
- **Sort** all edges in ascending order of weight.
- **Iterate** through the sorted edges.
- **Add** an edge to the MST **unless** it creates a cycle with the edges already selected.
- Stop when `V-1` edges have been added.

### Efficient Cycle Detection
We need a data structure to track connectivity as we add edges. A **[[Disjoint Sets（并查集）实现总结 |Union-Find (Disjoint Set)]]** data structure is perfect.
- Initially, each vertex is its own component.
- For an edge `(v, w)`, check if `v` and `w` are connected.
  - If **yes**, adding the edge creates a cycle → **skip it**.
  - If **no**, add the edge to the MST and **union** the two components.

### Runtime Analysis of Kruskal's Algorithm

| Operation            | Number of Times | Cost per Op | Total Cost      |
| -------------------- | --------------- | ----------- | --------------- |
| **Sort Edges**       | 1               | O (E log E) | O (E log E)     |
| **Union-Find Find**  | O (E)           | O (α(V))    | O (E α(V))      |
| **Union-Find Union** | O (V)           | O (α(V))    | O (V α(V))      |
| **Total**            |                 |             | **O (E log E)** |

> *`α(V)` is the inverse Ackermann function, which is effectively constant (`≤ 4`) for all practical inputs.
> Since `O(log E)` is equivalent to `O(log V)` for connected graphs, the runtime is **O (E log V)**.

---

## 5. Comparison: Prim vs. Kruskal

| Aspect                | Prim's Algorithm                          | Kruskal's Algorithm                           |
| --------------------- | ----------------------------------------- | --------------------------------------------- |
| **Approach**          | **Vertex-based**. Grows a single tree.    | **Edge-based**. Merges multiple components.   |
| **Best for**          | Dense graphs (`E ≈ V²`)                   | Sparse graphs (`E ≈ V`)                       |
| **Key Data Structure**| Priority Queue (Min-Heap)                 | Union-Find + Sorted Edges                     |
| **Typical Runtime**   | `O(E log V)` with Binary Heap             | `O(E log V)` (dominated by sorting)           |
| **Works on**          | Requires connected graph initially.       | Can find *forest* for disconnected graph.     |

### Choice of Algorithm
- **Use Prim's** when the graph is dense (e.g., using an **adjacency matrix**). It can be optimized to `O(V²)` without a heap.
- **Use Kruskal's** when the graph is sparse, or if the edges are **already sorted**. Its implementation is often simpler.

---

## 6. Implementations (Key Ideas)

### Prim's Algorithm (Optimized)
```java
// Key Idea: Use IndexMinPQ to maintain vertices by their distance to the MST.
public class PrimMST {
    private Edge[] edgeTo;        // edgeTo[v] = shortest edge from tree to v
    private double[] distTo;      // distTo[v] = weight of that edge
    private IndexMinPQ<Double> pq; // priority queue of vertices
    private boolean[] marked;     // marked[v] = true if v on tree (can be inferred from pq)

    private void relax(EdgeWeightedGraph G, int v) {
        for (Edge e : G.adj(v)) {
            int w = e.other(v);
            if (marked[w]) continue; // Already in the MST
            if (e.weight() < distTo[w]) {
                // Found a better edge to connect w to the tree
                distTo[w] = e.weight();
                edgeTo[w] = e;
                if (pq.contains(w)) pq.decreaseKey(w, distTo[w]);
                else                pq.insert(w, distTo[w]);
            }
        }
    }
}
```

### Kruskal's Algorithm
```java
// Key Idea: Sort edges, use Union-Find to avoid cycles.
public class KruskalMST {
    private Queue<Edge> mst = new Queue<>();

    public KruskalMST(EdgeWeightedGraph G) {
        // 1. Sort edges by weight
        Edge[] edges = G.edges().toArray(new Edge[0]);
        Arrays.sort(edges);

        // 2. Initialize Union-Find
        UnionFind uf = new UnionFind(G.V());

        // 3. Greedily add edges
        for (Edge e : edges) {
            int v = e.either(), w = e.other(v);
            if (!uf.connected(v, w)) { // Check if adding creates a cycle
                uf.union(v, w);       // Merge components
                mst.enqueue(e);       // Add edge to MST
                if (mst.size() == G.V() - 1) break; // Stop when tree is complete
            }
        }
    }
}
```

---

## Summary of Key Takeaways
1.  **The Cut Property** is the foundational theorem enabling greedy MST algorithms.
2.  **Prim's Algorithm** grows the MST from a single vertex, always adding the closest vertex to the existing tree. It is efficient for dense graphs.
3.  **Kruskal's Algorithm** builds the MST by adding edges in sorted order, skipping those that create cycles. It is efficient for sparse graphs and uses the Union-Find structure elegantly.
4.  Both algorithms run in **O (E log V)** time and are correct due to the cut property.
5.  The choice between Prim and Kruskal often depends on graph density and implementation simplicity.