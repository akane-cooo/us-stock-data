#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

work_dir=$(mktemp -d)
trap 'rm -rf -- "$work_dir"' EXIT

.venv/bin/python main.py --mode download 2>&1 | tee "$work_dir/download.log"
if grep -q 'failed symbols: ' "$work_dir/download.log"; then
  printf '%s\n' 'Some downloads failed. Release skipped.' >&2
  exit 1
fi

.venv/bin/python main.py --mode dump

release_date=$(tail -n 1 data/us_stock/calendars/day.txt)
if [[ ! "$release_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  printf '%s\n' 'The calendar has no valid release date.' >&2
  exit 1
fi

archive="$work_dir/us_stock-${release_date}.tar.gz"
tar -czf "$archive" -C data us_stock

gh release create "$release_date" "$archive"\
  --repo akane-cooo/us-stock-data \
  --title "$release_date" \
  --notes "US stock data through $release_date."