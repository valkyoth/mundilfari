#!/usr/bin/env python3
"""Fetch checksum-pinned public standards into the ignored local vault."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import ssl
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "standards" / "SOURCES.json"
CHECKSUMS = ROOT / "standards" / "PUBLIC_SHA256SUMS"
PRIVATE = ROOT / "standards" / "private"
MAX_ARTIFACT_BYTES = 16 * 1024 * 1024


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def checksum_records() -> dict[str, str]:
    records: dict[str, str] = {}
    for line in CHECKSUMS.read_text().splitlines():
        digest, filename = line.split("  ", 1)
        records[filename] = digest
    return records


def download(url: str, destination: pathlib.Path, expected: str) -> str:
    request = urllib.request.Request(
        url, headers={"User-Agent": "mundilfari-standards-fetch/1"}
    )
    context = ssl.create_default_context()
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", dir=PRIVATE
    )
    temporary = pathlib.Path(temporary_name)
    try:
        digest = hashlib.sha256()
        with os.fdopen(descriptor, "wb") as output:
            with urllib.request.urlopen(request, timeout=90, context=context) as reply:
                original = urllib.parse.urlsplit(url)
                final = urllib.parse.urlsplit(reply.geturl())
                if final.scheme != "https" or final.hostname != original.hostname:
                    fail(f"download redirected outside the reviewed host: {url}")
                declared = reply.headers.get("Content-Length")
                if declared is not None and int(declared) > MAX_ARTIFACT_BYTES:
                    fail(f"artifact exceeds size limit: {destination.name}")
                total = 0
                while chunk := reply.read(64 * 1024):
                    total += len(chunk)
                    if total > MAX_ARTIFACT_BYTES:
                        fail(f"artifact exceeds size limit: {destination.name}")
                    digest.update(chunk)
                    output.write(chunk)
            output.flush()
            os.fsync(output.fileno())
        actual = digest.hexdigest()
        if actual != expected:
            fail(f"checksum mismatch for {destination.name}")
        os.chmod(temporary, 0o444)
        os.replace(temporary, destination)
        return actual
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    if sys.argv[1:]:
        fail("usage: scripts/fetch-standard-sources.py")
    data = json.loads(REGISTRY.read_text())
    checksums = checksum_records()
    PRIVATE.mkdir(parents=True, exist_ok=True)
    lock_path = PRIVATE / "LOCK.json"
    if lock_path.exists():
        lock_data = json.loads(lock_path.read_text())
        if lock_data.get("schema") != 1 or not isinstance(
            lock_data.get("sources"), dict
        ):
            fail("invalid standards/private/LOCK.json")
        lock = lock_data["sources"]
    else:
        lock = {}
    for source in data["sources"]:
        if source["acquisition"] != "public-download":
            continue
        filename = source["local_filename"]
        expected = checksums.get(filename)
        if expected is None:
            fail(f"missing reviewed checksum for {filename}")
        destination = PRIVATE / filename
        if destination.is_symlink():
            fail(f"local source may not be a symlink: {filename}")
        if destination.exists():
            actual = hashlib.sha256(destination.read_bytes()).hexdigest()
            if actual != expected:
                fail(f"existing local checksum mismatch for {filename}")
        else:
            actual = download(source["artifact_url"], destination, expected)
        lock[source["id"]] = actual
        print(f"{filename}: OK")
    lock_path.write_text(json.dumps({"schema": 1, "sources": lock}, indent=2) + "\n")
    os.chmod(lock_path, 0o600)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, urllib.error.URLError) as error:
        fail(f"standards fetch failed: {error}")
