# Mundilfari Toolchain Policy

Mundilfari pins stable Rust `1.97.1` and supports published crates from Rust
`1.90.0` through `1.97.1`.

| Compiler | Support |
| --- | --- |
| `1.90.0` | MSRV; tests and all-feature check |
| `1.91.0`, `1.91.1` | supported |
| `1.92.0` | supported |
| `1.93.0`, `1.93.1` | supported |
| `1.94.0`, `1.94.1` | supported |
| `1.95.0` | supported |
| `1.96.0`, `1.96.1` | supported |
| `1.97.0` | supported |
| `1.97.1` | pinned development and release toolchain |

Rules:

- `scripts/check_latest_tools.sh` compares the pin with the official stable
  distribution manifest.
- `workspace.package.rust-version` remains the MSRV.
- Release gates check every installed supported compiler version.
- The full lint, documentation, package, audit, and release gate runs on the
  pin.
- Normal builds never require nightly.
- Repository-only automation may require Rust `1.97.1`.
- A new stable Rust release updates the pin and compatibility table without
  automatically changing the MSRV.

Compatibility command:

```bash
for toolchain in \
    1.90.0 1.91.0 1.91.1 1.92.0 1.93.0 1.93.1 1.94.0 1.94.1 \
    1.95.0 1.96.0 1.96.1 1.97.0 1.97.1; do
    cargo "+$toolchain" check --workspace --all-features
done
```
