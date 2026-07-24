#!/usr/bin/env python3
"""Publish Mundilfari crates in crates.io dependency order."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import tomllib


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "release-crates.toml"
PUBLISH_ORDER = (
    "mundilfari-core",
    "mundilfari-engine",
    "mundilfari-platform",
    "mundilfari",
)


def capture(command: list[str]) -> str:
    """Run a command and return stripped standard output."""
    return subprocess.check_output(command, cwd=ROOT, text=True).strip()


def try_capture(command: list[str]) -> str | None:
    """Return command output, or None when it fails."""
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def run(
    command: list[str],
    *,
    dry_run: bool,
    extra_env: dict[str, str] | None = None,
) -> None:
    """Print and optionally execute a release command."""
    print(f"+ {' '.join(command)}", flush=True)
    if dry_run:
        return
    environment = os.environ.copy()
    if extra_env is not None:
        environment.update(extra_env)
    subprocess.run(command, cwd=ROOT, check=True, env=environment)


def load_plan(path: Path) -> dict:
    """Load and validate release-crates.toml."""
    with path.open("rb") as handle:
        raw = tomllib.load(handle)
    release = raw.get("release", {})
    crates = raw.get("crates", {})
    version = release.get("version")
    if not isinstance(version, str):
        raise RuntimeError("release plan is missing [release].version")
    if set(crates) != set(PUBLISH_ORDER):
        raise RuntimeError("release plan crates do not match PUBLISH_ORDER")
    for name, entry in crates.items():
        if not isinstance(entry.get("version"), str):
            raise RuntimeError(f"{name} is missing version")
        if not isinstance(entry.get("publish"), bool):
            raise RuntimeError(f"{name} is missing publish boolean")
        if not isinstance(entry.get("reason"), str) or not entry["reason"].strip():
            raise RuntimeError(f"{name} is missing release reason")
    return {"version": version, "crates": crates}


def cargo_packages() -> dict[str, dict]:
    """Return workspace packages keyed by name."""
    metadata = json.loads(capture(["cargo", "metadata", "--format-version", "1", "--no-deps"]))
    member_ids = set(metadata["workspace_members"])
    return {
        package["name"]: package
        for package in metadata["packages"]
        if package["id"] in member_ids
    }


def verify_publish_order(packages: dict[str, dict], plan: dict) -> None:
    """Validate package set, versions, and dependency-first ordering."""
    if set(packages) != set(PUBLISH_ORDER):
        raise RuntimeError("workspace packages do not match PUBLISH_ORDER")
    seen: set[str] = set()
    for name in PUBLISH_ORDER:
        package = packages[name]
        expected = plan["crates"][name]["version"]
        if package["version"] != expected:
            raise RuntimeError(f"{name} is {package['version']}, expected {expected}")
        for dependency in package["dependencies"]:
            dep_name = dependency["name"]
            if dep_name in packages and dep_name not in seen:
                raise RuntimeError(f"{name} depends on later package {dep_name}")
        seen.add(name)


def publish_steps(plan: dict) -> tuple[str, ...]:
    """Return packages selected for this release."""
    return tuple(name for name in PUBLISH_ORDER if plan["crates"][name]["publish"])


def require_clean_tree(allow_dirty: bool) -> None:
    """Refuse an accidental dirty-tree publication."""
    if not allow_dirty:
        status = capture(["git", "status", "--porcelain"])
        if status:
            raise RuntimeError("refusing to publish from a dirty worktree")


def release_tag_at_head(version: str, require_tag: bool) -> bool:
    """Check whether v<version> exists and points at HEAD."""
    tag = f"v{version}"
    head = try_capture(["git", "rev-parse", "HEAD"])
    tagged = try_capture(["git", "rev-list", "-n", "1", tag])
    matches = head is not None and tagged == head
    if require_tag and not matches:
        raise RuntimeError(f"release tag {tag} does not point at HEAD")
    return matches


def run_preflight(version: str, *, tagged: bool, dry_run: bool) -> None:
    """Run the version gate and dependency checks."""
    parts = version.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise RuntimeError("release version must be numeric MAJOR.MINOR.PATCH")
    gate = ROOT / "scripts" / f"release_{'_'.join(parts)}_gate.sh"
    environment = (
        {"MUNDILFARI_RELEASE_PUBLISH_TAG": f"v{version}"} if tagged else None
    )
    command = [str(gate.relative_to(ROOT))] if gate.exists() else ["scripts/checks.sh"]
    run(command, dry_run=dry_run, extra_env=environment)
    run(
        ["scripts/validate-release-readiness.sh", f"v{version}"],
        dry_run=dry_run,
        extra_env=environment,
    )
    run(["cargo", "deny", "check"], dry_run=dry_run)
    run(["cargo", "audit"], dry_run=dry_run)


def wait_for_index(package: str, version: str, dry_run: bool) -> None:
    """Wait for crates.io index visibility before publishing dependents."""
    print(f"Published {package} {version}.")
    print(f"Confirm https://crates.io/crates/{package}/{version} before continuing.")
    if not dry_run:
        input("Press Enter after the version is visible: ")
        time.sleep(5)


def main() -> int:
    """Run release plan validation or publication."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", default=str(DEFAULT_PLAN))
    parser.add_argument("--version")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--require-tag", action="store_true")
    parser.add_argument("--skip-checks", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--start-at", choices=PUBLISH_ORDER)
    args = parser.parse_args()

    plan_path = Path(args.plan)
    if not plan_path.is_absolute():
        plan_path = (ROOT / plan_path).resolve()
    plan = load_plan(plan_path)
    version = args.version or plan["version"]
    if version != plan["version"]:
        raise RuntimeError("--version does not match release-crates.toml")

    packages = cargo_packages()
    verify_publish_order(packages, plan)
    if args.check:
        print(f"release plan {version} and publish order are valid")
        return 0

    require_clean_tree(args.allow_dirty or args.dry_run)
    tagged = release_tag_at_head(version, args.require_tag)
    steps = publish_steps(plan)
    if args.start_at is not None:
        if args.start_at not in steps:
            raise RuntimeError("--start-at package is not selected for publication")
        steps = steps[steps.index(args.start_at) :]

    print(f"Release {version}:")
    for package in steps:
        print(f"  {package} {plan['crates'][package]['version']}")
    if not args.yes:
        answer = input("Type the release version to publish: ").strip()
        if answer != version:
            print("version confirmation did not match", file=sys.stderr)
            return 1

    if not args.skip_checks:
        run_preflight(version, tagged=tagged, dry_run=args.dry_run)

    for index, package in enumerate(steps):
        command = ["cargo", "publish", "-p", package]
        if args.allow_dirty:
            command.append("--allow-dirty")
        run(command, dry_run=args.dry_run)
        if index + 1 < len(steps):
            wait_for_index(package, plan["crates"][package]["version"], args.dry_run)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1) from error
