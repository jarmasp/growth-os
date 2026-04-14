<purpose>

Write or expand a concept article in the Obsidian vault.
New concepts get a full 6-section article seeded with real codebase evidence.
Existing stubs get expanded. Existing full articles get specific sections updated.

</purpose>

<process>

<step name="setup">

```bash
VAULT=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_root'])")
CONCEPTS_DIR="$VAULT/10-concepts"
```

**Resolve slug** from `$ARGUMENTS`: lowercase, hyphens (e.g. "NestJS interceptors" → `nestjs-interceptors`).

**Determine domain** from concept type:
- `backend` — NestJS, TypeORM, patterns (guards, interceptors, pipes, modules, DI)
- `security` — auth, JWT, guards, RBAC, sessions
- `system-design` — architecture, CQRS, event-driven, distributed systems
- `infra` — GCP, Cloud Run, Pub/Sub, CI/CD, secrets

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

If invoked from cashea-backend (or any codebase), search for real usage:

```bash
# Search for the concept in source
grep -r "{keyword}" src/ --include="*.ts" -l 2>/dev/null | head -8
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

## How We Use It in cashea-backend

{Real file paths and patterns. E.g.:}
`src/modules/auth/guards/employee.guard.ts` — implements CanActivate; checks token via AuthService.

{If no codebase context: "Not yet encountered in cashea-backend — update when first used."}

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

If wikilinks in Related Concepts don't exist as files yet, note them as candidates for `/concept {slug}`.

</step>

</process>

<rules>

- Always add at least 2 wikilinks in Related Concepts — no orphan nodes.
- "How We Use It in cashea-backend" must have real paths when codebase is available.
- Never leave all sections empty — fill what can be filled, mark gaps with `[ ]` in Things to Learn.
- Confidence starts at `low`. Only `medium` or `high` with evidence.

</rules>
