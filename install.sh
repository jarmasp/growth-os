#!/bin/bash
# Growth OS — Install Claude Code commands globally
# Creates symlinks from ~/.claude/commands/ to growth-os/commands/
# Run once after cloning. Re-run to update after adding new commands.

set -e

GROWTH_OS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_COMMANDS_DIR="$HOME/.claude/commands"

mkdir -p "$CLAUDE_COMMANDS_DIR"

echo "Installing Growth OS commands..."

for cmd in "$GROWTH_OS_DIR/commands"/*.md; do
  filename=$(basename "$cmd")
  target="$CLAUDE_COMMANDS_DIR/$filename"

  if [ -L "$target" ]; then
    echo "  updating symlink: $filename"
    ln -sf "$cmd" "$target"
  elif [ -f "$target" ]; then
    echo "  replacing file with symlink: $filename"
    rm "$target"
    ln -sf "$cmd" "$target"
  else
    echo "  linking: $filename"
    ln -sf "$cmd" "$target"
  fi
done

echo ""
echo "Done. Commands available in Claude Code:"
for cmd in "$GROWTH_OS_DIR/commands"/*.md; do
  filename=$(basename "$cmd" .md)
  echo "  /$filename"
done
