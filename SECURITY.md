# Security Policy

Mundilfari is security-sensitive protocol and clock software. Treat time
arithmetic, parsing, state machines, source selection, authentication,
uncertainty, clock discipline, platform timestamps, privileged helpers,
release scripts, standards, CI, and dependencies as high risk until reviewed
and tested.

## Current Security Status

Version `0.1.0` is a repository foundation. It contains no protocol parsers,
network clients, cryptography, TLS, platform FFI, privileged clock control, or
production time source. Do not use it to make security or clock-discipline
decisions.

## Routine Checks

Run these regularly and before releases:

```bash
scripts/checks.sh
scripts/check_latest_tools.sh
scripts/release_0_1_gate.sh
cargo deny check
cargo audit
scripts/generate-sbom.sh --check
```

GitHub Actions run CI. GitHub CodeQL default setup must be enabled in repository
security settings. Do not add an advanced CodeQL workflow while default setup
is active. The required review is documented in
[GitHub Security Settings](docs/github-security-settings.md).

## Release Gate

Every release tag must point at a final pentest-report commit. The matching
`security/pentest/vX.Y.Z.md` report must have `Status: PASS`, and
`scripts/validate-release-readiness.sh vX.Y.Z` must pass before the tag is
created.

The report commit must be the direct linear child of the reviewed
implementation commit and may change only the permanent report. Do not rewrite
the release branch between review and tagging.

## Protocol Security Rules

- Parsing does not grant semantic validity or clock authority.
- Authentication, accuracy, uncertainty, freshness, and traceability are
  independent properties.
- No silent downgrade from authenticated to unauthenticated time.
- Legacy and historical protocols are disabled in secure defaults.
- GNSS interpretation comes only from admitted Navheim timing evidence;
  Mundilfari preserves invalidation, health, authentication, integrity,
  freshness, uncertainty, and provenance without re-decoding it.
- Navheim evidence never grants clock authority without independent
  Mundilfari source and discipline policy.
- Large, backward, or post-startup clock steps require explicit policy.
- Delay attacks remain in scope even when a protocol is authenticated.
- Official specifications, revisions, and verified errata precede protocol
  claims.
- Precision claims require end-to-end hardware and measurement evidence.

## Dependency Policy

The dependency policy lives in `deny.toml`. Unknown registries and git sources
are denied. Mundilfari implements time semantics and time protocols itself;
reviewed generic TLS, cryptographic, or OS-binding crates may be admitted only
at documented optional boundaries.

Every new or updated third-party crate requires:

- current-version verification;
- license, maintenance, MSRV, feature, transitive, and native-code review;
- no hidden `std`, network, filesystem, entropy, or privileged expansion in
  core crates;
- behavior and failure tests;
- threat-model, SBOM, and release-note updates;
- `cargo deny check` and `cargo audit` evidence.

## Reporting

Do not publish exploitable security details before a fix is available. Use a
private GitHub security advisory or contact the maintainers through the
repository's configured private security channel.
