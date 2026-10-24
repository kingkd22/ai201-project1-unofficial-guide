"""Load the cleaned documents and split them into chunks for embedding.

Chunking follows planning.md:
- split on headings first (Markdown headings, or numbered section headings in the textbook)
- sections under 300 chars are merged into the next section
- target ~1,500 chars per chunk, hard max 2,000; code fences are never split
- 200 chars of overlap only between chunks cut from the same long section
- every chunk is prefixed with "Document title > Section heading"

Usage:
    python ingest.py   # print chunk stats and 5 random sample chunks
"""

import random
import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent / "documents"

TARGET_SIZE = 1500
MAX_SIZE = 2000
MIN_SECTION = 300
OVERLAP = 200

FENCE_RE = re.compile(r"^(`{3,})")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)")


def load_documents():
    """Read every documents/*.md file and split off its Title/Source header."""
    docs = []
    for path in sorted(DOCS_DIR.glob("*.md")):
        header, _, body = path.read_text(encoding="utf-8").partition("\n---\n")
        meta = dict(line.split(": ", 1) for line in header.strip().splitlines() if ": " in line)
        docs.append({
            "doc_id": path.stem,
            "title": meta.get("Title", path.stem),
            "url": meta.get("Source", ""),
            "body": body.strip(),
        })
    return docs


# --- textbook cleaning ------------------------------------------------------

TB_EVEN_HEADER = re.compile(r"^\d{1,3} Chapter ?\d{1,2}\. ")          # "2 Chapter1. PythonPrimer"
TB_ODD_HEADER = re.compile(r"^\d{1,2}\.\d{1,2}\. .* \d{1,3}$")         # "1.1. PythonOverview 3"
TB_DOT_LEADER = re.compile(r"(\. ){4,}")                               # chapter contents lists
TB_CID = re.compile(r"\(cid:\d+\)")                                    # unmapped PDF glyphs
TB_FIGURE_LABELS = re.compile(r"^[A-Z0-9.,:-]+( [A-Z0-9.,:-]+)+$")    # "849 PVD 849 PVD"
TB_SECTION = re.compile(r"^(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?) ([A-Z][^.]{2,70})$")


def clean_textbook(body):
    """Turn the raw PDF text into Markdown-like text with real section headings."""
    lines = body.splitlines()
    # Keep the body only: from the first chapter opener up to the bibliography.
    start = lines.index("Chapter")
    end = max(i for i, l in enumerate(lines) if l.strip() == "Bibliography")
    out, skipping_exercises = [], False
    for line in lines[start:end]:
        line = TB_CID.sub("", line).strip()
        if TB_FIGURE_LABELS.match(line):
            continue
        if TB_EVEN_HEADER.match(line) or TB_ODD_HEADER.match(line) or TB_DOT_LEADER.search(line):
            continue
        if line in ("Chapter", "Contents") or re.fullmatch(r"\d{1,2}", line):
            continue
        m = TB_SECTION.match(line)
        if m:
            depth = m.group(1).count(".") + 1          # 3.3 -> ##, 3.3.1 -> ###
            skipping_exercises = m.group(2).strip() == "Exercises"
            if not skipping_exercises:
                out.append(f"\n{'#' * depth} {m.group(1)} {m.group(2).strip()}\n")
            continue
        if not skipping_exercises:
            # Textbook code has no fences, so "# comment" lines would parse as headings.
            out.append(" " + line if line.startswith("#") else line)
    text = "\n".join(out)
    text = re.sub(r"([A-Za-z])-\n([a-z])", r"\1\2", text)   # re-join hyphenated line breaks
    return text


# --- splitting ----------------------------------------------------------------

def split_sections(body):
    """Split text into (heading_path, text) sections, ignoring '#' lines inside code fences."""
    sections, path, buf, fence = [], [], [], None

    def flush():
        text = "\n".join(buf).strip()
        if text:
            sections.append((" > ".join(h for _, h in path), text))
        buf.clear()

    for line in body.splitlines():
        f = FENCE_RE.match(line)
        if f:
            if fence is None:
                fence = f.group(1)
            elif f.group(1).startswith(fence):
                fence = None
        h = HEADING_RE.match(line) if fence is None else None
        if h:
            flush()
            level = len(h.group(1))
            path = [(lvl, t) for lvl, t in path if lvl < level] + [(level, h.group(2).strip("# "))]
        buf.append(line)
    flush()
    return sections


def split_blocks(text):
    """Split section text into blocks: each code fence is one block, prose splits on blank lines."""
    blocks, buf, fence = [], [], None
    for line in text.splitlines():
        f = FENCE_RE.match(line)
        if fence is None and f:
            if buf:
                blocks.append(("prose", "\n".join(buf)))
            buf, fence = [line], f.group(1)
            continue
        if fence is not None:
            buf.append(line)
            if f and f.group(1).startswith(fence) and len(buf) > 1:
                blocks.append(("code", "\n".join(buf)))
                buf, fence = [], None
            continue
        if line.strip():
            buf.append(line)
        elif buf:
            blocks.append(("prose", "\n".join(buf)))
            buf = []
    if buf:
        blocks.append(("code" if fence else "prose", "\n".join(buf)))
    return [(kind, b.strip()) for kind, b in blocks if b.strip()]


