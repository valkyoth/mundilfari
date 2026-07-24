#!/usr/bin/env python3
"""Validate required fields for every Mundilfari release-plan milestone."""

from __future__ import annotations

import re
import sys
from pathlib import Path


HEADING = re.compile(r"^(?:### |## )(v(?:0\.\d+\.\d+|1\.0\.0(?:-rc\.\d+)?)) -? ?(.*)$")
NAVHEIM_PHASE = "## Phase 12: Navheim Integration As Final Feature Work"
HARDENING_PHASE = "## Phase 13: Final Conformance Hardening And Production Admission"
NAVHEIM_VERSIONS = [f"v0.{minor}.0" for minor in range(149, 158)]
REVIEW_COVERAGE = {
    "v0.2.0": ("transitive normative", "WireComplete"),
    "v0.3.0": ("per-source implementation evidence",),
    "v0.7.0": ("mathematical floor",),
    "v0.12.0": (
        "TAI-to-UTC",
        "realization-evidence",
        "source-neutral metadata",
        "does not own evidence provenance",
    ),
    "v0.12.1": (
        "LeapModelCandidate",
        "single-thread transactional",
        "no protocol type",
        "cannot update `TrustedClock`",
    ),
    "v0.9.0": ("maximum limb width",),
    "v0.11.0": ("ConversionContext", "bipm-si-brochure-9-v4.01"),
    "v0.11.1": ("iers-conventions-2010-tn36", "non-definitive working updates"),
    "v0.11.2": ("iau-2000-resolutions", "iau-2006-resolution-b3"),
    "v0.15.1": ("silently dropped",),
    "v0.15.2": ("authentication-without-authority", "no-engine dependency"),
    "v0.16.0": ("MonotonicClockId", "IncludesSuspend"),
    "v0.17.0": ("evidence-provenance/lifecycle", "monotonic-domain"),
    "v0.21.0": ('unsafe_code = "forbid"', "drop exactly once"),
    "v0.22.1": (
        "Canonical Schema Kernel",
        "maximum nesting depth",
        "never reused with new meaning",
    ),
    "v0.23.1": ("MachineInstanceGeneration", "checkpoint/restore"),
    "v0.24.0": ("full `MonotonicClockId` descriptor",),
    "v0.24.1": (
        "per-key operation/byte limits",
        "production-approved",
        "SecretMemoryProtection",
    ),
    "v0.25.0": ("canonical-schema decode/encode", "before descent"),
    "v0.29.0": (
        "schema, state, and provider-contract foundations",
        "execution-lifecycle generation",
    ),
    "v0.30.0": ("compiled, available, authorized", "suspend behavior"),
    "v0.33.0": ("page locking", "core-dump exclusion"),
    "v0.38.2": ("volatile access",),
    "v0.39.0": ("AppliedAdjustment", "TOCTOU"),
    "v0.39.1": ("torn-write", "RollbackProtection", "mutable local state/key"),
    "v0.39.2": (
        "ClockDisciplineLease",
        "DisciplineOwnership",
        "competing/external change",
    ),
    "v0.39.3": (
        "HelperPolicyCeiling",
        "DisciplineAuditRecord",
        "audit-full",
    ),
    "v0.53.0": ("unknown critical",),
    "v0.52.1": (
        "TimeDataProvider",
        "caller-serialized verify → stage → compare → commit",
        "no concurrent-reader",
    ),
    "v0.52.2": (
        "candidate data is never used",
        "no built-in production TLS claim",
    ),
    "v0.56.0": ("no production-assurance claim until",),
    "v0.59.0": ("association-local filtering only",),
    "v0.60.0": ("maximum faulty diversity groups",),
    "v0.61.0": ("engine-owned", "without either reimplementing"),
    "v0.61.1": (
        "one authenticated malicious server",
        "AdmittedLeapCandidate",
        "local smear-versus-step presentation policy",
        "no model installation",
    ),
    "v0.62.0": ("facade/application composition",),
    "v0.72.0": (
        "v0.24.1",
        "TLS/Rustls/certificate admission",
        "SecretMemoryProtection",
    ),
    "v0.75.0": (
        "TemporalValidity",
        "entire trusted time interval",
        "CredentialVerifier",
        "scalar `UnixTime`",
    ),
    "v0.75.1": (
        "CredentialValidationContextId",
        "CredentialPolicyGeneration",
        "TemporalValidationEvidence",
        "CRL/OCSP",
        "InvalidateImmediately",
        "ordinary clock refinement",
    ),
    "v0.76.0": ("operation and byte limits", "entropy/nonce failure"),
    "v0.78.1": ("draft-ietf-ntp-nts-keyexchange-pool-01",),
    "v0.79.1": ("amplification",),
    "v0.80.0": ("partial overlap remains `Indeterminate`",),
    "v0.91.0": ("PTPv3",),
    "v0.101.0": ("no source fusion",),
    "v0.107.2": ("Stable PTP Authentication", "authenticated-but-delayable"),
    "v0.107.1": ("draft-ietf-ntp-over-ptp-08",),
    "v0.114.0": ("fixed-capacity Sans-I/O",),
    "v0.133.0": (
        "maximum faulty diversity groups",
        "assertion provenance",
        "ConsensusPolicyGeneration",
        "second intersection",
    ),
    "v0.134.4": ("ActuationFeedback", "anti-windup", "competing actuation"),
    "v0.137.1": (
        "AdmittedLeapCandidate",
        "atomically rechecks",
        "external scale-offset data",
        "single-thread transactional",
        "concurrent-reader",
        "memory-ordering",
        "maximum read-latency",
    ),
    "v0.137.2": ("target_has_atomic", "no silent emulation"),
    "v0.137.3": ("estimate_now()", "known-false future value"),
    "v0.138.0": ("safe-facade contract", "whole-facade fuzzing"),
    "v0.140.1": ("compatibility/freeze ledger",),
    "v0.142.0": (
        "OS peer credentials",
        "cumulative phase",
        "fault latching",
        "process/machine-instance",
        "v0.39.3",
    ),
    "v0.146.0": ("TamperEvident", "explicit gap/loss events", "v0.39.3"),
    "v0.147.0": (
        "opaque secret-provider/key references",
        "atomic activate",
        "v0.39.3",
    ),
    "v0.148.0": (
        "honest ahead recovery",
        "frozen helper-policy/discipline-audit semantics",
        "CredentialValidationContextId",
        "AdmittedLeapCandidate",
        "all-component concurrent publication",
    ),
    "v0.157.0": ("CGGTTS coverage",),
    "v0.160.0": ("whole-safe-facade fuzzing",),
    "v0.162.0": (
        "SecretMemoryProtection",
        "CredentialValidationContextId",
        "CredentialPolicyGeneration",
        "TemporalValidationEvidence",
        "scalar `UnixTime`",
    ),
    "v0.164.0": ("Android/iOS lifecycle evidence",),
    "v0.166.0": ("safe-facade panic contract",),
    "v0.165.0": ("no unclassified", "family/bundle"),
    "v0.167.0": ("signed exact-commit attestation",),
}

