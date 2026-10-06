"""Ports workflows/weekly-review.md. Deterministic where the original workflow was
deterministic (score-trend averaging, skill-domain table, ticket listing); one model
call for everything that needs judgment (homework-log interpretation, learning-gap
flagging, W1-W5 scoring, resource recommendations) — same economy as reflect. Inbox
triage is a second, separate call: a different judgment over different input files.
"""
import re
from datetime import date, timedelta
from pathlib import Path

from . import config


def week_id(d: date | None = None) -> str:
    d = d or date.today()
    iso_year, iso_week, _ = d.isocalendar()
    return f"{iso_year}-[W]{iso_week:02d}"


def weekly_note_path(cfg: dict) -> Path:
    return config.vault_subdir(cfg, "weekly") / f"{week_id()}.md"


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(errors="ignore")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def gather_tickets(cfg: dict, days: int = 7) -> list[dict]:
    """Recent ticket notes (last `days` by frontmatter date), with id/title/concepts."""
    tickets_dir = config.vault_subdir(cfg, "tickets")
    if not tickets_dir.is_dir():
        return []
    cutoff = date.today() - timedelta(days=days)
    out = []
    for p in sorted(tickets_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True):
        fm = parse_frontmatter(p)
        try:
            d = date.fromisoformat(fm.get("date", ""))
        except ValueError:
            continue
        if d < cutoff:
            continue
        text = p.read_text(errors="ignore")
        title_m = re.search(r"^# (.+)$", text, re.M)
        out.append({
            "ticket": fm.get("ticket", p.stem),
            "date": fm.get("date", ""),
            "title": title_m.group(1).strip() if title_m else p.stem,
            "concepts": re.findall(r"\[\[([^\]]+)\]\]", text),
        })
    return out


def gather_homework(cfg: dict) -> str:
    path = config.vault_root(cfg) / "homework-log.md"
    return path.read_text() if path.exists() else "(homework-log.md not found)"


# ---------------------------------------------------------------------------
# Score trend — pure arithmetic over existing ticket frontmatter, ported directly
# from reflect.md's own inline python block (same logic, same windows).

DIMENSIONS = ["score", "score_d1", "score_d2", "score_d3", "score_d4", "score_d5"]


def gather_score_trend(cfg: dict) -> dict:
    tickets_dir = config.vault_subdir(cfg, "tickets")
    today = date.today()
    curr_start, prior_start = today - timedelta(days=7), today - timedelta(days=14)
    curr = {k: [] for k in DIMENSIONS}
    prior = {k: [] for k in DIMENSIONS}
    if tickets_dir.is_dir():
        for p in tickets_dir.glob("*.md"):
            fm = parse_frontmatter(p)
            if not fm.get("score_d1"):
                continue
            try:
                d = date.fromisoformat(fm.get("date", ""))
            except ValueError:
                continue
            bucket = curr if curr_start <= d <= today else prior if prior_start <= d < curr_start else None
            if bucket is None:
                continue
            for k in bucket:
                v = fm.get(k)
                if v and v.lstrip("-").isdigit():
                    bucket[k].append(int(v))

    def avg(xs):
        return round(sum(xs) / len(xs), 1) if xs else None

    curr_avg = {k: avg(v) for k, v in curr.items()}
    prior_avg = {k: avg(v) for k, v in prior.items()}
    return {
        "curr": curr_avg, "prior": prior_avg,
        "curr_count": len(curr["score_d1"]), "prior_count": len(prior["score_d1"]),
    }


def trend_arrow(curr_v, prior_v) -> str:
    if curr_v is None or prior_v is None:
        return "→"
    if curr_v > prior_v:
        return "↑"
    if curr_v < prior_v:
        return "↓"
    return "→"


def render_score_trend_table(trend: dict) -> str:
    rows = [
        ("D1 Cognitive Depth", "score_d1"), ("D2 Cycle Completeness", "score_d2"),
        ("D3 Loop Depth", "score_d3"), ("D4 Actionability", "score_d4"),
        ("D5 Linguistic Quality", "score_d5"),
    ]
    lines = ["| Dimension | This Week | Prior Week | Trend |", "|-----------|-----------|------------|-------|"]
    for label, key in rows:
        c, p = trend["curr"][key], trend["prior"][key]
        lines.append(f"| {label} | {c if c is not None else '—'} | {p if p is not None else '—'} | {trend_arrow(c, p)} |")
    c, p = trend["curr"]["score"], trend["prior"]["score"]
    lines.append(f"| **Total** | **{c if c is not None else '—'}** | **{p if p is not None else '—'}** | {trend_arrow(c, p)} |")
    table = "\n".join(lines)
    if trend["curr_count"] + trend["prior_count"] < 2:
        table += "\n\n_Insufficient data for trend — keep reflecting._"
    return table