def split_oversized(kind, block):
    """Break a block bigger than MAX_SIZE into ~TARGET_SIZE pieces, leaving room for a heading."""
    if kind == "code":
        # Split at blank lines inside the code, re-wrapping each piece in its own fence.
        lines = block.splitlines()
        opener, closer, inner = lines[0], lines[-1], "\n".join(lines[1:-1])
        units, sep = re.split(r"\n\s*\n", inner), "\n\n"
        wrap = lambda s: f"{opener}\n{s}\n{closer}"
        limit = TARGET_SIZE - len(opener) - len(closer) - 2
    else:
        units, sep, wrap, limit = block.splitlines(), "\n", (lambda s: s), TARGET_SIZE
    pieces, cur = [], ""
    for u in units:
        while len(u) > limit:                      # a single huge line/paragraph: hard cut
            pieces.append(u[:limit])
            u = u[limit:]
        if cur and len(cur) + len(sep) + len(u) > limit:
            pieces.append(cur)
            cur = u
        else:
            cur = f"{cur}{sep}{u}" if cur else u
    if cur:
        pieces.append(cur)
    return [(kind, wrap(p)) for p in pieces]


def overlap_tail(kind, block):
    """Last ~OVERLAP chars of a prose block, cut at a word boundary. Code is never reused."""
    if kind == "code" or len(block) <= OVERLAP:
        return "" if kind == "code" else block
    tail = block[-OVERLAP:]
    return tail[tail.find(" ") + 1:] if " " in tail else tail


def pack_section(text):
    """Greedily pack a section's blocks into chunks of ~TARGET_SIZE, never over MAX_SIZE."""
    blocks = []
    for kind, b in split_blocks(text):
        blocks.extend(split_oversized(kind, b) if len(b) > MAX_SIZE else [(kind, b)])
    # Each chunk is (overlap_text, [blocks]) so a small tail can later be merged back cleanly.
    chunks, blocks_in, last = [], [], None
    size = lambda ov, bl: len("\n\n".join(([ov] if ov else []) + bl))
    overlap = ""
    for kind, b in blocks:
        cur = size(overlap, blocks_in)
        if blocks_in and (cur + 2 + len(b) > MAX_SIZE or cur >= TARGET_SIZE):
            chunks.append((overlap, blocks_in))
            tail = overlap_tail(*last)
            overlap = tail if tail and len(tail) + 2 + len(b) <= MAX_SIZE else ""
            blocks_in = [b]
        else:
            blocks_in = blocks_in + [b]
        last = (kind, b)
    if blocks_in:
        # A short leftover (e.g. a lone "time complexity is O(n)" line after a big code
        # block) is folded back into the previous chunk when it fits.
        prev = chunks[-1] if chunks else None
        if prev and len("\n\n".join(blocks_in)) < MIN_SECTION and size(prev[0], prev[1] + blocks_in) <= MAX_SIZE:
            chunks[-1] = (prev[0], prev[1] + blocks_in)
        else:
            chunks.append((overlap, blocks_in))
    return ["\n\n".join(([ov] if ov else []) + bl) for ov, bl in chunks]


def chunk_document(doc):
    """Chunk one document into dicts with text + metadata for the vector store."""
    body = clean_textbook(doc["body"]) if doc["doc_id"].startswith("textbook") else doc["body"]
    title_key = doc["title"].strip().lower()
    sections = [
        (" > ".join(h for h in heading.split(" > ") if h.strip().lower() != title_key), text)
        for heading, text in split_sections(body)
    ]

    # Merge tiny sections into the following one so they aren't orphaned fragments, and
    # keep a subsection with its parent (e.g. "Problem" + "Solution") when both fit.
    merged, carry = [], ""
    for heading, text in sections:
        text = f"{carry}\n\n{text}" if carry else text
        if len(text) < MIN_SECTION:
            carry = text
            continue
        carry = ""
        if merged:
            parent, ptext = merged[-1]
            if parent and heading.startswith(parent + " > ") and len(ptext) + 2 + len(text) <= TARGET_SIZE:
                merged[-1] = (parent, f"{ptext}\n\n{text}")
                continue
        merged.append((heading, text))
    if carry:
        if merged:
            merged[-1] = (merged[-1][0], f"{merged[-1][1]}\n\n{carry}")
        else:
            merged.append(("", carry))

    chunks = []
    for heading, text in merged:
        for piece in pack_section(text):
            if all(HEADING_RE.match(l) for l in piece.splitlines() if l.strip()):
                continue  # heading with no body; the heading is already in the next chunk's prefix
            prefix = f"{doc['title']} > {heading}" if heading else doc["title"]
            chunks.append({
                "id": f"{doc['doc_id']}-{len(chunks):04d}",
                "text": f"{prefix}\n\n{piece}",
                "metadata": {
                    "doc_id": doc["doc_id"],
                    "title": doc["title"],
                    "url": doc["url"],
                    "heading": heading,
                    "chunk_index": len(chunks),
                },
            })
    return chunks


def build_chunks():
    return [c for doc in load_documents() for c in chunk_document(doc)]


if __name__ == "__main__":
    chunks = build_chunks()
    sizes = sorted(len(c["text"]) for c in chunks)
    print(f"documents: {len(load_documents())}   chunks: {len(chunks)}")
    print(f"chunk size  min {sizes[0]}  median {sizes[len(sizes) // 2]}  max {sizes[-1]}")
    by_source = {}
    for c in chunks:
        key = c["metadata"]["doc_id"].split("-")[0]
        by_source[key] = by_source.get(key, 0) + 1
    print("chunks per source:", by_source)
    random.seed(7)
    for c in random.sample(chunks, 5):
        print("\n" + "=" * 80 + f"\n[{c['id']}]  {c['metadata']['url']}\n" + "-" * 80)
        print(c["text"])
