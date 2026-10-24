Title: Depth-First Search (DFS) Algorithm Explained | Codecademy
Source: https://www.codecademy.com/article/depth-first-search-dfs-algorithm

---

# Depth-First Search (DFS) Algorithm Explained

Depth-First Search (DFS) is one of the most fundamental algorithms in computer science, used for traversing or searching data structures such as trees and graphs. It explores as far as possible along one branch before backtracking, making it particularly useful for scenarios like pathfinding, solving puzzles, and detecting cycles.

Let’s start the discussion by understanding what Depth-First Search is and its key characteristics.

## What is Depth-First Search?

Depth-First Search is an algorithm used for searching tree data structures for a particular node or a node with a particular value associated with it. It is also more generally used as a tree traversal algorithm, specifying an order in which to exhaustively access all nodes of a tree.

The algorithm begins at the root node and explores deeper into the tree until it reaches a leaf node. Then, it backtracks up the tree until it finds an unexplored child node. This process continues until the desired node is found or all nodes have been explored.

Key characteristics:

- Recursive nature: The natural recursive structure of DFS makes it easier to implement, but for very deep graphs, recursion can lead to stack overflow unless converted to an iterative approach.

- Memory usage: DFS generally requires less memory than BFS (Breadth-First Search) because it only stores the path it’s currently exploring, not all nodes at the current level.

- Deterministic traversal: For a given starting point and adjacency ordering, DFS will always produce the same traversal order, making it predictable for testing and debugging.

- Risk of infinite loops: If the graph has cycles and we don’t mark visited nodes, DFS can get stuck in an infinite loop. Hence, maintaining a visited set or array is crucial.

Here is a visual representation of the Depth-First Search algorithm:

Next, let’s explore how Depth First Search works in detail.

## How Depth-First Search works

There are two strategies for implementing Depth-First Search:

- Recursive implementation

- Iterative implementation

Let’s go through them one by one.

### Recursive implementation

The recursive version of the algorithm works by starting at the root node and breaking the tree up into subtrees, until it finds the target node, or until every node in the tree has been considered as the root of a subtree. We recursively call the function on all of our root’s children, treating each child node as a root of its own subtree.

We define a function that accepts a tree node and a target value as input parameters. The recursive DFS algorithm implements the following logic:

- If the input node value matches our target value, then return the input node.

- For each child of the input node, recursively call this function and return the first non-null value returned by a recursive call.

- If this root node has no children, or the recursive calls did not return any node, then return null.

To search a tree with this function, we invoke the function with the root node of our tree.

### Iterative implementation

The iterative algorithm does not make use of any recursive calls. Instead, we maintain a stack of references to unexplored siblings of the nodes we have already accessed. The recursive algorithm is effectively doing something very similar, but the program call stack is implicitly used to store the path from the root to the current node.

With the iterative algorithm, we need to implement a stack ourselves. These two implementations have the same time and space complexity, so the choice of which to implement is usually a matter of personal preference.

Let’s now have a look at the pseudocode for Depth-First Search.

## Depth-First Search pseudocode

Here is the pseudocode for the recursive implementation of Depth-First Search:

```
DFS(node): 
    if node is not visited: 
        mark node as visited 
        for each neighbor in node's adjacency list: 
            if neighbor is not visited: 
                DFS(neighbor) 
```

On the other hand, here is the pseudocode for the iterative implementation of Depth-First Search:

```
DFS_iterative(start): 
    create an empty stack 
    push start node onto stack 
    create an empty set for visited nodes 

    while stack is not empty: 
        node = pop from stack 
        if node is not visited: 
            mark node as visited 
            process node (e.g., print) 
            for each neighbor in node's adjacency list (in reverse order if needed): 
                if neighbor is not visited: 
                    push neighbor onto stack 
```

Now, we’ll learn how to implement Depth-First Search both recursively and iteratively in Python.

## Depth-First Search Python implementation

Here is the recursive implementation of Depth-First Search in Python:

