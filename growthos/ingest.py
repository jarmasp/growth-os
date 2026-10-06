"""Indexes the vault into the store. One document per note — vault notes are
short (tickets, concept articles, weeklies), so there's nothing to chunk yet;
chunking is a Phase 3 concern for book-length corpus, not personal notes.
"""
from . import config, store


def index_vault(cfg: dict) -> dict:
    db = store.connect()
    try:
        store.clear_collection(db, "vault")
        counts = {"tickets": 0, "concepts": 0, "weekly": 0}

        tickets_dir = config.vault_subdir(cfg, "tickets")
        if tickets_dir.is_dir():
            for p in tickets_dir.glob("*.md"):
                store.add_document(db, collection="vault", source=f"20-tickets/{p.name}",
                                    content=p.read_text(errors="ignore"), metadata={"kind": "ticket"})
                counts["tickets"] += 1

        concepts_dir = config.vault_subdir(cfg, "concepts")
        if concepts_dir.is_dir():
            for domain_dir in sorted(concepts_dir.iterdir()):
                if not domain_dir.is_dir():
                    continue
                for p in domain_dir.glob("*.md"):
                    store.add_document(
                        db, collection="vault", source=f"10-concepts/{domain_dir.name}/{p.name}",
                        content=p.read_text(errors="ignore"),
                        metadata={"kind": "concept", "domain": domain_dir.name, "slug": p.stem},
                    )
                    counts["concepts"] += 1

        weekly_dir = config.vault_subdir(cfg, "weekly")
        if weekly_dir.is_dir():
            for p in weekly_dir.glob("*.md"):
                store.add_document(db, collection="vault", source=f"30-weekly/{p.name}",
                                    content=p.read_text(errors="ignore"), metadata={"kind": "weekly"})
                counts["weekly"] += 1
    finally:
        db.close()
    return counts


def add_session(*, kind: str, identifier: str, content: str, metadata: dict | None = None) -> None:
    """Called automatically after a completed reflect/weekly run — populates the
    'sessions' collection for later recall. Phase 2 only writes it; Phase 4 wires
    it into the scoring prompts ("you hit this before")."""
    db = store.connect()
    try:
        store.add_document(db, collection="sessions", source=f"{kind}:{identifier}", content=content,
                            metadata={"kind": kind, **(metadata or {})})
    finally:
        db.close()


def concept_slugs_for(cfg: dict, query: str, k: int = 4) -> list[str]:
    """Replaces the old ls-based scan_concepts: retrieves the concepts whose
    content is actually relevant to this reflection/week instead of handing the
    model every slug in every domain folder unfiltered. Falls back to the plain
    folder scan when nothing has been indexed yet (fresh clone, `growth index`
    never run) so this never regresses a working install to zero links."""
    stats = store.stats()
    if not stats["counts"].get("vault"):
        from . import vault
        return vault.scan_concepts(cfg)
    hits = store.search(query, collection="vault", k=k * 3)
    slugs = [h["metadata"]["slug"] for h in hits if h["metadata"].get("kind") == "concept"]
    seen = set()
    return [s for s in slugs if not (s in seen or seen.add(s))][:k]
