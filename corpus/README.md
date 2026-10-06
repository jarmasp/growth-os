# corpus/

Original writeups of the frameworks growth-os's agents already apply — distilled
and cited, never the source books' own text. Shipped with the repo, so everyone who
clones growth-os gets this from day one; extend it by opening a PR with another
framework article in the same shape.

This directory is indexed by `growth index --corpus` into the `corpus` collection
tagged `scope: shared`. Your own corpus (books you own, internal docs, anything)
goes in a separate directory you configure via `personal_corpus_dir` in
`config.json` — gitignored, never shared, indexed the same way tagged `scope: personal`.

Each article: what the framework actually says (2-4 paragraphs, original prose),
exactly which agent/workflow in this repo applies it and where, and where to read
the real thing if you want the full depth — a citation, not a copy.

This file itself is excluded from indexing (see `growthos/corpus.py`'s `SKIP_FILES`).
