#!/usr/bin/env bash
set -euo pipefail
project="${1:-}"
if [[ -z "$project" ]]; then
  echo "Usage: ./use-project.sh <cashea|void-foundry>"
  exit 1
fi
base_dir="$(cd "$(dirname "$0")" && pwd)"
source_cfg="$base_dir/config.${project}.json"
if [[ ! -f "$source_cfg" ]]; then
  echo "Config not found: $source_cfg"
  exit 1
fi
cp "$source_cfg" "$base_dir/config.json"
echo "Switched growth-os config to: $project"
