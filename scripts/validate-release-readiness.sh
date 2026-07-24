#!/usr/bin/env sh
set -eu

tag="${1:-}"
case "$tag" in
    v*) ;;
    *)
        echo "usage: scripts/validate-release-readiness.sh vX.Y.Z" >&2
        exit 2
        ;;
esac

version="${tag#v}"
old_ifs="$IFS"
IFS=.
set -- $version
IFS="$old_ifs"
if [ "$#" -ne 3 ]; then
    echo "usage: scripts/validate-release-readiness.sh vX.Y.Z" >&2
    exit 2
fi
for component in "$@"; do
    case "$component" in
        ""|*[!0-9]*)
            echo "usage: scripts/validate-release-readiness.sh vX.Y.Z" >&2
            exit 2
            ;;
    esac
done

release_notes="release-notes/RELEASE_NOTES_${version}.md"
pentest_report="security/pentest/${tag}.md"
publish_tag="${MUNDILFARI_RELEASE_PUBLISH_TAG:-}"

if git rev-parse -q --verify "refs/tags/$tag" >/dev/null; then
    if [ "$publish_tag" != "$tag" ]; then
        echo "tag already exists locally: $tag" >&2
        exit 1
    fi
    test "$(git rev-list -n 1 "$tag")" = "$(git rev-parse HEAD)" || {
        echo "publish tag $tag does not point at HEAD" >&2
        exit 1
    }
elif [ -n "$publish_tag" ]; then
    echo "publish tag context requires existing tag: $tag" >&2
    exit 1
fi

test ! -f PENTEST.md || {
    echo "root PENTEST.md is temporary scratch input and must be removed" >&2
    exit 1
}
test -f "$release_notes" || {
    echo "missing release notes: $release_notes" >&2
    exit 1
}
test -s sbom/mundilfari.spdx.json || {
    echo "missing or empty SBOM: sbom/mundilfari.spdx.json" >&2
    exit 1
}
scripts/generate-sbom.sh --check
test -f "$pentest_report" || {
    echo "missing pentest report: $pentest_report" >&2
    exit 1
}
git cat-file -e "HEAD:$pentest_report" 2>/dev/null || {
    echo "pentest report must be committed in tag candidate: $pentest_report" >&2
    exit 1
}

grep -q '^Status: PASS$' "$pentest_report"
grep -Eq '^Reviewed-Commit: [0-9a-f]{40}$' "$pentest_report"
grep -Eq '^Tester: .+' "$pentest_report"
grep -Eq '^Scope: .+' "$pentest_report"
grep -Eq '^Date: [0-9]{4}-[0-9]{2}-[0-9]{2}$' "$pentest_report"

reviewed_commit="$(sed -n 's/^Reviewed-Commit: //p' "$pentest_report")"
git cat-file -e "${reviewed_commit}^{commit}" 2>/dev/null || {
    echo "reviewed commit $reviewed_commit was not found" >&2
    exit 1
}
test "$reviewed_commit" = "$(git rev-parse HEAD^)" || {
    echo "reviewed commit does not match first parent" >&2
    exit 1
}
test "$(git diff --name-only "$reviewed_commit" HEAD)" = "$pentest_report" || {
    echo "release report commit may only change $pentest_report" >&2
    exit 1
}
