---
title: Prevent uv Overwrites
description: When CI workflows mix multiple uv steps (e.g., install built wheels,
  then run tests/lint), make dependency installation *deterministic* and prevent later
  steps from overwriting earlier artifact installs.
repository: langchain-ai/langchain
label: CI/CD
language: Yaml
comments_count: 4
repository_stars: 136312
---

When CI workflows mix multiple uv steps (e.g., install built wheels, then run tests/lint), make dependency installation *deterministic* and prevent later steps from overwriting earlier artifact installs.

Apply these rules:
- Validate lock consistency in CI: run `uv lock --check` (or equivalent in your `uv_setup`).
- Use uv groups for scoped installs: `uv sync --group <name> ...`.
- Remember `uv sync` is subtractive: it can remove deps not in the selected group(s) (so expect functional differences vs non-sync installs).
- If a workflow installs an artifact (wheel) and subsequent steps might “sync” (directly or via `uv run`), stop uv from resynchronizing that environment.
  - Prefer restricting sync to the needed groups (e.g., `uv sync --only-group test ...`).
  - Or set `UV_NO_SYNC=true` when using `uv run`/test commands that would otherwise sync and replace the wheel with the local project.

Example pattern (wheel install + tests without overwriting):
```bash
# Install built wheel artifacts
uv pip install dist/*.whl

# Prevent later uv operations (including under uv run) from syncing/overwriting
export UV_NO_SYNC=true

# Run tests (may internally call uv run)
make tests  # should behave like: uv run --group test pytest ...
```

For group-scoped test deps, prefer:
```bash
uv sync --only-group test
# then run tests
uv run pytest
```

This avoids the common CI failure mode where a built wheel install is replaced by the local project (or where earlier dependency changes vanish after a later `uv run`).