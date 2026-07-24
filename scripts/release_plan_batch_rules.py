"""Release-plan guards for multi-root verification and batch refresh."""

from __future__ import annotations


def extend_batch_review_rules(
    coverage: dict[str, tuple[str, ...]],
) -> None:
    """Require batch safety contracts at their owner and consumer versions."""
    additions = {
        "v0.60.1": (
            "owned multi-root set",
            "individual proof/token identity equivalence",
            "BatchVerificationOutcome<T>",
            "BatchMemberId",
            "never caller order",
            "complete admitted membership",
            "shared derivation node is verified once",
            "Structural failure propagates",
            "root-specific evidence",
            "CompleteBatchVerification<T>",
            "globally aborts the transaction",
            "`Unprocessed`",
            "original policy-defined `n`",
            "eligible interval contributor",
            "contribute no interval and no vote",
            "atomic installation of",
            "PriorAuthorityDisposition::{Retained, Invalidated, Absent}",
            "older batch unchanged",
            "retiring the prior batch",
        ),
        "v0.61.0": (
            "consumes `CompleteBatchVerification`",
            "eligible interval contributors",
        ),
        "v0.133.0": (
            "caller-filtered result iterators",
            "accepted-bound members contribute intervals/votes",
        ),
        "v0.137.1": (
            "retires the prior batch/snapshot",
            "`PriorAuthorityDisposition`",
        ),
        "v0.139.0": ("authoritative prefix escapes", "prior-authority"),
        "v0.140.0": ("membership/result slots", "prior-authority disposition"),
        "v0.148.0": (
            "`BatchVerificationOutcome` complete/abort",
            "original-`n` membership accounting",
        ),
        "v0.160.0": ("shared-node-once charging", "prior-state mutation"),
        "v0.163.0": (
            "proof/token identity equivalence",
            "no-token global abort",
            "complete-membership witness enforcement",
            "original-`n`/no-vote enforcement",
            "prior retained/invalidated/absent outcomes",
        ),
        "v0.166.0": (
            "`BatchVerificationOutcome`",
            "`PriorAuthorityDisposition::{Retained, Invalidated, Absent}`",
        ),
    }
    for version, phrases in additions.items():
        coverage[version] = coverage.get(version, ()) + phrases
