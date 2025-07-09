---
title: Use workspace dependencies consistently
description: Always use workspace-level dependency declarations (`workspace = true`)
  rather than specifying exact versions in individual crates. This ensures consistency
  across your project, simplifies maintenance, and reduces the risk of version conflicts.
repository: vercel/turborepo
label: Configurations
language: Toml
comments_count: 2
repository_stars: 28115
---

Always use workspace-level dependency declarations (`workspace = true`) rather than specifying exact versions in individual crates. This ensures consistency across your project, simplifies maintenance, and reduces the risk of version conflicts.

When adding or updating dependencies:
1. Check if the dependency already exists at the workspace level
2. Use the workspace reference syntax when possible
3. If you need to modify features or settings, maintain the workspace reference

Example:
```diff
- git2 = { version = "0.19.0", default-features = false }
+ git2 = { workspace = true, default-features = false }
```

or

```diff
- futures = "0.3.30"
+ futures = { workspace = true }
```

This practice centralizes dependency management at the workspace level, making updates and security patches easier to apply consistently across all crates.