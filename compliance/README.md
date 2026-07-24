# Implementation Evidence Gate

Every production Rust source file in a published crate must have exactly one
entry in `IMPLEMENTATION_EVIDENCE.json`. The common repository gate rejects
unregistered source files, missing governing requirements, unlinked
requirements, nonexistent tests, and unreviewed protocol sources.

Each unit records:

- its implementation source, kind, and owning release milestone;
- the reviewed SHA-256 of that exact implementation source;
- every governing requirement with a precise document locator;
- one or more concrete tests linked from every requirement;
- for protocol/format/profile work, exact normative source identifiers,
  reviewed SHA-256 values, clauses, and errata dispositions.

RFC source identifiers use `rfc:<number>`. Other standards use
`external:<id>` from `standards/SOURCES.json`. Public source hashes must match
the committed checksum corpus. Restricted source hashes may be recorded
without publishing the document, but implementation remains blocked until the
legitimate local artifact and its clause/errata review exist.

This gate makes missing evidence mechanically impossible to overlook. It does
not assert that a test is sufficient or that a reviewer interpreted a
specification correctly. Milestone review, interoperability, conformance,
fuzzing, and exact-commit pentesting still decide that.

Any production-source edit changes its hash and fails the gate until the
requirements, exact documents, clause/errata dispositions, and linked tests
have been rechecked and the evidence hash is deliberately updated.

Run:

```bash
python3 scripts/check-implementation-evidence.py
python3 scripts/test-implementation-evidence.py
```