def render_skill_domain_table(cfg: dict) -> str:
    domains = cfg.get("user_profile", {}).get("priority_domains") or ["Core practice", "Adjacent skills"]
    domains = list(domains) + ["Communication"]
    lines = ["| Domain | Score (1-5) | Trend | Note |", "|--------|-------------|-------|------|"]
    lines += [f"| {d} | | → | |" for d in domains]
    return "\n".join(lines)


def render_tickets_table(tickets: list[dict]) -> str:
    if not tickets:
        return "_No ticket reflections this week._"
    lines = ["| Ticket | What I Did |", "|--------|------------|"]
    lines += [f"| {t['ticket']} | {t['title']} |" for t in tickets]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Note composition

WEEKLY_TEMPLATE = """---
week: {week}
date: {date}
tags: [weekly]
weekly_score: {total}
w1: {w1}
w2: {w2}
w3: {w3}
w4: {w4}
w5: {w5}
---

# Week {week} Review

## Tickets This Week

```dataview
TABLE ticket, date
FROM "{vault_name}/20-tickets"
WHERE date >= date(today) - dur(7 days)
SORT date DESC
```

{tickets_table}

## Reflection Score Trend

{score_trend_table}

## Skill Domain Self-Rating

{skill_domain_table}

_Dreyfus scale: 1 Novice (needs rules) · 2 Advanced Beginner (recognizes patterns) · 3 Competent (deliberate choices) · 4 Proficient (sees big picture) · 5 Expert (intuitive)_

## Learning Gaps This Week

```dataview
LIST
FROM "{vault_name}/10-concepts"
WHERE econtains(file.etags, "#learning-gap")
SORT file.mtime DESC
LIMIT 10
```

{learning_gaps}

## Resources in Queue

```dataview
LIST
FROM "{vault_name}/40-resources"
WHERE econtains(file.etags, "#to-read")
SORT file.mtime ASC
LIMIT 5
```

## Homework Log Status

{homework_status}

**Compromiso:** {w_q4}

## ¿Qué se repitió esta semana?

{w_q1}

## Brecha de skill

{w_q2}

## Esta semana puedo

{w_q3}

## Weekly Score

**{total}/10 — {band}**

| Dimension | Score | Feedback |
|---|---|---|
| W1 Learning Velocity | {w1}/3 | {w1_fb} |
| W2 Pattern Recognition | {w2}/2 | {w2_fb} |
| W3 Gap Specificity | {w3}/2 | {w3_fb} |
| W4 Capability Assertion | {w4}/2 | {w4_fb} |
| W5 System Health | {w5}/1 | {w5_fb} |

**Análisis:** {analysis}

{recommendations}
"""

BAND_LABELS = [(3, "Logging"), (5, "Noticing"), (7, "Growing"), (9, "Accelerating"), (10, "Compounding")]


def band_for(total: int) -> str:
    for ceiling, label in BAND_LABELS:
        if total <= ceiling:
            return label
    return "Compounding"


def compose_and_write(cfg: dict, *, path: Path, tickets: list[dict], trend: dict,
                       answers: dict, scores: dict) -> Path:
    note = WEEKLY_TEMPLATE.format(
        week=week_id(), date=date.today().isoformat(),
        vault_name=cfg.get("vault_name", "vault"),
        tickets_table=render_tickets_table(tickets),
        score_trend_table=render_score_trend_table(trend),
        skill_domain_table=render_skill_domain_table(cfg),
        learning_gaps=scores.get("learning_gaps") or "_None flagged this week._",
        homework_status=scores.get("homework_status", "(not computed)"),
        w_q1="Sin patrón cross-ticket esta semana." if answers["w1"].strip().upper() == "N/A" else answers["w1"],
        w_q2="Sin brecha nueva identificada esta semana." if answers["w2"].strip().upper() == "N/A" else answers["w2"],
        w_q3=answers["w3"], w_q4=answers["w4"],
        total=scores["total"], band=band_for(scores["total"]),
        w1=scores["w1"], w1_fb=scores["w1_fb"], w2=scores["w2"], w2_fb=scores["w2_fb"],
        w3=scores["w3"], w3_fb=scores["w3_fb"], w4=scores["w4"], w4_fb=scores["w4_fb"],
        w5=scores["w5"], w5_fb=scores["w5_fb"],
        analysis=scores["analysis"], recommendations=scores.get("recommendations", ""),
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(note)
    return path
