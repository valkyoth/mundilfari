#![no_std]
#![forbid(unsafe_code)]
#![doc = include_str!("../README.md")]

/// The engine capability made available by this release.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
#[non_exhaustive]
pub enum EngineCapability {
    /// The engine boundary exists and is connected to `mundilfari-core`.
    RepositoryFoundation,
}

/// Returns the engine capability currently implemented by this crate.
#[must_use]
pub const fn capability() -> EngineCapability {
    let _ = mundilfari_core::capability();
    EngineCapability::RepositoryFoundation
}

#[cfg(test)]
mod tests {
    use super::{EngineCapability, capability};

    #[test]
    fn reports_repository_foundation() {
        assert_eq!(capability(), EngineCapability::RepositoryFoundation);
    }
}
