# RFC Reference Corpus

This directory holds byte-exact, unmodified plain-text reference copies from
the [RFC Editor](https://www.rfc-editor.org/). Mundilfari uses them for
protocol review, requirement and errata analysis, security review, test-vector
provenance, and implementation verification.

The project claims no copyright in these RFCs. Their original notices,
authorship, status, disclaimers, and legal terms remain in force. They are not
licensed under Mundilfari's MIT OR Apache-2.0 software license. See the
[IETF Trust Legal Provisions](https://trustee.ietf.org/license-info/).

The copies must never be edited, annotated, reformatted, line-ending
normalized, or stripped of notices. Project analysis belongs in `docs/` and
the implementation's future requirement and errata ledgers.

## Review Model

`SOURCES` is both the acquisition allowlist and the first review gate. Every
entry binds an RFC Editor URL to:

- one narrowly named reason that Mundilfari needs the document; and
- the release milestone that must complete its semantic, errata, security,
  test-vector, and implementation-clause review.

`cross-cutting` entries govern every milestone. Source admission is not a
claim that a protocol is implemented or that its normative requirements have
already been dispositioned. Before work begins on the assigned milestone, its
release exit criteria require a clause-level review and all applicable RFC
Editor errata to be classified.

RFC 1119 is a special historical case: its RFC Editor text file is only a
catalog notice for a PostScript publication. The complete official artifact
must be acquired and reviewed locally before the NTPv2 compatibility milestone
can exit; the short tracked text must not be mistaken for the specification.

## Integrity And Offline Builds

- `SOURCES` permits only exact RFC Editor HTTPS text URLs.
- `SHA256SUMS` pins every tracked byte.
- `scripts/fetch-rfcs.sh` downloads only missing allowlisted files.
- `scripts/verify-rfcs.sh` rejects changed, missing, extra, or corrupt files.
- `scripts/test-rfc-sources.py` checks roles, milestones, URLs, corpus
  completeness, and authoritative documentation references.
- `scripts/lock-rfcs.sh` makes local copies read-only as a convenience guard.
- `.gitattributes` disables Git text normalization for RFC files.
- normal builds and CI never access the network.

Git does not preserve portable read-only permissions. The checksum manifest,
offline validation, CODEOWNERS review, and branch protection are authoritative.

## Updating The Corpus

1. Confirm the document is required by a planned Mundilfari behavior.
2. Add its exact RFC Editor URL, review role, and milestone to `SOURCES`.
3. Run `scripts/fetch-rfcs.sh --accept-new` in a clean review branch.
4. Inspect identity, notices, status, updates/obsoletes relationships, and
   relevant RFC Editor errata.
5. Commit the unmodified file, updated checksum, roadmap context, and review
   assignments together.
6. Run `scripts/checks.sh`.

The `--accept-new` operation deliberately requires an explicit flag because it
creates a new trust pin. Routine fetches require a pre-existing checksum.
Published RFCs are immutable; corrections are represented by errata or later
RFCs, never by modifying these files.

## Publication Exclusion

The workspace root is not a publishable package. Publishable crates use strict
package allowlists under `crates/`; this corpus must never enter a crates.io
archive.
