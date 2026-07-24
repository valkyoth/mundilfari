#!/usr/bin/env python3
"""Offline structural tests for the reviewed RFC corpus."""

from __future__ import annotations

import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = ROOT / "rfc" / "SOURCES"
CHECKSUMS = ROOT / "rfc" / "SHA256SUMS"
SOURCE_PATTERN = re.compile(
    r"(?P<number>[1-9][0-9]*) "
    r"https://www\.rfc-editor\.org/rfc/rfc(?P=number)\.txt "
    r"(?P<role>[a-z0-9]+(?:-[a-z0-9]+)*) "
    r"(?P<milestone>v0\.[1-9][0-9]*\.0|cross-cutting)"
)
RFC_REFERENCE = re.compile(r"\bRFC[ -]?([1-9][0-9]{2,4})\b", re.IGNORECASE)
AUTHORITATIVE_DOCS = (
    ROOT / "docs" / "PROTOCOLS.md",
    ROOT / "docs" / "RELEASE_PLAN.md",
    ROOT / "docs" / "IMPLEMENTATION_PLAN.md",
    ROOT / "docs" / "STANDARDS.md",
)
REQUIRED = {
    2119,
    3161,
    3339,
    4493,
    5905,
    7384,
    8174,
    8575,
    8633,
    8915,
    9249,
    9325,
    9523,
    9525,
    9557,
    9636,
    9748,
    9760,
    9769,
    9921,
}


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def read_sources() -> dict[int, tuple[str, str]]:
    records: dict[int, tuple[str, str]] = {}
    roles: set[str] = set()
    for line_number, raw in enumerate(SOURCES.read_text().splitlines(), 1):
        if not raw or raw.startswith("#"):
            continue
        match = SOURCE_PATTERN.fullmatch(raw)
        if match is None:
            fail(f"rfc/SOURCES:{line_number}: invalid source record")
        number = int(match.group("number"))
        role = match.group("role")
        if number in records:
            fail(f"duplicate RFC source: {number}")
        if role in roles and role not in {
            "ntp-history",
            "sntp-history",
            "requirement-language",
        }:
            fail(f"review role must be narrow and unique: {role}")
        records[number] = (role, match.group("milestone"))
        roles.add(role)
    if list(records) != sorted(records):
        fail("rfc/SOURCES must be numerically sorted")
    if missing := REQUIRED - records.keys():
        fail(f"required RFC sources missing: {sorted(missing)}")
    return records


def read_checksums() -> dict[int, str]:
    records: dict[int, str] = {}
    pattern = re.compile(r"([0-9a-f]{64})  rfc([1-9][0-9]*)\.txt")
    for line_number, raw in enumerate(CHECKSUMS.read_text().splitlines(), 1):
        match = pattern.fullmatch(raw)
        if match is None:
            fail(f"rfc/SHA256SUMS:{line_number}: invalid checksum record")
        number = int(match.group(2))
        if number in records:
            fail(f"duplicate RFC checksum: {number}")
        records[number] = match.group(1)
    return records


def main() -> None:
    sources = read_sources()
    checksums = read_checksums()
    if sources.keys() != checksums.keys():
        fail("RFC source and checksum sets differ")

    for number, expected in checksums.items():
        path = ROOT / "rfc" / f"rfc{number}.txt"
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            fail(f"RFC {number} checksum mismatch")

    referenced: set[int] = set()
    for path in AUTHORITATIVE_DOCS:
        referenced.update(int(value) for value in RFC_REFERENCE.findall(path.read_text()))
    if missing := referenced - sources.keys():
        fail(f"authoritative docs reference untracked RFCs: {sorted(missing)}")

    release_plan = (ROOT / "docs" / "RELEASE_PLAN.md").read_text()
    for number, (_, milestone) in sources.items():
        if milestone != "cross-cutting" and f"### {milestone} -" not in release_plan:
            fail(f"RFC {number} has an unknown roadmap milestone: {milestone}")
    readme = (ROOT / "README.md").read_text()
    if f"{len(sources)} checksum-locked RFCs" not in readme:
        fail("README RFC source count is stale")

    print(f"verified {len(sources)} reviewed RFC source records")


if __name__ == "__main__":
    main()
