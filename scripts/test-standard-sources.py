#!/usr/bin/env python3
"""Self-tests for external source registry parsing and trust pins."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import pathlib
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "verify-standard-sources.py"


def load_module():
    spec = importlib.util.spec_from_file_location("standard_sources", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load standards validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source(**overrides):
    record = {
        "id": "example-standard",
        "publisher": "Example Publisher",
        "title": "Example Standard",
        "status": "active",
        "redistribution": "local-only",
        "acquisition": "public-download",
        "milestone": "v0.2.0",
        "official_url": "https://example.test/standard",
        "artifact_url": "https://example.test/standard.txt",
        "local_filename": "example-standard.txt",
    }
    record.update(overrides)
    return record


def rejected(callback) -> None:
    with contextlib.redirect_stderr(io.StringIO()):
        try:
            callback()
        except SystemExit as error:
            assert error.code == 1
        else:
            raise AssertionError("invalid fixture was accepted")


def main() -> None:
    module = load_module()
    with tempfile.TemporaryDirectory() as directory:
        temporary = pathlib.Path(directory)
        registry = temporary / "SOURCES.json"
        checksums = temporary / "PUBLIC_SHA256SUMS"
        module.REGISTRY = registry
        module.CHECKSUMS = checksums

        def write_sources(records) -> None:
            registry.write_text(
                json.dumps(
                    {
                        "schema": 1,
                        "reviewed_at": "2026-07-24",
                        "sources": records,
                    }
                )
            )

        write_sources([source()])
        checksums.write_text(f"{'0' * 64}  example-standard.txt\n")
        assert len(module.validate_registry()) == 1
        assert module.public_checksums() == {"example-standard.txt": "0" * 64}

        write_sources([source(), source()])
        rejected(module.validate_registry)
        write_sources([source(official_url="http://example.test/standard")])
        rejected(module.validate_registry)
        write_sources([source(acquisition="manual")])
        rejected(module.validate_registry)
        write_sources([source(local_filename="../escape")])
        rejected(module.validate_registry)
        write_sources([source(milestone="v0.999.0")])
        rejected(module.validate_registry)
        write_sources([source(status="Invalid Status")])
        rejected(module.validate_registry)
        write_sources([source()])
        checksums.write_text("invalid checksum\n")
        rejected(module.public_checksums)

    print("external source registry self-tests passed")


if __name__ == "__main__":
    main()
