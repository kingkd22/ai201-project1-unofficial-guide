# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

**Solving data structures and algorithms (DSA) problems in code.** This guide makes the practical side of DSA searchable: problem-solving patterns (two pointers, sliding window, fast & slow pointers, modified binary search, BFS/DFS, dynamic programming), step-by-step walkthroughs, and working implementations with their time and space complexity. DSA is huge and broad, and official material (textbooks, language docs, lecture notes) mostly explains *what* a data structure or algorithm is. It rarely shows *how to recognize which technique a problem needs or how to turn it into working code*. That knowledge is scattered across tutorial sites, blogs and GitHub study notes, so it's hard to find and compare when you're stuck on a problem.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

All sources are downloaded and cleaned by `python fetch_sources.py` into `documents/` (86 files).

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | W3Schools DSA tutorial (59 content pages: sorting, searching, linked lists, stacks/queues, hash tables, trees, graphs, time complexity, DP/greedy) | Tutorial site | https://www.w3schools.com/dsa/ → `documents/w3schools-*.md` |
| 2 | "Several Coding Patterns for Solving DSA Problems during Interviews" (README + 16 pattern files, incl. Pattern 03 Fast & Slow Pointers and Pattern 11 Modified Binary Search) | GitHub study notes | https://github.com/Chanda-Abdul/Several-Coding-Patterns-for-Solving-Data-Structures-and-Algorithms-Problems-during-Interviews → `documents/github-patterns-*.md` |
| 3 | Tech Interview Handbook: Array cheatsheet for coding interviews | Interview guide | https://www.techinterviewhandbook.org/algorithms/array/ → `documents/techinterviewhandbook-array.md` |
| 4 | GeeksforGeeks: Big O Notation analysis | Tutorial article | https://www.geeksforgeeks.org/dsa/analysis-algorithms-big-o-analysis/ → `documents/gfg-big-o-analysis.md` |
| 5 | GeeksforGeeks: Two Pointers Technique | Tutorial article | https://www.geeksforgeeks.org/dsa/two-pointers-technique/ → `documents/gfg-two-pointers.md` |
| 6 | Built In: Sliding Window Algorithm Explained (12 worked problems) | Blog article | https://builtin.com/data-science/sliding-window-algorithm → `documents/builtin-sliding-window.md` |
| 7 | GeeksforGeeks: How does Floyd's slow and fast pointers approach work? | Proof / explanation | https://www.geeksforgeeks.org/dsa/how-does-floyds-slow-and-fast-pointers-approach-work/ → `documents/gfg-floyd-fast-slow-pointers.md` |
| 8 | GeeksforGeeks: N-Base modified binary search | Tutorial article | https://www.geeksforgeeks.org/dsa/n-base-modified-binary-search-algorithm/ → `documents/gfg-n-base-modified-binary-search.md` |
| 9 | Codecademy: Depth-First Search (DFS) Algorithm Explained | Tutorial article | https://www.codecademy.com/article/depth-first-search-dfs-algorithm → `documents/codecademy-dfs.md` |
| 10 | Codecademy: Breadth-First Search (BFS) Algorithm Explained | Tutorial article | https://www.codecademy.com/article/breadth-first-search-bfs-algorithm → `documents/codecademy-bfs.md` |
| 11 | Stack Overflow Blog: The complete beginner's guide to dynamic programming | Blog article | https://stackoverflow.blog/2022/01/31/the-complete-beginners-guide-to-dynamic-programming/ → `documents/stackoverflow-blog-dynamic-programming.md` |
| 12 | Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python* (Wiley, 2013) | Textbook (PDF) | https://nibmehub.com/opac-service/pdf/read/Data%20Structures%20and%20Algorithms%20in%20Python.pdf → `documents/textbook-goodrich-dsa-in-python.md` (**local only**: copyrighted, so gitignored and rebuilt by `fetch_sources.py`) |

