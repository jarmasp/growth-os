"""growth — the CLI entry point. Each growth:* command's shape matches the
judgment it actually needs: premortem/reflect/weekly's fixed Q&A is parsed
straight out of workflows/*.md (not duplicated); concept/reflect/weekly make
one stateless model call; onboard alone is multi-turn (its interview is
genuinely adaptive). index/search (Phase 2) add a local FTS5+vector store over
the vault and every completed session — see growthos/store.py.
"""
import argparse
import shutil
import sys

from . import (backend, concept as concept_mod, config, corpus as corpus_mod, inbox as inbox_mod,
               ingest, interview, onboard as onboard_mod, prompt, store, tokens, vault, weekly)


def _confirm(prompt_text: str) -> bool:
    return input(f"{prompt_text} ").strip().lower() in ("y", "yes", "s", "si", "sí")


def _resolve_target_path(cfg: dict, ticket_id: str, branch: str) -> "Path | None":
    """Shared existing-note handling for premortem: in-progress drafts are
    overwritten silently (same as the original workflow's rule); a resolved note
    needs confirmation. Returns None if the user declines to overwrite."""
    existing = vault.find_ticket_note(cfg, ticket_id)
    if not existing:
        return vault.default_ticket_path(cfg, ticket_id, branch)
    status = vault.read_frontmatter_field(existing.read_text(), "status")
    if status == "resolved":
        if not _confirm(f"Ya existe una reflection resuelta para {ticket_id} en {existing}. ¿Sobreescribir? [y/N]"):
            return None
    return existing


def cmd_premortem(args, cfg: dict) -> None:
    print("Pre-mortem: dame el contexto base del ticket:\n")
    ctx = interview.ask_upfront([
        ("branch", "Branch (el que usarás)"),
        ("ticket_id", "Ticket ID (e.g. CASH-1234)"),
        ("short_description", "Descripción corta del ticket"),
    ])
    branch, ticket_id, short_description = ctx["branch"], ctx["ticket_id"], ctx["short_description"]

    # ponytail: the original workflow silently fed CONTEXT.md/PLAN.md/RESEARCH.md to
    # the interviewing model so it could nudge vague Q2 answers. Nothing here
    # consumes that anymore -- no model is in this loop. Wire it back in if a
    # model-assisted vagueness check gets built on top of this.

    qs = interview.parse_questions(config.workflow_path("premortem.md"))
    answers = {
        "1": interview.ask(qs["1"]["text"]),
        "2": interview.ask(qs["2"]["text"]),
        "3": interview.ask(qs["3"]["text"]),
        "4": interview.ask(qs["4"]["text"]),
    }
    print("\nPre-mortem capturado -- escribiendo draft...")

    target_path = _resolve_target_path(cfg, ticket_id, branch)
    if target_path is None:
        print("Cancelado.")
        return

    if args.agent == "print":
        print("\n/growth premortem no necesita un modelo -- es puro templating de tus "
              "respuestas. Ignorando --agent print y escribiendo el draft directamente.\n")

    vault.write_premortem(target_path, branch=branch, ticket_id=ticket_id,
                           short_description=short_description, answers=answers)

    tickets_rel = config.vault_subdir(cfg, "tickets").name
    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pre-mortem escrito: {tickets_rel}/{target_path.name}

Predicciones registradas. Ahora puedes codear.
Cuando termines el ticket, corre `growth reflect` --
detectará este draft y completará la nota automáticamente.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")


