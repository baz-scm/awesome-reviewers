---
title: Justify dependency and build pins
description: Any config change that affects build/runtime behavior (dependency version
  pins, feature flags, build backend settings, tool/target sources like GPU wheels)
  must include a concrete compatibility rationale and align with the build tooling
  or runtime environment.
repository: karpathy/nanochat
label: Configurations
language: Toml
comments_count: 4
repository_stars: 53189
---

Any config change that affects build/runtime behavior (dependency version pins, feature flags, build backend settings, tool/target sources like GPU wheels) must include a concrete compatibility rationale and align with the build tooling or runtime environment.

How to apply:
- For **minimum versions**, state the exact capability that requires it (e.g., protocol support) and the cutover version.
- For **feature flags** (e.g., maturin/pyo3), state *why* it’s required for your install mode and runtime (editable installs, Docker multi-stage, avoiding dynamic linkage to build-stage `libpython`).
- For **version bumps**, explain the dependency constraint (e.g., must match maturin; an upstream library can’t support the newer version yet).
- For **environment-specific sources/targets** (CUDA/ROCm), document the compatibility tradeoffs (device-specific wheels vs multi-device, whether ROCm is bundled, which versions to prefer).

Example (`pyproject.toml`):
```toml
[build-system]
requires = ["maturin>=1.9.6,<2.0"]
build-backend = "maturin"

[tool.maturin]
features = ["pyo3/extension-module"]
# Needed so editable installs and Docker multi-stage builds don't depend on build-stage libpython.

[project]
dependencies = [
  # datasets' hf:// downloader requires pyarrow >= 21.0.0
  "pyarrow>=21.0.0",
]
```

Acceptance check:
- Every version/feature/source addition has a short “why” comment tied to a specific compatibility requirement; otherwise revert or move the change behind an explicitly documented constraint.