"""Config resolution: ~/.growth-os/config.json (canonical) with a fallback to the
repo-root config.json (the pre-v3.0 location, kept working so existing installs —
like growth-os-me's symlink setup — don't break until they run `growth init`).
"""
import json
import os
from pathlib import Path

GROWTH_OS_HOME = Path(os.environ.get("GROWTH_OS_HOME", Path(__file__).resolve().parent.parent))
CANONICAL_CONFIG = Path.home() / ".growth-os" / "config.json"
FALLBACK_CONFIG = GROWTH_OS_HOME / "config.json"
STATE_DIR = Path.home() / ".growth-os"


class ConfigError(RuntimeError):
    pass


def config_path() -> Path:
    override = os.environ.get("GROWTH_OS_CONFIG")
    if override:
        return Path(override).expanduser()
    if CANONICAL_CONFIG.exists():
        return CANONICAL_CONFIG
    if FALLBACK_CONFIG.exists() and not FALLBACK_CONFIG.is_symlink():
        # A real config.json committed at repo root (shouldn't happen in the public
        # repo — gitignored — but can happen in a private fork like growth-os-me).
        return FALLBACK_CONFIG
    if FALLBACK_CONFIG.is_symlink() and FALLBACK_CONFIG.exists():
        return FALLBACK_CONFIG
    raise ConfigError(
        "No config found. Run `growth init` to create ~/.growth-os/config.json, "
        "or `cp config.example.json config.json` at the repo root for the legacy path."
    )


def load() -> dict:
    path = config_path()
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise ConfigError(f"{path} is not valid JSON: {e}") from e


def vault_root(cfg: dict) -> Path:
    root = cfg.get("vault_root")
    if not root:
        raise ConfigError("config.json has no vault_root set.")
    return Path(root).expanduser()


def vault_subdir(cfg: dict, key: str) -> Path:
    name = cfg.get("vault", {}).get(key)
    if not name:
        raise ConfigError(f"config.json vault.{key} is not set.")
    return vault_root(cfg) / name


def workflow_path(name: str) -> Path:
    return GROWTH_OS_HOME / "workflows" / name


def agent_path(name: str) -> Path:
    return GROWTH_OS_HOME / "agents" / name
