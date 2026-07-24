#!/usr/bin/env bash
set -euo pipefail

accept_new=false
if [[ "${1:-}" == "--accept-new" ]]; then
    accept_new=true
    shift
fi
if (($# != 0)); then
    echo "usage: scripts/fetch-rfcs.sh [--accept-new]" >&2
    exit 2
fi

test -s rfc/SOURCES
mkdir -p rfc
touch rfc/SHA256SUMS
new_files=()

while read -r number url role milestone; do
    [[ -n "${number:-}" ]] || continue
    [[ "$number" != \#* ]] || continue
    expected="https://www.rfc-editor.org/rfc/rfc${number}.txt"
    if [[ "$url" != "$expected" || -z "${role:-}" ||
        -z "${milestone:-}" ]]; then
        echo "invalid RFC source entry for ${number}" >&2
        exit 1
    fi

    destination="rfc/rfc${number}.txt"
    checksum_record="$(
        grep -E "^[0-9a-f]{64}  rfc${number}[.]txt$" rfc/SHA256SUMS || true
    )"
    if [[ -e "$destination" ]]; then
        if [[ -z "$checksum_record" ]]; then
            echo "unreviewed local RFC file exists: ${destination}" >&2
            exit 1
        fi
        (
            cd rfc
            printf '%s\n' "$checksum_record" | sha256sum --check --status
        ) || {
            echo "existing RFC ${number} differs from its trust pin" >&2
            exit 1
        }
        continue
    fi
    if ! $accept_new &&
        [[ -z "$checksum_record" ]]; then
        echo "RFC ${number} has no reviewed checksum; use --accept-new" >&2
        exit 1
    fi

    temporary="${destination}.tmp"
    rm -f "$temporary"
    trap 'rm -f "$temporary"' EXIT
    curl --fail --location --silent --show-error --proto '=https' --tlsv1.2 \
        --connect-timeout 10 --max-time 90 --max-filesize 8388608 \
        "$url" --output "$temporary"
    test -s "$temporary"
    [[ "$(wc -c <"$temporary")" -le 8388608 ]]
    head -n 80 "$temporary" |
        grep -Eiq "(request for comments:[[:space:]]*${number}|^rfc[-[:space:]]+${number}([[:space:]]|$))"
    mv "$temporary" "$destination"
    trap - EXIT
    if [[ -z "$checksum_record" ]]; then
        new_files+=("rfc${number}.txt")
    fi
done <rfc/SOURCES

if ((${#new_files[@]} > 0)); then
    temporary_manifest="rfc/SHA256SUMS.tmp"
    cp rfc/SHA256SUMS "$temporary_manifest"
    (
        cd rfc
        sha256sum "${new_files[@]}" >>SHA256SUMS.tmp
        sort -k2V SHA256SUMS.tmp -o SHA256SUMS.tmp
    )
    mv "$temporary_manifest" rfc/SHA256SUMS
fi

scripts/verify-rfcs.sh
scripts/lock-rfcs.sh
