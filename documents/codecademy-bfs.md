Title: Breadth-First Search (BFS) Algorithm Explained | Codecademy
Source: https://www.codecademy.com/article/breadth-first-search-bfs-algorithm

---

# Breadth-First Search (BFS) Algorithm Explained

When working with graphs and trees, one of the most fundamental algorithms we use to explore nodes systematically is the breadth-first search (BFS) algorithm. It’s widely applied in computer science for finding the shortest path, web crawling, and even artificial intelligence (AI).

In this guide, we’ll explore what breadth-first search is, how it works, how to implement it programmatically, how it compares with depth-first search (DFS), and more.

Let’s start the discussion with a brief overview of breadth-first search.

## What is breadth-first search?

Breadth-first search is a popular graph traversal algorithm that explores all nodes at the present depth before proceeding to nodes at the next level of depth. In simpler terms, BFS visits neighbors first, then their neighbors, and so on.

BFS works on both graphs and trees. In graphs, it’s particularly useful for finding the shortest path in an unweighted graph. The algorithm uses a queue to track which vertex to visit next.

Now that we understand what breadth-first search is, let’s break down how it actually works step-by-step.

## How breadth-first search works

The breadth-first search algorithm works by exploring all neighboring nodes before moving to nodes at the next level of depth. It starts from a chosen source node and visits all nodes directly connected to it, then proceeds level by level until all reachable nodes have been explored. This ensures that nodes are visited in order of their distance from the source.

Let’s go through a step-by-step breakdown of how breadth-first search operates:

Step 1. Start from the source node: Choose a starting node to begin traversal.

Step 2. Mark the source as visited: Keep a record of visited nodes to avoid repetition or loops.

Step 3. Enqueue the source node: Use a queue (FIFO structure) to store nodes to be explored.

Step 4. Process the queue: BFS dequeues a node, visits its unvisited neighbors, marks them visited, and enqueues them.

Step 5. Move level by level: Continue until the queue is empty, visiting all nodes layer by layer.

This systematic, level-based approach ensures that BFS finds the shortest route from the source to any other node in an unweighted graph.

Here is a visual example that demonstrates how breadth-first search works:

Next, we’ll explore the pseudocode for implementing breadth-first search.

## BFS algorithm pseudocode

The pseudocode for the breadth-first search algorithm outlines the logical steps of the traversal process. It shows how we use a queue to explore nodes level by level, marking each as visited to avoid repetition. This simple structure forms the foundation for implementing BFS in any programming language:

```
BFS(Graph, start_node): 
    create a queue Q 
    mark start_node as visited 
    enqueue start_node into Q 
     
    while Q is not empty: 
        current_node = dequeue(Q) 
        for each neighbor of current_node: 
            if neighbor is not visited: 
                mark neighbor as visited 
                enqueue neighbor into Q 
```

Now, let’s translate this pseudocode into a working Python implementation.

## BFS Python implementation

Here is an example that implements the breadth-first search algorithm in Python:

```
from collections import deque 
 
def bfs(graph, start): 
    visited = set() 
    queue = deque([start]) 
 
    while queue: 
        node = queue.popleft() 
        if node not in visited: 
            print(node, end=" ") 
            visited.add(node) 
            for neighbor in graph[node]: 
                if neighbor not in visited: 
                    queue.append(neighbor) 
 
# An example graph represented as an adjacency list 
graph = { 
    'A': ['B', 'C'], 
    'B': ['D', 'E'], 
    'C': ['F'], 
    'D': [], 
    'E': ['F'], 
    'F': [] 
} 
 
bfs(graph, 'A') 

```

This BFS implementation shows how to initialize a queue, track visited nodes using a list or set, and iterate through each node’s neighbors, allowing us to traverse a graph efficiently and find shortest paths in unweighted graphs.

The output will be:

```
A B C D E F 

```

This output shows BFS traversing level by level — first exploring all neighbors of A, then their neighbors, and so on.

With the Python implementation covered, let’s analyze the time and space complexity of the breadth-first search algorithm.

## Breadth-first search time and space complexity

The time complexity of BFS algorithm depends on the number of nodes and edges in the graph. In the worst case, BFS visits every node and examines every edge once. For a graph having V vertices and E edges, the time complexity is O(V + E). This linear relationship makes BFS efficient for both sparse and dense graphs, ensuring that all reachable nodes are processed systematically.

In terms of space complexity, BFS requires additional memory to keep track of visited nodes and to store nodes in the queue. In the worst case, the queue may contain all nodes at a given level, which can be proportional to the number of vertices. Therefore, the space complexity of BFS is O(V).

In the next section, we’ll compare breadth-first search with another popular graph traversal algorithm, depth-first search (DFS).

## Breadth-first search vs depth-first search

When comparing breadth-first search and depth-first search, the main difference lies in how they explore nodes within a graph or tree. BFS explores nodes level by level, while DFS dives deep into one branch first. BFS uses a queue, ensuring the shortest path in unweighted graphs but with higher memory usage, whereas DFS uses a stack or recursion, consumes less memory, and doesn’t guarantee the shortest path. In essence, BFS explores broadly, while DFS dives deeply.

To learn more about the differences between breadth-first search and depth-first search, check out the Breadth-First Search vs Depth-First Search: Key Differences article on Codecademy.

Finally, let’s discover the real-world applications of breadth-first search.

## Real-world applications of breadth-first search

The breadth-first search algorithm is widely used across various domains:

- Shortest path finding: Used in unweighted graphs like road maps or network routing.

- Web crawlers: Search engines use BFS to crawl websites level by level.

- Social networks: Helps find degrees of connection (e.g., “friends of friends”).

- AI and robotics: BFS aids in state-space search and pathfinding.

These practical applications demonstrate BFS’s versatility and reliability in problem-solving.

## Conclusion

In this guide, we’ve explored the breadth-first search algorithm in detail, covering what it is, how it works, its pseudocode, and Python implementation. We also analyzed its time and space complexity, compared it with depth-first search, and highlighted its practical applications.

The breadth-first search algorithm is one of the most essential tools in computer science. By exploring nodes level by level using a queue, BFS guarantees complete and systematic traversal. Its efficiency, simplicity, and reliability make it a go-to approach for graph problems, AI pathfinding, and network applications.

If you want to learn more about implementing search algorithms in Python, check out the How to Implement Search Algorithms with Python course on Codecademy.

## Frequently asked questions

### 1. Why do we use the BFS algorithm?

We use breadth-first search (BFS) to explore nodes in the shortest possible way, making it ideal for identifying the shortest path in unweighted graphs.

### 2. Is BFS used in AI?

Yes. In artificial intelligence (AI), breadth-first search is used in search strategies to explore all possible states or actions systematically.

### 3. Does BFS use stack or queue?

The breadth-first search algorithm uses a queue to keep track of nodes to be explored, ensuring that nodes are visited level by level in the order they were discovered.

### 4. When should you use breadth-first search?

We should use breadth-first search when we need to find the shortest path, explore all neighbors equally, or ensure complete traversal in level order.

### 5. What’s the difference between breadth-first search and Dijkstra’s algorithm?

While breadth-first search works on unweighted graphs, Dijkstra’s algorithm is used for weighted graphs where edge costs vary. BFS can be seen as a simplified version of Dijkstra’s algorithm with equal weights.
