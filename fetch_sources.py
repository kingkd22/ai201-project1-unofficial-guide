"""Download and clean the source documents for the DSA Unofficial Guide.

Each source is fetched, reduced to its main article content (navigation, ads,
share buttons, scripts and interactive widgets removed), converted to light
Markdown that keeps headings, lists and code blocks, and written to
documents/<slug>.md with a small metadata header.

Usage:
    python fetch_sources.py            # fetch everything
    python fetch_sources.py w3schools  # only sources whose slug starts with "w3schools"
"""

import re
import sys
import time
from pathlib import Path
from urllib.parse import quote

import pdfplumber
import requests
from bs4 import BeautifulSoup, Comment, NavigableString, Tag

DOCS_DIR = Path(__file__).parent / "documents"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/130 Safari/537.36"}

W3_BASE = "https://www.w3schools.com/dsa/"
# Every content page in the w3schools DSA tutorial. Quiz/exam/exercise/syllabus
# pages are left out because they are interactive or just link lists.
W3_PAGES = """
intro algo_simple
data_arrays algo_bubblesort algo_selectionsort algo_insertionsort algo_quicksort
algo_countingsort algo_radixsort algo_mergesort algo_linearsearch algo_binarysearch
theory_linkedlists theory_linkedlists_memory data_linkedlists_types algo_linkedlists_operations
data_stacks data_queues
theory_hashtables data_hashsets data_hashmaps
theory_trees data_binarytrees algo_binarytrees_preorder algo_binarytrees_inorder
algo_binarytrees_postorder data_binarysearchtrees data_avltrees
theory_graphs data_graphs_implementation algo_graphs_traversal algo_graphs_cycledetection
theory_graphs_shortestpath algo_graphs_dijkstra algo_graphs_bellmanford
theory_mst_minspantree algo_mst_prim algo_mst_kruskal
theory_graphs_maxflow algo_graphs_fordfulkerson algo_graphs_edmondskarp
timecomplexity_theory timecomplexity_bblsort timecomplexity_selsort timecomplexity_insertionsort
timecomplexity_quicksort timecomplexity_countsort timecomplexity_radixsort timecomplexity_mergesort
timecomplexity_linearsearch timecomplexity_binarysearch
ref_euclidean_algorithm ref_huffman_coding ref_traveling_salesman ref_knapsack
ref_memoization ref_tabulation ref_dynamic_programming ref_greedy
""".split()

GH_REPO = "Chanda-Abdul/Several-Coding-Patterns-for-Solving-Data-Structures-and-Algorithms-Problems-during-Interviews"
GH_FILES = {
    "readme": "README.md",
    "p01-sliding-window": "✅  Pattern 01 : Sliding Window.md",
    "p02-two-pointers": "✅  Pattern 02: Two Pointers.md",
    "p03-fast-slow-pointers": "✅  Pattern 03: Fast & Slow pointers.md",
    "p04-merge-intervals": "✅  Pattern 04 : Merge Intervals.md",
    "p05-cyclic-sort": "✅  Pattern 05: Cyclic Sort.md",
    "p06-linkedlist-reversal": "✅  Pattern 06: In-place Reversal of a LinkedList.md",
    "p07-tree-bfs": "✅  Pattern 07: Tree Breadth First Search.md",
    "p08-tree-dfs": "✅  Pattern 08:Tree Depth First Search.md",
    "p09-two-heaps": "✅ 🙃 Pattern 09: Two Heaps.md",
    "p10-subsets": "✅  Pattern 10: Subsets.md",
    "p11-modified-binary-search": "✅  Pattern 11: Modified Binary Search.md",
    "p12-bitwise-xor": "✅ Pattern 12:  Bitwise XOR.md",
    "p13-top-k-elements": "✅ Pattern 13: Top 'K' Elements.md",
    "p14-k-way-merge": "✅ Pattern 14: K-way merge.md",
    "p15-01-knapsack-dp": "✅ Pattern 15: 0-1 Knapsack (Dynamic Programming).md",
    "p16-topological-sort": "✅ Pattern 16: 🔎 Topological Sort (Graph).md",
}

