---
title: Ecosystem Version Hygiene
description: 'When automating builds and publishing, apply two rules for version metadata
  correctness:


  1) Keep registry ecosystems independent unless you’re doing an explicit coordinated
  migration. If crates.io/PyPI/npm/WASM have separate release cadences, don’t force
  matching numbers across them—bump based on the target registry’s current release
  state and workflow.'
repository: firecrawl/pdf-inspector
label: CI/CD
language: Toml
comments_count: 2
repository_stars: 13696
---

When automating builds and publishing, apply two rules for version metadata correctness:

1) Keep registry ecosystems independent unless you’re doing an explicit coordinated migration. If crates.io/PyPI/npm/WASM have separate release cadences, don’t force matching numbers across them—bump based on the target registry’s current release state and workflow.

2) Prevent drift inside a single release toolchain by using one source of truth for the version.
- For example, when using maturin/PyO3, make the Python version come from Cargo.toml so pyproject.toml can’t silently diverge:

```toml
# pyproject.toml
[tool.maturin]
dynamic = ["version"]
```

```toml
# Cargo.toml
[package]
version = "0.1.4"
```

Operationally: in CI/CD reviews, verify (a) the version bump target matches the registry being published to, and (b) version fields are either derived from a single authoritative manifest or explicitly documented as intentionally independent to avoid accidental release inconsistencies.