def cmd_reflect(args, cfg: dict) -> None:
    print("Antes de empezar, dame el contexto base:\n")
    ctx = interview.ask_upfront([
        ("branch", "Branch (puede ser diferente a la actual)"),
        ("ticket_id", "Ticket ID (e.g. CASH-1234)"),
        ("short_description", "Descripción corta del ticket"),
    ])
    branch, ticket_id, short_description = ctx["branch"], ctx["ticket_id"], ctx["short_description"]

    draft = vault.detect_draft(cfg, ticket_id)
    draft_found = draft is not None
    git_ctx = vault.gather_git_context(branch)

    print(f"\nBranch: {branch}\nTicket: {ticket_id} -- {short_description}")
    if git_ctx["diff_stat"]:
        print(f"Files changed:\n{git_ctx['diff_stat']}")
    if draft_found:
        print("\nPre-mortem encontrado -- cargando contexto pre-codeo...\n")
        print(f"Pre-mortem:\n{draft['premortem']}\n")
        print(f"Assumptions capturadas antes de codear:\n{draft['assumptions']}\n")

    print("\nStarting reflection interview -- answer each question, then I'll write the note.")

    reflect_qs = interview.parse_questions(config.workflow_path("reflect.md"))
    answers = {}
    if draft_found:
        bridge_q = reflect_qs["_BRIDGE"]["text"].replace(
            "{draft_premortem failure points}", draft["premortem"] or "(ninguno capturado)"
        )
        bridge_answer = interview.ask(bridge_q)
        answers["q1"] = f"{draft['assumptions']}\n\n**Realidad:** {bridge_answer}"
    else:
        answers["q1"] = interview.ask(reflect_qs["1"]["text"])

    answers["q2"] = interview.ask(reflect_qs["2"]["text"])
    answers["q3"] = interview.ask(reflect_qs["3"]["text"])
    answers["q4"] = interview.ask(reflect_qs["4"]["text"])

    print("\nGracias -- escribiendo la nota...")

    if draft_found:
        target_path = draft["path"]
    else:
        target_path = _resolve_target_path(cfg, ticket_id, branch)
        if target_path is None:
            print("Cancelado.")
            return

    rubric = prompt.load_rubric()
    text_prompt = prompt.build_reflect_prompt(
        rubric_text=rubric,
        ticket_id=ticket_id, short_description=short_description,
        pattern="(not auto-detected in CLI v1 -- inferred by the model from git context)",
        files=git_ctx["diff_stat"],
        answers=answers,
        need_premortem_inference=not draft_found,
        git_context=git_ctx,
    )

    if args.agent == "print":
        print("\n" + "=" * 70)
        print(text_prompt)
        print("=" * 70)
        print("\nPrompt assembled above -- paste into any model. --agent print does not")
        print("write a note: there is no response yet to parse and score from.")
        return

    try:
        result = backend.run(args.agent, text_prompt, cfg)
    except backend.BackendError as e:
        print(f"Error calling {args.agent}: {e}", file=sys.stderr)
        sys.exit(1)

    entry = tokens.log("reflect", args.agent, text_prompt, result)
    print(tokens.summarize(entry))

    try:
        scores = prompt.parse_reflect_response(result.text)
    except prompt.ParseError as e:
        print(f"Model response could not be parsed: {e}", file=sys.stderr)
        print(f"Raw response:\n{result.text}", file=sys.stderr)
        sys.exit(1)

    if draft_found:
        premortem_section = draft["premortem"]
        assumptions_section = answers["q1"]
    else:
        premortem_section = scores["premortem_inferred"] or "(no se pudo inferir contexto desde git)"
        assumptions_section = ("Ticket was unambiguous -- no critical assumptions identified."
                                if answers["q1"].strip().upper() == "N/A" else answers["q1"])

    # Retrieval replaces the old ls-based scan: query the index with what the
    # ticket was actually about, now that the interview has given us real content
    # to search on, instead of handing the model every concept slug unfiltered.
    concept_query = f"{short_description} {answers['q2']} {answers['q3']}"
    concepts = ingest.concept_slugs_for(cfg, concept_query)

    vault.write_reflection(
        cfg, path=target_path, branch=branch, ticket_id=ticket_id,
        short_description=short_description,
        premortem=premortem_section, assumptions=assumptions_section,
        answers=answers, concepts=concepts, scores=scores,
    )
    vault.append_ledger(cfg, ticket_id=ticket_id, branch=branch, scores=scores)
    ingest.add_session(
        kind="reflect", identifier=ticket_id,
        content=f"{short_description}\n\n{answers['q2']}\n\n{answers['q3']}\n\n{scores['analysis']}",
        metadata={"ticket": ticket_id, "branch": branch, "score": scores["total"]},
    )

    print(f"""
─────────────────────────────────────────────────────────────────────────────
Reflection scored: {ticket_id}

  D1 Cognitive Depth    {scores['d1']}/3   {scores['d1_fb']}
  D2 Cycle Completeness {scores['d2']}/2   {scores['d2_fb']}
  D3 Loop Depth         {scores['d3']}/2   {scores['d3_fb']}
  D4 Actionability      {scores['d4']}/2   {scores['d4_fb']}
  D5 Linguistic Quality {scores['d5']}/1   {scores['d5_fb']}
  ─────────────────────
  Total                 {scores['total']}/10  ({vault.band_for(scores['total'])})

  {scores['analysis']}
─────────────────────────────────────────────────────────────────────────────

Written to: {target_path}""")


