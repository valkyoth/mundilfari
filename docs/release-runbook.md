# Release runbook

This runbook describes the mechanical path from an implementation-stop commit
to published Mundilfari crates. It does not replace the release-specific exit
criteria in [RELEASE_PLAN.md](RELEASE_PLAN.md).

## 1. Stop implementation

1. Complete the selected release-plan entry.
2. Update every affected crate version, `release-crates.toml`, the changelog,
   release notes, protocol registry, and standards baseline.
3. Generate the SBOM with `scripts/generate-sbom.sh --write`.
4. Run the matching `scripts/release_X_Y_gate.sh`.
5. Commit the complete candidate.

No source, test, documentation, dependency, or build change is allowed after
this point without invalidating the review.

## 2. Pentest the exact candidate

Give the independent reviewer the full commit identifier, threat model,
protocol inventory, dependency policy, release notes, and relevant fixtures.
The scope must cover the complete release delta and every exposed trust
boundary.

Do not create a permanent passing report before the review succeeds. After a
PASS, create `security/pentest/vX.Y.Z.md` from the template. Its
`Reviewed-Commit` is the implementation-stop commit.

## 3. Commit only the report

The report must be the sole path changed by the next commit. The readiness
validator enforces this two-commit history:

```text
implementation-stop commit  <- reviewed exact tree
└── report-only commit       <- candidate tag target
```

Run:

```sh
scripts/validate-release-readiness.sh vX.Y.Z
```

Any required correction restarts the implementation-stop and pentest process.

## 4. Tag and publish

Create the signed release tag on the report-only commit. In tag context, rerun
the validator and then use the publisher:

```sh
MUNDILFARI_RELEASE_PUBLISH_TAG=vX.Y.Z \
    scripts/validate-release-readiness.sh vX.Y.Z
scripts/release_crates.py --version X.Y.Z --require-tag
```

The publisher reruns the version gate, exact-commit readiness validation,
Cargo-deny, and Cargo-audit before publishing crates in dependency order. Wait
for each prerequisite crate to appear in the crates.io index before continuing.

## 5. Confirm the release

Verify checksums and documentation on crates.io, publish the matching GitHub
release notes, and confirm the GitHub release points at the signed tag. Retain
the SBOM, pentest report, and CI evidence.
