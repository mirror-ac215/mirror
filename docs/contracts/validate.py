# /// script
# requires-python = ">=3.11"
# dependencies = ["jsonschema>=4.23"]
# ///
"""Check every example in docs/contracts/examples against its schema.

Files named *.valid.json must pass; files named *.invalid.json must fail.
Run from the repo root:  uv run docs/contracts/validate.py
"""
import json
import pathlib
import sys

from jsonschema import Draft202012Validator

HERE = pathlib.Path(__file__).parent
schema = json.loads((HERE / "context_object.schema.json").read_text())
Draft202012Validator.check_schema(schema)  # is the schema itself well-formed?
validator = Draft202012Validator(schema)

failed = False
for example in sorted((HERE / "examples").glob("context_object.*.json")):
    errors = list(validator.iter_errors(json.loads(example.read_text())))
    should_pass = ".valid." in example.name
    ok = (not errors) == should_pass
    print("PASS" if ok else "FAIL", example.name)
    for e in errors:
        where = "/".join(map(str, e.path)) or "(top level)"
        print(f"   - {where}: {e.message}")
    failed = failed or not ok

sys.exit(1 if failed else 0)