---
title: Cache keys drive rebuilds
description: When using uv to build Python extensions via PEP 517 (e.g., maturin),
  ensure cache invalidation is keyed to the actual build inputs. Configure `tool.uv.cache-keys`
  so builds rerun only when the underlying sources for the compiled artifact change—especially
  Rust sources and Cargo manifests—rather than rebuilding whatever project owns the
  root...
repository: karpathy/nanochat
label: Caching
language: Toml
comments_count: 2
repository_stars: 53189
---

When using uv to build Python extensions via PEP 517 (e.g., maturin), ensure cache invalidation is keyed to the actual build inputs. Configure `tool.uv.cache-keys` so builds rerun only when the underlying sources for the compiled artifact change—especially Rust sources and Cargo manifests—rather than rebuilding whatever project owns the root `pyproject.toml`.

Apply this by:
- Adding Rust build inputs to `tool.uv.cache-keys` (e.g., `src/**/*.rs`, `Cargo.toml`, `Cargo.lock`, or the whole crate dir like `rustbpe/**`).
- Including the crate in the workspace so uv associates changes with the correct package (e.g., `rustbpe = { workspace = true }`).
- Verifying `uv sync` / `uv run` actually rebuilds the intended artifact when Rust code changes.

Example:
```toml
[tool.uv]
# Invalidate build cache when Rust crate inputs change
cache-keys = [
  { file = "pyproject.toml" },
  { file = "rustbpe/**" },
  # alternatively, more targeted keys like:
  # { file = "src/**/*.rs" },
  # { file = "Cargo.toml" },
  # { file = "Cargo.lock" }
]

# Ensure the crate is part of the workspace so the right package rebuilds
[rustbpe]
# (or in the relevant uv sources section)
# rustbpe = { workspace = true }
```