# (slug, url, CSS selector for the main content)
HTML_SOURCES = [
    ("techinterviewhandbook-array", "https://www.techinterviewhandbook.org/algorithms/array/", ".markdown"),
    ("gfg-big-o-analysis", "https://www.geeksforgeeks.org/dsa/analysis-algorithms-big-o-analysis/", ".article--viewer .text"),
    ("gfg-two-pointers", "https://www.geeksforgeeks.org/dsa/two-pointers-technique/", ".article--viewer .text"),
    ("gfg-floyd-fast-slow-pointers", "https://www.geeksforgeeks.org/dsa/how-does-floyds-slow-and-fast-pointers-approach-work/", ".article--viewer .text"),
    ("gfg-n-base-modified-binary-search", "https://www.geeksforgeeks.org/dsa/n-base-modified-binary-search-algorithm/", ".article--viewer .text"),
    ("builtin-sliding-window", "https://builtin.com/data-science/sliding-window-algorithm", "article"),
    ("codecademy-dfs", "https://www.codecademy.com/article/depth-first-search-dfs-algorithm", "codecademy"),
    ("codecademy-bfs", "https://www.codecademy.com/article/breadth-first-search-bfs-algorithm", "codecademy"),
    ("stackoverflow-blog-dynamic-programming", "https://stackoverflow.blog/2022/01/31/the-complete-beginners-guide-to-dynamic-programming/", ".s-prose"),
] + [(f"w3schools-{p.replace('_', '-')}", f"{W3_BASE}dsa_{p}.php", "#main") for p in W3_PAGES]

PDF_SOURCES = [
    ("textbook-goodrich-dsa-in-python",
     "https://nibmehub.com/opac-service/pdf/read/Data%20Structures%20and%20Algorithms%20in%20Python.pdf"),
]

# Elements that never carry article content.
JUNK_SELECTORS = [
    "script", "style", "noscript", "iframe", "svg", "img", "picture", "figure", "button", "form",
    "input", "nav", "aside", "footer", "header",
    # w3schools
    "#mainLeaderboard", "#midcontentadcontainer", ".nextprev", ".ws-share", "[id^=vueApp]",
    ".w3-example > h3", "a.w3-btn", ".exercisewindow", "#exercisecontainer", "[id^=user-profile]",
    # geeksforgeeks
    ".article-meta", ".improve-section", ".article-pgnavi", "[class*=sideBar]",
    # codecademy course cards
    "[class*=CardWrapper]",
    # misc ads / promos
    "[class*=advert]", "[class*=promo]", "[class*=newsletter]", "[class*=related]",
]

# Everything from one of these headings to the end of the page is link lists or ads.
TRAILING_SECTIONS = re.compile(
    r"\n#+ (Related articles|Learn more on Codecademy|Recommended courses)\b.*", re.S)


def to_markdown(node):
    """Convert an HTML subtree to light Markdown, keeping structure that matters for chunking."""
    out = []

    def walk(el):
        if isinstance(el, Comment):
            return
        if isinstance(el, NavigableString):
            out.append(str(el))
            return
        if not isinstance(el, Tag):
            return
        name = el.name
        if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            out.append(f"\n\n{'#' * int(name[1])} {el.get_text(' ', strip=True)}\n\n")
        elif name == "pre" or "w3-code" in (el.get("class") or []) or "code-block" in " ".join(el.get("class") or []):
            lines = el.select(".token-line")  # codecademy renders one div per code line
            code = "\n".join(l.get_text() for l in lines) if lines else el.get_text().strip("\n")
            out.append(f"\n\n```\n{code}\n```\n\n")
        elif name == "li":
            out.append("\n- ")
            for c in el.children:
                walk(c)
        elif name == "tr":
            cells = [c.get_text(" ", strip=True) for c in el.find_all(["td", "th"])]
            out.append("\n| " + " | ".join(cells) + " |")
        elif name == "br":
            out.append("\n")
        elif name in ("p", "div", "section", "ul", "ol", "table", "blockquote", "article"):
            out.append("\n\n")
            for c in el.children:
                walk(c)
            out.append("\n\n")
        else:
            for c in el.children:
                walk(c)

    walk(node)
    return "".join(out)


