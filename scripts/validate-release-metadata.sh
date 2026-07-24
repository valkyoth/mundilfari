#!/usr/bin/env sh
set -eu

test ! -f PENTEST.md
for file in \
    LICENSE-MIT LICENSE-APACHE SECURITY.md CHANGELOG.md Cargo.toml Cargo.lock \
    deny.toml rust-toolchain.toml release-crates.toml \
    release-notes/RELEASE_NOTES_0.1.0.md \
    .github/CODEOWNERS .github/FUNDING.yml .github/dependabot.yml \
    .github/workflows/ci.yml .github/workflows/release.yml \
    docs/IMPLEMENTATION_PLAN.md docs/RELEASE_PLAN.md docs/PROTOCOLS.md \
    docs/NAVHEIM_INTEGRATION.md \
    docs/STANDARDS.md docs/threat-model.md docs/toolchain-policy.md \
    docs/modularity-policy.md docs/unsafe-policy.md \
    docs/supply-chain-security.md docs/github-security-settings.md; do
    test -f "$file"
done

for script in \
    scripts/checks.sh scripts/check_latest_tools.sh \
    scripts/check_portable_targets.sh \
    scripts/test-check-latest-tools.sh scripts/check_doc_links.sh \
    scripts/check_shell_syntax.sh scripts/generate-sbom.sh \
    scripts/validate-modularity-policy.sh scripts/validate-security-policy.sh \
    scripts/validate-release-readiness.sh scripts/release_0_1_gate.sh \
    scripts/release_crates.py scripts/test-release-crates.py; do
    test -x "$script"
done

release_version="$(
    python3 -c 'import tomllib; print(tomllib.load(open("release-crates.toml", "rb"))["release"]["version"])'
)"
facade_version="$(
    cargo metadata --format-version 1 --no-deps |
        python3 -c 'import json,sys; d=json.load(sys.stdin); print(next(p["version"] for p in d["packages"] if p["name"]=="mundilfari"))'
)"
test "$release_version" = "$facade_version"
test "$release_version" = "0.1.0"

cmp -s README.md crates/mundilfari/README.md
grep -q 'license = "MIT OR Apache-2.0"' Cargo.toml
grep -q 'repository = "https://github.com/valkyoth/mundilfari"' Cargo.toml
grep -q 'rust-version = "1.90"' Cargo.toml
grep -q 'channel = "1.97.1"' rust-toolchain.toml
grep -q 'cargo-deny --version 0.20.2' .github/workflows/ci.yml
grep -q 'cargo-audit --version 0.22.2' .github/workflows/ci.yml
grep -q 'cargo-sbom --version 0.10.0' .github/workflows/ci.yml
grep -q 'actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1' \
    .github/workflows/ci.yml
grep -q 'workflow_dispatch:' .github/workflows/release.yml
! grep -q 'tags:' .github/workflows/release.yml
