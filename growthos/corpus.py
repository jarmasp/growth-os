"""Corpus ingest: epub/pdf/md/txt -> chunks -> store (collection='corpus').

Two sources, both indexed the same way, told apart by metadata['scope']:

- SHARED_DIR (growth-os/corpus/, shipped, tracked in git): original writeups of
  the frameworks already applied across agents/*.md (Kolb, Ericsson, Dreyfus,
  SDT, Argyris/Schön...) -- distilled and cited, never the books' own text.
  Available to everyone who clones the repo. Extensible: add another article,
  open a PR.
- cfg['personal_corpus_dir'] (configurable, gitignored, never committed):
  whatever anyone wants to add for themselves -- books they own, internal
  docs, anything. Stays on their machine; growth-os never uploads or shares it.
"""
import re
from pathlib import Path

from . import config, store

SHARED_DIR = config.GROWTH_OS_HOME / "corpus"
CHUNK_CHARS = 3200      # ~800 tokens
CHUNK_OVERLAP_CHARS = 300
SKIP_FILES = {"readme.md"}


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in (".md", ".txt"):
        return path.read_text(errors="ignore")
    if suffix == ".epub":
        return _extract_epub(path)
    if suffix == ".pdf":
        return _extract_pdf(path)
    raise ValueError(f"unsupported corpus file type: {suffix}")


def _extract_epub(path: Path) -> str:
    try:
        import ebooklib
        from ebooklib import epub
    except ImportError as e:
        raise RuntimeError("epub support needs `pip install -r requirements-corpus.txt`") from e
    book = epub.read_epub(str(path))
    parts = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        html = item.get_content().decode("utf-8", errors="ignore")
        text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"&nbsp;|&amp;|&lt;|&gt;|&#\d+;", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            parts.append(text)
    return "\n\n".join(parts)


def _extract_pdf(path: Path) -> str:
    try:
        import pypdf
    except ImportError as e:
        raise RuntimeError("pdf support needs `pip install -r requirements-corpus.txt`") from e
    reader = pypdf.PdfReader(str(path))
    return "\n\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text: str) -> list[dict]:
    """Paragraph-aware chunking targeting ~CHUNK_CHARS with a bit of overlap --
    good enough for book-length text. Short docs (shipped framework articles,
    personal notes) come back as a single chunk, same as a vault note.

    ponytail: 'offset' is the running character position where each chunk
    roughly starts, not an exact index into the original file -- fine for
    "around here" citation, not for byte-exact lookup. Upgrade if Phase 4's
    citations need to jump back to a precise original location."""
    text = text.strip()
    if len(text) <= CHUNK_CHARS:
        return [{"content": text, "offset": 0}] if text else []

    paragraphs = re.split(r"\n\s*\n", text)
    chunks, current, pos = [], "", 0
    for para in paragraphs:
        if current and len(current) + len(para) > CHUNK_CHARS:
            chunks.append({"content": current.strip(), "offset": pos})
            pos += max(len(current) - CHUNK_OVERLAP_CHARS, 0)
            current = current[-CHUNK_OVERLAP_CHARS:] + "\n\n" + para
        else:
            current += ("\n\n" if current else "") + para
    if current.strip():
        chunks.append({"content": current.strip(), "offset": pos})
    return chunks


def _index_dir(db, directory: Path, scope: str) -> int:
    if not directory.is_dir():
        return 0
    total_chunks = 0
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.name.lower() in SKIP_FILES:
            continue
        if path.suffix.lower() not in (".md", ".txt", ".epub", ".pdf"):
            continue
        try:
            text = extract_text(path)
        except RuntimeError as e:
            print(f"  skipped {path.name}: {e}")
            continue
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            store.add_document(
                db, collection="corpus", source=f"{scope}:{path.stem}#chunk{i}",
                content=chunk["content"],
                metadata={"scope": scope, "file": path.name, "chunk": i, "offset": chunk["offset"]},
            )
        total_chunks += len(chunks)
        print(f"  {path.name}: {len(chunks)} chunk(s) ({scope})")
    return total_chunks


def index_corpus(cfg: dict) -> dict:
    db = store.connect()
    try:
        store.clear_collection(db, "corpus")
        shared_n = _index_dir(db, SHARED_DIR, "shared")
        personal_dir = cfg.get("personal_corpus_dir")
        personal_n = _index_dir(db, Path(personal_dir).expanduser(), "personal") if personal_dir else 0
    finally:
        db.close()
    return {"shared_chunks": shared_n, "personal_chunks": personal_n}
