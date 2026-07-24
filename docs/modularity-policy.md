# Mundilfari Modularity Policy

Mundilfari must not become a monolithic source tree.

Rules:

- `mundilfari` is a facade, not an implementation home.
- Shared time domains live in `mundilfari-core`.
- Consensus, servo, and holdover live in `mundilfari-engine`.
- Safe OS, transport, timestamp, PHC, PPS, and device wrappers live in
  `mundilfari-platform`.
- `mundilfari-platform` remains safe; necessary unsafe/FFI lives only in small
  OS-family or device-specific `mundilfari-platform-*-sys` crates.
- Clock discipline uses a separate authorization boundary and a minimal
  protocol-free helper process.
- GNSS interpretation lives in Navheim, never in a Mundilfari core, protocol,
  platform, engine, or facade crate.
- Only the optional `mundilfari-navheim` companion may depend on Navheim.
- Generic PPS capture remains platform-owned; GNSS pulse semantics arrive from
  Navheim through the companion.
- Every independently useful protocol or tightly coupled family receives a
  focused crate.
- Wire parsing, validation, I/O, source policy, and clock discipline remain
  separate modules and dependency layers.
- Core and protocol wire crates do not depend on platform crates.
- Navheim never depends on Mundilfari, preventing an integration cycle.
- Stable crates do not expose experimental-draft types.
- Non-generated Rust files may not exceed 500 lines.
- Review for a split begins near 300 lines.
- Feature flags do not silently enable networking, insecure legacy behavior,
  a runtime, privileged operations, or system-clock modification.
- Capability APIs distinguish code compiled, resource available, caller
  authorized, and component healthy; a Cargo feature proves only the first.

The local gate is:

```bash
scripts/validate-modularity-policy.sh check
```
