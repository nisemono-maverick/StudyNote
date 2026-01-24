## 1. What is a Graph?
A **graph** consists of:
*   A set of **vertices** (also called **nodes**).
*   A set of **edges**, each connecting a pair of vertices.
**Trees** can be seen as a special type of graph with specific restrictions.

### The Simple Graph
In most contexts, when we say "graph," we refer to a **simple graph**, which has two key restrictions:
1.  **No self-loops**: An edge cannot connect a vertex to itself.
2.  **No parallel edges**: There cannot be two or more edges connecting the same pair of vertices.
![[Pasted image 20260112204706.png]]

## 2. Classifying Graphs
![[Pasted image 20260112205053.png]]
### 2.1 By Edge Directionality

| Type                         | Core Definition                                                | Key Feature                                                                                                    | Real-World Analogy                                                                                                                             |
| :--------------------------- | :------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| **Undirected Graph**         | Edges have **no direction**; they just represent a connection. | The relationship is **bidirectional** and **symmetric**. An edge `(A, B)` means A and B are connected equally. | **Friendship** (mutual), **road networks** (default two-way streets), **molecular structures**.                                                |
| **Directed Graph (Digraph)** | Edges have a direction, typically represented by an arrow.     | The relationship is **one-way** and **asymmetric**. An edge `A -> B` means a connection *from* A *to* B.       | **Social media follows** (A follows B), **web hyperlinks** (page A links to page B), **task dependencies** (A must finish before B can start). |

### 2.2 By the Presence of Cycles

| Type | Core Definition | Key Feature | Significance |
| :--- | :--- | :--- | :--- |
| **Acyclic Graph** | The graph contains **no cycles** (no circular paths). | It is impossible to start at a vertex and follow a sequence of edges to return to the starting vertex. | Represents strict hierarchies or dependencies (e.g., trees). |
| **Cyclic Graph** | The graph contains **at least one** cycle. | It is possible to start at a vertex, follow edges, and eventually return to it. | More common, can represent feedback loops and complex networks. |

### 2.3 With Edge Labels
 **Edge Labels**: A graph can be "with edge labels," meaning each edge carries an additional piece of data (e.g., a weight, cost, or type).

## 3. Common Graph Problems
*   **s-t Path**: Is there a path from vertex `s` to vertex `t`?
*   **Connectivity**: Is the graph connected? (Is there a path between *every* pair of vertices?)
*   **Biconnectivity**: Is there a vertex whose removal disconnects the graph?
*   **Shortest s-t Path**: What is the shortest path (by number of edges or edge weights) from `s` to `t`?
*   **Cycle Detection**: Does the graph contain a cycle?
*   **Euler Tour**: Is there a path that uses every edge **exactly once**?
*   **Hamilton Tour**: Is there a path that visits every vertex **exactly once**?
*   **Planarity**: Can the graph be drawn on a 2D plane without any edges crossing (except at vertices)?
*   **Isomorphism**: Are two graphs structurally identical?

## 4. Solving s-t Connectivity & Graph Traversal
A naive, incorrect attempt to see if `s` is connected to `t`:
```java
isConnected(Node s, Node t):
    if (s == t) return true;
    for (child in neighbors(s)):
        if isConnected(child, t) return true;
    return false;
```
**Problem**: This can run forever in cyclic graphs.
**Solution**: **Mark** visited vertices to avoid revisiting them.

### Depth-First Search (DFS)
The corrected algorithm is a **Depth-First Search**. It explores a branch as far as possible before backtracking and exploring the next branch.

**Depth-First Paths Algorithm** (recursive):
```
dfs(v):
    mark v;
    for (w in unmarked_neighbors(v)):
        set edgeTo[w] = v; // Remember we came from v to w
        dfs(w);
```

**DFS Paths Implementation (Java-style):**
```java
public class DepthFirstPaths {
    private boolean[] marked; // marked[v] = true if connected to source s
    private int[] edgeTo;     // edgeTo[w] = previous vertex on path from s to w
    private final int s;      // source vertex

    public DepthFirstPaths(Graph G, int s) {
        // ... initialize arrays
        this.s = s;
        dfs(G, s); // start DFS from source
    }

    private void dfs(Graph G, int v) {
        marked[v] = true;
        for (int w : G.adj(v)) {
            if (!marked[w]) {
                edgeTo[w] = v;
                dfs(G, w);
            }
        }
    }
    
    private void dfsIterative(Graph graph, int start) {
	    Stack<Integer> stack = new Stack<>();
	    stack.push(start);
	    
	    while (!stack.isEmpty()) {
	        int v = stack.pop();
	        if (!marked[v]) {
	            marked[v] = true;
	            for (int w : graph.adj(v)) {
	                if (!marked[w]) {
	                    edgeTo[w] = v;
	                    stack.push(w);
	                }
	            }
	        }
	    }
	}

    public boolean hasPathTo(int v) { return marked[v]; }

    public Iterable<Integer> pathTo(int v) {
        if (!hasPathTo(v)) return null;
        Stack<Integer> path = new Stack<>();
        // Backtrack from v to s using edgeTo
        for (int x = v; x != s; x = edgeTo[x]) {
            path.push(x);
        }
        path.push(s);
        return path;
    }
}
```

