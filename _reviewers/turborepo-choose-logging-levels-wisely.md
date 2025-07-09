---
title: Choose logging levels wisely
description: Select appropriate logging levels based on the frequency and importance
  of the logged operation. Use `trace` for high-frequency operations (e.g., operations
  executed once per package or file) to prevent log noise at lower verbosity levels,
  and reserve `debug` for less frequent, more significant events or aggregated information.
repository: vercel/turborepo
label: Logging
language: Rust
comments_count: 4
repository_stars: 28115
---

Select appropriate logging levels based on the frequency and importance of the logged operation. Use `trace` for high-frequency operations (e.g., operations executed once per package or file) to prevent log noise at lower verbosity levels, and reserve `debug` for less frequent, more significant events or aggregated information.

Include relevant context in log messages to make them actionable:

```rust
// Less useful - lacks context
debug!("files to cache: {:?}", files_to_be_cached.len());

// More useful - includes task identifier
debug!("{}: files to cache: {:?}", self.task_id, files_to_be_cached.len());

// For high-frequency operations, use trace
trace!("loading package.json from {}", path);
```

By thoughtfully selecting logging levels and providing context, you create logs that are both informative when needed and not overwhelming during regular operation. This enables effective debugging without drowning developers in noise when using increased verbosity.