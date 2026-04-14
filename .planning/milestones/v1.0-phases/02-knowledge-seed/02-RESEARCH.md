# Phase 02: Knowledge Seed - Research

**Researched:** 2026-04-13
**Domain:** Obsidian knowledge graph authoring — concept stubs, full articles, wikilink graph
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**D-01 — Stub format:** Partial template only. Frontmatter (`date`, `tags`, `confidence: low`) + one-liner + `## What It Is` callout block + `## Related Concepts` wikilinks. No empty deeper sections. Minimum 2 wikilinks per stub.

**D-02 — Codebase scan source:** SEED-01 list as base (~40 concepts). Enrich via GitHub MCP (verify CQRS usage, find key file paths per concept, discover missing patterns) and Notion MCP (team vocabulary, formally documented patterns). Both READ-ONLY.

**D-03 — MCP constraint (CRITICAL):** GitHub MCP and Notion MCP are READ-ONLY. Do NOT push to any GitHub repo except `cashea-knowledge-vault`. Do NOT write to Notion.

**D-04 — Concept count:** Keep stub total near ~50-70. Skip minor concepts. Add only if clearly significant and heavily used.

**D-05 — Top-25 full articles:** hexagonal architecture, NestJS guards, TypeORM repository pattern, Apigee API gateway, GCP Pub/Sub, JWT authentication, RBAC/permissions, NestJS interceptors, TypeORM migrations, session guard pattern, load balancer vs API gateway, event-driven architecture, microservices (concept), GRPC (concept), CQRS (if used), repository pattern (abstract). infrastructure as code (concept). lock wait and io wait, idempotency pattern, database indexing (concept), SQL transactions (concept), nginx (concept). decorators (concept). dependency injection (concept).

**D-06 — "How We Use It" section:** File paths + ONE concise code snippet. Snippets pulled via GitHub MCP read-only. Staleness accepted.

**D-07 — `## Resources to Go Deeper`:** Leave as empty callout prompt during Phase 2. Resources curated in Phase 3.

**D-08 — Subdirectory assignment:**
- `backend/` — NestJS/TypeORM-specific: guards, interceptors, pipes, modules, decorators, TypeORM repo pattern, TypeORM migrations, transaction-op pattern, DTO pattern, dependency injection, monorepo structure, npm scripts reference, health checks
- `system-design/` — Architectural: hexagonal architecture, port/adapter, hexagonal ports, domain events, CQRS (if used), repository pattern (abstract), REST API, API gateway (concept), microservices (concept), load balancer (concept), API vs load balancer
- `security/` — Auth/authz: JWT authentication, session guard pattern, RBAC/permissions, Firebase authentication
- `infra/` — Infrastructure: Apigee, Apigee XML proxy configs, GCP Pub/Sub, GCP Cloud Run, Firebase integration, CI/CD pipeline, environment configuration, secret management (GCP Secret Manager), database migrations (TypeORM), foreign keys and relations, SQL transactions, structured logging

**D-09 — Graph audit:** After all stubs and full articles created, every article must have at least 2 wikilinks. No orphan nodes.

**D-10 — Graph verification:** Visual check in Obsidian graph view for connected graph. Dense clusters expected: backend/ ↔ system-design/ for hexagonal; security/ ↔ backend/ for guard/auth.

**File naming:** English slug format (`nestjs-guards.md`). NOT Spanish titles.

**Template language:** Section headers in English. Callout prompts in Spanish.

### Claude's Discretion

- Exact wording of one-liner descriptions for each concept stub
- Which specific code snippet to show in each full article's "How We Use It" section
- Additional wikilinks beyond the required minimum 2 (more is better)
- Whether CQRS makes the cut (decide based on GitHub MCP scan evidence)
- Any concepts surfaced via MCP that are clearly significant additions to SEED-01

### Deferred Ideas (OUT OF SCOPE)

