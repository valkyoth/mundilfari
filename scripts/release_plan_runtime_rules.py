"""Additional release-plan guards for runtime hard-bound assessment."""

from __future__ import annotations


def extend_runtime_review_rules(
    coverage: dict[str, tuple[str, ...]],
    forbidden: dict[str, tuple[str, ...]],
) -> None:
    """Add runtime-assessment coverage without bloating the main validator."""
    additions = {
        "v0.39.1": ("historical evidence only after restore",),
        "v0.60.1": (
            "Runtime Bound-Condition Assessment And Policy Admission",
            "ConditionAssessment",
            "Supported",
            "Contradicted",
            "Indeterminate",
            "Expired",
            "Withdrawn",
            "PolicyAcceptedHardBound<T>",
            "provider callbacks return structured evidence, not `is_true`",
            "downstream invalidation graph",
            "but no clock",
        ),
        "v0.61.0": ("PolicyAcceptedHardBound", "explicit diagnostic results"),
        "v0.61.1": ("condition-assessment/accepted-bound identity",),
        "v0.133.0": (
            "PolicyAcceptedHardBound",
            "no servo or clock-publication authority",
        ),
        "v0.134.0": (
            "PolicyAcceptedHardBound",
            "assessment loss/expiry/withdrawal",
        ),
        "v0.134.1": (
            "accepted-bound assessment generation",
            "assessment expiry/stale token",
        ),
        "v0.134.3": ("PolicyAcceptedHardBound", "assessment loss invalidates"),
        "v0.135.0": (
            "PolicyAcceptedHardBound",
            "accepted-condition expiry/rejection",
        ),
        "v0.136.0": ("reassessed during holdover", "stale accepted token"),
        "v0.137.0": (
            "ConditionAssessment",
            "PolicyAcceptedHardBound",
            "conditional-not-synchronized refusal",
        ),
        "v0.137.1": (
            "PolicyAcceptedHardBound",
            "Conditional estimates publish only",
            "synchronized-to-",
        ),
        "v0.137.3": ("condition-assessment loss",),
        "v0.138.0": (
            "separate explicit result paths",
            "no `is_trusted` boolean",
            "conditional diagnostic preservation",
        ),
        "v0.140.1": ("historical evidence", "accepted-bound tokens"),
        "v0.142.0": ("PolicyAcceptedHardBound", "assessment-loss revocation"),
        "v0.148.0": (
            "ConditionAssessment",
            "PolicyAcceptedHardBound",
            "strict-versus-diagnostic facade behavior",
        ),
        "v0.163.0": (
            "runtime condition",
            "stale accepted-bound tokens",
            "strict-facade synchronized-label refusal",
        ),
        "v0.166.0": ("runtime assessment statuses", "no trusted boolean"),
    }
    exclusions = {
        "v0.7.3": ("PolicyAcceptedHardBound", "ConditionAssessment"),
        "v0.60.0": ("PolicyAcceptedHardBound", "ConditionAssessment"),
    }
    for version, phrases in additions.items():
        coverage[version] = coverage.get(version, ()) + phrases
    for version, phrases in exclusions.items():
        forbidden[version] = forbidden.get(version, ()) + phrases
