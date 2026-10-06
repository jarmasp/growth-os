"""The knowledge store: one SQLite file (~/.growth-os/index.db), FTS5 (keyword)
and sqlite-vec (semantic) side by side, fused with reciprocal rank fusion (RRF).

Collections: 'vault' (notes — tickets, concepts, weeklies), 'sessions' (every
completed reflect/weekly run, so the next one can recall "you hit this before"),
'corpus' (framework writeups + personal docs, chunked — see growthos/corpus.py;
metadata.scope is 'shared' (shipped, everyone gets it) or 'personal' (yours only)).

Graceful by design, not as an afterthought: a fresh install has zero vault notes
and no sqlite-vec/fastembed installed yet. Every function here degrades to
FTS5-only, or to an empty result, rather than raising — `reflect`/`weekly` must
complete end-to-end either way. `growth doctor` reports what's actually active.
"""
import json
import re
import sqlite3
import struct
import time
from pathlib import Path

from . import embed

DB_PATH = Path.home() / ".growth-os" / "index.db"
ZERO_HITS_LOG = Path.home() / ".growth-os" / "logs" / "zero-hits.jsonl"
RRF_K = 60  # standard reciprocal-rank-fusion constant

# ponytail: vec0's KNN always returns its k nearest neighbors, even when nothing
# in the store is actually related — without a floor, a truly unrelated note
# would still show up (and the zero-hit tripwire below would never fire, since
# there'd always be "a" nearest neighbor). Calibrated against measured cosine
# sims: unrelated pairs ~0.04-0.09, true paraphrases ~0.92-0.94, a real same-topic
# hit in this vault's own test data at 0.37 with noise trailing off below 0.15.
MIN_VEC_SIMILARITY = 0.25

# ponytail: no stopword library, just the worst offenders for a small personal
# vault in ES/EN -- OR-ing every raw token otherwise lets a single common word
# ("de", "con", "the") match nearly everything, drowning the real signal. Not
# exhaustive; extend if a specific word keeps showing up in noisy results.
STOPWORDS = frozenset("""
de la el en los las con por para que un una y o a su sus al del es son fue
the a an and or of to in on for with is are was were be been this that
""".split())


def vec_available() -> bool:
    try:
        import sqlite_vec  # noqa: F401
        return embed.available()
    except ImportError:
        return False


