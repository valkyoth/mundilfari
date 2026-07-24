"""Additional release-plan guards for runtime hard-bound assessment."""

from __future__ import annotations


def extend_runtime_review_rules(
    coverage: dict[str, tuple[str, ...]],
    forbidden: dict[str, tuple[str, ...]],
) -> None:
    """Add runtime-assessment coverage without bloating the main validator."""
    additions = {
        "v0.7.1": (
            "UnverifiedBoundDerivation<T>",
            "ClaimOriginId",
            "recipe-drop/detachment refusal",
        ),
        "v0.7.2": (
            "automatically composes",
            "recipe digests",
            "byte/storage",
            "cycle-detection",
            "digest-only claim",
        ),
        "v0.7.3": (
            "UnverifiedBoundDerivationRecord",
            "non-authoritative core `UnverifiedBoundDerivation<T>`",
            "malformed/truncated/spliced derivation records",
        ),
        "v0.8.0": ("selected era", "recipe preservation"),
        "v0.9.0": ("UnverifiedBoundDerivation", "recipe quantum"),
        "v0.11.0": ("UnverifiedBoundDerivation", "claim-recipe loss"),
        "v0.11.1": ("UnverifiedBoundDerivation", "recipe tests replace EOP"),
        "v0.11.2": ("UnverifiedBoundDerivation", "complete recipe"),
        "v0.11.3": ("UnverifiedBoundDerivation", "recipe substitution"),
        "v0.11.4": ("UnverifiedBoundDerivation", "recipe substitution"),
        "v0.12.0": ("UnverifiedBoundDerivation", "recipe table/EOP"),
        "v0.13.0": (
            "UnverifiedBoundDerivation",
            "policy/profile/branch/model/recipe",
        ),
        "v0.14.0": (
            "UnverifiedBoundDerivation",
            "statistical-only recipe refusal",
        ),
        "v0.15.0": (
            "UnverifiedBoundDerivation",
            "transitive-recipe preservation",
        ),
        "v0.16.0": (
            "MonotonicReadInterval",
            "resolution/quantization",
            "operation-supplied completion margin",
            "upper-edge deadline comparisons",
        ),
        "v0.22.1": (
            "UnverifiedBoundDerivationRecord",
            "no tag or decode",
        ),
        "v0.39.1": (
            "historical evidence only after restore",
            "UnverifiedBoundDerivationRecord",
            "has no direct `Deserialize`",
            "cross-engine copy",
        ),
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
            "EvidenceOrigin",
            "IntegrityBasis",
            "AuthorityBasis",
            "complete bounded transitive leaf-basis",
            "configured-assumption origin",
            "VerifiedBoundDerivation<T>",
            "`UnverifiedBoundDerivation<T>`",
            "root derivation binds",
            "rounding direction",
            "one snapshot-consistent transaction",
            "assessor-registry generation",
            "engine linearization point",
            "`MonotonicReadInterval`",
            "`latest >= valid_until`",
            "verification work crossing expiry",
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
            "`latest >= deadline`",
            "read-to-return completion margin",
            "suspend-inclusive monotonic domain",
            "timer starvation",
            "conditional-not-synchronized refusal",
        ),
        "v0.137.1": (
            "PolicyAcceptedHardBound",
            "verified derivation",
            "every concurrent strict read",
            "conservative `latest` edge",
            "read-to-return interval",
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
            "UnverifiedBoundDerivationRecord",
            "no direct deserialize path",
            "cross-engine copy",
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
            "UnverifiedBoundDerivationRecord",
            "structured per-atom `SupportBasis`",
            "conservative monotonic",
            "strict-versus-diagnostic facade behavior",
        ),
        "v0.163.0": (
            "runtime condition",
            "stale accepted-bound tokens",
            "missing/truncated/over-budget early recipes",
            "narrowed/spliced/substituted",
            "serialized-record replay/rollback/cross-engine restore",
            "transitive-basis laundering",
            "monotonic upper-edge expiry",
            "strict-facade synchronized-label",
        ),
        "v0.166.0": (
            "early non-authoritative derivation recipes",
            "unverified record",
            "verified root/derived claim proofs",
            "structured independent origin",
            "upper-edge deadline/domain enforcement",
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
