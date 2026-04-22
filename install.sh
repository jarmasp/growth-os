#!/bin/bash
# Growth OS — Install Claude Code commands globally
# Creates symlinks from ~/.claude/commands/growth/ to growth-os/commands/growth/
# Run once after cloning. Re-run to update after adding new commands.

set -e

GROWTH_OS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_COMMANDS_DIR="$HOME/.claude/commands"
GROWTH_COMMANDS_SRC="$GROWTH_OS_DIR/commands/growth"
GROWTH_COMMANDS_DST="$CLAUDE_COMMANDS_DIR/growth"

mkdir -p "$GROWTH_COMMANDS_DST"

# Remove old flat symlinks if upgrading from pre-namespace install
for old in reflect concept weekly onboard; do
  old_link="$CLAUDE_COMMANDS_DIR/$old.md"
  if [ -L "$old_link" ]; then
    echo "  removing old symlink: $old.md"
    rm "$old_link"
  fi
done

echo "Installing Growth OS commands..."

for cmd in "$GROWTH_COMMANDS_SRC"/*.md; do
  filename=$(basename "$cmd")
  target="$GROWTH_COMMANDS_DST/$filename"

  if [ -L "$target" ]; then
    echo "  updating symlink: growth/$filename"
    ln -sf "$cmd" "$target"
  elif [ -f "$target" ]; then
    echo "  replacing file with symlink: growth/$filename"
    rm "$target"
    ln -sf "$cmd" "$target"
  else
    echo "  linking: growth/$filename"
    ln -sf "$cmd" "$target"
  fi
done

echo ""
echo "Done. Commands available in Claude Code:"
for cmd in "$GROWTH_COMMANDS_SRC"/*.md; do
  filename=$(basename "$cmd" .md)
  echo "  /growth:$filename"
done

echo ""
echo "Next step: run /growth:onboard in Claude Code to set up your profile and scaffold your Obsidian vault."