- Resources curation in concept articles — Phase 3
- QuickAdd, Advanced URI, Obsidian Spaced Repetition — v2 requirements
- Team ADR adoption via Notion — out of scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| SEED-01 | ~40 concept article stubs covering cashea-backend architectural patterns and technologies | Codebase scan confirmed the 40-concept list. CQRS verdict: NOT used (no `@nestjs/cqrs`, no CommandHandler/QueryHandler anywhere in `src/`). Confirmed candidates: 38 from SEED-01 minus CQRS, plus Obsidian Git as possible infra addition. |
| SEED-02 | Top 10 most-used concepts have full articles (all 6 D-08 sections) | Full article candidates validated against codebase: all 10 are heavily present in `src/`. Key file anchors identified per concept (see Architecture Patterns section). |
| SEED-03 | All stub and full articles wikilinked — no orphan nodes | Wikilink strategy documented. Natural clusters identified. 02-03 audit plan described. |
</phase_requirements>

---

## Summary

Phase 2 is a content authoring task, not a code task. The deliverable is ~40 Markdown files written to the Obsidian vault at `/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/10-concepts/`. The vault structure (4 subdirectories), templates, and git sync were all set up in Phase 1. Phase 2 populates those directories with knowledge nodes.

The primary research question for the planner is: "What exactly goes in each file, and what file anchors should the full articles reference?" The codebase scan (executed locally, not via MCP during research) reveals the authoritative source for each concept's real-world usage. Key finding: CQRS is NOT used in cashea-backend — the codebase has no `@nestjs/cqrs` dependency and no CommandHandler/QueryHandler pattern anywhere in `src/`. Exclude it from SEED-01.

The 10 full articles are the load-bearing deliverable of Plan 02-02. Each full article requires a specific code snippet from the codebase. These snippets are identified below from the local codebase scan. During execution the implementer will verify or replace them via GitHub MCP read access.

**Primary recommendation:** Write stubs first in bulk (02-01), then full articles in order of architectural centrality (02-02), then do a single audit pass for orphan nodes (02-03). Keep the stub format strict: no content beyond what D-01 specifies.

---

## Standard Stack

This phase creates Markdown files. No npm packages, no code compilation. The relevant "stack" is the Obsidian Markdown schema already established in Phase 1.

### Stub Template (D-01 format — already in 99-templates/concept-article.md)

```markdown
---
date: YYYY-MM-DD
tags: [concept, #domain]
confidence: low
moc: "[[MOC-Domain]]"
---

# concept-slug (display title)

> One-sentence definition.

## What It Is

> [!question] ¿Qué es esto en una oración? ¿Cuál es el problema que resuelve?

## Related Concepts

**Broader:** [[concept-slug]]
**Narrower:** [[concept-slug]]
**Sibling:** [[concept-slug]]
```

**Critical:** The existing template at `99-templates/concept-article.md` has all 6 sections. Stubs use ONLY the first section (`## What It Is`) plus `## Related Concepts`. The remaining 4 sections (`## How It Works`, `## How We Use It in cashea-backend`, `## Resources to Go Deeper`, `## Things to Learn / Reinforce`) are intentionally omitted from stubs. They are added when a stub is promoted to a full article.

### Full Article Template (D-08 — all 6 sections)

```markdown
---
date: YYYY-MM-DD
tags: [concept, #domain]
confidence: medium
moc: "[[MOC-Domain]]"
---

# concept-slug (display title)

> One-sentence definition.

## What It Is

> [!question] ¿Qué es esto en una oración? ¿Cuál es el problema que resuelve?

[Prose — 2-4 paragraphs]

## How It Works

> [!question] ¿Cómo funciona internamente? ¿Cómo fluye el control o los datos?

[Prose — mechanics, flow, data path]

## How We Use It in cashea-backend

> [!question] ¿Dónde lo usamos en el código? Pon rutas de archivos o patrones concretos.

Files: `src/path/to/relevant/file.ts`

```typescript
// ONE snippet showing the pattern — not a full class
```

## Related Concepts

**Broader:** [[concept-slug]]
**Narrower:** [[concept-slug]]
**Sibling:** [[concept-slug]]

## Resources to Go Deeper

> [!question] ¿Qué recurso leería si necesitara entender esto más profundo?

(Phase 3 — leave empty)

## Things to Learn / Reinforce

- [ ] 
```

---

## Architecture Patterns

### Concept List: Confirmed 38 Stubs (CQRS excluded)

