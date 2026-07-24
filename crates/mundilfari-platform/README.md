<p align="center">
  <b>Security-first, no_std-first time protocols for Rust.</b><br>
  Exact time semantics, bounded protocol engines, and independently pentested releases on the path to production.
</p>

<div align="center">
  <a href="https://crates.io/crates/mundilfari-platform">Crates.io</a>
  |
  <a href="https://docs.rs/mundilfari-platform">Docs.rs</a>
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

# mundilfari-platform

`mundilfari-platform` is the isolated home for standard sockets, native clock
access, software and hardware timestamps, PHC and PPS devices, raw transports,
and bounded system-clock adjustment adapters.

The crate stays `no_std` by default. OS bindings and privileged capabilities
are opt-in and must never leak into protocol codecs. Version `0.1.0` contains
no system calls or unsafe code.

Licensed under `MIT OR Apache-2.0`.
