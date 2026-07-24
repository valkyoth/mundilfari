# Mundilfari Modularity Policy

Mundilfari must not become a monolithic source tree.

Rules:

- `mundilfari` is a facade, not an implementation home.
- Shared time domains live in `mundilfari-core`.
- Consensus, servo, and holdover live in `mundilfari-engine`.
- OS, transport, timestamp, PHC, PPS, and FFI live in
  `mundilfari-platform`.
- Every independently useful protocol or tightly coupled family receives a
  focused crate.
- Wire parsing, validation, I/O, source policy, and clock discipline remain
  separate modules and dependency layers.
- Core and protocol wire crates do not depend on platform crates.
- Stable crates do not expose experimental-draft types.
- Non-generated Rust files may not exceed 500 lines.
- Review for a split begins near 300 lines.
- Feature flags do not silently enable networking, insecure legacy behavior,
  a runtime, privileged operations, or system-clock modification.

The local gate is:

```bash
scripts/validate-modularity-policy.sh check
```
