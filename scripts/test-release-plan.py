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


if __name__ == "__main__":
    main()
