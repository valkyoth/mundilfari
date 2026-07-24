<p align="center">
  <b>Security-first, no_std-first time protocols for Rust.</b><br>
  Exact time semantics, bounded protocol engines, and independently pentested releases on the path to production.
</p>

<div align="center">
  <a href="https://crates.io/crates/mundilfari-engine">Crates.io</a>
  |
  <a href="https://docs.rs/mundilfari-engine">Docs.rs</a>
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

# mundilfari-engine

`mundilfari-engine` is the reusable `no_std` home for source consensus, clock
servos, holdover, trusted virtual clocks, and discipline policy. It depends
inward on `mundilfari-core` and never owns protocol packet formats or operating
system calls.

Version `0.1.0` establishes only the audited crate boundary.

Licensed under `MIT OR Apache-2.0`.
