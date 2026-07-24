#!/usr/bin/env bash
set -euo pipefail

shopt -s nullglob
files=(rfc/rfc*.txt)
if ((${#files[@]} == 0)); then
    echo "no RFC files found" >&2
    exit 1
fi
chmod a-w "${files[@]}"