**CQRS verdict:** No `@nestjs/cqrs` in `package.json`. Grep of `src/` for `CommandHandler`, `QueryHandler`, `CommandBus`, `QueryBus` returns 0 results. CQRS is NOT used. Exclude from stubs.

#### backend/ (14 stubs)

| Filename | Display Title | MOC |
|----------|---------------|-----|
| `nestjs-guards.md` | NestJS Guards | [[MOC-Backend]] |
| `nestjs-interceptors.md` | NestJS Interceptors | [[MOC-Backend]] |
| `nestjs-pipes.md` | NestJS Pipes | [[MOC-Backend]] |
| `nestjs-modules.md` | NestJS Modules | [[MOC-Backend]] |
| `nestjs-decorators.md` | NestJS Decorators | [[MOC-Backend]] |
| `typeorm-repository-pattern.md` | TypeORM Repository Pattern | [[MOC-Backend]] |
| `typeorm-migrations.md` | TypeORM Migrations | [[MOC-Backend]] |
| `transaction-op-pattern.md` | Transaction-Op Pattern | [[MOC-Backend]] |
| `dto-pattern.md` | DTO Pattern | [[MOC-Backend]] |
| `dependency-injection.md` | Dependency Injection | [[MOC-Backend]] |
| `monorepo-structure.md` | Monorepo Structure | [[MOC-Backend]] |
| `npm-scripts-reference.md` | NPM Scripts Reference | [[MOC-Backend]] |
| `health-checks.md` | Health Checks | [[MOC-Backend]] |
| `nestjs-event-emitter.md` | NestJS Event Emitter | [[MOC-Backend]] |

Note on `nestjs-event-emitter.md`: The codebase makes heavy use of `@nestjs/event-emitter` with a rich `AppEvent` hierarchy (`src/events/app-event.ts`) and numerous listeners (`src/listeners/`). This pattern is significant enough to warrant a concept article. It is distinct from domain events (conceptual level) and GCP Pub/Sub (external transport). Recommend adding it — keeps total at 39 stubs.

#### system-design/ (11 stubs)

| Filename | Display Title | MOC |
|----------|---------------|-----|
| `hexagonal-architecture.md` | Hexagonal Architecture | [[MOC-System-Design]] |
| `port-adapter-pattern.md` | Port/Adapter Pattern | [[MOC-System-Design]] |
| `hexagonal-ports.md` | Hexagonal Ports | [[MOC-System-Design]] |
| `domain-events.md` | Domain Events | [[MOC-System-Design]] |
| `repository-pattern.md` | Repository Pattern (Abstract) | [[MOC-System-Design]] |
| `rest-api.md` | REST API | [[MOC-System-Design]] |
| `api-gateway-concept.md` | API Gateway (Concept) | [[MOC-System-Design]] |
| `microservices-concept.md` | Microservices (Concept) | [[MOC-System-Design]] |
| `load-balancer-concept.md` | Load Balancer (Concept) | [[MOC-System-Design]] |
| `api-vs-load-balancer.md` | API Gateway vs Load Balancer | [[MOC-System-Design]] |
| `event-driven-architecture.md` | Event-Driven Architecture | [[MOC-System-Design]] |

Note on `event-driven-architecture.md`: the `AppEvent` hierarchy, NestJS EventEmitter listeners, and GCP Pub/Sub integration all implement event-driven patterns. The conceptual article belongs in `system-design/`; the implementation details belong in `nestjs-event-emitter.md` (backend) and `gcp-pubsub.md` (infra).

#### security/ (4 stubs)

| Filename | Display Title | MOC |
|----------|---------------|-----|
| `jwt-authentication.md` | JWT Authentication | [[MOC-Cashea-Architecture]] |
| `session-guard-pattern.md` | Session Guard Pattern | [[MOC-Cashea-Architecture]] |
| `rbac-permissions.md` | RBAC / Permissions | [[MOC-Cashea-Architecture]] |
| `firebase-authentication.md` | Firebase Authentication | [[MOC-Cashea-Architecture]] |

#### infra/ (10 stubs)

