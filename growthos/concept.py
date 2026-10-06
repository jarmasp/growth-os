"""Ports workflows/concept.md: write or expand a concept article. One model call —
unlike reflect/premortem's fixed interview, writing an explanation is inherently a
generation task, not a Q&A loop, so there's nothing for Python to ask one-at-a-time.
"""
import re
import subprocess
from datetime import date
from pathlib import Path

from . import config, vault

REQUIRED_SECTIONS = [
    "What It Is", "How It Works", "Related Concepts",
    "Resources to Go Deeper", "Things to Learn / Reinforce",
]


def resolve_slug(name: str) -> str:
    return vault.slugify(name)


def find_concept_file(cfg: dict, slug: str) -> Path | None:
    concepts_dir = config.vault_subdir(cfg, "concepts")
    matches = list(concepts_dir.glob(f"*/*{slug}*.md"))
    return matches[0] if matches else None


def classify_state(path: Path | None) -> str:
    """not_found | stub | full — a section counts as filled if it has more than a
    placeholder line (callout question, empty bullet, or blank) after its heading."""
    if path is None:
        return "not_found"
    text = path.read_text()
    filled = 0
    for heading in REQUIRED_SECTIONS:
        section = vault.read_section(text, heading)
        meaningful = [
            line for line in section.splitlines()
            if line.strip() and not line.strip().startswith(("> [!question]", "**Broader:**", "**Narrower:**", "**Sibling:**"))
        ]
        if meaningful:
            filled += 1
    return "full" if filled >= len(REQUIRED_SECTIONS) - 1 else "stub"


def gather_codebase_evidence(keyword: str, cwd: Path | None = None) -> str:
    """Language-agnostic grep from repo root, excluding common dep/build noise —
    same fix already applied to workflows/concept.md's own bash block."""
    cwd = cwd or Path.cwd()
    try:
        proc = subprocess.run(
            ["grep", "-rn", keyword, ".",
             "--exclude-dir=.git", "--exclude-dir=node_modules", "--exclude-dir=dist",
             "--exclude-dir=build", "--exclude-dir=vendor", "--exclude-dir=.venv",
             "--exclude-dir=target", "-l"],
            capture_output=True, text=True, timeout=30, cwd=cwd,
        )
        files = [f for f in proc.stdout.splitlines() if f][:8]
    except (OSError, subprocess.TimeoutExpired):
        return "(no codebase context)"
    if not files:
        return "(no codebase context — concept not found in current directory's source)"
    chunks = []
    for f in files[:2]:
        try:
            content = (cwd / f).read_text(errors="ignore")[:2000]
            chunks.append(f"--- {f} ---\n{content}")
        except OSError:
            continue
    return "\n\n".join(chunks) or f"Found in: {', '.join(files)} (could not read contents)"


ARTICLE_TEMPLATE = """---
date: {date}
tags: [concept, #{domain}]
confidence: {confidence}
moc: "[[MOC-{domain_title}]]"
---

# {title}

{body}
"""


def write_article(cfg: dict, *, slug: str, title: str, domain: str, confidence: str, body: str,
                   existing_path: Path | None) -> Path:
    path = existing_path or (config.vault_subdir(cfg, "concepts") / domain / f"{slug}.md")
    note = ARTICLE_TEMPLATE.format(
        date=date.today().isoformat(), domain=domain, domain_title=domain.replace("-", " ").title(),
        confidence=confidence, title=title, body=body.strip(),
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(note)
    return path


def extract_wikilinks(body: str) -> list[str]:
    return re.findall(r"\[\[([^\]]+)\]\]", body)
