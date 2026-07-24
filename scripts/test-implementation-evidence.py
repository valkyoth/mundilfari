#!/usr/bin/env python3
"""Mutation tests for the implementation evidence gate."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check-implementation-evidence.py"


def load_module():
    spec = importlib.util.spec_from_file_location("implementation_evidence", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load implementation evidence validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rejected(module, path: pathlib.Path) -> None:
    try:
        module.validate(ROOT, path)
    except ValueError:
        return
    raise AssertionError("invalid implementation evidence was accepted")


def main() -> None:
    module = load_module()
    original = json.loads(
        (ROOT / "compliance" / "IMPLEMENTATION_EVIDENCE.json").read_text()
    )
    with tempfile.TemporaryDirectory() as directory:
        evidence = pathlib.Path(directory) / "evidence.json"

        evidence.write_text(json.dumps(original))
        module.validate(ROOT, evidence)

        missing_source = json.loads(json.dumps(original))
        missing_source["units"].pop()
        evidence.write_text(json.dumps(missing_source))
        rejected(module, evidence)

        no_tests = json.loads(json.dumps(original))
        no_tests["units"][0]["tests"] = []
        evidence.write_text(json.dumps(no_tests))
        rejected(module, evidence)

        wrong_source_hash = json.loads(json.dumps(original))
        wrong_source_hash["units"][0]["source_sha256"] = "0" * 64
        evidence.write_text(json.dumps(wrong_source_hash))
        rejected(module, evidence)

        missing_locator = json.loads(json.dumps(original))
        missing_locator["units"][0]["requirements"][0]["locator"] = "missing section"
        evidence.write_text(json.dumps(missing_locator))
        rejected(module, evidence)

        unlinked = json.loads(json.dumps(original))
        unlinked["units"][0]["requirements"][0]["tests"] = ["missing-test"]
        evidence.write_text(json.dumps(unlinked))
        rejected(module, evidence)

        protocol_without_standard = json.loads(json.dumps(original))
        protocol_without_standard["units"][0]["kind"] = "protocol"
        evidence.write_text(json.dumps(protocol_without_standard))
        rejected(module, evidence)

        valid_protocol = json.loads(json.dumps(original))
        valid_protocol["units"][0]["kind"] = "protocol"
        valid_protocol["units"][0]["source_documents"] = [
            {
                "id": "rfc:5905",
                "sha256": module.rfc_hashes(ROOT)["rfc:5905"],
                "clauses": ["7"],
                "errata": "reviewed for fixture",
                "requirements": ["core-capability"],
            }
        ]
        evidence.write_text(json.dumps(valid_protocol))
        module.validate(ROOT, evidence)

        standard_without_requirement = json.loads(json.dumps(valid_protocol))
        standard_without_requirement["units"][0]["source_documents"][0][
            "requirements"
        ] = []
        evidence.write_text(json.dumps(standard_without_requirement))
        rejected(module, evidence)

        unknown_standard = json.loads(json.dumps(original))
        unknown_standard["units"][0]["kind"] = "protocol"
        unknown_standard["units"][0]["source_documents"] = [
            {
                "id": "rfc:999999",
                "sha256": "0" * 64,
                "clauses": ["1"],
                "errata": "reviewed",
                "requirements": ["core-capability"],
            }
        ]
        evidence.write_text(json.dumps(unknown_standard))
        rejected(module, evidence)

        wrong_hash = json.loads(json.dumps(original))
        wrong_hash["units"][0]["kind"] = "protocol"
        wrong_hash["units"][0]["source_documents"] = [
            {
                "id": "rfc:5905",
                "sha256": "0" * 64,
                "clauses": ["7"],
                "errata": "reviewed",
                "requirements": ["core-capability"],
            }
        ]
        evidence.write_text(json.dumps(wrong_hash))
        rejected(module, evidence)

    print("implementation evidence mutation tests passed")


if __name__ == "__main__":
    main()