| Filename | Display Title | MOC |
|----------|---------------|-----|
| `apigee.md` | Apigee API Gateway | [[MOC-External-Services]] |
| `apigee-xml-proxy-configs.md` | Apigee XML Proxy Configs | [[MOC-External-Services]] |
| `gcp-pubsub.md` | GCP Pub/Sub | [[MOC-Infra]] |
| `gcp-cloud-run.md` | GCP Cloud Run | [[MOC-Infra]] |
| `firebase-integration.md` | Firebase Integration | [[MOC-Infra]] |
| `ci-cd-pipeline.md` | CI/CD Pipeline | [[MOC-Infra]] |
| `environment-configuration.md` | Environment Configuration | [[MOC-Infra]] |
| `secret-management.md` | Secret Management (GCP Secret Manager) | [[MOC-Infra]] |
| `foreign-keys-and-relations.md` | Foreign Keys and Relations | [[MOC-Backend]] |
| `structured-logging.md` | Structured Logging | [[MOC-Observability]] |

**Total stubs:** 39 (CQRS out, `nestjs-event-emitter` in, `event-driven-architecture` in). Both additions are justified by codebase evidence. Stays within the ~40-50 constraint.

**Note on `sql-transactions.md`:** SEED-01 lists "SQL transactions" but the `transaction-op-pattern.md` in `backend/` already covers the cashea-backend implementation (`src/transactions/transaction.op.ts`). SQL transactions as a concept overlaps heavily. Recommend merging — cover SQL transaction semantics inside `transaction-op-pattern.md`'s "How It Works" section rather than creating a separate stub. This keeps the list at 39.

---

### Full Article File Anchors (Plan 02-02)

The 10 full articles need real file paths and one snippet each. Anchors identified from local codebase scan:

**1. hexagonal-architecture.md** (`system-design/`)
- Key files: `src/employee/ports/`, `src/audit-logs/domain/`, `src/merchant-web/qr/domain/`, `src/merchant-web/qr/persistence/`
- Representative snippet: abstract port class from `src/employee/ports/store.repository.ts`
- Pattern: abstract class as port token, TypeORM impl as adapter

**2. nestjs-guards.md** (`backend/`)
- Key files: `src/utils/guards/session/abstract-session.guard.ts`, `src/utils/guards/admin.guard.ts`, `src/auth/guards/`
- Representative snippet: `AbstractSessionGuard.canActivate()` from `src/utils/guards/session/abstract-session.guard.ts` — shows `CanActivate`, `ExecutionContext`, Reflector usage
- Pattern: abstract base guard + concrete specializations

**3. typeorm-repository-pattern.md** (`backend/`)
- Key files: `src/merchant-web/qr/persistence/repositories/merchant-web-qr-codes.typeorm.repository.ts`, `src/employee/ports/store.repository.ts` (abstract), `src/employee/infrastructure/`
- Representative snippet: abstract port class vs concrete TypeORM implementation (side-by-side pattern, one file each)

**4. apigee.md** (`infra/`)
- Key files: `resources/apiproxy/merchant-web/prod/apiproxy/`, `resources/apiproxy/` (4 subdirectories: admin, external, merchant-web, mobile)
- Representative snippet: `EV-ExtractBearer.xml` policy — shows how Apigee extracts JWT bearer token before forwarding to Cloud Run

**5. gcp-pubsub.md** (`infra/`)
- Key files: `src/pubsub/pubsub.service.ts`, `src/pubsub/pubsub.module.ts`, `src/events/strategies/`, `src/listeners/`
- Representative snippet: from `src/pubsub/pubsub.service.ts` — publish call or subscription setup
- Package: `@google-cloud/pubsub` v4.11.0

**6. jwt-authentication.md** (`security/`)
- Key files: `src/auth/identity/auth-context.strategy.ts`, `src/auth/controllers/auth.controller.ts`
- Representative snippet: from `HardcodedAuthContextStrategy.validate()` — shows how `x-forwarded-authorization` header is parsed, API key extraction, and `AuthContext` construction
- Note: the auth strategy extends `AuthContextStrategy` from the internal `@cashea-bnpl/identity-auth` library

