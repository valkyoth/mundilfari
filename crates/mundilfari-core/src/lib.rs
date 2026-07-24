#![no_std]
#![forbid(unsafe_code)]
#![doc = include_str!("../README.md")]

/// The foundation capability made available by this release.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
#[non_exhaustive]
pub enum CoreCapability {
    /// The crate boundary and its security policy are established.
    RepositoryFoundation,
}

/// Returns the foundation capability currently implemented by this crate.
#[must_use]
pub const fn capability() -> CoreCapability {
    CoreCapability::RepositoryFoundation
}

#[cfg(test)]
mod tests {
    use super::{CoreCapability, capability};

    #[test]
    fn reports_repository_foundation() {
        assert_eq!(capability(), CoreCapability::RepositoryFoundation);
    }
}
