#!/usr/bin/env sh
set -eu

for file in crates/*/src/lib.rs; do
    grep -q '#!\[forbid(unsafe_code)\]' "$file"
done

grep -q 'unknown-git = "deny"' deny.toml
grep -q 'unknown-registry = "deny"' deny.toml
grep -q 'panic = "abort"' Cargo.toml
grep -q 'CodeQL default setup' SECURITY.md
grep -q 'CodeQL analysis default setup is active' docs/github-security-settings.md
test -f docs/secret-handling-policy.md
test -f docs/threat-model.md
test -f docs/STANDARDS.md
test -f docs/PROTOCOLS.md
test -f docs/NAVHEIM_INTEGRATION.md
grep -q 'Navheim determines time from GNSS' docs/NAVHEIM_INTEGRATION.md
grep -q 'mundilfari-navheim' docs/RELEASE_PLAN.md
grep -q 'Phase 12: Navheim Integration As Final Feature Work' docs/RELEASE_PLAN.md
grep -q 'No new feature or protocol scope is introduced after `v0.157.0`' docs/RELEASE_PLAN.md
! rg -n '\bunsafe\s*\{' crates --glob '*.rs'
! rg -n \
    'name = "mundilfari-(gps|galileo|glonass|beidou|qzss|navic|nmea|rtcm|rinex|gpsd)' \
    crates --glob Cargo.toml

cargo metadata --format-version 1 |
    python3 -c '
import json
import sys

metadata = json.load(sys.stdin)
external = sorted(
    package["name"]
    for package in metadata["packages"]
    if package["source"] is not None
)
if external:
    raise SystemExit(
        "v0.1.0 must have no third-party Cargo packages: " + ", ".join(external)
    )
'
