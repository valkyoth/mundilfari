#!/usr/bin/env sh
set -eu

scripts/checks.sh
scripts/check_latest_tools.sh

for toolchain in \
    1.90.0 1.91.0 1.91.1 1.92.0 1.93.0 1.93.1 1.94.0 \
    1.94.1 1.95.0 1.96.0 1.96.1 1.97.0 1.97.1; do
    cargo "+$toolchain" check --workspace --all-features
done

scripts/check_portable_targets.sh
