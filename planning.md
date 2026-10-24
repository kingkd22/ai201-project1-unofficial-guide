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

**Chunk size:** About 1,500 characters, with a max of 2,000. I split each document on its headings first, then only break up sections that are longer than 2,000 characters (at paragraph breaks). Tiny sections under 300 characters get merged into the next one.

*Update after building it (Milestone 3):* I added two rules once I saw the real chunks. A subsection stays with its parent if both fit in 1,500 characters, because otherwise problems got split from their "Solution" subsections. And a short leftover at the end of a section (like a lone "time complexity is O(n)" line) gets folded back into the previous chunk. Size and overlap numbers didn't change. Final count: 2,047 chunks.

**Overlap:** 200 characters, but only when a long section gets split. I don't overlap across headings since a new heading usually means a new topic.

**Reasoning:** My documents are long tutorials and pattern notes, not short reviews. Almost every section is one idea, like one problem or one step of an algorithm, usually laid out as explanation, then code, then the time/space complexity. I measured the web and GitHub docs: the median section is about 815 characters and most are under 1,740, and 90% of code blocks are under about 1,640. So 1,500 characters should fit a whole explanation + code block in one chunk most of the time. I'm also never going to split in the middle of a code block, because half a function isn't useful. Each chunk will start with the document title and section heading (like "Pattern 11: Modified Binary Search > Ceiling of a Number") so a chunk that's mostly code can still match a question about the concept.

The textbook is different since it's a PDF. It's over half the whole corpus and the text came out messy, so before chunking I'll clean it up: cut the table of contents, index, and bibliography, remove the page headers/page numbers, fix words that got hyphenated across lines, split on the numbered section headings (like "11.3 AVL Trees"), and drop the Exercises sections since they're just practice questions with no answers.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** BAAI/bge-small-en-v1.5 through sentence-transformers, running locally. I picked it over all-MiniLM-L6-v2 because MiniLM only reads the first 256 tokens (around 1,000 characters) of a chunk, which would cut off the end of my 1,500-character chunks, and that's usually where the code and complexity are. bge-small reads up to 512 tokens and is about as fast. I'll store the embeddings in ChromaDB using cosine similarity, with the document title, URL, and section heading saved as metadata so I can cite sources.

**Top-k:** 5. Some of my questions need info from two different pages (like Dijkstra vs Bellman-Ford), so I want more than 2–3 chunks, but not so many that the answer gets buried. Since the textbook is more than half of all chunks, I'll grab the top 10 and only keep 2 chunks max from any one document, so the textbook can't take every spot.

*Update after testing retrieval (Milestone 4):* I changed this to the top 25 with max 3 per document. With 10 and 2, the ceiling-of-a-number question only got 2 chunks back, because all 10 candidates were from Pattern 11, and the chunk with the actual code got cut.

**Production tradeoff reflection:** If cost wasn't an issue, the main thing I'd look for is a longer context length, since code eats up tokens fast and a bigger window would let a chunk hold a full problem walkthrough. A bigger or code-focused model would probably also match plain-English questions to code chunks better, but it'd be slower or cost money per call if it's an API. Multilingual support doesn't really matter for me since all my sources are in English. Running locally is free and private but slower to re-index, while an API model would likely be more accurate but adds cost, latency, and depending on another company.

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

I tried to spread these across different sources and formats. Q2 and Q3 are the ones I think are most likely to fail: Q2's answer is split between text and a code block, and Q3 needs chunks from two different pages.

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Explanation and code getting split up.** A lot of answers are a paragraph explaining the approach followed by the code. If a chunk boundary lands between them, retrieval might return one without the other. Q2 (ceiling of a number) is the riskiest, since part of the answer is in the text and the "return -1" check is only in the code.

2. **Answers that need two documents.** Q3 needs both the Dijkstra page and the Bellman-Ford page. If all 5 chunks come from one page, the answer will be incomplete or the model might fill in the rest from its own knowledge. The 2-chunks-per-document limit should help with this.

3. **The textbook adding noise.** It's huge and the PDF text is messy (lost code indentation, page headers, broken words). Leftover junk could get retrieved instead of the cleaner web pages. The cleanup step and the per-document limit are meant to handle this, but if it still happens I'll document it as a failure case.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```
 ┌──────────────────────────────────────────────────────────────────────────┐
 │ 1. DOCUMENT INGESTION            fetch_sources.py                        │
 │    requests + BeautifulSoup (HTML), raw GitHub Markdown, pdfplumber (PDF)│
 │    → documents/*.md  (86 files, Title/Source header + cleaned Markdown)  │
 └──────────────────────────────────┬───────────────────────────────────────┘
                                    ▼
 ┌──────────────────────────────────────────────────────────────────────────┐
 │ 2. CHUNKING                      ingest.py  (plain Python + re)          │
 │    textbook cleaning → split on headings → merge <300 / split >2,000     │
 │    ~1,500-char chunks, 200 overlap, code fences kept whole,              │
 │    "Title > Heading" prefix + metadata {source, url, heading}            │
 └──────────────────────────────────┬───────────────────────────────────────┘
                                    ▼
 ┌──────────────────────────────────────────────────────────────────────────┐
 │ 3. EMBEDDING + VECTOR STORE      index.py                                │
 │    sentence-transformers  BAAI/bge-small-en-v1.5 (384-d, normalized)     │
 │    → ChromaDB persistent collection (cosine), stored in chroma_db/       │
 └──────────────────────────────────┬───────────────────────────────────────┘
                                    ▼
 ┌──────────────────────────────────────────────────────────────────────────┐
 │ 4. RETRIEVAL                     rag.py  retrieve(query)                 │
 │    embed query (bge prefix) → 25 nearest → max 3 per document → top 5    │
 │    drop chunks with distance > 0.38 (refuse if none are left)            │
 └──────────────────────────────────┬───────────────────────────────────────┘
                                    ▼
 ┌──────────────────────────────────────────────────────────────────────────┐
 │ 5. GENERATION                    rag.py  generate_answer(query)          │
 │    Groq API  openai/gpt-oss-20b, temperature 0.2                         │
 │    grounded system prompt + numbered context chunks → answer + [n] cites │
 │    + "Sources:" list (title + URL); refuses when context lacks answer    │
 └──────────────────────────────────┬───────────────────────────────────────┘
                                    ▼
                    QUERY INTERFACE  app.py  (Gradio web UI)
```

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

**Milestone 3 — Ingestion and chunking:** I'll give Claude my Chunking Strategy section, the architecture diagram, and a couple of sample files from documents/, and ask it to write ingest.py with load_documents(), clean_textbook(), and chunk_document(). To check it, I'll print the chunk count and sizes, make sure nothing is over 2,000 characters, check that no code block got cut in half, and read through a few random chunks myself.

**Milestone 4 — Embedding and retrieval:** I'll give Claude my Retrieval Approach section and ask it to write build_index() (embed with bge-small and store in ChromaDB) and retrieve(query) with the top-5 / max-2-per-document rule. Before adding any generation, I'll run my 5 test questions through retrieval only and check that the right source shows up in the results for each one.

**Milestone 5 — Generation and interface:** I'll give Claude the grounding requirements (only answer from the retrieved chunks, always cite sources, say so if the answer isn't there) and ask it to write generate_answer() using openai/gpt-oss-20b on Groq and a simple Gradio app. I'll check that every answer lists its sources, that an off-topic question gets refused, and compare the answers to my expected answers.
