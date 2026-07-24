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

Any new or changed production source must update
`compliance/IMPLEMENTATION_EVIDENCE.json`. Link every governing requirement to
concrete tests. Protocol, profile, format, and protocol-integration code must
also record exact reviewed source identifiers, SHA-256 values, clauses, and
errata dispositions. The common gate rejects an unregistered source file or a
requirement without a real test function. Any production-source edit changes
its reviewed implementation hash and requires the evidence review to be
performed again.

## Security-Sensitive Changes

Treat these areas as high risk:

- time arithmetic, epochs, eras, scales, and leap-second conversion;
- wire parsing, resource limits, state transitions, and timers;
- source authentication, freshness, consensus, and downgrade policy;
- clock servos, holdover, and any clock-modification authority;
- cryptographic, TLS, entropy, or certificate boundaries;
- raw sockets, timestamp ancillary data, PHC, PPS, and platform FFI;
- Navheim version admission, GNSS evidence mapping, and invalidation handling;
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

Navheim is the planned GNSS implementation dependency, but it may appear only
in `mundilfari-navheim` after the stable upstream timing API passes the complete
admission process. Do not copy provisional Navheim types or GNSS decoders into
this workspace.
