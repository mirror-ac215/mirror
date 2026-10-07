"""Validate Mirror's shared JSON Schema examples and OpenAPI contracts.

The command is deliberately repository-level: it validates the written contract
sources even when no service implementation changes in the same pull request.

Run from the repository root:
    uv run --project docs/contracts python docs/contracts/validate.py
"""

from __future__ import annotations

import json
import pathlib
import sys
from collections.abc import Iterable

import yaml
from jsonschema import Draft202012Validator
from openapi_spec_validator import validate

HERE = pathlib.Path(__file__).parent


def validate_context_examples() -> bool:
    """Validate the context-object schema and its valid/invalid examples."""
    schema = json.loads((HERE / "context_object.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    failed = False
    examples: Iterable[pathlib.Path] = sorted(
        (HERE / "examples").glob("context_object.*.json")
    )
    for example in examples:
        errors = list(validator.iter_errors(json.loads(example.read_text(encoding="utf-8"))))
        should_pass = ".valid." in example.name
        ok = (not errors) == should_pass
        print("PASS" if ok else "FAIL", example.name)
        if not ok:
            for error in errors:
                where = "/".join(map(str, error.path)) or "(top level)"
                print(f"   - {where}: {error.message}")
        failed = failed or not ok
    return not failed


def openapi_contract_paths() -> list[pathlib.Path]:
    """Discover every OpenAPI contract so future services are not skipped."""
    return sorted(HERE.glob("*.openapi.yaml"))


def validate_openapi_contracts() -> bool:
    """Validate every repository OpenAPI source document structurally."""
    paths = openapi_contract_paths()
    if not paths:
        print("FAIL no OpenAPI contract files found")
        return False

    failed = False
    for path in paths:
        try:
            specification = yaml.safe_load(path.read_text(encoding="utf-8"))
            validate(specification)
        except Exception as error:  # validator exceptions vary across spec versions
            print("FAIL", path.name)
            print(f"   - {error}")
            failed = True
        else:
            print("PASS", path.name)
    return not failed


def main() -> int:
    """Run every shared-contract check and return a CI-friendly exit code."""
    context_ok = validate_context_examples()
    openapi_ok = validate_openapi_contracts()
    return 0 if context_ok and openapi_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
