---
title: Respect connectivity state
description: 'Applications should gracefully handle different network connectivity
  states and provide appropriate feedback to users. Follow these guidelines:


  1. **Check connectivity state before network operations** - Always verify if the
  application is in offline mode before attempting network requests'
repository: astral-sh/uv
label: Networking
language: Rust
comments_count: 4
repository_stars: 60322
---

Applications should gracefully handle different network connectivity states and provide appropriate feedback to users. Follow these guidelines:

1. **Check connectivity state before network operations** - Always verify if the application is in offline mode before attempting network requests
2. **Provide specific error messages** - When operations fail due to connectivity restrictions, include the exact reason in error messages
3. **Implement smart caching strategies** - Reduce network requests by checking local caches first
4. **Handle status codes appropriately** - Differentiate between retryable errors (like rate limits) and fatal errors with appropriate retry strategies

Example for offline handling:
```rust
if network_settings.connectivity.is_offline() {
    writeln!(
        printer.stderr(),
        "{}",
        format_args!(
            "{}{} Operation is not possible because network connectivity is disabled (i.e., with `--offline`)",
            // formatting details
        )
    )?;
    return Ok(ExitStatus::Failure);
}
```

Example for checking cache before network request:
```rust
// Check if we already have the resource locally before making a network request
if let (Some(rev), Some(db)) = (self.git.precise(), &maybe_db) {
    if db.contains(rev) {
        debug!("Using existing Git source `{}`", self.git.repository());
        return Ok((maybe_db.unwrap(), rev, None));
    }
}

// Only make network request if needed
// Handle different status codes appropriately
let decision = status_code_strategy.handle_status_code(status_code, index, capabilities);
```