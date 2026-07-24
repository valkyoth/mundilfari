# Mundilfari 0.1.0 Release Notes

Status: awaiting implementation pentest

## Summary

`0.1.0` establishes the repository, architecture, security, documentation, and
release foundation for a `no_std`-first time-protocol framework.

This version does not implement a time protocol, trusted clock, network client,
clock servo, hardware timestamp, or privileged clock adjustment.

## Added

- `mundilfari`, `mundilfari-core`, `mundilfari-engine`, and
  `mundilfari-platform` published crate boundaries.
- Repository-only Rust `1.97.1` task-runner boundary.
- Rust `1.90.0` MSRV through pinned stable `1.97.1` compatibility policy.
- MIT OR Apache-2.0 licensing.
- Detailed implementation and release plans through an exact `1.0.0` release
  candidate.
- Initial protocol registry spanning Internet/NTP/NTS, PTP, Navheim-derived
  GNSS observations, PPS, radio, industrial, automotive, wireless, media,
  space, formats, and trusted timestamp evidence.
- Strict rule that Navheim determines GNSS time while Mundilfari decides how
  validated GNSS evidence participates in a larger clock system.
- Planned optional `mundilfari-navheim` companion crate, blocked until Navheim
  publishes its independently reviewed stable timing API.
- Dependency-last roadmap ordering: all Navheim-independent protocols,
  engines, servos, and applications precede the final Navheim integration and
  CGGTTS feature phase.
- `no_std`, dependency layering, 500-line, unsafe, standards, supply-chain,
  threat-model, and secret-handling policies.
- GitHub CI, Dependabot, CODEOWNERS, funding, issue, pull request, and manual
  release metadata.
- Release script, exact-commit pentest handoff, latest tool checks, package
  checks, SBOM controls, and local policy gates.

## Security Notes

- The published workspace has no third-party Cargo dependencies.
- All first-party Rust crates forbid unsafe code.
- No parser consumes untrusted protocol input in this release.
- No code can access or modify an OS or hardware clock in this release.
- CodeQL uses GitHub default setup; no advanced workflow is added.

## Verification

```bash
scripts/checks.sh
scripts/check_latest_tools.sh
scripts/release_0_1_gate.sh
```

The release is not tag-ready until an exact-commit pentest passes and
`scripts/validate-release-readiness.sh v0.1.0` accepts the permanent report.
