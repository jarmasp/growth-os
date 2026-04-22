<purpose>

Run the Growth OS onboarding interview and write the resulting user profile to config.json.
Runs once when setting up a new Growth OS instance, or on demand to update the profile.

The onboarding agent conducts an adaptive 4–5 question interview based on coaching and
vocational psychology frameworks. It is not a replacement for a professional. Its output
is a structured profile that personalizes all future workflows (/growth:reflect, /growth:weekly, /growth:concept).

</purpose>

<process>

<step name="setup">

```bash
cat ~/Documents/growth-os/config.json
```

Check if `user_profile` key already exists in config.json:
- If present: set `FIRST_RUN=false`. Show current profile and ask:
  ```
  Ya tienes un perfil guardado. ¿Quieres actualizarlo (responde "actualizar")
  o salir sin cambios (cualquier otra cosa)?
  ```
  If not "actualizar" → exit.
  If "actualizar" → continue with interview, will overwrite profile at the end.
  Note: in update mode, vault scaffolding is skipped — only config.json and user-profile.md are updated.

- If absent: set `FIRST_RUN=true`. Greet the user:
  ```
  Bienvenido al Growth OS.

  Antes de configurar tu sistema, quiero entender quién eres y hacia dónde vas.
  Voy a hacerte 4–5 preguntas. No hay respuestas correctas ni incorrectas.
  Sé tan honesto como puedas — el sistema funciona mejor cuanto más real sea el perfil.

  Esto no reemplaza a un coach o psicólogo. Es una orientación para que tu sistema
  de crecimiento apunte hacia lo que genuinamente importa.

  ¿Listo? Empecemos.
  ```

</step>

<step name="interview">

Load and follow the onboarding agent:
`~/Documents/growth-os/agents/onboarding-agent.md`

The agent conducts the interview, synthesizes the profile, and waits for user confirmation.
Do not proceed to the next step until the user confirms the profile with "ok" or equivalent.

Capture the confirmed JSON profile object returned by the agent as `PROFILE_JSON`.

</step>

<step name="write_profile">

Read the current config.json:
```bash
cat ~/Documents/growth-os/config.json
```

Merge `PROFILE_JSON` into config.json under the key `"user_profile"`.
Use Python to merge — do not overwrite the entire file:

```bash
python3 - <<'PY'
import json, pathlib

config_path = pathlib.Path.home() / "Documents/growth-os/config.json"
config = json.loads(config_path.read_text())

profile = PROFILE_JSON  # injected by workflow

config["user_profile"] = profile

# Sync concept_domains from priority_domains so workflows stay consistent
if profile.get("priority_domains"):
    config["concept_domains"] = profile["priority_domains"]

# Sync project_name if provided
if profile.get("company") and profile.get("role"):
    config.setdefault("project_name", profile.get("company", "your project"))

config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n")
print("Profile written.")
PY
```

</step>

<step name="setup_vault">

**If `FIRST_RUN=false` (profile update run): skip this entire step.**
Output: `Vault scaffolding skipped — updating profile only.`

Scaffold the Obsidian vault on first-time setup only.
Read from the now-updated config.json:

```bash
VAULT=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_root'])")
VAULT_NAME=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_name'])")
GROWTH_OS="$HOME/Documents/growth-os"
DATE=$(date +"%Y-%m-%d")
```

**1. Create folder structure** — skip if folders already exist:

```bash
python3 - <<'PY'
import json, pathlib

config = json.loads(pathlib.Path.home().joinpath("Documents/growth-os/config.json").read_text())
vault = pathlib.Path(config["vault_root"])

# Standard vault folders
standard = ["00-inbox", "20-tickets", "30-weekly", "40-resources", "50-mocs", "99-templates"]
for folder in standard:
    (vault / folder).mkdir(parents=True, exist_ok=True)

# Concept domain subfolders
for domain in config.get("concept_domains", []):
    (vault / "10-concepts" / domain).mkdir(parents=True, exist_ok=True)
    print(f"  Created: 10-concepts/{domain}/")

# Project docs folder (60-project) with subfolders
project_docs_root = config.get("vault", {}).get("project_docs", "60-project")
for sub in config.get("project_docs_subfolders", ["adr", "modules", "domain", "business", "runbooks"]):
    (vault / project_docs_root / sub).mkdir(parents=True, exist_ok=True)
    print(f"  Created: {project_docs_root}/{sub}/")
PY
```

**2. Install customized templates** — copy each file from `growth-os/templates/` to
`{vault}/99-templates/`, substituting `YOUR_VAULT_NAME` with the real `vault_name`:

```bash
python3 - <<'PY'
import json, pathlib, re

config = json.loads(pathlib.Path.home().joinpath("Documents/growth-os/config.json").read_text())
vault = pathlib.Path(config["vault_root"])
vault_name = config["vault_name"]
growth_os = pathlib.Path.home() / "Documents/growth-os"
templates_src = growth_os / "templates"
templates_dst = vault / "99-templates"

for src in templates_src.glob("*.md"):
    dst = templates_dst / src.name
    if dst.exists():
        print(f"  Template exists, skipping: {src.name}")
        continue
    content = src.read_text()
    content = content.replace("YOUR_VAULT_NAME", vault_name)
    dst.write_text(content)
    print(f"  Template installed: {src.name}")
PY
```

**3. Create starter files** — only if they do not already exist:

**homework-log.md** at vault root:
```markdown
---
date: {DATE}
tags: [homework]
---

# Homework Log

Persistent task backlog for deliberate practice drills. Tasks carry forward across
weeks until done. Add your recurring drills below — they will be surfaced by /growth:weekly.

## Recurring Drills

<!-- One drill per line. Format: - [ ] [Name] — [description] — 🔁 [frequency] -->

## One-off Tasks

<!-- Practice tasks with no recurrence. Remove when done. -->
```

