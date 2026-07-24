#!/usr/bin/env python3
"""Fail closed unless every published implementation has requirements and tests."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "compliance" / "IMPLEMENTATION_EVIDENCE.json"
KINDS = {
    "algorithm",
    "application",
    "format",
    "foundation",
    "integration",
    "platform",
    "protocol",
}
TEST_KINDS = {
    "conformance",
    "fuzz",
    "hardware",
    "integration",
    "interop",
    "property",
    "security",
    "simulation",
    "unit",
}
PROTOCOL_KINDS = {"format", "integration", "protocol"}
SAFE_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
SHA256 = re.compile(r"[0-9a-f]{64}")
MILESTONE = re.compile(r"v0\.[1-9][0-9]*\.[0-9]+")


def fail(message: str) -> None:
    raise ValueError(message)


def relative_file(root: pathlib.Path, value: Any, label: str) -> pathlib.Path:
    if not isinstance(value, str) or not value:
        fail(f"{label} must be a nonempty path")
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value.startswith("standards/private/"):
        fail(f"{label} is unsafe: {value}")
    result = root / path
    if not result.is_file():
        fail(f"{label} does not exist: {value}")
    return result


def production_sources(root: pathlib.Path) -> set[str]:
    result = {
        path.relative_to(root).as_posix()
        for path in (root / "crates").glob("*/src/**/*.rs")
        if path.is_file()
    }
    result.update(
        path.relative_to(root).as_posix()
        for path in (root / "crates").glob("*/build.rs")
        if path.is_file()
    )
    return result


def rfc_hashes(root: pathlib.Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in (root / "rfc" / "SHA256SUMS").read_text().splitlines():
        digest, filename = line.split("  ", 1)
        result[f"rfc:{filename.removeprefix('rfc').removesuffix('.txt')}"] = digest
    return result


def external_sources(root: pathlib.Path) -> tuple[set[str], dict[str, str]]:
    registry = json.loads((root / "standards" / "SOURCES.json").read_text())
    identifiers = {f"external:{source['id']}" for source in registry["sources"]}
    by_filename = {
        source["local_filename"]: f"external:{source['id']}"
        for source in registry["sources"]
    }
    hashes: dict[str, str] = {}
    for line in (root / "standards" / "PUBLIC_SHA256SUMS").read_text().splitlines():
        digest, filename = line.split("  ", 1)
        hashes[by_filename[filename]] = digest
    return identifiers, hashes


def validate_standard(
    record: Any,
    known: set[str],
    pinned: dict[str, str],
    requirement_ids: set[str],
    unit_id: str,
) -> None:
    if not isinstance(record, dict):
        fail(f"{unit_id}: source document is not an object")
    identifier = record.get("id")
    if identifier not in known:
        fail(f"{unit_id}: unknown source document {identifier}")
    digest = record.get("sha256")
    if not isinstance(digest, str) or SHA256.fullmatch(digest) is None:
        fail(f"{unit_id}: source document {identifier} lacks reviewed SHA-256")
    if identifier in pinned and pinned[identifier] != digest:
        fail(f"{unit_id}: source document {identifier} hash differs from corpus")
    clauses = record.get("clauses")
    if not isinstance(clauses, list) or not clauses or not all(
        isinstance(clause, str) and clause.strip() for clause in clauses
    ):
        fail(f"{unit_id}: source document {identifier} lacks exact clauses")
    if not isinstance(record.get("errata"), str) or not record["errata"].strip():
        fail(f"{unit_id}: source document {identifier} lacks errata disposition")
    linked = record.get("requirements")
    if (
        not isinstance(linked, list)
        or not linked
        or not set(linked) <= requirement_ids
    ):
        fail(f"{unit_id}: source document {identifier} lacks valid requirements")


def validate(root: pathlib.Path, evidence: pathlib.Path) -> None:
    data = json.loads(evidence.read_text())
    if data.get("schema") != 1 or re.fullmatch(
        r"20[0-9]{2}-[01][0-9]-[0-3][0-9]", data.get("reviewed_at", "")
    ) is None:
        fail("invalid implementation evidence header")
    units = data.get("units")
    if not isinstance(units, list) or not units:
        fail("implementation evidence has no units")

    rfc = rfc_hashes(root)
    external, external_hashes = external_sources(root)
    known_sources = set(rfc) | external
    pinned_sources = rfc | external_hashes
    release_plan = (root / "docs" / "RELEASE_PLAN.md").read_text()
    unit_ids: set[str] = set()
    covered_sources: set[str] = set()

    for unit in units:
        if not isinstance(unit, dict):
            fail("implementation unit is not an object")
        unit_id = unit.get("id")
        if not isinstance(unit_id, str) or SAFE_ID.fullmatch(unit_id) is None:
            fail(f"invalid implementation unit id: {unit_id}")
        if unit_id in unit_ids:
            fail(f"duplicate implementation unit id: {unit_id}")
        unit_ids.add(unit_id)
        source = unit.get("source")
        source_path = relative_file(root, source, f"{unit_id} source")
        source_digest = unit.get("source_sha256")
        if not isinstance(source_digest, str) or SHA256.fullmatch(source_digest) is None:
            fail(f"{unit_id}: source lacks reviewed SHA-256")
        if hashlib.sha256(source_path.read_bytes()).hexdigest() != source_digest:
            fail(f"{unit_id}: implementation changed without evidence review")
        if source in covered_sources:
            fail(f"source registered more than once: {source}")
        covered_sources.add(source)
        kind = unit.get("kind")
        if kind not in KINDS:
            fail(f"{unit_id}: invalid implementation kind")
        milestone = unit.get("milestone")
        if not isinstance(milestone, str) or MILESTONE.fullmatch(milestone) is None:
            fail(f"{unit_id}: invalid milestone")
        if f"### {milestone} -" not in release_plan:
            fail(f"{unit_id}: unknown milestone {milestone}")

        tests = unit.get("tests")
        if not isinstance(tests, list) or not tests:
            fail(f"{unit_id}: no test evidence")
        test_ids: set[str] = set()
        for test in tests:
            test_id = test.get("id") if isinstance(test, dict) else None
            if not isinstance(test_id, str) or SAFE_ID.fullmatch(test_id) is None:
                fail(f"{unit_id}: invalid test id")
            if test_id in test_ids:
                fail(f"{unit_id}: duplicate test id {test_id}")
            test_ids.add(test_id)
            test_file = relative_file(root, test.get("file"), f"{unit_id} test file")
            name = test.get("name")
            if not isinstance(name, str) or re.fullmatch(r"[a-z][a-z0-9_]*", name) is None:
                fail(f"{unit_id}: invalid test function name")
            if re.search(rf"\bfn\s+{re.escape(name)}\s*\(", test_file.read_text()) is None:
                fail(f"{unit_id}: test function not found: {name}")
            if test.get("kind") not in TEST_KINDS:
                fail(f"{unit_id}: invalid test kind")

        requirements = unit.get("requirements")
        if not isinstance(requirements, list) or not requirements:
            fail(f"{unit_id}: no governing requirements")
        requirement_ids: set[str] = set()
        linked_tests: set[str] = set()
        for requirement in requirements:
            requirement_id = requirement.get("id") if isinstance(requirement, dict) else None
            if not isinstance(requirement_id, str) or SAFE_ID.fullmatch(requirement_id) is None:
                fail(f"{unit_id}: invalid requirement id")
            if requirement_id in requirement_ids:
                fail(f"{unit_id}: duplicate requirement id {requirement_id}")
            requirement_ids.add(requirement_id)
            requirement_document = relative_file(
                root, requirement.get("document"), f"{unit_id} requirement document"
            )
            locator = requirement.get("locator")
            if not isinstance(locator, str) or not locator.strip():
                fail(f"{unit_id}: requirement {requirement_id} lacks locator")
            if locator not in requirement_document.read_text():
                fail(f"{unit_id}: requirement locator not found: {locator}")
            linked = requirement.get("tests")
            if not isinstance(linked, list) or not linked or not set(linked) <= test_ids:
                fail(f"{unit_id}: requirement {requirement_id} lacks valid linked tests")
            linked_tests.update(linked)
        if linked_tests != test_ids:
            fail(f"{unit_id}: test evidence is not linked to a requirement")

        documents = unit.get("source_documents")
        if not isinstance(documents, list):
            fail(f"{unit_id}: source_documents is not a list")
        if kind in PROTOCOL_KINDS and not documents:
            fail(f"{unit_id}: protocol/format/integration work lacks source documents")
        for document in documents:
            validate_standard(
                document, known_sources, pinned_sources, requirement_ids, unit_id
            )

    expected = production_sources(root)
    if covered_sources != expected:
        missing = sorted(expected - covered_sources)
        extra = sorted(covered_sources - expected)
        fail(f"implementation source coverage differs; missing={missing}, extra={extra}")


def main() -> int:
    try:
        validate(ROOT, EVIDENCE)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"implementation evidence invalid: {error}", file=sys.stderr)
        return 1
    digest = hashlib.sha256(EVIDENCE.read_bytes()).hexdigest()
    print(f"implementation evidence valid: {len(production_sources(ROOT))} sources ({digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
