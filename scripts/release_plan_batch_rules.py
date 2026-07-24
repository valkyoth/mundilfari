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
            "CompleteMemberStatus<T>",
            "`Unprocessed` variant",
            "`AbortMemberDiagnostic`",
            "globally aborts the transaction",
            "`Unprocessed`",
            "exists only inside",
            "construct or convert",
            "original policy-defined `n`",
            "eligible interval contributor",
            "contribute no interval and no vote",
            "atomic installation of",
            "fixed-size `PriorAuthorityObservation`",
            "PriorAuthorityDisposition::{Retained, Invalidated, Absent}",
            "at the refresh linearization point",
            "prior-authority identity/generation",
            "exact-domain",
            "unchanged prior `valid_until`",
            "invalidation generation and typed reason",
            "not caller receipt",
            "older batch unchanged",
            "retiring the prior batch",
        ),
        "v0.61.0": (
            "consumes `CompleteBatchVerification`",
            "eligible interval contributors",
            "has no",
            "`AbortMemberDiagnostic`/`Unprocessed` input path",
        ),
        "v0.133.0": (
            "caller-filtered result iterators",
            "accepted-bound members contribute intervals/votes",
            "refused before orchestration",
        ),
        "v0.137.1": (
            "retires the prior batch/snapshot",
            "`PriorAuthorityObservation`",
            "no caller may use the report",
        ),
        "v0.138.0": (
            "refresh APIs return `PriorAuthorityObservation`",
            "delayed blocking",
        ),
        "v0.139.0": (
            "authoritative prefix escapes",
            "`PriorAuthorityObservation` is historical",
            "authority through receipt",
        ),
        "v0.140.0": (
            "disjoint result buffers",
            "fixed-size",
            "cross-status construction",
        ),
        "v0.140.1": (
            "`CompleteMemberStatus`",
            "`AbortMemberDiagnostic`",
            "`Unprocessed` has no complete-witness encoding",
            "through-receipt authority claim",
        ),
        "v0.148.0": (
            "`BatchVerificationOutcome` complete/abort",
            "original-`n` membership accounting",
            "disjoint complete-member versus abort-diagnostic",
            "fixed-size interval-valued linearization observation",
        ),
        "v0.160.0": (
            "shared-node-once charging",
            "prior-state mutation",
            "separately bounded",
            "prior-observation variant",
        ),
        "v0.163.0": (
            "batch/individual proof/token",
            "no-token global abort",
            "complete-membership witness enforcement",
            "compile-fail complete/abort status mixing",
            "original-`n`/no-vote enforcement",
            "prior retained/invalidated/absent outcomes",
            "immediate post-linearization expiry/invalidation",
            "prior identity/generation",
        ),
        "v0.166.0": (
            "`BatchVerificationOutcome`",
            "`AbortMemberDiagnostic`",
            "cannot reach a complete witness/quorum",
            "fixed-size `PriorAuthorityObservation`",
            "`PriorAuthorityDisposition::{Retained, Invalidated, Absent}`",
            "not authority",
        ),
    }
    for version, phrases in additions.items():
        coverage[version] = coverage.get(version, ()) + phrases