```
def dfs(graph, start, visited=None): 
    if visited is None: 
        visited = set() 

    visited.add(start) 
    print(start, end=" ")  # Process the node 

    for neighbor in graph[start]: 
        if neighbor not in visited: 
            dfs(graph, neighbor, visited) 

# Example graph (Adjacency List) 
graph = { 
    'A': ['B', 'C'], 
    'B': ['D', 'E'], 
    'C': ['F'], 
    'D': [], 
    'E': ['F'], 
    'F': [] 
} 

# Run DFS 
dfs(graph, 'A') 

```

The output is:

```
A B D E F C 

```

On the other hand, here is the iterative implementation of Depth-First Search in Python:

```
def dfs_iterative(graph, start): 
    visited = set() 
    stack = [start] 

    while stack: 
        node = stack.pop() 
        if node not in visited: 
            print(node, end=" ") 
            visited.add(node) 
            # Reverse for consistent order with recursion 
            stack.extend(reversed(graph[node])) 

# Example usage 
graph = { 
    'A': ['B', 'C'], 
    'B': ['D', 'E'], 
    'C': ['F'], 
    'D': [], 
    'E': ['F'], 
    'F': [] 
} 

dfs_iterative(graph, 'A') 

```

The output is:

```
A B D E F C 

```

The next thing that we’ll discuss is the time and space complexity of Depth-First Search.

## Time and space complexity of Depth-First Search

Depth-First Search has a time complexity of O(n) where n is the number of nodes in the tree. In the worst case, we will examine every node of a tree.

Depth-First Search has a space complexity of O(n) where n is the number of nodes in the tree. In the worst case, we will need to store a reference to every node in a stack. Consider an adversarial example of a linked list as a type of tree with no branching. Trees like this could reach the worst-case space complexity if the target node is the leaf node or is absent from the tree altogether.

Lastly, we’ll take a look at the applications of Depth-First Search.

## Applications of Depth-First Search

Depth-First Search is widely used in:

- Pathfinding (e.g., maze solving)

- Cycle detection in graphs

- Topological sorting

- Finding connected components

- Artificial Intelligence (game tree exploration)

- Solving puzzles like Sudoku, N-Queens

## Conclusion

In this tutorial, we had a detailed discussion on Depth-First Search, covering what it is, its key characteristics, and how it works. Then, we went through its pseudocode and Python implementation for both the recursive and iterative strategies. Lastly, we had a look at the time complexity, space complexity, and applications of Breadth-First Search.

Depth-First Search is a powerful and intuitive algorithm for traversing trees and graphs. Its recursive nature makes it simple to implement, and its deep exploration strategy makes it suitable for a wide range of applications, from problem-solving to AI pathfinding.

If you want to learn more about implementing search algorithms in Python, check out the How to Implement Search Algorithms with Python course on Codecademy.

## Frequently asked questions

### 1. What is DFS and BFS?

DFS (Depth-First Search) explores as far as possible along one branch before backtracking, while BFS (Breadth-First Search) explores all neighbors at the current depth before moving deeper.

### 2. What are the three types of DFS?

The three types of Depth-First Search are pre-order, in-order, and post-order traversals.

### 3. What is a DFS used for?

Depth-First Search is used for pathfinding, cycle detection, solving puzzles, topological sorting, and exploring graph connectivity.

### 4. Which is faster DFS or BFS?

In terms of time complexity, both Depth-First Search and Breadth-First Search are equal. Speed depends on the problem—DFS may find solutions faster in deep search spaces, while BFS may be quicker for shortest-path problems.

### 5. Which uses more memory, BFS or DFS?

Typically, Breadth-First Search uses more memory because it stores all nodes at the current level, while Depth-First Search only stores nodes along the current path.

Codecademy Team

'The Codecademy Team, composed of experienced educators and tech experts, is dedicated to making tech skills accessible to all. We empower learners worldwide with expert-reviewed content that develops and enhances the technical skills needed to advance and succeed in their careers.'

Meet the full team