def tidy(text):
    """Collapse whitespace outside code fences and drop leftover boilerplate lines."""
    text = TRAILING_SECTIONS.sub("\n", text.replace("​", ""))
    parts = re.split(r"(```.*?```)", text, flags=re.S)
    for i in range(0, len(parts), 2):  # even indexes are prose, odd are code fences
        p = re.sub(r"[ \t\xa0]+", " ", parts[i])
        p = re.sub(r" *\n *", "\n", p)
        parts[i] = p
    text = "".join(parts)
    text = re.sub(r"\n(- *\n)+", "\n", text)        # empty list bullets
    text = re.sub(r"\n{3,}", "\n\n", text)
    boilerplate = re.compile(r"^(Run Example »|Try it Yourself »|Comment|More info|Advertise with us|Share|Link Copied|❮ Previous|Next ❯|Articles)$")
    return "\n".join(l for l in text.splitlines() if not boilerplate.match(l.strip())).strip() + "\n"


def get(url):
    r = requests.get(url, headers=HEADERS, timeout=60)
    r.raise_for_status()
    return r


def write_doc(slug, title, url, body):
    path = DOCS_DIR / f"{slug}.md"
    path.write_text(f"Title: {title}\nSource: {url}\n\n---\n\n{body}", encoding="utf-8")
    print(f"  {path.name:55} {len(body):>9,} chars")


def fetch_html(slug, url, selector):
    soup = BeautifulSoup(get(url).text, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else slug
    if selector == "codecademy":
        # Codecademy uses generated class names; the article is the container
        # two levels above the H1.
        main = soup.select_one("main h1").parent.parent
    else:
        main = soup.select_one(selector)
    if main is None:
        raise ValueError(f"selector {selector!r} matched nothing")
    for sel in JUNK_SELECTORS:
        for el in main.select(sel):
            el.decompose()
    write_doc(slug, title, url, tidy(to_markdown(main)))


def fetch_github(slug, path):
    raw_url = f"https://raw.githubusercontent.com/{GH_REPO}/main/{quote(path)}"
    page_url = f"https://github.com/{GH_REPO}/blob/main/{quote(path)}"
    md = get(raw_url).text
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)              # markdown images
    md = re.sub(r"<img[^>]*>", "", md, flags=re.I)              # html images
    md = re.sub(r"</?(p|div|br|details|summary|sub|sup|b|i)[^>]*>", "", md, flags=re.I)
    title = next((l.lstrip("# ").strip() for l in md.splitlines() if l.startswith("#")), path)
    write_doc(f"github-patterns-{slug}", title, page_url, tidy(md))


def fetch_pdf(slug, url):
    pdf_path = DOCS_DIR / f"{slug}.pdf"
    if not pdf_path.exists():
        pdf_path.write_bytes(get(url).content)
    with pdfplumber.open(pdf_path) as pdf:
        title = (pdf.metadata or {}).get("Title", slug)
        # x_tolerance=1: the default (3) glues words together in this PDF.
        pages = [p.extract_text(x_tolerance=1) for p in pdf.pages]
    body = "\n\n".join(t for t in pages if t and t.strip())
    write_doc(slug, title, url, body.strip() + "\n")


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    DOCS_DIR.mkdir(exist_ok=True)
    jobs = (
        [(s, lambda s=s, u=u, sel=sel: fetch_html(s, u, sel)) for s, u, sel in HTML_SOURCES]
        + [(f"github-patterns-{s}", lambda s=s, p=p: fetch_github(s, p)) for s, p in GH_FILES.items()]
        + [(s, lambda s=s, u=u: fetch_pdf(s, u)) for s, u in PDF_SOURCES]
    )
    failures = []
    for slug, job in jobs:
        if not slug.startswith(only):
            continue
        try:
            job()
        except Exception as e:  # keep going; report at the end
            failures.append((slug, e))
            print(f"  FAILED {slug}: {e}")
        time.sleep(0.5)  # be polite to the sites
    if failures:
        print(f"\n{len(failures)} source(s) failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
