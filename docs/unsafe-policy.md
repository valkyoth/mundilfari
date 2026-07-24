# Mundilfari Unsafe Policy

Current first-party crates use:

```rust
#![forbid(unsafe_code)]
```

No unsafe Rust is admitted in `v0.1.0`.

Future unsafe code is permitted only in dedicated, narrowly scoped
`mundilfari-platform-*-sys` or acceleration crates for:

- system-call and FFI boundaries;
- ancillary control-message traversal;
- CPU intrinsics and reviewed SIMD;
- volatile secret clearing;
- application-supplied memory-mapped hardware.

Unsafe is forbidden for ordinary packet parsing, date arithmetic, premature
bounds-check removal, casting wire bytes to structs, and protocol policy.

Every unsafe block requires:

- a `SAFETY:` explanation;
- a documented invariant and caller obligation;
- unit and platform tests;
- Miri or sanitizer evidence where applicable;
- registration in this document;
- changed-scope security review and pentest before release.

The safe `mundilfari-platform` crate validates sys-crate outputs and continues
to forbid unsafe. Core, engine, facade, protocol, crypto-state, and IPC-schema
crates also continue to forbid unsafe. Sys crates do not inherit the workspace
`unsafe_code = "forbid"` lint; they deny `unsafe_op_in_unsafe_fn`, document
their exception, and are rejected unless every unsafe block appears in the
machine-readable unsafe inventory.

Miri covers pure wrapper logic and mock memory where applicable. Sanitizers,
ABI/layout assertions, fault injection, and hardware tests cover real FFI
boundaries. MMIO adapters additionally document volatile access, alignment,
endianness, ownership, memory ordering, and reset behavior. None of this is
described as proof of the kernel, driver, DMA engine, or device.
