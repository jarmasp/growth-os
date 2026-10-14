#!/bin/bash
# Growth OS — install. Clone -> this script -> edit config -> `growth onboard`.
# Claude Code / Cursor are optional extras (install-claude-code.sh, cursor/install-cursor.sh),
# not required: `growth <command>` is a standalone CLI, stdlib only.

set -e

GROWTH_OS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found on PATH -- install Python 3.10+ first." >&2
  exit 1
fi

echo "Growth OS install ($GROWTH_OS_DIR)"
echo ""

"$GROWTH_OS_DIR/growth" init
echo ""
"$GROWTH_OS_DIR/growth" doctor

LOCAL_BIN="$HOME/.local/bin"
case ":$PATH:" in
  *":$LOCAL_BIN:"*)
    mkdir -p "$LOCAL_BIN"
    ln -sf "$GROWTH_OS_DIR/growth" "$LOCAL_BIN/growth"
    echo ""
    echo "Linked: $LOCAL_BIN/growth -> $GROWTH_OS_DIR/growth -- run 'growth' from anywhere."
    ;;
  *)
    echo ""
    echo "$LOCAL_BIN isn't on your PATH, so 'growth' wasn't linked there."
    echo "Either add it to PATH and re-run this script, or just call $GROWTH_OS_DIR/growth directly."
    ;;
esac

echo ""
echo "Next steps:"
echo "  1. Edit your config (vault_root, vault_name, project_name) -- see the config path above."
echo "  2. growth onboard"
echo "  3. growth premortem / growth reflect on your next ticket"
echo ""
echo "Optional (both plain pip installs, skip either and the CLI degrades gracefully):"
echo "  pip install -r requirements-index.txt   # semantic search for growth index/search"
echo "  pip install -r requirements-corpus.txt  # .epub/.pdf parsing for a personal corpus"
echo ""
echo "Optional, only if you also want /growth:* slash commands inside an editor:"
echo "  bash $GROWTH_OS_DIR/install-claude-code.sh   # Claude Code"
echo "  bash $GROWTH_OS_DIR/cursor/install-cursor.sh  # Cursor"
