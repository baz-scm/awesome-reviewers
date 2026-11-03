---
title: Pyproject configuration standards
description: 'All integration packages must follow consistent `pyproject.toml` conventions:


  1. **Build system**: Use `hatchling` as the build backend with `uv` for dependency
  management, not `poetry`. Example:'
repository: run-llama/llama_index
label: Configurations
language: Toml
comments_count: 15
repository_stars: 52785
---

All integration packages must follow consistent `pyproject.toml` conventions:

1. **Build system**: Use `hatchling` as the build backend with `uv` for dependency management, not `poetry`. Example:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[dependency-groups]
dev = [ ... ]
```

2. **Dependency version ranges**: Pin dependencies using sensible semver-compatible ranges (`>=X.Y.Z,<X+1.0.0`), not exact pins (`==`) unless strictly required, and not overly wide ranges that span multiple major versions (e.g. avoid `>=0.1.0,<8.0.0`). Double-check that the lower/upper bounds are internally consistent (no off-by-one errors) and only include dependencies that are actually required by the package code/tests — don't duplicate a dependency already listed in `dependencies` inside the `dev` group, and don't promote example-notebook-only dependencies to base dependencies.

3. **Version bumps**: The package `version` bump must match the nature of the change — a patch bump (`0.10.10` → `0.10.11`) for fixes, a minor bump for new features or newly introduced dependencies, and a more significant bump when default behavior changes. Always verify agent-suggested version bumps before merging.

4. **Python support**: `requires-python` should target the current minimum supported Python version (avoid already-EOL versions like 3.9); only require a higher minimum if a hard dependency mandates it, and document why.

5. **Metadata completeness**: Ensure required `[tool.llamahub]` sections (e.g. `import_path`, `class_authors`) are filled in correctly, and remove placeholder/leftover comments from the template.

Following these rules keeps builds reproducible across integrations and prevents dependency/version mismatches from breaking downstream consumers.