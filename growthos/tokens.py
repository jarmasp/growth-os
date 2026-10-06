"""Token/cost logging — one jsonl line per model call, so the Phase 1 token-economy
claim (interview moved to Python, one stateless call per run) is measured, not asserted.

ponytail: char/4 is a rough English-ish estimate, used only when a backend doesn't
report real usage (codex, generic backends). Swap for a real tokenizer if estimates
drift noticeably from billed usage.
"""
import json
import time
from pathlib import Path

LOG_PATH = Path.home() / ".growth-os" / "logs" / "tokens.jsonl"


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def log(command: str, agent: str, prompt: str, result) -> dict:
    usage = result.usage or {}
    has_real_usage = any(v is not None for v in usage.values())
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "command": command,
        "agent": agent,
        "prompt_chars": len(prompt),
        "usage": usage if has_real_usage else None,
        "estimated_tokens": None if has_real_usage else estimate_tokens(prompt) + estimate_tokens(result.text),
        "cost_usd": result.cost_usd,
    }
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def summarize(entry: dict) -> str:
    if entry["usage"]:
        u = entry["usage"]
        bits = [f"{k}={v}" for k, v in u.items() if v is not None]
        cost = f", ${entry['cost_usd']:.4f}" if entry.get("cost_usd") is not None else ""
        return f"tokens: {', '.join(bits)}{cost}"
    return f"tokens: ~{entry['estimated_tokens']} (estimated, no usage reported by backend)"