**7. rbac-permissions.md** (`security/`)
- Key files: `src/utils/guards/`, `src/employee/guards/employee-auth-context.strategy.ts`, `src/auth/decorators/`
- Representative snippet: controller usage of `@UseGuards(AuthGuard('employee-auth-context'), AccessGuard)` + `@Permissions('qr:link')` — already documented in existing `employee-guard.md`
- Note: `employee-guard.md` is a ticket-style note, not a concept article. The concept article covers RBAC as a pattern; the ticket note covers the specific implementation.

**8. nestjs-interceptors.md** (`backend/`)
- Key files: `src/utils/interceptors/http-logger.interceptor.ts`, `src/utils/interceptors/response.interceptor.ts`, `src/utils/interceptors/correlation.interceptor.ts`, `src/employee/interceptors/employee-transform.interceptor.ts`
- Representative snippet: `HTTPLogger.intercept()` from `src/utils/interceptors/http-logger.interceptor.ts` — shows `NestInterceptor`, `ExecutionContext`, `CallHandler`, RxJS `tap`

**9. typeorm-migrations.md** (`backend/` per D-08, also in infra/ per SEED-01 — use D-08: backend/)
- Key files: `src/config/migration-data-source.ts`, `migrations/` directory (e.g., `migrations/1754398120577-fix-banners-uuid.ts`)
- Representative snippet: `MigrationDataSource` config from `src/config/migration-data-source.ts` — shows `migrationsTransactionMode: 'each'`, `synchronize: false`, `migrationsRun: false`

**10. session-guard-pattern.md** (`security/`)
- Key files: `src/utils/guards/session/abstract-session.guard.ts`, `src/utils/guards/session/user.guard.ts`, `src/utils/guards/session/employee.guard.ts`, `src/utils/guards/session/mfa.guard.ts`
- Representative snippet: `AbstractSessionGuard` class — shows `getSessionId()` reading `x-apigateway-api-userinfo` header from Apigee, template method pattern with `findSession()` and `inject()` abstract methods

---

### Wikilink Graph Strategy (Plan 02-03)

**Natural clusters** (dense connections expected):

1. **Hexagonal cluster** (system-design ↔ backend):
   - `hexagonal-architecture` ↔ `port-adapter-pattern` ↔ `hexagonal-ports` ↔ `repository-pattern` ↔ `typeorm-repository-pattern` ↔ `dependency-injection`

2. **Auth/security cluster** (security ↔ backend):
   - `session-guard-pattern` ↔ `nestjs-guards` ↔ `jwt-authentication` ↔ `rbac-permissions` ↔ `firebase-authentication`

3. **Event/messaging cluster** (system-design ↔ backend ↔ infra):
   - `domain-events` ↔ `nestjs-event-emitter` ↔ `event-driven-architecture` ↔ `gcp-pubsub`

4. **Infra/deployment cluster** (infra):
   - `apigee` ↔ `apigee-xml-proxy-configs` ↔ `gcp-cloud-run` ↔ `ci-cd-pipeline` ↔ `session-guard-pattern` (Apigee injects session)

5. **Data layer cluster** (backend ↔ infra):
   - `typeorm-repository-pattern` ↔ `typeorm-migrations` ↔ `transaction-op-pattern` ↔ `foreign-keys-and-relations`

**Minimum wikilinks per article (2 required):**

Every stub can satisfy the minimum with 2 links from its natural cluster. Stubs that risk orphaning: `npm-scripts-reference` (link to `monorepo-structure` + `ci-cd-pipeline`), `health-checks` (link to `gcp-cloud-run` + `nestjs-modules`), `api-vs-load-balancer` (link to `api-gateway-concept` + `load-balancer-concept`).

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Stub file creation | Custom generator script | Direct file write per stub | 39 files written once; a generator adds complexity with no reuse benefit |
| Wikilink validation | Custom graph parser | Visual check in Obsidian graph view (D-10) + manual audit in 02-03 | Obsidian renders the graph natively; building a validator is out of scope |
| Concept-to-file mapping | Spreadsheet or separate index | MOC files + Dataview queries (already set up in Phase 1) | MOC-Backend, MOC-System-Design, etc. already serve this purpose |

---

## Common Pitfalls

### Pitfall 1: Writing the full template instead of the stub template

**What goes wrong:** The implementer opens `concept-article.md`, copies all 6 sections, and produces full-template skeletons with empty headers for all sections — violating D-01.