def _pack(vec: list[float]) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec)


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row

    if vec_available():
        import sqlite_vec
        db.enable_load_extension(True)
        sqlite_vec.load(db)
        db.enable_load_extension(False)

    db.executescript("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            collection TEXT NOT NULL,
            source TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata TEXT NOT NULL DEFAULT '{}'
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
            content, content='documents', content_rowid='id'
        );
        CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
            INSERT INTO documents_fts(rowid, content) VALUES (new.id, new.content);
        END;
        CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
            INSERT INTO documents_fts(documents_fts, rowid, content) VALUES ('delete', old.id, old.content);
        END;
    """)
    if vec_available():
        db.execute(f"""
            CREATE VIRTUAL TABLE IF NOT EXISTS documents_vec USING vec0(
                embedding FLOAT[{embed.DIM}]
            )
        """)
    return db


def clear_collection(db: sqlite3.Connection, collection: str) -> int:
    ids = [r["id"] for r in db.execute("SELECT id FROM documents WHERE collection = ?", (collection,))]
    for doc_id in ids:
        db.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
        if vec_available():
            db.execute("DELETE FROM documents_vec WHERE rowid = ?", (doc_id,))
    db.commit()
    return len(ids)


def add_document(db: sqlite3.Connection, *, collection: str, source: str, content: str,
                  metadata: dict | None = None) -> int:
    cur = db.execute(
        "INSERT INTO documents (collection, source, content, metadata) VALUES (?, ?, ?, ?)",
        (collection, source, content, json.dumps(metadata or {}, ensure_ascii=False)),
    )
    doc_id = cur.lastrowid
    if vec_available() and content.strip():
        try:
            vec = embed.embed_one(content)
            db.execute("INSERT INTO documents_vec (rowid, embedding) VALUES (?, ?)", (doc_id, _pack(vec)))
        except Exception as e:
            # Embedding failures (e.g. first-run network/cert issue) must not block
            # indexing — the document still gets FTS5 coverage.
            print(f"  (embedding skipped for {source}: {e})")
    db.commit()
    return doc_id


def _min_terms_required(n_terms: int) -> int:
    # ponytail: an OR-of-all-terms query is fine for a short deliberate search
    # ("guard chains", "rate limiter") -- both/all terms usually need to match
    # anyway for the doc to rank well. It breaks on a long natural-language
    # query: a single incidental word out of nine (a short Spanish/English
    # function word FTS5's tokenizer still treats as a real token -- "hay",
    # "cuando" -- missed by STOPWORDS) can out-rank nothing-else-matched and
    # win on pure RRF rank, since rank doesn't see how *weak* that one match
    # was. Requiring a minimum overlap scales with query length instead of
    # chasing stopwords one coincidence at a time.
    return 1 if n_terms <= 2 else max(2, n_terms // 4)


def _fts_search(db: sqlite3.Connection, query: str, collection: str | None, limit: int) -> list[dict]:
    terms = [t for t in query.replace('"', ' ').split() if t and t.lower() not in STOPWORDS]
    if not terms:
        return []
    match_expr = " OR ".join(f'"{t}"' for t in terms)
    sql = """
        SELECT documents.id, documents.source, documents.content, documents.metadata, documents.collection,
               bm25(documents_fts) AS score
        FROM documents_fts JOIN documents ON documents.id = documents_fts.rowid
        WHERE documents_fts MATCH ?
    """
    params = [match_expr]
    if collection:
        sql += " AND documents.collection = ?"
        params.append(collection)
    sql += " ORDER BY bm25(documents_fts) LIMIT ?"
    params.append(limit * 3)  # overfetch -- the overlap filter below drops some
    try:
        rows = [dict(r) for r in db.execute(sql, params)]
    except sqlite3.OperationalError:
        return []  # malformed FTS query (stray syntax token) -- degrade to no keyword hits

    min_overlap = _min_terms_required(len(terms))
    term_patterns = [re.compile(rf"\b{re.escape(t.lower())}\b") for t in terms]

    def overlap(content: str) -> int:
        lower = content.lower()
        return sum(1 for pat in term_patterns if pat.search(lower))

    kept = [r for r in rows if overlap(r["content"]) >= min_overlap]
    return kept[:limit]


def _vec_search(db: sqlite3.Connection, query: str, collection: str | None, limit: int) -> list[dict]:
    if not vec_available():
        return []
    try:
        qvec = embed.embed_one(query)
    except Exception:
        return []
    sql = """
        SELECT documents.id, documents.source, documents.content, documents.metadata, documents.collection,
               documents_vec.distance AS distance
        FROM documents_vec JOIN documents ON documents.id = documents_vec.rowid
        WHERE documents_vec.embedding MATCH ? AND k = ?
    """
    params = [_pack(qvec), limit if not collection else limit * 4]  # overfetch when filtering post-hoc
    rows = [dict(r) for r in db.execute(sql, params)]
    if collection:
        rows = [r for r in rows if r["collection"] == collection][:limit]
    for r in rows:
        r["score"] = 1 - (r["distance"] ** 2) / 2  # unit vectors: cosine sim from L2 distance
    return [r for r in rows if r["score"] >= MIN_VEC_SIMILARITY]


def search(query: str, collection: str | None = None, k: int = 10, log_zero_hits: bool = True) -> list[dict]:
    """Hybrid BM25 + vector search, fused with RRF. Each result: source, content,
    collection, metadata (parsed), fused_score. Degrades to FTS5-only when
    sqlite-vec/fastembed aren't available; to [] when the store has no documents
    or neither path matches — never raises for an unmatched or empty query."""
    db = connect()
    try:
        fts_hits = _fts_search(db, query, collection, k * 2)
        vec_hits = _vec_search(db, query, collection, k * 2)
    finally:
        db.close()

    ranked: dict[int, float] = {}
    by_id: dict[int, dict] = {}
    for rank, hit in enumerate(fts_hits, start=1):
        ranked[hit["id"]] = ranked.get(hit["id"], 0) + 1 / (RRF_K + rank)
        by_id[hit["id"]] = hit
    for rank, hit in enumerate(vec_hits, start=1):
        ranked[hit["id"]] = ranked.get(hit["id"], 0) + 1 / (RRF_K + rank)
        by_id.setdefault(hit["id"], hit)

    results = []
    for doc_id, fused in sorted(ranked.items(), key=lambda kv: kv[1], reverse=True)[:k]:
        hit = by_id[doc_id]
        results.append({
            "source": hit["source"], "content": hit["content"], "collection": hit["collection"],
            "metadata": json.loads(hit["metadata"]), "fused_score": fused,
        })

    if not results and log_zero_hits:
        _log_zero_hit(query, collection)
    return results


def _log_zero_hit(query: str, collection: str | None) -> None:
    ZERO_HITS_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "query": query, "collection": collection}
    with ZERO_HITS_LOG.open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def stats() -> dict:
    db = connect()
    try:
        counts = {r["collection"]: r["n"] for r in db.execute(
            "SELECT collection, COUNT(*) AS n FROM documents GROUP BY collection"
        )}
        corpus_scopes = {r["scope"]: r["n"] for r in db.execute(
            "SELECT json_extract(metadata, '$.scope') AS scope, COUNT(*) AS n "
            "FROM documents WHERE collection = 'corpus' GROUP BY scope"
        )}
    finally:
        db.close()
    return {
        "path": str(DB_PATH), "counts": counts, "corpus_scopes": corpus_scopes,
        "vec_available": vec_available(), "embed_model": embed.MODEL_NAME if vec_available() else None,
    }