The NeetCode "Big O Notation" lesson (https://neetcode.io/courses/lessons/big-o-notation) was on the original source list but was dropped. It's a JavaScript-rendered (likely video) lesson with no extractable text, and Big O is already covered by sources 1, 4 and 12.

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** About 1,500 characters (target), with a hard max of 2,000 characters of body text. I split on headings first and only break up sections that are too big. Final chunks have a median size of 1,514 characters.

**Overlap:** 200 characters, but only between chunks cut from the same long section (taken from the end of the previous prose block, cut at a word boundary). There's no overlap across headings, since a new heading is a new topic, and code is never repeated as overlap.

**Why these choices fit your documents:** My documents are long tutorials and pattern notes, not short reviews. Almost every section is one idea (one problem, one algorithm step, one FAQ answer) laid out as explanation → code → complexity. I measured the web/GitHub docs before picking the size: the median section is ~815 characters, 75% are under 1,740, and 90% of code blocks are under ~1,640. So ~1,500 characters usually keeps a whole explanation and its code together. The rules in `ingest.py`:
- Split each document on its Markdown headings (ignoring `#` lines inside code fences, which are code comments).
- Sections under 300 characters get merged into the next section, so I don't get fragments like a lone heading.
- A subsection stays with its parent when both fit in 1,500 characters (for example, a problem statement and its `#### Solution`).
- Long sections are packed block by block (paragraphs and code blocks) up to ~1,500 characters. Code blocks are never split unless one block alone is over 2,000 characters, in which case it's split at blank lines and each piece is re-wrapped in its own fence.
- A short leftover at the end of a section (like a lone "time complexity is O(n)" line) is folded back into the previous chunk.
- Every chunk starts with `Document title > Section heading`, so a chunk that's mostly code still matches a question about the concept. Each chunk also stores `doc_id`, `title`, `url`, `heading` and `chunk_index` as metadata for citations.

**Preprocessing (the ingestion pipeline):** `fetch_sources.py` downloads every source and cleans it before chunking:
- **HTML pages:** keeps only the main article element and removes nav, headers/footers, ads, share buttons, scripts, the interactive W3Schools widgets, Codecademy course cards and author bio, and "Related articles"/"Recommended courses" link lists. The rest is converted to Markdown that keeps headings, lists, tables and code blocks.
- **GitHub:** the raw Markdown is downloaded, with images and leftover HTML tags removed.
- **Textbook:** text is extracted with pdfplumber (`x_tolerance=1`, because the default glued words together). `ingest.py` then cuts the table of contents, bibliography and index, strips the running page headers/page numbers and `(cid:NN)` glyph codes, removes figure-label lines, re-joins words hyphenated across lines, turns numbered sections (`3.3.1 The "Big-Oh" Notation`) into headings, and drops the Exercises sections (practice questions with no answers).

I checked the output after chunking:
- no chunk body is over 2,000 characters
- every chunk has balanced code fences
- no HTML entities or leftover textbook headers
- no empty chunks

**Final chunk count:** 2,047 chunks from 86 documents: 933 textbook, 602 GitHub patterns, 395 W3Schools, 44 Built In, 36 GeeksforGeeks, 20 Codecademy, 9 Tech Interview Handbook, 8 Stack Overflow blog. That's slightly above the ~2,000 the assignment uses as a "too small" warning, but that guideline assumes about 10 documents. My corpus is 86 documents and ~2.9M characters, and the median chunk is still ~1,500 characters.

---

## Sample Chunks

<!-- Paste 5 representative chunks from your document collection after running your ingestion pipeline.
     For each chunk, note which source document it came from.
     These must be actual text — not screenshots. -->

**Chunk 1** (`github-patterns-p11-modified-binary-search-0003`), from `github-patterns-p11-modified-binary-search.md` (GitHub Pattern 11: Modified Binary Search)

````text
Pattern 11: Modified Binary Search > Ceiling of a Number (medium)

## Ceiling of a Number (medium)

> Given an array of numbers sorted in an ascending order, find the ceiling of a given number `key`. The ceiling of the `key` will be the smallest element in the given array greater than or equal to the `key`.
>
> Write a function to return the index of the ceiling of the `key`. If there isn’t any ceiling return `-1`.

This problem follows the Binary Search pattern. Since Binary Search helps us find a number in a sorted array efficiently, we can use a modified version of the Binary Search to find the ceiling of a number.

We can use a similar approach as discussed in Order-agnostic Binary Search. We will try to search for the `key` in the given array. If we find the `key`, we return its `index` as the ceiling. If we can’t find the `key`, the next big number will be pointed out by the index `start`.

Since we are always adjusting our range to find the `key`, when we exit the loop, the start of our range will point to the smallest number greater than the `key` as shown in the above picture.

We can add a check in the beginning to see if the `key` is bigger than the biggest number in the input array. If so, we can return `-1`.
````

**Chunk 2** (`gfg-floyd-fast-slow-pointers-0002`), from `gfg-floyd-fast-slow-pointers.md` (GeeksforGeeks: Floyd's slow and fast pointers)

````text
How does Floyd's slow and fast pointers approach work? - GeeksforGeeks

- m = (i-1)*n + (n-k), Here (i-1) * n covers the complete cycles before the final partial cycle, and n - k covers the remaining distance to the meeting point.

Finding the Start of the Cycle

Once the slow and fast pointers meet within the loop, the next step is to identify the start of the cycle. To do this, we reset one of the pointers - let’s say the slow pointer to the head of the linked list. The other pointer, the fast pointer, remains at the point where the two pointers initially met. Both pointers are then moved one node at a time. As they traverse the list, the pointer that was reset to the head will cover the distance m to the start of the loop. Since the total distance m + k covered by the slow pointer is a multiple of the cycle length n, both pointers will eventually converge at the start of the cycle. This simultaneous movement ensures that the pointer starting from the head meets the pointer at the start of the cycle, there by successfully identifying the beginning of the loop.

Floyd’s Cycle-Finding Algorithm is efficient in detecting loops in a linked list with a time complexity O(n) and space complexity of O(1).

Please refer to Find Starting node of cycle for more details.
````

**Chunk 3** (`w3schools-algo-graphs-dijkstra-0001`), from `w3schools-algo-graphs-dijkstra.md` (W3Schools: Dijkstra's Algorithm)

````text
DSA Dijkstra's Algorithm > Dijkstra's Algorithm

## Dijkstra's Algorithm

Dijkstra's algorithm finds the shortest path from one vertex to all other vertices.

It does so by repeatedly selecting the nearest unvisited vertex and calculating the distance to all the unvisited neighboring vertices.

Dijkstra's algorithm is often considered to be the most straightforward algorithm for solving the shortest path problem.

Dijkstra's algorithm is used for solving single-source shortest path problems for directed or undirected paths. Single-source means that one vertex is chosen to be the start, and the algorithm will find the shortest path from that vertex to all other vertices.

Dijkstra's algorithm does not work for graphs with negative edges. For graphs with negative edges, the Bellman-Ford algorithm that is described on the next page, can be used instead.

To find the shortest path, Dijkstra's algorithm needs to know which vertex is the source, it needs a way to mark vertices as visited, and it needs an overview of the current shortest distance to each vertex as it works its way through the graph, updating these distances when a shorter distance is found.

How it works:

- Set initial distances for all vertices: 0 for the source vertex, and infinity for all the other.

- Choose the unvisited vertex with the shortest distance from the start to be the current vertex. So the algorithm will always start with the source as the current vertex.

- For each of the current vertex's unvisited neighbor vertices, calculate the distance from the source and update the distance if the new, calculated, distance is lower.
````

**Chunk 4** (`codecademy-dfs-0009`), from `codecademy-dfs.md` (Codecademy: Depth-First Search)

````text
Depth-First Search (DFS) Algorithm Explained | Codecademy > Depth-First Search (DFS) Algorithm Explained > Frequently asked questions > 4. Which is faster DFS or BFS?

### 3. What is a DFS used for?

Depth-First Search is used for pathfinding, cycle detection, solving puzzles, topological sorting, and exploring graph connectivity.

### 4. Which is faster DFS or BFS?

In terms of time complexity, both Depth-First Search and Breadth-First Search are equal. Speed depends on the problem—DFS may find solutions faster in deep search spaces, while BFS may be quicker for shortest-path problems.

### 5. Which uses more memory, BFS or DFS?

Typically, Breadth-First Search uses more memory because it stores all nodes at the current level, while Depth-First Search only stores nodes along the current path.
````

**Chunk 5** (`textbook-goodrich-dsa-in-python-0188`), from `textbook-goodrich-dsa-in-python.md` (Goodrich et al. textbook, section 3.3.1)

````text
Data Structures and Algorithms in Python > 3.3 Asymptotic Analysis > 3.3.1 The “Big-Oh” Notation

Even with this interpretation,
there is considerable freedom in how we can use arithmetic operations with the big-
Oh notation, and with this freedom comes a certain amount of responsibility.

Characterizing Running Times Using the Big-Oh Notation
The big-Oh notation is used widely to characterize running times and space bounds
in terms of some parameter n, which varies from problem to problem, but is always
defined as a chosen measure of the “size” of the problem. For example, if we
are interested in finding the largest element in a sequence, as with the find max
algorithm, we should let n denote the number of elements in that collection. Using
the big-Oh notation, we can write the following mathematically precise statement
on the running time of algorithm find max (Code Fragment 3.1) for any computer.
Proposition 3.7: Thealgorithm, find max,forcomputingthemaximumelement
ofa listof n numbers, runs in O(n) time.
Justification: The initialization before the loop begins requires only a constant
number of primitive operations. Each iteration of the loop also requires only a constant number of primitive operations, and the loop executes n times. Therefore,
we account for the number of primitive operations being c  + c  · n for appropriate
````

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `BAAI/bge-small-en-v1.5` through sentence-transformers, running locally. Embeddings are normalized and stored in ChromaDB (`chroma_db/`, collection `dsa_guide`) with cosine distance. Queries get bge's retrieval prefix ("Represent this sentence for searching relevant passages: "); chunks don't. I chose it over the default `all-MiniLM-L6-v2` because MiniLM only reads the first 256 tokens (~1,000 characters) of each chunk. My chunks are ~1,500 characters, and the cut-off part is usually the code and the complexity line. bge-small reads 512 tokens, outputs the same 384 dimensions, ran on my laptop CPU in a couple of minutes for all 2,047 chunks, and scores better on retrieval benchmarks.

Retrieval settings (`rag.py`): top-k = 5, picked from the 25 nearest chunks with at most 3 chunks per document, so the textbook (933 of the 2,047 chunks) can't take every slot.

**Production tradeoff reflection:** If cost didn't matter, the first thing I'd change is context length. Code is token-heavy, so a model with an 8k-token window (bge-m3, OpenAI `text-embedding-3-large`) would let one chunk hold a whole problem walkthrough instead of splitting explanation and code. Accuracy on this kind of text is the next issue: a code-aware model (like Voyage's code embeddings) would probably match a plain-English question to a JavaScript or Python chunk better than a general model, but larger models are slower per query and API models charge per token. Multilingual support doesn't matter for my sources since they're all English, but it would if non-native speakers wanted to ask questions in their own language. Local vs. API: local is free, private, works offline and has no rate limits, but re-embedding is CPU-bound. An API model is usually more accurate and needs no hardware, but adds network latency, ongoing cost, and a dependency on the provider keeping that model version around (changing models means re-embedding everything).

---

## Retrieval Test Results

<!-- Run these 3 queries through your retrieval system and record the top returned chunks.
     For at least 2 of the 3, explain why the returned chunks are relevant to the query.
     Results must be text — not screenshots. -->

**Query 1:** In Floyd's fast and slow pointer algorithm, once the two pointers meet inside the loop, how do you find the node where the cycle starts, and what are the time and space complexities?

Top returned chunks:
- `gfg-floyd-fast-slow-pointers-0002` (distance 0.084). *How does Floyd's slow and fast pointers approach work? - GeeksforGeeks*
- `gfg-floyd-fast-slow-pointers-0000` (distance 0.098). *How does Floyd's slow and fast pointers approach work? - GeeksforGeeks*
- `gfg-floyd-fast-slow-pointers-0001` (distance 0.144). *How does Floyd's slow and fast pointers approach work? - GeeksforGeeks*
- `github-patterns-p03-fast-slow-pointers-0005` (distance 0.191). *Pattern 3: Fast & Slow pointers* > Start of LinkedList Cycle (medium)
- `github-patterns-p03-fast-slow-pointers-0003` (distance 0.191). *Pattern 3: Fast & Slow pointers* > LinkedList Cycle (easy)

Relevance explanation: The top chunk (distance 0.084) is the GeeksforGeeks section that answers the question directly: reset the slow pointer to the head, leave the fast pointer at the meeting point, move both one node at a time, and they meet at the cycle start, in O(n) time and O(1) space. The next GfG chunk has the math for *why* it works (m + k is a multiple of the cycle length), and the GitHub Pattern 3 chunk "Start of LinkedList Cycle" gives the same method with code, so the answer is covered by two independent sources.

---

**Query 2:** How do you modify binary search to find the ceiling of a key in a sorted array (smallest element ≥ key)?

Top returned chunks:
- `github-patterns-p11-modified-binary-search-0003` (distance 0.083). *Pattern 11: Modified Binary Search* > Ceiling of a Number (medium)
- `github-patterns-p11-modified-binary-search-0005` (distance 0.130). *Pattern 11: Modified Binary Search* > Ceiling of a Number (medium) > Similar Problem
- `github-patterns-p11-modified-binary-search-0004` (distance 0.142). *Pattern 11: Modified Binary Search* > Ceiling of a Number (medium)
- `textbook-goodrich-dsa-in-python-0636` (distance 0.234). *Data Structures and Algorithms in Python* > 11.1 Binary Search Trees > 11.1.5 Performance of a Binary Search Tree
- `textbook-goodrich-dsa-in-python-0623` (distance 0.236). *Data Structures and Algorithms in Python* > 11.1 Binary Search Trees > 11.1.2 Searches

Relevance explanation: All three top chunks come from the "Ceiling of a Number" problem in GitHub Pattern 11. The first (0.083) is the explanation (if the key is found, return its index; otherwise `start` ends on the next bigger number; return -1 if the key is larger than the last element). Chunk `-0004` is the matching JavaScript code. The related "Similar Problem" (floor of a number) also shows up. Getting the code chunk in the top 5 needed a tweak: with my original cap of 2 chunks per document, the code chunk was dropped (see below).

---

**Query 3:** Why can't Dijkstra's algorithm be used on graphs with negative edge weights, what should you use instead, and what happens if the graph has a negative cycle?

Top returned chunks:
- `w3schools-theory-graphs-shortestpath-0002` (distance 0.163). *DSA Shortest Path* > Positive and Negative Edge Weights
- `w3schools-theory-graphs-shortestpath-0003` (distance 0.177). *DSA Shortest Path* > Negative Cycles in Shortest Path Problems
- `w3schools-algo-graphs-bellmanford-0007` (distance 0.195). *DSA Bellman-Ford Algorithm* > Negative Cycles in The Bellman-Ford Algorithm
- `textbook-goodrich-dsa-in-python-0866` (distance 0.198). *Data Structures and Algorithms in Python* > 14.6 Shortest Paths > 14.6.1 Weighted Graphs
- `w3schools-algo-graphs-dijkstra-0012` (distance 0.203). *DSA Dijkstra's Algorithm* > Dijkstra's Algorithm on Directed Graphs

Relevance explanation: The answer is spread across W3Schools pages, and retrieval pulled from three of them. "Positive and Negative Edge Weights" says Dijkstra only works when all edges are positive and that Bellman-Ford handles negative edges. "Negative Cycles in Shortest Path Problems" and the Bellman-Ford page's negative-cycle section explain that a negative cycle means no shortest path exists, because you can always go around once more, and that Bellman-Ford can detect this. The W3Schools Dijkstra page chunk that says "does not work for graphs with negative edges" verbatim was *not* in the top 5, but the retrieved chunks cover the same facts.

**Tuning note:** My first version followed planning.md (top 10 candidates, max 2 chunks per document). For Query 2, all 10 candidates came from Pattern 11, so only 2 chunks were returned, and the ceiling *code* chunk (`-0004`, distance 0.142) was thrown out. I changed it to 25 candidates with max 3 per document. All 5 evaluation questions now return 5 chunks, and every top result has a distance below 0.17.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Example Responses

<!-- Provide at least 2 grounded responses (query + response + source attribution)
     and 1 out-of-scope query showing your system's refusal.
     All entries must be text — not screenshots. -->

**Grounded response 1**

Query:

Response:

Source attribution:

---

**Grounded response 2**

Query:

Response:

Source attribution:

---

**Out-of-scope query**

Query:

System response (refusal):

---

## Query Interface

<!-- Describe your query interface: what are the input fields, what does the output look like?
     Then provide a complete sample interaction transcript showing a real exchange. -->

**Input fields:**

**Output format:**

---

**Sample Interaction Transcript**

<!-- Show a complete query → response exchange as it actually appears in your interface.
     Must be text — not a screenshot. -->

> **User:** 

> **System:** 

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
