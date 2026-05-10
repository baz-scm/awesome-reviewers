---
title: Deterministic CI Runs
description: 'Ensure GitHub Actions CI runs are repeatable, targeted, and don’t rely
  on brittle hacks.


  1) Run tests using the environment you just prepared

  - If you use `uv sync`, run pytest using the created venv/python (or otherwise guarantee
  `uv run` uses the synced environment without re-installing).'
repository: karpathy/nanochat
label: CI/CD
language: Yaml
comments_count: 9
repository_stars: 53189
---

Ensure GitHub Actions CI runs are repeatable, targeted, and don’t rely on brittle hacks.

1) Run tests using the environment you just prepared
- If you use `uv sync`, run pytest using the created venv/python (or otherwise guarantee `uv run` uses the synced environment without re-installing).
- Keep platform-specific dependency workarounds explicit (e.g., CPU-only torch on runners without CUDA).

2) Install the project instead of mutating PYTHONPATH
- Prefer editable installs so imports behave the same as in real usage.
- Example:
```yaml
- name: Set up uv
  uses: astral-sh/setup-uv@v7

- name: Install dependencies
  run: |
    uv sync --extra cpu
    uv pip install -e .
    # CPU-only torch for Linux runners without CUDA
    uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

- name: Run tests
  run: |
    .venv/bin/pytest tests/
```

3) Keep workflows minimal and aligned with support
- Restrict `on.push` to `master/main` (and use `pull_request` for PR validation) rather than running on every branch push.
- Keep OS/Python matrices to versions you truly support; avoid redundant `if:` conditions for OSes not in the matrix.
- Use consistent, up-to-date versions of actions/tools and avoid redundant installs when the action already provides them.

Applying this prevents CI flakiness from environment mismatches, reduces “works on my machine” import issues, and cuts unnecessary CI load.