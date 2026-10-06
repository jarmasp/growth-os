"""Ports workflows/onboarding.md + agents/onboarding-agent.md. Unlike reflect/
premortem/weekly, this interview is genuinely adaptive — the agent picks each next
question from what was just said, per its own 5-phase branching logic. That can't be
flattened into a fixed input() loop without losing the thing that makes it useful.

So this is the one place Phase 1's "interview in Python, one model call" pattern
doesn't apply: the model is in the loop every turn, replaying the growing transcript
each time (stateless calls, stateful behavior) — acceptable because onboarding runs
once per person, or rarely on profile updates, not per ticket.
"""
import json
import re
from datetime import date
from pathlib import Path

from . import backend, config, tokens, vault

PROTOCOL = """
PROTOCOL — you are mid-conversation with the user, conducting the interview in
<interview> phase by phase. Respond with EXACTLY ONE of these, nothing else:

QUESTION: <the single next question to ask right now, nothing else on the line>

or, once all 5 phases have been genuinely covered (do not cut the interview short):

SUMMARY:
<the full confirmation block from <synthesis>, exactly as specified, starting at
the ━━━ line and ending at the ━━━ line>

Never output both in the same response. No commentary outside the marker.
"""

CONFIRM_WORDS = ("ok", "okay", "listo", "dale", "si", "sí", "yes")


def _call(agent: str, cfg: dict, persona: str, transcript: str) -> tuple[str, object]:
    text_prompt = f"{persona}\n\n{PROTOCOL.strip()}\n\nCONVERSATION SO FAR:\n{transcript or '(none yet — this is the first message)'}"
    result = backend.run(agent, text_prompt, cfg)
    entry = tokens.log("onboard", agent, text_prompt, result)
    print(f"  [{tokens.summarize(entry)}]")
    return result.text.strip(), result


def run_interview(agent: str, cfg: dict) -> dict | None:
    persona = config.agent_path("onboarding-agent.md").read_text()
    transcript = ""

    while True:
        reply, _ = _call(agent, cfg, persona, transcript)

        if reply.upper().startswith("QUESTION:"):
            question = reply.split(":", 1)[1].strip()
            answer = input(f"\n{question}\n\n> ").strip()
            transcript += f"\nASSISTANT: {question}\nUSER: {answer}\n"
            continue

        if reply.upper().startswith("SUMMARY:"):
            summary = reply.split(":", 1)[1].strip()
            print(f"\n{summary}\n")
            reply2 = input("¿Esto te representa? (ok / indica qué cambiar) ").strip()
            if reply2.lower() in CONFIRM_WORDS:
                transcript += f"\nASSISTANT: {summary}\nUSER CONFIRMED: {reply2}\n"
                break
            transcript += f"\nASSISTANT: {summary}\nUSER CORRECTION: {reply2}\n"
            continue

        print(f"Unexpected response from the model, retrying:\n{reply}")
        return None

    # Final call: extract the confirmed profile as pure JSON.
    final_prompt = (f"{persona}\n\nCONVERSATION SO FAR:\n{transcript}\n\n"
                     "The user just confirmed the summary. Output ONLY the JSON object "
                     "specified in <output>, nothing else — no markdown fences, no commentary.")
    result = backend.run(agent, final_prompt, cfg)
    entry = tokens.log("onboard", agent, final_prompt, result)
    print(f"  [{tokens.summarize(entry)}]")

    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", result.text.strip())
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Could not parse profile JSON: {e}\nRaw:\n{result.text}")
        return None


# ---------------------------------------------------------------------------
# write_profile — deterministic merge into config.json

def write_profile(profile: dict) -> Path:
    cfg_path = config.config_path()
    cfg = json.loads(cfg_path.read_text())
    cfg["user_profile"] = profile
    if profile.get("priority_domains"):
        cfg["concept_domains"] = profile["priority_domains"]
    if profile.get("company") and profile.get("role"):
        cfg.setdefault("project_name", profile.get("company", "your project"))
    cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    return cfg_path


# ---------------------------------------------------------------------------
# setup_vault — deterministic scaffolding, direct port of onboarding.md's own
# embedded python blocks.

STANDARD_FOLDERS = ["00-inbox", "20-tickets", "30-weekly", "40-resources", "50-mocs", "99-templates"]


