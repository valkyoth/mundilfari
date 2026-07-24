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
            "SupportBasis",
            "ConfiguredAssumption",
            "visible configured assumption",
            "VerifiedBoundDerivation<T>",
            "root derivation binds",
            "rounding direction and policy",
            "one snapshot-consistent transaction",
            "assessor-registry generation",
            "engine linearization point",
            "provider callbacks return structured evidence, not `is_true`",
            "adversarial interval narrowing",
            "no mixed or partial assessment/token",
            "downstream invalidation graph",
            "but no clock",
        ),
        "v0.61.0": (
            "PolicyAcceptedHardBound",
            "derivation identity, condition",
            "through explicit diagnostic",
        ),
        "v0.61.1": (
            "verified-bound-derivation",
            "support-basis report",
        ),
        "v0.133.0": (
            "PolicyAcceptedHardBound",
            "verified-derivation and assessment",
            "unmodified per-atom `SupportBasis`",
            "no servo or clock-publication authority",
        ),
        "v0.134.0": (
            "PolicyAcceptedHardBound",
            "verified-derivation or assessment",
        ),
        "v0.134.1": (
            "accepted-bound verified-derivation/assessment generations",
            "assessment expiry/stale token",
        ),
        "v0.134.3": (
            "PolicyAcceptedHardBound",
            "verified-derivation generations",
            "derivation or assessment",
        ),
        "v0.135.0": (
            "PolicyAcceptedHardBound",
            "derivation or assessment loss",
            "accepted-condition expiry/rejection",
        ),
        "v0.136.0": (
            "reassessed during holdover",
            "invalidated observation/model derivations",
            "stale accepted token",
        ),
        "v0.137.0": (
            "ConditionAssessment",
            "PolicyAcceptedHardBound",
            "verified-derivation identity",
            "every strict `TrustedClock::now()` read",
            "At or after the exact",
            "suspend-inclusive monotonic domain",
            "timer starvation",
            "conditional-not-synchronized refusal",
        ),
        "v0.137.1": (
            "PolicyAcceptedHardBound",
            "verified derivation",
            "every concurrent strict read",
            "cached pre-expiry label",
            "idle-expiry",
            "estimates publish only with explicit",
            "synchronized-to-",
        ),
        "v0.137.3": ("condition-assessment loss",),
        "v0.138.0": (
            "separate explicit result paths",
            "no `is_trusted` boolean",
            "exact per-atom `SupportBasis`",
            "verified-derivation status",
            "conditional diagnostic preservation",
        ),
        "v0.140.1": (
            "historical evidence",
            "accepted-bound tokens",
            "cannot construct verified",
        ),
        "v0.142.0": (
            "PolicyAcceptedHardBound",
            "verified-derivation and condition-assessment",
            "derivation/assessment-loss",
        ),
        "v0.148.0": (
            "ConditionAssessment",
            "PolicyAcceptedHardBound",
            "VerifiedBoundDerivation",
            "typed per-atom `SupportBasis`",
            "read-side exact-domain",
            "strict-versus-diagnostic facade behavior",
        ),
        "v0.163.0": (
            "runtime condition",
            "stale accepted-bound tokens",
            "narrowed/spliced/substituted derivations",
            "configured-assumption basis laundering",
            "idle/read-side expiry",
            "strict-facade synchronized-label",
        ),
        "v0.166.0": (
            "verified root/derived claim proofs",
            "typed support basis",
            "deadline/domain enforcement",
            "no trusted boolean",
        ),
    }
    exclusions = {
        "v0.7.3": (
            "PolicyAcceptedHardBound",
            "ConditionAssessment",
            "VerifiedBoundDerivation",
        ),
        "v0.60.0": (
            "PolicyAcceptedHardBound",
            "ConditionAssessment",
            "VerifiedBoundDerivation",
            "SupportBasis",
        ),
    }
    for version, phrases in additions.items():
        coverage[version] = coverage.get(version, ()) + phrases
    for version, phrases in exclusions.items():
        forbidden[version] = forbidden.get(version, ()) + phrases
