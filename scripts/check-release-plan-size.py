#!/usr/bin/env python3
"""Fail when one roadmap milestone grows beyond one safe review pass."""

from __future__ import annotations

import re
import sys
from pathlib import Path


HEADING = re.compile(r"^### (v(?:0\.\d+\.\d+|1\.0\.0-rc\.\d+)) ", re.MULTILINE)
MAX_MILESTONE_LINES = 180
MAX_DELIVERABLES = 16


def validate(text: str) -> list[str]:
    """Return deterministic milestone-size violations."""
    errors: list[str] = []
    matches = list(HEADING.finditer(text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.start() : end]
        version = match.group(1)
        line_count = len(block.splitlines())
        deliverable_text = block.partition("Deliverables:")[2].partition("Verification:")[0]
        deliverables = sum(line.startswith("- ") for line in deliverable_text.splitlines())
        if line_count > MAX_MILESTONE_LINES:
            errors.append(
                f"{version} has {line_count} lines; maximum is {MAX_MILESTONE_LINES}"
            )
        if deliverables > MAX_DELIVERABLES:
            errors.append(
                f"{version} has {deliverables} deliverables; maximum is {MAX_DELIVERABLES}"
            )
    return errors


def main(argv: list[str]) -> int:
    """Validate the configured or default release plan."""
    path = Path(argv[1]) if len(argv) == 2 else Path("docs/RELEASE_PLAN.md")
    errors = validate(path.read_text(encoding="utf-8"))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"{path} milestone sizes are within review limits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