def cmd_concept(args, cfg: dict) -> None:
    slug = concept_mod.resolve_slug(args.name)
    existing_path = concept_mod.find_concept_file(cfg, slug)
    state = concept_mod.classify_state(existing_path)

    sections_to_update = None
    existing_body = None
    if state == "full":
        print(f"Full article already exists: {existing_path}")
        sections_to_update = input(
            "¿Qué sección actualizar? (nombre de la sección, o 'all' para repasar todo) "
        ).strip()
        existing_body = existing_path.read_text().split("---\n", 2)[-1].split("\n# ", 1)[-1]
    elif state == "stub":
        print(f"Stub found, expanding: {existing_path}")
        existing_body = existing_path.read_text().split("---\n", 2)[-1].split("\n# ", 1)[-1]
    else:
        print(f"No existing article for '{slug}' — writing a new one.")

    evidence = concept_mod.gather_codebase_evidence(args.name)
    text_prompt = prompt.build_concept_prompt(
        concept_name=args.name,
        domains=cfg.get("concept_domains", []),
        project_name=cfg.get("project_name", "your project"),
        codebase_evidence=evidence,
        existing_body=existing_body,
        sections_to_update=sections_to_update,
    )

    if args.agent == "print":
        print("\n" + "=" * 70)
        print(text_prompt)
        print("=" * 70)
        return

    try:
        result = backend.run(args.agent, text_prompt, cfg)
    except backend.BackendError as e:
        print(f"Error calling {args.agent}: {e}", file=sys.stderr)
        sys.exit(1)

    entry = tokens.log("concept", args.agent, text_prompt, result)
    print(tokens.summarize(entry))

    try:
        parsed = prompt.parse_concept_response(result.text)
    except prompt.ParseError as e:
        print(f"Model response could not be parsed: {e}", file=sys.stderr)
        print(f"Raw response:\n{result.text}", file=sys.stderr)
        sys.exit(1)

    domain = parsed["domain"] if parsed["domain"] in cfg.get("concept_domains", []) else \
        (cfg.get("concept_domains") or ["uncategorized"])[0]
    path = concept_mod.write_article(
        cfg, slug=slug, title=args.name, domain=domain,
        confidence=parsed["confidence"], body=parsed["body"], existing_path=existing_path,
    )
    wikilinks = concept_mod.extract_wikilinks(parsed["body"])
    rel = path.relative_to(config.vault_root(cfg))
    print(f"\nConcept written: {rel}")
    print(f"Wikilinks: {', '.join(wikilinks) if wikilinks else '(none — add at least 2 manually)'}")
    print(f"Confidence: {parsed['confidence']}")


