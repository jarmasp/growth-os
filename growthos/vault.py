"""Vault I/O: git context gathering, draft detection, concept scanning, note
composition/writing, frontmatter score injection, ledger append.

Ports workflows/premortem.md's write_draft and workflows/reflect.md's gather_context
/ write_note / score steps exactly — same file structure, same rules (status
in-progress vs resolved, same filename scheme, same frontmatter keys).
"""
import re
import subprocess
from datetime import date
from pathlib import Path

from . import config


def slugify(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower())
    return text.strip("-")


def git(*args: str) -> str:
    try:
        proc = subprocess.run(["git", *args], capture_output=True, text=True, timeout=30)
        return proc.stdout.strip() if proc.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def gather_git_context(branch: str) -> dict:
    """Mirrors reflect.md's git log/diff extraction. Degrades to empty strings
    outside a git repo or against a nonexistent branch — never raises."""
    return {
        "log": git("log", f"main...{branch}", "--oneline"),
        "diff_stat": "\n".join(git("diff", f"main...{branch}", "--stat").splitlines()[-10:]),
    }


def gather_planning_artifacts(cwd: Path | None = None) -> str:
    """premortem.md's CONTEXT.md/PLAN.md/RESEARCH.md scan."""
    cwd = cwd or Path.cwd()
    found = []
    for name in ("CONTEXT.md", "PLAN.md", "RESEARCH.md"):
        found.extend(cwd.rglob(name))
    texts = []
    for p in found[:5]:
        try:
            texts.append(f"--- {p} ---\n{p.read_text()[:3000]}")
        except OSError:
            continue
    return "\n\n".join(texts)


def scan_concepts(cfg: dict) -> list[str]:
    """Scans every domain in config_domains — the bash version only checked 4
    hardcoded folders (backend/security/system-design/infra), silently missing
    any domain a user added via /growth:onboard. Fixed here: iterate config."""
    root = config.vault_subdir(cfg, "concepts")
    slugs = []
    for domain in cfg.get("concept_domains", []):
        d = root / domain
        if d.is_dir():
            slugs.extend(p.stem for p in d.glob("*.md"))
    return slugs


def find_ticket_note(cfg: dict, ticket_id: str) -> Path | None:
    tickets_dir = config.vault_subdir(cfg, "tickets")
    if not tickets_dir.is_dir():
        return None
    matches = sorted(tickets_dir.glob(f"{ticket_id}*"))
    return matches[0] if matches else None


