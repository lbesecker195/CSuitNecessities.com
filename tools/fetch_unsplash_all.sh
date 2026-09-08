#!/usr/bin/env bash
# Fill in Unsplash photos for every remaining product, waiting out the
# 50-requests/hour demo-app rate limit between passes.
#
#   export UNSPLASH_ACCESS_KEY=...
#   ./tools/fetch_unsplash_all.sh
#
# Safe to stop and re-run: products that already have a photoId are skipped.
set -u
cd "$(dirname "$0")/.."

remaining() {
  python3 -c "
import yaml
o = yaml.safe_load(open('data/offers.yaml'))
print(sum(1 for v in o.values() if not v.get('photoId')))"
}

for pass in $(seq 1 6); do
  left=$(remaining)
  if [ "$left" -eq 0 ]; then
    echo "== all products have photos =="
    break
  fi
  echo "== pass $pass: $left products still need a photo =="
  python3 tools/fetch_unsplash.py 2>&1 | tail -40

  left=$(remaining)
  [ "$left" -eq 0 ] && { echo "== complete =="; break; }

  echo "== rate limited with $left left; sleeping 62 min for the window to reset =="
  sleep 3720
done

echo "== final: $(remaining) products without a photo =="
hugo --gc --minify 2>&1 | tail -3
