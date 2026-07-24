#!/usr/bin/env sh
set -eu

unset MUNDILFARI_RELEASE_PUBLISH_TAG

tmp="$(mktemp -d "${TMPDIR:-/tmp}/mundilfari-readiness.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
mkdir -p "$tmp/bin"

fake_cargo="$tmp/bin/cargo"
printf '%s\n' \
    '#!/usr/bin/env sh' \
    'set -eu' \
    'test "${1:-}" = "sbom"' \
    'printf '"'"'{"spdxVersion":"SPDX-2.3"}\n'"'"'' \
    >"$fake_cargo"
chmod +x "$fake_cargo"
PATH="$tmp/bin:$PATH"
export PATH

source_readiness="$(pwd)/scripts/validate-release-readiness.sh"
source_generate="$(pwd)/scripts/generate-sbom.sh"
source_compare="$(pwd)/scripts/compare_sbom.py"

make_fixture() {
    name="$1"
    repo="$tmp/$name"
    mkdir -p \
        "$repo/scripts" \
        "$repo/release-notes" \
        "$repo/security/pentest" \
        "$repo/sbom"
    cp "$source_readiness" "$repo/scripts/validate-release-readiness.sh"
    cp "$source_generate" "$repo/scripts/generate-sbom.sh"
    cp "$source_compare" "$repo/scripts/compare_sbom.py"
    (
        cd "$repo"
        git init -q
        git config user.email "release-readiness@example.invalid"
        git config user.name "Release Readiness Test"
        printf 'fixture\n' >README.md
        git add README.md
        git commit -q -m "fixture"
    )
    printf '%s\n' "$repo"
}

assert_fails_with() {
    expected="$1"
    shift
    if "$@" >"$tmp/stdout" 2>"$tmp/stderr"; then
        echo "expected command to fail: $*" >&2
        exit 1
    fi
    if ! grep -q "$expected" "$tmp/stderr"; then
        echo "expected stderr to contain: $expected" >&2
        sed -n '1,120p' "$tmp/stderr" >&2
        exit 1
    fi
}

write_release_notes() {
    version="$1"
    printf '# Release %s\n' "$version" \
        >"release-notes/RELEASE_NOTES_${version}.md"
}

write_sbom() {
    printf '{"spdxVersion":"SPDX-2.3"}\n' >sbom/mundilfari.spdx.json
}

write_pentest() {
    tag="$1"
    reviewed_commit="$2"
    report="security/pentest/${tag}.md"
    printf '%s\n' \
        'Status: PASS' \
        "Reviewed-Commit: $reviewed_commit" \
        'Tester: Release Readiness Test' \
        'Scope: Fixture release metadata.' \
        'Date: 2026-07-24' \
        >"$report"
}

repo="$(make_fixture bad-tag)"
(
    cd "$repo"
    assert_fails_with "usage: scripts/validate-release-readiness.sh vX.Y.Z" \
        scripts/validate-release-readiness.sh "0.2.0"
    assert_fails_with "usage: scripts/validate-release-readiness.sh vX.Y.Z" \
        scripts/validate-release-readiness.sh "v0.2.0-extra"
)

repo="$(make_fixture existing-tag)"
(
    cd "$repo"
    git tag v9.9.9
    assert_fails_with "tag already exists locally: v9.9.9" \
        scripts/validate-release-readiness.sh "v9.9.9"
)

repo="$(make_fixture missing-inputs)"
(
    cd "$repo"
    assert_fails_with "missing release notes" \
        scripts/validate-release-readiness.sh "v0.2.0"
    write_release_notes "0.2.0"
    assert_fails_with "missing or empty SBOM" \
        scripts/validate-release-readiness.sh "v0.2.0"
    write_sbom
    assert_fails_with "missing pentest report" \
        scripts/validate-release-readiness.sh "v0.2.0"
)

repo="$(make_fixture uncommitted-report)"
(
    cd "$repo"
    reviewed_commit="$(git rev-parse HEAD)"
    write_release_notes "0.2.0"
    write_sbom
    write_pentest "v0.2.0" "$reviewed_commit"
    assert_fails_with "pentest report must be committed" \
        scripts/validate-release-readiness.sh "v0.2.0"
)

repo="$(make_fixture mixed-report-commit)"
(
    cd "$repo"
    reviewed_commit="$(git rev-parse HEAD)"
    write_release_notes "0.2.0"
    write_sbom
    write_pentest "v0.2.0" "$reviewed_commit"
    printf 'changed\n' >>README.md
    git add README.md security/pentest/v0.2.0.md
    git commit -q -m "report plus code"
    assert_fails_with "release report commit may only change" \
        scripts/validate-release-readiness.sh "v0.2.0"
)

repo="$(make_fixture ready)"
(
    cd "$repo"
    reviewed_commit="$(git rev-parse HEAD)"
    write_release_notes "0.2.0"
    write_sbom
    write_pentest "v0.2.0" "$reviewed_commit"
    git add security/pentest/v0.2.0.md
    git commit -q -m "report"
    scripts/validate-release-readiness.sh "v0.2.0"
    git tag "v0.2.0"
    MUNDILFARI_RELEASE_PUBLISH_TAG="v0.2.0" \
        scripts/validate-release-readiness.sh "v0.2.0"
)

repo="$(make_fixture stale-publish-tag)"
(
    cd "$repo"
    git tag "v0.2.0"
    printf 'later\n' >later.txt
    git add later.txt
    git commit -q -m "later"
    assert_fails_with "does not point at HEAD" \
        env MUNDILFARI_RELEASE_PUBLISH_TAG="v0.2.0" \
        scripts/validate-release-readiness.sh "v0.2.0"
)

echo "release readiness fixture tests passed"
