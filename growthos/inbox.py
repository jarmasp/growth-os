"""Ports workflows/weekly-review.md's process_inbox step: read every file in
00-inbox/, propose where each belongs, show the plan, execute only on confirmation.
A separate model call from the weekly score — different judgment over different
input (arbitrary file contents vs. the week's interview answers).
"""
import re
from pathlib import Path

from . import config

TRIAGE_OUTPUT_CONTRACT = """
Respond in EXACTLY this format and nothing else — one line per file, in the same order
given, nothing before or after:

===PLAN===
<filename> | <MOVE:dest_subpath | DELETE | STUB:10-concepts/domain> | <one-line reason>
...
"""


def read_inbox(cfg: dict) -> list[dict]:
    inbox_dir = config.vault_subdir(cfg, "inbox")
    if not inbox_dir.is_dir():
        return []
    files = []
    for p in sorted(inbox_dir.glob("*.md")):
        files.append({"name": p.name, "path": p, "excerpt": p.read_text(errors="ignore")[:1200]})
    return files


def build_triage_prompt(cfg: dict, files: list[dict]) -> str:
    domains = cfg.get("concept_domains", [])
    listing = "\n\n".join(f"--- {f['name']} ---\n{f['excerpt']}" for f in files)
    return f"""
Categorize each inbox file below for a Growth OS vault. Rules, first match wins:
- frontmatter tags contains "moc" -> MOVE:50-mocs
- frontmatter tags contains "ticket" -> MOVE:20-tickets
- tags contains "#to-read" or content describes a book/article/video/podcast -> MOVE:40-resources
- content is a concept/explanation doc -> MOVE:10-concepts/{{domain}}, domain is the closest
  match from: {", ".join(domains)}
- content is redundant with something that would already exist in the vault -> DELETE
- no clear category -> STUB:10-concepts/{{domain}} (best-guess domain from the list above)

FILES:
{listing}

{TRIAGE_OUTPUT_CONTRACT.strip()}
""".strip()


def parse_triage_response(text: str, files: list[dict]) -> list[dict]:
    m = re.search(r"===PLAN===\s*\n(.*)", text, re.DOTALL)
    body = m.group(1).strip() if m else text.strip()
    by_name = {f["name"]: f for f in files}
    plan = []
    for line in body.splitlines():
        line = line.strip()
        if not line or "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3 or parts[0] not in by_name:
            continue
        plan.append({"name": parts[0], "action": parts[1], "reason": parts[2]})
    return plan


def execute_plan(cfg: dict, plan: list[dict], skip_indices: set[int]) -> dict:
    inbox_dir = config.vault_subdir(cfg, "inbox")
    vault_root = config.vault_root(cfg)
    moved, deleted, skipped = [], [], []
    for i, item in enumerate(plan, start=1):
        src = inbox_dir / item["name"]
        if i in skip_indices:
            skipped.append(item["name"])
            continue
        action = item["action"]
        if action == "DELETE":
            src.unlink(missing_ok=True)
            deleted.append(item["name"])
        elif action.startswith("MOVE:") or action.startswith("STUB:"):
            dest_sub = action.split(":", 1)[1]
            dest_dir = vault_root / dest_sub
            dest_dir.mkdir(parents=True, exist_ok=True)
            src.rename(dest_dir / item["name"])
            moved.append(item["name"])
        else:
            skipped.append(item["name"])
    return {"moved": moved, "deleted": deleted, "skipped": skipped}