**DFS Node Ordering:**
We can record the order in which nodes are visited.
*   **Preorder**: Add the node to the list when we **first visit it** (when we push it onto the stack).
*   **Postorder**: Add the node to the list when we **finish exploring all its neighbors** (when we pop it from the stack).
*   **DFS with Restart**: If the graph is not fully connected, we restart DFS from an unmarked vertex until all vertices are visited.

### Breadth-First Search (BFS)
BFS explores the graph in "layers." It finds the **shortest path** (in terms of number of edges) from a source vertex to all others.

**BFS Algorithm:**
1.  Initialize a queue with the source vertex `s` and mark `s`.
2.  While the queue is not empty:
	*   Remove the vertex `v` from the front of the queue.
	*   For each unmarked neighbor `n` of `v`:
		*   Mark `n`.
		*   Set `edgeTo[n] = v` and `distTo[n] = distTo[v] + 1`.
		*   Add `n` to the end of the queue.

**BFS Implementation (Java-style):**
```java
import java.util.*;  
  
public class BreadthFirstSearch {  
    private boolean[] marked;  
    private int[] edgeTo;  
    private int[] distTo;  
    private final int source;  
  
    public BreadthFirstSearch(Graph graph, int source) {  
        validateVertex(graph, source);  
  
        marked = new boolean[graph.V()];  
        edgeTo = new int[graph.V()];  
        distTo = new int[graph.V()];  
        this.source = source;  
  
        // 初始化 edgeTo，使用 -1 表示未访问  
        for (int i = 0; i < edgeTo.length; i++) {  
            edgeTo[i] = -1;  
            distTo[i] = -1;  
        }  
  
        bfs(graph, source);  
    }  
  
    private void bfs(Graph graph, int start) {  
        Queue<Integer> queue = new LinkedList<>();  
        marked[start] = true;  
        distTo[start] = 0;  
        queue.offer(start);  
        while (!queue.isEmpty()) {  
            int v = queue.poll();  
            for (int w : graph.adj(v)) {  
                if (!marked[w]) {  
                    marked[w] = true;  
                    edgeTo[w] = v;  
                    distTo[w] = distTo[v] + 1;  
                    queue.offer(w);  
                }  
            }  
        }  
    }  
  
    public boolean hasPathTo(int v) {  
        validateVertex(v);  
        return marked[v];  
    }  
  
    public int distTo(int v) {  
        validateVertex(v);  
        return distTo[v];  
    }  
  
    public Iterable<Integer> pathTo(int v) {  
        validateVertex(v);  
        if (!hasPathTo(v)) return null;  
        Stack<Integer> path = new Stack<>();  
        for (int x = v; x != source; x = edgeTo[x]) {  
            path.push(x);  
        }  
        path.push(source);  
        return path;  
    }  
  
    private void validateVertex(Graph graph, int v) {  
        if (v < 0 || v >= graph.V()) {  
            throw new IllegalArgumentException(  
                    "Vertex " + v + " is not between 0 and " + (graph.V() - 1)  
            );  
        }  
    }  
  
    private void validateVertex(int v) {  
        if (v < 0 || v >= marked.length) {  
            throw new IllegalArgumentException(  
                    "Vertex " + v + " is not between 0 and " + (marked.length - 1)  
            );  
        }  
    }  
}
```


## 5. Graph Representations

### Common Graph API (Princeton)
```java
public class Graph {
    public Graph(int V);               // Create an empty graph with V vertices
    public void addEdge(int v, int w); // Add an edge v-w
    Iterable<Integer> adj(int v);      // Vertices adjacent to v
    int V();                           // Number of vertices
    int E();                           // Number of edges
    // ...
}
```
With this API, to find the degree (number of neighbors) of a vertex, you would write:
```java
public static int degree(Graph G, int v) {
    int degree = 0;
    for (int w : G.adj(v)) degree++;
    return degree;
}
```

### Representation 1: Adjacency Matrix
*   Use a `V` x `V` boolean matrix `M`.
*   `M[v][w] = true` if there is an edge from `v` to `w`.
*   **Space:** O (V²). Often inefficient for **sparse** graphs (graphs with far fewer than V² edges).
*   **Edge check:** O (1) to check if a specific edge exists.
*   **List neighbors:** O (V) to iterate over all neighbors of a vertex.
* ![[Pasted image 20260117234702.png]]

### Representation 2: Edge Set
*   Store a collection (e.g., list, set) of all edges.
*   Each edge is stored as a pair of vertex identifiers `(v, w)`.
*   Simple but inefficient for most queries.

### Representation 3: Adjacency List **(Most Common)**
*   Maintain an array of size `V` (or a map from vertex id to a list).
*   The entry at index `v` points to a list (e.g., bag, linked list) of all vertices adjacent to `v`.
*   **Space:** O (V + E). Efficient for both sparse and dense graphs.
*   **Edge check:** O (degree (v)) to check for a specific edge from `v`.
*   **List neighbors:** O (degree (v)) to iterate over all neighbors of `v`.
![[Pasted image 20260117235738.png]] ![[Pasted image 20260117235745.png]]