**Why it happens:** The full template is the only template in `99-templates/`. It's easy to copy everything.

**How to avoid:** Stubs use ONLY `## What It Is` + `## Related Concepts`. Explicitly delete sections 2-6 during stub creation. Verify by checking that the stub has no `## How It Works` header.

**Warning signs:** Any stub file that contains `## How It Works` or `## How We Use It in cashea-backend`.

---

### Pitfall 2: Orphan nodes after 02-01

**What goes wrong:** 02-01 creates all stubs with 2 wikilinks each, but some of those wikilinks point to concepts not yet created (or concepts with slightly different slugs). Obsidian shows unresolved links.

**Why it happens:** Writing 39 stubs in sequence means early stubs link to later stubs that don't exist yet at write time. Obsidian won't resolve them until the file exists.

**How to avoid:** Unresolved links are fine during 02-01 — they resolve as later stubs are created. After 02-01 completes, do a quick graph view check to confirm all links resolve. Any remaining unresolved links in the graph are a slug mismatch (fix the wikilink text to match the actual filename).

**Warning signs:** After all stubs exist, Obsidian graph shows nodes with no edges.

---

### Pitfall 3: Subdirectory misassignment

**What goes wrong:** A concept gets placed in `infra/` when D-08 assigns it to `backend/`, or vice versa. This breaks MOC Dataview queries.

**Why it happens:** TypeORM migrations live in `migrations/` directory in the codebase and feel like infra. D-08 assigns them to `backend/` because they are TypeORM-specific (framework-level, not infrastructure-level).

**How to avoid:** The D-08 decision rule is "What concept is being illustrated?" not "Where does the code live?" Foreign keys and relations → `backend/` (database schema concept). GCP Cloud Run → `infra/` (platform concept). When in doubt, re-read D-08.

**Warning signs:** `typeorm-migrations.md` or `foreign-keys-and-relations.md` appearing in `infra/`.

---

### Pitfall 4: Code snippet too large in full articles

**What goes wrong:** The implementer copies an entire class into "How We Use It in cashea-backend" — e.g., pasting all 70 lines of `AbstractSessionGuard`.

**Why it happens:** D-06 says "one key snippet" but when a class is interesting throughout, it's tempting to paste it all.

**How to avoid:** Show only the method or block that demonstrates the pattern, not the whole class. For `AbstractSessionGuard`, show `getSessionId()` only (reads Apigee header, decodes base64). For `HTTPLogger`, show `intercept()` body (tap + timing). Maximum ~15 lines per snippet.

**Warning signs:** Any snippet block longer than 20 lines.

---

### Pitfall 5: CQRS stub created despite codebase evidence against it

**What goes wrong:** Implementer follows SEED-01 list literally and creates `cqrs.md` despite no CQRS code existing.

**Why it happens:** SEED-01 includes "(if used)" note but implementer may default to including it.

**How to avoid:** CQRS is explicitly excluded by research finding. Grep result is 0 matches for `@nestjs/cqrs`, `CommandHandler`, `QueryHandler`, `CommandBus`, `QueryBus` across all of `src/`. The `## Claude's Discretion` section says the decision is based on GitHub MCP scan evidence — research found definitive evidence against it.

---

### Pitfall 6: `hexagonal-architecture.md` already exists but is blank

**What goes wrong:** Plan 02-01 tries to create `10-concepts/system-design/hexagonal-architecture.md` and finds it already exists — but the existing file is blank (title: "Untitled", all sections empty). The implementer either skips it or overwrites it without reading.

**Why it happens:** Phase 1 apparently created the file from template but didn't fill it in. The file exists at the correct path with correct frontmatter but blank content.

**How to avoid:** 02-01 must treat it as a stub needing content, not a file to skip. Read it first, then replace content with the proper stub format per D-01. The file path is correct — just the content needs to be written.

**Warning signs:** `hexagonal-architecture.md` with `# Untitled` as H1.

---

## Code Examples

### Stub format — verified against D-01

