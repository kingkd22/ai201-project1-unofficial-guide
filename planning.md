# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

**Solving data structures and algorithms (DSA) problems in code.** This guide covers the practical side of DSA: problem-solving patterns (two pointers, sliding window, fast & slow pointers, modified binary search, BFS/DFS, dynamic programming), step-by-step walkthroughs, and working implementations with their time and space complexity. DSA is a huge, broad topic, and official material (textbooks, language docs, lecture notes) mostly explains *what* a structure or algorithm is, not *how to recognize which technique a problem needs or how to turn it into code*. That practical know-how is scattered across tutorial sites, blogs and GitHub study notes, which makes it hard to find and compare. This system puts it in one searchable place.

**Example questions the system should answer:** "After the fast and slow pointers meet, how do I find where the cycle starts?", "How do I modify binary search to find the ceiling of a number?", "Why doesn't Dijkstra's algorithm work with negative edges, and what should I use instead?", "What's the difference between memoization and tabulation?", "Which uses more memory, BFS or DFS?"

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

All documents are downloaded and cleaned by `fetch_sources.py` into `documents/` (86 files, ~2.9M characters). Each file starts with a `Title:` / `Source:` header so the source URL can be cited later.

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | W3Schools DSA tutorial (59 pages) | Full reference tutorial: arrays, sorting, searching, linked lists, stacks/queues, hash tables, trees, graphs (Dijkstra, Bellman-Ford, MST, max flow), time complexity, DP/greedy. Each page has explanation → manual run-through → Python code → complexity. | https://www.w3schools.com/dsa/ → `documents/w3schools-*.md` |
| 2 | "Several Coding Patterns" GitHub repo (README + 16 pattern files) | Interview pattern notes (Grokking-style): sliding window, two pointers, fast & slow pointers, merge intervals, cyclic sort, tree BFS/DFS, two heaps, subsets, modified binary search, XOR, top-K, k-way merge, 0/1 knapsack DP, topological sort. Problem statement → approach → JS code → complexity. | https://github.com/Chanda-Abdul/Several-Coding-Patterns-for-Solving-Data-Structures-and-Algorithms-Problems-during-Interviews → `documents/github-patterns-*.md` |
| 3 | Tech Interview Handbook: Array cheatsheet | Interview-focused cheatsheet: array time complexities, corner cases, techniques (sliding window, two pointers, precomputation, index as hash key), essential practice questions. | https://www.techinterviewhandbook.org/algorithms/array/ |
| 4 | GeeksforGeeks: Big O analysis | Big O definition, properties, common complexity classes with code examples. | https://www.geeksforgeeks.org/dsa/analysis-algorithms-big-o-analysis/ |
| 5 | GeeksforGeeks: Two pointers technique | When to use two pointers, the sorted two-sum walkthrough, and a correctness argument. | https://www.geeksforgeeks.org/dsa/two-pointers-technique/ |
| 6 | Built In: Sliding window algorithm | Concept explanation plus 12 worked problems with Python solutions and an FAQ. | https://builtin.com/data-science/sliding-window-algorithm |
| 7 | GeeksforGeeks: Why Floyd's fast/slow pointers work | Mathematical proof of cycle detection and how to find the cycle's start node. | https://www.geeksforgeeks.org/dsa/how-does-floyds-slow-and-fast-pointers-approach-work/ |
| 8 | GeeksforGeeks: N-base modified binary search | An alternative binary search formulation using powers of the base. | https://www.geeksforgeeks.org/dsa/n-base-modified-binary-search-algorithm/ |
| 9 | Codecademy: Depth-first search | DFS concept, recursive and iterative Python implementations, complexity, applications, FAQ. | https://www.codecademy.com/article/depth-first-search-dfs-algorithm |
| 10 | Codecademy: Breadth-first search | BFS concept, queue-based Python implementation, complexity, applications, FAQ. | https://www.codecademy.com/article/breadth-first-search-bfs-algorithm |
| 11 | Stack Overflow Blog: Beginner's guide to dynamic programming | DP as "a way of thinking", memoization illustrated with Fibonacci. | https://stackoverflow.blog/2022/01/31/the-complete-beginners-guide-to-dynamic-programming/ |
| 12 | Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python* (Wiley, 2013) | Full 770-page textbook (PDF, text extracted with pdfplumber). **Local only.** It is copyrighted, so it's gitignored and never committed; run `fetch_sources.py` to rebuild it. | https://nibmehub.com/opac-service/pdf/read/Data%20Structures%20and%20Algorithms%20in%20Python.pdf → `documents/textbook-goodrich-dsa-in-python.md` |


---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | In Floyd's fast and slow pointer algorithm, once the two pointers meet inside the loop, how do you find the node where the cycle starts, and what are the time and space complexities? | Reset one pointer (e.g. slow) to the head of the list, leave the other at the meeting point, then move **both one node at a time**. The node where they meet again is the start of the cycle. O(n) time, O(1) space. *(GfG Floyd article; GitHub Pattern 03)* |
| 2 | How do you modify binary search to find the ceiling of a key in a sorted array (smallest element ≥ key)? | If the key is greater than the last (largest) element, return -1. Otherwise run normal binary search: if `arr[middle] == key`, return that index. If the loop ends without finding it, `start` points to the smallest element greater than the key, so return `start`. *(GitHub Pattern 11)* |
| 3 | Why can't Dijkstra's algorithm be used on graphs with negative edge weights, what should you use instead, and what happens if the graph has a negative cycle? | W3Schools states Dijkstra's algorithm does not work for graphs with negative edges; use **Bellman-Ford** instead. With a negative cycle there is no shortest path (you can always go one more round and get a shorter path), but Bellman-Ford can be implemented to detect and report negative cycles. *(W3Schools Dijkstra + Bellman-Ford pages)* |
| 4 | What is the difference between memoization and tabulation in dynamic programming? | Memoization is **top-down**: a recursive function starts at the main problem, breaks it into smaller subproblems, and stores results so they aren't recomputed. Tabulation is **bottom-up** and not recursive: it fills a table starting with the most basic subproblems (e.g. F(0), F(1)) and builds up to the final answer. *(W3Schools memoization/tabulation/DP pages; SO blog)* |
| 5 | Which uses more memory, BFS or DFS, and why? Is one faster? | BFS typically uses more memory because it stores all nodes at the current level (in its queue). DFS only stores nodes along the current path. Their time complexity is the same; which finishes first depends on the problem (DFS for deep search spaces, BFS for shortest-path problems). *(Codecademy DFS/BFS FAQs)* |

These are deliberately spread across different sources and formats: a proof-style article (Q1), a code-heavy JS pattern file (Q2), an answer that combines two pages (Q3), a concept answer repeated across several sources (Q4), and a short FAQ answer (Q5). Q2 and Q3 are the most likely to fail. Q2's answer is split between prose and a code block, and Q3 needs chunks from two different pages.

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
