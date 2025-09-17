---
title: SQL query best practices
description: Always include ORDER BY clauses in paginated queries to ensure consistent
  results across multiple requests. Without explicit ordering, databases may return
  results in different orders each time, making pagination unreliable and potentially
  causing data to be skipped or duplicated.
repository: unionlabs/union
label: Database
language: Rust
comments_count: 3
repository_stars: 74800
---

Always include ORDER BY clauses in paginated queries to ensure consistent results across multiple requests. Without explicit ordering, databases may return results in different orders each time, making pagination unreliable and potentially causing data to be skipped or duplicated.

Additionally, use compile-time query verification macros like `query!` instead of `query` to catch SQL errors at build time rather than runtime.

Example of problematic pagination:
```rust
// BAD: No ORDER BY clause
let mut stmt = conn.prepare("SELECT id, address, time, tx_hash FROM requests WHERE tx_hash IS NULL LIMIT ?1 OFFSET ?2")?;
```

Example of proper pagination:
```rust
// GOOD: Explicit ordering ensures consistent pagination
let mut stmt = conn.prepare("SELECT id, address, time, tx_hash FROM requests WHERE tx_hash IS NULL ORDER BY id LIMIT ?1 OFFSET ?2")?;

// BETTER: Use compile-time verification
let requests = sqlx::query!(
    "SELECT id, address, time, tx_hash FROM requests WHERE tx_hash IS NULL ORDER BY id LIMIT $1 OFFSET $2",
    limit,
    offset
).fetch_all(pool).await?;
```

For time-based pagination, consider using cursor-based pagination with timestamps instead of OFFSET to handle concurrent insertions more gracefully.