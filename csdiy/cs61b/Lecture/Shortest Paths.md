Last time, use two ways to find paths in graph
- DFS and BFS

| Problem                | Solution | Efficiency (adj. list)             |
| :--------------------- | :------- | :--------------------------------- |
| **s-t paths**          | DFS      | $O(V+E)$ time<br>$\Theta(V)$ space |
| **s-t shortest paths** | BFS      | $O(V+E)$ time<br>$\Theta(V)$ space |

Space Efficiency. Is one more efficient than the other?

DFS is worse for spindly graphs.
• Call stack gets very deep.
• Computer needs O (V) memory to remember recursive calls (see CS 61 C).

BFS is worse for absurdly "bushy" graphs.
• Queue gets very large. In worst case, queue will require 0 (V) memory.
• Example: 1,000,000 vertices that are all connected. 999,999 will be enqueued at once.

Note: In our implementations, we have to spend O (V) memory anyway to track distTo and edgeTo arrays.

• Can optimize by storing distTo and edgeTo in a map instead of an array.



when we handle a question that edge has weight, BFS is not good for it does not consider the edge weights
BFS will yield a route of length 330 m instead of therefore we need an algorithm that takes into account edge distances, also known as “edge weights”.
![[Pasted image 20260124153750.png]] ![[Pasted image 20260124153801.png]]


Goal: Find the shortest paths form source vertex s to every other vertex.
Observaton: Soluton will always be a tree

Some bad Algrithms
1. like BFS
Add the start (A) to the fringe.
While fringe is not empty:
Remove a vertex from the fringe and mark it.
For each outgoing edge v→w: if w is not already part of SPT, add the edge, and add w to fringe.
![[Pasted image 20260124154043.png]]
why it is bad
edges are not equal. when we mark a vertex, we can not find another path to that vertex, but that might be the shorter one.
The edge B→A is not added to SPT, because A is already part of the SPT.

2. Dummy nodes
Create a new graph by adding a bunch of dummy nodes every init along an edge, then run breadth-first search.

• When we hit one of our original nodes, add edge to the SPT.
![[Pasted image 20260124154213.png]]
why it is bad
a graph has big weight

3. Best-First Search
Add the start (A) to the fringe.
While fringe is not empty:
     Remove the closest vertex from the fringe and mark it.
     For each outgoing edge v→w: if w is not already part of SPT,  add the edge, and add w to fringe.
![[Pasted image 20260124155014.png]]
we still get the wrong answer, beacause we already add A->B to fringe ,so C->B does not consider.
the right thing: add edge C->B, and thrown out edge A->B

Dijkstra's Algorithm
Add all vertices to the fringe. 
     Remove the closest vertex from the fringe and mark it.
     For each outgoing edge v→w: if the edge gives a better distance to w,  
    add the edge, and update w in the fringe.

implement tips:
Because we choose the closest vertex everytime, we can use the PQ to implement fringe
use distTo, edgeTo array, firnge queue


Dijkstra’s:
- PQ.add(source, 0)
- For other vertices v, PQ.add(v, infinity)
- While PQ is not empty:
- p = PQ.removeSmallest()
- Relax all edges from p
Relaxing an edge p → q with weight w:
- If distTo[p] + w < distTo[q]:
- distTo[q] = distTo[p] + w
- edgeTo[q] = p    
- PQ.changePriority(q, distTo[q])

when weight is negative number, Dijkstra's Algorithm fail

Runtime Analysis
when we relax a edge, we change the priority of Fringe

|                       | Operaritons | Cost per operation | Total cost |
| :-------------------- | :---------- | :----------------- | ---------- |
| **PQ add**            | V           | $O(logV)$          | $O(VlogV)$ |
| **PQ removeSmallest** | V           | $O(logV)$          | $O(VlogV)$ |
| PQ changePriority     | E           | $O(logV)$          | $O(ElogV)$ |

assume E > V, runtime $O(ElogV)$

Is this a good algorithm for a navigation application?
how we find the SP from Denver to NYC with Dijkstra’s
Dijkstra’s will explore every place within nearly two thousand miles of Denver before it locates NYC.
we only care about the **single target** NYC

A* Algorithm
add a penalty to nodes far away from target
- Visit vertices in order of d(Denver, v) + h(v, goal), where h(v, goal) is an estimate of the distance from v to our goal NYC.
- the penalty h (v, goal) is Prior 

if we want to find a way from A to B, but not through C, we can penalty h (C, B) infinity