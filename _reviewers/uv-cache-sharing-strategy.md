---
title: Cache sharing strategy
description: When implementing caching in build systems, carefully configure cache
  sharing behavior based on your concurrency requirements. Improper sharing settings
  can lead to build failures when multiple processes attempt to access the same cache
  simultaneously.
repository: astral-sh/uv
label: Caching
language: Dockerfile
comments_count: 2
repository_stars: 60322
---

When implementing caching in build systems, carefully configure cache sharing behavior based on your concurrency requirements. Improper sharing settings can lead to build failures when multiple processes attempt to access the same cache simultaneously.

For Docker BuildKit cache mounts:
- Use `sharing=shared` (default) for caches with internal locking mechanisms or read-only access patterns
- Use `sharing=locked` when cache contents cannot handle concurrent writers
- Use `sharing=private` for isolated per-build caches that don't benefit from sharing
- Consider using tmpfs mounts to exclude directories containing temporary or easily regenerated data

Example of proper cache configuration:
```dockerfile
RUN \
  # Global cache that safely handles concurrent access
  --mount=type=cache,target=/var/lib/apt/lists,type=cache,sharing=shared \
  # Cache that needs exclusive access to prevent corruption
  --mount=type=cache,target="/root/.cache/rustup",id="rustup-toolchain",sharing=locked \
  # Project-specific build cache with isolated ID to prevent unintended sharing
  --mount=type=cache,target="target/",id="cargo-target-${APP_NAME}-${TARGETPLATFORM}",sharing=locked \
  # Exclude temporary directories from caching with tmpfs
  --mount=type=tmpfs,target="${CARGO_HOME}/registry/src" \
  --mount=type=tmpfs,target="${CARGO_HOME}/git/checkouts" \
  cargo build --release
```

Always consider the concurrency patterns of your build environment. Remember that caches with the same ID are shared across different builds, which can cause unexpected interactions between unrelated projects.