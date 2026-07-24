#!/usr/bin/env python3
"""Validate external standards metadata and, optionally, local-only bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "standards" / "SOURCES.json"
CHECKSUMS = ROOT / "standards" / "PUBLIC_SHA256SUMS"
PRIVATE = ROOT / "standards" / "private"
LOCK = PRIVATE / "LOCK.json"
REQUIRED_FIELDS = {
    "id",
    "publisher",
    "title",
    "status",
    "redistribution",
    "acquisition",
    "milestone",
    "official_url",
    "local_filename",
}
ACQUISITIONS = {"public-download", "manual", "metadata-only"}
REDISTRIBUTION = {"local-only", "restricted"}
MILESTONE = re.compile(r"v0\.[1-9][0-9]*\.[0-9]+")
SAFE_NAME = re.compile(r"[a-z0-9][a-z0-9._-]*")


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def load_json(path: pathlib.Path) -> Any:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{path.relative_to(ROOT)}: {error}")


def validate_registry() -> list[dict[str, str]]:
    data = load_json(REGISTRY)
    if data.get("schema") != 1 or not re.fullmatch(
        r"20[0-9]{2}-[01][0-9]-[0-3][0-9]", data.get("reviewed_at", "")
    ):
        fail("invalid standards registry header")
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        fail("standards registry has no sources")

    identifiers: set[str] = set()
    filenames: set[str] = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            fail(f"source {index} is not an object")
        missing = REQUIRED_FIELDS - source.keys()
        if missing:
            fail(f"source {index} lacks fields: {sorted(missing)}")
        identifier = source["id"]
        filename = source["local_filename"]
        if not SAFE_NAME.fullmatch(identifier) or not SAFE_NAME.fullmatch(filename):
            fail(f"unsafe source identifier or filename: {identifier}")
        if identifier in identifiers or filename in filenames:
            fail(f"duplicate source identifier or filename: {identifier}")
        identifiers.add(identifier)
        filenames.add(filename)
        if source["acquisition"] not in ACQUISITIONS:
            fail(f"invalid acquisition for {identifier}")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", source["status"]):
            fail(f"invalid status for {identifier}")
        if not source["publisher"].strip() or not source["title"].strip():
            fail(f"missing publisher or title for {identifier}")
        if source["redistribution"] not in REDISTRIBUTION:
            fail(f"invalid redistribution for {identifier}")
        if not MILESTONE.fullmatch(source["milestone"]):
            fail(f"invalid milestone for {identifier}")
        if not source["official_url"].startswith("https://"):
            fail(f"non-HTTPS official URL for {identifier}")
        if source["acquisition"] == "public-download":
            if not source.get("artifact_url", "").startswith("https://"):
                fail(f"public download lacks HTTPS artifact URL: {identifier}")
        elif "artifact_url" in source:
            fail(f"non-public source has an artifact URL: {identifier}")
        release_plan = (ROOT / "docs" / "RELEASE_PLAN.md").read_text()
        if f"### {source['milestone']} -" not in release_plan:
            fail(f"unknown roadmap milestone for {identifier}")
    return sources


def public_checksums() -> dict[str, str]:
    result: dict[str, str] = {}
    pattern = re.compile(r"([0-9a-f]{64})  ([a-z0-9][a-z0-9._-]*)")
    for line_number, line in enumerate(CHECKSUMS.read_text().splitlines(), 1):
        match = pattern.fullmatch(line)
        if match is None:
            fail(f"standards/PUBLIC_SHA256SUMS:{line_number}: invalid record")
        digest, filename = match.groups()
        if filename in result:
            fail(f"duplicate public checksum: {filename}")
        result[filename] = digest
    return result


def verify_ignore_rule() -> None:
    check = subprocess.run(
        ["git", "check-ignore", "-q", "standards/private/probe.document"],
        cwd=ROOT,
        check=False,
    )
    if check.returncode != 0:
        fail("standards/private is not protected by .gitignore")
    tracked = subprocess.run(
        ["git", "ls-files", "standards/private"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if tracked:
        fail("local-only standards artifacts are tracked by Git")


def verify_local(sources: list[dict[str, str]], checksums: dict[str, str]) -> None:
    lock_data = load_json(LOCK) if LOCK.exists() else {"sources": {}}
    locked = lock_data.get("sources", {})
    if not isinstance(locked, dict):
        fail("invalid standards/private/LOCK.json")
    missing_manual: list[str] = []
    for source in sources:
        filename = source["local_filename"]
        path = PRIVATE / filename
        if source["acquisition"] == "metadata-only":
            continue
        if not path.exists():
            if source["acquisition"] == "public-download":
                fail(f"missing public local source: {filename}")
            missing_manual.append(source["id"])
            continue
        if path.is_symlink() or not path.is_file():
            fail(f"local source is not a file: {filename}")
        hasher = hashlib.sha256()
        with path.open("rb") as document:
            while chunk := document.read(64 * 1024):
                hasher.update(chunk)
        digest = hasher.hexdigest()
        if source["acquisition"] == "public-download":
            if checksums.get(filename) != digest:
                fail(f"public local checksum mismatch: {filename}")
        if locked.get(source["id"]) != digest:
            fail(f"local lock mismatch: {source['id']}")
    if missing_manual:
        print(
            f"manual acquisition pending for {len(missing_manual)} sources: "
            + ", ".join(missing_manual)
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", action="store_true")
    args = parser.parse_args()
    sources = validate_registry()
    checksums = public_checksums()
    expected = {
        source["local_filename"]
        for source in sources
        if source["acquisition"] == "public-download"
    }
    if checksums.keys() != expected:
        fail("public-download source and checksum sets differ")
    readme = (ROOT / "README.md").read_text()
    if f"{len(sources)} external-source records" not in readme:
        fail("README external source count is stale")
    verify_ignore_rule()
    if args.local:
        verify_local(sources, checksums)
    print(
        f"verified {len(sources)} external source records "
        f"({len(expected)} public local downloads)"
    )


if __name__ == "__main__":
    main()
