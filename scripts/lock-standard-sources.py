#!/usr/bin/env python3
"""Explicitly trust-pin legitimately acquired local standards documents."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "standards" / "SOURCES.json"
CHECKSUMS = ROOT / "standards" / "PUBLIC_SHA256SUMS"
PRIVATE = ROOT / "standards" / "private"
LOCK = PRIVATE / "LOCK.json"


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if sys.argv[1:] != ["--accept-local"]:
        fail("usage: scripts/lock-standard-sources.py --accept-local")
    registry = json.loads(REGISTRY.read_text())
    public = {
        filename: digest
        for digest, filename in (
            line.split("  ", 1) for line in CHECKSUMS.read_text().splitlines()
        )
    }
    sources: dict[str, str] = {}
    PRIVATE.mkdir(parents=True, exist_ok=True)
    for source in registry["sources"]:
        path = PRIVATE / source["local_filename"]
        if not path.exists():
            continue
        if path.is_symlink() or not path.is_file():
            fail(f"local source is not a regular file: {path.name}")
        hasher = hashlib.sha256()
        with path.open("rb") as document:
            while chunk := document.read(64 * 1024):
                hasher.update(chunk)
        digest = hasher.hexdigest()
        expected = public.get(path.name)
        if expected is not None and digest != expected:
            fail(f"public source checksum mismatch: {path.name}")
        sources[source["id"]] = digest
        os.chmod(path, 0o444)
        print(f"{source['id']}: {digest}")
    if not sources:
        fail("no registered local standards documents found")
    LOCK.write_text(json.dumps({"schema": 1, "sources": sources}, indent=2) + "\n")
    os.chmod(LOCK, 0o600)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        fail(f"cannot lock local standards: {error}")
