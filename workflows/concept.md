<purpose>

Write or expand a concept article in the Obsidian vault.
New concepts get a full 6-section article seeded with real codebase evidence.
Existing stubs get expanded. Existing full articles get specific sections updated.

</purpose>

<process>

<step name="setup">

```bash
VAULT=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_root'])")
PROJECT_NAME=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c.get('project_name','your project'))")
CONCEPT_DOMAINS=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c.get('concept_domains', []))")
CONCEPTS_DIR="$VAULT/10-concepts"
```

**Resolve slug** from `$ARGUMENTS`: lowercase, hyphens (e.g. "NestJS interceptors" → `nestjs-interceptors`).

**Determine domain**: read `concept_domains` from config.json and choose the closest match. If no match, default to the first domain in the list.

</step>

<step name="check_existing">

```bash
find "$CONCEPTS_DIR" -name "*{slug}*" 2>/dev/null
```

- **Not found**: create new full article.
- **Stub found** (has one-liner but sections are empty/minimal): expand to full article.
- **Full article found**: report current state, ask which section to update.

</step>

<step name="gather_codebase_evidence">

If a project codebase is available (check `project_name` from config.json), search for real usage:

```bash
# Search for the concept in source — language-agnostic, excludes common dep/build noise
grep -rn "{keyword}" . \
  --exclude-dir={.git,node_modules,dist,build,vendor,.venv,target} \
  -l 2>/dev/null | head -8
```

Read 1–2 of the most relevant files to extract:
- Real file paths that use this concept
- Concrete usage pattern (not generic description)
- Any quirks specific to this codebase

If invoked outside a codebase: skip search, note "no codebase context."

</step>

<step name="write_article">

Use this exact structure:

```markdown
---
date: {YYYY-MM-DD}
tags: [concept, #{domain}]
confidence: {low|medium|high}
moc: "[[MOC-{Domain}]]"
---

# {Concept Name}

> {One-sentence definition — what it is and why it exists.}

## What It Is

{2–3 sentences. No jargon in the first sentence.}

## How It Works

{Internal mechanics. Control flow, data flow, execution order. Concrete, not abstract.}

## How We Use It in {project_name}

{Real file paths, patterns, or examples from the project. If no project context:
"Not yet encountered in {project_name} — update when first used."}

## Related Concepts

**Broader:** [[{parent-concept}]]
**Narrower:** [[{child-concept}]]
**Sibling:** [[{peer-concept}]]

## Resources to Go Deeper

- Official: {NestJS docs > Guards / relevant section}
- Deep: {book or article — from 40-resources if applicable}
- Mental model: {one-sentence analogy}

## Things to Learn / Reinforce

- [ ] {specific gap or exercise derived from codebase usage}
- [ ] {something to try or verify}
```

**Confidence**:
- `low` — written from general knowledge, no codebase evidence
- `medium` — backed by real usage found in codebase
- `high` — deeply understood, production-tested

</step>

<step name="write_and_report">

**Path**: `$CONCEPTS_DIR/{domain}/{slug}.md`

Overwrite if stub. Report section diff if expanding.

Report:
```
Concept written: 10-concepts/{domain}/{slug}.md
Wikilinks added: [[x]] → [[y]]
Confidence: {level}
```

If wikilinks in Related Concepts don't exist as files yet, note them as candidates for `/growth:concept {slug}`.

</step>

</process>

<rules>

- Always add at least 2 wikilinks in Related Concepts — no orphan nodes.
- "How We Use It in {project_name}" must have real paths or examples when project context is available.
- Never leave all sections empty — fill what can be filled, mark gaps with `[ ]` in Things to Learn.
- Confidence starts at `low`. Only `medium` or `high` with evidence.

</rules>
