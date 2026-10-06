"""Builds the one stateless model call /growth reflect needs, and parses its
response. The rubric text is read verbatim from agents/reflection-scorer.md at
call time — it is never duplicated here, so editing the rubric in that file is
the only thing anyone has to do to change scoring behavior.
"""
import re

from . import config

OUTPUT_CONTRACT = """
Respond in EXACTLY this format and nothing else — no preamble, no markdown fences
around the whole thing, no commentary before or after:

===SCORES===
D1=<int 0-3>
D2=<int 0-2>
D3=<int 0-2>
D4=<int 0-2>
D5=<int 0-1>
===FEEDBACK===
D1: <one-line specific feedback>
D2: <one-line specific feedback>
D3: <one-line specific feedback>
D4: <one-line specific feedback>
D5: <one-line specific feedback>
===ANALYSIS===
<2-3 sentences: strongest point, what to push deeper on next reflection. Direct tone,
reference actual words from the answers, no padding.>
===PREMORTEM===
<if asked for inference below: business context (1-2 sentences), then 3 numbered
probable failure points, then the key design pattern/decision, inferred from the git
context only -- never invented. If no inference was requested, write exactly: NONE>
"""


def build_reflect_prompt(*, rubric_text: str, ticket_id: str, short_description: str,
                          pattern: str, files: str, answers: dict,
                          need_premortem_inference: bool, git_context: dict | None) -> str:
    parts = [rubric_text.strip()]
    parts.append(f"""
Score this reflection. Context:

TICKET: {ticket_id} -- {short_description}
PATTERN: {pattern or "(not detected)"}
FILES: {files or "(not detected)"}

Q1 (Assumptions / bridge): {answers.get("q1", "")}
Q2 (What Was Hard): {answers.get("q2", "")}
Q3 (What I Learned): {answers.get("q3", "")}
Q4 (What I'd Do Differently): {answers.get("q4", "")}
""".strip())

    if need_premortem_inference:
        git_context = git_context or {}
        parts.append(f"""
Also infer the Pre-mortem section for this ticket from the git context below: business
context (what problem this solves), the 3 most probable failure points, and the key
design pattern. Keep it factual, inferred from the commits only -- never invent detail
that isn't evidenced.

GIT LOG:
{git_context.get("log") or "(no commits found between main and this branch)"}

GIT DIFF STAT:
{git_context.get("diff_stat") or "(no diff found)"}
""".strip())

    parts.append(OUTPUT_CONTRACT.strip())
    return "\n\n".join(parts)


class ParseError(RuntimeError):
    pass


def _section(text: str, name: str) -> str:
    m = re.search(rf"==={name}===\s*\n(.*?)(?=\n===|\Z)", text, re.DOTALL)
    if not m:
        raise ParseError(f"Model response missing ==={name}=== section.")
    return m.group(1).strip()


def parse_reflect_response(text: str) -> dict:
    scores_block = _section(text, "SCORES")
    feedback_block = _section(text, "FEEDBACK")
    analysis = _section(text, "ANALYSIS")
    premortem_block = _section(text, "PREMORTEM")

    scores = {}
    for m in re.finditer(r"D(\d)=(\d+)", scores_block):
        scores[f"d{m.group(1)}"] = int(m.group(2))
    for key in ("d1", "d2", "d3", "d4", "d5"):
        if key not in scores:
            raise ParseError(f"Model response missing score for {key.upper()}.")

    for m in re.finditer(r"D(\d):\s*(.+)", feedback_block):
        scores[f"d{m.group(1)}_fb"] = m.group(2).strip()

    scores["total"] = scores["d1"] + scores["d2"] + scores["d3"] + scores["d4"] + scores["d5"]
    scores["analysis"] = analysis
    scores["premortem_inferred"] = None if premortem_block.strip().upper() == "NONE" else premortem_block
    return scores


def load_rubric() -> str:
    return config.agent_path("reflection-scorer.md").read_text()
