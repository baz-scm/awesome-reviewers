---
title: explicit dependency configuration
description: Ensure dependency configurations are explicit and predictable to avoid
  confusion and unexpected build behavior. Avoid package aliases that obscure the
  actual dependency being used, prefer published versions over git dependencies for
  stability, and be explicit about features that control critical behaviors like linking.
repository: denoland/deno
label: Configurations
language: Toml
comments_count: 4
repository_stars: 103714
---

Ensure dependency configurations are explicit and predictable to avoid confusion and unexpected build behavior. Avoid package aliases that obscure the actual dependency being used, prefer published versions over git dependencies for stability, and be explicit about features that control critical behaviors like linking.

When specifying dependencies:
- Avoid confusing package aliases: `ring = { version = "1.0.0", package = "aws-lc-rs" }` can cause long-term confusion
- Use published versions instead of git dependencies: `esbuild_rs = { version = "0.1.0", git = "..." }` should use a released version
- Be explicit about features that control behavior: `lcms2 = { version = "6.1.0" }` may silently fall back to static linking; disable `static-fallback` feature if dynamic linking is required
- Consider whether workspace dependencies or explicit versions better communicate intent for each specific case

This prevents silent fallbacks, reduces confusion about what's actually being used, and makes build behavior more predictable across different environments.