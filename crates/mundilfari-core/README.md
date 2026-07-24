<p align="center">
  <b>Security-first, no_std-first time protocols for Rust.</b><br>
  Exact time semantics, bounded protocol engines, and independently pentested releases on the path to production.
</p>

<div align="center">
  <a href="https://crates.io/crates/mundilfari-core">Crates.io</a>
  |
  <a href="https://docs.rs/mundilfari-core">Docs.rs</a>
  |
  <a href="https://github.com/valkyoth/mundilfari/blob/main/docs/RELEASE_PLAN.md">Release Plan</a>
  |
  <a href="https://github.com/valkyoth/mundilfari/blob/main/SECURITY.md">Security</a>
</div>

<br>

<p align="center">
  <a href="https://github.com/valkyoth/mundilfari">
    <img src="https://raw.githubusercontent.com/valkyoth/mundilfari/main/.github/images/mundilfari.webp" alt="Mundilfari Rust time protocol framework">
  </a>
</p>

# mundilfari-core

`mundilfari-core` is the dependency-free, allocation-free foundation for
Mundilfari. It will own checked time arithmetic, epochs, eras, scales, leap
seconds, uncertainty, provenance, bounded wire utilities, and platform-neutral
transport and clock traits.

Version `0.1.0` establishes only the audited crate boundary. Time semantics are
introduced in later release-plan milestones and are not claimed as available
yet.

Licensed under `MIT OR Apache-2.0`.