def scaffold_vault(cfg: dict) -> list[str]:
    report = []
    vault = config.vault_root(cfg)
    if not vault.is_dir():
        return [f"SKIPPED — vault_root does not exist on disk: {vault}. "
                f"Create your Obsidian vault first, then re-run `growth onboard`."]

    for folder in STANDARD_FOLDERS:
        (vault / folder).mkdir(parents=True, exist_ok=True)
    for domain in cfg.get("concept_domains", []):
        (vault / "10-concepts" / domain).mkdir(parents=True, exist_ok=True)
    project_docs_root = cfg.get("vault", {}).get("project_docs", "60-project")
    for sub in cfg.get("project_docs_subfolders", ["adr", "modules", "domain", "business", "runbooks"]):
        (vault / project_docs_root / sub).mkdir(parents=True, exist_ok=True)
    report.append(f"Folders: {', '.join(STANDARD_FOLDERS)}, 10-concepts/{{{', '.join(cfg.get('concept_domains', []))}}}")

    templates_src = config.GROWTH_OS_HOME / "templates"
    templates_dst = vault / "99-templates"
    templates_dst.mkdir(parents=True, exist_ok=True)
    installed = 0
    for src in templates_src.glob("*.md"):
        dst = templates_dst / src.name
        if dst.exists():
            continue
        dst.write_text(src.read_text().replace("YOUR_VAULT_NAME", cfg.get("vault_name", "vault")))
        installed += 1
    report.append(f"Templates: {installed} installed in 99-templates/")

    starters = 0
    homework_log = vault / "homework-log.md"
    if not homework_log.exists():
        homework_log.write_text(f"""---
date: {date.today().isoformat()}
tags: [homework]
---

# Homework Log

Persistent task backlog for deliberate practice drills. Tasks carry forward across
weeks until done. Add your recurring drills below — they will be surfaced by `growth weekly`.

## Recurring Drills

<!-- One drill per line. Format: - [ ] [Name] — [description] — 🔁 [frequency] -->

## One-off Tasks

<!-- Practice tasks with no recurrence. Remove when done. -->
""")
        starters += 1
    ledger = vault / "reflection-scores.md"
    if not ledger.exists():
        ledger.write_text(vault_module_ledger_header())
        starters += 1
    report.append(f"Starters: {starters} created (homework-log.md, reflection-scores.md)")

    mocs_dir = vault / "50-mocs"
    mocs_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    moc_count = 0
    for domain in cfg.get("concept_domains", []):
        title = domain.replace("-", " ").title()
        moc_path = mocs_dir / f"MOC-{title}.md"
        if moc_path.exists():
            continue
        moc_path.write_text(f"""---
date: {today}
tags: [moc]
---

# MOC — {title}

```dataview
LIST
FROM "{cfg.get('vault_name', 'vault')}/10-concepts/{domain}"
SORT file.mtime DESC
```
""")
        moc_count += 1

    moc_project = mocs_dir / "MOC-Project.md"
    if not moc_project.exists():
        project_docs_root = cfg.get("vault", {}).get("project_docs", "60-project")
        subs = cfg.get("project_docs_subfolders", ["adr", "modules", "domain", "business", "runbooks"])
        sections = "\n\n".join(
            f'## {sub.title()}\n\n```dataview\nLIST\nFROM "{cfg.get("vault_name", "vault")}/{project_docs_root}/{sub}"\nSORT file.mtime DESC\n```'
            for sub in subs
        )
        moc_project.write_text(f"""---
date: {today}
tags: [moc, project-doc]
---

# MOC — Project Docs

Documentación específica del proyecto. Separada del aprendizaje personal.

{sections}
""")
        moc_count += 1
    report.append(f"MOCs: {moc_count} created in 50-mocs/")
    return report


def vault_module_ledger_header() -> str:
    # ponytail: reuses the exact ledger header reflect's own ledger writes, so a
    # vault scaffolded here and one created lazily by `growth reflect` are identical.
    return vault.LEDGER_HEADER


# ---------------------------------------------------------------------------
# write_vault_note — renders the confirmed JSON profile, no further model call

PROFILE_NOTE_TEMPLATE = """---
date: {date}
tags: [meta, profile]
---

# Growth OS — Perfil de usuario

> Este perfil se generó a través del onboarding del Growth OS.
> Actualizarlo con `growth onboard` cuando tu contexto cambie significativamente.

## Identidad

- **Nombre:** {name}
- **Rol:** {role} en {company}
- **Herramientas/medios:** {primary_tools}
- **Experiencia:** {experience_years} años — nivel Dreyfus: {dreyfus_level}

## Hacia dónde voy

**Objetivo 12–18m:** {primary_goal}

**Motor principal:** {motivation_type}

**Señal de flow:** {flow_signal}

## ¿Qué me frena?

{blockers}

**Competing commitment:** {competing_commitment}

**Tensión identificada:** {identified_tension}

## Cómo aprendo

**Estilo:** {learning_style}

**Etapa Kolb que omite:** {kolb_skipped_stage}

## Por qué este oficio

{craft_motivation}

## Dominios prioritarios

{priority_domains}
"""


def write_profile_note(cfg: dict, profile: dict) -> Path:
    # ponytail: `.get(key, "—")` only falls back when the key is MISSING, not when
    # it's present and explicitly null (which the model does for optional fields
    # like name) -- `.get(key) or "—"` covers both, used uniformly below.
    vault_root = config.vault_root(cfg)
    note = PROFILE_NOTE_TEMPLATE.format(
        date=date.today().isoformat(),
        name=profile.get("name") or "—", role=profile.get("role") or "—",
        company=profile.get("company") or "—",
        primary_tools=", ".join(profile.get("primary_tools") or []) or "—",
        experience_years=profile.get("experience_years") if profile.get("experience_years") is not None else "—",
        dreyfus_level=profile.get("dreyfus_level") or "—",
        primary_goal=profile.get("primary_goal") or "—",
        motivation_type=profile.get("motivation_type") or "—",
        flow_signal=profile.get("flow_signal") or "—",
        blockers="\n".join(f"- {b}" for b in (profile.get("blockers") or [])) or "- —",
        competing_commitment=profile.get("competing_commitment") or "—",
        identified_tension=profile.get("identified_tension") or "—",
        learning_style=profile.get("learning_style") or "—",
        kolb_skipped_stage=profile.get("kolb_skipped_stage") or "ninguna clara",
        craft_motivation=profile.get("craft_motivation") or "—",
        priority_domains="\n".join(f"- {d}" for d in (profile.get("priority_domains") or [])) or "- —",
    )
    path = vault_root / "user-profile.md"
    path.write_text(note)
    return path
