#!/usr/bin/env sh
set -eu

find scripts -type f -name '*.sh' -print | while IFS= read -r script; do
    first_line=$(sed -n '1p' "$script")
    case "$first_line" in
        *bash) bash -n "$script" ;;
        *) sh -n "$script" ;;
    esac
done
