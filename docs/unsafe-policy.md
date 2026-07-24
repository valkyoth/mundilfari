# Mundilfari Unsafe Policy

Current first-party crates use:

```rust
#![forbid(unsafe_code)]
```

No unsafe Rust is admitted in `v0.1.0`.

Future unsafe code is permitted only in a dedicated, narrowly scoped platform
or acceleration module for:

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

The workspace always denies `unsafe_op_in_unsafe_fn`.
