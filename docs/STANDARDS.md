# Standards Provenance Policy

Mundilfari implements protocols only from authoritative, legitimately obtained
specifications.

The machine-readable standards registry planned after `v0.1.0` records:

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

## Licensed Documents

IEEE, ISO, IEC, ITU-T, SMPTE, AUTOSAR, SAE, and similar documents may
restrict redistribution. Do not commit unauthorized copies.

NMEA, RTCM, GNSS interface specifications, receiver protocols, OSNMA/QZNMA,
and other GNSS interpretation standards are tracked and implemented by
Navheim. Mundilfari records only the exact admitted Navheim API/version and
the standards needed to verify its adapter behavior; it does not reproduce
Navheim's normative GNSS implementation.

Private licensed documents belong under `standards/private/`, which is ignored.
The public repository may retain identifiers, hashes, independently written
implementation notes, clause references, and legally redistributable vectors.

Normative behavior must not be reconstructed from random websites or copied
from another implementation.

## Drafts

Active drafts are revision-pinned behind experimental features. A new draft
revision is reviewed as a protocol change. Final RFC migration keeps the old
decoder under an explicit compatibility feature where needed and never
silently reinterprets stored messages or cryptographic transcripts.
