#!/usr/bin/env bash
# Swap the active set of swappable site images.
#
# Two source sets live in image-sources/:
#   image-sources/handdrawn/  - original pencil/woodcut sketches
#   image-sources/photo/      - photographic versions (square, 1024x1024)
#
# This copies the chosen set over the live files in images/.
# After running, rebuild the site:  uv run python build/build.py
#
# Usage:
#   scripts/set-images.sh handdrawn   # revert to the sketches
#   scripts/set-images.sh photo       # use the photos
#
# To supply a BETTER image: drop a square PNG into image-sources/photo/
# using the same filename (e.g. talk.png), then run:  scripts/set-images.sh photo
set -euo pipefail

SET="${1:-}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/image-sources/$SET"

if [[ "$SET" != "handdrawn" && "$SET" != "photo" ]]; then
  echo "Usage: $0 <handdrawn|photo>" >&2
  exit 1
fi
if [[ ! -d "$SRC" ]]; then
  echo "No such set: $SRC" >&2
  exit 1
fi

n=0
for f in "$SRC"/*.png; do
  cp "$f" "$ROOT/images/$(basename "$f")"
  n=$((n+1))
done
echo "Activated '$SET' set: copied $n images to images/"
echo "Now rebuild:  uv run python build/build.py"
