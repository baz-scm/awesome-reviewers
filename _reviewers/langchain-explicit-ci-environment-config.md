---
title: Explicit CI Environment Config
description: Make CI and build configuration deterministic by explicitly selecting
  tool versions and target environments, and by ensuring monorepo config paths match
  what downstream generators expect.
repository: langchain-ai/langchain
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 136312
---

Make CI and build configuration deterministic by explicitly selecting tool versions and target environments, and by ensuring monorepo config paths match what downstream generators expect.

Apply this by:
- Pin/configure tool versions in workflows (don’t rely on defaults).
- Ensure `uv`/Python install steps target the intended venv explicitly (or deterministically discover it), rather than inheriting an existing/global `VIRTUAL_ENV` or relying on auto-activation.
- Validate monorepo package metadata (e.g., `path`) so config-driven steps (like docs/provider discovery) can find the expected files.

Example (targeting the correct venv with `uv`):
```sh
# Prefer deterministic venv selection; keep it explicit to avoid global overlap.
VIRTUAL_ENV=.venv uv pip install dist/*.whl

# If you prefer deriving it, ensure your script finds/creates the same venv
# that the rest of the pipeline uses, then pass VIRTUAL_ENV accordingly.
uv venv
VIRTUAL_ENV=.venv uv pip install dist/*.whl
```

Example (monorepo package config):
```yaml
# Ensure `path` reflects the package root the build/docs tooling expects.
- name: toolbox-langchain
  repo: googleapis/mcp-toolbox-sdk-python
  path: .   # (not a nested subdir) when the generator expects package-root contents
```