def cmd_weekly(args, cfg: dict) -> None:
    note_path = weekly.weekly_note_path(cfg)
    if note_path.exists():
        # ponytail: the original workflow offers a merged "mid-week update" section
        # instead of overwriting. Simplified here to confirm-or-abort; add the merge
        # if mid-week re-runs turn out to be common.
        if not _confirm(f"{note_path.name} ya existe para esta semana. ¿Sobreescribir? [y/N]"):
            print("Cancelado.")
            return

    tickets = weekly.gather_tickets(cfg)
    homework_log = weekly.gather_homework(cfg)
    trend = weekly.gather_score_trend(cfg)

    print(f"Tickets esta semana: {len(tickets)}")
    for t in tickets:
        print(f"  - {t['ticket']}: {t['title']}")
    if not tickets:
        print("  (ninguno -- igual corremos la entrevista y escribimos la review)")

    print("\nStarting weekly interview -- answer each question, then I'll write the note.")
    qs = interview.parse_questions(config.workflow_path("weekly-review.md"))
    answers = {
        "w1": interview.ask(qs["1"]["text"]),
        "w2": interview.ask(qs["2"]["text"]),
        "w3": interview.ask(qs["3"]["text"]),
        "w4": interview.ask(qs["4"]["text"]),
    }
    print("\nGracias -- escribiendo la nota...")

    rubric = prompt.load_weekly_rubric()
    text_prompt = prompt.build_weekly_prompt(
        rubric_text=rubric, week=weekly.week_id(), tickets=tickets,
        homework_log=homework_log, answers=answers,
    )

    if args.agent == "print":
        print("\n" + "=" * 70)
        print(text_prompt)
        print("=" * 70)
        return

    try:
        result = backend.run(args.agent, text_prompt, cfg)
    except backend.BackendError as e:
        print(f"Error calling {args.agent}: {e}", file=sys.stderr)
        sys.exit(1)

    entry = tokens.log("weekly", args.agent, text_prompt, result)
    print(tokens.summarize(entry))

    try:
        scores = prompt.parse_weekly_response(result.text)
    except prompt.ParseError as e:
        print(f"Model response could not be parsed: {e}", file=sys.stderr)
        print(f"Raw response:\n{result.text}", file=sys.stderr)
        sys.exit(1)

    weekly.compose_and_write(cfg, path=note_path, tickets=tickets, trend=trend,
                              answers=answers, scores=scores)
    ingest.add_session(
        kind="weekly", identifier=weekly.week_id(),
        content=f"{answers['w1']}\n\n{answers['w2']}\n\n{answers['w3']}\n\n{scores['analysis']}",
        metadata={"week": weekly.week_id(), "score": scores["total"]},
    )

    print(f"""
─────────────────────────────────────────────────────────────────────────────
Weekly review scored: {weekly.week_id()}

  W1 Learning Velocity     {scores['w1']}/3   {scores['w1_fb']}
  W2 Pattern Recognition   {scores['w2']}/2   {scores['w2_fb']}
  W3 Gap Specificity       {scores['w3']}/2   {scores['w3_fb']}
  W4 Capability Assertion  {scores['w4']}/2   {scores['w4_fb']}
  W5 System Health         {scores['w5']}/1   {scores['w5_fb']}
  ─────────────────────
  Total                    {scores['total']}/10  ({weekly.band_for(scores['total'])})

  {scores['analysis']}
{scores.get('recommendations', '')}
─────────────────────────────────────────────────────────────────────────────

Written to: {note_path}""")

    cmd_process_inbox(args, cfg)