REVIEW_FORBIDDEN = {
    "v0.12.0": (
        "versioned leap table, provenance, activation, and hash",
        "leap announcement and conflict model",
    ),
    "v0.12.1": ("caller-admitted",),
    "v0.52.1": ("concurrent readers", "atomic activate pipeline"),
    "v0.61.1": ("the caller passes",),
    "v0.75.1": ("revocation configuration/evidence, trusted-time",),
}


def milestones(text: str) -> list[tuple[str, str]]:
    """Split release text into versioned milestone blocks."""
    found: list[tuple[str, int]] = []
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = HEADING.match(line)
        if match:
            found.append((match.group(1), index))
    result: list[tuple[str, str]] = []
    for offset, (version, start) in enumerate(found):
        end = found[offset + 1][1] if offset + 1 < len(found) else len(lines)
        result.append((version, "\n".join(lines[start:end])))
    return result


def validate(text: str) -> list[str]:
    """Return validation errors for one release-plan document."""
    errors: list[str] = []
    blocks = milestones(text)
    if not blocks:
        return ["no versioned milestones found"]
    seen: set[str] = set()
    for version, block in blocks:
        if version in seen:
            errors.append(f"duplicate milestone {version}")
        seen.add(version)
        for field in ("Status:", "Goal:", "Deliverables:", "Verification:", "Exit criteria:"):
            if field not in block:
                errors.append(f"{version} missing {field}")
        expected = (
            f"`{version} implementation stop reached. "
            f"Run {'final ' if version == 'v1.0.0' else ''}pentest for this exact commit.`"
        )
        if expected not in block:
            errors.append(f"{version} missing exact pentest exit sentence")
    return errors


