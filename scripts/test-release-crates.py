#!/usr/bin/env python3
"""Unit tests for release_crates.py policy functions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "release_crates.py"
SPEC = importlib.util.spec_from_file_location("release_crates", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load release_crates.py")
release_crates = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release_crates)


def plan() -> dict:
    """Return a valid synthetic plan."""
    return {
        "version": "0.1.0",
        "crates": {
            name: {"version": "0.1.0", "publish": True, "reason": "test"}
            for name in release_crates.PUBLISH_ORDER
        },
    }


def package(name: str, dependencies: tuple[str, ...] = ()) -> dict:
    """Return synthetic cargo metadata."""
    return {
        "name": name,
        "version": "0.1.0",
        "dependencies": [{"name": dep} for dep in dependencies],
    }


def packages() -> dict[str, dict]:
    """Return packages in valid dependency order."""
    return {
        "mundilfari-core": package("mundilfari-core"),
        "mundilfari-engine": package("mundilfari-engine", ("mundilfari-core",)),
        "mundilfari-platform": package("mundilfari-platform", ("mundilfari-core",)),
        "mundilfari": package(
            "mundilfari",
            ("mundilfari-core", "mundilfari-engine", "mundilfari-platform"),
        ),
    }


def assert_fails(expected: str, function, *args) -> None:
    """Require a RuntimeError containing expected."""
    try:
        function(*args)
    except RuntimeError as error:
        if expected not in str(error):
            raise AssertionError(f"expected {expected!r} in {error!r}") from error
        return
    raise AssertionError("expected RuntimeError")


def run_tests() -> None:
    """Execute all unit cases."""
    release_crates.verify_publish_order(packages(), plan())
    assert release_crates.publish_steps(plan()) == release_crates.PUBLISH_ORDER

    bad_version = packages()
    bad_version["mundilfari"]["version"] = "0.2.0"
    assert_fails("expected 0.1.0", release_crates.verify_publish_order, bad_version, plan())

    bad_order = packages()
    bad_order["mundilfari-core"]["dependencies"] = [{"name": "mundilfari-engine"}]
    assert_fails("later package", release_crates.verify_publish_order, bad_order, plan())

    partial = plan()
    partial["crates"]["mundilfari-engine"]["publish"] = False
    assert "mundilfari-engine" not in release_crates.publish_steps(partial)


if __name__ == "__main__":
    run_tests()