def cmd_process_inbox(args, cfg: dict) -> None:
    files = inbox_mod.read_inbox(cfg)
    if not files:
        print("\nInbox is empty -- nothing to triage.")
        return

    text_prompt = inbox_mod.build_triage_prompt(cfg, files)

    if args.agent == "print":
        print("\n" + "=" * 70)
        print(text_prompt)
        print("=" * 70)
        return

    try:
        result = backend.run(args.agent, text_prompt, cfg)
    except backend.BackendError as e:
        print(f"Error calling {args.agent} for inbox triage: {e}", file=sys.stderr)
        return

    entry = tokens.log("process_inbox", args.agent, text_prompt, result)
    print(tokens.summarize(entry))

    plan = inbox_mod.parse_triage_response(result.text, files)
    if not plan:
        print("No se pudo generar un plan de triage -- nada movido.")
        return

    print(f"\nInbox triage plan -- {len(plan)} files found:\n")
    for i, item in enumerate(plan, start=1):
        print(f"{i}. {item['name']} -> {item['action']} ({item['reason']})")

    reply = input("\nProceed? (reply `proceed` to execute all, `skip N` or `skip N M` to exclude items, "
                  "anything else aborts.) ").strip()
    if reply == "proceed":
        skip = set()
    elif reply.startswith("skip "):
        skip = {int(n) for n in reply[5:].split() if n.isdigit()}
    else:
        print("Aborted -- nothing moved.")
        return

    result_counts = inbox_mod.execute_plan(cfg, plan, skip)
    print(f"""
Inbox triage complete.
  Moved:   {len(result_counts['moved'])} ({', '.join(result_counts['moved']) or 'none'})
  Skipped: {len(result_counts['skipped'])} ({', '.join(result_counts['skipped']) or 'none'})
  Deleted: {len(result_counts['deleted'])} ({', '.join(result_counts['deleted']) or 'none'})""")


def cmd_onboard(args, cfg: dict) -> None:
    if args.agent == "print":
        print("growth onboard needs a real back-and-forth with the model (the interview is "
              "adaptive, not fixed questions) -- --agent print has nothing to export here.")
        sys.exit(1)

    first_run = "user_profile" not in cfg
    if not first_run:
        print("Ya tienes un perfil guardado. ¿Quieres actualizarlo (responde \"actualizar\")")
        reply = input("o salir sin cambios (cualquier otra cosa)? ").strip().lower()
        if reply != "actualizar":
            print("Sin cambios.")
            return
        print("\nVault scaffolding skipped — updating profile only.")
    else:
        print("""Bienvenido al Growth OS.

Antes de configurar tu sistema, quiero entender quién eres y hacia dónde vas.
Voy a hacerte 4–5 preguntas. No hay respuestas correctas ni incorrectas.
Sé tan honesto como puedas — el sistema funciona mejor cuanto más real sea el perfil.

Esto no reemplaza a un coach o psicólogo. Es una orientación para que tu sistema
de crecimiento apunte hacia lo que genuinamente importa.

¿Listo? Empecemos.""")

    profile = onboard_mod.run_interview(args.agent, cfg)
    if profile is None:
        print("Onboarding abortado -- nada se escribió.")
        sys.exit(1)

    cfg_path = onboard_mod.write_profile(profile)
    cfg = config.load()  # re-read: write_profile may have synced concept_domains/project_name

    if first_run:
        print("\nScaffolding vault...")
        for line in onboard_mod.scaffold_vault(cfg):
            print(f"  {line}")

    note_path = onboard_mod.write_profile_note(cfg, profile)

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Onboarding completo.

  Perfil guardado en: {cfg_path}
  Nota de vault:      {note_path}

  Próximos pasos:
  · Abre Obsidian — las carpetas y templates ya están instalados
  · Activa el plugin Templater y apúntalo a 99-templates/ en tu vault
  · Corre `growth premortem` / `growth reflect` después de tu próximo ticket
  · Corre `growth weekly` al final de esta semana
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")


def cmd_init(args) -> None:
    dest = config.CANONICAL_CONFIG
    if dest.exists():
        print(f"{dest} already exists -- not overwriting. Edit it directly.")
        return
    example = config.GROWTH_OS_HOME / "config.example.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(example.read_text())
    print(f"Wrote {dest} from config.example.json.")
    print("Edit vault_root, vault_name, and project_name, then run `growth premortem` "
          "or `growth reflect`.")


