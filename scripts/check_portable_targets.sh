#!/usr/bin/env sh
set -eu

for target in \
    x86_64-unknown-linux-gnu \
    x86_64-pc-windows-msvc \
    x86_64-unknown-freebsd \
    x86_64-unknown-netbsd \
    x86_64-apple-darwin \
    aarch64-linux-android \
    aarch64-apple-ios; do
    cargo +1.97.1 check \
        --workspace \
        --no-default-features \
        --target "$target"
done
