"""Interview engine: questions are parsed out of workflows/*.md, not duplicated in
Python. Editing a question's wording in the markdown (the actual asset) is enough —
nothing in growthos/ needs to change in step.

Each question block in the workflows looks like:

    **Q1 -- Assumptions**
    ```
    Que asumiste en este ticket? ...
    ```

parse_questions() extracts {id: {"title": ..., "text": ...}} in file order.
"""
import re
from pathlib import Path

_QBLOCK_RE = re.compile(
    r"\*\*Q([A-Za-z0-9_]+)\s*--\s*([^\n*]+?)\*\*\s*\n```\s*\n(.*?)\n```",
    re.DOTALL,
)


def parse_questions(workflow_path: Path) -> dict:
    text = workflow_path.read_text()
    questions = {}
    for m in _QBLOCK_RE.finditer(text):
        qid, title, body = m.group(1), m.group(2).strip(), m.group(3).strip()
        questions[qid] = {"title": title, "text": body}
    if not questions:
        raise RuntimeError(
            f"No Q-blocks parsed from {workflow_path} — its question format may have "
            "changed. growthos/interview.py's _QBLOCK_RE needs updating to match."
        )
    return questions


def ask(prompt_text: str) -> str:
    """One question, wait for one answer. The actual interview mechanic —
    no model involved, which is most of Phase 1's token savings."""
    print(f"\n{prompt_text}\n")
    return input("> ").strip()


def ask_upfront(fields: list[tuple[str, str]]) -> dict:
    """gather_context's upfront block: branch / ticket id / description, asked
    together as separate prompts (matches the original 'dame el contexto base' block)."""
    answers = {}
    for key, label in fields:
        answers[key] = input(f"{label}: ").strip()
    return answers
