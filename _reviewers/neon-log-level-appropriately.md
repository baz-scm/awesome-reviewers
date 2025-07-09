---
title: Log level appropriately
description: 'Select the appropriate log level based on operational significance and
  ensure messages are clear, accurate, and formatted for human readability:


  1. **ERROR**: Use for failures requiring immediate attention'
repository: neondatabase/neon
label: Logging
language: Rust
comments_count: 6
repository_stars: 19015
---

Select the appropriate log level based on operational significance and ensure messages are clear, accurate, and formatted for human readability:

1. **ERROR**: Use for failures requiring immediate attention
2. **WARN**: Use for unusual but non-critical situations
3. **INFO**: Use for significant but normal operations
4. **DEBUG**: Use for detailed diagnostic information that won't impact performance

Consider the frequency and volume of log entries when selecting levels. High-frequency operations should use lower log levels (DEBUG) to avoid log pollution and performance degradation.

Format log messages for runtime readability with variables logically positioned:

```rust
// Bad - Poor readability in runtime logs
warn!(
    "could not create image layers due to {}; this is not critical because the requested image LSN is below the GC curoff",
    err
);

// Good - Clear and readable at runtime
warn!(
    "failed to create image layers but lsn is <= gc_cutoff, therefore this can happen: lsn={lsn} gc_cutoff={gc_cutoff}: {err}",
);
```

Ensure log messages accurately describe the operation being performed and provide meaningful context. Avoid logging routine operations in tight loops, especially at higher log levels.