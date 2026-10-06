#!/usr/bin/env bash
set -euo pipefail
project="${1:-}"
base_dir="$(cd "$(dirname "$0")" && pwd)"
if [[ -z "$project" ]]; then
  available=$(ls "$base_dir"/config.*.json 2>/dev/null | sed -E 's#.*/config\.(.*)\.json#\1#' | grep -v '^example$' | paste -sd '|' -)
  echo "Usage: ./use-project.sh <${available:-your-project-name}>"
  exit 1
fi
source_cfg="$base_dir/config.${project}.json"
if [[ ! -f "$source_cfg" ]]; then
  echo "Config not found: $source_cfg"
  exit 1
fi
cp "$source_cfg" "$base_dir/config.json"
echo "Switched growth-os config to: $project"