def read_frontmatter_field(text: str, field: str) -> str | None:
    m = re.search(rf"^{field}:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else None


def read_section(text: str, heading: str) -> str:
    m = re.search(rf"## {re.escape(heading)}\n\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    return m.group(1).strip() if m else ""


def detect_draft(cfg: dict, ticket_id: str) -> dict | None:
    """Returns {"path", "premortem", "assumptions"} if an in-progress draft
    exists for this ticket, else None."""
    path = find_ticket_note(cfg, ticket_id)
    if not path:
        return None
    text = path.read_text()
    if read_frontmatter_field(text, "status") != "in-progress":
        return None
    return {
        "path": path,
        "premortem": read_section(text, "Pre-mortem"),
        "assumptions": read_section(text, "Assumptions"),
    }


def check_existing_resolved(cfg: dict, ticket_id: str) -> Path | None:
    path = find_ticket_note(cfg, ticket_id)
    if path and read_frontmatter_field(path.read_text(), "status") == "resolved":
        return path
    return None


# ---------------------------------------------------------------------------
# Premortem draft

PREMORTEM_TEMPLATE = """---
date: {date}
ticket: {ticket_id}
branch: {branch}
status: in-progress
tags: [ticket]
score:
score_d1:
score_d2:
score_d3:
score_d4:
score_d5:
---

# {ticket_id} -- {short_description}

## Pre-mortem

**Contexto de negocio:** {q1}

**Puntos de falla probables:**
{q2_list}

**Patrón de diseño:** {q3}

## Assumptions

{q4}

## What Was Hard

<!-- Completar con /growth:reflect después de resolver el ticket. -->

## What I Learned

<!-- Completar con /growth:reflect después de resolver el ticket. -->

## Concepts Encountered

<!-- Completar con /growth:reflect después de resolver el ticket. -->

- [[]]

## What I'd Do Differently

<!-- Completar con /growth:reflect después de resolver el ticket. -->

## Reflection Score

<!-- Completar con /growth:reflect después de resolver el ticket. -->
"""


def format_failure_points(answer: str) -> str:
    """Best-effort numbered-list formatting of a free-text failure-points answer.

    ponytail: covers the three realistic shapes (one item per line, inline
    numbered "1. ... 2. ...", or plain sentences) — not a general prose parser.
    Falls back to a single item when nothing splits cleanly, which is always safe."""
    text = answer.strip()
    lines = [l.strip(" -") for l in text.splitlines() if l.strip()]
    if len(lines) >= 2:
        parts = lines
    else:
        parts = [p.strip() for p in re.split(r"(?:^|\s)\d+[\.\)]\s*", text) if p.strip()]
        if len(parts) < 2:
            parts = [p.strip() for p in re.split(r"\.\s+", text) if p.strip()]
    if len(parts) < 2:
        return f"1. {text}"
    return "\n".join(f"{i+1}. {p.rstrip('.')}." for i, p in enumerate(parts[:3]))


def default_ticket_path(cfg: dict, ticket_id: str, branch: str) -> Path:
    return config.vault_subdir(cfg, "tickets") / f"{ticket_id}-{slugify(branch)}.md"


def write_premortem(path: Path, *, branch: str, ticket_id: str, short_description: str,
                     answers: dict) -> Path:
    """`path` is decided by the caller (cli.py): the existing draft/resolved note's
    path when overwriting, or default_ticket_path() for a fresh one."""
    note = PREMORTEM_TEMPLATE.format(
        date=date.today().isoformat(),
        ticket_id=ticket_id,
        branch=branch,
        short_description=short_description,
        q1=answers["1"],
        q2_list=format_failure_points(answers["2"]),
        q3=answers["3"],
        q4="No critical assumptions identified." if answers["4"].strip().upper() == "N/A" else answers["4"],
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(note)
    return path


# ---------------------------------------------------------------------------
# Reflection note

REFLECT_TEMPLATE = """---
date: {date}
ticket: {ticket_id}
branch: {branch}
status: resolved
tags: [ticket]
score: {total}
score_d1: {d1}
score_d2: {d2}
score_d3: {d3}
score_d4: {d4}
score_d5: {d5}
---

# {ticket_id} -- {short_description}

## Pre-mortem

{premortem}

## Assumptions

{assumptions}

## What Was Hard

{q2}

## What I Learned

{q3}

## Concepts Encountered

{concepts}

## What I'd Do Differently

{q4}

## Reflection Score

**{total}/10 -- {band}**

| Dimension | Score | Feedback |
|---|---|---|
| D1 Cognitive Depth | {d1}/3 | {d1_fb} |
| D2 Cycle Completeness | {d2}/2 | {d2_fb} |
| D3 Loop Depth | {d3}/2 | {d3_fb} |
| D4 Actionability | {d4}/2 | {d4_fb} |
| D5 Linguistic Quality | {d5}/1 | {d5_fb} |

**Análisis:** {analysis}
"""

BAND_LABELS = [
    (3, "Reporting"), (5, "Noticing"), (7, "Analyzing"), (9, "Internalizing"), (10, "Mastering"),
]


def band_for(total: int) -> str:
    for ceiling, label in BAND_LABELS:
        if total <= ceiling:
            return label
    return "Mastering"


def format_concepts(slugs: list[str]) -> str:
    if not slugs:
        return "- [[]] (no matching concepts found — candidate for /growth:concept)"
    return "\n".join(f"- [[{s}]]" for s in slugs)


def write_reflection(cfg: dict, *, path: Path, branch: str, ticket_id: str,
                      short_description: str, premortem: str, assumptions: str,
                      answers: dict, concepts: list[str], scores: dict) -> Path:
    note = REFLECT_TEMPLATE.format(
        date=date.today().isoformat(),
        ticket_id=ticket_id,
        branch=branch,
        short_description=short_description,
        premortem=premortem,
        assumptions=assumptions,
        q2=answers["q2"],
        q3=answers["q3"],
        concepts=format_concepts(concepts),
        q4="No changes -- approach was correct." if answers["q4"].strip().lower() == "nada" else answers["q4"],
        total=scores["total"], band=band_for(scores["total"]),
        d1=scores["d1"], d1_fb=scores["d1_fb"],
        d2=scores["d2"], d2_fb=scores["d2_fb"],
        d3=scores["d3"], d3_fb=scores["d3_fb"],
        d4=scores["d4"], d4_fb=scores["d4_fb"],
        d5=scores["d5"], d5_fb=scores["d5_fb"],
        analysis=scores["analysis"],
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(note)
    return path


LEDGER_HEADER = """# Reflection Score Ledger

Append a row after every scored reflection. One row per `/growth:reflect` run. Total = sum of D1..D5.

Dimension maxima: D1 Cognitive Depth (3) · D2 Cycle Completeness (2) · D3 Loop Depth (2) · D4 Actionability (2) · D5 Linguistic Quality (1) · Total (10)

| Date | Ticket | Total | D1 | D2 | D3 | D4 | D5 | Branch |
|------|--------|-------|----|----|----|----|----|--------|
"""


def append_ledger(cfg: dict, *, ticket_id: str, branch: str, scores: dict) -> Path:
    ledger = config.vault_root(cfg) / "reflection-scores.md"
    if not ledger.exists():
        ledger.write_text(LEDGER_HEADER)
    row = (f"| {date.today().isoformat()} | {ticket_id} | {scores['total']} | {scores['d1']} | "
           f"{scores['d2']} | {scores['d3']} | {scores['d4']} | {scores['d5']} | {branch} |\n")
    with ledger.open("a") as f:
        f.write(row)
    return ledger
