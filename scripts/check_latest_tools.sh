#!/usr/bin/env sh
set -eu

ci_file=".github/workflows/ci.yml"
rust_toolchain_file="${RUST_TOOLCHAIN_FILE:-rust-toolchain.toml}"
rust_stable_manifest_url="${RUST_STABLE_MANIFEST_URL:-https://static.rust-lang.org/dist/channel-rust-stable.toml}"
checkout_repo_url="${CHECKOUT_REPO_URL:-https://github.com/actions/checkout.git}"

pinned_rust_version() {
    sed -n 's/^channel = "\([0-9][0-9.]*\)"$/\1/p' "$rust_toolchain_file" |
        head -n 1
}

latest_stable_rust_version() {
    curl -fsSL "$rust_stable_manifest_url" |
        sed -n '/^\[pkg\.rust\]$/,/^\[/ {
            s/^version = "\([0-9][0-9.]*\) .*/\1/p
        }' |
        head -n 1
}

check_latest_rust() {
    pinned="$(pinned_rust_version)"
    latest="$(latest_stable_rust_version)"
    test -n "$pinned" || {
        echo "missing pinned Rust version" >&2
        exit 1
    }
    test -n "$latest" || {
        echo "could not determine latest stable Rust version" >&2
        exit 1
    }
    test "$pinned" = "$latest" || {
        echo "Rust is not latest stable: pinned $pinned, latest $latest" >&2
        exit 1
    }
}

ci_tool_version() {
    tool="$1"
    sed -n "s/.*cargo install --locked ${tool} --version \\([0-9][^ ]*\\).*/\\1/p" \
        "$ci_file" | head -n 1
}

latest_crate_version() {
    cargo info "$1" | sed -n 's/^version: //p' | head -n 1
}

check_cargo_tool() {
    tool="$1"
    pinned="$(ci_tool_version "$tool")"
    latest="$(latest_crate_version "$tool")"
    test -n "$pinned" || {
        echo "missing pinned CI version for $tool" >&2
        exit 1
    }
    test -n "$latest" || {
        echo "could not determine latest crates.io version for $tool" >&2
        exit 1
    }
    test "$pinned" = "$latest" || {
        echo "$tool is not latest: pinned $pinned, latest $latest" >&2
        exit 1
    }
}

check_all_actions_sha_pinned() {
    failed=0
    while IFS= read -r ref; do
        case "$ref" in
            "") ;;
            [0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]) ;;
            *)
                echo "GitHub Actions ref is not a full SHA: $ref" >&2
                failed=1
                ;;
        esac
    done <<EOF
$(sed -n 's/^[[:space:]]*uses: [^@][^@]*@\([^[:space:]]*\).*/\1/p' .github/workflows/*.yml)
EOF
    test "$failed" -eq 0
}

checkout_pin_line() {
    sed -n 's/.*uses: actions\/checkout@\([0-9a-f]\{40\}\) # \(v[0-9][0-9.]*\).*/\1 \2/p' \
        "$ci_file" | head -n 1
}

latest_checkout_tag() {
    git ls-remote --tags --refs "$checkout_repo_url" 'refs/tags/v*' |
        sed 's#.*refs/tags/##' |
        grep -E '^v[0-9]+(\.[0-9]+)*$' |
        sort -V |
        tail -n 1
}

checkout_tag_sha() {
    git ls-remote --tags --refs "$checkout_repo_url" "refs/tags/$1" |
        awk '{ print $1 }'
}

check_checkout_action() {
    pin_line="$(checkout_pin_line)"
    test -n "$pin_line" || {
        echo "actions/checkout must use a full SHA and semver comment" >&2
        exit 1
    }
    pinned_sha="$(printf '%s\n' "$pin_line" | awk '{ print $1 }')"
    pinned_tag="$(printf '%s\n' "$pin_line" | awk '{ print $2 }')"
    latest_tag="$(latest_checkout_tag)"
    test "$pinned_tag" = "$latest_tag" || {
        echo "actions/checkout is not latest: pinned $pinned_tag, latest $latest_tag" >&2
        exit 1
    }
    latest_sha="$(checkout_tag_sha "$latest_tag")"
    test "$pinned_sha" = "$latest_sha" || {
        echo "actions/checkout $latest_tag SHA mismatch" >&2
        exit 1
    }
}

check_latest_rust
if [ "${CHECK_LATEST_TOOLS_RUST_ONLY:-0}" = "1" ]; then
    exit 0
fi

check_cargo_tool cargo-deny
check_cargo_tool cargo-audit
check_cargo_tool cargo-sbom
check_all_actions_sha_pinned
check_checkout_action
