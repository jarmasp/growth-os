"""Thin wrapper around fastembed. Optional dependency: everything in store.py
degrades to FTS5-only search when it isn't installed, so a fresh `growth` clone
works before anyone runs `pip install -r requirements-index.txt`.

Model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384-dim,
~220MB, ONNX via fastembed — no server, unlike ollama). Chosen for D6: Jose's
reflections are Spanish, the rubrics and any future book corpus are English.
Verified empirically before building on it: true cross-lingual paraphrases of
the same concept score ~0.92-0.94 cosine; unrelated pairs score ~0.04-0.09. A
monolingual model would silently fail across that boundary instead of erroring.
"""
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
DIM = 384

_model = None


def available() -> bool:
    try:
        import fastembed  # noqa: F401
        return True
    except ImportError:
        return False


def _get_model():
    global _model
    if _model is None:
        from fastembed import TextEmbedding
        _model = TextEmbedding(model_name=MODEL_NAME)
    return _model


def embed(texts: list[str]) -> list[list[float]]:
    """First call downloads the model (~220MB) to the fastembed cache and can
    take a while; later calls are fast. Needs network once, ever, per machine.

    If this fails with CERTIFICATE_VERIFY_FAILED on a corporate-managed laptop
    (seen on a Cashea machine behind MDM TLS inspection): the root cert lives in
    the macOS Keychain, which `curl` trusts but Python's own cert store doesn't.
    Fix: `pip install pip-system-certs` (patches Python to use the OS trust
    store) — not a growth-os bug, a Python-on-managed-devices gotcha."""
    model = _get_model()
    # L2-normalize: fastembed's raw output isn't unit-length (measured norm ~5.1
    # on this model) — normalized, sqlite-vec's L2 distance ranks identically to
    # cosine similarity, and distance converts to a clean 0-1 similarity score.
    out = []
    for vec in model.embed(texts):
        norm = sum(x * x for x in vec) ** 0.5 or 1.0
        out.append([float(x) / norm for x in vec])
    return out


def embed_one(text: str) -> list[float]:
    return embed([text])[0]
