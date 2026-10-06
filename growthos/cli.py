"""growth — the CLI entry point. Ports workflows/premortem.md and workflows/reflect.md
step for step: same questions (parsed from the markdown, not duplicated), same file
structure, same rules. The interview runs in Python; the model is called at most once
per run, only where real judgment is needed (reflect's scoring + premortem inference).
"""
import argparse
import shutil
import sys

from . import backend, config, interview, prompt, tokens, vault


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
    concepts = vault.scan_concepts(cfg)

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

    vault.write_reflection(
        cfg, path=target_path, branch=branch, ticket_id=ticket_id,
        short_description=short_description,
        premortem=premortem_section, assumptions=assumptions_section,
        answers=answers, concepts=concepts, scores=scores,
    )
    vault.append_ledger(cfg, ticket_id=ticket_id, branch=branch, scores=scores)

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


def main() -> None:
    parser = argparse.ArgumentParser(prog="growth", description="Growth OS CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_pre = sub.add_parser("premortem", help="Before coding: capture predictions")
    p_pre.add_argument("--agent", default=None, help="claude | codex | print | <custom from config>")

    p_ref = sub.add_parser("reflect", help="After coding: reflect and score")
    p_ref.add_argument("--agent", default=None, help="claude | codex | print | <custom from config>")

    sub.add_parser("init", help="Create ~/.growth-os/config.json from the example")
    sub.add_parser("doctor", help="Diagnose config + backends")

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

    if args.agent is None:
        args.agent = cfg.get("default_backend", "claude")

    if args.command == "premortem":
        cmd_premortem(args, cfg)
    elif args.command == "reflect":
        cmd_reflect(args, cfg)


if __name__ == "__main__":
    main()
