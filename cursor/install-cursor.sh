#!/usr/bin/env bash
# Growth OS — install Cursor global integration (skills, rules, slash commands).
# Run from anywhere after clone:
#   bash ~/Documents/growth-os/cursor/install-cursor.sh

set -euo pipefail

GROWTH_OS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOT_CURSOR="${DOT_CURSOR:-$HOME/.cursor}"
CURSOR_CURSOR="$GROWTH_OS_DIR/cursor"

mkdir -p "$DOT_CURSOR/skills" "$DOT_CURSOR/rules" "$DOT_CURSOR/commands/growth"

link_skill() {
  local name="$1"
  local src="$CURSOR_CURSOR/skills/$name"
  local dest="$DOT_CURSOR/skills/$name"
  [[ -d "$src" ]] || { echo "skip skill (missing): $name" >&2; return 0; }
  ln -sfn "$src" "$dest"
  echo "  skill: $dest -> $src"
}

link_rule() {
  local src="$1"
  local base
  base="$(basename "$src")"
  local dest="$DOT_CURSOR/rules/$base"
  [[ -e "$src" ]] || return 0
  ln -sfn "$src" "$dest"
  echo "  rule: $dest -> $src"
}

link_command() {
  local src="$1"
  local base
  base="$(basename "$src")"
  local dest="$DOT_CURSOR/commands/growth/$base"
  ln -sfn "$src" "$dest"
  echo "  command: $dest -> $src"
}

echo "Growth OS → Cursor (source: $GROWTH_OS_DIR)"

for skill in growth-reflect growth-premortem growth-weekly growth-concept growth-onboard; do
  link_skill "$skill"
done

for rule in "$CURSOR_CURSOR"/rules/*.mdc; do
  [[ -f "$rule" ]] && link_rule "$rule"
done

for cmd in "$GROWTH_OS_DIR"/commands/growth/*.md; do
  [[ -f "$cmd" ]] && link_command "$cmd"
done

# Stable path expected by workflows (~/Documents/growth-os)
if [[ ! -e "$HOME/Documents/growth-os" ]]; then
  ln -sfn "$GROWTH_OS_DIR" "$HOME/Documents/growth-os"
  echo "  symlink: ~/Documents/growth-os -> $GROWTH_OS_DIR"
fi

echo ""
echo "Done. Reload Cursor (Cmd+Shift+P → Developer: Reload Window)."
echo "Commands: /growth-reflect, /growth-premortem, /growth-weekly, /growth-concept, /growth-onboard"
echo "Also works via Claude Code: bash $GROWTH_OS_DIR/install.sh"
