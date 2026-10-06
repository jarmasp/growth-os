"""Backends: one subprocess call per run, agent-agnostic.

claude/codex get native handling (real token/cost usage where the CLI reports it).
Anything else goes through config.json's "backends" dict as a plain argv template —
adding a new agent is a line of JSON, not a code change.

ponytail: no async, no retries, no streaming — one call, one result. Add when a
workflow needs to pipeline multiple calls (nothing in Phase 1 does).
"""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


class BackendError(RuntimeError):
    pass


class Result:
    def __init__(self, text: str, usage: dict | None = None, cost_usd: float | None = None):
        self.text = text.strip()
        self.usage = usage or {}
        self.cost_usd = cost_usd


def run_claude(prompt: str) -> Result:
    if not shutil.which("claude"):
        raise BackendError("`claude` CLI not found on PATH.")
    proc = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "json"],
        capture_output=True, text=True, timeout=600,
    )
    if proc.returncode != 0:
        raise BackendError(f"claude -p failed: {proc.stderr.strip() or proc.stdout.strip()}")
    data = json.loads(proc.stdout)
    usage = data.get("usage", {})
    return Result(
        text=data.get("result", ""),
        usage={
            "input_tokens": usage.get("input_tokens"),
            "output_tokens": usage.get("output_tokens"),
            "cache_read_input_tokens": usage.get("cache_read_input_tokens"),
            "cache_creation_input_tokens": usage.get("cache_creation_input_tokens"),
        },
        cost_usd=data.get("total_cost_usd"),
    )


def run_codex(prompt: str) -> Result:
    if not shutil.which("codex"):
        raise BackendError("`codex` CLI not found on PATH.")
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        out_file = Path(tmp.name)
    try:
        proc = subprocess.run(
            ["codex", "exec", "--output-last-message", str(out_file), prompt],
            capture_output=True, text=True, timeout=600,
        )
        if proc.returncode != 0:
            raise BackendError(f"codex exec failed: {proc.stderr.strip() or proc.stdout.strip()}")
        text = out_file.read_text() if out_file.exists() else proc.stdout
    finally:
        out_file.unlink(missing_ok=True)
    # codex exec doesn't report structured token usage on stdout in non-JSON mode —
    # tokens.py falls back to a char-count estimate when usage is empty.
    return Result(text=text, usage={})


def run_generic(argv_template: list[str], prompt: str) -> Result:
    argv = [a.replace("{prompt}", prompt) for a in argv_template]
    if not shutil.which(argv[0]):
        raise BackendError(f"`{argv[0]}` not found on PATH.")
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=600)
    if proc.returncode != 0:
        raise BackendError(f"{argv[0]} failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return Result(text=proc.stdout, usage={})


BUILTIN = {"claude": run_claude, "codex": run_codex}


def run(agent: str, prompt: str, cfg: dict) -> Result:
    if agent in BUILTIN:
        return BUILTIN[agent](prompt)
    custom = cfg.get("backends", {}).get(agent)
    if custom:
        return run_generic(custom, prompt)
    raise BackendError(
        f"Unknown agent '{agent}'. Built-in: {', '.join(BUILTIN)}. "
        f"Configured: {', '.join(cfg.get('backends', {})) or '(none)'}."
    )
