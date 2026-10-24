"""Gradio web UI for the DSA Unofficial Guide.

Usage:
    python app.py   # then open http://localhost:7860
"""

import gradio as gr

from rag import ask

EXAMPLES = [
    "After the fast and slow pointers meet, how do I find where the cycle starts?",
    "How do I modify binary search to find the ceiling of a number in a sorted array?",
    "Why doesn't Dijkstra's algorithm work with negative edge weights?",
    "What's the difference between memoization and tabulation?",
    "When should I use the sliding window technique?",
]


def handle_query(question):
    question = (question or "").strip()
    if not question:
        return "Type a question about data structures or algorithms.", "", ""
    result = ask(question)
    sources = "\n".join(f"- {s}" for s in result["sources"]) or "_No sources: the guide's documents don't cover this question._"
    retrieved = "\n\n".join(
        f"**{c['id']}** (distance {c['distance']:.3f})\n\n```text\n{c['text'][:600]}{'…' if len(c['text']) > 600 else ''}\n```"
        for c in result["chunks"]
    ) or "_No chunks were close enough to the question._"
    return result["answer"], sources, retrieved


with gr.Blocks(title="DSA Unofficial Guide") as demo:
    gr.Markdown(
        "# DSA Unofficial Guide\n"
        "Ask how to solve data structures & algorithms problems. Answers come **only** from the collected "
        "sources (W3Schools, GeeksforGeeks, Codecademy, Built In, a coding-patterns GitHub repo, and a DSA "
        "textbook), with citations like [1] that match the source list."
    )
    question = gr.Textbox(label="Your question", placeholder="e.g. How does Floyd's cycle detection work?", lines=2)
    ask_btn = gr.Button("Ask", variant="primary")
    gr.Examples(EXAMPLES, inputs=question)
    answer = gr.Markdown(label="Answer")
    gr.Markdown("### Sources")
    sources = gr.Markdown()
    with gr.Accordion("Retrieved chunks (what the answer was based on)", open=False):
        retrieved = gr.Markdown()

    ask_btn.click(handle_query, inputs=question, outputs=[answer, sources, retrieved])
    question.submit(handle_query, inputs=question, outputs=[answer, sources, retrieved])


if __name__ == "__main__":
    demo.launch()
