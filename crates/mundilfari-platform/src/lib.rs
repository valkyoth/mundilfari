#![no_std]
#![forbid(unsafe_code)]
#![doc = include_str!("../README.md")]

/// The platform capability made available by this release.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
#[non_exhaustive]
pub enum PlatformCapability {
    /// The platform boundary exists and contains no operating-system code yet.
    RepositoryFoundation,
}

/// Returns the platform capability currently implemented by this crate.
#[must_use]
pub const fn capability() -> PlatformCapability {
    let _ = mundilfari_core::capability();
    PlatformCapability::RepositoryFoundation
}

#[cfg(test)]
mod tests {
    use super::{PlatformCapability, capability};

    #[test]
    fn reports_repository_foundation() {
        assert_eq!(capability(), PlatformCapability::RepositoryFoundation);
    }
}
