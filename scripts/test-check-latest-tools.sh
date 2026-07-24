#!/usr/bin/env sh
set -eu

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

toolchain_file="$tmp_dir/rust-toolchain.toml"
manifest_file="$tmp_dir/channel-rust-stable.toml"

write_toolchain() {
    version="$1"
    printf '[toolchain]\nchannel = "%s"\n' "$version" >"$toolchain_file"
}

write_toolchain "1.97.1"
cat >"$manifest_file" <<'EOF'
manifest-version = "2"

[pkg.rust]
version = "1.97.1 (fixture)"
EOF

RUST_TOOLCHAIN_FILE="$toolchain_file" \
RUST_STABLE_MANIFEST_URL="file://$manifest_file" \
CHECK_LATEST_TOOLS_RUST_ONLY=1 \
    scripts/check_latest_tools.sh

write_toolchain "1.97.0"
if RUST_TOOLCHAIN_FILE="$toolchain_file" \
    RUST_STABLE_MANIFEST_URL="file://$manifest_file" \
    CHECK_LATEST_TOOLS_RUST_ONLY=1 \
    scripts/check_latest_tools.sh >/dev/null 2>&1; then
    echo "stale Rust pin was accepted" >&2
    exit 1
fi

printf 'manifest-version = "2"\n' >"$manifest_file"
if RUST_TOOLCHAIN_FILE="$toolchain_file" \
    RUST_STABLE_MANIFEST_URL="file://$manifest_file" \
    CHECK_LATEST_TOOLS_RUST_ONLY=1 \
    scripts/check_latest_tools.sh >/dev/null 2>&1; then
    echo "missing stable Rust version was accepted" >&2
    exit 1
fi

echo "latest tool check tests passed"