**reflection-scores.md** at vault root — use the canonical ledger format:
```markdown
# Reflection Score Ledger

Append a row after every scored reflection. One row per `/growth:reflect` run. Total = sum of D1..D5.

Dimension maxima: D1 Cognitive Depth (3) · D2 Cycle Completeness (2) · D3 Loop Depth (2) · D4 Actionability (2) · D5 Linguistic Quality (1) · Total (10)

| Date | Ticket | Total | D1 | D2 | D3 | D4 | D5 | Branch |
|------|--------|-------|----|----|----|----|----|--------|
```

**4. Create MOC stub files** — one per concept domain + one for project docs, only if file does not exist:

For each domain in `concept_domains`, write `$VAULT/50-mocs/MOC-{Domain}.md`:
```markdown
---
date: {DATE}
tags: [moc]
---

# MOC — {Domain}

```dataview
LIST
FROM "{VAULT_NAME}/10-concepts/{domain}"
SORT file.mtime DESC
```
```

Use Python to generate all MOC files:
```bash
python3 - <<'PY'
import json, pathlib

config = json.loads(pathlib.Path.home().joinpath("Documents/growth-os/config.json").read_text())
vault = pathlib.Path(config["vault_root"])
vault_name = config["vault_name"]
mocs_dir = vault / "50-mocs"
from datetime import date
today = date.today().isoformat()

for domain in config.get("concept_domains", []):
    title = domain.replace("-", " ").title()
    moc_path = mocs_dir / f"MOC-{title}.md"
    if moc_path.exists():
        print(f"  MOC exists, skipping: {moc_path.name}")
        continue
    content = f"""---
date: {today}
tags: [moc]
---

# MOC — {title}

\`\`\`dataview
LIST
FROM "{vault_name}/10-concepts/{domain}"
SORT file.mtime DESC
\`\`\`
"""
    moc_path.write_text(content)
    print(f"  MOC created: {moc_path.name}")

# Project docs MOC
project_docs_root = config.get("vault", {}).get("project_docs", "60-project")
subs = config.get("project_docs_subfolders", ["adr", "modules", "domain", "business", "runbooks"])
moc_project = mocs_dir / "MOC-Project.md"
if not moc_project.exists():
    sections = "\n\n".join(
        f"## {sub.title()}\n\n```dataview\nLIST\nFROM \"{vault_name}/{project_docs_root}/{sub}\"\nSORT file.mtime DESC\n```"
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
    print("  MOC created: MOC-Project.md")
PY
```

**5. Report scaffold results:**
```
Vault scaffolded:
  Folders:   00-inbox, 10-concepts/{domains}, 20-tickets, 30-weekly, 40-resources, 50-mocs, 99-templates
  Templates: {N} installed in 99-templates/
  Starters:  homework-log.md, reflection-scores.md
  MOCs:      {N} created in 50-mocs/
```

Skip this step entirely (with a note) if `vault_root` does not exist on disk — the user
needs to create the Obsidian vault first and re-run `/growth:onboard`.

</step>

<step name="write_vault_note">

Resolve vault path from config.json. Write a profile note to the vault root:

```bash
VAULT=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_root'])")
```

Write `$VAULT/user-profile.md` with this structure:

```markdown
---
date: {YYYY-MM-DD}
tags: [meta, profile]
---

# Growth OS — Perfil de usuario

> Este perfil se generó a través del onboarding del Growth OS.
> Actualizarlo con `/growth:onboard` cuando tu contexto cambie significativamente.

## Identidad

- **Nombre:** {name}
- **Rol:** {role} en {company or context}
- **Herramientas/medios:** {primary_tools}
- **Experiencia:** {experience_years} años — nivel Dreyfus: {dreyfus_level}

## Hacia dónde voy

**Objetivo 12–18m:** {primary_goal}

**Motor principal:** {motivation_type} — {motivation explanation}

**Señal de flow:** {flow_signal or "—"}

## ¿Qué me frena?

{blockers as bullet list}

**Competing commitment:** {competing_commitment or "—"}

**Tensión identificada:** {identified_tension or "—"}

## Cómo aprendo

**Estilo:** {learning_style} — {evidence sentence from interview}

**Etapa Kolb que omite:** {kolb_skipped_stage or "ninguna clara"}

## Por qué este oficio

{craft_motivation}

## Dominios prioritarios

{priority_domains as bullet list}
```

If the file already exists: overwrite it (onboarding update case).

</step>

<step name="report">

Output:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Onboarding completo.

  Perfil guardado en: ~/Documents/growth-os/config.json
  Nota de vault:      {VAULT}/user-profile.md

  Próximos pasos:
  · Abre Obsidian — las carpetas y templates ya están instalados
  · Activa el plugin Templater y apúntalo a 99-templates/ en tu vault
  · Corre /growth:reflect después de tu próximo ticket o proyecto
  · Corre /growth:weekly al final de esta semana
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

</step>

</process>

<rules>

- Never write partial profile data. If the user abandons mid-interview, exit cleanly with no writes.
- Never infer fields the user didn't address — leave them as null in the JSON, not guessed.
- If the user corrects the synthesized profile, update every affected field before writing.
- The vault note is human-readable context — the config.json entry is machine-readable context for workflows. Both must be consistent after this workflow completes.
- setup_vault is idempotent — running /growth:onboard again must not overwrite existing notes or templates, only create what's missing.
- If vault_root does not exist on disk, skip setup_vault and report clearly: "Vault path not found — create your Obsidian vault first, then re-run /growth:onboard."

</rules>
