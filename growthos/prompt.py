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


# ---------------------------------------------------------------------------
# growth concept

CONCEPT_OUTPUT_CONTRACT = """
Respond in EXACTLY this format and nothing else — no preamble, no commentary:

===DOMAIN===
<one slug from the allowed list, the closest semantic match>
===CONFIDENCE===
<low, medium, or high -- low if no codebase evidence was given, medium if the evidence
below backs the article, high only for something deeply understood / production-tested>
===BODY===
<the full article body, starting with "> {one-sentence definition}" then every
required section as "## Heading" markdown, in this exact order: What It Is, How It
Works, How We Use It in {project_name}, Related Concepts, Resources to Go Deeper,
Things to Learn / Reinforce. Related Concepts must include at least 2 [[wikilinks]].
If updating only specific sections (told below), output the COMPLETE body with those
sections rewritten and every other section preserved verbatim from the existing
article -- never drop a section you weren't asked to change.>
"""


def build_concept_prompt(*, concept_name: str, domains: list[str], project_name: str,
                          codebase_evidence: str, existing_body: str | None,
                          sections_to_update: str | None) -> str:
    parts = [f"""
Write or expand a Growth OS concept article for: "{concept_name}"

Allowed domains (pick the closest semantic match): {", ".join(domains)}
Project: {project_name}

Codebase evidence (real usage found via grep -- ground the article in this, don't invent paths):
{codebase_evidence}
""".strip()]

    if existing_body:
        parts.append(f"EXISTING ARTICLE BODY (do not lose any section not being updated):\n{existing_body}")
        if sections_to_update:
            parts.append(f"The user asked to update only: {sections_to_update}. Rewrite only those "
                          f"sections; copy every other section through unchanged.")
    else:
        parts.append("No existing article -- write a new one from scratch.")

    parts.append(CONCEPT_OUTPUT_CONTRACT.strip())
    return "\n\n".join(parts)


def parse_concept_response(text: str) -> dict:
    domain = _section(text, "DOMAIN").strip().lower()
    confidence = _section(text, "CONFIDENCE").strip().lower()
    body = _section(text, "BODY")
    return {"domain": domain, "confidence": confidence, "body": body}


# ---------------------------------------------------------------------------
# growth weekly

WEEKLY_OUTPUT_CONTRACT = """
Respond in EXACTLY this format and nothing else — no preamble, no commentary:

===HOMEWORK===
<2-4 lines: one per recurring drill (PR rewrite: once per sprint · Naked system design:
biweekly · One-concept deepening: weekly), each either "done this sprint/week" (cite
evidence from the homework log) or "overdue" with what's overdue. Base this only on
the homework log text given below -- never invent a drill that isn't in it.>
===LEARNING_GAPS===
<for any concept from CONCEPTS that seems to have felt unclear based on the week's
answers, one line each: "- #learning-gap: [[slug]] -- why it felt unclear". If none,
write exactly: NONE>
===SCORES===
W1=<int 0-3>
W2=<int 0-2>
W3=<int 0-2>
W4=<int 0-2>
W5=<int 0-1>
===FEEDBACK===
W1: <one-line specific feedback>
W2: <one-line specific feedback>
W3: <one-line specific feedback>
W4: <one-line specific feedback>
W5: <one-line specific feedback>
===ANALYSIS===
<2-3 sentences: what was strongest, what to push deeper next week. Direct tone,
reference actual words from the answers.>
===RECOMMENDATIONS===
<one bullet per dimension that scored below its max (skip maxed dimensions entirely).
Recommendations may ONLY reference CONCEPTS, TICKETS, and DRILLS_OVERDUE given below --
never invent a book, course, or tool. If every dimension is maxed, write exactly: NONE>
"""


def build_weekly_prompt(*, rubric_text: str, week: str, tickets: list[dict],
                         homework_log: str, answers: dict) -> str:
    tickets_desc = "\n".join(f"- {t['ticket']}: {t['title']}" for t in tickets) or "(none this week)"
    concepts = sorted({c for t in tickets for c in t["concepts"]})
    parts = [rubric_text.strip(), f"""
Score this weekly review. Context:

WEEK: {week}
TICKETS:
{tickets_desc}

CONCEPTS encountered this week: {", ".join(concepts) or "(none)"}

HOMEWORK LOG (raw):
{homework_log}

W-Q1 (Patrón de la semana): {answers['w1']}
W-Q2 (Brecha de skill): {answers['w2']}
W-Q3 (Capability assertion): {answers['w3']}
W-Q4 (Drills): {answers['w4']}
""".strip(), WEEKLY_OUTPUT_CONTRACT.strip()]
    return "\n\n".join(parts)


def parse_weekly_response(text: str) -> dict:
    homework_status = _section(text, "HOMEWORK")
    learning_gaps_raw = _section(text, "LEARNING_GAPS")
    scores_block = _section(text, "SCORES")
    feedback_block = _section(text, "FEEDBACK")
    analysis = _section(text, "ANALYSIS")
    recommendations_raw = _section(text, "RECOMMENDATIONS")

    scores = {}
    for m in re.finditer(r"W(\d)=(\d+)", scores_block):
        scores[f"w{m.group(1)}"] = int(m.group(2))
    for key in ("w1", "w2", "w3", "w4", "w5"):
        if key not in scores:
            raise ParseError(f"Model response missing score for {key.upper()}.")
    for m in re.finditer(r"W(\d):\s*(.+)", feedback_block):
        scores[f"w{m.group(1)}_fb"] = m.group(2).strip()

    scores["total"] = scores["w1"] + scores["w2"] + scores["w3"] + scores["w4"] + scores["w5"]
    scores["analysis"] = analysis
    scores["homework_status"] = homework_status
    scores["learning_gaps"] = None if learning_gaps_raw.strip().upper() == "NONE" else learning_gaps_raw
    scores["recommendations"] = ("📚 Para la próxima semana:\n" + recommendations_raw
                                  if recommendations_raw.strip().upper() != "NONE" else "")
    return scores


def load_weekly_rubric() -> str:
    return config.agent_path("weekly-reviewer.md").read_text()
