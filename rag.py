"""Retrieval (and, from Milestone 5, grounded generation) for the DSA Unofficial Guide."""

from index import QUERY_PREFIX, get_collection, get_model

TOP_K = 5
CANDIDATES = 25
MAX_PER_DOC = 3


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