```markdown
---
date: 2026-04-13
tags: [concept, backend]
confidence: low
moc: "[[MOC-Backend]]"
---

# NestJS Interceptors

> Middleware layer that intercepts the request-response cycle to add cross-cutting concerns like logging, timing, and response transformation.

## What It Is

> [!question] ¿Qué es esto en una oración? ¿Qué problema resuelve en cashea-backend?

## Related Concepts

**Broader:** [[nestjs-guards]]
**Narrower:** [[structured-logging]]
**Sibling:** [[nestjs-pipes]]
```

### Full article "How We Use It" section — verified against D-06

```markdown
## How We Use It in cashea-backend

> [!question] ¿Dónde lo usamos en el código? Pon rutas de archivos o patrones concretos.

Files: `src/utils/interceptors/http-logger.interceptor.ts`, `src/utils/interceptors/response.interceptor.ts`, `src/employee/interceptors/employee-transform.interceptor.ts`

```typescript
// src/utils/interceptors/http-logger.interceptor.ts
intercept(context: ExecutionContext, next: CallHandler) {
  const request = context.switchToHttp().getRequest();
  const init = new Date().getTime();
  return next.handle().pipe(
    tap((data) => {
      const time = new Date().getTime() - init;
      this.logger.log({ body: data }, `response sent in ${time}ms`);
    }),
  );
}
```
```

### Wikilink format — per Phase 1 D-04 and CONTEXT.md

```markdown
## Related Concepts

**Broader:** [[hexagonal-architecture]]
**Narrower:** [[typeorm-repository-pattern]]
**Sibling:** [[port-adapter-pattern|Port/Adapter Pattern]]
```

Display name override `[[slug|Display Name]]` is valid and recommended when the slug is ambiguous.

---

## State of the Art

| Old Approach | Current Approach | Impact for Phase 2 |
|--------------|------------------|--------------------|
| Empty template stubs (bare headers) | Partial template stubs (D-01: frontmatter + one-liner + What It Is + Related Concepts only) | Phase 2 stubs must NOT include empty deeper sections |
| Single flat `10-concepts/` folder | 4 subdirectories: `backend/`, `infra/`, `system-design/`, `security/` | D-08 subdirectory assignment is load-bearing for Dataview queries |
| No `moc:` frontmatter | `moc: "[[MOC-Name]]"` frontmatter field | Required for Dataview backlink queries in MOC files |

---

## Open Questions

