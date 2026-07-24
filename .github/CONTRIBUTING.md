# Contributing To Mundilfari

Mundilfari is security-sensitive time-protocol infrastructure. Contributions
must keep the workspace explicit, bounded, tested, and honest about protocol,
platform, accuracy, authentication, and conformance claims.

## License

Mundilfari is licensed under `MIT OR Apache-2.0`. By contributing, you agree
that your contribution is available under those terms.

## Development Setup

Use the pinned Rust toolchain from `rust-toolchain.toml`.

```bash
cargo check --workspace --all-features
cargo test --workspace --all-features
```

Before opening a pull request, run:

```bash
scripts/checks.sh
```

## Security-Sensitive Changes

Treat these areas as high risk:

- time arithmetic, epochs, eras, scales, and leap-second conversion;
- wire parsing, resource limits, state transitions, and timers;
- source authentication, freshness, consensus, and downgrade policy;
- clock servos, holdover, and any clock-modification authority;
- cryptographic, TLS, entropy, or certificate boundaries;
- raw sockets, timestamp ancillary data, PHC, PPS, and platform FFI;
- daemon privilege separation and local IPC;
- CI, release scripts, specifications, dependencies, and generated fixtures.

Do not post exploitable details in public issues. Follow
[SECURITY.md](../SECURITY.md).

## Dependency Policy

Before adding or updating a third-party crate:

- verify the latest crates.io version;
- document why generic infrastructure is needed instead of first-party
  time-protocol logic;
- review license, maintenance, MSRV, default features, transitive crates, and
  native code;
- keep it optional outside the capability that needs it;
- avoid git dependencies;
- update `Cargo.lock`, SBOM evidence, threat model, and dependency records;
- run `cargo deny check`, `cargo audit`, and behavior-specific tests.
