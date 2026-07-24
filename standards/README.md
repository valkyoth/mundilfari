# External Standards Source Registry

This directory records the non-RFC specifications needed by Mundilfari. It
deliberately separates public review metadata from document bytes.

It also holds the ignored complete PDF rendering of RFC 1119 because that
RFC's tracked text artifact is only a catalog notice, not the NTPv2 body.

`SOURCES.json` is committed. It identifies the publisher, exact standard or
family, official source, access state, redistribution decision, implementation
milestone, and acquisition method. `PUBLIC_SHA256SUMS` pins public artifacts
that the project downloads for local review but does not redistribute.
Family entries are discovery placeholders only. They must be split into exact
revision, amendment, corrigendum, interpretation, profile, and registry
records before their implementation milestone.

All acquired non-RFC artifacts live below `standards/private/`. That directory
is ignored in full, regardless of whether a particular document is free to
download. This fail-closed rule prevents an unclear or later-changed license
from accidentally publishing a standards corpus to GitHub or crates.io.

## Commands

- `scripts/verify-standard-sources.py` validates the committed registry and
  confirms the private directory cannot be tracked.
- `scripts/fetch-standard-sources.py` downloads only entries explicitly marked
  `public-download`, only from their pinned HTTPS artifact URL, verifies their
  public checksum, and writes them read-only below `standards/private/`.
- `scripts/lock-standard-sources.py --accept-local` explicitly checksum-locks
  legitimately acquired manual documents in ignored
  `standards/private/LOCK.json`.
- `scripts/verify-standard-sources.py --local` additionally checks downloaded
  bytes and reports the manual acquisitions still required.

The fetch command never downloads `manual` or `metadata-only` entries, accepts
no credentials, and cannot make builds network-dependent. Licensed documents
must be obtained through the publisher or the user's legitimate institutional
access and saved under the registry's `local_filename`.

## Review Gate

Possessing a document is not an implementation review. Before an assigned
release milestone may begin protocol implementation, it must:

1. possess the exact legitimately obtained revision locally;
2. inspect it and explicitly pin its local SHA-256 with
   `scripts/lock-standard-sources.py --accept-local`;
3. review normative clauses, amendments, corrigenda, and official errata;
4. recursively classify every normative reference and record included and
   excluded behavior in the milestone requirement ledger;
5. derive tests independently or use vectors whose provenance permits it.

Entries marked `identifier-review`, `revision-review`, partially documented,
or otherwise unresolved block implementation until the exact revision,
transitive normative dependencies, and official access route are resolved.
Mundilfari does not infer normative behavior from summaries, vendor code, or
random websites.

GNSS navigation and receiver standards remain Navheim's responsibility. This
registry contains only the Navheim interface contract needed by the future
adapter, never a duplicate GNSS standards corpus.