def validate_review_coverage(text: str) -> list[str]:
    """Ensure architecture-review requirements stay in their owning versions."""
    errors: list[str] = []
    blocks = dict(milestones(text))
    for version, phrases in REVIEW_COVERAGE.items():
        block = blocks.get(version)
        if block is None:
            errors.append(f"review coverage milestone {version} is missing")
            continue
        for phrase in phrases:
            if phrase not in block:
                errors.append(f"{version} missing review requirement: {phrase}")
    for version, phrases in REVIEW_FORBIDDEN.items():
        block = blocks.get(version)
        if block is None:
            continue
        for phrase in phrases:
            if phrase in block:
                errors.append(f"{version} contains stale review requirement: {phrase}")
    return errors


def validate_version_order(text: str) -> list[str]:
    """Require strictly increasing v0 milestone and patch ordering."""
    errors: list[str] = []
    previous: tuple[int, int] | None = None
    previous_name = ""
    for version, _ in milestones(text):
        match = re.fullmatch(r"v0\.(\d+)\.(\d+)", version)
        if match is None:
            continue
        current = (int(match.group(1)), int(match.group(2)))
        if previous is not None and current <= previous:
            errors.append(f"milestone {version} is not after {previous_name}")
        previous = current
        previous_name = version
    return errors


def validate_navheim_order(text: str) -> list[str]:
    """Ensure Navheim remains the final feature phase."""
    errors: list[str] = []
    navheim_start = text.find(NAVHEIM_PHASE)
    hardening_start = text.find(HARDENING_PHASE)
    if navheim_start < 0:
        return ["missing final Navheim feature phase"]
    if hardening_start < 0:
        return ["missing post-Navheim hardening phase"]
    if hardening_start <= navheim_start:
        return ["full-system hardening must follow Navheim integration"]

    before = text[:navheim_start]
    navheim_section = text[navheim_start:hardening_start]
    navheim_versions = [version for version, _ in milestones(navheim_section)]
    if navheim_versions != NAVHEIM_VERSIONS:
        errors.append(
            "Navheim feature phase must contain exactly v0.149.0 through v0.157.0"
        )
    if "CGGTTS Interchange" in before:
        errors.append("CGGTTS must remain in the final Navheim feature phase")
    if "mundilfari-navheim Crate Boundary" in before:
        errors.append("the Navheim companion must not be introduced early")
    if "CGGTTS Interchange" not in navheim_section:
        errors.append("the final Navheim feature phase must contain CGGTTS")
    cggtts = navheim_section.find("### v0.156.0 - CGGTTS Interchange")
    gate = navheim_section.find(
        "### v0.157.0 - Navheim Interoperability And Security Gate"
    )
    if cggtts < 0 or gate < 0 or gate <= cggtts:
        errors.append("the final Navheim security gate must follow CGGTTS")
    if "No new feature or protocol scope is introduced after `v0.157.0`." not in text:
        errors.append("missing post-Navheim feature freeze")
    return errors


def main(argv: list[str]) -> int:
    """Validate the configured or default document."""
    path = Path(argv[1]) if len(argv) == 2 else Path("docs/RELEASE_PLAN.md")
    text = path.read_text(encoding="utf-8")
    errors = validate(text)
    errors.extend(validate_version_order(text))
    errors.extend(validate_review_coverage(text))
    errors.extend(validate_navheim_order(text))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"{path} release milestone format is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
