# Shared contract validation

This folder contains the written agreements between Mirror components: the API
contracts and the gateway-to-LLM context-object schema. Think of a contract as
the labelled plug shared by two components: both sides need the same shape
before they can connect.

## The normal workflow

Use these commands **only when you change a file in this folder**.

```bash
cd docs/contracts
uv run python validate.py
```

This one command checks the valid and invalid context-object examples and every
top-level `*.openapi.yaml` contract. It exits with an error if any written
contract is malformed.

## First setup or lockfile update

After a fresh clone, or when `pyproject.toml` or `uv.lock` changes, install the
exact locked validator tools first:

```bash
cd docs/contracts
uv sync --frozen --all-groups
```

Then use the normal validation command above.

## When changing the validator or CI itself

Only run this extra test suite when changing `validate.py`, `tests/`,
`pyproject.toml`, `uv.lock`, or the contract-validation section of the CI
workflow:

```bash
cd docs/contracts
uv run pytest -v
```

These tests protect the validator and make sure the overall GitHub CI result
fails when a required contract check fails, is cancelled, or is skipped.

## Adding a future service contract

Name the file:

```text
<service-name>.openapi.yaml
```

For example, a future text-to-speech service would use
`tts-service.openapi.yaml`. The validator discovers every file following this
pattern automatically, so you do not need to update a separate list or CI job.

## What this check proves, and what it does not

Passing contract validation proves that the **written** OpenAPI and JSON Schema
documents are structurally valid. It does not prove that a running service
implements them correctly. The service owner must still add endpoint and
integration tests in that service's own folder.

## Rules for dependency updates

- This is a Python 3.11 `uv` project, separate from each service project.
- Keep `pyproject.toml` and `uv.lock` together in the same pull request when
  changing validator dependencies.
- Do not use `uvx` for routine contract checks: it bypasses the committed lockfile.
- Do not run `uv sync` from the repository root; this repository has separate
  component projects rather than one root Python project.