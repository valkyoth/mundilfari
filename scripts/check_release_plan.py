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
    if "No new feature or protocol scope is introduced after `v0.157.0`." not in text:
        errors.append("missing post-Navheim feature freeze")
    return errors


def main(argv: list[str]) -> int:
    """Validate the configured or default document."""
    path = Path(argv[1]) if len(argv) == 2 else Path("docs/RELEASE_PLAN.md")
    text = path.read_text(encoding="utf-8")
    errors = validate(text)
    errors.extend(validate_navheim_order(text))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"{path} release milestone format is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