def cmd_doctor(args) -> None:
    print("Growth OS doctor\n")
    cfg = {}
    try:
        path = config.config_path()
        cfg = config.load()
        print(f"Config: {path}")
        root = config.vault_root(cfg)
        print(f"Vault root: {root} {'(exists)' if root.is_dir() else '(MISSING)'}")
        tickets = config.vault_subdir(cfg, "tickets")
        n = len(list(tickets.glob("*.md"))) if tickets.is_dir() else 0
        print(f"Ticket reflections: {n}")
        ledger = root / "reflection-scores.md"
        print(f"Reflection ledger: {'exists' if ledger.exists() else 'not created yet'}")
    except config.ConfigError as e:
        print(f"Config: ERROR -- {e}")

    print("\nBackends:")
    for name in ("claude", "codex"):
        print(f"  {name}: {'found' if shutil.which(name) else 'NOT on PATH'}")
    for name, argv in cfg.get("backends", {}).items():
        print(f"  {name} (custom): {'found' if shutil.which(argv[0]) else 'NOT on PATH -- ' + argv[0]}")
    print("  print: always available (no model call)")

    print("\nKnowledge store:")
    st = store.stats()
    print(f"  Index: {st['path']}")
    print(f"  Vector search: {'available (' + st['embed_model'] + ')' if st['vec_available'] else 'NOT available -- FTS5 keyword search only (pip install -r requirements-index.txt)'}")
    for collection in ("vault", "sessions"):
        print(f"  {collection}: {st['counts'].get(collection, 0)} documents")
    corpus_n = st["counts"].get("corpus", 0)
    scopes = st.get("corpus_scopes", {})
    print(f"  corpus: {corpus_n} chunks (shared: {scopes.get('shared', 0)}, personal: {scopes.get('personal', 0)})")
    personal_dir = cfg.get("personal_corpus_dir")
    print(f"  personal_corpus_dir: {personal_dir or '(not set)'}")
    try:
        import ebooklib, pypdf  # noqa: F401
        print("  epub/pdf parsing: available")
    except ImportError:
        print("  epub/pdf parsing: NOT available (pip install -r requirements-corpus.txt)")
    if store.ZERO_HITS_LOG.exists():
        n = sum(1 for _ in store.ZERO_HITS_LOG.open())
        print(f"  Zero-hit queries logged: {n} (see {store.ZERO_HITS_LOG})")


def cmd_index(args, cfg: dict) -> None:
    print("Indexing vault...")
    counts = ingest.index_vault(cfg)
    print(f"  Tickets: {counts['tickets']}")
    print(f"  Concepts: {counts['concepts']}")
    print(f"  Weekly reviews: {counts['weekly']}")

    if args.corpus:
        print("\nIndexing corpus...")
        corpus_counts = corpus_mod.index_corpus(cfg)
        print(f"  Shared (shipped with growth-os): {corpus_counts['shared_chunks']} chunks")
        print(f"  Personal ({cfg.get('personal_corpus_dir') or 'not configured'}): "
              f"{corpus_counts['personal_chunks']} chunks")

    st = store.stats()
    if not st["vec_available"]:
        print("\n(Vector search unavailable -- indexed with FTS5 keyword search only. "
              "`pip install -r requirements-index.txt` for semantic search too.)")
    print(f"\nIndex: {st['path']}")


def cmd_search(args, cfg: dict) -> None:
    results = store.search(args.query, collection=args.collection, k=args.k)
    if not results:
        print(f"No results for: {args.query!r}"
              + (f" (collection={args.collection})" if args.collection else ""))
        print("Logged to the zero-hit tripwire." if store.ZERO_HITS_LOG.exists() else "")
        return
    for i, r in enumerate(results, start=1):
        snippet = " ".join(r["content"].split())[:160]
        print(f"{i}. [{r['collection']}] {r['source']} (score={r['fused_score']:.4f})")
        print(f"   {snippet}...\n")


