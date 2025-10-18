---
title: optimize remote fetch operations
description: When implementing network operations that fetch data from remote sources,
  configure specific refspecs or patterns to fetch only the required data rather than
  everything available. This reduces network bandwidth usage, improves performance,
  and ensures future operations remain efficient.
repository: jj-vcs/jj
label: Networking
language: Rust
comments_count: 2
repository_stars: 21171
---

When implementing network operations that fetch data from remote sources, configure specific refspecs or patterns to fetch only the required data rather than everything available. This reduces network bandwidth usage, improves performance, and ensures future operations remain efficient.

For Git remote operations, specify target branches/bookmarks explicitly:

```rust
// Instead of fetching everything
expand_fetch_refspecs(remote_name, vec![StringPattern::everything()])

// Fetch only specified branches
expand_fetch_refspecs(
    remote_name,
    target_branches
        .unwrap_or(&[StringPattern::everything()])
        .to_vec(),
)
```

Configure remotes with specific refspecs so that future fetch operations automatically use the same selective patterns. This prevents unnecessary network traffic and keeps the local repository focused on relevant data.

The same principle applies to other network operations: be explicit about what data you need rather than fetching everything available, and persist these preferences for consistency across operations.