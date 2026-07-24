#![no_std]
#![forbid(unsafe_code)]
#![doc = include_str!("../README.md")]

/// Common time domains and protocol-neutral traits.
pub use mundilfari_core as core;
/// Source consensus, servo, and holdover foundations.
pub use mundilfari_engine as engine;
/// Platform, transport, timestamp, and clock adapter foundations.
pub use mundilfari_platform as platform;

/// Reports whether every initial published crate boundary is connected.
#[must_use]
pub const fn repository_foundation_ready() -> bool {
    let _ = core::capability();
    let _ = engine::capability();
    let _ = platform::capability();
    true
}

#[cfg(test)]
mod tests {
    #[test]
    fn all_foundation_crates_are_connected() {
        assert!(super::repository_foundation_ready());
    }
}