def cmd_ask(args, cfg: dict) -> None:
    """growth search --collection corpus, with citation-formatted output --
    the corpus is meant to be quoted from, not just located."""
    results = store.search(args.query, collection="corpus", k=args.k)
    if not results:
        print(f"No corpus passages found for: {args.query!r}")
        print("Run `growth index --corpus` first if you haven't, or "
              "`growth doctor` to check what's indexed.")
        return
    for i, r in enumerate(results, start=1):
        meta = r["metadata"]
        snippet = " ".join(r["content"].split())[:400]
        label = f"{meta.get('file', r['source'])} ({meta.get('scope', '?')})"
        print(f"{i}. [{label}]\n   {snippet}\n")


def main() -> None:
    parser = argparse.ArgumentParser(prog="growth", description="Growth OS CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_pre = sub.add_parser("premortem", help="Before coding: capture predictions")
    p_pre.add_argument("--agent", default=None, help="claude | codex | print | <custom from config>")

    p_ref = sub.add_parser("reflect", help="After coding: reflect and score")
    p_ref.add_argument("--agent", default=None, help="claude | codex | print | <custom from config>")

    p_con = sub.add_parser("concept", help="Write or expand a concept article")
    p_con.add_argument("name", help='Concept name, e.g. "NestJS interceptors"')
    p_con.add_argument("--agent", default=None, help="claude | codex | print | <custom from config>")

    p_week = sub.add_parser("weekly", help="End of sprint: review, score, triage inbox")
    p_week.add_argument("--agent", default=None, help="claude | codex | print | <custom from config>")

    p_onb = sub.add_parser("onboard", help="Adaptive profile interview + vault scaffold")
    p_onb.add_argument("--agent", default=None, help="claude | codex | <custom from config> (no print)")

    p_idx = sub.add_parser("index", help="Rebuild the vault index (FTS5 + vector search)")
    p_idx.add_argument("--corpus", action="store_true",
                        help="Also (re)index the corpus: shared framework writeups + your personal_corpus_dir")

    p_search = sub.add_parser("search", help="Hybrid search over the indexed vault/sessions/corpus")
    p_search.add_argument("query")
    p_search.add_argument("--collection", default=None, choices=["vault", "sessions", "corpus"])
    p_search.add_argument("-k", type=int, default=10)

    p_ask = sub.add_parser("ask", help="Search the corpus specifically, citation-formatted")
    p_ask.add_argument("query")
    p_ask.add_argument("-k", type=int, default=5)

    sub.add_parser("init", help="Create ~/.growth-os/config.json from the example")
    sub.add_parser("doctor", help="Diagnose config + backends + index")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
        return
    if args.command == "doctor":
        cmd_doctor(args)
        return

    try:
        cfg = config.load()
    except config.ConfigError as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(1)

    # index/search don't take --agent (no model call) -- hasattr avoids an
    # AttributeError on those rather than giving every subparser a dead flag.
    if hasattr(args, "agent") and args.agent is None:
        args.agent = cfg.get("default_backend", "claude")

    if args.command == "premortem":
        cmd_premortem(args, cfg)
    elif args.command == "reflect":
        cmd_reflect(args, cfg)
    elif args.command == "concept":
        cmd_concept(args, cfg)
    elif args.command == "weekly":
        cmd_weekly(args, cfg)
    elif args.command == "onboard":
        cmd_onboard(args, cfg)
    elif args.command == "index":
        cmd_index(args, cfg)
    elif args.command == "search":
        cmd_search(args, cfg)
    elif args.command == "ask":
        cmd_ask(args, cfg)


if __name__ == "__main__":
    main()
