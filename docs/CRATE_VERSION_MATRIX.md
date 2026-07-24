# Crate version matrix

Only crates marked **crates.io** are published. Repository-only tools may use
Rust 1.97.1 features and never enter the public dependency graph.

| Crate or tool | Distribution | Version | Rust floor | Default environment |
| --- | --- | ---: | ---: | --- |
| `mundilfari-core` | crates.io | 0.1.0 | 1.90.0 | `no_std` |
| `mundilfari-engine` | crates.io | 0.1.0 | 1.90.0 | `no_std` |
| `mundilfari-platform` | crates.io | 0.1.0 | 1.90.0 | `no_std` |
| `mundilfari` | crates.io | 0.1.0 | 1.90.0 | `no_std` |
| `tools/xtask` | repository only | 0.1.0 | 1.97.1 | `std` |

The current compatibility window tests every stable patch from Rust 1.90.0
through 1.97.1 that appears in [toolchain-policy.md](toolchain-policy.md).

## Planned Companion

`mundilfari-navheim` is not a current workspace member. It will become an
optional crates.io crate only after Navheim publishes its reviewed stable GNSS
timing API. Its initial version and exact Navheim compatibility range remain
unset until upstream admission. It must retain the published-library Rust
1.90.0 floor unless a separately reviewed compatibility decision says
otherwise.
