#!/usr/bin/env python3
"""Unit tests for the release-plan size ceiling."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check-release-plan-size.py"
SPEC = importlib.util.spec_from_file_location("check_release_plan_size", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load release-plan size validator")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def milestone(deliverables: int, padding: int = 0) -> str:
    """Build one deterministic roadmap fixture."""
    items = "".join(f"- item {index}.\n" for index in range(deliverables))
    extra = "context\n" * padding
    return (
        "### v0.1.0 - Fixture\n\nStatus: planned.\n\nGoal: fixture.\n\n"
        f"Deliverables:\n\n{items}{extra}\nVerification:\n\n- tested.\n\n"
        "Exit criteria:\n\n- complete.\n"
    )


def main() -> None:
    """Cover exact limits and both overflow modes."""
    assert checker.validate(milestone(checker.MAX_DELIVERABLES)) == []
    assert any(
        "deliverables" in error
        for error in checker.validate(milestone(checker.MAX_DELIVERABLES + 1))
    )
    assert any(
        "lines" in error
        for error in checker.validate(milestone(1, checker.MAX_MILESTONE_LINES))
    )


if __name__ == "__main__":
    main()
