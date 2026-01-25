## 1. Basic Graph Search Methods

### DFS (Depth-First Search)
- **Purpose**: Find any path from source to target
- **Efficiency**: $O(V+E)$ time, $\Theta(V)$ space (adjacency list)
- **Best for**: Checking connectivity, topological ordering
- **Worst case**: Spindly graphs (deep recursion stack)

### BFS (Breadth-First Search)
- **Purpose**: Find shortest path in unweighted graphs
- **Efficiency**: $O(V+E)$ time, $\Theta(V)$ space (adjacency list)
- **Best for**: Unweighted graphs, level-order traversal
- **Worst case**: "Bushy" graphs (large queue)

## 2. The Weighted Graph Problem

**Problem**: BFS fails with weighted edges because it doesn't consider edge weights.

**Example**: BFS might choose a 330 m route when a 150 m route exists, simply because the 330 m route has fewer edges.
![[Pasted image 20260124153750.png]] ![[Pasted image 20260124153801.png]]

**Goal**: Find shortest paths from source vertex s to every other vertex in weighted directed graphs.
**Observaton**: Soluton will always be a tree

## 3. Failed Approaches

### 3.1 Naive BFS Extension
```python
Add start to fringe
While fringe not empty:
    Remove vertex from fringe and mark it
    For each outgoing edge v→w:
        If w not in SPT, add edge and add w to fringe
```
**Problem**: Once a vertex is marked, we can't find a better (shorter) path to it.

### 3.2 Dummy Nodes
- Convert weighted edges to multiple unit edges
- Run BFS on expanded graph
![[Pasted image 20260124154213.png]]

**Problem**: Explodes graph size with large weights, impractical memory usage.

### 3.3 Best-First Search
```python
Add start to fringe
While fringe not empty:
    Remove CLOSEST vertex from fringe and mark it
    For each outgoing edge v→w:
        If w not in SPT, add edge and add w to fringe
```
**Problem**: Still greedy - may not update vertices when better paths are found.

## 4. Dijkstra's Algorithm

### Core Idea
Always expand the vertex with the smallest known distance from source, updating neighbors if better paths are found.

### Algorithm Steps
```
1. Add all vertices to priority queue (fringe) with distance ∞
2. Set source distance to 0
3. While PQ not empty:
    p = PQ.removeSmallest()
    For each edge p→q with weight w:
        If distTo[p] + w < distTo[q]:
            Update distTo[q] = distTo[p] + w
            Update edgeTo[q] = p
            PQ.changePriority(q, distTo[q])
```

### Implementation Details

**Data Structures**:
- `distTo[v]`: shortest known distance from source to v
- `edgeTo[v]`: last edge on shortest path to v
- Priority Queue: stores vertices ordered by current best distance

**Edge Weighted Digraph Implementation**:
```java
public class EdgeWeightedDigraph {
    private List<DirectedEdge>[] adj;
    private List<DirectedEdge> edges;
    
    public void addEdge(DirectedEdge e) {
        // Validate vertices and weight
        if (!hasEdge(e.from(), e.to())) {
            adj[e.from()].add(e);
            edges.add(e);
        }
    }
}
```

**Dijkstra Implementation**:
```java
public class DijkstraSP {
    private double[] distTo;
    private DirectedEdge[] edgeTo;
    private IndexMinPQ<Double> pq;
    
    public DijkstraSP(EdgeWeightedDigraph graph, int source) {
        // Initialize all distances to infinity
        distTo = new double[graph.V()];
        for (int i = 0; i < graph.V(); i++) {
            distTo[i] = Double.POSITIVE_INFINITY;
        }
        distTo[source] = 0.0;
        
        // Process vertices in priority order
        while (!pq.isEmpty()) {
            int v = pq.delMin();
            for (DirectedEdge e : graph.adj(v)) {
                relax(e);
            }
        }
    }
    
    private void relax(DirectedEdge e) {  
	    int from = e.from();  
	    int to = e.to();  
	    if (distTo[from] + e.weight() < distTo[to]) {  
	            distTo[to] = distTo[from] + e.weight();  
	            edgeTo[to] = e;  
	            pq.changeKey(to, distTo[to]);  
	    }  
	}
}
```

### Runtime Analysis

|                       | Operaritons | Cost per operation | Total cost |
| :-------------------- | :---------- | :----------------- | ---------- |
| **PQ add**            | V           | $O(logV)$          | $O(VlogV)$ |
| **PQ removeSmallest** | V           | $O(logV)$          | $O(VlogV)$ |
| **PQ changePriority** | E           | $O(logV)$          | $O(ElogV)$ |

**Overall**: O (E log V) assuming E > V

### Early Termination Optimization
For single-target queries, stop when target vertex is removed from PQ:
```java
while (!pq.isEmpty()) {
    int v = pq.delMin();
    if (v == target) break;  // Early exit
    // ... relax edges
}
```

### Limitations
- **Negative weights**: Dijkstra fails with negative edge weights
- **Single-source focus**: Explores many irrelevant vertices for single-target queries

## 5. A* Algorithm

### Motivation
Dijkstra explores all directions equally. A* biases search toward the target using a heuristic.

### Algorithm
```
f(v) = g(v) + h(v, goal)
where:
  g(v) = actual distance from source to v
  h(v, goal) = heuristic estimate from v to goal
```

**Properties**:
- If h (v) is admissible (never overestimates), A* finds optimal path
- If h (v) is consistent, vertices are processed at most once

### Implementation
```java
public class AStarSP {
    private final ToDoubleFunction<Integer> heuristic;
    
    private void relax(DirectedEdge e) {
        // Similar to Dijkstra but with heuristic
        double newPriority = distTo[to] + heuristic.applyAsDouble(to);
        pq.changeKey(to, newPriority);
    }
}
```

### Heuristic Examples
- **Euclidean distance**: Straight-line distance in spatial graphs
- **Manhattan distance**: Grid-based navigation
- **Penalty functions**: Avoid certain areas by setting h (v) = ∞

## 6. Practical Considerations

### Memory Optimization
- Use maps instead of arrays for `distTo` and `edgeTo` when graph is sparse
- Consider bidirectional search for very large graphs

### Real-World Applications
- Navigation systems (Google Maps, GPS)
- Network routing protocols
- Game AI pathfinding
- Logistics and supply chain optimization