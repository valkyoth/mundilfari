# Standards Provenance Policy

Mundilfari implements protocols only from authoritative, legitimately obtained
specifications. Source acquisition is auditable and is never part of a Cargo
build, test, package, or documentation command.

The repository has two source classes:

- [`rfc/`](../rfc/README.md) contains tracked, unmodified, checksum-locked RFC
  Editor text whose original notices and legal terms remain in force.
- [`standards/`](../standards/README.md) contains public metadata and checksum
  pins, while all acquired non-RFC document bytes stay below the ignored
  `standards/private/` vault.

The initial source baseline exists at `v0.1.0`. The complete clause, errata,
license, conformance, and implementation-disposition registry remains the
explicit `v0.2.0` deliverable. That registry records:

- publisher, identifier, title, revision, and publication date;
- stable, informational, experimental, obsolete, historic, vendor-published,
  licensed, partial, or unavailable status;
- normative/informative classification;
- official source URL;
- local SHA-256 where a document is lawfully held;
- license and redistribution restrictions;
- incorporated updates and verified errata;
- implemented/excluded clause map;
- official conformance suite or vector source;
- last review date.

`scripts/verify-rfcs.sh`, `scripts/test-rfc-sources.py`, and
`scripts/verify-standard-sources.py` run offline in the common gate. Networked
refreshes are explicit maintainer operations:

- `scripts/fetch-rfcs.sh` accepts only RFC Editor URLs in the reviewed
  allowlist; adding a new checksum trust pin requires `--accept-new`.
- `scripts/fetch-standard-sources.py` accepts only registry entries marked
  `public-download`, verifies their committed SHA-256, and writes only to the
  ignored local vault.

Source admission is not an implementation or conformance claim. Every source
has a roadmap assignment, and its milestone must still review normative
clauses, updates, errata, security consequences, and vector provenance.

## Licensed Documents

IEEE, ISO, IEC, ITU-T, SMPTE, AUTOSAR, SAE, and similar documents may
restrict redistribution. Do not commit unauthorized copies.

NMEA, RTCM, GNSS interface specifications, receiver protocols, OSNMA/QZNMA,
and other GNSS interpretation standards are tracked and implemented by
Navheim. Mundilfari records only the exact admitted Navheim API/version and
the standards needed to verify its adapter behavior; it does not reproduce
Navheim's normative GNSS implementation.

Every non-RFC document, including freely downloadable drafts, belongs under
`standards/private/`, which is ignored. This fail-closed rule prevents
accidental publication when redistribution terms are unclear or later change.
The public repository retains identifiers, official URLs, hashes,
independently written implementation notes, clause references, and legally
redistributable vectors.

Normative behavior must not be reconstructed from random websites or copied
from another implementation.

Entries marked `identifier-review`, `revision-review`, or requiring manual
acquisition block their implementation milestone until the exact legitimate
source is present and reviewed. Missing licensed documents are a planned
blocker, not permission to guess.

Every production implementation file is also covered by the offline
`compliance/IMPLEMENTATION_EVIDENCE.json` gate. Protocol/format/integration
entries must identify the exact registered sources, reviewed hashes, clauses,
errata dispositions, governing requirements, and concrete linked tests.
Adding code without that evidence fails the common repository check.

## Drafts

Active drafts are revision-pinned behind experimental features. A new draft
revision is reviewed as a protocol change. Final RFC migration keeps the old
decoder under an explicit compatibility feature where needed and never
silently reinterprets stored messages or cryptographic transcripts.

The 2026-07-24 local baseline pins:

- `draft-ietf-ntp-ntpv5-09`;
- `draft-ietf-ntp-over-ptp-08`;
- `draft-ietf-ntp-nts-for-ptp-03`;
- `draft-ietf-ntp-roughtime-19`;
- `draft-ietf-ntp-nts-keyexchange-pool-01`; and
- XEP-0202 Entity Time.

The standards-closure milestone refreshes every draft and official publisher
record before `1.0.0`; a newer revision is never silently substituted for
these checksum-pinned bytes.