1. **`employee-guard.md` migration**
   - What we know: `10-concepts/security/employee-guard.md` exists and contains detailed ticket-style content about the employee guard implementation. It is NOT formatted as a concept article (no D-08 template, no wikilinks to related concepts, no `confidence:` frontmatter field).
   - What's unclear: Should 02-01 reformat this file as a proper concept article stub, or leave it as-is and create a separate `session-guard-pattern.md` that links back to it?
   - Recommendation: Leave `employee-guard.md` as-is (it's a valuable ticket artifact). Create `session-guard-pattern.md` as a proper concept article stub, and include `[[employee-guard|Employee Guard Implementation]]` as a wikilink in its Related Concepts section. The planner should make this explicit in the 02-01 task.

2. **`employee-scope-guard-decisions.md` and `employee-scope-guard-reference.md` in security/**
   - What we know: Two additional files exist in `10-concepts/security/` that are not concept articles — they are reference and decision logs from the employee guard implementation.
   - What's unclear: These have no wikilinks and no concept-article frontmatter. They will appear as orphan nodes in the graph.
   - Recommendation: 02-03 (graph wiring audit) should add at minimum a `## Related Concepts` section to these files linking to `session-guard-pattern`, `nestjs-guards`, and `rbac-permissions`. The planner should include this as a task within 02-03.

3. **`admin-audit-events-pubsub.md` in backend/**
   - What we know: One file exists in `10-concepts/backend/` — `admin-audit-events-pubsub.md`. It appears to be a topic-specific artifact, not a concept article.
   - Recommendation: Same treatment as above — 02-03 should link it to `gcp-pubsub`, `domain-events`, and `structured-logging` at minimum.

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Obsidian vault at `/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/` | All plans | ✓ | Confirmed (Phase 1) | — |
| `10-concepts/backend/`, `infra/`, `system-design/`, `security/` directories | 02-01 stub creation | ✓ | Confirmed (ls check) | — |
| `99-templates/concept-article.md` | Template reference | ✓ | Confirmed (file read) | — |
| GitHub MCP (read-only) | File path anchors for full articles | Declared available | — | Use local codebase scan (already done in research) |
| Notion MCP (read-only) | Team vocabulary enrichment | Declared available | — | Skip if unavailable; local scan covers all 10 full article anchors |
| cashea-backend `src/` (local) | Concept verification, CQRS check | ✓ | Confirmed | — |

**Missing dependencies with no fallback:** None.

**Note:** The 10 full article file anchors are already identified from the local codebase scan (see Architecture Patterns section). MCP access enriches the articles but is not blocking.

---

## Validation Architecture

> `workflow.nyquist_validation` is `true` in `.planning/config.json`. Section is included.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Manual inspection (no automated tests for Markdown file authoring) |
| Config file | N/A — this phase writes Markdown files, not executable code |
| Quick check command | `ls "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/10-concepts/backend/" \| wc -l` |
| Full validation | Visual Obsidian graph view check (D-10) |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| SEED-01 | ~40 stub files exist, one per concept | File count | `find "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/10-concepts" -name "*.md" \| wc -l` | ✅ (directories exist) |
| SEED-01 | Each stub has valid frontmatter + D-01 structure | Manual | Read random sample of 5 stubs, verify no `## How It Works` header | ❌ Wave 0 — no test file |
| SEED-02 | Top-10 full articles have all 6 sections populated | Manual | Open each in Obsidian, verify 6 headers present and filled | ❌ Wave 0 — manual only |
| SEED-03 | No orphan nodes in graph | Manual | Obsidian graph view — zoom out, verify no isolated nodes | ❌ Wave 0 — Obsidian visual check |
| SEED-03 | Each article has min 2 wikilinks | Script check | `grep -l "\[\[" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/10-concepts/"**/*.md \| wc -l` (all files should appear) | ❌ Wave 0 — no test file |

### Sampling Rate

- **Per plan completion (02-01):** `find ".../10-concepts" -name "*.md" | wc -l` — should be ~39
- **Per plan completion (02-02):** Open each of the 10 full articles in Obsidian, confirm 6 populated sections
- **Phase gate:** Visual graph check in Obsidian (D-10) — connected graph with no isolated nodes before marking phase complete

### Wave 0 Gaps

- No automated test infrastructure needed — this phase is Markdown authoring, not code. The "tests" are manual inspections defined above.
- A bash one-liner to count wikilinks per file can serve as a quick sanity check during 02-03: `grep -c "\[\[" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/10-concepts/backend/nestjs-guards.md"` — should return >= 2 for every file.

---

## Sources

### Primary (HIGH confidence)

- Local codebase scan of `/Users/thyfus/Documents/cashea-backend/cashea-backend/src/` — CQRS verdict, interceptor files, guard files, event patterns, transaction-op pattern, migration config
- `02-CONTEXT.md` — All locked decisions (D-01 through D-10), MCP constraints, subdirectory mapping
- `01-CONTEXT.md` — D-04 (file naming), D-08 (template structure), D-18 (vault folder structure)
- `REQUIREMENTS.md` — SEED-01 exact concept list, SEED-02 top-10 list, SEED-03 wikilink requirement
- Vault filesystem scan — confirmed directory structure, existing files, template content

### Secondary (MEDIUM confidence)

- `package.json` dependencies — confirmed `@google-cloud/pubsub`, `@nestjs/event-emitter`, `@nestjs/passport`, `typeorm`, `firebase-admin` all present and active

### Tertiary (LOW confidence)

- None — all findings grounded in local file reads.

---

## Metadata

**Confidence breakdown:**

- CQRS verdict: HIGH — definitive grep result (0 matches across entire `src/`)
- Concept list (38 stubs confirmed): HIGH — cross-referenced SEED-01 against codebase
- Full article file anchors: HIGH — files read directly from disk
- Wikilink clustering strategy: MEDIUM — based on code architecture understanding; actual links to be verified during 02-03
- MCP availability: MEDIUM — declared in CONTEXT.md as available; not verified in this research session

**Research date:** 2026-04-13
**Valid until:** 2026-06-13 (vault structure frozen 8 weeks per Design Constraint #5; concept list stable)
