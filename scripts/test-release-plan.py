#!/usr/bin/env python3
"""Unit tests for check_release_plan.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_release_plan.py"
SPEC = importlib.util.spec_from_file_location("check_release_plan", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load release plan validator")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


VALID = """### v0.1.0 - Test

Status: planned.

Goal: test.

Deliverables:

- one.

Verification:

- one.

Exit criteria:

- done;
- `v0.1.0 implementation stop reached. Run pentest for this exact commit.`
"""


def main() -> None:
    """Exercise valid, missing-field, duplicate, and wrong-exit cases."""
    assert checker.validate(VALID) == []
    assert any("missing Goal:" in error for error in checker.validate(VALID.replace("Goal:", "Aim:")))
    assert any("duplicate" in error for error in checker.validate(VALID + "\n" + VALID))
    assert any(
        "exact pentest" in error
        for error in checker.validate(VALID.replace("this exact commit", "some commit"))
    )

    roadmap = f"""{checker.NAVHEIM_PHASE}
### v0.149.0 - Navheim Upstream Admission
### v0.150.0 - mundilfari-navheim Crate Boundary
### v0.151.0 - Exact GNSS Instant And Scale Mapping
### v0.152.0 - GNSS Evidence And Observation Mapping
### v0.153.0 - GNSS Event Lifecycle And Withdrawal
### v0.154.0 - Generic PPS To Navheim Correlation Bridge
### v0.155.0 - Navheim Frequency And Time-Transfer Evidence
### v0.156.0 - Navheim Interoperability And Security Gate
### v0.157.0 - CGGTTS Interchange
{checker.HARDENING_PHASE}
No new feature or protocol scope is introduced after `v0.157.0`.
"""
    assert checker.validate_navheim_order(roadmap) == []
    assert any(
        "CGGTTS" in error
        for error in checker.validate_navheim_order(
            "### v0.10.0 - CGGTTS Interchange\n" + roadmap
        )
    )

    release_plan = (ROOT / "docs" / "RELEASE_PLAN.md").read_text(encoding="utf-8")
    assert checker.validate_review_coverage(release_plan) == []
    assert any(
        "v0.7.0" in error
        for error in checker.validate_review_coverage(
            release_plan.replace("mathematical floor", "floor convention", 1)
        )
    )


if __name__ == "__main__":
    main()
