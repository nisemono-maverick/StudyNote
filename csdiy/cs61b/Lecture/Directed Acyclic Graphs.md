## Overview
A Directed Acyclic Graph (DAG) is a directed graph with no cycles. DAGs are fundamental in many applications including task scheduling, dependency resolution, and data processing pipelines.

## Topological Sort
A topological ordering of a directed graph is a linear ordering of its vertices such that for every directed edge `(u, v)`, vertex `u` comes before vertex `v` in the ordering.

**Key Property:** A topological sort only exists if the graph is a DAG.

### Visual Representation
When vertices are arranged in topological order, all edges point from left to right (forward direction).

### Applications
- Task scheduling with prerequisites
- Dependency resolution in build systems
- Course prerequisite chains
- Event sequencing

## Algorithms for Topological Sort

### 1. DFS Postorder Method
```java
// Using DFS to get topological order
public void dfsTopological(EdgeWeightedDigraph graph, int v) {
    marked[v] = true;
    for (DirectedEdge edge : graph.adj(v)) {
        int to = edge.to();
        if (!marked[to]) {
            dfsTopological(graph, to);
        }
    }
    topologicalOrder.push(v); // Postorder: add after visiting all neighbors
}
```
**Steps:**
1. Perform DFS from vertices with no incoming edges
2. Add vertices to stack in postorder (after processing all descendants)
3. Reverse the stack to get topological order

### 2. Kahn's Algorithm (Indegree-based)
```java
public void kahn(EdgeWeightedDigraph graph) {
    List<Integer> indegree = new ArrayList<>();
    Queue<Integer> queue = new LinkedList<>();
    
    // Calculate indegree for each vertex
    for (int v = 0; v < graph.V(); v++) {
        indegree.add(v, graph.indegree(v));
        if (graph.indegree(v) == 0) queue.add(v);
    }
    
    int visitedCount = 0;
    while (!queue.isEmpty()) {
        visitedCount++;
        int v = queue.poll();
        topologicalSort.add(v);
        
        // Reduce indegree of neighbors
        for (DirectedEdge edge : graph.adj(v)) {
            indegree.set(edge.to(), indegree.get(edge.to()) - 1);
            if (indegree.get(edge.to()) == 0) queue.offer(edge.to());
        }
    }
    
    // Check for cycles
    if (visitedCount != graph.V()) {
        throw new IllegalArgumentException("Graph has a cycle");
    }
}
```
**Cycle Detection:** Kahn's algorithm naturally detects cycles - if not all vertices are visited, a cycle exists.

## Shortest Path on DAG
Unlike general graphs, DAGs allow efficient shortest path computation even with negative edge weights (where Dijkstra fails).

### Algorithm
```java
public DAGSP(EdgeWeightedDigraph graph) {
    // Initialize distances to infinity
    for (int i = 0; i < graph.V(); i++) {
        distTo[i] = Double.POSITIVE_INFINITY;
    }
    
    // Get topological order
    topologicalSort = getTopologicalOrder(graph);
    
    // Start from first vertex in topological order
    distTo[topologicalSort.get(0)] = 0.0;
    
    // Process vertices in topological order
    for (Integer v : topologicalSort) {
        // Relax all outgoing edges
        for (DirectedEdge edge : graph.adj(v)) {
            int to = edge.to();
            if (distTo[v] + edge.weight() < distTo[to]) {
                distTo[to] = distTo[v] + edge.weight();
                edgeTo[to] = edge;
            }
        }
    }
}
```

**Time Complexity:** O (V + E) - linear time!

**Why it works:**
- Processing vertices in topological order ensures that when we relax an edge `(u, v)`, we have already found the shortest path to `u`
- No need for priority queues or complex relaxation schemes

## Longest Path on DAG
For general graphs, the Longest Path Problem is NP-hard. However, for DAGs it can be solved efficiently through reduction.

### Solution by Reduction
1. Multiply all edge weights by -1
2. Find shortest path on the transformed graph
3. Multiply resulting path length by -1 to get longest path

```java
public double longestPath(EdgeWeightedDigraph graph, int source, int target) {
    // Create a copy of the graph with negated weights
    EdgeWeightedDigraph negatedGraph = negateWeights(graph);
    
    // Find shortest path on negated graph
    DAGSP shortestPathFinder = new DAGSP(negatedGraph);
    
    // Negate the result to get longest path
    return -shortestPathFinder.distTo(target);
}
```

**Limitation:** This approach only works because DAGs have no cycles, preventing infinite loops with negative weights.

## Reduction Technique
The longest path solution demonstrates a **reduction** - transforming one problem into another:

1. **Original Problem:** Find longest path in DAG
2. **Reduction:** Transform graph by negating weights
3. **Solve Reduced Problem:** Find shortest path in transformed DAG
4. **Interpret Result:** Negate the answer to get longest path

Reduction is a fundamental problem-solving technique where we:
- Transform instance of problem A into instance of problem B
- Solve problem B using existing algorithm
- Transform solution of B back to solution of A

## Applications

### Real-World Use Cases
1. **Build Systems:** Determining compilation order
2. **Package Managers:** Resolving dependency chains
3. **Course Scheduling:** Prerequisite sequencing
4. **PERT Charts:** Project scheduling and critical path method
5. **Data Processing:** Pipeline stage ordering

### Example: Task Scheduling
```
Tasks: A, B, C, D, E
Dependencies: A→B, A→C, B→D, C→D, D→E
Topological Order: A, B, C, D, E (or A, C, B, D, E)
```
