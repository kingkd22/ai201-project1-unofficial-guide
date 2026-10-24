"""Retrieval and grounded generation for the DSA Unofficial Guide.

Usage:
    python rag.py "How do I find the start of a cycle in a linked list?"
"""

import os
import re
import sys

from dotenv import load_dotenv
from groq import Groq

from index import QUERY_PREFIX, get_collection, get_model

TOP_K = 5
CANDIDATES = 25
MAX_PER_DOC = 3
# Chunks farther than this (cosine distance) are treated as irrelevant. In-scope DSA questions
# scored 0.14-0.32 on their best chunk; off-topic questions scored 0.42+.
MAX_DISTANCE = 0.38

LLM_MODEL = "openai/gpt-oss-20b"
REFUSAL = "I don't have enough information in my sources to answer that."

SYSTEM_PROMPT = f"""You are the DSA Unofficial Guide, an assistant that answers questions about data structures and algorithms using ONLY the numbered source excerpts provided in the user message.

Rules:
1. Use only facts, steps, code, and complexities that appear in the excerpts. Do not add anything from your own knowledge, even if you are confident it is true.
2. Cite every claim with the excerpt number(s) it came from, like [1] or [2][3]. Every sentence that states a fact needs a citation.
3. If the excerpts do not contain the answer, reply with exactly: "{REFUSAL}" and nothing else.
4. If the excerpts only answer part of the question, answer that part and say plainly which part the sources do not cover.
5. If you show code, copy it from an excerpt and label its language (Python or JavaScript) as it appears in the source.
6. Be concise: a short explanation, then steps or code only if they help."""

_client = None


def get_client():
    global _client
    if _client is None:
        load_dotenv()
        _client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _client


def retrieve(query, k=TOP_K, candidates=CANDIDATES, max_per_doc=MAX_PER_DOC):
    """Return the top-k chunks for a query, keeping at most max_per_doc chunks per document.

    Each result is {"id", "text", "metadata", "distance"}; distance is cosine distance (lower = closer).
    """
    embedding = get_model().encode([QUERY_PREFIX + query], normalize_embeddings=True).tolist()
    res = get_collection().query(query_embeddings=embedding, n_results=candidates)
    results, per_doc = [], {}
    for cid, text, meta, dist in zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0]):
        doc = meta["doc_id"]
        if per_doc.get(doc, 0) >= max_per_doc:
            continue
        per_doc[doc] = per_doc.get(doc, 0) + 1
        results.append({"id": cid, "text": text, "metadata": meta, "distance": dist})
        if len(results) == k:
            break
    return results


def build_prompt(query, chunks):
    """Number each excerpt and label it with its source so the model can cite [n]."""
    parts = []
    for n, c in enumerate(chunks, 1):
        m = c["metadata"]
        parts.append(f"[{n}] Source: {m['title']}\nURL: {m['url']}\n\n{c['text']}")
    excerpts = "\n\n-----\n\n".join(parts)
    return f"Source excerpts:\n\n{excerpts}\n\n-----\n\nQuestion: {query}"


def format_sources(chunks, cited):
    """Build the source list in code from retrieval metadata, so attribution never depends on the LLM."""
    lines, seen = [], set()
    for n, c in enumerate(chunks, 1):
        if n not in cited:
            continue
        m = c["metadata"]
        heading = f" > {m['heading']}" if m["heading"] else ""
        key = (m["title"], m["heading"])
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"[{n}] {m['title']}{heading}  ({m['url']})")
    return lines


def ask(query):
    """Answer a question from the retrieved chunks only.

    Returns {"answer", "sources": [str], "chunks": [retrieved chunk dicts]}.
    """
    chunks = [c for c in retrieve(query) if c["distance"] <= MAX_DISTANCE]
    if not chunks:
        # Nothing relevant was retrieved: refuse without calling the LLM at all.
        return {"answer": REFUSAL, "sources": [], "chunks": []}

    response = get_client().chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(query, chunks)},
        ],
        temperature=0.2,
        max_completion_tokens=2048,
    )
    answer = response.choices[0].message.content.strip()
    if answer.startswith(REFUSAL):
        return {"answer": REFUSAL, "sources": [], "chunks": chunks}

    cited = {int(n) for n in re.findall(r"\[(\d+)\]", answer) if 1 <= int(n) <= len(chunks)}
    # If the model forgot to cite, fall back to listing every chunk it was given.
    sources = format_sources(chunks, cited or set(range(1, len(chunks) + 1)))
    return {"answer": answer, "sources": sources, "chunks": chunks}


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or input("Question: ")
    result = ask(question)
    print(result["answer"])
    if result["sources"]:
        print("\nSources:")
        print("\n".join(result["sources"]))
